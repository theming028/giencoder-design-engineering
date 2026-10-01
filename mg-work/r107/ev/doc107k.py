# -*- coding: utf-8 -*-
u"""r107 第十拍记忆同步：acceptance / apply107 docstring / HANDOFF / PAGES / PLAYBOOK / 仓库 MEMORY / 工作区 MEMORY / 两份日志。

幂等：每步的 mark 都必须是「只有改后才存在」的串；跑两遍第二遍应全为「跳过」。
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))

APPLIED, SKIPPED = [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def patch(p, steps, label):
    t, nl = rd(p)
    n0 = len(t)
    for mark, old, new, sub in steps:
        if mark and mark in t:
            SKIPPED.append(label + u' · ' + sub)
            continue
        if old is None:                       # None = 尾部追加
            APPLIED.append(label + u' · ' + sub)
            t = t + new
            continue
        c = t.count(old)
        if c != 1:
            sys.exit(u'!! %s · %s：锚点命中 %d 次（应 1）' % (label, sub, c))
        APPLIED.append(label + u' · ' + sub)
        t = t.replace(old, new, 1)
    if len(t) != n0:
        wr(p, t, nl)
    print(u'   %-42s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


# ============================================================ 1. acceptance.md 第十五节
ACC = os.path.join(REPO, 'mg-work', 'r107', 'acceptance.md')
ACC_NEW = u"""
## 十五、第十拍（邵先生 2026-10-01 13:2x 返工 · 一条）

> 原文：**「`td-rv-menu giencoder-dropdown-popup td-rv-opts giencoder-popup-open`
> 菜单的位置不对，应该显示在触发按钮的下方」**

### 第十拍 ① 三枚 `.td-rv-menu` 从「钉面板 `top: 42px`」改为「按触发器现场摆位」

**症状**：点「显示选项」（`.td-rv-opts`）时，菜单跑到**触发按钮上方**。

**量出来的实况**（1440 / 右栏开 / 审查模块；`dy = 菜单 top − 触发器 bottom`）：

| 菜单 | 触发器 | 所在容器 | 触发器 bottom | 菜单 top | dy | 判定 |
|---|---|---|---|---|---|---|
| `.td-mod-menu` | `.td-browse-add` | 标签栏 | 84.5 | 91.0 | **+6.5** | OK |
| `.td-rv-scope-menu` | `.td-rv-scope` | **工具条** | 126.0 | 91.0 | **−35.0** | 错 |
| `.td-rv-opts` | `.td-browse-ico[data-td-rv-opts]` | **工具条** | 125.0 | 91.0 | **−34.0** | 错 |
| `.td-commit-menu` | `.td-rv-commit` | **工具条** | 127.0 | 91.0 | **−36.0** | 错 |

**根因**：四枚下拉共用一条基类规则 `{ position: absolute; top: 42px }`（相对 `.td-browse`，
42px = 标签栏 44px 下方）。但 `.td-mod-menu` 的触发器在**标签栏**里，另三枚的触发器在
**审查模块的工具条**（`.td-mod-bar`，绝对 93~134）里 ⇒ 同一条 `top` 对后者就变成「按钮上方 35px」。
**一条规则服务两种锚点高度 ⇒ 必然错一半。**

**修法**（JS 现场摆位；`.td-mod-menu` 一字不动）：

```js
var RV_GAP = 6, RV_PAD = 4;
function placeRv(menu, trigger) {
  if (!trigger || !menu.classList.contains('td-rv-menu')) return;
  var host = menu.offsetParent;                  /* = .td-browse（position: relative） */
  if (!host) return;
  var hr = host.getBoundingClientRect();
  var ox = hr.left + host.clientLeft, oy = hr.top + host.clientTop;   /* 包含块原点 = padding box */
  var tr = trigger.getBoundingClientRect();
  var top = tr.bottom - oy + RV_GAP;
  var left = tr.left - ox;
  var maxLeft = host.clientWidth - menu.offsetWidth - RV_PAD;
  if (left > maxLeft) left = maxLeft;            /* 右侧放不下 ⇒ 向左收，贴住面板右内边 */
  if (left < RV_PAD) left = RV_PAD;
  menu.style.top = Math.round(top) + 'px';
  menu.style.left = Math.round(left) + 'px';
  menu.style.right = 'auto';                     /* 不清 right，会与 left 一起把盒子拉宽 */
}
```

调用点 = `toggleMenu()` 的**打开分支**，且必须在**摘掉 `[hidden]` 之后**（否则量到 0×0）：

```js
menu.removeAttribute('hidden');
menu.classList.add(POP_OPEN);
if (trigger) trigger.setAttribute('aria-expanded', 'true');
placeRv(menu, trigger);          /* ← 新增 */
```

CSS 侧只做两件事：把共用规则**拆成两条**，并给 `.td-rv-menu` 一个**静态兜底** `top: 83px`
（JS 未生效时的近似值；真位置一律由行内样式接管）。

**为什么否决了纯 CSS**（三条路都试过）：
1. 静态 `top: calc(44px + 40px * var(--ui-fs-ratio) + 6px)` —— 工具条高度确实是
   `min-height: calc(40px * var(--ui-fs-ratio))`，但标签栏高度来自**跨代资产** `browse.css`
   （写死 `height: 40px`、**实测 44**）⇒ 两个魔法数**来源不同**，且字号一缩放就脱节。
2. 「包含块换成 `.td-mod-bar` + `top: 100%`」—— 祖先 `.td-mod { overflow: hidden }` 会裁掉菜单
   （这正是当年改用 `.td-browse` 当参照的原因）。
3. 水平也做不到：三枚触发器的 x 各不相同，「各自对齐各自触发器」纯 CSS 表达不了。

**判据**（1440 / 清缓存 / 三枚全开）：

| 菜单 | dy | dxLeft | coversH | 行内值 |
|---|---|---|---|---|
| `.td-rv-scope-menu` | **+6.0** | **+0.0** | true | top 83 / left 12 |
| `.td-rv-opts` | **+6.0** | **−0.1** | true | top 82 / left 710 |
| `.td-commit-menu` | **+6.0** | −14.1 | true | top 84 / left 726 |
| `.td-mod-menu`（**回归**） | +6.5 | −118.0 | true | 仍是 CSS 的 42 / 64 ⇒ **未受影响** |

★ `.td-commit-menu` 的 `dxLeft = −14.1` 是 **clamp 生效**（菜单宽 168 > 按钮 84 ⇒ 右缘贴住面板右内边 4px），
**不是错位**。
★ **行内确实接管了**：`opts` 实测行内 `top: 82px` ≠ CSS 兜底 `83px`。

**窄栏降级**（`--av-browse-w: 315px`）：三枚均 `insideMod = true`（不被 `.td-mod{overflow:hidden}` 裁）、
`inPanel L/R = true`；opts 被 clamp 到 `left = 137`（= `313 − 172 − 4`）⇒ 贴住右内边。

**行为回归**（真机 / 真键盘 `press Escape` / 真鼠标）：

| 步骤 | 结果 |
|---|---|
| 打开 `.td-rv-opts` | `top 82 / left 710` ✓ |
| `press Escape` | 关闭 ✓ |
| **再次打开** | 位置**完全一致**（82 / 710）⇒ 内联重算幂等 ✓ |
| 点面板空白 | 关闭 ✓ |
| 打开 `.td-rv-scope-menu` → 点工具条 | 关闭 ✓ |
| 右键 `.td-diff-h` | `.td-ctxmenu` 落在指针处（`top 300 / left 900`）✓，Esc 关 ✓ |

### 第十拍 门禁 / 产物

幂等 ✓（`应用 0 项 / 跳过 3 项`；`apply107.py` 第二遍「已是目标态」）｜`check-syntax.py pages/*.html` **10/10**｜
`verify-design.py ./pages` 与 `vd-r107j.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜
`scan-flatten.py panel.css` 仍 **2 条**（本拍**不动字号**）｜
改动面 = `M pages/conversation.html`（`+2419 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍遗留）
+ `?? mg-work/r107/`。
产物 **934109 → 936625 字符（+2516；相对 HEAD +137394）**；UTF-8（LF 归一）**1029334** / 工作区 **1036446** /
LF `sha1 bc830fa56c0c`。
资产 `panel.css 43657`（CRLF）· `panel.js 52203`（LF）。探针 `ev/p107k_pos.js`（几何对照）+ `ev/p107k_narrow.js`
（越界判据）+ `probe107k{,1,2,3}.sh` + `shots107k.sh`；出图 `raw/k-*.png`。备份 `ev/bak10/`。
★ **体位**：本拍仍**未动** `_mods.html` / `browse.html` ⇒ 不必重跑 `splice107.py` / `make107.py`；
改序只剩 `part107/panel.{css,js}` → `ev/patch107k.py` → `apply107.py`（part 文件是**运行时读**的）。
"""

# ============================================================ 2. apply107.py docstring
APPLY = os.path.join(REPO, 'mg-work', 'r107', 'apply107.py')
APPLY_ANCHOR = u"\n体位与历代一致：本脚本 = **净底（base.html 摘掉历代注入块）+ 重新注入本代块**，"
APPLY_NEW = u"""
★ **第十拍（2026-10-01 13:2x 邵先生一条）** —— 仍是 r107 未提交期的**就地返工**，
  `GENS` / 注入块 id / `NAV_TAG` 依旧一字不动；两处落点都在 `part107/` 内（`panel.css` + `panel.js`，
  均为就地改）；`_mods.html` / `browse.html` 一字未动 ⇒ 不必重跑 `splice107.py` / `make107.py`：
    ① **三枚 `.td-rv-menu` 的位置不对（跑到触发按钮上方）** —— 四枚下拉共用一条
       `{ position: absolute; top: 42px }`（42px = 标签栏 44px 下方），但 `.td-mod-menu` 的触发器
       在**标签栏**里、另三枚（`.td-rv-scope-menu` / `.td-rv-opts` / `.td-commit-menu`）的触发器
       在**审查模块的工具条**（`.td-mod-bar`）里 ⇒ 实测 dy（菜单 top − 触发器 bottom）
       = **−35.0 / −34.0 / −36.0**（即跑到按钮**上方** 35px 左右）。
       修法 = 新增 `placeRv(menu, trigger)`，在 `toggleMenu()` 的打开分支（**摘掉 `[hidden]` 之后**，
       否则量到 0×0）按触发器的**实际几何**现场摆位：垂直 = 触发器下方 6px、水平 = 左缘对齐触发器、
       右侧放不下就 clamp 到面板内边（`left = host.clientWidth − menu.offsetWidth − 4`）；
       量宽高用 `offsetWidth/offsetHeight`（**不受入场 `scale(0.96)` 影响**，`getBoundingClientRect` 会）。
       CSS 只把共用规则**拆成两条**并给 `.td-rv-menu` 一个静态兜底 `top: 83px`（`.td-mod-menu` 的
       `42px` 不动）。
       ★ 否决纯 CSS 的三条理由：静态 `top` 依赖「标签栏高度（**跨代资产** browse.css 写死 40、
         **实测 44**）」+「工具条高度（`calc(40px * ratio)`）」两个**来源不同**的魔法数 ⇒ 字号一缩放
         就脱节；「包含块换成 `.td-mod-bar` + `top:100%`」会被祖先 `.td-mod{overflow:hidden}` 裁掉；
         「各自水平对齐各自触发器」纯 CSS 表达不了（三枚按钮 x 各不相同）。
       ★ 实测：三枚 dy 全 **+6.0**、dxLeft **+0.0 / −0.1 / −14.1**（末者是 clamp 生效，非错位）；
         `.td-mod-menu` 回归不变（仍 `42 / 64`）；窄栏 315 三枚全部 `insideMod = true` 未被裁。
         行为回归：Esc 关 / 点空白关 / 重开位置一致 / 右键菜单（`.td-ctxmenu`）不受影响，全绿。
"""

# ============================================================ 3. HANDOFF.md
HANDOFF = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')
HANDOFF_TAIL_ANCHOR = u"""   产物 **930384 → 934109 字符**（+3725），`+2373 / −8` 行。

---

## 三、r88 ~ r92 做了什么（前情提要）"""
HANDOFF_TAIL_NEW = u"""   产物 **930384 → 934109 字符**（+3725），`+2373 / −8` 行。

**⑩ 第十拍（邵先生 2026-10-01 13:2x 返工 · 一条）** —— **`.td-rv-menu` 菜单跑到触发按钮上方**：
1. 四枚下拉共用一条基类规则 `{ position:absolute; top:42px }`（相对 `.td-browse`，42px = 标签栏下方）。
   但 `.td-mod-menu` 的触发器（`+`）在**标签栏**里、另三枚（`.td-rv-scope-menu` / `.td-rv-opts` /
   `.td-commit-menu`）的触发器在**审查模块的工具条**里 ⇒ 后者实测 dy = **−35.0 / −34.0 / −36.0**
   （在按钮**上方** 35px 左右）。★ **一条 `top` 服务两种锚点高度 ⇒ 必然错一半。**
2. 修法 = 新增 `placeRv(menu, trigger)`，在 `toggleMenu()` 打开分支（**摘掉 `[hidden]` 之后**）
   按触发器的**实际几何**现场摆位：垂直 = 下方 6px；水平 = 左缘对齐触发器，右侧放不下就
   clamp 到面板右内边。量宽高用 `offsetWidth`（不受入场 `scale(0.96)` 影响）。
   CSS 只把共用规则拆两条 + 给 `.td-rv-menu` 一个静态兜底 `top: 83px`；**`.td-mod-menu` 一字不动**。
3. ★ 实测三枚 dy 全 **+6.0**、dxLeft **0.0 / −0.1 / −14.1**（末者 = clamp 生效）；`.td-mod-menu`
   回归不变；窄栏 315 三枚全部 `insideMod=true` 未被 `.td-mod{overflow:hidden}` 裁；
   Esc 关 / 点空白关 / 重开位置一致 / 右键菜单不受影响 —— 全绿。
   门禁：幂等 ✓ / `check-syntax` 10/10 / `verify-design` 与上轮逐字节同 / `scan-flatten` 仍 2 条。
   产物 **934109 → 936625 字符**（+2516），`+2419 / −8` 行。适配层**零字号改动**。

---

## 三、r88 ~ r92 做了什么（前情提要）"""

# ============================================================ 4. PAGES.md
PAGES = os.path.join(REPO, '.workbuddy', 'memory', 'PAGES.md')
PAGES_TAIL_ANCHOR = u"""> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四**节）。"""
PAGES_TAIL_NEW = u"""> **⑩ 三枚 `.td-rv-menu` 改为「按触发器现场摆位」** —— 原四枚共用一条 `top:42px`（钉在标签栏下方），
> 而这三枚的触发器在**审查工具条**里 ⇒ 菜单跑到**按钮上方** 34~36px（实测 dy = −35.0 / −34.0 / −36.0）；
> 新增 `placeRv()` 在打开瞬间按触发器**实际几何**摆位（垂直 +6px / 水平锚定触发器 / 右侧放不下 clamp 到面板内边），
> `.td-mod-menu` 一字不动
> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五**节）。"""

PAGES_ROWS = u"""| **`.td-rv-menu` 摆位** | ★ **第十拍 ①**：**按触发器实际几何现场摆位**（`panel.js` 的 `placeRv()`，在 `toggleMenu()` 打开分支、**摘掉 `[hidden]` 之后**调用）。⚠ 原四枚共用基类 `{ position:absolute; top:42px }`（相对 `.td-browse`）—— 该值只对**触发器在标签栏**的 `.td-mod-menu` 成立，另三枚的触发器在**审查工具条**里 ⇒ 实测 dy（菜单 top − 触发器 bottom）= **−35.0 / −34.0 / −36.0**（跑到按钮**上方**）。量宽高用 `offsetWidth`（不受入场 `scale(0.96)` 影响） |
| **`.td-rv-menu` 的 clamp** | ★ **第十拍 ①**：`left = host.clientWidth − menu.offsetWidth − 4`（右侧放不下 ⇒ 向左收，贴住面板右内边）。★ 窄栏 315 实测三枚全部 `insideMod = true`（**没被 `.td-mod{overflow:hidden}` 裁**）。CSS 只留静态兜底 `top: 83px`；⚠ 写行内 `left` **必须同时 `right:'auto'`**，否则与基类的 `right` 一起把盒子拉宽 |
"""

# ============================================================ 5. PLAYBOOK.md
PLAYBOOK = os.path.join(REPO, '.workbuddy', 'memory', 'PLAYBOOK.md')
PLAYBOOK_NEW = u"""
## P3.46 ★★ r107 第十拍（一条 · 2026-10-01 13:2x 邵先生返工）

**① 「一条定位规则服务两种锚点高度」⇒ 必然错一半（浮层摆位的通病）**
* 症状：同一个基类里的下拉菜单，**有的位置对、有的跑到触发按钮上方**（实测上方 35px）。
* 根因：四枚共用 `{ position: absolute; top: 42px }`（相对面板容器）。
  `.td-mod-menu` 的触发器在**标签栏**里 ⇒ 42px 恰好是「按钮下方」；
  另三枚的触发器在**工具条**（标签栏之下 40px）里 ⇒ 同一个 42px 就变成「按钮**上方**」。
* ★ **配方：浮层的锚点是「触发器的实际几何」，不是「面板的某个固定偏移」。**
  打开瞬间按 `trigger.getBoundingClientRect()` 摆位（本站既有口径：`.td-ctxmenu` 的 `ctxShow()`、
  划词浮条的 `selShow()` 都这么写）。**同一基类里只要触发器的容器不同，就必须逐个算。**
* ★ 判据不是「看着对」：量 **`dy = 菜单 top − 触发器 bottom`**（应恒为一个 gap）+ `coversH`
  （菜单水平是否覆盖触发器）。

**② 别用「静态 `top: calc(...)`」代替现场摆位 —— 只要算式里的两个数来自不同源，就会脱节**
* 本站的诱惑写法：`top: calc(44px + 40px * var(--ui-fs-ratio) + 6px)`。
* 为什么不能要：工具条高度确实是 `min-height: calc(40px * ratio)`（随字号缩放），
  但**标签栏高度来自跨代资产 `browse.css`**（写死 `height: 40px`、**实测 44**）⇒ 两个魔法数
  **来源不同、缩放行为不同**；一旦 `--ui-fs-ratio` ≠ 1 或那层被改，算式立刻失准。
* 通用化：**「看起来能算」不等于「算得住」** —— 算式里出现「另一个模块的高度 / 另一个资产写死的值」
  就要改用运行时量测。

**③ 浮层摆位的三条硬规矩（本拍踩全了）**
* **必须在摘掉 `[hidden]` 之后量 / 摆** —— 隐藏元素 `offsetWidth` / `getBoundingClientRect` 全是 0。
* **量尺寸用 `offsetWidth` / `offsetHeight`，不要用 `getBoundingClientRect()`** ——
  入场动画若带 `scale(0.96)`，rect 会把 0.96 **乘进去**（读数偏小 4%）。`offset*` 不受 transform 影响。
* **写行内 `left` 必须同时 `right: 'auto'`** —— absolute 元素同时有 `left` 与 `right` 时会被**拉宽**；
  基类里那半条 `right: 8px` 不清掉，纵向摆位对了、横向仍会变形。

**④ clamp 到容器内边 = 天然的窄栏降级（顺手就做掉）**
* 菜单固定宽（168~172），触发器靠近右缘时右缘必然溢出 ⇒
  `left = min(left, host.clientWidth − menu.offsetWidth − 4)`。
* ★ 判据写成**「是否仍在裁剪祖先之内」**：本站菜单挂在 `.td-mod{overflow:hidden}` 里 ⇒ 必须量
  `insideMod`（左/右/上/下四条都在内），不能只看「在面板内」。窄栏 315 实测三枚全 `true`。

★ **体位**：本拍仍**未动** `_mods.html` / `browse.html` ⇒ 不必重跑 `splice107.py` / `make107.py`；
改序 = `part107/panel.css` + `part107/panel.js`（均就地改） → `ev/patch107k.py` → `apply107.py`。
产物 `934109 → 936625` 字符；`+2419 / −8` 行；门禁全绿；**零字号改动**（`scan-flatten` 仍 2 条）。
"""

# ============================================================ 6. 仓库 MEMORY.md
MEM = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')
MEM_OLD_BLOCK = u"""> **产物**：`conversation.html` **799231（= HEAD）→ 866988 → 876008 → 894916 → 920259 → 921730 → 925776 → 927464 → 930384 Unicode 字符**（八拍合计 **+131153**）；
> UTF-8 字节（LF 归一）**1019883** ｜ 工作区字节（CRLF）**1026880** ｜ LF `sha1 c8b5e944e2de`；`base.html` **472150 逐字节不变**。
> **八查**：幂等 ✓（**每拍连跑两遍**）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
> `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜代数残留 **0**（`r107-conv-*` 各 1、`r106-*`/`r102-*`/`r101-*`/`r93-conv-*` 全 0）｜
> `git status` = `M pages/conversation.html`（`+2299 / −3` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍文案）+ `?? mg-work/r107/`。
> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.44**；各拍要点见 **PAGES P3.11i（共八拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十三节）**。
"""

MEM_TAIL_OLD = u"""> **产物**：`conversation.html` **799231 → … → 930384 → 934109 Unicode 字符**（九拍合计 **+134878**）；
> UTF-8 字节（LF 归一）**1025618** ｜ 工作区字节（CRLF）**1032684** ｜ LF `sha1 147f703da06f`；`base.html` **472150 逐字节不变**。
> **九查**：幂等 ✓（每拍连跑两遍）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
> `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜
> `scan-flatten.py` `panel.css` 仍 **2 条**（第九拍**零 CSS 改动**）｜代数残留 **0**｜
> `git status` = `M pages/conversation.html`（`+2373 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`。
> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.45**；各拍要点见 **PAGES P3.11i（共九拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十四节）**。"""

MEM_TAIL_NEW = MEM_TAIL_OLD + u"""
> **第十拍（一条）** = ⑮ **三枚 `.td-rv-menu`（对比范围 / 显示选项 / 提交·推送）跑到触发按钮上方** —— 四枚共用一条
> `{ position:absolute; top:42px }`（相对 `.td-browse`，42px = 标签栏下方），但 `.td-mod-menu` 的触发器在**标签栏**里、
> 另三枚的触发器在**审查工具条**里 ⇒ 实测 dy = **−35.0 / −34.0 / −36.0**。★ **一条 `top` 服务两种锚点高度 ⇒ 必然错一半。**
> 修法 = 新增 `placeRv(menu, trigger)`，在 `toggleMenu()` 打开分支（**摘掉 `[hidden]` 之后**）按触发器**实际几何**摆位：
> 垂直 = 下方 6px；水平 = 左缘对齐触发器、右侧放不下 clamp 到面板右内边；量宽高用 **`offsetWidth`**
> （不受入场 `scale(0.96)` 影响）。CSS 只拆共用规则 + 给 `.td-rv-menu` 静态兜底 `top: 83px`；**`.td-mod-menu` 一字不动**。
> ★ 实测三枚 dy 全 **+6.0**、dxLeft **0.0 / −0.1 / −14.1**（末者 = clamp 生效）；`.td-mod-menu` 回归不变；
> 窄栏 315 三枚全部 `insideMod=true`（**未被 `.td-mod{overflow:hidden}` 裁**）；Esc 关 / 点空白关 / **重开位置一致** /
> 右键菜单（`.td-ctxmenu`）不受影响 —— 全绿。
> 「为什么否决纯 CSS」= 静态算式依赖「标签栏高度（**跨代资产** browse.css 写死 40、**实测 44**）」+
> 「工具条高度（`calc(40px*ratio)`）」两个**来源不同**的魔法数 ⇒ 字号一缩放即脱节。
>
> **产物**：`conversation.html` **799231 → … → 934109 → 936625 Unicode 字符**（十拍合计 **+137394**）；
> UTF-8 字节（LF 归一）**1029334** ｜ 工作区字节（CRLF）**1036446** ｜ LF `sha1 bc830fa56c0c`；`base.html` **472150 逐字节不变**。
> **十查**：幂等 ✓（每拍连跑两遍）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
> `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜
> `scan-flatten.py` `panel.css` 仍 **2 条**（第十拍**不动字号**）｜代数残留 **0**｜
> `git status` = `M pages/conversation.html`（`+2419 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`。
> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.46**；各拍要点见 **PAGES P3.11i（共十拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十五节）**。"""

# ============================================================ 7. 工作区 MEMORY.md
WSMEM = os.path.join(WS, '.workbuddy', 'memory', 'MEMORY.md')
WSMEM_ANCHOR = u"## 二、Windows 环境速记"
WSMEM_NEW = u"""46. ★★ **浮层的锚点是「触发器的实际几何」，不是「容器的固定偏移」**（r107 第十拍）：
    同一基类里的多枚下拉只要**触发器分属不同容器**，共用一条 `top:Npx` 就**必然错一半**
    （本站 4 枚共用 `top:42px`：触发器在标签栏的那枚对，在工具条的 3 枚跑到**按钮上方** 35px）。
    ★ 修法 = 打开瞬间按 `trigger.getBoundingClientRect()` 现场摆位（本站既有口径：`.td-ctxmenu` /
    划词浮条都这么写）。★ 判据 = 量 **`dy = 菜单 top − 触发器 bottom`**（应恒为一个 gap）+ `coversH`。
47. ★★ **浮层摆位三条硬规矩**（r107 第十拍全踩过）：
    ① 必须在**摘掉 `[hidden]` 之后**量/摆（隐藏元素 rect/offset 全 0）；
    ② 量尺寸用 **`offsetWidth/offsetHeight`**，**别用 `getBoundingClientRect()`** ——
       入场动画带 `scale(0.96)` 时 rect 会把 0.96 乘进去（读数偏小 4%）；`offset*` 不受 transform 影响；
    ③ 写行内 `left` **必须同时 `right:'auto'`**，否则与基类的 `right` 一起把盒子**拉宽**。
48. ★★ **别用「静态 `top: calc(...)`」代替现场摆位**（r107 第十拍）：算式里只要有**两个来源不同**的数
    （本站 = 工具条高度 `calc(40px*ratio)` + 标签栏高度来自**跨代资产** browse.css 写死 40、**实测 44**），
    字号一缩放就脱节。★ 另：clamp 到容器内边（`clientWidth − 自身宽 − 4`）= **天然的窄栏降级**；
    判据要量**「是否仍在裁剪祖先（`.td-mod{overflow:hidden}`）之内」**，不能只量「在面板内」。
## 二、Windows 环境速记"""

# ============================================================ 8. 两份日志
LOG_REPO = os.path.join(REPO, '.workbuddy', 'memory', '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')
LOG_NEW = u"""
### 第十拍（邵先生 2026-10-01 13:2x · 右栏下拉菜单位置，一条）

**症状**：`.td-rv-opts`（显示选项）打开后菜单跑到**触发按钮上方**。

**根因**：四枚下拉共用一条基类 `{ position:absolute; top:42px }`（相对 `.td-browse`，42px = 标签栏下方）。
`.td-mod-menu` 的触发器（`+`）在**标签栏**里 ⇒ 天然「按钮下方」；另三枚（`.td-rv-scope-menu` /
`.td-rv-opts` / `.td-commit-menu`）的触发器在**审查模块的工具条**里 ⇒ 实测 dy（菜单 top − 触发器 bottom）
= **−35.0 / −34.0 / −36.0**。★ **一条 `top` 服务两种锚点高度 ⇒ 必然错一半。**

**修法**：`panel.js` 新增 `placeRv(menu, trigger)`，在 `toggleMenu()` 打开分支（**摘掉 `[hidden]` 之后**）
按触发器**实际几何**现场摆位 —— 垂直 = 下方 6px；水平 = 左缘对齐触发器、右侧放不下就 clamp 到面板右内边；
量宽高用 `offsetWidth`（**不受入场 `scale(0.96)` 影响**）；写行内 `left` 时**同时 `right:'auto'`**。
`panel.css` 只把共用规则拆两条 + 给 `.td-rv-menu` 静态兜底 `top: 83px`；**`.td-mod-menu` 一字不动**。
★ 否决纯 CSS：静态 `top: calc(...)` 依赖「标签栏高度（跨代资产 browse.css 写死 40、**实测 44**）」+
「工具条高度（`calc(40px*ratio)`）」两个**来源不同**的魔法数 ⇒ 字号一缩放即脱节；
「包含块换成 `.td-mod-bar` + `top:100%`」会被祖先 `.td-mod{overflow:hidden}` 裁掉。

**验证**：1440 三枚 dy 全 **+6.0**、dxLeft **0.0 / −0.1 / −14.1**（末者 = clamp 生效，非错位）；
`.td-mod-menu` 回归不变（仍 `42 / 64`）；1024 档同上；窄栏 315 三枚全部 `insideMod=true` 未被裁；
行为回归（Esc 关 / 点空白关 / **重开位置一致** / 右键菜单不受影响）全绿。
**产物**：`conversation.html` 934109 → **936625** 字符（`+2419 / −8` 行）；`base.html` 与其余 8 页逐字节不变。
门禁：幂等 ✓（`应用 0 / 跳过 3`）/ `check-syntax` 10/10 / `verify-design` 与上轮**逐字节同** /
`scan-flatten` 仍 2 条（零字号改动）。**探针** `ev/p107k_pos.js` + `p107k_narrow.js` + `probe107k{,1,2,3}.sh` +
`shots107k.sh`；**出图** `raw/k-*.png`；**备份** `ev/bak10/`。🚫 未 commit / 未 push。
"""


def main():
    # 1. acceptance.md：尾部追加第十五节
    patch(ACC, [(u'## 十五、第十拍（邵先生 2026-10-01 13:2x 返工 · 一条）', None, ACC_NEW, u'追加第十五节')],
          'acceptance.md')
    # 2. apply107.py docstring
    patch(APPLY, [(u'第十拍（2026-10-01 13:2x 邵先生一条）', APPLY_ANCHOR, APPLY_NEW + APPLY_ANCHOR, u'docstring 第十拍段')],
          'apply107.py')
    # 3. HANDOFF
    patch(HANDOFF, [
        (u'（十拍累积）', u'（八拍累积）', u'（十拍累积）', u'头行 八拍→十拍'),
        (u'共**十拍**', u'共**九拍**', u'共**十拍**', u'r107 段头 九拍→十拍'),
        (u'（**十五节**，含第二 ~ 十拍返工）', u'（**十四节**，含第二 ~ 九拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.45**；',
         u'（**十五节**，含第二 ~ 十拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.46**；', u'节数 + P3.46'),
        (u'**⑩ 第十拍（邵先生 2026-10-01 13:2x 返工 · 一条）**', HANDOFF_TAIL_ANCHOR, HANDOFF_TAIL_NEW, u'追加第十拍段'),
    ], 'HANDOFF.md')
    # 4. PAGES
    patch(PAGES, [
        (u'· **共十拍**）', u'· **共九拍**）', u'· **共十拍**）', u'P3.11i 标题 九拍→十拍'),
        (u'**十拍要点**', u'**九拍要点**', u'**十拍要点**', u'逐拍要点标题'),
        (u'**⑩ 三枚 `.td-rv-menu`', PAGES_TAIL_ANCHOR, PAGES_TAIL_NEW, u'逐拍要点 +⑩'),
        (u'**`.td-rv-menu` 摆位**', u'\n\n**⚠ 改这一块之前必看**\n',
         u'\n' + PAGES_ROWS + u'**⚠ 改这一块之前必看**\n', u'固定事实表 +2 行'),
    ], 'PAGES.md')
    # 5. PLAYBOOK
    patch(PLAYBOOK, [(u'## P3.46 ★★ r107 第十拍', None, PLAYBOOK_NEW, u'追加 P3.46')], 'PLAYBOOK.md')
    # 6. 仓库 MEMORY.md
    patch(MEM, [
        (u'· 十拍）—— 🚫 未提交', u'· 九拍）—— 🚫 未提交', u'· 十拍）—— 🚫 未提交', u'r107 段头 九拍→十拍'),
        (u'★ 本代**十拍**（同一代、', u'★ 本代**九拍**（同一代、`apply107.py` 就地返工九次',
         u'★ 本代**十拍**（同一代、`apply107.py` 就地返工十次', u'本代九拍→十拍'),
        (u'第八拍产物段已并入下方', MEM_OLD_BLOCK,
         u'> （第八拍产物段已并入下方「第十拍」段 —— 见 PLAYBOOK P3.39 ~ P3.46。）\n', u'删第八拍残留产物块'),
        (u'十拍合计 **+137394**', MEM_TAIL_OLD, MEM_TAIL_NEW, u'追加第十拍要点 + 更新产物段'),
    ], 'MEMORY.md(仓库)')
    # 7. 工作区 MEMORY.md
    patch(WSMEM, [(u'46. ★★ **浮层的锚点', WSMEM_ANCHOR, WSMEM_NEW, u'硬规则 +46~48')], 'MEMORY.md(工作区)')
    # 8. 两份日志
    patch(LOG_REPO, [(u'### 第十拍（邵先生 2026-10-01 13:2x', None, LOG_NEW, u'追加第十拍')], '日志(repo)')
    patch(LOG_WS, [(u'### 第十拍（邵先生 2026-10-01 13:2x', None, LOG_NEW, u'追加第十拍')], '日志(ws)')

    print()
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for x in APPLIED:
        print(u'  + ' + x)
    for x in SKIPPED:
        print(u'  = ' + x)


if __name__ == '__main__':
    main()
