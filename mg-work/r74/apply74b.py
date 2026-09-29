#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r74 补丁 B —— base.html：需求 2（版权区三行）+ 需求 5（波点水波纹涟漪）+ 需求 7（浮窗进/退场微动效）。

幂等：NEW 标记命中即 SKIP；锚点 count 必须为 1；跑完复跑应得「应用 0 页」。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'base.html')

MARK_STYLE = '<style id="r74-base-css">'
MARK_SCRIPT = '<script id="r74-base-js">'
TAIL = '</body>'

CSS = """<style id="r74-base-css">
  /* ★ 第 74 轮 · 需求 7：基础工作台的浮窗补「显示 / 关闭」微动效，
     参数与研发工作台（第 73 轮那套 r73-pop-in）完全对齐：
       进场 = 淡入 + 下移 4px 复位 + 0.97 微缩放，160ms cubic-bezier(0.34, 0.69, 0.1, 1)
       退场 = 同一组值的反向（由页尾脚本克隆节点播放） */
  @keyframes r74-pop-in {
    from {
      opacity: 0;
      translate: 0 4px;
      scale: 0.97;
    }
  }
  /* ① 顶栏「切换空间」下拉：React 条件渲染、挂在 body 下、无类名，
        只能按内联样式特征选（position:fixed + z-index:1000）。 */
  body > div[style*="position: fixed"][style*="z-index: 1000"] {
    animation: r74-pop-in 160ms cubic-bezier(0.34, 0.69, 0.1, 1) both;
  }
  /* ② 会话项操作菜单（createPortal 挂 body） */
  [role="menu"][aria-label="会话操作"] {
    animation: r74-pop-in 160ms cubic-bezier(0.34, 0.69, 0.1, 1) both;
  }
  /* ③ 输入框左侧「+」的添加菜单 /「技能选择」面板：
        这两个容器常驻 DOM、靠 React 在 style 上有无定位来开关 ——
        用属性选择器让「拿到定位的那一刻」才匹配 ⇒ 进场动画自然起跑。 */
  [role="menu"][aria-label="添加内容"][style*="position: absolute"],
  [role="listbox"][aria-label="技能选择"][style*="position: absolute"] {
    animation: r74-pop-in 160ms cubic-bezier(0.34, 0.69, 0.1, 1) both;
  }

  /* ★ 第 74 轮 · 需求 5：点击 main 空白处 → 波点泛起一圈浅水波纹。
     涟漪 = 再叠一层点阵，用环形 mask 只让「波前」那一圈露出来；
     波前半径 --r74-rip-r 由 @property 注册成 <length> 才能被动画插值。
     元素插在 main 最前 → 与 ::before 同处内容之下，不遮任何正文。
     · 半径上限固定 360px（= 一滴水落在水面上的涟漪尺度），不做「扫到最远角」：
       ① 「浅浅的」本就不该把整页点亮；② craft.md 要求 UI 动画 ≤ 300ms，
       360px / 300ms = 1.2px/ms —— 与原先「扫全页」的波前速度同量级，波前不会糊成一道闪光。 */
  @property --r74-rip-r {
    syntax: '<length>';
    inherits: false;
    initial-value: 0px;
  }
  .r74-ripple {
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image: radial-gradient(circle, rgba(var(--gray-8), 0.42) 1.5px, transparent 1.5px);
    background-size: 20px 20px;
    -webkit-mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 44px),
        #000 calc(var(--r74-rip-r) - 14px),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 14px));
    mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 44px),
        #000 calc(var(--r74-rip-r) - 14px),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 14px));
    /* ⚠️ 缓动必须用 linear + 分段关键帧：试过 cubic-bezier(0.22,1,0.36,1)，
       它在 36% 进度处就把半径推到 95% ⇒ 波前"唰"地一下到边，看不出扩散。 */
    animation: r74-ripple-out 300ms linear forwards;
  }
  @keyframes r74-ripple-out {
    0% {
      --r74-rip-r: 0px;
      opacity: 0;
    }
    8% {
      opacity: 0.95;
    }
    55% {
      --r74-rip-r: calc(var(--r74-rip-cap, 360px) * 0.62);
      opacity: 0.8;
    }
    100% {
      --r74-rip-r: var(--r74-rip-cap, 360px);
      opacity: 0;
    }
  }
</style>
"""

JS = """<script id="r74-base-js">
/* ==========================================================================
   第 74 轮 · base.html 页尾脚本（勿手改此块）
     ① 需求 2 —— 版权区拆成「© 2026 中电金信」+「中电金信研究院 · … · 版本：1.2.5」两行
     ② 需求 5 —— 点击 main 空白处生成一圈水波纹
     ③ 需求 7 —— 浮窗退场：React 条件卸载是把节点直接摘掉，CSS 追不上，
                 故在点击（捕获段，早于 React）先给当前可见浮窗拍快照，
                 节点真消失时用快照克隆一份 ghost 播退场，160ms 后自行销毁。
   ========================================================================== */
(function () {
  'use strict';

  /* ---------------- ① 需求 2：版权区 ---------------- */
  (function () {
    var L1 = '\\u00a9 2026 \\u4e2d\\u7535\\u91d1\\u4fe1';
    var L2 = '\\u4e2d\\u7535\\u91d1\\u4fe1\\u7814\\u7a76\\u9662 \\u00b7 \\u6570\\u5b57\\u6784\\u5efa\\u5e73\\u53f0\\u5b9e\\u9a8c\\u5ba4\\uff08PAA\\uff09 \\u00b7 \\u7248\\u672c\\uff1a1.2.5';
    function run() {
      var host = document.querySelector('main div[class*="pb-6"][class*="text-center"]');
      if (!host) return false;
      var ps = host.querySelectorAll('p');
      if (ps.length < 2) return false;
      var last = ps[ps.length - 1];
      if (last.getAttribute('data-r74-cr') === '1') return true;
      last.textContent = L1;
      last.setAttribute('data-r74-cr', '1');
      var p3 = document.createElement('p');
      p3.setAttribute('data-r74-cr', '1');
      p3.textContent = L2;
      host.appendChild(p3);
      return true;
    }
    var n = 0, t = setInterval(function () { n++; if (run() || n > 60) clearInterval(t); }, 100);
  })();

  /* ---------------- ② 需求 5：波点水波纹 ---------------- */
  (function () {
    var bound = false;
    function arm() {
      if (bound) return true;
      var host = document.querySelector('main.dot-bg');
      if (!host) return false;
      bound = true;
      document.addEventListener('pointerdown', function (e) {
        var t = e.target;
        if (!t || !t.closest) return;
        if (!t.closest('main.dot-bg')) return;
        /* 「空白处」= 不在可交互控件上 */
        if (t.closest('button, a, input, textarea, select, label, [role="button"], [role="tab"], [contenteditable="true"]')) return;
        var r = host.getBoundingClientRect();
        if (!r.width || !r.height) return;
        var x = (e.clientX - r.left) / r.width * 100;
        var y = (e.clientY - r.top) / r.height * 100;
        var el = document.createElement('span');
        el.className = 'r74-ripple';
        el.setAttribute('aria-hidden', 'true');
        el.style.setProperty('--r74-rip-x', x.toFixed(2) + '%');
        el.style.setProperty('--r74-rip-y', y.toFixed(2) + '%');
        /* 固定 360px（水珠涟漪尺度）；不再按「到最远角」算 —— 理由见 CSS 段注释 */
        el.style.setProperty('--r74-rip-cap', '360px');
        el.addEventListener('animationend', function () { if (el.parentNode) el.parentNode.removeChild(el); });
        host.insertBefore(el, host.firstChild);
      }, true);
      return true;
    }
    var n = 0, t = setInterval(function () { n++; if (arm() || n > 60) clearInterval(t); }, 100);
  })();

  /* ---------------- ③ 需求 7：浮窗退场 ghost ---------------- */
  (function () {
    var DUR = 160;
    var EASE = 'cubic-bezier(0.34, 0.69, 0.1, 1)';
    var SEL = 'body > div[style*="position: fixed"], [role="menu"], [role="listbox"]';
    var SNAP = new Map();
    var mo = null;

    function live(el) {
      if (!el || el.nodeType !== 1 || !el.isConnected) return false;
      if (el.getAttribute('data-r74-ghost') === '1') return false;
      var cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') return false;
      if (parseFloat(cs.opacity) < 0.05) return false;
      var r = el.getBoundingClientRect();
      return r.width > 12 && r.height > 12;
    }

    function snap() {
      var list = document.querySelectorAll(SEL), i, el, r;
      for (i = 0; i < list.length; i++) {
        el = list[i];
        if (SNAP.has(el) || !live(el)) continue;
        r = el.getBoundingClientRect();
        SNAP.set(el, {
          html: el.outerHTML,
          x: r.left, y: r.top,
          /* 用 offsetWidth/Height 而不是 rect：进场动画带 scale(.97) 时 rect 会缩水 */
          w: el.offsetWidth || r.width, h: el.offsetHeight || r.height,
          z: getComputedStyle(el).zIndex
        });
      }
      SNAP.forEach(function (v, k) { if (!k.isConnected) SNAP.delete(k); });
      if (SNAP.size && !mo) start();
    }

    function start() {
      if (mo) return;
      mo = new MutationObserver(function (muts) {
        var i, j, m;
        for (i = 0; i < muts.length; i++) {
          m = muts[i];
          if (m.type === 'childList') {
            for (j = 0; j < m.removedNodes.length; j++) {
              if (m.removedNodes[j].nodeType === 1) fire(m.removedNodes[j]);
            }
          } else if (m.attributeName === 'style') {
            fire(m.target);
          }
        }
        if (!SNAP.size) stop();
      });
      mo.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['style'] });
    }

    function stop() {
      if (!mo) return;
      mo.disconnect();
      mo = null;
    }

    function fire(el) {
      var rec = SNAP.get(el);
      if (!rec) return;
      SNAP.delete(el);
      var g = document.createElement('div');
      g.setAttribute('data-r74-ghost', '1');
      g.setAttribute('aria-hidden', 'true');
      g.style.cssText = 'position:fixed;left:' + rec.x + 'px;top:' + rec.y + 'px;width:' + rec.w +
        'px;height:' + rec.h + 'px;z-index:' + (parseInt(rec.z, 10) || 1000) +
        ';pointer-events:none;overflow:hidden;';
      g.innerHTML = rec.html;
      (function strip(node) {
        if (node.nodeType !== 1) return;
        if (node.hasAttribute && node.hasAttribute('id')) node.removeAttribute('id');
        var kids = node.children || [];
        for (var i = 0; i < kids.length; i++) strip(kids[i]);
      })(g);
      document.body.appendChild(g);
      var done = function () { if (g.parentNode) g.parentNode.removeChild(g); };
      try {
        var anim = g.animate(
          [{ opacity: 1, transform: 'translateY(0) scale(1)' },
           { opacity: 0, transform: 'translateY(4px) scale(0.97)' }],
          { duration: DUR, easing: EASE, fill: 'forwards' }
        );
        if (anim && anim.finished) anim.finished.then(done, done);
        else setTimeout(done, DUR + 60);
      } catch (err) {
        done();
      }
    }

    document.addEventListener('click', snap, true);
    document.addEventListener('keydown', snap, true);
  })();
})();
</script>
"""


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    if MARK_STYLE in s or MARK_SCRIPT in s:
        print('  SKIP  base.html 已含 r74 标记')
        print('应用: 0 页 | 跳过: 1 页')
        return

    if s.count(TAIL) != 1:
        sys.exit('!! 锚点异常：</body> 出现 %d 次' % s.count(TAIL))

    before_style = s.count('<style')
    before_script = s.count('<script')

    i = s.rindex(TAIL)
    s2 = s[:i] + CSS + JS + s[i:]

    checks = [
        ('<style> 增量', s2.count('<style') - before_style, 1),
        ('</style> 增量', s2.count('</style>') - s.count('</style>'), 1),
        ('<script> 增量', s2.count('<script') - before_script, 1),
        ('</script> 增量', s2.count('</script>') - s.count('</script>'), 1),
        (MARK_STYLE, s2.count(MARK_STYLE), 1),
        (MARK_SCRIPT, s2.count(MARK_SCRIPT), 1),
        ('r74-ripple', s2.count('r74-ripple'), 4),
        ('r74-pop-in', s2.count('r74-pop-in'), 4),
        ('r74-ripple-out', s2.count('r74-ripple-out'), 2),
        ('data-r74-cr', s2.count('data-r74-cr'), 3),
    ]
    for name, got, want in checks:
        if got != want:
            sys.exit('!! 自检失败 %s: 实得 %s（期望 %s）' % (name, got, want))
        print('  ok  %-24s = %s' % (name, got))

    io.open(PAGE, 'w', encoding='utf-8').write(s2)
    print('应用: 1 页 | 跳过: 0 页')


if __name__ == '__main__':
    main()
