#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r76 补丁 —— 5 项需求，一次生成终态（幂等）。

  1. 全局滚动条 hover 色浅一级          → 9 页内联 + 2 处局部手写 + DS 源（2 css）
  2. base.html 波点涟漪「明显」化        → 画到内容之上 + 换点色/加宽环带/加大半径
  3. 数字分身 main 内容「亮相」微动效     → 叶子块错峰淡入 + 上移 8px
  4. base.html 技能选择浮窗纵向自适应     → max-height 夹到可用空间（纯声明式）
  5. 任务详情收起后会话栏回弹            → 左栏在收起期间出场吸收空间 + 会话栏宽度同步

幂等三要素：NEW 标记命中即 SKIP → OLD 串 count 必须恰为 1（否则 sys.exit）
→ 跑完复跑一次应为「应用: 0 页」。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGES = os.path.join(ROOT, 'pages')
DS = os.path.join(ROOT, 'giencoder-design-system')

PAGE_NAMES = ['automation', 'avatar', 'base', 'dev', 'kanban',
              'req-kanban', 'settings', 'skills', 'task-detail']

TAIL = '</body>'

# ─────────────────────────── 需求 1：滚动条 hover 浅一级 ───────────────────────────
OLD_HOVER_GLOBAL = '::-webkit-scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .24)}'
NEW_HOVER_GLOBAL = '::-webkit-scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .20)}'
OLD_HOVER_TD = '--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.24);'
NEW_HOVER_TD = '--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.20);'
OLD_HOVER_AV = '::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.24); }'
NEW_HOVER_AV = '::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.20); }'
OLD_HOVER_DS = '::-webkit-scrollbar-thumb:hover {\n    background-color: rgba(var(--gray-10), 0.24);\n  }'
NEW_HOVER_DS = '::-webkit-scrollbar-thumb:hover {\n    background-color: rgba(var(--gray-10), 0.20);\n  }'
OLD_VAR_DS = '--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.28);'
NEW_VAR_DS = '--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.20);'

# ─────────────────────────── 需求 2 + 4：base.html 注入块 ───────────────────────────
BASE_CSS = """<style id="r76-base-css">
  /* ★ 第 76 轮 · 需求 2：点击 main 空白处的波点水波纹要「明显」。

     本轮由邵先生拍板：涟漪画在内容之上。此前它在内容之下，而 main 绝大部分面积
     被白色输入卡盖住 ⇒ 只有卡片四周的缝隙能看见，取帧实测 t=160ms 全画幅
     仅 343 个像素发生变化（0.08%），热区窄到看不见。

     元素本身仍由第 74 轮页尾脚本生成（它负责定位变量与播放结束自毁），
     这里只重置绘制，四处一起加强：
       ① 层级：由 0 提到 10。实测 main 内有非 auto 层级的后代只有 1000 / 9999 的弹层，
          故涟漪高于所有常规内容、仍低于弹层；
       ② 点色：灰阶由 gray-8 换到更深一档的 gray-9，不透明度同步微升 ——
          在卡片白底上也要看得清；
       ③ 环带：单薄前缘换成「波峰 + 尾迹」双带，可见带宽由 58px 放到约 106px；
       ④ 半径：上限由 360px 提到 480px（仍在 300ms 内推进 ⇒ 1.6px/ms，
          与原先 1.2px/ms 同量级，波前不会糊成一道闪光）。 */
  .r74-ripple {
    z-index: 10;
    --r76-rip-cap: 480px;
    background-image: radial-gradient(circle, rgba(var(--gray-9), 0.42) 1.5px, transparent 1.5px);
    background-size: 20px 20px;
    -webkit-mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 130px),
        rgba(0, 0, 0, 0.34) calc(var(--r74-rip-r) - 74px),
        transparent calc(var(--r74-rip-r) - 40px),
        #000 calc(var(--r74-rip-r) - 18px),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 16px));
    mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 130px),
        rgba(0, 0, 0, 0.34) calc(var(--r74-rip-r) - 74px),
        transparent calc(var(--r74-rip-r) - 40px),
        #000 calc(var(--r74-rip-r) - 18px),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 16px));
    animation: r76-ripple-out 300ms linear both;
  }
  /* 波前用 linear 推进（缓动会在中段把半径一次推到接近终值，看不出「扩散」），
     分段关键帧只负责「先起、后收」的不透明度包络。 */
  @keyframes r76-ripple-out {
    0% {
      --r74-rip-r: 0px;
      opacity: 0;
    }
    7% {
      opacity: 1;
    }
    55% {
      --r74-rip-r: calc(var(--r76-rip-cap) * 0.62);
      opacity: 0.9;
    }
    100% {
      --r74-rip-r: var(--r76-rip-cap);
      opacity: 0;
    }
  }
  /* 减动画偏好：元素仍要播完并自毁（若直接不渲染，脚本就收不到播放结束事件、
     节点会一直留在 main 里），所以只把时长压到不可感知。 */
  @media (prefers-reduced-motion: reduce) {
    .r74-ripple {
      animation-duration: 1ms;
    }
  }

  /* ★ 第 76 轮 · 需求 4：纵向空间不足时，「技能选择」浮窗不再被裁掉。

     实测（1440 宽 × 560/640/720/800/900 五档，与宽度无关）：
     浮窗按内联规则挂在输入卡正上方，卡顶 = 视口高的一半减去 62px，
     故浮窗可用高 = 卡顶 - 8 - main 顶 = 视口高的一半减去 118px。
     视口高低于约 876 时该值小于 320（浮窗自身的内联高），
     上缘就冲出 main 的顶，被输入卡 / main / 根容器三层裁切
     （实测溢出 77.3px @ 720、157.3px @ 560）。
     修法：只夹 max-height —— 内联规则给的是 height，max-height 天然可压过它；
     被压掉的高度由浮窗内既有的可滚动列表承载。
     纯声明式 ⇒ 窗口缩放自动跟随，不需要脚本，也不与 React 的内联样式打架。 */
  [role="listbox"][aria-label="技能选择"][style*="position: absolute"] {
    max-height: calc(50vh - 120px);
  }
</style>
"""

BASE_TOKENS = ['r76-ripple-out', '--r76-rip-cap', 'rgba(var(--gray-9), 0.42)', 'calc(50vh - 120px)']

# ─────────────────────────── 需求 3：avatar.html 注入块 ───────────────────────────
AV_CSS = """<style id="r76-av-css">
  /* ★ 第 76 轮 · 需求 3：数字分身 main 容器内内容的「亮相」微动效。

     main 里的内容由页尾脚本从模板一次性注入（React 侧只留空壳），
     所以这里写的动画只在首屏渲染那一次播，不会被重渲染打断。

     只给「叶子块」加动画，不碰 .av-main-grid / .av-main-rows 这两个容器 ——
     否则父子的不透明度会相乘、观感发闷。
     错峰按「头部 → 分隔线 → 4 张卡 → 3 行 → 页脚」递进 35~40ms，
     幅度保守（上移 8px + 淡入，260ms），曲线沿用全站既有的那条。 */
  @keyframes r76-av-in {
    from {
      opacity: 0;
      translate: 0 8px;
    }
  }
  .av-main > .av-main-head,
  .av-main > .av-main-rule,
  .av-main > .av-main-grid > *,
  .av-main > .av-main-rows > *,
  .av-main > .av-main-foot {
    animation: r76-av-in 260ms cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  .av-main > .av-main-rule {
    animation-delay: 40ms;
  }
  .av-main > .av-main-grid > :nth-child(1) {
    animation-delay: 80ms;
  }
  .av-main > .av-main-grid > :nth-child(2) {
    animation-delay: 115ms;
  }
  .av-main > .av-main-grid > :nth-child(3) {
    animation-delay: 150ms;
  }
  .av-main > .av-main-grid > :nth-child(4) {
    animation-delay: 185ms;
  }
  .av-main > .av-main-rows > :nth-child(1) {
    animation-delay: 220ms;
  }
  .av-main > .av-main-rows > :nth-child(2) {
    animation-delay: 255ms;
  }
  .av-main > .av-main-rows > :nth-child(3) {
    animation-delay: 290ms;
  }
  .av-main > .av-main-foot {
    animation-delay: 325ms;
  }
  @media (prefers-reduced-motion: reduce) {
    .av-main > .av-main-head,
    .av-main > .av-main-rule,
    .av-main > .av-main-grid > *,
    .av-main > .av-main-rows > *,
    .av-main > .av-main-foot {
      animation: none;
    }
  }
</style>
"""

AV_TOKENS = ['r76-av-in', 'translate: 0 8px', '.av-main > .av-main-rows > :nth-child(3)']

# ─────────────────────────── 需求 5：task-detail.html 注入块 ───────────────────────────
TD_CSS = """<style id="r76-td-css">
  /* ★ 第 76 轮 · 需求 5：任务详情页预览栏收起后，AI 会话栏不再「关完再整体弹一下」。

     改前实测（1440×900；此宽度下左栏不在浏览态保留，即缺 .is-keep-left）：
       · 预览栏 1024→0 走满 200ms（平滑），但左栏这 200ms 里是 display:none，
         腾出的空间无人接收 —— 会话栏一直待在行的最左（8..408，宽 400）；
       · React 摘掉 .is-browse 的那一帧，会话栏 8..408 → 952..1432、
         宽度 400→480、左栏 0→936 三件事一起硬跳，
         而预览栏早已关完 ⇒ 观感就是「关完之后会话栏猛地弹回右边」。
       （第 74 轮修的是 .is-keep-left 那一支：在左栏被保留时让它 flex-grow 吸收空间。
         该分支要求行宽不小于约 1609（≈视口 1625），1920 实测全程单调、无跳变；
         1440 / 1600 这类常见笔记本宽度走的是上面这一支，所以问题仍在。）

     修法：把第 74 轮那套「左栏吸收」推广到不保留左栏的那一支。
       ① 收起期间让左栏以 display:flex + flex:1 1 0px 出场，从 0 长到 936，
          正好吸收预览栏腾出的空间；basis 为 0 ⇒ 起始帧不占位，与改前同一起点；
          右侧补上与拖动条同宽的间距，与普通态里那 8px 对齐，
          使收起结束时的几何与普通态逐位重合（936 + 8 + 480 = 行宽 1424）。
       ② 收起期间把会话栏宽度提前切到普通态值（浏览态是 400、普通态是 480），
          并给宽度补一条同长过渡 ⇒ 这一项也在 200ms 内走完，
          摘类时不再剩下 80px 的宽度硬跳。

     ⚠️ 两条都只在 .is-closing 存在时命中 ⇒ 只影响「收起」，
        展开与拖动路径零改动；减动画偏好下过渡被关掉，退化为瞬时（与全站一致）。 */
  .td-root.is-browse:not(.is-keep-left):has(> .td-browse-slot > .td-browse.is-closing) > .td-left {
    display: flex;
    flex: 1 1 0px;
    min-width: 0;
    max-width: none;
    margin-right: var(--td-gap);
  }
  .td-root.is-browse:has(> .td-browse-slot > .td-browse.is-closing) > .td-right {
    width: var(--td-right-w);
    transition: outline-color 140ms var(--transition-timing-function-standard),
                box-shadow 180ms var(--transition-timing-function-standard),
                width 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1)),
                border-right-width 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1)),
                border-top-right-radius 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1)),
                border-bottom-right-radius 200ms var(--td-browse-ease, cubic-bezier(0.22, 1, 0.36, 1));
  }
  @media (prefers-reduced-motion: reduce) {
    .td-right {
      transition: none;
    }
  }
</style>
"""

TD_TOKENS = ['r76-td-css', 'is-browse:not(.is-keep-left)', 'margin-right: var(--td-gap);']

REPORT = []


def replace_once(s, old, new, label):
    """精确替换一次；已替换过则跳过；锚点缺失/不唯一即中断。"""
    n = s.count(old)
    if n == 0:
        if s.count(new):
            REPORT.append(('skip', label, '已应用'))
            return s, False
        sys.exit('!! 锚点缺失：%s' % label)
    if n != 1:
        sys.exit('!! 锚点不唯一：%s 出现 %d 次' % (label, n))
    REPORT.append(('ok', label, '1 处'))
    return s.replace(old, new), True


def inject_before_body(path, mark, css, deps, tokens):
    s = io.open(path, encoding='utf-8').read()
    name = os.path.basename(path)
    if mark in s:
        REPORT.append(('skip', name + ' 注入块', '已存在'))
        return
    if s.count(TAIL) != 1:
        sys.exit('!! %s 的 </body> 出现 %d 次' % (name, s.count(TAIL)))
    for dep, want in deps:
        if s.count(dep) != want:
            sys.exit('!! %s 前置依赖异常：%s 出现 %d 次（期望 %d）' % (name, dep, s.count(dep), want))

    b_style, b_estyle = s.count('<style'), s.count('</style>')
    b_script, b_escript = s.count('<script'), s.count('</script>')

    i = s.rindex(TAIL)
    s2 = s[:i] + css + s[i:]

    checks = [
        ('<style> 增量', s2.count('<style') - b_style, 1),
        ('</style> 增量', s2.count('</style>') - b_estyle, 1),
        ('<script> 增量（应为 0）', s2.count('<script') - b_script, 0),
        ('</script> 增量（应为 0）', s2.count('</script>') - b_escript, 0),
        (mark, s2.count(mark), 1),
    ]
    for tok in tokens:
        checks.append((tok + ' 增量', s2.count(tok) - s.count(tok), css.count(tok)))
    for nm, got, want in checks:
        if got != want:
            sys.exit('!! 自检失败 [%s] %s: 实得 %s（期望 %s）' % (name, nm, got, want))
        REPORT.append(('ok', '%s · %s' % (name, nm), str(got)))

    io.open(path, 'w', encoding='utf-8').write(s2)


def main():
    # ── 需求 1：9 页内联全局 hover ──
    for nm in PAGE_NAMES:
        p = os.path.join(PAGES, nm + '.html')
        s = io.open(p, encoding='utf-8').read()
        s, changed = replace_once(s, OLD_HOVER_GLOBAL, NEW_HOVER_GLOBAL, nm + ' 全局 hover')
        if changed:
            io.open(p, 'w', encoding='utf-8').write(s)

    # ── 需求 1：两处局部手写档 ──
    for nm, old, new, label in (
        ('task-detail', OLD_HOVER_TD, NEW_HOVER_TD, 'task-detail 局部变量 hover'),
        ('avatar', OLD_HOVER_AV, NEW_HOVER_AV, 'avatar 卡内滚动条 hover'),
    ):
        p = os.path.join(PAGES, nm + '.html')
        s = io.open(p, encoding='utf-8').read()
        s, changed = replace_once(s, old, new, label)
        if changed:
            io.open(p, 'w', encoding='utf-8').write(s)

    # ── 需求 1：DS 源（权威值，与页面同步）──
    p = os.path.join(DS, 'colors_and_type.css')
    s = io.open(p, encoding='utf-8').read()
    s, c1 = replace_once(s, OLD_HOVER_DS, NEW_HOVER_DS, 'DS colors_and_type 滚动条 hover')
    s, c2 = replace_once(s, OLD_VAR_DS, NEW_VAR_DS, 'DS colors_and_type 局部变量 hover')
    if c1 or c2:
        io.open(p, 'w', encoding='utf-8').write(s)

    p = os.path.join(DS, 'gienx-templates', '_shared', 'tokens.css')
    s = io.open(p, encoding='utf-8').read()
    s, changed = replace_once(s, OLD_HOVER_DS, NEW_HOVER_DS, 'DS tokens.css 滚动条 hover')
    if changed:
        io.open(p, 'w', encoding='utf-8').write(s)

    # ── 需求 2 + 4：base.html ──
    inject_before_body(
        os.path.join(PAGES, 'base.html'),
        '<style id="r76-base-css">', BASE_CSS,
        deps=[('<style id="r74-base-css">', 1), ('<script id="r74-base-js">', 1),
              ('<style id="r75-base-css">', 1), ('@keyframes r74-pop-in', 1)],
        tokens=BASE_TOKENS)

    # ── 需求 3：avatar.html ──
    inject_before_body(
        os.path.join(PAGES, 'avatar.html'),
        '<style id="r76-av-css">', AV_CSS,
        deps=[('id="av-main-tpl"', 1), ('<style id="av-main-css">', 1)],
        tokens=AV_TOKENS)

    # ── 需求 5：task-detail.html ──
    inject_before_body(
        os.path.join(PAGES, 'task-detail.html'),
        '<style id="r76-td-css">', TD_CSS,
        deps=[('<style id="r74-td-css">', 1),
              ('is-browse:has(> .td-browse-slot > .td-browse.is-closing)', 1)],
        tokens=TD_TOKENS)

    ok = sum(1 for k, _, _ in REPORT if k == 'ok')
    sk = sum(1 for k, _, _ in REPORT if k == 'skip')
    for k, label, val in REPORT:
        print('  %-5s %-56s %s' % (k, label, val))
    print('应用: %d 处 | 跳过: %d 处' % (ok, sk))


if __name__ == '__main__':
    main()
