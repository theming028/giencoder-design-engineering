# -*- coding: utf-8 -*-
u"""r107 第十拍补丁：三枚 `.td-rv-menu` 从「钉在面板 top:42px」改为「按触发器现场摆位」。

改序（只能下→上）：part107/panel.css + part107/panel.js → 重跑 apply107.py 落页面。
幂等：跑两遍，第二遍应为「跳过」（判据 = 哨兵串 r107-k1 / r107-k2 已存在）。
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CSS = os.path.join(REPO, 'mg-work', 'r107', 'part107', 'panel.css')
JS = os.path.join(REPO, 'mg-work', 'r107', 'part107', 'panel.js')

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def edit(t, old, new, label, mark):
    if mark in t:
        SKIPPED.append(label)
        return t
    c = t.count(old)
    if c != 1:
        sys.exit(u'!! %s：锚点命中 %d 次（应 1）' % (label, c))
    APPLIED.append(label)
    return t.replace(old, new, 1)


# ============================================================ 1. CSS
CSS_OLD = u"""/* 四枚下拉：定位参照是 `.td-browse`（有 position: relative），不是各自的父元素 ——
   `.td-rv-opts` 挂在**审查模块自己的工具条**里，若以工具条为包含块会被 `.td-mod{overflow:hidden}` 裁掉。
   四枚同用 `top: 42px`（= 标签栏 44px 下方）。右键菜单（`.td-ctxmenu`）改 `position: fixed` 跟随指针。 */
.td-mod-menu.giencoder-dropdown-popup,
.td-rv-menu.giencoder-dropdown-popup { position: absolute; top: 42px; z-index: 30; }
.td-ctxmenu.giencoder-dropdown-popup { position: fixed; top: 0; left: 0; z-index: 60; }
.td-mod-menu { left: 64px; right: auto; }
.td-rv-scope-menu { left: 8px; right: auto; }
.td-rv-opts, .td-commit-menu { right: 8px; left: auto; }
"""

CSS_NEW = u"""/* r107-k1
   四枚下拉：定位参照是 `.td-browse`（有 position: relative），不是各自的父元素 ——
   `.td-rv-opts` 挂在**审查模块自己的工具条**里，若以工具条为包含块会被 `.td-mod{overflow:hidden}` 裁掉。
   右键菜单（`.td-ctxmenu`）走 `position: fixed` 跟随指针，不在此列。
   `.td-mod-menu` 的触发器（`+`）就在标签栏里 ⇒ `top: 42px`（= 标签栏 44px 下方）天然是「按钮下方」，不动。
   ★★ 第十拍（真 bug）：另外三枚 `.td-rv-menu`（对比范围 / 显示选项 / 提交·推送）的触发器
   **全在审查模块的工具条**（`.td-mod-bar`）里 —— 它们共用同一条 `top: 42px` ⇒ 菜单跑到
   **触发按钮上方**去了。1440 实测 dy（菜单 top − 触发器 bottom）= **−35.0 / −34.0 / −36.0**。
   ⇒ 这三枚改由 panel.js 的 `placeRv()` 在**打开的瞬间**按触发器实际几何现场摆位：
      垂直 = 触发器下方 6px（与 `.td-mod-menu` 的实测 gap 6.5 同口径）；
      水平 = 锚定触发器左缘，右侧放不下就向左收贴住面板右内边。
   ⇒ 下面的 `top` 只是 **JS 未生效时的兜底**（默认字号下的静态近似值），真位置由行内样式接管。
   ⚠ 不能改用「包含块换成 `.td-mod-bar` + `top: 100%`」的纯 CSS 写法：祖先 `.td-mod{overflow:hidden}`
     会把菜单裁掉（这是当年改用 `.td-browse` 当参照的原因，见上）。
   ⚠ 也不能改写成静态 `calc(44px + 40px * var(--ui-fs-ratio) + 6px)`：工具条高度确实是
     `min-height: calc(40px * var(--ui-fs-ratio))`，但标签栏高度来自跨代资产 browse.css（写死 40、
     实测 44）⇒ 静态算式会随字号缩放脱节；而且「按各自触发器水平对齐」纯 CSS 表达不了
     （三枚按钮的 x 各不相同）。 */
.td-mod-menu.giencoder-dropdown-popup { position: absolute; top: 42px; z-index: 30; }
.td-rv-menu.giencoder-dropdown-popup { position: absolute; top: 83px; z-index: 30; }
.td-ctxmenu.giencoder-dropdown-popup { position: fixed; top: 0; left: 0; z-index: 60; }
.td-mod-menu { left: 64px; right: auto; }
.td-rv-scope-menu { left: 8px; right: auto; }
.td-rv-opts, .td-commit-menu { right: 8px; left: auto; }
"""

# ============================================================ 2. JS
JS_ANCHOR = u"""  function toggleMenu(menu, trigger) {"""

JS_PLACE = u"""  /* r107-k2
     三枚 `.td-rv-menu` 的触发器都在**审查模块的工具条**（`.td-mod-bar`）里，而基类规则把菜单
     钉在 `.td-browse` 的 `top: 42px`（= 标签栏下方）⇒ 菜单跑到**触发按钮上方** 34~36px
     （1440 实测 dy = −35.0 / −34.0 / −36.0）。这里在**打开瞬间**按触发器实际几何现场摆位。
     ▸ 与 `.td-ctxmenu` 的 `ctxShow()` / 划词浮条的 `selShow()` 同一套做法（本页既有口径）。
     ▸ 为什么不用纯 CSS / 为什么非这三枚：见 panel.css 第 1 节 `r107-k1` 那段注释。
     ⚠ 必须在 `[hidden]` 摘掉**之后**调用（否则量到 0×0）；
       量宽高用 `offsetWidth/offsetHeight` —— 不受入场 `scale(0.96)` 过渡影响
       （`getBoundingClientRect()` 会把 0.96 乘进去，量出来的宽是错的）。
     ⚠ `.td-mod-menu` 走同一条 `toggleMenu`，但它不带 `.td-rv-menu` ⇒ 这里直接放行，
       保持它原来的 CSS 落位（`top: 42px; left: 64px`）不动。 */
  var RV_GAP = 6, RV_PAD = 4;
  function placeRv(menu, trigger) {
    if (!trigger || !menu.classList.contains('td-rv-menu')) return;
    var host = menu.offsetParent;                     /* = `.td-browse`（position: relative） */
    if (!host) return;
    var hr = host.getBoundingClientRect();
    var ox = hr.left + host.clientLeft;               /* 包含块原点 = padding box 左上角 */
    var oy = hr.top + host.clientTop;
    var tr = trigger.getBoundingClientRect();
    var top = tr.bottom - oy + RV_GAP;                /* 触发器下缘往下 6px */
    var left = tr.left - ox;                          /* 左缘对齐触发器 */
    var maxLeft = host.clientWidth - menu.offsetWidth - RV_PAD;
    if (left > maxLeft) left = maxLeft;               /* 右侧放不下 ⇒ 向左收，贴住面板右内边 */
    if (left < RV_PAD) left = RV_PAD;
    menu.style.top = Math.round(top) + 'px';
    menu.style.left = Math.round(left) + 'px';
    menu.style.right = 'auto';                        /* 不清掉基类的 right，会与 left 一起把盒子拉宽 */
  }

"""

JS_OLD = u"""      menu.classList.add(POP_OPEN);
      if (trigger) trigger.setAttribute('aria-expanded', 'true');
"""

JS_NEW = u"""      menu.classList.add(POP_OPEN);
      if (trigger) trigger.setAttribute('aria-expanded', 'true');
      placeRv(menu, trigger);                         /* r107-k2 */
"""


def patch(p, steps):
    t, nl = rd(p)
    n0 = len(t)
    for old, new, label, mark in steps:
        t = edit(t, old, new, label, mark)
    if len(t) != n0:
        wr(p, t, nl)
    print(u'   %-52s %d -> %d' % (os.path.relpath(p, REPO), n0, len(t)))


patch(CSS, [(CSS_OLD, CSS_NEW, u'panel.css · 拆共用定位规则 + rv 菜单兜底 top', u'r107-k1')])
patch(JS, [
    (JS_ANCHOR, JS_PLACE + JS_ANCHOR, u'panel.js · 新增 placeRv()', u'r107-k2'),
    (JS_OLD, JS_NEW, u'panel.js · toggleMenu 打开时调用 placeRv()', u'placeRv(menu, trigger);'),
])

print()
print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
for x in APPLIED:
    print(u'  + ' + x)
for x in SKIPPED:
    print(u'  = ' + x)
