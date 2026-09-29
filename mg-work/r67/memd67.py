# -*- coding: utf-8 -*-
"""第 67 轮 B 定稿：把本轮知识固化进 MEMORY.md（4 处精确替换）+ 追加当日日志。"""
import io
import os
import sys

MEM = '.workbuddy/memory/MEMORY.md'
LOG = '.workbuddy/memory/2026-09-29.md'

REPS = []

# ---------- 替换 1：§ 三 强化「注释污染断言」 ----------
REPS.append((
    '三/注释污染',
    """  ⚠️ **新增的注释里不能出现被断言的 token**（r67 实锤）：我在 JS 新注释里写「SHIMMER_SPREAD / bindShimmer
  已移除」，四个残留断言当场全炸 —— 与"禁止全文件关键词总数"属同一类陷阱。
  **注释只描述"做了什么"，不要复述被删（改）的标识符。**""",
    """  ⚠️ **新增的注释里不能出现被断言的 token / 标签名**（r67 **一轮踩了 3 次**）：
  ① JS 注释写「SHIMMER_SPREAD / bindShimmer 已移除」→ 四个残留断言当场全炸；
  ② CSS 块注释写「见页尾 DOT-SPOT v1 块」→ **提前命中 JS 块的 newmark**，JS 块被误判"已存在"而跳过；
  ③ JS 块注释写「本块在 `</body>` 前执行」→ `</body>` 计数断言直接失败。
  ⇒ **注释只描述"做了什么"，不复述被删/被改/被断言的标识符与标签名。**
  **护身符**＝给补丁脚本加一条**元守卫**：直接检查新增块常量里
  `</body>` `</html>` `<body` `<style` `</style>` `<div` `</div>` 的出现次数是否等于允许值
  （见 `mg-work/r67/apply67b.py` 的「自检 E」）—— 把这类复发自动拦下。
  ⚠️ **"有意新增"的标签要用「精确增减量」、不能沿用"零变化"**：本轮有意注入一个脚本块 ⇒
  `<script>`/`</script>` 各 **Δ+1** 才是正确断言（正是铁律里的"被改对象的精确增减量"）。
  ⚠️ **页内本就存在的同名词不可断言绝对值**：`pointermove` 该页原本就有监听 → 只能断言"改前→改后差值"。
  ⚠️ **沿用他处声明的 token 要在本块内断言为 0**：本轮新块沿用 r12 那层的点阵色，
  故 `var(--gray-7)` 在本块内应为 **0**（避免两处口径漂移）。""",
))

# ---------- 替换 2：§ 7.1 加「React 异步挂载」 ----------
REPS.append((
    '7.1/页尾脚本',
    """- **A/B 对照页别放在 `pages/` 里跑校验**：`verify-design.py ./pages` 会把它一并计入（76 → 97）
  → **跑校验前必须先删掉**。""",
    """- **A/B 对照页别放在 `pages/` 里跑校验**：`verify-design.py ./pages` 会把它一并计入（76 → 97）
  → **跑校验前必须先删掉**。
- ⚠️ **页尾同步脚本取不到还没渲染的 DOM**（r67 血泪）：本页是 React 产物，注入的 `<script>` 在 `</body>` 前
  **同步执行**时外壳的 `main` 还不存在 → `document.querySelector('main.dot-bg')` 返回 **null**、监听器永远绑不上。
  症状极具迷惑性：CSS 全绿、`transitionProperty` 也对、伪元素 mask 也在，**就是不动、变量恒为初始值**。
  ⇒ 正解＝**文档级事件委托**（`document.addEventListener('pointermove', e => e.target.closest('main.dot-bg'))`），
  不必等渲染、也不必 `MutationObserver`；再配 rAF 节流（每帧至多写一次变量）。""",
))

# ---------- 替换 3：§ 7.3 加取证三则 + set media ----------
REPS.append((
    '7.3/取证三则',
    """- ⚠️ **同一 URL 可能并存多个 page target**（`task-detail.html` 与 `task-detail.html?fresh`）：
  CDP 里模糊匹配会截到**错的标签页**（probe 报 `open=true` 但截图里没弹窗）→ 必须用 `location.href` **精确匹配**；
  截图前先 `$AB eval 'location.href'` 取真 URL 再传给脚本。""",
    """- ⚠️ **同一 URL 可能并存多个 page target**（`task-detail.html` 与 `task-detail.html?fresh`）：
  CDP 里模糊匹配会截到**错的标签页**（probe 报 `open=true` 但截图里没弹窗）→ 必须用 `location.href` **精确匹配**；
  截图前先 `$AB eval 'location.href'` 取真 URL 再传给脚本。
- ⚠️ **验证"过渡是渐进的"必须用「页内一次性采样」**（r67 血泪）：`派发事件 → sleep → eval` 会误判 ——
  实测 agent-browser 每次 eval 的 CDP 往返有 50~150ms，足以吃掉 260ms 的过渡，读到的永远是终值、
  被误判成"瞬间跳变"。正解：**同一个 eval 里**派发事件 + 用 `setTimeout` 采 8 个点写进 `window.__s`，
  再另起一次 eval 取回。实测曲线 `10% → 18.39 → 33.79 → 47.78 → 65.89 → 83.53 → 90%`
  （5 个中间态 + 明显 ease-out 前快后慢特征）。
- **「某一层零变化」的最强证明 ＝ 把它推到画布外再逐像素比**（r67）：验证"旧版点阵没被动过"时，
  把光斑圆心设成 `-500%` 让它彻底移出 ⇒ 画面只剩旧层，与改前对比 **目标容器内最大差异 = 0**；
  若剩余差异与"同页连拍两张"的对照实验**行数 / y 区间完全一致**，即可判定是页面自身噪声、与改动无关。
- **diff 热力图**（r67）：以"目标特效被移除"的那张为基线，对多个状态的截图求 `ImageChops.difference`
  并**增强 N×**（原始差异很淡 → `point(lambda v: min(255, v*7))`），一眼看出特效的作用范围与位置是否跟随。
- ℹ️ **`agent-browser set media` 可直接模拟媒体特性**（比手写 CDP 省事）：
  `agent-browser set media [dark|light] [reduced-motion]` —— 实测 `transitionProperty` 由
  `--dot-x, --dot-y` / `0.26s` 变为 `none` / `0s`；恢复用 `set media light`。""",
))

# ---------- 替换 4：§ 9.7 升级为「鼠标跟随」完整配方 ----------
REPS.append((
    '9.7/鼠标跟随配方',
    """### 9.7 动画化渐变的「圆心」必须用 `@property` 注册类型（r67 实测）
`radial-gradient(circle 190px at var(--dx) var(--dy), …)` 的圆心若要随 keyframes 移动，
`--dx/--dy` **必须 `@property` 注册**，否则 keyframes 里改值**不插值**（瞬间跳变）：
```css
@property --dx { syntax: '<percentage>'; inherits: false; initial-value: 26%; }
@keyframes wand { 0%,100% { --dx:24%; --dy:30% } 25% { --dx:72%; --dy:26% } }
```
实测：`getComputedStyle(el).maskImage` 的圆心由 `26% 32%` → `47.9983% 28.0001%` ✅
（Chromium/Electron 均支持；项目里已有 `@property --border-beam-angle` 先例）。
用途：让 mask / 柔光的「光斑」巡游 —— **点阵只在光斑内显现**，是最干净、最像 AI 产品登录页的动态波点做法。""",
    """### 9.7 「光斑跟随指针」标准配方（r67 定稿 · base.html 的 `.dot-bg`）
底层点阵**保持原样不动**，只在它上面叠一层深一档的点阵、用 mask 圆形光斑控制可见范围，
圆心由指针驱动 —— 点阵只在光斑内"被照亮"，跟随鼠标移动。

```css
/* ① 必须 @property 注册：否则 transition / keyframes 对自定义属性不插值（瞬间跳变） */
/* ② inherits 必须 true：JS 改不了伪元素样式，变量只能写在主元素上、再由 ::before 继承 */
@property --dot-x { syntax: '<percentage>'; inherits: true; initial-value: 50%; }
@property --dot-y { syntax: '<percentage>'; inherits: true; initial-value: 46%; }
/* ③ 过渡写在**主元素**上最可靠（值先平滑、再被伪元素继承），别写在伪元素上 */
.dot-bg { position: relative; transition: --dot-x 260ms ease-out, --dot-y 260ms ease-out; }
.dot-bg::before {
  content: ''; position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(circle, rgba(var(--gray-8), 0.22) 1.5px, transparent 1.5px);
  background-size: 20px 20px;                       /* 与底层同网格 ⇒ 两层点位逐点重合 */
  -webkit-mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0,0,0,.55) 42%, transparent 78%);
          mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0,0,0,.55) 42%, transparent 78%);
}
@media (prefers-reduced-motion: reduce) { .dot-bg { transition: none; } }  /* 交互响应保留，只去掉缓动 */
```
配套 JS（**必须文档级事件委托**，见 §7.1「页尾同步脚本取不到还没渲染的 DOM」）：
`document.addEventListener('pointermove', e => { const m = e.target.closest('main.dot-bg'); … })`
→ 换算百分比 → rAF 节流 → `m.style.setProperty('--dot-x', px + '%')`。
只在指针落到目标内时更新；**移出后保持最后位置、不回弹**。

**层级**：目标容器 `position: static` 且无 stacking context，唯一子元素是 `relative` ⇒
`::before`（positioned、z-index auto）在 tree order 上位于内容之前 ⇒ 与内容同属绘制步骤 6、**内容压在其上**。
⚠️ 此处**不要**用 `isolation: isolate` 图省事 —— 页内有 `position:fixed; z-index:9999` 的弹窗，
隔离会把 9999 困在容器内、可能被外层元素盖住。

**验收数字**（base.html，1440 视口）：浅点阵 `rgba(107,107,107,.1)` / `20px 20px` / `0% 0%` 与改前一致；
光斑 50/46 → 80/75 → 16/20 → 62/44 精确等于鼠标百分比；60×60 窗口墨量 0.15 → 0.46（3 倍）→ 0.15；
布局 mainRect / kidRect 零位移。

用途：让 mask / 柔光的「光斑」跟随指针或巡游 —— **点阵只在光斑内显现**，是最干净、
最像 AI 产品登录页的动态波点做法。纯 CSS 巡游版把圆心写进 `@keyframes` 即可（见 r67 的 A+D 版）。""",
))

txt = io.open(MEM, encoding='utf-8').read()
n0 = len(txt.encode())
ok = 0
for label, old, new in REPS:
    c = txt.count(old)
    if c != 1:
        sys.exit('✗ [%s] 锚点命中 %d 次（期望 1）' % (label, c))
    txt = txt.replace(old, new, 1)
    ok += 1
io.open(MEM, 'w', encoding='utf-8').write(txt)
n1 = len(txt.encode())
print('MEMORY.md 替换 %d/%d 处 | %d → %d 字节 (%+d)' % (ok, len(REPS), n0, n1, n1 - n0))

# ---------- 追加当日日志 ----------
LOG_APPEND = """

---

## 第 67 轮 B 定稿：动态波点改为「鼠标跟随版」（用户口径调整）

用户原话：「**旧版的波点的色彩和位置不变，深色的波点会跟随鼠标移动**」
⇒ 上一版做的 A+D（浅点阵漂移 + 光斑自动巡游）**被推翻自动动效**：
   · A 层浅点阵**去掉漂移**，色彩 / 位置 / 尺寸与 r12 **一字未变**；
   · D 层光斑圆心改由**指针位置**驱动，配 CSS 过渡做平滑跟随。

**补丁** `mg-work/r67/apply67b.py`（2 处替换，**+3431 B**；首跑 ALL PASS、复跑「应用 0 / 跳过 2 / Δ0」）
① CSS：在 r12 原有两条 `.dot-bg` 规则**之后**追加新块（原规则一字未动，只在其后覆盖）；
② JS：页尾 `<!-- /SHELL-TABS-FIX -->` 与 `</body>` 之间注入 `DOT-SPOT v1` 块。

```css
@property --dot-x { syntax:'<percentage>'; inherits:true; initial-value:50%; }
@property --dot-y { syntax:'<percentage>'; inherits:true; initial-value:46%; }
.dot-bg { position:relative; transition: --dot-x 260ms ease-out, --dot-y 260ms ease-out; }
.dot-bg::before { content:''; position:absolute; inset:0; pointer-events:none;
  background-image: radial-gradient(circle, rgba(var(--gray-8), .22) 1.5px, transparent 1.5px);
  background-size: 20px 20px;
  -webkit-mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0,0,0,.55) 42%, transparent 78%);
          mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0,0,0,.55) 42%, transparent 78%); }
@media (prefers-reduced-motion: reduce) { .dot-bg { transition: none; } }
```
JS 用**文档级事件委托** + rAF 节流，把指针位置换算成百分比写进 `.dot-bg` 的 inline 变量。

### ★ 本轮最大的坑：页尾同步脚本 + React 异步挂载
第一版 JS 直接 `document.querySelector('main.dot-bg')` → **返回 null**，监听器永远绑不上。
原因：脚本在 `</body>` 前**同步执行**时，外壳的 React 还没把 `main` 渲染出来。
症状极具迷惑性 —— CSS 全绿、`transitionProperty` 正确、伪元素 mask 也在，**就是光斑不动、变量恒为初始值**。
⇒ 正解：**文档级事件委托** `document.addEventListener('pointermove', e => e.target.closest('main.dot-bg'))`，
不必等渲染、也不用 MutationObserver。

### ★ 三个 `@property` 硬约束（本轮全部流血验证）
1. 想让 **transition 对自定义属性生效** ⇒ 必须 `@property` 注册类型，否则瞬间跳变；
2. **JS 改不了伪元素样式** ⇒ 变量写在 `.dot-bg` 上，**`inherits` 必须为 `true`** 才能传给 `::before`；
3. transition 写在**主元素**上才可靠（值平滑后再被伪元素继承），别写在伪元素上。

### ★ 取证技巧三则（都值得复用）
1. **「某层零变化」的最强证明 ＝ 把它推到画布外**：把光斑圆心设 `-500%` ⇒ 画面只剩旧版点阵，
   与改前逐像素比 **main 区域最大差异 = 0**；剩下的 26 行差异全在侧栏，且与「同页连拍两张」
   对照实验的**行数、y 区间完全一致** ⇒ 判定为页面自身噪声。
2. **过渡曲线要用「页内一次性采样」**：`派发 → sleep → eval` 会被 CDP 往返延迟（50~150ms）吃掉，
   把 260ms 的过渡读成"瞬间跳变"。正解＝同一个 eval 里派发 + `setTimeout` 采点写进 `window.__s`。
   实测曲线 `10% → 18.39 → 33.79 → 47.78 → 65.89 → 83.53 → 90%`（5 个中间态，ease-out 特征明显）。
3. **diff 热力图**：以「光斑移出画布」为基线，对四张不同鼠标位置的截图求 diff 并增强 7×，
   四块亮斑位置与鼠标落点一一对应 ⇒ 一眼证明"跟着指针走"。
   产出 `ev/31-spot-heatmap.png`、`ev/30-spot-follow.png`（放大对照：墨量 0.15 → 0.46 → 0.15）。

### ★ agent-browser 新能力：`set media`
`agent-browser set media [dark|light] [reduced-motion]` 可直接模拟媒体特性，比手写 CDP 省事。
实测 `transitionProperty`：`--dot-x, --dot-y` / `0.26s` → reduce 下 `none` / `0s`，且光斑仍即时跟随。

### 运行时验收（computed style，权威）
| 项 | 结果 |
|---|---|
| A 层（旧版波点） | `rgba(107,107,107,.1)` / `20px 20px` / `0% 0%` / `animation: none` ⇒ 与改前逐字一致 |
| 光斑跟随 | 50/46 → 80/75 → 16/20 → 62/44（精确等于鼠标百分比）；移出 main 后保持不动、不回弹 |
| 布局 | mainRect [268,48,1164,844] / kidRect [269,49,1162,842] = 改前完全一致；hOverflow = 0 |
| 墨量（60×60 窗口） | 光斑外 0.15 → 光斑内 0.46（3 倍）→ 移开后 0.15 |

### ★ 断言污染这个坑，本轮踩了 3 次（必须记死）
1. CSS 块注释写「见页尾 DOT-SPOT v1 块」⇒ **提前命中 JS 块的 newmark**，JS 块被误判"已存在"而跳过；
2. JS 块注释写 `pointermove` ⇒ 词频差值断言多算 1；
3. JS 块注释写 `</body>` ⇒ `</body>` 计数断言直接失败。
⇒ **新增注释只描述「做了什么」，绝不复述被断言 / 被删的标识符与标签名。**
已在 `apply67b.py` 加**元守卫「自检 E」**：直接检查 `CSS_BLOCK` / `JS_BLOCK` 里
`</body>` `</html>` `<body` `<style` `</style>` `<div` `</div>` 的计数是否等于允许值，自动拦下复发。
（另：`<script>`/`</script>` 因本轮**有意**新增脚本块 ⇒ 期望值是精确 **Δ+1**，不能沿用"零变化"。）

**校验**：`verify-design.py ./pages` → 76 问题（67 warning / 9 info / **0 critical**），
与 HEAD 基线逐条完全一致 ⇒ **零新增**（`pages/gaps.log` 已还原）。

**未推送**：按 §十 约定，本轮用户未要求推送 ⇒ 只留工作区改动待确认。
"""
io.open(LOG, 'a', encoding='utf-8').write(LOG_APPEND)
print('当日日志已追加 | 现 %d 行' % len(io.open(LOG, encoding='utf-8').read().split('\n')))
