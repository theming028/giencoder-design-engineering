#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r74 补丁 C —— avatar.html       （需求 3 对话框按钮态切换 + 需求 4 头像 hover 摇晃）
   r74 补丁 D —— task-detail.html （需求 8 预览栏进/出与左栏、AI 栏同步缓动）

幂等：NEW 标记命中即 SKIP；跑完复跑应得「应用 0 页」。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGES = os.path.join(ROOT, 'pages')
TAIL = '</body>'

# ============================================================ C · avatar（需求 3、4）
AV_MARK_CSS = '<style id="r74-av-css">'
AV_MARK_JS = '<script id="r74-av-js">'

AV_CSS = """<style id="r74-av-css">
  /* ★ 第 74 轮 · 需求 4：鼠标移到数字分身头像上 → 里面的脸摇晃几下（调皮感）。
     ⚠️ 摇晃的是「脸里的字形」而不是「脸那个盒子」—— 盒子带浅灰底 + 圆角，
        整体倾斜会把底一起扭过去（像卡片歪了），不是摇头。字形由本页脚本包一层
        .r74-face-glyph 提供（主内容是 <template> 克隆出来的，观察器兜住后置插入）。
     ⚠️ 用 rotate 独立属性而非 transform：与字形上将来可能出现的 transform 天然复合、互不覆盖。
     轴心压到 78% 高度（接近下巴）⇒ 是「摇头」而不是「绕中心打转」。
     ⚠️ 时长 300ms 是 craft.md 的硬上限（UI 动画 ≤ 300ms）：300ms 内摆 3 个峰
       （-9° / +8° / -5°），约 5 次/秒 —— 落成「快速摇几下」而不是糊成一片抖动。
       想要更慢更"黏"的摇晃就得突破 300ms，会把 verify-design.py 的 CRAFT-ANIM 打红。 */
  @keyframes r74-face-wiggle {
    0%, 100% { rotate: 0deg; }
    18% { rotate: -9deg; }
    48% { rotate: 8deg; }
    78% { rotate: -5deg; }
  }
  .av-main-avatar:hover .r74-face-glyph {
    transform-origin: 50% 78%;
    animation: r74-face-wiggle 300ms cubic-bezier(0.36, 0.07, 0.19, 0.97) 1;
  }

  /* ★ 第 74 轮 · 需求 3：AI 对话侧栏打开后，触发器文案换成「关闭对话窗口」、图标换成 X，
     且 X 进场时自转一圈吸引注意。
     动画只挂在 data-r74-state="on" 上 —— X 那个 <svg> 是本页脚本在状态切换时新建的节点，
     挂载即匹配规则 ⇒ 天然只在「变 X」那一次播一遍；状态不变不会重播。
     300ms 转满 360°，末尾用 bezier(0.34,1.3,…) 过冲到 ≈368° 再回落 —— 一圈之外带一点回弹。 */
  @keyframes r74-x-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  [data-av-chat-toggle][data-r74-state="on"] > svg {
    transform-origin: 50% 50%;
    animation: r74-x-spin 300ms cubic-bezier(0.34, 1.3, 0.64, 1);
  }
</style>
"""

AV_JS = """<script id="r74-av-js">
/* ==========================================================================
   第 74 轮 · avatar.html 页尾脚本（勿手改此块）
   需求 3：AI 对话侧栏「开」→ 触发器文案变「关闭对话窗口」、图标变 X（并自转一圈）；
           「关」→ 还原成「通过对话完善数字分身」+ 对话气泡。
   ⚠️ 不改页面原有的 openChat / closeChat / syncTriggers（它们在 IIFE 里，外部摸不到），
      改为监听 <html data-av-chat-open> 的属性变化 + 观察 body 子树
      （主内容来自 <template> 克隆，克隆时机晚于本脚本，必须由观察器兜住）。
   需求 4：给头像脸里那枚字形包一层 .r74-face-glyph，让 CSS 只旋转字形、不扭动脸的盒子。
   ========================================================================== */
(function () {
  'use strict';
  var LABEL_ON = '\\u5173\\u95ed\\u5bf9\\u8bdd\\u7a97\\u53e3';                        /* 关闭对话窗口 */
  var LABEL_OFF = '\\u901a\\u8fc7\\u5bf9\\u8bdd\\u5b8c\\u5584\\u6570\\u5b57\\u5206\\u8eab'; /* 通过对话完善数字分身 */
  var X_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"'
    + ' fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    + ' class="size-3.5" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
  var CHAT_SVG = null;      /* 关闭态下的原图标（对话气泡），开合来回都靠它还原 */
  var root = document.documentElement;

  function remember() {
    if (CHAT_SVG) return;
    var s = document.querySelector('[data-av-chat-toggle] > svg');
    if (s) CHAT_SVG = s.outerHTML;
  }

  /* ---------- 需求 3：触发器文案 + 图标 ---------- */
  function syncTrigger() {
    remember();
    var open = root.hasAttribute('data-av-chat-open');
    var key = open ? 'on' : 'off';
    var btns = document.querySelectorAll('[data-av-chat-toggle]');
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i];
      if (b.getAttribute('data-r74-state') === key) continue;
      var svg = b.querySelector('svg');
      var want = open ? X_SVG : CHAT_SVG;
      if (svg && want && svg.outerHTML !== want) {
        svg.insertAdjacentHTML('afterend', want);
        svg.parentNode.removeChild(svg);
      }
      var nodes = b.childNodes;
      for (var j = 0; j < nodes.length; j++) {
        var n = nodes[j];
        if (n.nodeType === 3 && n.nodeValue.replace(/\\s/g, '')) {
          n.nodeValue = open ? LABEL_ON : LABEL_OFF;
        }
      }
      b.setAttribute('data-r74-state', key);
    }
  }

  /* ---------- 需求 4：字形包一层，供 CSS 单独旋转 ---------- */
  function wrapFace() {
    var faces = document.querySelectorAll('.av-main-avatar-face');
    for (var i = 0; i < faces.length; i++) {
      var f = faces[i];
      var first = f.firstElementChild;
      if (first && first.className === 'r74-face-glyph') continue;
      var g = document.createElement('span');
      g.className = 'r74-face-glyph';
      while (f.firstChild) g.appendChild(f.firstChild);
      f.appendChild(g);
    }
  }

  /* ---------- 驱动：属性变化 + 子树变化，rAF 合并（自收敛：状态一致就不再写 DOM） ---------- */
  var queued = false;
  function pump() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; wrapFace(); syncTrigger(); });
  }
  new MutationObserver(pump).observe(root, { attributes: true, attributeFilter: ['data-av-chat-open'] });
  new MutationObserver(pump).observe(document.body, { childList: true, subtree: true });
  pump();
  /* 兜底：克隆时机若比首帧更晚，前 3 秒每 150ms 补一次（幂等，命中即空转） */
  var n = 0, t = setInterval(function () { pump(); if (++n > 20) clearInterval(t); }, 150);
})();
</script>
"""

# ============================================================ D · task-detail（需求 8）
TD_MARK = '<style id="r74-td-css">'

TD_CSS = """<style id="r74-td-css">
  /* ★ 第 74 轮 · 需求 8：任务详情页「文件预览栏」的进 / 出，与左栏、AI 会话栏做成一套同步动效。
     ── 改前实测（1920×1080，rAF 逐帧采样 .td-root 各子项宽度）──
       · 展开：t=0 slot=0 → t≈9ms slot=816。一帧内到位。真因不是「过渡没建」——冻结帧里
         flex-basis 的 CSS 过渡确实存在，是**左栏在同一帧被钳死在 600**，于是预览栏的可用余量
         当帧就是 816，它的实用宽被余量顶死 ⇒ 过渡出来的 basis 全被裁掉，看着像瞬变。
         同一帧里 AI 会话栏右缘圆角 8→0 / 右描边 1→0 也是瞬变。
       · 收起：slot 816→0 走满 200ms（平滑），但左栏全程钉在 600 —— 腾出的 816px 无人接收，
         成了 AI 会话栏右侧的一片空白；直到 t≈245ms React 摘掉 .is-browse / .is-keep-left，
         左栏 600→1416、圆角 0→8、描边 0→1 三件事一起硬跳。
         观感 =「预览栏自己关完，别的东西再一起跳」⇒ 用户说的各关各的。
     ── 改法：一进一出同一条 200ms 曲线 ──
       关键事实：.td-browse-slot 的**实用宽**不由它自己的 flex-basis 决定，而是
       「行宽 − 左栏 − 8px − AI 会话栏」的余量（它的 basis 恒大于余量 ⇒ 永远被压到余量）。
       因此只要驱动**左栏**宽度，预览栏的长短与 AI 会话栏的位置就自动同帧跟随，无需各自补动画。
       ⚠️ 左栏在浏览态被 min-width / max-width 双双钳死在 600px，必须先放开夹子，否则
          flex-basis 动画会被 max-width 截断成常数（这是本改动唯一的硬前提）。 */

  /* ① 展开：左栏从「普通态的整行宽」收窄到 600px，预览栏随之从 0 长到 816px。
        from 用普通态公式反推（普通态：左栏 = 行宽 − 8px 拖动条 − AI 会话栏宽），
        不写死 1416 —— 右栏被拖动过时同样成立；to 取元素自身计算值（keep-left 的 basis）。 */
  @keyframes r74-left-fold {
    from { flex-basis: calc(100% - var(--td-gap, 8px) - var(--td-right-w, 480px)); }
  }
  .td-root.is-browse.is-keep-left .td-left {
    min-width: 0;
    max-width: none;
    animation: r74-left-fold 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1));
  }

  /* ② 收起：左栏换成「可伸」的同宽 basis —— 预览栏每缩 1px，左栏就长 1px，
        腾出的空间被左栏当场吸收，AI 会话栏不再被撇在原地、右端也不留空白。
        basis 仍是 --td-left-keep-w（600）⇒ 起始帧零位移（与改前同一起点）；
        t≈195ms 时恰好长到 1416，与 .is-browse 被摘掉后的普通态宽度重合 ⇒ 也不会二次跳变。
        flex-shrink 置 0：保证起始帧的收缩由预览栏独家承担。 */
  .td-root.is-browse.is-keep-left:has(> .td-browse-slot > .td-browse.is-closing) .td-left {
    flex-grow: 1;
    flex-shrink: 0;
  }

  /* ③ AI 会话栏的右缘：浏览态是「与预览栏拼成一条缝」（直角 + 无右描边），
        普通态是「独立圆角卡片」（圆角 8 + 1px 描边）。改前这一步在 t≈245ms 硬跳。
        这里把「还原」的触发点提前到 is-closing 出现的那一帧，与预览栏同起同落。
        ⚠️ 两个端点都写成 border 简写：页面原规则的 `border-right: 0` 会把 border-style
           重置成 none，那样 border-width 0↔1px 插值出来也不可见。 */
  .td-root.is-browse .td-right {
    border-right: 0px solid var(--td-panel-line);
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
  .td-root.is-browse:has(> .td-browse-slot > .td-browse.is-closing) .td-right {
    border-right: 1px solid var(--td-panel-line);
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
  }

  /* ④ 过渡表：必须把页面原有那条（outline-color / box-shadow）一并重述 ——
        transition 是整条覆盖不是合并，漏写就会把拖动提示态的两条过渡弄丢。 */
  .td-left {
    transition: outline-color 140ms var(--transition-timing-function-standard),
                box-shadow 180ms var(--transition-timing-function-standard);
  }
  .td-right {
    transition: outline-color 140ms var(--transition-timing-function-standard),
                box-shadow 180ms var(--transition-timing-function-standard),
                border-right-width 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1)),
                border-top-right-radius 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1)),
                border-bottom-right-radius 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1));
  }

  /* ⑤ 减动画偏好：本块的 transition 是后注入的，会盖掉页面原有的 reduce 兜底，必须自己补一条。 */
  @media (prefers-reduced-motion: reduce) {
    .td-root.is-browse.is-keep-left .td-left { animation: none; }
    .td-left,
    .td-right { transition: none; }
  }
</style>
"""

# 变更对象精确计数：token -> 注入块「去注释后」应出现的真实代码次数
# （注释里出现同一个 token 不算证据，故计数前先剥注释；另同时校验文件级增量 == 块原始次数）
AV_TOKENS = {'r74-av-css': 1, 'r74-av-js': 1, 'r74-face-wiggle': 2, 'r74-x-spin': 2,
             'r74-face-glyph': 3, 'data-r74-state': 3, 'data-av-chat-toggle': 3}
TD_TOKENS = {'r74-td-css': 1, 'r74-left-fold': 2, 'is-closing)': 2, 'flex-grow: 1': 1,
             'border-top-right-radius 200ms': 1}


def code_only(block):
    """剥掉 CSS /* */ 与行首 // 注释，只留可执行部分。"""
    block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
    return re.sub(r'(?m)^\s*//.*$', '', block)


def inject_raw(s, block):
    if s.count(TAIL) != 1:
        sys.exit('!! </body> 出现 %d 次（要求恰好 1）' % s.count(TAIL))
    i = s.rindex(TAIL)
    return s[:i] + block + s[i:]


def report(label, s, s2, block, tokens):
    """① 标签级增量；② 被改对象增量；③ 被改对象在块内确有可执行代码（非仅注释）。"""
    code = code_only(block)
    pairs = [('<style>', s2.count('<style') - s.count('<style'), block.count('<style')),
             ('</style>', s2.count('</style>') - s.count('</style>'), block.count('</style>')),
             ('<script>', s2.count('<script') - s.count('<script'), block.count('<script')),
             ('</script>', s2.count('</script>') - s.count('</script'), block.count('</script>'))]
    for name, got, want in pairs:
        if got != want:
            sys.exit('!! %s 自检失败 %-32s 增量 %s ≠ 注入块自带 %s' % (label, name, got, want))
        print('  ok  %-6s %-34s Δ=%-3s' % (label, name, got))
    for name, want in tokens.items():
        got = s2.count(name) - s.count(name)
        if got != block.count(name):
            sys.exit('!! %s 自检失败 %-32s 文件增量 %s ≠ 块原始次数 %s'
                     % (label, name, got, block.count(name)))
        if code.count(name) != want:
            sys.exit('!! %s 自检失败 %-32s 块内可执行代码 %s 处（期望 %s）'
                     % (label, name, code.count(name), want))
        print('  ok  %-6s %-34s Δ=%-3s 代码内=%s' % (label, name, got, want))


def main():
    n = 0

    # ---------- C · avatar：CSS + JS 一次注入 ----------
    av = os.path.join(PAGES, 'avatar.html')
    s = io.open(av, encoding='utf-8').read()
    if AV_MARK_CSS in s:
        print('  SKIP  avatar.html         已含 r74 标记')
    else:
        s2 = inject_raw(s, AV_CSS + AV_JS)
        report('avatar', s, s2, AV_CSS + AV_JS, AV_TOKENS)
        io.open(av, 'w', encoding='utf-8').write(s2)
        print('  OK    avatar.html')
        n += 1

    # ---------- D · task-detail：纯 CSS ----------
    td = os.path.join(PAGES, 'task-detail.html')
    s = io.open(td, encoding='utf-8').read()
    if TD_MARK in s:
        print('  SKIP  task-detail.html    已含 r74 标记')
    else:
        s2 = inject_raw(s, TD_CSS)
        report('td', s, s2, TD_CSS, TD_TOKENS)
        io.open(td, 'w', encoding='utf-8').write(s2)
        print('  OK    task-detail.html')
        n += 1

    print('应用: %d 页' % n)


if __name__ == '__main__':
    main()
