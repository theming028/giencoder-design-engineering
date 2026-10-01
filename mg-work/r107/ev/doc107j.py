# -*- coding: utf-8 -*-
"""r107 第九拍（2026-10-01 13:1x 邵先生两条）—— 记忆同步（幂等，连跑两遍验）。

落点：
  1. mg-work/r107/acceptance.md      追加「## 十四、第九拍」
  2. mg-work/r107/apply107.py        docstring 补第九拍段
  3. .workbuddy/memory/HANDOFF.md    头行 / 二·g / 追加 ⑨ 小节
  4. .workbuddy/memory/PAGES.md      P3.11i「共八拍」→「共九拍」+ ⑨ 行 + 固定事实表 +2 行
  5. .workbuddy/memory/PLAYBOOK.md   追加 P3.45（五条新教训）
  6. .workbuddy/memory/MEMORY.md     索引 P3.45 + r107 段多处
  7. E:/GienCoder/.workbuddy/memory/MEMORY.md  硬规则 42~45
  8. 两份当日日志
"""
import io, sys

HANDOFF = '.workbuddy/memory/HANDOFF.md'
PAGES = '.workbuddy/memory/PAGES.md'
PLAYBOOK = '.workbuddy/memory/PLAYBOOK.md'
REPO_MEM = '.workbuddy/memory/MEMORY.md'
WS_MEM = 'E:/GienCoder/.workbuddy/memory/MEMORY.md'
ACC = 'mg-work/r107/acceptance.md'
APPLY = 'mg-work/r107/apply107.py'
LOG_REPO = '.workbuddy/memory/2026-10-01.md'
LOG_WS = 'E:/GienCoder/.workbuddy/memory/2026-10-01.md'

APPLIED = []
SKIPPED = []


def rd(p):
    return io.open(p, 'rb').read().decode('utf-8')


def wr(p, t):
    io.open(p, 'wb').write(t.encode('utf-8'))


def fit(s, t):
    """让新增块的换行与文件现有换行一致（本仓 md 有 CRLF 也有 LF）。"""
    return s.replace('\n', '\r\n') if '\r\n' in t else s


def patch(p, steps, label):
    t = rd(p)
    n0 = len(t)
    for mark, old, new, sub in steps:
        if mark and mark in t:
            SKIPPED.append(label + ' · ' + sub + '（已存在）')
            continue
        if not mark and old not in t:
            if new in t:
                SKIPPED.append(label + ' · ' + sub + '（已应用）')
                continue
            sys.exit('!! %s · %s：旧串与新串都不存在' % (label, sub))
        c = t.count(old)
        if c != 1:
            sys.exit('!! %s · %s：锚点命中 %d 次（应 1）' % (label, sub, c))
        t = t.replace(old, fit(new, t), 1)
        APPLIED.append(label + ' · ' + sub)
    if len(t) != n0:
        wr(p, t)
    print('   %-46s %d -> %d' % (p, n0, len(t)))


def append_once(p, mark, block, label):
    t = rd(p)
    if mark in t:
        SKIPPED.append(label + '（已存在）')
        print('   %-46s %d (无变化)' % (p, len(t)))
        return
    wr(p, t.rstrip('\n') + fit(block, t))
    APPLIED.append(label)
    print('   %-46s %d -> %d' % (p, len(t), len(rd(p))))


# ================================================================ 1. acceptance.md
ACC_BLOCK = '''

## 十四、第九拍

邵先生 2026-10-01 13:1x 两条（**r107 未提交期就地返工，不另起代数**）：

> 在新右栏"全屏"后：
> 1、原全屏按钮的图标没有变为"取消全屏"的图标；
> 2、"拖动调整文件预览栏宽度"的功能不正常，按下鼠标不能正常左右拖动，似乎一下就复位了。

### ① 全屏后按钮图标不翻（真 bug）

**根因**：按钮的内联 SVG 是 `browse.html` 里**写死**的「四角朝外」字形，
`panel.js` 切换时只翻了 `aria-pressed` / `title` / `aria-label`（实测这三项都对），
**`<path d>` 一个字节没动** ⇒ 字形永远是「最大化」。

**修法**（`part107/panel.js`）：抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；
MAX 那套**从 DOM 读出来缓存**（不另抄一份免得漂移），MIN 那套硬编码四条
（Lucide `minimize`：`M8 3v3a2 2 0 0 1-2 2H3` / `M21 8h-3a2 2 0 0 1-2-2V3` /
`M3 16h3a2 2 0 0 1 2 2v3` / `M16 21v-3a2 2 0 0 1 2-2h3`），只切 `d` 属性、**不重建节点**
（不碰 React，hover / focus / 键盘可达性一字不变）。

**判据**：全屏后 4 条 path 的 `d` = MIN 那套 ✓；拖拽退出后回 MAX ✓；再全屏又 MIN ✓；
收起侧栏后回 MAX ✓。★ **目视复核**（`raw/j3-bar-1440-max.png` vs `j3-bar-1440-min.png`）：
一个四角朝外、一个四角朝内，方向相反。

### ② 全屏后拖分栏条「一按就复位」（真 bug，两个因）

**因 (a)：拖拽起点取的是「内部缓存」，不是实况。**
`ctrl-conv.js` 的 `bindSplit()` 里 `startPanel = panelW`；而 `panelW` 只在
「恢复记忆 / 拖动 / 双击复位 / 键盘」时更新 —— r107 的「最大化」是**绕过控制器直接写
`--av-browse-w`** ⇒ 缓存停在 641，实际已是 1040。实测（1440 / 右栏开 / 全屏 1040）：

| 动作 | 改前 `--av-browse-w` | 应为 |
|---|---|---|
| pointerdown | 1040 | 1040 |
| pointermove(-120) | **761**（= 641 + 120） | 1160 → 钳回 1040 |

⇒ 一按下拖动，右栏从 1040 猛缩到 761（≈ 记忆宽）—— 正是报障的「一下就复位」。

**因 (b)：`pointermove` / `pointerup` 挂在元素上，只靠 `setPointerCapture` 兜底。**
全屏后分栏条紧贴窗口左缘，往左拖时指针很快离开元素；一旦捕获没生效（元素被 React 重挂 /
`pointerId` 失配），拖动就**中途断掉**。

**修法**：
* (a) 起点改读**实际渲染宽** —— 先落 `.is-col-dragging`（= `transition: none`）再取
  `getBoundingClientRect()`（拿到的是**终值**而非过渡中间值），并把缓存同步回来；
* (b) `pointermove` / `pointerup` / `pointercancel` / `blur` **一律挂 `window`**（站内其它拖拽同口径）；
* 另加两条**退出路径**：**全屏态下按下分栏条 = 放弃全屏**（`setMax(false, true)` —— 只清状态、
  **不动宽**，宽度交给控制器从实际宽起算）；**侧栏收起时也退出全屏**。

**判据**（1440 / 清 localStorage / 全屏 1040 / 合成 PointerEvent）：

| 动作 | 结果 |
|---|---|
| 全屏 | `--av-browse-w` 1040 ｜ `data-td-maxw` 1040 ｜ `aria-pressed` true ｜ 图标 MIN |
| pointerdown | `maxw` → **(none)**（静默退全屏）、宽度仍 **1040** |
| move(+80) **派发到 `document.body`** | **1040 → 960** ✓（起点 = 实际宽 ✓；事件确已挂 `window` ✓） |
| pointerup | 960 保持；按钮回 `aria-pressed=false` / 图标 MAX |
| 收起侧栏 | `maxw` **(none)** / `aria-pressed` false / 图标 MAX ✓ |

1024 档同流程：全屏 624 → move(+80) ⇒ **561**（= `MIN_PANEL`，钳位正确）。
**回归**：文件树分栏条（`[data-td-split="tree"]`）先把右栏拉到 900 再拖 ⇒ 240 → **280** ✓
（同一函数的两处绑定都验过）。

### 体位 / 覆盖件说明（本拍唯一的结构性决定）

`part105/*` 是**跨代资产**（源页 `avatar.html` 的移植源，历代刻意不回头动它）。
本拍要改的 `bindSplit()` 正在 `part105/ctrl-conv.js` 里 ⇒ 按
`_read_part()` 的 `PART_DIRS = (part107, part105)` **双目录回退**语义，在 `part107/` 放一份
**逐字副本 + 一处修正**（`part107/ctrl-conv.js`）—— **part105 原文与 `avatar.html` 零影响**。
⚠ 代价 = 副本会漂移，已在副本头部写明来源与差异点。

★ **别用 MutationObserver 盯「后插节点」的父级**：那条 flex 行与分栏条都是 ctrl-conv 在
`place()` 里后插的，本文件跑得更早 ⇒ 初次观察挂在**旧父级**上、**永不触发**
（本拍第一版就是这么坏的：收起后 `data-td-maxw` 残留 784、按钮仍是「还原」态）。
正解 = 搭 ctrl-conv 既有的 `setOpen()` **必定 dispatch 一次 resize** 这个事件流。

### ⑨ 本拍门禁 / 产物

幂等 ✓（`应用 0 项 / 跳过 3 项`；`apply107.py` 第二遍「已是目标态」）｜`check-syntax.py pages/*.html` **10/10**｜
`verify-design.py ./pages` 与 `vd-r107i2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜
`scan-flatten.py` `panel.css` 仍 **2 条**（本拍**零 CSS 改动**）｜
改动面 = `M pages/conversation.html`（`+2373 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍文案）
+ `?? mg-work/r107/`（含新建 `part107/ctrl-conv.js`）。
产物 **930384 → 934109 字符（+3725；相对 HEAD +134878）**。
★ **体位**：本拍**未动** `_mods.html` / `browse.html` ⇒ 不必重跑 `splice107.py` / `make107.py`，
改序只剩 `part107/*` → `apply107.py`（part 文件是**运行时读**的，改完直接重跑即落页面）。
'''

# ================================================================ 2. apply107.py
APPLY_BLOCK = '''★ **第九拍（2026-10-01 13:1x 邵先生两条）** —— 仍是 r107 未提交期的**就地返工**，
  `GENS` / 注入块 id / `NAV_TAG` 依旧一字不动（工作区仍是 `M conversation.html` + `?? mg-work/r107/`）；
  一处落 `part107/panel.js`（就地改），一处落**新建的 `part107/ctrl-conv.js`（覆盖件）**；
  `_mods.html` / `browse.html` 一字未动 ⇒ 不必重跑 `splice107.py` / `make107.py`：
    ① **全屏后按钮图标不翻** —— 内联 SVG 是 HTML 写死的「四角朝外」，JS 只翻了
       `aria-pressed` / `title` / `aria-label` ⇒ 抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；
       MAX 那套**从 DOM 读出来缓存**、MIN 那套硬编码（Lucide `minimize` 四条），只切 `d`、不重建节点。
    ② **全屏后拖分栏条「一按就复位」** —— 两个因：
       (a) 起点取**内部缓存** `panelW`（「最大化」绕过控制器直接写 `--av-browse-w`
           ⇒ 缓存停在 641 而实际 1040）⇒ 改读**实际渲染宽**（先落 `.is-col-dragging` 停过渡、
           再取几何 = 终值）并把缓存同步回来；
       (b) `pointermove` / `pointerup` 挂**元素**、只靠 `setPointerCapture` 兜 ⇒ 改挂 **`window`** + `blur`。
       另补两条退出路径：**全屏态下按下分栏条 = 放弃全屏**（`setMax(false, true)`，不动宽）；
       **收起侧栏也退全屏**（搭 ctrl-conv `setOpen()` 必定 dispatch 的 resize，**不观察 DOM** ——
        那条 flex 行是后插的，初次观察会挂错父级、永不触发，本拍踩过）。
    ★★ **part105 是跨代资产，不在原地改**：`_read_part()` 按 `PART_DIRS = (part107, part105)`
       双目录回退 ⇒ 本代在 `part107/ctrl-conv.js` 放**逐字副本 + 一处修正**，
       part105 与 `avatar.html` 零影响（⚠ 副本会漂移，已在文件头写明）。

'''

# ================================================================ 3. HANDOFF.md
HANDOFF_G9 = '''**⑨ 第九拍（邵先生 2026-10-01 13:1x 返工 · 两条）** —— 两条都在右栏「全屏」这条线上：
1. **全屏后按钮图标不翻**（真 bug）—— 内联 SVG 是 `browse.html` 写死的「四角朝外」，
   `panel.js` 只翻了 `aria-pressed` / `title` / `aria-label`，`<path d>` 一字未动。
   ⇒ 抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；MAX **从 DOM 读出来缓存**、MIN 硬编码
   （Lucide `minimize` 四条），只切 `d`、不重建节点。
   ★ 目视复核：`raw/j3-bar-1440-{max,min}.png` 两枚字形方向相反。
2. **全屏后拖分栏条「一按就复位」**（真 bug，两个因）——
   (a) `ctrl-conv.js` 的 `startPanel = panelW` 取的是**内部缓存**，而「最大化」绕过控制器直接写
       `--av-browse-w` ⇒ 缓存停在 641、实际 1040 ⇒ 一按下拖动宽度猛跳到 **761**（实测）；
       改读**实际渲染宽**（先 `.is-col-dragging` 停过渡再取几何）并同步缓存。
   (b) `pointermove` / `pointerup` 挂**元素**、只靠 `setPointerCapture` 兜 ⇒ 改挂 **`window`** + `blur`。
   ★ 判据 = 把 `pointermove` **派发到 `document.body`** 仍能拖动（1040 → 960 ✓）。
   另补两条退出路径：**全屏态下按下分栏条 = 放弃全屏**（`setMax(false, true)`，不动宽）；
   **收起侧栏也退全屏** —— 搭 ctrl-conv `setOpen()` 必定 dispatch 的 resize，
   **别用 MutationObserver 盯后插节点的父级**（本拍第一版就这么坏的：观察挂在旧父级、永不触发
   ⇒ `data-td-maxw` 残留、按钮仍是「还原」态）。
★ **体位**：`part105/ctrl-conv.js` 是**跨代资产**（源页 `avatar.html` 的移植源）⇒ 本代按
   `_read_part()` 的双目录回退，在 `part107/ctrl-conv.js` 放**逐字副本 + 一处修正**，
   part105 与 avatar 零影响（⚠ 副本漂移已在文件头写明）。适配层**零 CSS 改动**。
   门禁全绿（幂等 / `check-syntax` 10/10 / `verify-design` 逐字节同 / `scan-flatten` 仍 2 条），
   产物 **930384 → 934109 字符**（+3725），`+2373 / −8` 行。

'''

# ================================================================ 4. PAGES.md
PAGES_TAIL_OLD = '''> **⑧ 全局宽度不足出省略号（三类分治）/ 去掉「折叠此文件」/ `.td-sum-h` 15px / `.td-diff-path` 展开中粗 / `.td-diff-path` 与 `.td-diff-rows` 内 13px / `.r107-stats` 居中**
> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三**节）。'''

PAGES_TAIL_NEW = '''> **⑧ 全局宽度不足出省略号（三类分治）/ 去掉「折叠此文件」/ `.td-sum-h` 15px / `.td-diff-path` 展开中粗 / `.td-diff-path` 与 `.td-diff-rows` 内 13px / `.r107-stats` 居中** ·
> **⑨ 全屏按钮图标随态切换（四角朝外 ⇄ 朝内，切 `<path d>`、不重建节点）/ 全屏态拖拽起点改读「实际渲染宽」（先停过渡再取几何）/ 拖拽事件改挂 `window` / 全屏态按下分栏条＝放弃全屏 / 收起侧栏也退全屏**
> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四**节）。'''

PAGES_ROWS = '''| **全屏按钮图标** | ★ **第九拍 ①**：`browse.html` 里写死的「四角朝外」SVG 是**静态 HTML** ⇒ 光翻 `aria-pressed` / `title` 不够，必须切 `<path d>`。MAX **从 DOM 读出来缓存**、MIN 硬编码（Lucide `minimize` 四条），只改属性、不重建节点 |
| **右栏拖拽起点** | ★ **第九拍 ②**：`ctrl-conv.js` 的拖拽起点一律读**实际几何**（先落 `.is-col-dragging` = `transition:none` 再取 rect ⇒ 拿到**终值**）。⚠ 宿主若**绕过控制器直接写 `--av-browse-w`**（「最大化」就是这样），内部缓存 `panelW` 必然脱节 ⇒ 「一按下就跳回记忆宽」。事件侧：`pointermove` / `pointerup` 挂 **`window`**（磁捕获不可靠） |
'''

# ================================================================ 5. PLAYBOOK.md
PB_BLOCK = '''

## P3.45 ★★ r107 第九拍（两条 · 2026-10-01 13:1x 邵先生返工）

**① 「宿主绕过控制器直接写布局变量」⇒ 内层缓存必然脱节**（拖拽 / 缩放类交互的通病）
* 症状：**全屏后一按下分栏条，宽度猛跳回记忆宽**（实测 1040 → 761），用户描述成「一下就复位」。
* 根因：内层控制器用 `startPanel = panelW`（**闭包缓存**），而外层的「最大化」**绕过控制器**
  直接 `slot.style.setProperty('--av-browse-w', …)` ⇒ 缓存停在 641 而实际 1040。
* 配方：**拖拽第一帧一律读「实际几何」**，并把缓存同步回来。⚠ 两步走：
  ① 先落拖拽态类（本站 = `.is-col-dragging`，规则带 `transition: none`）**停掉过渡**；
  ② 再 `getBoundingClientRect()` —— 此时才是**终值**，否则会读到过渡中间值。
* 判据：`pointermove` 之后的声明值 = `实际起点 ± dx`（**不是** `缓存 ± dx`）。

**② 拖拽的 `pointermove` / `pointerup` 必须挂 `window`（挂元素 = 能跑但脆）**
* 本站 `panel.js` 的标签重排早已挂 `window`，但 `part105/ctrl-conv.js` 一直挂**元素**
  + `setPointerCapture` ⇒ 平时看着没事，**全屏后分栏条贴住窗口左缘**时指针一下就跑出元素；
  一旦捕获没生效（元素被 React 重挂 / `pointerId` 失配）拖动就**中途断掉**。
* ★ **决定性判据**：合成 `PointerEvent` 时把 `pointermove` / `pointerup` **派发到 `document.body`**
  —— 挂 `window` 的照样响应，挂元素的**静默失效**。比「按住鼠标拖」快且可复现。
* 顺带补 `blur` 兜底（防切窗口后一直卡在 dragging）。

**③ 要改跨代移植件 ⇒ 走「本代覆盖件」，别在原目录动刀**
* `_read_part()` 按 `PART_DIRS = (part107, part105)` **顺序回退** ⇒ 在 `part107/` 放**同名文件**
  即可**遮蔽**上游，源页 `avatar.html` 零影响（本仓历代刻意不回头改 `part105/*`）。
* ⚠ 代价 = **副本会漂移** ⇒ 副本头部必须写明「来自哪份、差异点、日后人工同步」。
* 适用判据：要改的代码在跨代件里、且**行为对所有消费页都是改善**（本次 = 拖拽起点更准）。

**④ 别用 `MutationObserver` 盯「后插节点」的父级 —— 会绑在错的元素上**
* 场景：想「右栏收起时退出全屏」，于是观察 `slot.parentElement` 的 class。
* 坑：那条 flex 行与分栏条都是**另一个脚本在 `place()` 里后插**的，本脚本跑得更早
  ⇒ 初次观察挂在**旧父级**、**永不触发**（症状：收起后 `data-td-maxw` 照旧残留、按钮仍「还原」态）。
* 正解：**搭已有的事件流** —— 三个收起入口（页头开关 / × / Esc）最终都走 `ctrl-conv.setOpen(false)`，
  而它**必定 `dispatchEvent(new Event('resize'))`** ⇒ 在同一条 resize handler 里判一下即可（零新监听）。
* 通用化：**「某状态该退出」优先挂到「已有的确定性事件」上，而不是去观察 DOM 的副作用。**

**⑤ 「独占态」（全屏 / 最大化 / 沉浸）必须把**退出路径**列全**
* 本拍齐了三条：① 点按钮还原 ② **拖拽接管**（新）③ **容器收起**（新）。
* 漏 ② = 用户拖一下宽度就与按钮状态不符；漏 ③ = 收起再打开按钮是「还原」字形、宽度却是记忆值，
  且**下一次 resize 会突然弹回全屏宽**。
* 配方：写这类状态前先把「谁会结束它」列成清单、逐条挂上；**退出用 silent 变体**（只改状态、不动尺寸），
  免得「退出动作」本身又触发一次布局跳变。

★ **体位**：本拍**未动** `_mods.html` / `browse.html` ⇒ 不必重跑 `splice107.py` / `make107.py`；
改序 = `part107/panel.js`（就地）+ `part107/ctrl-conv.js`（新建覆盖件） → `apply107.py`。
产物 `930384 → 934109` 字符；`+2373 / −8` 行；门禁全绿；**零 CSS 改动**（`scan-flatten` 仍 2 条）。
'''

# ================================================================ 6. 仓库 MEMORY.md
MEM_IDX_INLINE = '''｜**P3.45=r107 第九拍（两条）** ★★ **宿主「绕过控制器直接写布局变量」⇒ 内层缓存必然脱节**（拖拽起点读缓存 ⇒ 一按下就跳回记忆宽；**第一帧读实际几何，且先停过渡再取 rect 才是终值**） / ★★ **拖拽 `pointermove`/`pointerup` 必须挂 `window`**（挂元素 + `setPointerCapture` 平时能跑、贴边/重挂即断；★ **判据配方 = 把 move 派发到 `document.body`** 看还响不响应） / **改跨代移植件走「本代同名覆盖件」**（`PART_DIRS` 顺序回退；⚠ 副本会漂移，头部写明来源与差异） / **别用 `MutationObserver` 盯「后插节点」的父级**（会绑在旧父级、永不触发；**搭已有确定性事件流** —— 如「收起必定 dispatch 一次 resize」） / **「独占态」要把退出路径列全**（按钮 / 拖拽接管 / 容器收起），退出用 **silent 变体**（只改状态不动尺寸）'''

MEM_R107_G9 = '''> **第九拍（两条）** = ⑬ **全屏后按钮图标不翻**（内联 SVG 是 HTML 写死的「四角朝外」，JS 只翻 `aria-pressed`/`title`/`aria-label`
> ⇒ 抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；MAX **从 DOM 读出来缓存**、MIN 硬编码（Lucide `minimize` 四条），只切 `d`、不重建节点）｜
> ⑭ **全屏后拖分栏条「一按就复位」**（两因：(a) `startPanel = panelW` 取**内部缓存**，而「最大化」绕过控制器直接写 `--av-browse-w`
> ⇒ 缓存 641 / 实际 1040 ⇒ 一按下猛跳 761；改读**实际渲染宽**（先 `.is-col-dragging` 停过渡再取几何）；(b) `pointermove`/`pointerup`
> 挂**元素** ⇒ 改挂 **`window`** + `blur`。★ 判据 = **把 move 派发到 `document.body` 仍能拖**（1040 → 960）。
> 另补两条退出路径：**全屏态按下分栏条 = 放弃全屏**（`setMax(false,true)` 不动宽）· **收起侧栏也退全屏**（搭 resize，不观察 DOM））。
> ★ **体位**：`part105/ctrl-conv.js` 是跨代资产 ⇒ 本代在 `part107/ctrl-conv.js` 放**逐字副本 + 一处修正**（`_read_part()` 双目录回退，part105 与 avatar 零影响）。
'''

# ================================================================ 7. 工作区 MEMORY.md
WS_BLOCK = '''42. ★★ **拖拽 / 缩放类交互，第一帧一律读「实际几何」，别读闭包缓存**（r107 第九拍）：
    宿主脚本**绕过内层控制器直接写布局变量**（如 `--av-browse-w`）时，内层 `startPanel = panelW`
    这种缓存必然脱节 ⇒ 现象是「一按下就跳回旧值」。且**先落拖拽态类（`transition:none`）再取 rect**，
    否则读到的是**过渡中间值**。
43. ★★ **拖拽的 `pointermove` / `pointerup` 必须挂 `window`**（r107 第九拍实证）——
    挂元素 + `setPointerCapture` 平时能跑，**元素贴边 / 元素被重挂**时就断。
    ★ 判据配方：合成 `PointerEvent` 时把 move/up **派发到 `document.body`**，挂 window 的照样响应。
44. ★★ **要改跨代移植件 ⇒ 在本代目录放「同名覆盖件」**（r107 第九拍）：`PART_DIRS=(part107, part105)`
    顺序回退 ⇒ `part107/` 同名文件遮蔽上游，源页零影响；⚠ **副本会漂移**，头部必须写明来源与差异点。
45. ★★ **别用 `MutationObserver` 观察「后插节点」的父级**（r107 第九拍踩过）：另一个脚本 `place()`
    后插的元素，本脚本跑得更早 ⇒ 观察挂在**旧父级**、永不触发。
    ★ 正解 = **搭已有的确定性事件流**（如「容器收起必定 dispatch 一次 resize」）。
    同理：**「独占态」（全屏 / 沉浸 / 最大化）要把退出路径列全**（按钮 / 拖拽接管 / 容器收起），
    退出用 silent 变体（只改状态、不动尺寸）。

'''

# ================================================================ 8. 日志
LOG_BLOCK = '''

### 第九拍（邵先生 2026-10-01 13:1x · 右栏「全屏」两条）

1. **全屏后按钮图标不翻** —— 内联 SVG 是 `browse.html` 写死的「四角朝外」，JS 只翻 `aria-pressed` /
   `title` / `aria-label` ⇒ 抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`，切 `<path d>`
   （MAX 从 DOM 读出来缓存 / MIN 硬编码 Lucide `minimize` 四条），只改属性、不重建节点。
2. **全屏后拖分栏条「一按就复位」** —— (a) 拖拽起点读**闭包缓存** `panelW`（实际 1040、缓存 641）
   ⇒ 改读**实际几何**（先落 `.is-col-dragging` 停过渡再取 rect = 终值）；(b) `pointermove` / `pointerup`
   改挂 **`window`**（原挂元素 + `setPointerCapture`）。另补两条退出路径：全屏态按下分栏条 = 放弃全屏
   （silent，不动宽）；收起侧栏也退全屏（搭 ctrl-conv `setOpen()` 必定 dispatch 的 resize，
   **不观察 DOM** —— 后插节点的父级会绑错，本拍第一版踩过）。
   ★ `part105/ctrl-conv.js` 是**跨代资产** ⇒ 用 `part107/ctrl-conv.js` **覆盖件**
   （`_read_part()` 双目录回退；逐字副本 + 一处修正，part105 与 `avatar.html` 零影响）。
3. **产物**：`conversation.html` 930384 → **934109** 字符（`+2373 / −8` 行）；`base.html` 与其余 8 页逐字节不变。
   门禁：幂等 ✓ / `check-syntax` 10/10 / `verify-design` 与上轮**逐字节同** / `scan-flatten` 仍 2 条（零 CSS 改动）。
   🚫 未 commit / 未 push。
'''


def main():
    # ---- 1
    append_once(ACC, '## 十四、第九拍', ACC_BLOCK, 'acceptance.md · 十四节（第九拍）')

    # ---- 2
    patch(APPLY, [
        ('**第九拍（2026-10-01 13:1x',
         '\n\n体位与历代一致：本脚本 = **净底',
         '\n\n' + APPLY_BLOCK + '体位与历代一致：本脚本 = **净底',
         'docstring 第九拍段'),
    ], 'apply107.py')

    # ---- 3
    patch(HANDOFF, [
        (None, '最后更新：2026-10-01 13:0x', '最后更新：2026-10-01 14:0x', '头行时间'),
        (None, '共**八拍**）—— **新一代（r106 已交付', '共**九拍**）—— **新一代（r106 已交付', '二·g 标题'),
        (None, '（**十三节**，含第二 ~ 八拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.44**；',
         '（**十四节**，含第二 ~ 九拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.45**；', '二·g 引言'),
        ('⑨ 第九拍（邵先生 2026-10-01 13:1x',
         '\n---\n\n## 三、r88 ~ r92 做了什么（前情提要）',
         '\n' + HANDOFF_G9 + '---\n\n## 三、r88 ~ r92 做了什么（前情提要）', '追加 ⑨ 小节'),
    ], 'HANDOFF.md')

    # ---- 4
    patch(PAGES, [
        (None, '2026-10-01 · **共八拍**', '2026-10-01 · **共九拍**', 'P3.11i 标题'),
        (None, '> **八拍要点**：', '> **九拍要点**：', '逐拍要点 · 标题'),
        (None, PAGES_TAIL_OLD, PAGES_TAIL_NEW, '逐拍要点 · 追加 ⑨ / 十四节'),
        ('| **全屏按钮图标** |', '\n\n**⚠ 改这一块之前必看**\n',
         '\n' + PAGES_ROWS + '\n**⚠ 改这一块之前必看**\n', '固定事实表 +2 行'),
    ], 'PAGES.md')

    # ---- 5
    append_once(PLAYBOOK, '## P3.45 ', PB_BLOCK, 'PLAYBOOK.md · P3.45')

    # ---- 6
    patch(REPO_MEM, [
        ('｜**P3.45=r107',
         '｜ skill（用户级）：design-to-code-modular',
         MEM_IDX_INLINE + '｜ skill（用户级）：design-to-code-modular',
         '索引 · 追加 P3.45'),
        (None, '右栏（r107 · 共八拍：', '右栏（r107 · 共九拍：', '索引 · P3.11i 共八拍→九拍'),
        (None, '+ 统计行居中**）**）', '+ 统计行居中** / **全屏按钮图标随态切换（MAX⇄MIN）+ 全屏态拖拽起点修正（读实际几何）+ 拖拽与收起联动退全屏**）**）',
         '索引 · P3.11i 拍次描述补 ⑨'),
        (None, '> **r107（2026-10-01 09:3x ~ 12:4x · 会话详情页「侧栏模块标签化」= 复刻 Codex 右栏 · 八拍）',
         '> **r107（2026-10-01 09:3x ~ 13:1x · 会话详情页「侧栏模块标签化」= 复刻 Codex 右栏 · 九拍）',
         'r107 段 · 标题（八拍→九拍）'),
        (None, '★ 本代**八拍**（同一代、`apply107.py` 就地返工八次、**始终未提交**）',
         '★ 本代**九拍**（同一代、`apply107.py` 就地返工九次、**始终未提交**）',
         'r107 段 · 八拍→九拍'),
        ('> **第九拍（两条）**',
         '> ★ ① 与 ⑥ **可共存**（居中 + 溢出时 Chromium 退化为 `start`、省略号照落行尾））。',
         '> ★ ① 与 ⑥ **可共存**（居中 + 溢出时 Chromium 退化为 `start`、省略号照落行尾））。\n' + MEM_R107_G9,
         'r107 段 · 追加第九拍块'),
        (None,
         '> **产物**：`conversation.html` **799231 → … → 927464 → 930384 Unicode 字符**（八拍合计 **+131153**）；\n'
         '> UTF-8 字节（LF 归一）**1019883** ｜ 工作区字节（CRLF）**1026880** ｜ LF `sha1 c8b5e944e2de`；`base.html` **472150 逐字节不变**。',
         '> **产物**：`conversation.html` **799231 → … → 930384 → 934109 Unicode 字符**（九拍合计 **+134878**）；\n'
         '> UTF-8 字节（LF 归一）**1025618** ｜ 工作区字节（CRLF）**1032684** ｜ LF `sha1 147f703da06f`；`base.html` **472150 逐字节不变**。',
         'r107 段 · 产物与三种口径'),
        (None,
         '> **八查**：幂等 ✓（每拍连跑两遍）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜\n'
         '> `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜\n'
         '> `scan-flatten.py` 改前改后均 **2 条**（无新增压平）｜代数残留 **0**｜\n'
         '> `git status` = `M pages/conversation.html`（`+2299 / −3` 行）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`。\n'
         '> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.44**；各拍要点见 **PAGES P3.11i（共八拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十三节）**。',
         '> **九查**：幂等 ✓（每拍连跑两遍）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜\n'
         '> `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜\n'
         '> `scan-flatten.py` `panel.css` 仍 **2 条**（第九拍**零 CSS 改动**）｜代数残留 **0**｜\n'
         '> `git status` = `M pages/conversation.html`（`+2373 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`。\n'
         '> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.45**；各拍要点见 **PAGES P3.11i（共九拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十四节）**。',
         'r107 段 · 九查 / 改动面 / 引用行'),
    ], 'MEMORY.md')

    # ---- 7
    patch(WS_MEM, [
        ('42. ★★ **拖拽 / 缩放类交互', '\n## 二、Windows 环境速记',
         '\n' + WS_BLOCK.rstrip('\n') + '\n## 二、Windows 环境速记', '硬规则 42~45'),
    ], 'WS_MEMORY.md')

    # ---- 8
    append_once(LOG_REPO, '### 第九拍（邵先生 2026-10-01 13:1x', LOG_BLOCK, '仓库日志 · 第九拍')
    append_once(LOG_WS, '### 第九拍（邵先生 2026-10-01 13:1x', LOG_BLOCK, '工作区日志 · 第九拍')

    print('\n-- 应用 %d 项 / 跳过 %d 项 --' % (len(APPLIED), len(SKIPPED)))
    for s in APPLIED:
        print('   + ' + s)
    for s in SKIPPED:
        print('   = ' + s)


if __name__ == '__main__':
    main()
