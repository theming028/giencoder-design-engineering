# r109 验收 · 会话详情页右栏（第一拍「批注链路四件重做」+ 第二拍「五条 + 一条配套」+ 第三拍「批注原点 / 卡片对齐 / 全站暗色」）

> 需求（邵先生 2026-10-02 08:5x，逐字）：
> ① 「右栏浏览器模式下，`td-page-blank` 这个容器要删除」；
> ② 「`td-annot-bar` 这个容器要显示到上面去，不要显示在下面，不容易被注意到」；
> ③ 「`td-url-annot` 这个批注按钮，在进入批注模式后，按钮就变成红色系的『退出批注』按钮」；
> ④ 「这个发起批注 `td-elnote` 的设计请使用我自己的设计方案 …… 请精确的像素级还原，如果有不明确的就询问我」。
>
> 邵先生补充的四条澄清（逐字）：
> · 稿2 顶部那段话 → **「就是输入框的内容示例」**；
> · 高度行为 → **「输入的文字多了后才自动向下撑开，最高撑高到200px，溢出就内滚」**；
> · Ctrl 联动 → **「按钮 + 提示都变」**；
> · 「退出批注」的红 → **「浅底红 + 红字」**；
> · 追问答 → 提示 **「字不变，只高亮后半句」**、卡高 **「按行数算，1 行=86」**。
>
> ★ 长期硬约束（沿用）：**绝对不得改动其他不必涉及的模块**；**完全确保整体产品的稳定性不被破坏**；**只落地静态交互**。
> ★ 本代**是新一代**（r108 十九拍已于 2026-10-02 交付并推送 `172e580`）⇒ 按硬规则「**已交付才新建 rNN+1**」
>   开 `mg-work/r109/`，**不再就地返工 `apply108.py`**。

---

## 零、产物与口径（★ 三种口径勿混用）

| 项 | 读数 |
|---|---|
| 前置 | r108 十九拍 → **`172e580`**（已推送）；记忆同步 `0e1afe0`；`HEAD` 工作区干净 |
| 本代补丁 | **新建** `mg-work/r109/apply109.py`（**3647 行 / 190523 字符**）—— 由 `ev/make109.py` 从 `apply108.py` 做精确替换生成 |
| 本拍补丁 | `ev/patch109l1.py`（39802 B，6 条编辑 / 跨层自检 1 套 / `--check` 模式） |
| 资产 | `part109/{_head.html 4792（**+0，一字未动**） / _mods.html 71501（+434） / panel.css 83427（+6658） / panel.js 77185（+4994） / browse.html 106685（+434，`ev/splice109.py` 的产物）}` |
| 设计稿素材 | `raw/design1-initial.png`(748×168) · `design2-typing.png`(748×288) · `anchor-18332.png`(96×96) · 四张 MCP 导出 SVG · `node_1409-18319/1204-18467/1409-18332.json` |
| 真机截图 | `raw/{a-note-empty, b-note-typing, c-note-ctrl, d-note-reopen, e-note-18px}.png` + 四张整屏 |
| `pages/conversation.html` | **1024825 → 1036907 Unicode 字符（+12082）**；行 **8488 → 8733（+245）**；UTF-8 字节（LF 归一）1137298 → **1154553（+17255）**；工作区字节（CRLF）**1163285** |
| **其余 9 页** | **`base.html`（472150 字符，逐字节不变）+ 8 个外壳页 —— 一页都没动**（`git status` 里只有 `conversation.html` 一个 ` M`） |
| 幂等 | ✓ `patch109l1.py` 连跑两遍均「**应用 0 / 跳过 6**」且跨层自检「全部存活 ✓」、`conversation.html` md5 原地不变（`b580edfefa92e41dac3b59681d5192f8`）；✓ `apply109.py` 第二遍「base.html / conversation.html 均已是目标态（无改动）」 |
| JS/CSS 语法 | `python mg-work/check-syntax.py pages/*.html` ⇒ **10/10 通过**（conversation `script=9 style=16`，与 r108 一致） |
| 设计回归 | `python verify-design.py ./pages` ⇒ **md5 `3dbf654337559509110899e48bef1b1c`**，与 r107 基线 `vd-r107l2.txt` / 本代 `vd-l1.txt` **逐字节相同** ⇒ **零新增、一处渐变都没引** |
| 字号压平 | `python mg-work/r108/ev/scan-flatten.py mg-work/r109/part109/panel.css` ⇒ **2 条**（= 基线 `.td-mod-bar` / `.td-url`，与 r107/r108 同） |

> ⚠ 工作区字节 − blob 字节 = 「行数」个字节 = `core.autocrlf=true` 的行尾差，**不是内容改动**。
> ⚠ 本页字符数**必须**先归一化行尾再比：`len(text.replace('\r\n','\n'))`。

---

## 一、★ 本代体位：`GENS` 扩到七代，nav 继续沿用 `r106-nav-js`

```python
GENS = (('r93', …), ('r101', …), ('r102', …),
        ('r106', 'r106-conv-css', 'r106-conv-js', 'r106-nav-js'),
        ('r107', 'r107-conv-css', 'r107-conv-js', 'r106-nav-js'),
        ('r108', 'r108-conv-css', 'r108-conv-js', 'r106-nav-js'),
        ('r109', 'r109-conv-css', 'r109-conv-js', 'r106-nav-js'))   # ← 本代新增
NAV_TAG = 'r106'      # build_nav_js / 残留自检都用它
```

★ **CSS / JS 两块换名成 `r109-conv-*`**（本代两块都改了）；**nav 块一字未改 ⇒ 按硬规则「跨代沿用的宿主标记不换名」继续用 `r106-nav-js`** ——
收益：`base.html` + 8 个外壳页**逐字节不变**，本代仍只有 `conversation.html` 一页进 `git diff`。

```
   base.html            已是目标态（无改动）
   conversation.html    1024825 → 1036907 (+12082)  应用
```

★ `PART_DIRS` 也扩成四级回落：`part109` → `r108/part108` → `r107/part107` → `r102/part105`（本代只覆盖改过的三件）。
★ 改序（硬规则「双层产物只能下→上改」）：
`part109/{_head.html, _mods.html, panel.css, panel.js}` → `ev/splice109.py` → `apply109.py`（`browse.html` 是 splice 的**产物**，禁手改）。

---

## 二、落地 ① `td-page-blank` 容器删净（DOM + CSS 双清零）

**改前**：`_mods.html` 里 `.td-page` 的头部有一条演示用的 26px 灰带
`<div class="td-page-blank">&nbsp;</div>`，`panel.css` 里配一条
`.td-page-blank { height: 26px; margin: -12px -12px 12px; background: var(--color-fill-2); }`。

**落地**：**DOM 与规则两处都删**（不留死规则 —— 上一拍的 DOM 已删，本拍补 CSS 这一半）。

* `part109/_mods.html`：删元素，原地留说明注释（`<!-- r109-l1 ①：… -->`）。
* `part109/panel.css`：删整条规则，原地留 `/* r109-l1 · ① td-page-blank 已删 */` 留痕。

**真机**：`pageBlankCount: 0`（`p109a.js`，查 `document.querySelectorAll('.td-page-blank').length`）。

### 2.1 ★ 守卫判据必须先剥注释（本拍第一次踩）

`splice109.py` 里原本写的是「产物里**不得**再出现 `class="td-page-blank"`」，结果归零断言一开始就**假报失败** ——
绊倒它的是**我自己那段说明注释**（注释正文里逐字写了「这里原有 `<div class="td-page-blank">&nbsp;</div>`」）。
**修法**：所有「归零」类判据一律先剥 HTML 注释再查：

```python
bare = re.sub(r'<!--.*?-->', '', out, flags=re.S)      # ★ 先剥注释
assert 'class="td-page-blank"' not in bare
```

> 这是硬规则「**判据不能写裸词**」的**第三种形态**：不只是「裸词被无关文案命中」，还包括
> 「**判据被自己的解释性注释命中**」—— 注释里引用被删元素的名字，是最自然的写法，也最容易把守卫绊倒。

### 2.2 `splice109.py` 的四条守卫（顺序有意义）

```python
bare = re.sub(r'<!--.*?-->', '', out, flags=re.S)
assert 'class="td-page-blank"' not in bare          # ① 归零
assert 'data-td-annot-bar' in bare                  # ② 标注条还在
i_view = out.index('data-td-view'); i_bar = out.index('data-td-annot-bar'); i_page = out.index('class="td-page"')
assert i_view < i_bar < i_page                      # ③ 标注条已挪到 .td-view 首位（见第三节）
assert '<span>标注</span>' in bare                  # ④ 工具条那枚按钮未被动
```

产物 `part109/browse.html` = **106685 字符**（r108 的 106251 ⇒ **+434**，与 `_mods.html` 的 +434 一致）。

---

## 三、落地 ② `td-annot-bar` 贴顶（★★ 只改 CSS 不够，必须连 DOM 一起挪）

**改前**：`.td-annot-bar` 是 `.td-view` 的**末位子件**，CSS 是 `position: sticky; bottom: 0;`。
表现：标注条沉在右栏底部，邵先生说「不容易被注意到」。

**落地（两处一起才生效）**：

1. **DOM**（`part109/_mods.html`）：把整块 `.td-annot-bar` 从 `.td-view` **末尾**挪到 **`.td-view` 内首位子件**
   —— 位置在 `<div class="td-page">` **之前**。
2. **CSS**（`part109/panel.css`）：`bottom: 0` → **`top: 0`**（`z-index: 2` 不动）。

### 3.1 ★★ 为什么只改 `bottom:0 → top:0` 不出来

`position: sticky` 的 `top` 约束**只在元素是「滚动容器里首个可滚动子件」之前**才追得上：
元素排在滚动内容**末尾**时，页面滚到它上方时 sticky 的 `top` 已经**追不上**（它的静态位置本就在视口之下，
sticky 只能把它往下拽到 `top` 边界以内 —— 而它根本还没进视口）。
⇒ **必须把它挪成 `.td-view` 的首位子件**，`top: 0` 才有意义。

真机（`p109a.js` / `a1.json`）验证四个量：

| 量 | 读数 | 说明 |
|---|---|---|
| `barIsFirstChild` | **`true`** | DOM 侧首位子件（另查 `i_view < i_bar < i_page`） |
| `bar.position` | `"sticky"` | computed |
| `bar.top` / `bar.bottom` | **`"0px"`** / `"auto"` | 已换向 |
| `bar.dTop` = `bar.top − view.top` | **`0`** | 贴到 `.td-view` 顶沿，分毫不差 |

其余：`barCount: 1`（唯一）、`barHiddenBefore: true`（进标注态前隐藏）、`barHiddenAfter: false`（进标注态后可见）、
`bar.box.w: 629`（撑满右栏）、`bar.bg: rgb(55, 112, 247)`（主色）。

---

## 四、落地 ③ `td-url-annot` → 红色系「退出批注」

**改前**：`.td-url-annot[aria-pressed='true'] { background: var(--color-primary-1); color: var(--color-primary-6); }`
（浅**蓝**底 + 蓝字），文案恒为「标注」。

**落地（两处）**：

* **CSS**：按邵先生「**浅底红 + 红字**」——
  `background: var(--color-danger-light-1)`（= red-1 **`#FFECE8`**）+ `color: var(--color-danger-6)`（= red-6 **`#F53F3F`**）。
  **全部走 DS token，零硬编码 hex。**
* **JS**（`panel.js` 的 `setAnnot(on)`）：进入/退出批注态时改文案 `标注 ⇄ 退出批注`。

```js
for (var i = 0; i < annotBtns.length; i++) {
  annotBtns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
  /* ★ r109-l1 ③：工具条那枚「标注」进入批注态后改文案为「退出批注」。
     ⚠ 只认 `.td-url-annot` —— 标注条里那枚「完成」也带 `data-td-annot`，不动它。 */
  if (annotBtns[i].classList.contains('td-url-annot')) {
    var lb = annotBtns[i].querySelector('span');
    if (lb) lb.textContent = on ? '退出批注' : '标注';
  }
}
```

★ **判据必须带上下文**：全 `_mods.html` 里 `data-td-annot=` 共 **2** 处 —— `td-url-annot` 与标注条里的「完成」，
所以点击处理是共用的，**只有文案切换需要区分**（靠 `.contains('td-url-annot')`，不靠下标、不靠顺序）。

真机（`a1.json`）：

| 量 | 进入批注态前 | 进入后 |
|---|---|---|
| `uaLabel` | `"标注"` | **`"退出批注"`** |
| `uaBg` | `rgba(0, 0, 0, 0)` | **`rgb(255, 236, 232)`** = red-1 |
| `uaColor` | （缺省） | **`rgb(245, 63, 63)`** = red-6 |
| `uaBorder` | `rgba(0, 0, 0, 0)` | `rgba(0, 0, 0, 0)`（无框，与设计一致） |

> 另注：`aria-pressed` 是**既有**语义（本轮沿用），文案与红态都挂在它上面 ⇒ 可访问性不留缺口。

---

## 五、落地 ④ `td-elnote` 三稿逐像素重做（★ 本拍最大件）

### 5.1 三张稿的精确参数（**已逐像素量出**，全部以「卡片描边外沿」为逻辑原点 · 1×）

| | 稿1 初始态（356×48）<br>`1409:18319` | 稿2 输入态（356×108）<br>`1204:18467` | 稿3 锚点（24×24）<br>`1409:18332` |
|---|---|---|---|
| **pin** | 24×24 @(0,12)：白底 + `2px solid #3770F7` 描边 + `border-radius: 12px 12px 12px 0`（**左下角纯直角**）+ 中心 6px 实心蓝点 | 同左 | 整块实心 `#3770F7` + 白 `1`；`font-size:12px / line-height:16px / font-weight:500` |
| **卡片** | 320×48：白底 + `1px #E5E5E5` + 8 圆角 + `0 4px 12px rgba(0,0,0,.08)` | 320×108 同款 | — |
| **输入区** | 占位「输入你的注释」14px `#A9A9A9`，墨迹 @(12.5,17)–(95,30) | 296×44 @(12,12)；14px / 22 两行（行 1 墨迹 y16~29.5、行 2 y38~51） | — |
| **底行** | — | 296×28 @(12,68)：左提示墨迹 @(13,77)–(158,88.5) 12px `#A9A9A9`；gap 8；「取消」48×28 @(204,68) + 「添加」48×28 @(260,68) | — |
| **按钮** | 「添加」48×28 底 `#DAE4FE` 白字（**禁用**）、圆角 4、12px | 「取消」= 白底 + `1px #E5E5E5` 描边 + 黑字；「添加」= `#3770F7` 白字；均 12px / 圆角 4 | — |
| **卡内距** | **12 = 1px 描边 + 11px padding**（`left:12 width:296` 从描边**外沿**起算） | 同 | — |

### 5.2 ★ 三条从稿子里反推出来的「公式」（写进 CSS 注释，防后人改坏）

1. **内距 12 = 1px 描边 + 11px padding**
   稿2 的底行写的是 `left:12 width:296`、**从描边外沿起算**。全局 `box-sizing: border-box` 下，
   只有 `padding: 11px` 才对得上（独立佐证：量到的正文墨迹左沿 = 卡左 + 13 = 描边 1 + 内距 12）。
   ⇒ **不是 `padding: 12px`**。
2. **卡高公式（邵先生「按行数算，1 行=86」）= `12 + 22n + 12 + 28 + 12`**
   ⇒ 空态 **48**、1 行 **86**、2 行（稿2）**108**。CSS 侧靠「输入区按内容高撑 + 卡片 `height:auto`」自洽，
   不写死数字（这样 `--ui-fs` 换档自动跟随）。
3. **封顶 200 + 溢出内滚**（邵先生「最高撑高到200px，溢出就内滚」）
   ⇒ 卡片 `max-height: calc(200px * var(--ui-fs-ratio))` + `overflow: hidden`；
   **输入区 `overflow-y: auto` 自己滚**（不是卡片滚）—— 底行因此常驻不被顶走。

### 5.3 CSS 侧：整块旧气泡换掉（10 条选择器 + 旧块 9 条归零）

旧「元素评论气泡」整块（`.td-elnote` / `[hidden]` / `-t` / `-t b` / `textarea` / `:focus` / `-f` / `-f button` / `.is-primary`）
**全部替换**为新的一套（片段见 `part109/panel.css` 的 `/* r109-l1 · ④ 元素评论气泡 + 已批注锚点 */` 段）：

```
.td-elnote            position:absolute; z-index:3; left:12px; width:356px; max-width:calc(100% - 24px);
                      display:flex; align-items:flex-start; gap:12px
.td-elnote[hidden]    display:none
.td-elnote-pin        24×24 · margin-top 12 · border 2px solid --color-primary-6
                      · border-radius 12/12/12/0 · 底 --color-bg-2
.td-elnote-pin::after 6×6 圆点 · 居中 · --color-primary-6
.td-elnote-pin.is-done  实心主色 + 白字 · 500 / line-height 16   ← 稿3 的「已批注」外形
.td-anchor            同形同色，落点另算（见 5.5）
.td-elnote-card       flex:1 1 auto · row · gap 12 · height 48 · max-height 200 · overflow hidden
                      · padding 11 · border 1px --color-border-2 · 圆角 8 · --shadow2-down
.td-elnote-card.has-text  column / stretch / height auto          ← 有内容才纵列
.td-elnote-input      block · flex:1 1 auto · min-height 0 · width 100% · border 0
                      · resize none · overflow-y auto · line-height 22 · --color-text-1
.td-elnote-input::placeholder  opacity 1 · --color-neutral-5      ← 压过页面全局灰
.td-elnote-foot       flex none · space-between · gap 12
.td-elnote-card:not(.has-text) .td-elnote-hint,
.td-elnote-card:not(.has-text) .td-elnote-cancel   display:none   ← 稿1 没有提示、没有取消
.td-elnote-hint       ellipsis 单行 · 12px · --color-neutral-5
.td-elnote-hint em    font-style: normal                          ← 语义化「后半句」载体
.td-elnote-card.is-ctrl .td-elnote-hint em  --color-primary-6      ← Ctrl 只点亮后半句
.td-elnote-acts       flex none · gap 8
.td-elnote-acts .giencoder-btn              padding 0 11px · 12px
.td-elnote-acts .giencoder-btn:not(:focus-visible)  box-shadow:none
.td-elnote-ok[disabled]  --btn-bg: --color-primary-2 · opacity 1 · cursor default · pointer-events none
```

★ **三处「DS 默认值 vs 稿子」的对齐**（都写进了 CSS 注释）：

| 差 | DS 默认 | 稿子 | 处置 |
|---|---|---|---|
| 内距 | `padding: 0 16px`（small 档 12） | 字宽 24 + 左右各 12 = **48 宽** | `padding: 0 11px` —— DS 的 `.giencoder-btn` 自带 `border: 1px solid #0000` ⇒ 11 + 1 = 12 |
| 字号 | `--font-size-body-3`（14） | **12px**（墨迹宽 22.5 ≈ 24 − 字侧边距） | `font-size: var(--font-size-body-1)` |
| 那圈 ring | `.giencoder-btn-primary` 带 `box-shadow: 0 0 0 1px var(--btn-ring)` | 48×28 **净尺寸** | `:not(:focus-visible) { box-shadow: none }` —— **留住** `:focus-visible` 的焦点环（可访问性不能一起干掉） |

★ **禁用态不走 DS**：DS 的 `.giencoder-btn[disabled] { opacity: .4 }` 主色叠 40% 会得到 `#AFC6FA`，
与稿子的 `#DAE4FE` 差得远 ⇒ 改 `--btn-bg: var(--color-primary-2)`。
**为什么能这么改**：DS 的 primary 里写的是 `--btn-ring: var(--btn-bg)` + `box-shadow: 0 0 0 1px var(--btn-ring)`
—— 自定义属性**在使用时才解析** ⇒ 换 `--btn-bg` 会把底色和那圈同色 ring **一起**换掉。
同时 `opacity: 1` 覆掉 DS 的 `.4`、`pointer-events: none` 保住「点不动」。

★ **`:focus-visible` 上的 `:not()` 不是洁癖**：DS 的 `.giencoder-btn:focus-visible` 是键盘可达性的唯一视觉反馈，
本层的 `box-shadow: none` 若不带 `:not()`，会把焦点环一起删掉。

### 5.4 JS 侧：气泡交互重做（`panel.js`，段见源码）

```js
elnote.innerHTML =
    '<span class="td-elnote-pin" aria-hidden="true"></span>'
  + '<div class="td-elnote-card">'
  +   '<textarea class="td-elnote-input" rows="1" aria-label="元素评论" placeholder="输入你的注释"></textarea>'
  +   '<div class="td-elnote-foot">'
  +     '<span class="td-elnote-hint">Enter添加，<em>Ctrl+Enter发送</em></span>'
  +     '<span class="td-elnote-acts">'
  +       '<button type="button" class="td-elnote-cancel giencoder-btn giencoder-btn-size-small giencoder-btn-secondary" data-td-elnote-cancel="1">取消</button>'
  +       '<button type="button" class="td-elnote-ok giencoder-btn giencoder-btn-size-small giencoder-btn-primary" data-td-elnote-ok="1" disabled>添加</button>'
  +     '</span></div></div>';
```

新增状态与函数：`noteCard / notePin / noteTa / noteOk / noteCancel`、`noteList[]`、`noteCur`、`noteCtrlOn`、
`noteFind(el)`、`noteGrow()`、`noteCtrl(on)`、`noteEdit(el)`、`noteDrop(el,n)`、`noteCommit()`。

```js
function noteGrow() {                       /* 卡高 = 12 + 输入区 + 12 + 28 + 12（空态锁 48） */
  var has = noteTa.value.replace(/\s+/g, '') !== '';
  noteCard.classList.toggle('has-text', has);
  if (noteOk) noteOk.disabled = !has;
  if (!has) { noteTa.style.height = ''; return; }
  noteTa.style.height = 'auto';
  noteTa.style.height = noteTa.scrollHeight + 'px';
}
function noteCtrl(on) {                     /* 邵先生：「按钮 + 提示都变」「字不变，只高亮后半句」 */
  noteCtrlOn = on;
  noteCard.classList.toggle('is-ctrl', on);   /* 后半句高亮交给 .is-ctrl（CSS） */
  if (noteOk) noteOk.textContent = on ? '发送' : '添加';
}
```

★ **`noteCommit()` 不再 `setAnnot(false)`**（本拍的语义决定）：
稿3 的存在说明「**加完一条留在批注模式**」才是原意 —— 加完就退出的话，锚点根本来不及被看到。
锚点**常驻**（与 Figma 批注同族：它是「页面上已经存在的意见」，不随批注模式开合）。

★ **事件与兜底**：
* `elnote.addEventListener('click', e => e.stopPropagation())` —— 气泡挂在 `.td-view` 里，
  它自己的点击会冒到 view 那条「点元素开气泡」的监听上 ⇒ 点「取消」会顺手把气泡**重新打开**。断在气泡这层。
* `noteTa` 的 `Enter` ⇒ `preventDefault()` + `noteCommit()`（稿2 提示写的是「Enter添加，Ctrl+Enter发送」，
  静态演示里两者落到同一枚提交上；顺手拦掉换行，免得输入框里长出一行）。
* **Ctrl 挂在 `document` 上**（邵先生说的是「按下 ctrl 键」，不该限定焦点在输入框里）：
  `keydown/keyup` 判 `e.key === 'Control'`；`window.blur` 兜底归位（切走窗口时不卡在「发送」态）。

### 5.5 稿3 锚点落点：**被标注元素的右上角**（★ 稿子未给，本层取通行读法）

```js
a.style.left = (er.right - vr.left + view.scrollLeft - 12) + 'px';
a.style.top  = (er.top   - vr.top  + view.scrollTop  - 12) + 'px';
```

`−12` = 让 24×24 的锚点**中心咬住那个角**。稿子只给了锚点长相、没给落点 ⇒ 取「右上角」（Figma 批注同款）。
**若有偏差请邵先生指定。**

### 5.6 ★★ 真机踩到的功能性 Bug：重开气泡时回填文本被压成 0 高

**现象**：已批注元素重开气泡，卡片停在 **48** 而应 **108**（截图只剩底行）。

**根因**：`noteEdit()` 里先调 `noteGrow()`、后 `removeAttribute('hidden')`。
`noteGrow()` 用 `ta.scrollHeight` 定高，而此刻气泡还在 `display: none` 下 ⇒ **`scrollHeight` 恒为 0**
⇒ 回填的长文本被压成 0 高。

**修**：`noteEdit()` 里把 `noteGrow()` 移到 `removeAttribute('hidden')` **之后**，
并在 `patch109l1.py` 的 `verify()` 里加一条**静态判据**（`i_unhide < i_grow`），防回归：

```js
function noteEdit(el) {
  …
  elnote.style.top = (er.bottom - vr.top + view.scrollTop + 8) + 'px';
  elnote.removeAttribute('hidden');      /* ★★ 先摘 [hidden] … */
  noteGrow();                            /* ★★ … 再量几何（隐藏元素量不出 scrollHeight） */
}
```

复测（`d1.json`）：`reopen.cardH: 108 / taH: 44 / taInlineH: "44px"`，截图 `raw/d-note-reopen.png` 正确。

> 与硬规则「**摘 `[hidden]` + 挂开态类必须在同一 tick 之外留一次重排**」**同族**：
> 「隐藏元素量不出几何」是这条规则的另一张脸 —— 不只是过渡被跳过，连**布局量**都是假的。

### 5.7 逐像素对照（`ev/pix109.py` → `pix109.log`）

**定标**（实测确认）：设计稿是 **scale=2** 导出；**卡片描边外沿在 PNG 的 (72, 28)**；
⇒ 逻辑 `x = (imgX − 72)/2 + 36`、`y = (imgY − 28)/2`（`+36` 是因为卡片在 356 宽的弹层里从 36 起）。
真机元素截图是 **1×**（`screenshot "<sel>"` 直接出 356×48 / 356×108），卡片描边外沿就在 (36, 0)。

#### 稿1 空态（`design1-initial.png` ↔ `a-note-empty.png`，356×48）

| 地标（卡内逻辑 px） | 设计稿 | 真机 | 差（真机−设计） | |
|---|---|---|---|---|
| 卡片 `#E5E5E5` 描边外框 | (0, 0, 320, 48) | (0, 0, 320, 48) | **(0, 0, 0, 0)** | OK |
| 「添加」禁用钮 `#DAE4FE` | (262, 10, 310, 38) | (260, 10, 308, 38) | (−2, 0, −2, 0) | ★ 已知 |
| 占位墨迹 `#A9A9A9` | (12.5, 17, 95, 30) | (13, 17, 95, 30) | (+0.5, 0, 0, 0) | OK |

取样：设计「添加」底 `(218,228,254)` / 真机 `(218,228,254)` —— **逐字节同**；
设计占位墨 `(180,180,180)` / 真机 `(195,195,195)` —— 差在**取样点落在字形的哪一半**（AA 边缘），非色差。

> **★ 唯一已知偏差（有意）**：稿1 的「添加」停在卡右缘内 **10px**、稿2 停在 **12px** ——
> 同一枚按钮在手放的两稿里差 2px，本层**统一取 12**（稿2 那侧是自动布局值）。
> 若要严格照稿1，需给「空态」单独加一条 `.td-elnote-card:not(.has-text) .td-elnote-acts { margin-right: -2px }`，请邵先生定夺。

#### 稿2 输入态（`design2-typing.png` ↔ `b-note-typing.png`，356×108）

| 地标（卡内逻辑 px） | 设计稿 | 真机 | 差 | |
|---|---|---|---|---|
| 卡片 `#E5E5E5` 描边外框 | (0, 0, 320, 12) | (0, 0, 320, 12) | **(0, 0, 0, 0)** | OK |
| 正文第 1 行墨迹 `#1F1F1F` | (13, 16, 305, 29.5) | (14, 17, 305, 29) | (+1, +1, 0, −0.5) | OK |
| 正文第 2 行墨迹 | (13.5, 38, 171.5, 51) | (13, 39, 169, 51) | (−0.5, +1, **−2.5**, 0) | ★ 文本尾部 AA |
| 底行提示墨迹 `#A9A9A9` | (13, 77, 158, 88.5) | (13, 77, 153, 88) | (0, 0, **−5**, −0.5) | ★ 尾字 AA |
| 「取消」次钮 `#E5E5E5` 描边 | (204, 68, 252, 96) | (204, 68, 252, 96) | **(0, 0, 0, 0)** | OK |
| 「添加」主钮 `#3770F7` | (260, 68, 308, 96) | (260, 68, 308, 96) | **(0, 0, 0, 0)** | OK |

取样：设计「添加」底 `(55,112,247)` / 真机 `(55,112,247)` —— **逐字节同**。
★ 两处「超 1px」都在**字形右沿**（文本尾部最后一笔的抗锯齿落点），不是布局差：
下方取样行也说明同一件事 —— 设计正文取样 `(176,176,176)` vs 真机 `(244,244,244)`，
差在**取样点落在字形的哪一半**（字间空白 vs 笔画上），不是色差。
**结构性地标（卡框、两枚按钮）全部差 0。**

#### 稿2 的 Ctrl 态（设计稿没有这一帧，看「只改该改的」）

| 量 | 读数 | 判据 |
|---|---|---|
| 主钮尺寸 `#3770F7` 外框 | (260, 68, 308, 96) | 与稿2 **完全一致**（文案变长不撑宽 —— 48 是 `min-width` 的结果，不是被文案撑的） |
| 提示前半句墨迹 | (13, 77, 68, 88) | 与稿2 一致（**不动**） |
| 提示后半句墨迹 | (104, 78, 151, 87) | 落在 `#3770F7` 区（**只点亮后半句**） |

真机 computed（`c1.json`）：

| 量 | Ctrl 前 | Ctrl 后 |
|---|---|---|
| `okTxt` | `"添加"` | **`"发送"`** |
| `emColor`（后半句） | `rgb(169, 169, 169)` | **`rgb(55, 112, 247)`** |
| `hintColor`（整块） | `rgb(169, 169, 169)` | `rgb(169, 169, 169)`（**不变** —— 前半句不动） |
| `cardCtrl`（`.is-ctrl`） | `false` | `true` |
| `okBox` 宽 | `48` | `48`（**不变**） |

#### 稿3 锚点（`anchor-18332.png` / `node_1409-18332.json` ↔ `d-brw-anchored.png`）

真机（`d1.json`）：

```
anchor.box  = 24 × 24        anchor.bg/color   = rgb(55,112,247) / rgb(255,255,255)
anchor.txt  = "1"            anchor.fs / fw / lh = 12px / 500 / 16px
anchor.br   = "12px 12px 12px 0px"      anchor.bw / bc = 2px / rgb(55,112,247)
anchorVsTarget = { dRight: 12, dTop: -12 }      ← 右上角落点
anchorCount = 1            anchorInView = true
okTxtAtCommit = "发送"     noteHidden = true     isAnnotating = true   barVisible = true
```

★ 稿3 把数字写成 `left: 9px; top: 4px` 的绝对定位 —— 那是「24 盒里居中一个单字」的**产物**，
本层用 flex 居中表达同一件事（两位数也不会跑偏），真机 `br / bg / color / fs / fw / lh` 五项与稿3 全等。

#### 重开气泡回填（`d-note-reopen.png`）

```
reopen.isDone      = true            pin 变实心态
reopen.num         = "1"
reopen.bg/color    = rgb(55,112,247) / rgb(255,255,255)
reopen.dotContent  = "none"          ::after 的点已撤
reopen.taVal       = "正常输入文字时，卡片右下角是回车按钮，按下回车键即可添加此条注释。"   ← 原文回填
reopen.hasText     = true            reopen.okDisabled = false
reopen.cardH       = 108             reopen.taH = 44      reopen.taInlineH = "44px"
```

### 5.8 200px 压顶 + 内滚 + 字号杠杆（`--ui-fs: 18` 档 · `p109e.js` / `e1.json`）

把页面根字号杠杆推到 **18**（`ratio = calc(18 / 14)`）后重测三态：

| 态 | 读数 |
|---|---|
| 空态 | `note 356×61.7` / `card 313.16×61.7` / `pin 30.84` / `ta 222.31×28.28`（`lh 28.2857px`、`fs 18px`）/ `ok 54.84×36` |
| 输入态 | `note/card 356×157 / 313.16×157`；`ta 289.16×85`；`foot 289.16×36 @y584.08`；`hint 159.47×28.28` |
| **长文本压顶** | `card 313.16×**257.14**`；`ta 289.16×**185.14**`；`taScrollH 509 > taClientH 185` ⇒ **`taCanScroll: true`**；`maxh "257.143px"`；`cardOverflow "hidden"`；`footVisible 36` |
| 横向溢出 | **`docOverflowX: 0`** |

三条结论：
1. **封顶是「按比例」的**：`257.14 = 200 × 18/14` —— 走 `max-height: calc(200px * var(--ui-fs-ratio))`，
   随字号杠杆等比放大，**不是写死 200**（DS 字号杠杆的既定体位）。
2. **滚动发生在输入区**（`taCanScroll: true`），卡片本身 `overflow: hidden` ⇒ **底行常驻不被顶走**（`footVisible: 36`）。
3. 同档其余几何全部等比：`pin 30.84 = 24×18/14`、卡宽 `313.16 = 320×18/14 − …`、空态卡高 `61.7`。

截图：`raw/e-note-18px.png`（9932 B）。

---

## 六、本拍排掉的坑（八条）

| # | 坑 | 处置 |
|---|---|---|
| 1 | **`splice109.py` 归零判据被自己的注释绊倒** —— 注释正文里逐字写了被删元素的名字 | 一切归零判据**先剥 HTML 注释**：`re.sub(r'<!--.*?-->', '', out, flags=re.S)` |
| 2 | **`.td-elnote-f` 被新类名 `.td-elnote-foot` 的「裸前缀」命中** | 改词边界 `\.td-elnote-f(?![-\w])` |
| 3 | **`.td-elnote-t` 被第 14 节选择器组里遗留的「死选择器」命中** | 顺手把那条死选择器**摘掉**（编辑 ④b）——死选择器不该留 |
| 4 | **「添加评论」是裸词**，JS 里本来就有三处无关的右键菜单项（「在此行添加评论」「已在该行添加评论」） | 只查**带上下文**的一整串（`'<div class="td-elnote-t">评论元素'`、`'添加评论</button>'`） |
| 5 | **跨代标记判据抄错** —— 原写 `/* r106-l1 */` / `/* r93-l1 */`（实际 r93 只在 `_mods.html` 的注释里），JS 侧写 `r108-l6 ①` | 按**实际清单**逐条查：CSS `r107-l1/l2 + r108-l1…l7 + r109-l1`；JS `r107-l2 / r108-l6 / r108-l7 / r108-l8` |
| 6 | **`verify-design.py` 门禁新增 1 条 `TOKEN-GAP`** —— 我在 CSS **注释**里逐字写了 `#9ca3af`，被打成「CSS 硬编码色值」 | 注释改成不含 hex 的措辞（「尾风那档 gray-400」）；改后与基线**只差「Token 缺口记录」那一行的路径**，**内容零差异** |
| 7 | **`patch109l1.py` 的 `IndexError`** —— `j_bare.split('浏览器模块')[1]`，而「浏览器模块」只在注释里（已被 `/\*.*?\*/` 剥掉）⇒ 分割锚点失效 | 改用代码里的 `var brw = pane.querySelector('.td-brw')` 起、`'var BRW_TEXT'` 止，并加「片段里必须有 `noteCommit`」的兜底判据 |
| 8 | **`pix109.py` 第一版两个错**：① `convert('RGB')` 后**透明像素变纯黑** ⇒ 按颜色筛把画布边缘的 `(0,0,0)` 全吃进来（「占位墨迹」假报成 `(0,-14,338,70)`）；② `Frame.find` 签名误用 `find(BORDER, 6, x0=…)` ⇒ `TypeError: 'function' object is not subscriptable` | ① 所有判据**先限定在卡片内区**（`Frame.region/P`）；② 全部改 `findp(pred, lx0, ly0, lx1, ly1)` |

> **本拍「裸词/裸前缀」连中三次（坑 2 / 3 / 4）** —— 与 PLAYBOOK 里那条「**判据不能写裸词**」是同族，
> 本拍把它的形态补全成三种：**①被无关文案命中 · ②被新类名的前缀命中 · ③被自己写的解释性注释命中**。
> 推而广之：**归零判据必须同时剥 HTML 注释、CSS 块注释与 JS 行注释**，并给 CSS 选择器加词边界。

> **另一处结构性教训（坑 6）**：**CSS 注释也是 CSS 文本** —— 门禁会把它一并扫。
> 解释「为什么不用某个色值」时**不要逐字写出那个 hex**，改写成人能读的指代（「尾风那档 gray-400」）。

---

## 七、幂等与门禁（产物定稿后复跑）

```bash
python mg-work/r109/ev/patch109l1.py        # 应用 0 项 / 跳过 6 项 · 全部存活 ✓ · md5 不变
python mg-work/r109/apply109.py             # base.html / conversation.html 均「已是目标态（无改动）」
python mg-work/check-syntax.py pages/*.html # 10/10 通过
python verify-design.py ./pages             # md5 3dbf6543…（与 r107 基线逐字节同）
python mg-work/r108/ev/scan-flatten.py mg-work/r109/part109/panel.css   # 2 条（= 基线）
git status --porcelain                      # 只有 ` M pages/conversation.html`
```

**真机探针链**（同一时刻只允许一个 UI 实测进程 ⇒ 每探针在**一次 bash 调用**内跑完）：

| 探针 | 覆盖 | 落点 |
|---|---|---|
| `p109z.js` | 确认右栏模块进入方式 = 点 `[data-td-open-mod="browser"]` | `z4.json` |
| `p109a.js` | ①②③ + ④稿1 空态 | `a1.json` · `a-note-empty.png` · `a-full-annotating.png` |
| `p109b.js` | ④稿2 输入态 | `b1.json` · `b-note-typing.png` |
| `p109c.js` | Ctrl 联动 | `c1.json` · `c-note-ctrl.png` |
| `p109d.js` | 提交 → 稿3 锚点 → 重开回填 | `d1.json` · `d-brw-anchored.png` · `d-note-reopen.png` |
| `p109e.js` | `--ui-fs=18` 档 + 200 压顶 + 内滚 + `docOverflowX` | `e1.json` · `e-note-18px.png` |

---

## 八、本拍改动清单

### 8.1 交付面（进 `git diff` 的只有一页 + 记忆）

| 文件 | 变化 |
|---|---|
| `pages/conversation.html` | 1024825 → **1036907** 字符（+12082）；8488 → **8733** 行（+245）；`git diff --numstat` = **`300 55`** |
| **其余 9 页** | **零改动**（`base.html` 逐字节不变、8 个外壳页一字未动） |
| `.workbuddy/memory/{HANDOFF,PAGES,PLAYBOOK,MEMORY}.md`（**仓库内 · 随 git 同步**） | 记忆同步（见第十节）；`2026-10-02.md` 为**新建** |
| ⚠ `pages/gaps.log` | 门禁写过 ⇒ 已 `git checkout --` 还原，**不进交付** |
| ⚠ `E:/GienCoder/.workbuddy/memory/{MEMORY.md,2026-10-02.md}`（工作区速记） | 同步更新（**不在 git 里**） |

### 8.2 `mg-work/r109/`（过程资产，不进 `git diff`）

| 生产链 | `_head.html`（+0，一字未动）/ `_mods.html`（+434）/ `panel.css`（+6658）/ `panel.js`（+4994）/ `browse.html`（+434，splice 产物） |
|---|---|
| 构建 | `apply109.py`（3647 行 / 190523 字符，由 `ev/make109.py` 生成）/ `ev/splice109.py` |
| 补丁 | `ev/patch109l1.py`（39802 B，6 条编辑 + 跨层自检 + `--check`） |
| 取证 | `ev/p109{a,b,c,d,e,z}.js` + `probe109{a,b,e,z}.sh` + `a1/b1/c1/d1/e1/z4.json` + `ev/pix109.py`（+ `pix109.log`） |
| 素材 | `raw/` 15 张（设计稿 PNG/SVG/JSON + 真机截图） |
| 门禁基线 | `ev/vd-l1base.txt`（336 行）/ `ev/vd-l1.txt`（340 行）/ `ev/tmp/vd0/`（改前基线目录）；改前备份 `ev/bak-l1/{panel.css.before 99265 B, panel.js.before 86588 B, _mods.html.before 76299 B}` |

---

## 九、交接（r109 · 第一拍）

**已完成**：邵先生四条 + 五条澄清**全部落地并取证**：

| 需求 | 结论 |
|---|---|
| ① 删 `td-page-blank` | DOM + CSS **双清零**；真机 `pageBlankCount: 0` |
| ② `td-annot-bar` 贴顶 | DOM 挪首 + CSS `top: 0`；真机 `barIsFirstChild:true` / `position:sticky` / `top:"0px"` / `dTop:0` |
| ③ 红色系「退出批注」 | `标注 → 退出批注`；`#FFECE8`（red-1）底 + `#F53F3F`（red-6）字，全 token |
| ④ `td-elnote` 三稿 | 结构性地标**逐像素差 0**（卡框、两枚按钮）；Ctrl / 锚点 / 重开回填 / 200 压顶 / 字号杠杆全部取证 |

**遗留（有意保留、未动，等邵先生发话）**：两处同型入口硬切 —— 右键菜单 `ctxShow()` 与 `.zd-menu` 的 `placeZdMenu()`
入场无 0.2s spring；**关**的那一侧仍是「摘 `POP_OPEN` + 置 `[hidden]`」（无退场动画）。
（与 r108 十九拍同一笔账，本拍按「不得改动不必涉及的模块」未动。）

**待邵先生定夺的两处**：
1. 稿1 的「添加」右内距 **10px** vs 稿2 的 **12px** —— 本层统一取 12，要不要给空态单开一条 −2px 补偿？
2. 已批注锚点的落点取「**右上角**」（稿子未给）—— 若想换左/右下，一句话即可改 `noteDrop()` 的两个 `−12`。

**体位**：本代未 commit（等邵先生显式说「commit」）；未交付期返工**就地改 `ev/patch109l1*.py`**，
已交付才新建 `r110`。跨代沿用宿主标记**不换名**（`r106-nav-js`）。

---

## 十、记忆同步（`ev/doc109l1.py`，实测读数）

**脚本**：`mg-work/r109/ev/doc109l1.py`（六步 / 35 条步骤；`mark = new` 幂等 + 「mark 歧义」硬断言 + `--check`）。

| 文件 | 字符变化 |
|---|---|
| `.workbuddy/memory/HANDOFF.md` | 163066 → **172617**（首行 + 顶部 r109 块 + 降级链 + §一 状态段 + conversation/mg-work 表行 + 二·h 改「已封板」+ **新增 §二·i r109** + §六 两条待拍板 + §七 三处口径 + §八 回滚） |
| `.workbuddy/memory/PAGES.md` | 110538 → **112804**（P3.11i 标题「共二十拍」+ 固定事实表 r109 四行 + 必看清单 23~26） |
| `.workbuddy/memory/PLAYBOOK.md` | 213034 → **216931**（**新增 P3.56** 八条 + 附录标题 92 → **98 条** + 附录追加 93~98） |
| `.workbuddy/memory/MEMORY.md`（仓库） | 40663 → **43060**（r108 段末标「已封板」+ 追加 **r109 第一拍段**） |
| `.workbuddy/memory/2026-10-02.md`（仓库） | **新建** → 1165 |
| `E:/GienCoder/.workbuddy/memory/MEMORY.md`（工作区，**3000 限额**） | 2984 → **2994**（余量 6）—— 压缩了 r107/r108 两行才腾出空间 |
| `E:/GienCoder/.workbuddy/memory/2026-10-02.md`（工作区） | **新建** → 1165 |

**幂等**：连跑三遍 ⇒ 第一遍「1 应用 / 28 跳过」（那 1 项是纯追加）、第二遍「**0 应用 / 35 跳过**」、第三遍同。`--check` 只报「两份当日日志尚不存在」（预期）。

> ⚠ **限额硬断言**：脚本在写完工作区 `MEMORY.md` 后立刻量字符数，>3000 直接 `sys.exit` ——
> 第一次跑就**真的撞了**（3035 > 3000）⇒ 把 r107/r108 两行压成一行、并精简 r109 那行（省 41 字符）后复跑通过。
> ★ 教训：**「最近拍」是限额里最贵的一块** —— 加新拍之前先想好从哪儿腾位置。

**收尾定格**：`git status --porcelain` =
` M .workbuddy/memory/{HANDOFF,MEMORY,PAGES,PLAYBOOK}.md` + ` M pages/conversation.html` + `?? .workbuddy/memory/2026-10-02.md` + `?? mg-work/r109/`
（**`pages/gaps.log` 已还原、不在列表里**）。

---
---

# 第二拍（r109-l2）· 邵先生新五条 + 一条真机实测出来的配套

> 需求（邵先生 2026-10-02 09:xx，逐字）：
> ① 「当右栏展开时，`zd-host` 容器会自动折叠为迷你按钮状态」；
> ② 「`td-term` 容器内的字号都调整为 13px」；
> ③ 「`r93-ib r93-bt` 这个重新生产的图标异常，请修复」；
> ④ 「添加已添加的批注的锚点 `td-anchor` 会以编辑态的形式显示批注详情」；
> ⑤ 「批注的锚点 `td-anchor` 需要支持任意拖动位置」。
>
> ★ 本拍唯一的追问（`AskUserQuestion` 一答）：② 的范围 —— `.td-term-tabs` / `.td-term-tab` /
>   `.td-term-tabadd` 在 DOM 上是 `.td-term` 的**兄弟**、严格讲不在「容器内」。邵先生答：
>   **「整个终端模块都改 13px（推荐）」**。

---

## 十一、第二拍总览

### 11.1 落地面

| 层 | 文件 | 变化 | 说明 |
|---|---|---|---|
| 静态 | `part109/panel.css` | `83427 → 84764`（+1337） | ② 四条字号 + ⑤ 锚点可拖动声明 + 注释 |
| 静态 | `part109/panel.js` | `77185 → 84643`（+7458） | ④ 反查/定位 + ④⑤ 锚点重写 + ⑤ 拖拽 + ① 折叠联动 + ⑤配套 夹取 |
| 拼装 | `part109/browse.html` | `106685 → 106685`（**0**） | `ev/splice109.py` 产物，四个分片长度同值（前缀 247 + 头部 4792 + Files 正文 30130 + 新模块 71501） |
| 生成器 | `ev/make109.py` | `5139 → 7629` | ③ 的**真正落点**（`EDITS` 表新增 E8） |
| 应用器 | `apply109.py` | `190523 → 191131`（3658 行，8 处替换） | `ev/make109.py` 重生成 |
| **交付面** | `pages/conversation.html` | **`1036907 → 1045713`（+8806）**，行 `8733 → 8918`，md5 **`dc240794ab4ed6d262b02b739f68753f`** | 只有这一页变 |
| 补丁 | `ev/patch109l2.py` | **新建** 34092 字符 / 795 行 | `--check` / `--bak` / `do_css` `do_js` `do_l1` `do_make` / `verify()` |
| 判据同步 | `ev/patch109l1.py` | `31751 → 31851` | l1 的 `noteEdit` 分割锚点由 `'function noteEdit(el) {'` 放宽为 `'function noteEdit(el'` |

**改序（下→上，一律重跑自愈）**：
```
ev/patch109l2.py        →  part109/panel.css + panel.js（+ patch109l1.py 判据 + make109.py EDITS）
ev/splice109.py         →  part109/browse.html
ev/make109.py           →  apply109.py
apply109.py             →  pages/conversation.html
```

### 11.2 ★ 本拍最贵的一条认知：③ 的落点不在 `apply109.py`

`apply109.py` **不是**手改对象 —— 它是 `ev/make109.py` 从 `mg-work/r108/apply108.py` 逐字生成的
（`make109.py` 的 `EDITS` 表 = 若干条精确替换；表以外**一字不差**）。所以「改一个内联图标」
的正确落点是 **`make109.py` 的 `EDITS` 表**，不是应用器本身。
本拍新增 **E8**（`ICON_INLINE['regen']` 的整段重画），`make109.py` 重跑即自愈。

> ★ 推论：**凡「图标 / 常量表 / 生成期替换」类改动，先问「谁生成的 apply」**。
>   直接改 `apply109.py` 会在下一次 `make109.py` 重跑时**被静默冲掉**。

---

## 十二、① 右栏展开 ⇒ `zd-host` 自动折叠为胶囊

### 12.1 信号源的选择（三种做法，只取一种）

| 候选 | 为什么不要 |
|---|---|
| hook 页头那枚开关（`.r93-baract[data-r93-browse]`）的 `click` | 收起右栏有**三条**路径：开关按钮 / 宿主 Esc / 面板自带 `[data-td-browse-close]`；且 `panel.js` 的 `ensureOpen()` 还会**合成** `b.click()` ⇒ hook click 必漏 |
| 盯「右栏标签切换」 | 切标签时右栏**本来就是展开的** —— 需求是「展开**时**折叠」，盯标签会在用户手动摊回卡片后、一换标签又给折回去 |
| **盯 `.av-browse-on`** ✔ | 它是宿主 `ctrl-conv.js` 的 `setOpen()` **唯一**写入的状态类、打在**外壳 flex 行**（`div:has(> main)` = `#av-browse-slot.parentElement`）上；宿主自己就拿它当判据（`browseOpen()`）⇒ 它就是「右栏展开」的**唯一真身**，不是又造一个 |

### 12.2 实现（`panel.js`，zd IIFE 内 `toMini()` 之后）

```js
var browseSlot = document.getElementById('av-browse-slot');
var zdRowEl = null, zdRowOn = null, zdRowMo = null;
function zdRowCheck() {
  if (!zdRowEl) return;
  var on = zdRowEl.classList.contains('av-browse-on');
  if (on === zdRowOn) return;
  zdRowOn = on;
  if (on) toMini();                       /* 只在「开」这一侧动手 —— 反向不摊回 */
}
function zdRowSync() {
  var row = browseSlot ? browseSlot.parentElement : null;
  if (!row) return;
  if (row !== zdRowEl) {                  /* 首次挂上 / React 重挂 ⇒ 换观察对象 */
    if (zdRowMo) zdRowMo.disconnect();
    zdRowEl = row;
    zdRowOn = row.classList.contains('av-browse-on');
    zdRowMo = new MutationObserver(zdRowCheck);
    zdRowMo.observe(row, { attributes: true, attributeFilter: ['class'] });
    if (zdRowOn) toMini();
    return;
  }
  zdRowCheck();
}
if (browseSlot) {
  zdRowSync();
  var zdRowMo0 = new MutationObserver(zdRowSync);
  zdRowMo0.observe(document.body, { childList: true, subtree: true });
}
```

**两条设计取舍**：
- **反向不摊回**：邵先生只说了「展开**时**折叠」。收起右栏不该替用户改变他手动选定的形态（他可能就是要一直看胶囊）。
- **`childList` 观察器兜「异步」**：`#av-browse-slot` 由宿主 `place()` **异步**插到 `main` 之后（React 首帧晚于本脚本）⇒ 首挂可能拿不到 `parentElement`，且 React 重挂会换行元素。

### 12.3 ★ 真机矩阵（`p109k.js` / `k1.json`，1440×900）

| # | 动作 | `av-browse-on` | `[data-zd-card]` | `[data-zd-mini]` | 卡片盒 | 结论 |
|---|---|---|---|---|---|---|
| a0 | **页面初态** | false | **visible** | hidden | `1095,105 320×484` | 右栏默认关闭 + 卡片态 |
| a1 | 手动摊成卡片 | false | visible | hidden | `1095,105 320×484` | （本来就是卡片，无需点） |
| a2 | **点开关展开右栏** | **true** | **hidden** | **visible** | 胶囊 `671.91,105 103.09×32` | ✔ **自动折叠** |
| a3 | 用户点胶囊手动摊回 | true | **visible** | hidden | `455,105 320×484` | ✔ 手动可逆 |
| a4 | **再收起右栏** | false | **visible** | hidden | `1095,105 320×484` | ✔ **反向不自动折回** |

### 12.4 ★ 取证踩的坑：「初态」必须独立一趟取

第一版探针把 ① 排在 ②（点浏览器模块）**之后** ⇒ `ensureOpen()` 已经把右栏打开过、
`toMini()` 早就跑完了 ⇒ a0 读到的 `cardHidden` 是 **true**，**① 的判据被前一步污染、完全失去鉴别力**。
修法：① 单列一趟、在**未碰任何开关**的初态下测（`p109k.js` 一进来就先拍 `a0_fresh`）。

---

## 十三、② 终端模块字号统一 13px

### 13.1 范围（追问的由来）

DOM 上是这样的：`<section.td-mod#av-browse-pane-terminal>` 下先 `<div.td-term-tabs>`
（两枚 `.td-term-tab` + 一枚 `.td-term-tabadd`），**再**是两个**兄弟** `<div.td-term>`。
⇒ 「`.td-term` 容器内」严格讲只覆盖正文块。追问后邵先生定 **整个终端模块都改**（否则会出现
「正文 13 / 标签 12」的参差）。

### 13.2 四条规则 · 只换 token、盒模型一行未动

| 选择器 | 改前 | 改后 |
|---|---|---|
| `.td-term` | `var(--font-size-body-1)` | `var(--font-size-body-2)` |
| `.td-term-tabs` | 同上 | 同上 |
| `.td-term-tab` | 同上 | 同上 |
| `.td-term-tabadd` | 同上 | 同上 |

token 口径（页面内联 DS）：`--ui-fs:14` → `--ui-fs-ratio: calc(var(--ui-fs) / 14)`，
`--font-size-body-2: calc(13px * var(--ui-fs-ratio))` ⇒ **默认档 ratio = 1 ⇒ 恰好 13px**；
`--ui-fs` 一抬，全站等比放大（这才是字号杠杆的正确行为）。

### 13.3 ★ 真机读数（`p109k.js` / `k1.json`，终端模块已激活）

| 项 | 读数 | 判据 |
|---|---|---|
| `.td-term` ×2 的 `font-size` | **`13px` / `13px`** | ✔ |
| `.td-term-tabs` | **`13px`** | ✔ |
| `.td-term-tab` ×2 | **`13px` / `13px`** | ✔ |
| `.td-term-tabadd` | **`13px`** | ✔ |
| `.td-term` `line-height` | `20px` | **未动**（盒模型零改动） |
| `.td-term` 盒 | `639×764`，`scrollH 764 == clientH 764`、`scrollW 639 == clientW 639` | **无内滚、无横溢** |
| `.td-term-tabs` `min-height` / 盒高 | `34px` / `34` | **未动** |
| `.td-term-tab` `height` | `22px` | **未动** |
| `.td-term-tab-nm`（`zsh`） | `scrollW 19 == clientW 19`，`clipped: false` | **文字未被截断** |
| `.td-term-tabadd` | `22×22` | **未动** |
| `.td-term-caret` | `7×13` | **未动**（这是 `height` 不是字号；13px 恰好等于新字号的 1em，故刻意不动） |

---

## 十四、③ `r93-ib r93-bt`（重新生成）图标重画

### 14.1 真值来源与判据口径

设计真值 = `mg-work/r93/raw/design-rgb.png` 的 14px 盒（`x956..969 / y225..231`，相对 y = PNG y − 225）。
墨迹只有 **14×7 = 36 px**、四级灰（134/149/164/194，白 255）。图解 = **上半圆弧**（apex 在 x7、右端收圆头）
+ 左下**实心箭头**（尖端指左下、开口朝上、两翼之间 x4 列有分叉），弧左端与箭头之间**故意缺一口**。

### 14.2 ★★ 拟合判据：**看「坏格数」，不看总 err**

- `ev/tools/evalpath.py`（本拍新建）：解析**真实 SVG path 串** → 按 SVG F.6.5 推弧心 → SS=8 覆盖率光栅化 → 与设计位图比。
- `ev/tools/refiteregen.py`（本拍新建）：起止角自由 + **墨迹盒硬约束** `BOX=(0.10,4.20,13.90,11.00)` 的坐标下降 + 多起点（4 手写 + 26 随机，`seed=109`）。
- 实测：**旧串** `M13.9 9.4A5 5 0 0 0 4.1 8.9` + `M1.05 7.85 4.4 7.95 2.95 10.6Z` ⇒ **err 15.046**；**新串** ⇒ **err 2.298**（**6.5×**）。
- ★ **两个反例（都真踩了）**：
  1. **「越界罚项」是错的**：给 `err()` 加「越界包络罚项」想防过拟合 ⇒ 把**正确的弧顶**也罚了（设计真值在弧顶下方本来就有洞），err 从 2.3 抬到 10.7、解被推到「弧更扁」的另一侧。**正解 = 收紧参数的物理边界，不是加罚项。**
  2. **别只看总 err**：多起点能拿到 err **2.192 < 2.298** 的「c 解」，但它有 **7 个格**与设计差 ≥0.33（箭头在 y10 整行弱 0.4~0.5）。按「坏格数」判：**a = 1 个**（`(x2,y8)` 0→0.84）、b = 5、c = 7 ⇒ **a 才是最贴设计的解**，总 err 更小的 c 是过拟合。

### 14.3 新路径（唯一残差 = 「圆弧 + 凸三角」两种图元表达不了设计里那个凹口）

```
'regen': '<svg viewBox="0 0 14 14" fill="none" aria-hidden="true">'
         '<path d="M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5" stroke="currentColor" '
         'stroke-width="1.3" stroke-linecap="round"/>'
         '<path d="M2.07 11.4 5.61 9.61 1.05 7.56Z" fill="currentColor"/></svg>',
```
宿主用点：`.r93-umeta` 行内 `'<button class="r93-ib r93-bt" type="button" title="重新生成"><span class="r93-iblk r93-i14">' + IC('regen') + '</span></button>'`；host 盒 `.r93-iblk.r93-i14 { width:14px; height:14px }`。

### 14.4 ★ 真机读数（`p109k.js` / `k1.json`）

| 项 | 读数 |
|---|---|
| 按钮盒 / `iblk` / `svg` | `24×24` / `14×14` / `14×14`（`viewBox="0 0 14 14"`） |
| `path[0].d` / `path[1].d` | `M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5` / `M2.07 11.4 5.61 9.61 1.05 7.56Z` ✔ 新串 |
| `stroke-width` / `linecap` / `fill` | `1.3` / `round` / 弧 `stroke=currentColor`、三角 `fill=currentColor` |
| 旧串归零 | `document.documentElement.outerHTML.indexOf('M13.9 9.4') < 0` ⇒ **true**（全页 0 次） |
| `transitionDuration` | `0s`（图标无过渡） |

### 14.5 ★★ 真机 1× 渲染 vs 设计位图的对照口径（`ev/tools/cmpregen2.py` → `raw/cmp-regen-l2.png`）

- **墨迹盒完全一致**：设计 `(1,5,12,10)` == 真机 `(1,5,12,10)` ✔
- **归一化必须按「各自最深像素」**：设计最深 **134**、真机最深 **78**（图标色 `#4E4E4E` —— 比设计的
  最深灰更深）⇒ 若两边都除以 `121`（设计口径），真机每一格都会被系统性放大 ~46%，
  第一版就这么报出「err 3.043 / 25 个坏格」的**假失败**。按各自最深归一后 = **err 1.620 / 5 个坏格**，
  且这 5 格全是浏览器 1× 光栅化 1.3px 描边的**亚像素抗锯齿**（含已知残差 `(2,8) +0.82`）。
- ★ 口径结论：**真机 1× 截图与 SS=8 数学模型不可逐格比**；1× 真机只做两件事 ——
  **① 墨迹盒一致；② 观感一致**（见 `cmp-regen-l2.png`：左设计 / 右真机，弧顶、右端收圆、
  左下箭头簇与「弧—箭头之间那道口」都对得上）。逐格精度用 `evalpath.py` 在设计位图上判。

---

## 十五、④ 已批注锚点 → 以**编辑态**显示批注详情

### 15.1 三处改动

1. **反查**（`noteList` 里 `rec.el` 是单向的：被标注元素 → 批注；点锚点这一头要反着走）：
```js
function noteOfAnchor(a) {
  for (var i = 0; i < noteList.length; i++) if (noteList[i].anchor === a) return noteList[i];
  return null;
}
```
2. **`noteEdit(el, at)` 加「定位参照物」**：点锚点看详情时传的是**锚点** ⇒ 气泡落在锚点下方。
   锚点可以拖到任意位置（⑤），若还按「被标注元素」定位，拖远之后气泡会跟锚点脱开。
```js
function noteEdit(el, at) {
  var prev = noteFind(el);
  var ref = at || el;                     /* ★ 默认 = 被标注元素自己 */
  ...
  var er = ref.getBoundingClientRect(), vr = view.getBoundingClientRect();
```
3. **`noteDrop` 换按钮语义**：摘掉 r109-l1 挂的 `aria-hidden="true"`（那时它确实只是标记），
   换成 `role="button"` + `tabindex="0"` + `aria-label="查看第 N 条批注"` + `title="点击查看批注 · 拖动可挪位置"`；
   `bindAnchor(a)` 里配 `click` / `keydown`（Enter / Space）⇒ `anchorOpen(a)`。

### 15.2 ★ 真机读数（`p109i.js` / `i1.json`，真鼠标单击锚点）

| 项 | 读数 | 判据 |
|---|---|---|
| `.td-elnote` `hidden` | **false** | ✔ 气泡重开 |
| `.td-elnote-input.value` | = 提交时那段原文（逐字相同） | ✔ 编辑态回填 |
| `.td-elnote-pin.textContent` / `is-done` | **`1`** / **true** | ✔ 锚点编号 |
| `.td-elnote-ok` | `disabled: false`、文案仍「添加」 | ✔ 可用 |
| 气泡顶缘 − 锚点底缘 | **`8`**（px） | ✔ **证明是按锚点定位** |
| `.td-anchor` | `role=button` `tabindex=0` `aria-label=查看第 1 条批注` `cursor: grab` `touch-action: none` `user-select: none` `border-radius: 12px 12px 12px 0` `bg: rgb(55,112,247)` `z-index: 2` | ✔ |

### 15.3 ★ update 语义（`p109j.js` / `j1.json`）

点开 → 改文案 → 再提交：`anchorCount` **1 → 1**、锚点 `left/top` **`605px/734px` 原地不动**、
气泡重新收起；再点开 ⇒ `taValue` = **已编辑**那版、`pin` 仍 `1`。
⇒ **编辑已存在的批注 = 就地更新，不会新增锚点、不会挪位置。**

---

## 十六、⑤ 锚点任意拖动 + ★★ 一条真机实测出来的**配套修复**

### 16.1 手势与夹取

- `pointerdown`（左键）→ `window` 上挂 `pointermove` / `pointerup` / `pointercancel` / `blur`（**捕获段**，站内其它拖拽同口径）。
- **4px 阈值分流「拖 vs 点」**（`ANCHOR_MIN = 4`）：越过阈值才 `_tdMoved = true` + 挂 `.is-dragging`；
  松手后那一下 `click` 被 `_tdMoved` 吃掉（否则每拖一次都顺手弹一次气泡）。
- **`_tdMoved` 在 `pointerdown` 处复位**（不是只在 `click` 里复位）⇒ 「拖完松手落在锚点之外、没有
  click」这一支也自愈：下一次 `pointerdown` 即复位，不会「以后点一下没反应」。
- `anchorPlace(a, left, top)` 把位置夹进 `.td-view` 的**可视区**（`scrollLeft + clientWidth - offsetWidth`）——
  绝对定位子件跟着内容滚，不夹就能把锚点拖出视野、再也点不到。
- CSS：`cursor: grab` / `.is-dragging{cursor: grabbing}` / `touch-action: none` / `user-select: none`；
  **刻意不加 `transition`**（拖动要跟手，过渡 = 拖影）；**刻意不抬 `z-index`**（锚点 z=2，上面压着气泡 z=3）。

### 16.2 ★ 真机读数（真鼠标 `mouse move/down/up`）

| 项 | 读数 |
|---|---|
| ⑤-a 拖 `+40/+30` | 内联 `left 202px → 242px`、`top 182px → 212px`（**精确**）；`is-dragging` 松手后清除；`elnoteHidden` = **true**（**没弹气泡**） |
| ⑤-b 拖到视口 `1439,899`（超出 `.td-view`） | 内联 `left/top = 605px/734px` == `expectMax.L/.T = 605/734`（**精确夹到可视区边界**）；`inView: true` |
| 页面横向溢出 | `documentElement.scrollWidth − innerWidth = 0` |

### 16.3 ★★ 实测出来的缺陷：锚点拖到底角 ⇒ 气泡被 `.td-view` 裁掉

`.td-elnote` 是 `.td-view`（`overflow: auto`）的**子件** ⇒ `noteEdit` 里那条
`top = 锚点底缘 + 8` 在锚点贴底时会把气泡**整块推出生效区**。

**修复前实测（`p109i.js` / `i2.json`）**：

```
锚点内联 605px/734px（屏幕 1397,867）→ 气泡盒 {l:804, t:899, w:356, h:108}
.td-view 盒 {t:133, h:758}（可视底 = 891）
⇒ clip.bubbleBottomBelowView = 116   clip.visibleH = -8   clip.fullyHidden = true   ← 一点都看不见
```

**修法（`noteEdit` 内）** —— 把「写 `top`」挪到「摘 `[hidden]` + `noteGrow()`」之后，并加可视带夹取：

```js
elnote.removeAttribute('hidden');
noteGrow();
var er = ref.getBoundingClientRect(), vr = view.getBoundingClientRect();
var top = er.bottom - vr.top + view.scrollTop + 8;
var vTop = view.scrollTop, vBot = view.scrollTop + view.clientHeight;
var h = elnote.offsetHeight;
if (h && view.clientHeight && top + h > vBot) top = vBot - h;
if (top < vTop) top = vTop;
elnote.style.top = Math.round(top) + 'px';
```

**为什么算「⑤ 的配套」而不是「另开一摊」**：需求 ⑤「锚点可任意拖动」是**因**、气泡被裁是**果** ——
⑤ 不落地这个缺陷根本不存在。且改动**只碰 ④ 已经改过的那几行定位代码**，
`.td-elnote` 的 CSS（`left: 12px` / 宽 356 / 三稿几何）一行未动。

**修复后实测**：`bubbleBottomBelowView 116 → 0`、`visibleH −8 → 108`、`fullyHidden true → false`
（气泡底缘正好贴住 `.td-view` 可视底）；而**常规位置仍是 `气泡顶 = 锚点底 + 8`**（`bubbleDTop = 8`）、
`visibleH = 108` ⇒ **只在这一支生效，r109-l1 已验收的常态观感一字未变**。

> 三条安全前提（都实测过）：
> · **先摘 `[hidden]` 再量高** —— 隐藏态 `offsetHeight` 恒为 0，量不出真实高、夹取会失效。
>   l1 的判据本来就是「先摘 `[hidden]` 再 `noteGrow()`」，顺序不动，只是把定位挪到其后。
> · **不引入位移动画** —— `.td-elnote` 自身 `transitionDuration` 实测 **`0s`**（只有 pin 的
>   `background-color` 与两枚按钮各自有过渡）。
> · **`pages/conversation.html` +1042 字符**（1044671 → 1045713）就是这条。

### 16.4 ★ 一处「看着像 bug、其实是探针 bug」

`p109j.js` 原来用**合成** `a.click()` 重开气泡，读出来 `elnoteHidden = true`（像失败）。
真因：⑤-b 的拖动**松手落在锚点之外 ⇒ 浏览器不发 `click`** ⇒ `_tdMoved` 留在 `true`；
合成 `click()` **不经过 `pointerdown`** ⇒ 标记没被复位 ⇒ 这一下被当成「拖动的尾巴」吃掉。
**真机路径本来是对的**（下次 `pointerdown` 就复位）。修法：探针改成**真鼠标**在锚点中心
`move/down/up`（顺带把 ④ 也用真鼠标复核了一遍），另留 `p109r.js` 做标记复位的辅助对照。

---

## 十七、幂等与门禁（第二拍定稿后复跑）

| 项 | 命令 | 读数 |
|---|---|---|
| 补丁幂等 | `python ev/patch109l2.py`（第二次） | **应用 0 项 / 跳过 12 项**，`verify()` 全绿 |
| ★★ **自愈** | 从 `ev/bak-l2/{panel.js,panel.css}.before` **干净基线全量重放** | 应用 10 项 / 跳过 2 项 / **全部存活 ✓**；产物与「就地修改后」的产物 **`diff` 0 差异**（panel.js 84643 / panel.css 84764） |
| 生成器自检 | `python ev/make109.py` | `apply109.py` 3658 行 / 191131 字符 / **8 处替换** |
| 应用器幂等 | `python apply109.py`（第二次） | `base.html` / `conversation.html` **均已是目标态（无改动）** |
| 语法门禁 | `python mg-work/check-syntax.py pages/*.html` | **10/10 通过**（`conversation.html script=9 style=16`，与 r108 一致） |
| 字号压平门禁 | `python mg-work/r108/ev/scan-flatten.py mg-work/r109/part109/panel.css` | **仍 2 条**（= 基线 `.td-mod-bar` / `.td-url`）⇒ 本拍**没引新的可压平规则** |
| 设计回归门禁 | `python verify-design.py ./pages > ev/vd-l2b.txt` | 与 `vd-l1now.txt`（上一拍）**0 diff**、与 `vd-l2.txt`（本拍夹取前）**0 diff** ⇒ **零新增差异、一处渐变都没引**（工具自身 exit=1 是常态） |
| 跨代标记 | `panel.css` / `panel.js` | `r107-l1` 2/0 · `r108-l*` 13/12 · `r109-l1` 10/6 · **`r109-l2` 6/6** 全在 |

> ⚠ `patch109l1.py` 的 `noteEdit` 判据被本层**放宽**：`split('function noteEdit(el) {')`
> → `split('function noteEdit(el')`。原因：本拍把签名改成 `(el, at)`，l1 的**精确**分割锚点会失效。
> **后一层必须替前一层保住判据** —— l1 那条 `i_unhide < i_grow` 的语义（先摘 `[hidden]` 再 `noteGrow()`）
> 在放宽后**仍然成立且仍被检查**（本拍 ⑤配套 的改动也守住了它）。
> 另外 `patch109l2.py` 里 `noteOfAnchor` 那条是**追加式**编辑（`noteFind` 原文一字不动），
> `old` 永远是 `new` 的子串 ⇒ 那条显式 `strict=False`（幂等性仍由 mark 保证）。

---

## 十八、第二拍改动清单 · 交接 · 记忆同步

### 18.1 交付面（进 `git diff` 的只有一页 + 记忆）

| 文件 | 变化 |
|---|---|
| `pages/conversation.html` | `1036907 → 1045713`（+8806），md5 `dc240794ab4ed6d262b02b739f68753f` |
| 其余 9 页 | **一页未动**（`base.html` md5 `044ca6c6d134534f9383685f597aede4` 不变） |
| `pages/gaps.log` | 被 `verify-design.py` 写过 ⇒ **收尾 `git checkout --` 还原** |
| `.workbuddy/memory/*` | 见 18.3 |

### 18.2 `mg-work/r109/`（过程资产，不进 `git diff`）

- **新建**：`ev/patch109l2.py`（34092）· `ev/p109k.js` `p109g.js` `p109h.js` `p109i.js` `p109j.js` `p109r.js`
  · `ev/probe109l2.sh` · `ev/tools/{evalpath,refiteregen,cmpregen2,l2shots,stats}.py` · `ev/bak-l2/`
  · `raw/{f-zd-mini, g-regen-btn, d2-anchor-committed, d2-anchor-reopen, e2-anchor-clamped,
  e2-anchor-corner-note, cmp-regen-l2, l2-evidence}.png`
  · `ev/raw/design-regen-{224-grid,224,arrow-36x,30x,30x-smooth,cluster-60x}.png`（上一步的图解资产）
- **改动**：`ev/patch109l1.py`（+100）· `ev/make109.py` · `ev/splice109.py` 重跑
- **读数留档**：`ev/{f1,g1,h1,h2,i1,i2,j1,k1}.json` · `ev/l2probe.txt` · `ev/vd-l2.txt` / `vd-l2b.txt` · `ev/l2-*.log`

### 18.3 记忆同步（`ev/doc109l2.py`）

见下一节实测读数。

### 18.4 交接给邵先生

**这五条都按逐字需求落地、真机取证完毕，且顺手修掉一条由 ⑤ 引出的必现缺陷（气泡被裁）。**
仍**未 commit**（等显式指示）。下一拍若要动右栏，按硬规则：**本代未交付 ⇒ 就地改 `ev/patch109l*.py`**。

---

# 第三拍（r109-l3）· 邵先生三条：批注原点 / 卡片对齐 / 全站暗色

## 十九、第三拍总览

### 19.1 需求逐字（2026-10-02 10:2x）

> **1**、添加批注的点击触发点与输入批注的容器 `td-elnote` 没有在一个原点，位置漂移太远，需要做到**在哪里点击就在哪里添加**，
> 包括**预览批注**的也是一样，另外**编辑态**时原来的「添加」文案需变为「**保存**」；
> **2**、对话内容中的类似 `r93-card r93-card--edge` 这样的容器前面的**缩进都取消**，两端都对齐吧；
> **3**、我需要支持**全局 UI 界面（基础工作台和研发工作台）的暗色模式**，用户可以在**设置页面的「外观」里**去选择。
> 请你帮我调研一下当前的浅色模式和暗色模式的适配情况，**所有的色值全部要来自 giencoder 设计系统的色彩系统**。你先思考一下解决方案，有疑惑或不确定的可以询问我。

### 19.2 本拍唯一一次追问（三条决策，邵先生已答）

| 问题 | 邵先生的选择 |
|---|---|
| ③ 的落地范围 | **「机制层 + 基础工作台 5 页」**（先落开关机制 + 设置页接线 + base / avatar / automation / skills / settings 适配到位；研发工作台 5 页下一轮） |
| 首次进入的默认档 | **「跟随系统」**（`auto`） |
| 色值收敛尺度 | **「按需收敛（推荐）」** |

### 19.3 落地面（全部在本代 `mg-work/r109/` 内，不进 `git diff`）

| 件 | 前 | 后 | 说明 |
|---|---|---|---|
| `part109/panel.js` | 84643 | **88077** | ① 的 JS 侧（`noteAt` 单一原点 + 编辑态文案收口） |
| `part109/panel.css` | 84764 | **84764（未动）** | ① 全是 JS 行为，CSS 一行未改 |
| `part109/browse.html` | 106685 | **106685（0）** | `splice109.py` 的产物，四片同长、逐字稳定 |
| `ev/patch109l3.py` | 25098 | **29068** | 本层补丁（10 条编辑 + 上一层的判据放宽） |
| `ev/make109.py` | 7629 | **10681** | 新增 **E9**（② 卡片）+ **E10**（③-d 净底锚点） |
| `apply109.py`（生成物） | 191131 | **192105**（3676 行） | **10 处替换** |
| `ev/theme/apply-theme.py` | — | **9549**（新建） | ③-a **机制层**（全站 10 页） |
| `ev/theme/apply-dark.py` | — | **25406**（新建） | ③-c **适配层**（基础工作台 5 页 + 越界清扫） |

### 19.4 改序（★ ⑦ 条，后两条**必须最后跑**）

```
1. part109/panel.js                  ← ①
2. ev/make109.py                     ← ②（E9）+ ③-d（E10）
3. ev/splice109.py                   → 重建 part109/browse.html
4. ev/make109.py                     → 重生成 apply109.py
5. apply109.py                       → 落 pages/base.html + pages/conversation.html
6. ev/theme/apply-theme.py           → 全站 10 页注入主题块
7. ev/theme/apply-dark.py            → 基础工作台 5 页注入适配层（+ 越界清扫）
```

> ★ ⑥⑦ 必须最后跑：`apply109.py` 会从 `base.html` 的**净底重建** `conversation.html`，
> 主题块落在 `base.html` 上就会跟着过去；适配块也会跟着过去（见 §二十九·2 那条真缺陷）。

### 19.5 ★★ 交付面增量（**三方独立印证**，口径已统一）

**口径**：工程「字符」= `decode('utf-8')` 后 `\r\n → \n` 的 `len()`（`wc -c` / `git diff --numstat` 是**字节**，两套口径**禁混用**）。

| 文件 | HEAD（r108 封板 `172e580`） | 现在 | 增量 |
|---|---|---|---|
| `base.html` | 472150 | **487942** | **+15792** |
| `avatar.html` | 568090 | **583882** | +15792 |
| `automation.html` | 361696 | **377488** | +15792 |
| `skills.html` | 361583 | **377375** | +15792 |
| `settings.html` | 459222 | **475014** | +15792 |
| `conversation.html` | 1024825 | **1054348** | +29523 |
| `dev.html` | 450205 | **455029** | +4824 |
| `kanban.html` | 568052 | **572876** | +4824 |
| `req-kanban.html` | 513791 | **518615** | +4824 |
| `task-detail.html` | 767836 | **772660** | +4824 |

**增量能被三块注入物逐字解释（零剩余）**：

| 注入块 | 长度 | 落在哪几页 |
|---|---|---|
| `<style id="r109-theme-css">` | 752 | **全部 10 页** |
| `<script id="r109-theme-js">` | 4072 | **全部 10 页** |
| `<style id="r109-dark-css">` | 10951 | **基础工作台 5 页** |
| `<html … data-gi-dark="1">`（护栏属性） | 17 | **基础工作台 5 页** |

- 基础工作台 5 页：`752 + 4072 + 10951 + 17 = **15792**` ✓ 与实测**逐字符相等**
- 研发工作台 4 页（dev / kanban / req-kanban / task-detail）：`752 + 4072 = **4824**` ✓
- `conversation.html`：`+4824`（机制层）+ `+24699`（拍 1 的 12082 + 拍 2 的 8806 + 拍 3 ①② 的 3811）= `+29523` ✓

**第二个独立印证**：`verify-design.py` 的「渐变计数」——本拍的暗色块里新增了 1 组 `linear-gradient` + 1 组 `radial-gradient`，
工具按**每页**统计 ⇒ 只有被注入的**那 5 页**各 **+2**：

| 页 | 上一轮 | 本轮 | Δ |
|---|---|---|---|
| automation / avatar / base / settings / skills | 47 / 48 / 62 / 48 / 47 | 49 / 50 / 64 / 50 / 49 | **各 +2** |
| conversation / dev / kanban / req-kanban / task-detail | 63 / 48 / 58 / 54 / 50 | 63 / 48 / 58 / 54 / 50 | **各 0** |

⇒ 工具的**独立计数**替「适配层只落 5 页、一页不多一页不少」做了第二次证明。

**第三个独立印证**：逐页实测护栏（§二十六·1 那张表）——10 页「适配/未适配」的判定与上表**完全同集合**。

---

## 二十、① 批注原点对齐（`noteAt` 单一原点）+ 编辑态「保存」

### 20.1 病根：**三个原点各在一处**

| 物件 | 原来的原点 | 说明 |
|---|---|---|
| 用户点击 | **元素上任意一处** | 点长段落左端 / 右端，语义完全不同 |
| `.td-anchor` 落点 | 被标注元素的**右上角** − 12 | r93 起的读法（稿子只给了锚点长相、没给落点） |
| `.td-elnote` 气泡 | CSS 里写死的 `left: 12px` | **常量**，与点击点无关 |

⇒ 点长段落**左端**时：锚点跑到段落**右端**、气泡钉在视图**左边**，三者互不相干 —— 就是邵先生说的「位置漂移太远」。

### 20.2 修法：把「**本次点击点**」定成唯一原点（`noteAt`）

- 新增 `var noteAt = null;`（`.td-view` 的**内容坐标**，与滚动解耦）；
- 点选监听里记下点击点（`noteAt = { x: e.clientX − viewRect.left + view.scrollLeft, y: … }`）；
- 落锚点时：`.td-anchor`（24×24）的**中心**咬住它；
- 气泡定位：**左边缘**对齐它（并把水平方向也纳入可视带夹取，补上拍 2 只做了竖直方向的那一半）；
- **「预览批注的也是一样」**：点已存在的锚点看详情时，原点 = **锚点自己**（`anchorOpen` 里写 `noteAt`）。

### 20.3 ★ 真机读数（`ev/theme/probe-l3.py` → `ev/theme/l3-origin.log`，**全真鼠标**）

| 项 | 读数 |
|---|---|
| 目标块 | `td-page-card`，box `{l:824, t:326.58, w:181.66, h:95.5}` |
| ★ **真实点击点**（视口） | `{x:880, y:349}` = 目标块**左起 56 / 上起 22**（**刻意偏离中心**，中心落点与左上落点可分） |
| 点击点（`.td-view` 内容坐标） | `{x:88, y:216}` |
| **气泡**（内容坐标） | `l=88, t=297`，尺寸 `356×48`，CSS `left: 88px` |
| ★★ **气泡左 − 点击点** | **0**（期望 ≈ 0） |
| 新增态按钮 | 「**添加**」/「取消」(`display:none`)、`hint display=none`、占位符 `输入你的注释` |
| 提交后锚点数 | `0 → 1`（**就地新增一条**） |
| ★★ **锚点中心（视口）** | **`{x:880, y:349}`** ≡ 真实点击点（**逐整数相等**） |

### 20.4 编辑态文案收口（「添加」⇒「保存」）

- `noteCtrl(on)` 里统一收口：`noteCur`（当前正在编辑的那条记录）查得到 ⇒ 按钮文案**恒为「保存」**。
  这样「编辑态下按一下 Ctrl」不会把文案翻回「添加」。
- ★ 真机（**真鼠标**点开**已存在**的锚点）：

| 项 | 读数 |
|---|---|
| `elnoteHidden` | `false`（气泡打开） |
| ★ 按钮文案 | **「保存」**（不是「添加」） |
| `cancel` display | `flex`（编辑态才长出来） |
| `pin` / `is-done` | `1` / `true` |
| `ok.disabled` | `false` |
| `taValue` | 原文**逐字回填** |
| 气泡顶 − 锚点底 | **8** |
| 气泡左 − 锚点左 | **0** |
| 锚点数 | `1`（**就地 update**，不新增） |

---

## 二十一、② 对话卡片两端对齐（E9）

### 21.1 落点：**不在 `part109/*`**，在生成器的 EDITS 表

`.r93-card` 的 CSS 长在 `apply109.py` 的**内联样式**里，而 `apply109.py` 是 `ev/make109.py` 从 `apply108.py`
**逐字生成**的 ⇒ 与第二拍 ③（图标）**同一条路**：改 `ev/make109.py` 的 `EDITS` 表，本层新增 **E9**。

```diff
 .r93-card {
-  position: relative; width: calc(100% - 18px); margin-left: 18px; border-radius: 8px;
+  position: relative; width: 100%;          margin-left: 0;    border-radius: 8px;
```

> ⚠ 只动**宽度两项**：`border-radius` / `background` / `padding` / 字号 / 高度**一字未动**。
> `.r93-card--full`（`width:100%; margin-left:0`）自此成为本规则的**冗余**，但它是「显式满宽」的语义声明、
> 且被多处调用 ⇒ **保留不动**。

### 21.2 ★ 真机读数（**全量抽查，不是抽一张**）

| 项 | 读数 |
|---|---|
| 单张（`r93-card r93-card--ctx`） | `box {l:45, w:714}`；父 `r93-fb` 内容左 `45`、内容右 `759` |
| `marginLeft` / `marginRight` | `0px` / `0px` |
| ★ `dLeft`（左边缘 − 父内容左） | **0** |
| ★ `dRight`（父内容右 − 右边缘） | **0** |
| ★★ **全量 12 张 `r93-card` 的 `dLeft` / `marginLeft`** | **全 `0` / 全 `0px`**（含 4 张 `--edge`、1 张 `--quiz`、1 张 `--ctx`） |

⇒ 「只改了一处」这种最容易出的漏改，被**全量**排掉。

---

## 二十二、③ 暗色：调研结论 —— 「机制层做了、页面却不变色」的**五类真根因**

### 22.1 先说明一件事实：DS 早就写好了暗色档

`giencoder-design-system/colors_and_type.css` 里本来就有

```css
body[giencoder-theme='dark'], [giencoder-theme='dark'] { … }
```

包含 **12 组色阶 × 10 级**（`--gray-1…10` / `--giencoderblue-1…10` / `--blue-N` / `--red-N` / `--green-N` …）
+ `--color-{bg,text,fill,border}-1…N` 语义色，并且**已内联进全部 10 页**。
⇒ 「切主题」在 token 层**零成本**：只要在 `<html>` 上挂/摘一个 `giencoder-theme="dark"`。

### 22.2 但页面**几乎不变色** —— 逐个定位后一共五类

| # | 根因 | 为什么 token 翻转救不了 |
|---|---|---|
| ① | **第二套 shadcn HSL token 层** | 页面除 DS 外还内联了 `:root{--background:0 0% 98.82%; --foreground:240 4.76% 4.12%; …}`（81 个 token）+ `body{background-color:hsl(var(--background));color:hsl(var(--foreground))}`，**排在 DS 的 `body{…}` 之后、同特异性 ⇒ 它胜出**；这套 token 不在暗色档翻转 ⇒ body 恒为 `rgb(252,252,252)` / `rgb(10,10,11)`，而**满屏文字都是从 body 继承**的 |
| ② | **React 写死的内联样式 / Tailwind 字面色** | `div.flex.h-dvh` 内联 `background: rgb(244,245,246)`；`.bg-[#F4F5F6]` / `.bg-[#E4E6EA]` / `.bg-white` / `[class~="border-[#ECEEF2]"]`；内联 `rgb(229,229,229)` / `rgb(255,255,255)` / `rgb(236,242,255)` ⇒ **内联只输给样式表里的 `!important`** |
| ③ | **页面自定义变量的字面色** | `.av-main{--av-ink-2:#6B6B6B;--av-ink-4:#A9A9A9}`、`.td-browse{--td-code-key:#0451A5;…}`（页面注释自写「DS 暂无对应语义 token」） |
| ④ | **亮色 hover / 激活态** | `.ws-trigger-hover:hover{#e4e6ea!important}`、`.model-dropdown-menu-item:hover{#f3f4f5!important}`、`.ws-dropdown-hover:hover` / `.ws-item-hover:hover`、尾风 `.hover\:\!bg-\[\#E9ECEE\]:hover`（**真实转义是 `!bg`**，不是 `bg`）；静态截图看不见，暗色下会「闪白」 |
| ⑤ | **顶栏装饰位图** | `r92-hdr-css` 给 `header[class*="h-12"]` 铺 `assets/images/bg-img-1.png`（1580×134、平底 `#F6F8FA`、右侧 8px 点距点阵）⇒ 暗色下**整条顶栏**被这张浅色位图盖住（像素实测 `(243,245,248)`，而其余整屏已全暗）；第 101 轮那块再把 `background-size` 改成 `70%` |

> ★ 页面里其实**自带**一份标准的 `.dark{…}` 灰阶变体块 —— 但它是**自成一体的灰阶**（`--background:0 0% 3.92%`），
> **不是 DS 色彩系统**。按邵先生「所有色值全部要来自 giencoder 设计系统的色彩系统」的要求 ⇒ **不用它**，
> 改为把这套 token 在暗色档**重指到 DS 暗色 token**。

### 22.3 ★★ 一个必须写进判据的顺序事实

| 块 | 文档位置 | 与我的块比 |
|---|---|---|
| `r109-dark-css`（我的） | 排在页面**全部样式之后**、`</head>` 之前 | — |
| `r74-nc-css` / `r92-hdr-css` / `r101-hdr-css` / `r88-set-css` / `av-main-css` / `av-browse-css` | **body 内、排在我之后** | ⇒ **只能靠特异性或 `!important` 取胜**（`!important` 平手时**文档顺序**才起作用，而它们在后面） |

⇒ 本层所有与它们竞争的规则：前缀 `html[giencoder-theme='dark']:not([data-r93-page])` 把特异性抬到 **0-2-1 起**，
顶栏那块（要压 `r92` + `r101` 两块**同特异性**注入）再加 `!important`。

---

## 二十三、③-a 机制层（`ev/theme/apply-theme.py`）

### 23.1 为什么「切主题 = 挂一个属性」

底座是 DS 自己的暗色档，页面里**不需要另造一套暗色变量** ⇒ 机制层只做四件事：
**读存储 → 定档 → 挂属性 → 跟随系统变化**。注入两块（`r109-theme-css` 752 + `r109-theme-js` 4072）。

### 23.2 档位与默认值

- `localStorage['gi-ui-theme']`，取值 `light` / `dark` / `auto`；
- **缺省 `auto`（跟随系统）** —— 邵先生 2026-10-02 定的默认档；
- `auto` 档监听 `matchMedia('(prefers-color-scheme: dark)')` 的 `change`（Safari < 14 的 `addListener` 一并兜）；
- 档位本身另留一个**不参与任何样式**的可读标记 `data-gi-theme`（探针 / 以后的顶栏快捷入口用）。

### 23.3 本块只补一件 DS 没管的事：`color-scheme`

`color-scheme` 管的是**浏览器原生部件**（滚动条、`<select>` 下拉、`<input type=checkbox>`、表单自动填充底色、默认焦点环）。
不写的话，暗色页面里会横出一条刺眼的**白色滚动条**。

> ⚠ **刻意不用** `@media (prefers-color-scheme: dark)`：档位由用户**显式选定**（可能是「选了浅色但系统是深色」），
> 媒体查询会把这一格判错。**属性选择器永远跟着用户的档走**。

### 23.4 ★★ 护栏（防结构性「半暗半亮」）

**问题**：机制层是全局的（10 页），适配层本拍只有 5 页 ⇒ 未适配页切暗会变成
「**DS token 翻暗、外壳仍浅**」（外壳底是 React 写死的内联样式 + 尾风字面类，都不吃 token）
⇒ 近白文字压浅底 = **不可读**，直接违反「不破坏稳定性」的硬约束。

**修法**：机制层读 `<html data-gi-dark="1">`（由 `apply-dark.py` 与 `#r109-dark-css` **同进同出**）
⇒ 没有这个属性就 `DARK_OK = false`，**一律按浅色渲染**（不挂属性、不翻 token）。

```js
var DARK_OK = root.getAttribute('data-gi-dark') === '1';
function isDark(m) { return DARK_OK && (m === 'dark' || (m === 'auto' && !!MQ && MQ.matches)); }
```

**为什么用 `<html>` 属性、而不是去查 DOM 里的 `#r109-dark-css`**（两个坑都踩过）：

1. 机制层在 `<head>` 内**同步执行**，此刻它后面的那张样式表**还没被解析出来**，查不到
   ⇒ 会把「已适配页」也误判成未适配，暗色**永远不生效**；
2. 也不能用夹在 `theme-css` 与 `theme-js` 之间的 `<meta>`：会**破坏 `apply-theme.py` 的邻接剥离正则**
   （`RE_THEME` 要求那两块**首尾相接**）。

`<html>` 属性两条都满足：HTML 第一个字节就解析出来、且**不在任何注入块内部**。

### 23.5 首帧（FOUC）

主题块紧跟 r87 的字号块（`r87-ui-js`）之后，仍在 `<head>` 内、仍**早于首次绘制**
⇒ 不会「先画浅色再跳暗色」。与字号机制**同一体位、同一条链**。

---

## 二十四、③-b 设置页「外观」接线 + ★ 真机七步

### 24.1 接线（**捕获阶段** + 不与 `ctlSeg()` 抢）

设置页那三枚按钮（浅色 / 深色 / 跟随系统）由 r85 / r87 的 `ctlSeg()` 生成，此前是**纯装饰**：
点击只切 `aria-pressed` + 弹 toast，不写任何状态、也不改任何东西。

机制层在 **document 捕获阶段**接一手 ⇒ **先于** `ctlSeg()` 自己那个冒泡 handler 跑：

```js
document.addEventListener('click', function (e) {
  var b = e.target && e.target.closest ? e.target.closest('.r85-seg > .giencoder-btn') : null;
  if (!b || !b.parentElement) return;
  var kids = b.parentElement.children, k = 0;
  for (var i = 0; i < kids.length; i++) { if (kids[i] === b) k = i; }
  set(['light', 'dark', 'auto'][k]);
}, true);
```

两边分工：**我负责「落盘 + 切主题」，它照旧负责「pressed + toast」**。

### 24.2 `aria-pressed` 回填（否则会「显示浅色被选、实际跟随系统」）

`ctlSeg()` 生成时**写死**「第 0 枚（浅色）= 真」，而默认档是 `auto` ⇒ 必须回填。
⚠ 面板是 React **晚挂**的：脚本运行时 `.r85-seg` 还不存在 ⇒ 用**短命** `MutationObserver` 等它出现，
回填成功后**立刻断开**（最长 5s 兜底）；常规情况 `syncSeg()` 一次就中，**零开销**。

### 24.3 ★ 真机七步（`ev/theme/probe-appearance.py` → `a-pressed.log`，**三枚按钮全部真鼠标**）

| 步 | 动作 | `mode` | `html` 属性 | `stored` | `aria-pressed` | `--color-bg-1` | 外壳底色 |
|---|---|---|---|---|---|---|---|
| A | 初始（未点） | `auto` | `None` | `None` | `[false,false,**true**]` | `#fff` | `rgb(244,245,246)` |
| B | **真鼠标点「深色」** | `dark` | **`dark`** | `dark` | `[false,**true**,false]` | **`#17171a`** | **`rgb(23,23,26)`** |
| C | 真鼠标点「浅色」 | `light` | `None` | `light` | `[**true**,false,false]` | `#fff` | `rgb(244,245,246)` |
| D | 真鼠标点「跟随系统」 | `auto` | `None` | `auto` | `[false,false,**true**]` | `#fff` | `rgb(244,245,246)` |
| E | `set media dark`（**系统转暗**） | `auto` | **`dark`** | `auto` | `[false,false,true]` | **`#17171a`** | **`rgb(23,23,26)`** |
| F | `set media light`（系统转浅） | `auto` | `None` | `auto` | `[false,false,true]` | `#fff` | `rgb(244,245,246)` |
| G | **reload 后** | `auto` | `None` | `auto` | `[false,false,**true**]` | `#fff` | `rgb(244,245,246)` |

**这一步判三件事**：
1. **A 的回填是对的** —— 第 3 枚「跟随系统」被选中，不是 `ctlSeg()` 写死的第 0 枚「浅色」；
2. **E 证明 `auto` 真的跟随系统**（不是"看起来像"）—— `set media dark` 后属性自动挂上、底色自动翻暗，而**用户没点任何东西**；
3. **G 证明档位持久化 + 回填**（reload 后 `stored=auto` 保留、pressed 仍指向第 3 枚）。

暗色档的「外观」面板见 `raw/theme/dark/settings-appearance.png`（裁切件 `raw/theme/crop/settings-appearance-seg.png`）：
三枚按钮在暗底上读得清，且「跟随系统」那枚有可辨的已选态。

---

## 二十五、③-c 适配层（`ev/theme/apply-dark.py`）

作用域 = **`html[giencoder-theme='dark']:not([data-r93-page])`**
（前者 = 机制层挂的属性；后者 = 把 conversation 排除掉 —— 见 §29.2，
且**一条规则都不在浅色档生效 ⇒ 浅色零风险**）。

| 根因 | 修法 | 关键选择 |
|---|---|---|
| ① shadcn HSL 层 | **`BRIDGE` 17 项**：把这套 token 在暗色档重指到 DS 暗色 token（`background→bg-1`、`foreground→text-1`、`card→bg-2`、`muted-foreground→text-3`、`border→border-2`、`ring→border-3` …） | 消费方是 `hsl(var(--x))` ⇒ **必须写 HSL 三元组**，由右侧 DS token **现算**（不手抄） |
| ② 内联 / 尾风字面色 | `RULES` 一组属性选择器 + 类选择器，**全部带 `!important`** | `[style*="background: rgb(244, 245, 246)"]`、`[style*="color: rgb(107, 107, 107)"]`、`[fill="#1F1F1F"]`… |
| ③ 页面自定义变量 | `LOCAL_VARS`：`.av-main` 的 `--av-ink-2/-4`、`.td-browse` 的 `--td-code-*` | ★★ **DS 阶梯镜像**（见下） |
| ④ 亮色 hover / 激活态 | `HOVERS` 六条页面 hover + 两条尾风 + 两条 `skills-popup-*` | 含**逐字复用** `r74-nc-css` 的长选择器（叠前缀后 0-6-1） |
| ⑤ 顶栏位图 | **不用位图**，按素材同样的几何用 DS token 现画 | `--color-bg-1` 平底 + `rgb(var(--gray-2))` 圆点、8px 点距、只露右侧 ~23%（与素材点阵区一致） |

### 25.1 ★★ 「DS 阶梯镜像」——整个适配层最可证的一条

DS 的原语色阶，浅色档与暗色档是**严格镜像**的（实测 `--gray-N` 浅 ↔ `--gray-(11−N)` 暗）：

| 浅色档 | 值 | ↔ | 暗色档 | 值 |
|---|---|---|---|---|
| `--gray-1` | `247,247,247` | ↔ | `--gray-10` | `247,247,247` |
| `--gray-4` | `201,201,201` | ↔ | `--gray-7` | `201,201,201` |
| `--gray-5` | `169,169,169` | ↔ | `--gray-6` | `169,169,169` |
| `--gray-7` | `107,107,107` | ↔ | `--gray-4` | `107,107,107` |
| `--gray-10` | `31,31,31` | ↔ | `--gray-1` | `31,31,31` |

而页面里那些字面值**恰好踩在某个阶梯步上**（`#6B6B6B` ≡ `--gray-7` 浅；`#A9A9A9` ≡ `--gray-5` 浅）
⇒ 暗色档直接写 `rgb(var(--gray-7))` / `rgb(var(--gray-5))`，**自动取到同一步阶的镜像亮度**。
**可证、可核、浅色零风险**（浅色档那条规则根本不生效）。

### 25.2 为什么是「按需收敛」而不是「全量替换」

- 全量重写会**动到不必涉及的规则**（违反硬约束）；
- 按需收敛的边界很清楚：**只改「暗色下会不可读 / 会闪白 / 会整块盖亮」的地方**，
  其余一律交给 DS 自己的暗色档；
- 收敛完的**验收判据**也是可量化的：像素级亮像素占比 + 残留清单（见下节）。

---

## 二十六、③-c 双档取证

### 26.1 像素级（`raw/theme/{light,dark}/*.png` + Pillow 复算，1440×900）

判据：`lum = (0.2126R + 0.7152G + 0.0722B)/255`，统计 `lum > 0.55` 的像素占比；
另按 **12×8 网格**找热点格（每格 120×112 px）。

| 页 | 浅色档亮像素比 | 暗色档亮像素比 | 暗色最热格 |
|---|---|---|---|
| base | 0.9917 | **0.0094** | 0.088 |
| avatar | 0.9792 | **0.0361** | 0.156 |
| automation | 0.9913 | **0.0120** | 0.216 |
| skills | 0.9906 | **0.0131** | 0.181 |
| settings | 0.9928 | **0.0131** | 0.082 |

⇒ 暗色档亮像素 **≤ 3.6%**，且**热点格全部 ≤ 0.22**（下面逐个落实身份）。

### 26.2 ★ 三个「看着亮」的残留 —— 身份**全部落实**（不是"忽略"，是"证明它是合法的"）

| 残留 | 位置 | 身份 | 结论 |
|---|---|---|---|
| automation / skills 热点格 `(9,0)`、`(10,0)`（0.216 / 0.181） | 顶栏右侧 + 主区按钮 | **① 顶栏点阵**（`rgb(var(--gray-2))` = `(43,43,43)`，DS 暗色档实测值）+ **② 蓝色主按钮**（`(84,151,255)` ≡ `--giencoderblue-6` **暗色档**值，镜像浅色 `#3770F7`） | **合法**：主色按钮在暗色下本就该亮；点阵是素材几何的忠实复刻 |
| avatar 热点格 `(4,3)`（0.156） | 正文区 | **文字字形**（`--color-text-1` 暗 = `rgb(247,247,247)`） | **合法**：暗底上的正常文字 |
| base 暗色 `darkFg` 2 项 | `p` / `div.pb-6.text-center…` | **`--color-text-4`**（DS 的「四级文字」token：浅 = `rgb(201,201,201)`、暗 = `rgb(107,107,107)`） | **不是回归**：浅色档对比度 **1.67:1**、暗色档 **2.90:1** ⇒ 暗色档**反而更清楚**；探针把它标出来属于启发式误报 |

**定点采样**（暗色档，`raw/theme/dark/*.png`）：

| 采样点 | 暗色档 | 浅色档 | 说明 |
|---|---|---|---|
| skills 顶栏底 | `(23,23,26)` | `(246,248,250)` | = `--color-bg-1` 暗 / 浅 |
| skills 顶栏点阵 | `(43,43,43)` | `(221,227,235)` | = `--gray-2` 暗（镜像浅色档） |
| skills 主区底 | `(23,23,26)` | `(255,255,255)` | = `--color-bg-1` |
| skills 侧栏底 | `(23,23,26)` | — | 同上 |
| skills 主按钮 | `(84,151,255)` | `(55,112,247)` | = `--giencoderblue-6` 暗 / 浅 |
| base 主区底 | `(35,35,36)` | — | = `--color-bg-2` 暗 |
| settings 卡片底 | `(31,31,31)` | — | = `--color-bg-3` 暗 |

### 26.3 残留清单（CSS 侧，收敛后）

| 项 | base | avatar | automation | skills | settings |
|---|---|---|---|---|---|
| 暗色档 `brightBg` | **1** | **1** | **1** | **1** | **6** |
| 暗色档 `darkFg` | **2** | **0** | **0** | **0** | **0** |

- `brightBg` 的 1 项（5 页共有）：`button.size-3.rounded-full.bg-[#FEBC2E]` = macOS **黄灯点** —— **必须保留**；
- settings 多的 5 项：
  - `span.giencoder-switch-handle`（×3）= `--color-white`（暗色档**刻意不缺省** ⇒ 浅色圆钮在暗色下是常规做法）；
  - `.r85-sl-tick.is-on`（×2）/ `.r85-sl-done` / `.r85-sl-thumb` = `--color-text-1`（暗 = `rgb(247,247,247)`）
    —— 它们是**滑块的刻度 / 已选段 / 滑柄**，必须在轨道上**高对比**，用 text-1 是**设计本身的定义**；
- `darkFg` 的 2 项 = `--color-text-4`（见 §26.2 第三行）。

### 26.4 浅色档**零变化**

- 适配层全部规则的前缀是 `html[giencoder-theme='dark']…` ⇒ 浅色档**一条都不匹配**；
- 独立印证：`verify-design.py` 的逐页问题数**完全不变**（76 = 🟡66 / 🔵10 / 🔴0），
  与上一轮的差异**只有**「5 页各 +2 渐变」+ 行号偏移 + `gaps.log` 自身；
- 逐页护栏表里 5 个未适配页切暗后**底色分毫不变**（`rgb(244,245,246)` / `rgb(229,237,245)`）。

### 26.5 ★ 护栏逐页实测（`ev/theme/scan-guard.sh` → `g-run.log`）

| 页 | `supported` | 请求 `dark` 后的 `html` 属性 | `--color-bg-1` | 外壳底色 | `isDark` |
|---|---|---|---|---|---|
| base / avatar / automation / skills / settings | **`True`** | **`dark`** | **`#17171a`** | **`rgb(23,23,26)`** | **`True`** |
| conversation / dev / kanban / req-kanban / task-detail | **`False`** | **`None`** | `#fff` | `rgb(244,245,246)` / `rgb(229,237,245)` | **`False`** |

⇒ 未适配页**即便被显式请求 `dark`，也一律保持浅色** —— 「半暗半亮」在**机制层就被拦住**，不是靠适配层补救。

---

## 二十七、幂等与门禁（第三拍定稿后复跑）

| 项 | 命令 | 读数 |
|---|---|---|
| 机制层幂等 | `python ev/theme/apply-theme.py`（第二次） | **变更 0 页 / 已是目标态 10 页** |
| 适配层幂等 | `python ev/theme/apply-dark.py`（第二次） | **变更 0 页 / 已是目标态 5 页** |
| 本层补丁幂等 | `python ev/patch109l3.py`（第二次） | **应用 0 项 / 跳过 12 项**，跨层自检**全部存活 ✓** |
| 生成器幂等 | `python ev/make109.py`（连跑两遍） | 两遍都是 **3676 行 / 192105 字符 / 10 处替换** |
| ★★ **整链固定点** | 按 §19.4 的 7 步**连跑两轮** | 两轮产物 **quickhash 完全一致**（`149403f4de5cda353026b4fe5374b830`） |
| ★★ **往返无损** | `apply109` 把适配块带进 conversation（`+10951`）→ `apply-dark` 越界清扫摘回（`−10951`） | `conversation.html` **md5 逐字节还原**（`55a1f9a3135e3522c8fe0b893a791367`） |
| 语法门禁 | `python mg-work/check-syntax.py pages/*.html` | **10/10 通过** |
| 字号压平门禁 | `python mg-work/r108/ev/scan-flatten.py mg-work/r109/part109/panel.css` | **仍 2 条**（基线 `.td-mod-bar` / `.td-url`）⇒ 本拍**没引新的可压平规则** |
| 设计回归门禁 | `python verify-design.py ./pages` | 汇总 **76 不变**（🟡66 / 🔵10 / 🔴0）；与上一轮差异**只有** 5 页各 +2 渐变 + 行号偏移 |
| 跨代标记 | `panel.css` / `panel.js` | `r107-l1` · `r108-l*` · `r109-l1` · `r109-l2` · `r109-l3` 全在 |

> ⚠ `apply109.py` **单独**不是固定点（每轮都会把适配块从 `base.html` 的净底带进 `conversation.html`）——
> 但它在**文档改序里的位置**就是「适配层之前」，而 `apply-dark.py` 的**越界清扫**每轮强制
> 「适配块只存在于被适配的 5 页」。**链的固定点成立**（上表第 5 行），且往返**逐字节无损**（第 6 行）。

---

## 二十八、第三拍改动清单 · 交接

### 28.1 交付面（进 `git diff` 的 10 页 + 记忆）

见 §19.5 那张表（三方独立印证）。`pages/gaps.log` 被 `verify-design.py` 写过 ⇒ **收尾 `git checkout --` 还原**。

### 28.2 `mg-work/r109/`（过程资产，不进 `git diff`）

- **新建**：`ev/theme/apply-theme.py`（9549）· `ev/theme/apply-dark.py`（25406）
  · `ev/theme/{scan-dark2.sh, scan-guard.sh, probe-appearance.py, probe-appearance-shot.py,
  probe-l3.py, chk-net.py, p-verify.js, p-guard.js, p-seg.js, p-state.js, p-l3{a,b,c,d}.js,
  p-theme.js, p-hard.js, p-why.js, p-chain.js, p-composer.js, p-anc.js, p-body.js, p-dark.js, p-shell.js}`
  · `ev/theme/bak-l3d/`（收尾排障用的全量快照）
- **改动**：`ev/patch109l3.py`（25098 → **29068**，加 ③-d 的 E10 + 更新改序）· `ev/make109.py`（7629 → **10681**）
- **资产**：`raw/theme/{light,dark}/*.png`（10 张）· `raw/theme/crop/*.png` · `raw/l3-note-edit.png`
  · `ev/theme/{v-*,g-*,s-*,a-pressed.log,l3-origin.log,l3-*.json,final-gate*.log,d7-run.log,g-run.log,pa-run2.log}`

### 28.3 交接给邵先生

**三条全部按逐字需求落地、真机取证完毕**；③ 按您定的范围（机制层 + 基础工作台 5 页）、默认档（跟随系统）、
收敛尺度（按需收敛）落地，**所有色值来自 DS 色彩系统**（页面自带的非 DS 灰阶块**刻意未用**）。

仍**未 commit**（等显式指示）。下一拍若要动研发工作台 5 页的暗色，按硬规则：
**本代未交付 ⇒ 就地改 `ev/theme/*.py` 与 `ev/patch109l*.py`**，范围表 `SCOPE` 扩到 10 页即可（护栏天然支持）。

---

## 二十九、本拍反例集（★ 每条都真踩过，都值得进 PLAYBOOK）

### 29.1 ★★ 判据不能写「裸串」—— 但这次是**注释**里的裸串把链打死了

**现象**：收尾复跑门禁时 `python mg-work/r109/apply109.py` 突然报

```
!! 摘块后基线里仍残留标记 'r101-hdr-css'
```

**定位**（`ev/theme/chk-net.py` 复刻了它的净底自检）：`apply109.py` 剥完四类注入块后，
要求净底里**不得再出现** `r101-hdr-css` / `r93-conv-host` / 各代 `rXXX-conv-css|js` 这些 token。
而我在 `r109-dark-css` 的**中文注释**里写了

```
⚠ 本块注入在 `</head>` 前，而 `r88-set-css` / `av-main-css` / `av-browse-css` /
  `r92-hdr-css` / `r101-hdr-css` 都在 **body 内、排在本块之后** ⇒ …
```

⇒ 那个**字面**留在净底里 ⇒ 自检炸 ⇒ **整条 apply 链断掉**（自愈能力归零）。

**修法**：把注释里的注入块 id 字面全部去掉（改写成「第 92 / 101 两代顶栏装饰块」这种**不含 token 的说法**），
并在生成器里补一条**防止后人再犯**的硬警告：*写本块注释时不得出现任何注入块 id 的字面*。

> ★ 这条与 PLAYBOOK 的老规矩同源（**判据不能写裸词 / 裸前缀 / 裸后缀 / 裸子串**），
> 但这次的角色反了：不是「我的判据写松了」，而是「**我的产物里多了一个别人判据盯着的字面**」。
> ⇒ 新规矩：**往产物里写注释时，先想清楚有没有别的层会拿这些 token 当判据。**

### 29.2 ★★ 给 `<html>` 加属性，会**打断下游的逐字锚点**，还会**外溢护栏**

**现象**：修好 §29.1 后，`apply109.py` 接着报

```
!! <html> 锚点命中 0 次（应 1 次）
```

**根因**：`apply109.py` 用 `HTML_OLD = '<html lang="zh-CN">'` **逐字**匹配，再把 conversation 的 `<html>`
换成带 `data-r93-page="conversation"` 的版本。而护栏给被适配页写成了
`<html lang="zh-CN" data-gi-dark="1">` ⇒ **子串不再存在** ⇒ 命中 0。

**更危险的是「放过去会怎样」**（这才是必须一起修的）：
- conversation **丢掉 `data-r93-page`** ⇒ 暗色块的作用域锚失效；
- 而且护栏标记**随净底外溢**到 conversation ⇒ 机制层认为它「已适配」⇒ **未适配页会被真正切暗**
  ⇒ 就是护栏本来要防的**半暗半亮**。

**修法（E10，落在 `ev/make109.py` 的 EDITS 表）**：

```python
_i = net.find('<html')
if _i < 0 or _i > 200:
    sys.exit('!! `<html` 开标签位置异常（%d）' % _i)
_j = net.find('>', _i)
_attrs = re.sub(' *data-(?:gi-dark|r93-page)="[^"]*"', '', net[_i + 5:_j])
conv = (net[:_i] + '<html' + _attrs + ' data-r93-page="conversation">' + net[_j + 1:])
```

① 认**文档里第一个** `<html` 开标签（属性任意）；
② 落 `data-r93-page` 前**先摘掉** `data-gi-dark` 与旧 `data-r93-page`。

> ★★ **第一次修还踩了一脚**：我原本写的是 `<html[^>]*>` 全串正则 ⇒ 报「命中 **8** 次」。
> 原因是**我自己那些注释里**写了 `<html>` / `<html data-gi-dark="1">` 字面，被正则一起数了。
> ⇒ 与 §29.1 **同一个陷阱**：**注释里的 HTML / id 字面，会被别的层的正则当成真货**。
> 最终改成 `find('<html')` + 位置上限断言（`_i <= 200`），彻底不用正则。

### 29.3 ★ 机制层与适配层覆盖范围不同 ⇒ **必须设护栏**

机制层全局（10 页）、适配层本拍 5 页。没有护栏时，未适配页切暗 =
「DS token 翻暗 + 外壳仍浅（React 内联 + 尾风字面都不吃 token）」= **近白文字压浅底**。
护栏落在 `<html data-gi-dark="1">`，与适配块**同进同出**（`apply-dark.py` 一个脚本里同时管两件事）
⇒ 不存在「改了机制忘了改护栏」。

★ 为什么不能用「查 DOM 里的 `#r109-dark-css`」：机制层在 `<head>` 里**同步执行**，那张样式表**还没解析**。
★ 为什么不能用 `<meta>`：会破坏 `apply-theme.py` 的**邻接**剥离正则（两块必须首尾相接）。

### 29.4 ★★★ `agent-browser` 的输出**绝不能接管道**

CLI 会把 stdout 写端交给它 fork 的**常驻守护进程** ⇒ 管道**永不 EOF** ⇒ `| tail` / `| head` **永久等待**
（症状 = 命令「挂死」、无输出、最后 SIGTERM）。
**一律 `subprocess` + 重定向到文件**（本拍所有探针脚本都按这条写，`scan-*.sh` 头部也写了警告）。

### 29.5 ★★ 注释里的裸 `<style` 会撑破 `check-syntax.py`

它的 `STYLE_RE = re.compile(r'<style\b([^>]*)>(.*?)</style\s*>', re.S|re.I)` 是**纯文本正则**
⇒ 注释里出现**裸的 `<` + `style`**（或 `<` + `script`）字面，会被当成开标签吞掉后续内容，
报「花括号 / 注释不配对」。本拍真踩（改措辞后 10/10 通过）。

### 29.6 ★ 反例三则（收尾排障时用上的小判据）

1. **`grep` 在本机查中文返回空** ⇒ 一律用 Python 读片段；
2. **`bash -c` / `python -c` 里的 `\s` 会被 shell 吃掉**（变成 `/s`）⇒ 复杂正则写进文件再跑，别塞进 `-c`；
3. **`diff` 两份「看起来完全不同」的报告时先 `--strip-trailing-cr`** —— 本拍 1336 行差异其实是**行尾 CRLF**，
   内容**逐字节一致**（差点误判成回归）。


---

# 30. 第四拍 · 邵先生四条（DS 释义 / 色值铁律 / 全站浅暗适配 / 更新任务卡缩进）

> 全部落点仍在 **r109 未交付期** ⇒ 返工**就地**改 `ev/theme/*.py` 与 `ev/make109.py`，
> **未新建 r110**，**未 commit / 未 push**。
> 链序：`make109.py` → `apply109.py` → `apply-theme.py` → `apply-dark.py` → **`apply-tokens.py`**（本拍新增，排最后）。

## 30.1 第 4 条：「更新任务清单卡」左缩进去掉（E11）

| 项 | 值 |
|---|---|
| 落点 | `make109.py` 的 `EDITS` 表首项 **E11**（源 `r108/apply108.py` 命中 **1** 次） |
| 旧 | `.r93-todocard { position: relative; **width: calc(100% - 18px); margin-left: 18px;** … }` |
| 新 | `.r93-todocard { position: relative; **width: 100%; margin-left: 0;** … }` |

★ `.r93-card` 本来就已经是 `width: 100%; margin-left: 0`，**两张卡现在同宽**。
★ 卡的 `height: 220px; padding: 16px 20px 12px; border-radius: 8px; background/border` **一字未动**
（定高卡 ⇒ 只动横向，绝不动高度 —— 这是本任务唯一的风险点）。
★ 锚点必须带 `.r93-todocard {` 那一行：裸 `width: calc(100% - 18px); margin-left: 18px` 在 `apply108.py`
里**命中 2 次**（E9 注释里的引用 + 本规则）；带宿主行后收敛到 **1**。

## 30.2 第 2 条铁律：色值一律走 DS 变量（**不做无授权的泛化替换**）

### 30.2.1 先把「DS」是什么钉死（第 1 条）

`giencoder-design-system/colors_and_type.css`（22204 字符 = **DS 本体**），结构三段：

1. **13 个原语族 × 10 级**，以 **RGB 三元组**书写、由 `rgb(var(--族-级))` 消费：
   `blue / cyan / giencoderblue / gold / gray / green / lime / magenta / orange / pinkpurple / purple / red / yellow`。
2. **90 个语义 token**：`--color-bg-1..5`、`--color-text-1..4`、`--color-fill-1..4`、
   `--color-border-1..4`、`--color-primary/danger/success/warning/link`、`--color-white/black`、
   `--color-mask-bg`、`--color-tooltip-bg`、`--color-spin-layer-bg`、`--color-menu-dark-*` …
3. **暗色档** `body[giencoder-theme='dark'], [giencoder-theme='dark'] { … }`。

★★★ **本拍最重要的机制发现 —— 「阶梯镜像」**：

| 原语 | 浅色档 | 暗色档 |
|---|---|---|
| `--gray-1` | 247,247,247 | **31,31,31** |
| `--gray-10` | 31,31,31 | **247,247,247** |

即 **暗色档 = 浅色档逐级镜像**（`N` ↔ `11-N`），**同族同索引在暗色档拿到相反亮度**。
⇒ 于是：

- **原语阶梯 / `--color-text-*` / `--color-fill-*` / `--color-border-*`** 写着 `rgb(var(--gray-N))`，
  **暗色档自动翻转**（语义 token 里大部分**不在暗色档重声明**，纯靠镜像生效）。
- 只有 **`--color-bg-1..5`** 是**字面重声明**（浅色全 `#ffffff` → 暗色 `#17171A / #232324 / #2E2E30 / #484849 / #5F5F60`）。
- **`--color-white` / `--color-black` 两档都不重声明** ⇒ 「必须保持白/黑」的语义锚点。

★ **`#e5edfe` 为什么会漏**：它落在自定义属性 `--td-bubble` 上，而自定义属性「消费方看不出来」⇒
脚本对自定义属性只收 **Δ ≤ 6**；`#E5EDFE → --blue-1` 是 Δ**10** ⇒ 被挡。本拍进 OVERRIDE 表放行。

★★★ **另一个必须记住的坑（本拍重新确认）**：**`neutral()` 判不出「冷灰」**。
`#E5EDF5` 三通道极差 **16**（245-229）⇒ 被判「有色相」⇒ 走「最近通道」全局搜索 ⇒
**被挑到 `--green-1`（236,247,236，Δ10）** —— 冷灰被拉成**浅绿**。
最近的**灰**阶是 `--gray-3`（Δ**16**，超过 1 级）⇒ 两条路都不可接受 ⇒ **保留字面 + 暗色档定向覆盖**。

### 30.2.2 本轮实际落地的替换（**两批，共 242 处**）

| 批次 | 手法 | 处数 | 浅色档最大 Δ |
|---|---|---|---|
| 批次一 | 纯启发式（EXACT 逐位等值 / NEAR 最大通道差 ≤ 12） | **210 处 / 38 值** | ≤ 10 |
| 批次二 | **显式 OVERRIDE 表**（逐条人工核对「角色 + Δ」，Δ 全 ≤ 11） | **32 处 / 12 值 / 6 页** | ≤ 11 |

批次二的 12 条（全部落在**会随档翻转**的 token 上 ⇒ **一处改动同时解掉铁律 2 与第 3 条**）：

| 值 | → | 角色 | Δ |
|---|---|---|---|
| `#E5EDFE` | `rgb(var(--blue-1))` | 用户聊天气泡底（`--td-bubble` / `--r93-bubble`） | 10 |
| `#D3E2FF` | `rgb(var(--giencoderblue-2))` | 激活 / 悬停描边 | 7 |
| `#E7EBF1` | `rgb(var(--gray-2))` | 发丝线 / 面包屑线 | 11 |
| `#EBEBED` | `rgb(var(--gray-2))` | 会话分隔线（`--r93-line`） | 7 |
| `#EBECED` | `rgb(var(--gray-2))` | 看板表格线 / 分割线 | 7 |
| `#333333` | `rgb(var(--gray-9))` | 主图标色（`--r93-ioc`） | 10 |
| `#FDDDC3` | `rgb(var(--orange-2))` | 标签描边 | 9 |
| `#E7F0FF` | `rgb(var(--blue-1))` | 蓝标签底 | 7 |
| `#FF6157` | `rgb(var(--red-5))` | 状态·延期 | 8 |
| `#3686FF` | `rgb(var(--blue-6))` | 状态·协同 | 11 |
| `#DAE3ED` | **双角色分流**：`var(--color-fill-3)`（面） / `var(--color-border-2)`（线） | 顶栏底 / 分栏描边 | 11 |
| `#3491FA` | 豁免（属性名含 `logo` ⇒ 品牌 logo） | — | 0 |

★ `#DAE3ED` 的**双角色分流**靠属性名正则（`line|border|bd|edge|hairline|stroke|outline|divider`）——
两档**数值相同**，但「面」该给 `--color-fill-*`、「线」该给 `--color-border-*`（实测 7 : 1）。

### 30.2.3 ★ 侦察工具自身的两处修正（否则数字虚高 2.6 倍）

`hard-colors.py` 原来**不判属性** ⇒ 报「**454** 处硬编码」。补上属性豁免后真实为 **176 处 / 68 值**：

1. **41 处 `#000000` 全在 `mask-image` / `-webkit-mask-image` 里** —— 那是**遮罩 alpha 通道，根本不是颜色**
   （例：`mask-image: linear-gradient(#000 calc(100% - 52px), transparent)`）。原样列出会误导人。
2. 阴影 / `filter` 里的黑白色是**主题中性 scrim**，DS 用 `--shadow*` **整条**表达，不拆色值。
3. 另外原来**没跳过暗色规则** ⇒ 会把 `[giencoder-theme='dark'] { … }` 里的**暗色值**也算进来。

★ 收尾据此新增判据：**「报出 ≠ 未适配」，侦察器必须与替换脚本的豁免表逐条对齐。**

## 30.3 第 3 条：全站（**10 页**）浅暗适配

### 30.3.1 范围扩到 10 页 + 去掉护栏排除

`apply-dark.py`：`SCOPE` 5 页 → **10 页**；`PRE` 从 `html[giencoder-theme='dark']:not([data-r93-page])`
去掉 `:not(...)`。

★★ **为什么扩范围就能生效**：各页**早就自带页面级暗色档**（`[giencoder-theme='dark']{ --r93-line…}`、
`[giencoder-theme='dark'] .td-browse{…}`、kanban 的十余条 `.kb-*` 等），它们不生效的**唯一**原因是
机制层护栏 `data-gi-dark` 没挂 ⇒ `DARK_OK=false` ⇒ 一律按浅色渲染。

### 30.3.2 真机量化（`p-mix.js` 暗色探针，全 10 页，**三轮**）

| 轮次 | 亮残合计 | 说明 |
|---|---|---|
| 扩范围前 | **86** | 适配层只 5 页 |
| 扩范围 + ⑥-a/b/c | **51** | dev / kanban / req-kanban / task-detail 外壳与彩底 |
| **本拍（⑥-d/e + 批次二）** | **49** | 两处**真缺陷**归零 |

★★ 49 的构成（**已逐条定性**）：

| 项 | 处数 | 定性 |
|---|---|---|
| macOS 交通灯 `#FF5F57` / `#FEBC2E` / `#28C840`（shadow ×3 + bg ×1，每页 4 处） | **40** | **正确**（窗口装饰，非产品用色；品牌/系统豁免） |
| settings `.r85-sl-done` / `.r85-sl-thumb` = `rgb(247,247,247)` | 4 | **正确**（`var(--color-text-1)`，暗色档就是该亮） |
| conversation `.r93-adot` = `rgb(255,182,93)` | 2 | **正确**（`rgb(var(--orange-7))`：浅 `210,95,0` → 暗 `255,182,93`，**确实在翻转**） |
| settings `.giencoder-switch-handle` = `#fff` | 3 | **正确**（`var(--color-white)`，两档都是白，DS 组件本体） |

### 30.3.3 本拍修掉的**两处真缺陷**

1. **`task-detail .td-msg-user` 用户气泡** —— `--td-bubble: #E5EDFE`（**浅色硬编码**，不随档翻转）
   ⇒ 暗色下是**亮蓝气泡**。修法：`→ rgb(var(--blue-1))`（浅 Δ10，暗自动转深蓝）。
2. **`settings .r85-sw.giencoder-switch` 未选中轨道** —— r85 为对齐设计稿（40×24）加了**页面级覆盖**
   `background: rgb(var(--gray-7))`，把 DS 组件本体的 `var(--color-fill-3)` 顶掉了。
   浅色 `--gray-7` = 107（中深灰，符合设计稿）；**暗色档镜像 ⇒ `--gray-7` = 201** ⇒ 轨道**发亮**，
   看着像「已开启」，**语义反了**。
   ★ 修法 = **保亮度不保索引**：暗色档改挂 `rgb(var(--gray-4))`（暗色档 = 107），与浅色档**同亮度**。
   ★ 这是全站**唯一**一处「页面覆盖 DS 组件本体」的取色（实测扫出），已记入 PLAYBOOK。

### 30.3.4 ★★ 必须撤掉的两个旧覆盖（否则新值被顶回错的）

批次二把 `--td-appbar` / `--td-pane-line` / `--r81-hover-bg` 的**字面值**换成了
`var(--color-fill-3)` / `var(--color-border-2)`（自身即随档翻转）⇒ 必须从 `PAGE_VARS` **撤掉**。
否则 `--td-pane-line` 会拿 `--color-border-1`（暗色档 = **242 浅灰**）盖掉正确值
⇒ 暗色下多一条**发亮的分栏线**。（本拍真踩，靠删条目收敛。）

## 30.4 「不得影响浅色模式」的**像素级取证** + **噪音底**（本拍新增方法论）

### 30.4.1 ★★★ 先量「噪音底」再谈「有没有改坏」

同一页面、同一状态**连拍两张**（`shots-t1` vs `shots-t1b`），逐像素 diff：

| 结论 | 数值 |
|---|---|
| 有差异像素 | **0.00% ~ 0.13%**（多数 0.02%，kanban 最差 0.09%~0.13%） |
| **最大 Δ** | **最高 ~196**（抗锯齿 / 1px 位移） |

⇒ **判据**：Δ 大**不等于**改色 —— **0.02% 量级 + 大 Δ = 像素互换（位置/抗锯齿）**；
真正改色要看 **大面积 + 中小 Δ**。这条直接把上一轮「Δ41 像素互换 = 改色」的误判纠正掉。

### 30.4.2 终态 vs 基线（浅色档）

| 页 | 差异像素 | maxΔ | 归因 |
|---|---|---|---|
| dev / settings / req-kanban-light | **0.00%** | 0 | 批次二对这三页浅色**零影响** |
| base / automation / skills / avatar-light | 0.02%~0.14% | ≤ 166 | **在噪音底内** |
| kanban-light | 0.95% | 162 | 主因 `--kb-appbar/tbl-line/tag-blue-bg`（Δ7~11） |
| conversation-light | 3.92% | 115 | 主因 E11 布局位移（Δ1-2）+ 气泡 `#E5EDFE→blue-1`（Δ10） |
| task-detail-light | 1.26% | **11** | 顶栏 Δ11 + 气泡 Δ10 |

★★ **浅色档全部真实改动收敛在 Δ ≤ 11**（且最大那几处 Δ11 / Δ10 正是邵先生授权的
「就近映射 ≤1 级色差」）；所有 Δ > 11 的像素都落在**噪音底量级**内。

### 30.4.3 暗色档的改动是**有效改动**（不是噪音）

以 `shots-t1b`（同态基线）为参照，本拍在暗色档的差异集中在 **Δ81-255** 桶：

| 页 | 暗色差异像素 | Δ81-255 | 定性 |
|---|---|---|---|
| task-detail-dark | **6.49%** | 82880 | 气泡 + 顶栏**由亮转暗** ⇒ 正是要的效果 |
| req-kanban-dark | 1.18% | 14399 | 同上（外壳 / 线） |
| kanban-dark | 0.61% | 6772 | 同上 |
| dev-dark | 0.55% | 6766 | 同上 |
| settings-dark | 0.14% | 1435 | 开关轨道 `201 → 107` |

## 30.5 门禁（收尾两跑）

| 门禁 | 结果 |
|---|---|
| `check-syntax.py pages/*.html` | **10/10 通过**（script/style 计数逐页列出） |
| `verify-design.py ./pages` | **75 个问题 / 0 critical**；其中「硬编码色值」类 **2 → 1**（基线 76 → 75，**无新增**） |
| `apply-dark.py` 幂等复跑 | **变更 0 页 / 已是目标态 10 页** |
| `apply-tokens.py` 幂等复跑 | **合计 0 处** |

★ 独立印证：`verify-design.py` 只剩 **1** 条硬编码色值（`req-kanban.html:976`
`.rq-type--sub { color: #0FA79A }`）—— 它与本拍侦察器的结论**独立**对上。

## 30.6 ★ 待裁决（未做，**已量化**，不擅自落地）

**剩余硬编码的诚实口径 = CSS 144 处 + `<script>`（React bundle）146 处。**

★ 为什么 `<script>` **整块跳过**：JS 里的色值可能是**字符串拼接 / 模板 / 状态机**，替换语义不可控
（本拍实测：JS 内共 **146 处 / 36 值**，集中在**文件类型图标色**（`#FFA000` 文件夹 / `#2196F3` /
`#699650` / `#DE8F3E`）、**图标字形色**（`#A9A9A9` / `#6B6B6B` / `#7766FD`）、**品牌**（`#EA4335` Google 红 / `#FFFFFF`）。

**CSS 侧剩余分五类；共同点 = DS 里没有 ≤1 级色差的等价 token**：

| # | 类别 | 代表值 → 最优候选 | Δ | 说明 |
|---|---|---|---|---|
| 1 | **类型/状态标签前景色**（系统性） | `#7766FD`→`--purple-5` / `#F3881E`→`--orange-5` / `#0FA79A`→`--cyan-7` / `#5592EB`→`--giencoderblue-5` / `#009E61`→`--green-8` | **15~56** | **规律极清晰**：底已是 `rgb(var(--族-1))`，前景就是**同族深档** ⇒ 语义无歧义，只是 Δ 大 |
| 2 | **代码语法高亮** | `#0451A5`→`--blue-8`(13) / `#A31515`→`--red-8`(9) / `#098658`→`--cyan-9`(**37，绿变青**) | 9~37 | 邵先生已表态「语法高亮色也要收敛」；暗色档已在 `LOCAL_VARS` 里另给了一套 |
| 3 | **头像身份色板** `--avatar-bg-1..7` | `#E57470` / `#E88B4D` / `#DCAB35` / `#A2C143` / `#67B85D` / `#47C2C4` / `#4C93D4` | 大 | 类似 Gmail 的身份色，**偏品牌** |
| 4 | **冷灰外壳** `#E5EDF5` | 无（灰阶 Δ16 / 误配绿 Δ10） | 16 | 已用暗色档定向覆盖（浅色零变化） |
| 5 | **暗色半透明浮层** `rgba(29,33,41,.8)`（`.avatar-tooltip`，10 页 ×2） | `--color-tooltip-bg`（**但暗色档翻成近白，会白字压白底**） | — | 现状是**两档都成立的磨砂深底**，属「主题中性」而非缺陷 |

★ 这五类**没有一条**能在「Δ ≤ 1 级」与「不动浅色模式」两条同时成立下映射。
⇒ 按邵先生「若有不确定的因素可以询问我」，**列此表待裁决**，不擅自落地。

---

# 三十一、第九拍 —— 下拉菜单面板配色统一到「默认权限」基准

## 31.1 起因与真机取证

邵先生：「全局所有的下拉菜单的暗色模式没有统一，全部以基础工作台对话框『默认权限』的
下拉菜单的暗色模式的配色为准。」+「比如 base.html 页面选择工作目录、选择大模型、添加、
标准模式等这些下拉菜单的配色等细节没有与『默认权限』的下拉菜单的配色统一起来。」

真机取证（`raw/dd9-dark/panel-*.json`）显示暗色档面板底**差 64 级**：

| 面板 | 暗色底 | 磨砂 | 判定 |
|---|---|---|---|
| 默认权限（**基准**） | `rgba(31,31,31,0.88)` | `blur(10px) saturate(100%)` | 基准 |
| 技能 | `rgba(31,31,31,0.88)` | `blur(10px) saturate(100%)` | ✅ 已同基准 |
| 标准模式 / 大模型 / 工作目录 | `rgb(95,95,96)` | 无 | ❌ 亮 64 级 |
| 添加 | `rgb(35,35,36)` | `blur(20px)` | ❌ 暗一级且无边框 |

**根因 = 三种面板用了三个不同 DS 变量**：基准 = `rgba(var(--gray-1), 0.88)`（半透明+磨砂）；
select 浮层 = `var(--color-bg-5)`（暗色 `#5f5f60`，不透明）；添加菜单 = `var(--color-bg-2)`。

## 31.2 `ev/theme/apply-popup.py`（链尾第 8 层）

**只做整条精确配对**（写死原文 → 新文 + 断言全站次数），不做通用改值：

| 配对 | 处数 | 新规格 |
|---|---|---|
| `.giencoder-select-popup` 底 | 10（每页 1） | `rgba(var(--gray-1),0.88)` + `blur(10px) saturate(100%)` |
| 添加菜单 inline 底 | 2（base/conversation） | 同上（磨砂由 `blur(20px)` 归一） |

`z-index / radius / 尺寸 / 阴影` **一字不动**。浅色档：`#fff → rgba(247,247,247,0.88)` —— 与基准**同款**。

## 31.3 ★★ 静态普查：全站下拉家族**已经是统一的**

`audit-menu2.py` 做**浅/暗双档矩阵**（识别 `html[giencoder-theme='dark']` 前缀）：

```
全站 10 页下拉项 hover 100% = --color-fill-2（= 基准 .perm-menu-item）· 硬编码 0 条
```

三类「例外」均合理：`.giencoder-menu-item:hover = fill-1`（**DOM 实例 0**，死规则）、
`.dropdown-item-disabled:hover = transparent`、`.is-danger = --color-danger-light-1`。

真机双档复验：暗色 6 个下拉全部 `rgba(31,31,31,.88)` + `blur(10px) saturate(1)`；
浅色全部 `rgba(247,247,247,.88)`。settings 页下拉：浅 `rgb(242,242,242)` → 暗 `rgb(43,43,43)` ✅。

## 31.4 ★ 方法论：`__hovered()` —— 问浏览器**谁真正在 hover**

原判据 `elementFromPoint` / 面积法**都不可靠**：浮层背景是铺满面板的 SVG，元素查询会返回它；
改用面积法后，浮层与下层控件矩形重叠时会选中面积更小的下层 ⇒ 假失败。

**正解**：`e.matches(':hover')` —— 直接问浏览器 z-order 最顶层是谁。
修正后 settings 页正确读出 `242 → 43`。

---

# 三十二、第十拍 —— 暗色描边降一级 + `ZCode` 归一

## 32.1 ① 邵先生：「暗色下 `--color-border-2` 看着太亮，浅色下却很合适」

**根因（量化）**：DS 的暗色档把 `border-1/2/3` 声明成与浅色档**同一级灰度索引**
（border-1 = gray-2、border-2 = gray-3、border-3 = gray-4）。但暗色档的灰度阶梯是浅色档的
**镜像**（`N ↔ 11−N`）⇒ 同一索引在暗色下落在阶梯的**亮端**：

| 令牌 | 浅（底 #fff=255） | 暗旧（底 #17171a=23） | 暗新 |
|---|---|---|---|
| border-1 | 242 · Δ13 | 43 · **Δ20** | **31** · Δ8 |
| border-2 | 229 · Δ26 | 78 · **Δ55** | **43** · Δ20 |
| border-3 | 201 · Δ54 | 107 · **Δ84** | **78** · Δ55 |

暗色 Δ 系统性比浅色大 2~3 倍 ⇒ 观感「太亮、不搭调」。

**裁决（AskUserQuestion）**：「border-1/2/3 各降一级（推荐）」⇒ 暗色 31 / 43 / 78。

**`ev/theme/apply-border.py`（链尾第 10 层之一）** —— ★ **非侵入**：
不改写 DS 编译包，只追加 `<style id="r109-border-css">` 覆盖块（与 `r109-theme-css` /
`r109-dark-css` / `r109-tw-css` 同一架构）；选择器与 DS 暗色块**逐字相同**、位置更靠后 ⇒ 覆盖必然生效。
**只动 border-1/2/3** —— `--color-border-4` 与 `--color-border`（无后缀）全站 `var()` 引用量 **= 0**
（死令牌），按红线不动。

真机双档复验（`raw/bd10/`，base / conversation / settings / kanban 四页）：

```
浅  border-1/2/3 = rgb(242,242,242) / rgb(229,229,229) / rgb(201,201,201)   ← 逐位不变 ✅
暗  border-1/2/3 = rgb(31,31,31)    / rgb(43,43,43)    / rgb(78,78,78)      ← 正是裁决值 ✅
```

## 32.2 ② 邵先生：「查找全站是否有『ZCode 』文案，若有统一替换为『GienCoder』」

`probe-zcode.py` 全仓普查（排除 node_modules / .git / .workbuddy / mg-work）：
**仅 6 处，全部在 `pages/conversation.html`，且全部在注释里** ⇒ 页面**无任何可见 ZCode 文案**。
含 2 处上游出处 `zai-org/ZCode`（Apache-2.0）。

**裁决**：「全部替换为 GienCoder」⇒ `ev/theme/apply-zcode.py`（链尾最后一层）。
⚠ 与别的层相反：本层**故意改写注释区**（目标就在注释里），因此**不启用**注释护栏。

## 32.3 ★★★ 本拍最大的坑：`apply109.py` 会把 conversation.html **整页重建**

`apply109.py` 是 `make109.py` 的**生成物**，其 skip 判据是**整页 `old == new`**；
而 conversation.html 的底色载荷是**第一拍生成的**，第 4~9 层所有的 `data-gi-dark` / r93 令牌化 /
`r109-*-css` 块都在它**之后**才叠上去 ⇒ **判据永不成立** ⇒ 每次跑都把 conversation **整页回滚**
到第一拍形态（实测 `-702` 字符：`--r93-line` 从 `rgb(var(--gray-2))` 退回 `#EBEBED`、
`data-gi-dark="1"` 被摘掉，共 **21 段**）。

**好消息 = 整链是「下一个人自我修复」的**：第 4/5/6 层重建令牌化、第 8 层重挂面板、
第 10 层重挂 border 块与 ZCode ⇒ **两轮整链 md5 完全一致**（收敛/自愈已验证）。

**坏消息（真踩过）**：中途停在 apply109 之后 = **页面处于损坏态**。
⇒ **红线：改完之后必须把整链（第 1~10 层）跑到尾**，不能单跑某一层就收工。

## 32.4 ★ 新踩的坑：块「逐字节比对」与 CRLF

`apply-border.py` 首版用 `m.group(0) == BLOCK` 判「已是目标态」。本块以 `\n` 写入，
但**其它层重写页面时用 `newline=None` 落盘会把 `\n` 翻成 `\r\n`** ⇒ 逐字节比永远「有差异」⇒
本层反复刷新，并连带触发第 8 层重挂 ⇒ **整链抖动**。

**修法**：比较一律**先规范化换行**（`\r\n → \n` 后比），即与工程「字符口径」一致 ⇒ 根治。
（`probe-blockdiff.py` 取证：修前 5 页 CRLF=21，修后 10 页逐字节一致。）

## 32.5 门禁（第十拍定稿后复跑）

| 项目 | 结果 |
|---|---|
| `check-syntax.py pages/*.html` | **10/10 通过** |
| `verify-design.py ./pages` | **74 个问题 / 0 critical**（与上轮 75 持平，**无新增**） |
| `apply-theme/dark/tokens/literals/popup` 幂等复跑 | **全部 0 变更** |
| `apply-border.py` 幂等复跑 | **新注入 0 / 刷新 0 / 已是目标态 10 页** |
| `apply-zcode.py` 幂等复跑 | **替换 0 处** |
| 第 4~10 层连跑前后 md5 | **差异 0 行** |

★ `verify-design.py` 会覆写 `pages/gaps.log`（**已跟踪文件**）⇒ 跑完必须
`git checkout -- pages/gaps.log` 复原。


---

## 33. 第十一拍 —— 邵先生三条（下拉浅色档改白 · 设置页去波点 · LOGO 改白〔撤销〕）

**日期**：2026-10-02 · **🚫 未提交 / 未 push** · **同代就地返工**（改 `ev/theme/*.py`，未建 r110）

### 33.1 原话与裁决

> **①「全站所有的下拉菜单的容器背景色在浅色模式下都应该是白色，重要；② 把暗色模式下 base.html 页面的 LOGO 的黑灰部分改成白色，浅色模式下的不要变；③ 去掉设置页面的波点背景效果。」**

| # | 指令 | 裁决 | 落地 |
|---|---|---|---|
| 1 | 下拉浅色档 → 白 | — | ✅ `ev/theme/apply-menuwhite.py`（第 11 层） |
| 2 | LOGO 暗色改白 | **「那就算了」** | ❌ **撤销，不动** |
| — | 技能面板暗色 0.9 vs 基准 0.88 | **「统一到 0.88 基准」** | ✅ 并入第 11 层 step1b |
| 3 | 去掉设置页波点 | — | ✅ `ev/theme/apply-dots.py`（第 12 层） |

### 33.2 #1 下拉菜单浅色档 = 白（`apply-menuwhite.py`）

**改动量（真机取证驱动）**：

| 步骤 | 内容 | 处数 |
|---|---|---|
| step1 | `rgba(var(--gray-1),0.88)` → `var(--color-bg-1)`（**四种写法变体**） | **28**（10+10+2+6） |
| step1b | 既有暗色覆盖 `0.9 → 0.88` | **20**（10+10） |
| step2 | 10 页注入 `<style id="r109-menuwhite-css">` 压回暗色档 | **10 页** |

**四种写法变体**（缺一不可）：① `background:rgba(var(--gray-1),0.88)`（紧凑，`.giencoder-select-popup`）② `background:rgba(var(--gray-1), 0.88)`（`.skills-popup-bg`）③ `background: rgba(var(--gray-1), 0.88)`（`.td-skill-pop` 内联）④ `` background:`rgba(var(--gray-1), 0.88)` ``（JS 模板串）。

**真机浅色档取证**（`raw/dd9-light/panel-{0..5}.json`，base 页 6 类下拉）：

| 面板 | 容器 | 浅色底 |
|---|---|---|
| panel-0 添加菜单 | `[role=menu]` | **`rgb(255,255,255)`** ✅ |
| panel-1 技能面板 | `[role=listbox].giencoder-select` | **`rgb(255,255,255)`** ✅ |
| panel-2 标准模式 | `.giencoder-select-popup` | **`rgb(255,255,255)`** ✅ |
| panel-3 大模型 | `.giencoder-select-popup` | **`rgb(255,255,255)`** ✅ |
| panel-4 工作目录 | `.giencoder-select-popup` | **`rgb(255,255,255)`** ✅ |
| panel-5 默认权限（基准） | `[role=listbox]` | **`rgb(255,255,255)`** ✅ |

**真机暗色档取证**（`raw/dd9-dark/panel-{0..5}.json`，**补齐覆盖缺口后**）：

| 面板 | 容器 | 暗色底（初版） | 暗色底（补齐后） |
|---|---|---|---|
| panel-0 添加菜单 | `[role=menu]` | ~~`rgb(23,23,26)`~~ | **`rgba(31,31,31,0.88)`** ✅ |
| panel-1 技能面板 | `[role=listbox]` | ~~`rgb(23,23,26)`~~ | **`rgba(31,31,31,0.88)`** ✅ |
| panel-2/3/4 select-popup | `.giencoder-select-popup` | `rgba(31,31,31,0.88)` | **`rgba(31,31,31,0.88)`** ✅ |
| panel-5 默认权限 | `[role=listbox]` | ~~`rgb(23,23,26)`~~ | **`rgba(31,31,31,0.88)`** ✅ |

⇒ **6 类暗色档全部统一到基准** ✅（邵先生 A 指令）。

### 33.3 ★★ 覆盖缺口（落地后真机复验才发现，已补）

第 1 步把 28 处（**含基准「默认权限」自己**）改成 `var(--color-bg-1)`（暗色 = `#17171a` 不透明深黑），
但覆盖块初版只压回 `.giencoder-select-popup` / `.skills-popup-bg` / `.td-skill-pop` 三类
⇒ **「添加菜单 / 技能面板 / 默认权限」这 3 类 `role=menu` / `role=listbox` 的内联 style 面板** 停在 `rgb(23,23,26)`。

**补法**：覆盖块加 **3 条 `aria-label` 精确选择器**（内联 `style` 优先级最高 ⇒ 必须 `!important`）：
`[role=menu][aria-label=添加内容]` / `[role=listbox][aria-label=权限选择]` / `[role=listbox][aria-label=技能选择]`。

### 33.4 #3 去掉设置页波点（`apply-dots.py`）

**侦察**：波点在 `<main class="… bg-white dot-bg">`（浅 `radial-gradient(circle, rgba(107,107,107,.1) 1.5px, …)` / 暗 `rgba(201,201,201,.1)`）。
`.dot-bg` 的 CSS **定义在共享 DS 包**（10 页共用，改不得）；`bg-white dot-bg` 在 **7 页**都有、7 页 `<main>` **逐字相同** ⇒ 纯 CSS 选不出 settings。

**修法**：`settings.html` 的 `<html>` 加 `data-r109-nodots="1"` + `</head>` 前注入
`html[data-r109-nodots="1"] .dot-bg{background-image:none !important}`。

**真机双档复验**（`raw/dots11/`）：

| 页面 | 浅色档 `main.dot-bg` background-image | 暗色档 |
|---|---|---|
| **settings** | **`none`** ✅ | **`none`** ✅ |
| **base** | `radial-gradient(circle, rgba(107,107,107,0.1) 1.5px, …)` ✅ **保留** | `radial-gradient(circle, rgba(201,201,201,0.1) 1.5px, …)` ✅ **保留** |

### 33.5 ★★★ 本拍最大工程发现：整链不可循环

`apply109.py` 的净底摘除清单 = `RE_STYLE / RE_JS / RE_NAV / RE_HDR`（r100/r101 那几代），
**不含第 4~12 层注入的新块** ⇒ 从「链尾态」重跑整链时，那些新块被带进 `net`、复制到 conversation。

**实测**：

| 轮次 | `apply109` 对 conversation 的输入 → 输出 | 10 页 md5 汇总 |
|---|---|---|
| 第 1 轮 | 1073188 → 1072511（−677） | `b77ca89f…` |
| 第 2 轮 | **1073191** → **1072514**（−677） | `4468cebc…`（**不同**） |

⇒ **每轮 +3 字符/页**、10 页 md5 全变。⚠ 与第十拍日志「两轮整链一致」**不矛盾**：那是**只有 1~10 层**时成立；
**第 11 层会改写 `rgba(var(--gray-1),0.88) → var(--color-bg-1)`（即改写 apply109 重建的产物）⇒ 判据互打破 ⇒ 抖动**。

**正确工作流**：

```
cp mg-work/r109/ev/bak-r109-l10/*.html pages/   # 回到本代定稿基线
python mg-work/r109/ev/theme/apply-menuwhite.py  # 只跑增量层
python mg-work/r109/ev/theme/apply-dots.py
```

（脚本 = `ev/theme/chain-l11.sh`）**连跑三轮 md5 完全一致** `6d963968b1db8ae216c845c9f4f9916b` ✅。

**基线重建**：`ev/bak-r109-l10/`（第 10 拍定稿态；md5 汇总 `098d8f9e…`）。
⚠ **原 `ev/bak-zcode/` 已被污染**（含 `menuwhite=1`；根因是某次 `snapshot` 覆盖），已用 `bak-menuwhite/`（= 第 9 拍末 + `apply-zcode`）修正。
**定稿快照** = `ev/bak-r109-final/`（见其 `FINAL.md5`）。

### 33.6 三个实现坑（全部实测踩过并修正）

1. **step1b 产物与 step1 搜索串逐字相同 ⇒ 跨遍污染**：step1b 产出 `background: rgba(var(--gray-1), 0.88)`（两边带空格，变体③）⇒ 下一遍 step1 把它改成 `var(--color-bg-1)`（暗色 `#17171a` **纯黑**）。
   **修法** = step1b 产物刻意用「**冒号后有空格、逗号后无空格**」（`rgba(var(--gray-1),0.88)`）—— step1 三种变体都匹配不到 ⇒ 跨遍幂等。
2. **阶段顺序决定幂等**：必须 **阶段 1 = step1 → 阶段 2 = step1b**（终点阶段放最后），颠倒则暗色覆盖被改成深黑。
3. **`snapshot()` 覆盖干净快照**：第 2/3 遍重跑又拍一次，把含改动的页面盖了干净基线 ⇒ `--revert` 失效。
   **修法** = `snapshot(force=False)` 已存在则拒绝覆盖 + `undo-menuwhite.py` 逆运算器（RESTORE 表全部**带选择器上下文**的唯一串）。

### 33.7 门禁（第十一拍定稿后）

| 项目 | 结果 |
|---|---|
| `check-syntax.py pages/*.html` | **10/10 通过** |
| `verify-design.py ./pages` | **74 个问题 / 0 critical**（与第十拍一致，**无新增**） |
| 第 11/12 层连跑三轮 md5 | **完全一致** `6d963968b1db8ae216c845c9f4f9916b` |

★ 跑完必须 `git checkout -- pages/gaps.log` 复原。

---

## 第三十四节 · r109 第十二拍（邵先生四条）

**声明**：`四条无歧义，未动用 AskUserQuestion。`

### 逐条验收（真机 1440×900 · `raw/l12/`）

| # | 需求原文 | 判据 | 实测 | 结论 |
|---|---|---|---|---|
| ① | 标题栏 `.r93-bar` 背景色应该是白色的 | `.r93-bar` computed `background-color` + `backdrop-filter`（双档） | 浅 `rgb(255, 255, 255)` / 暗 `rgb(23, 23, 26)`（= `--color-bg-1`）；`backdrop-filter: none`；`h:44` 不变 | ✅ |
| ② | `.r93-att.r93-t14` 卡片是本地文件，支持点击展开右栏浏览内容 | 点 md 卡 / xlsx 卡 → 右栏预览页签状态 | `产品初版设计方案.md` ⇒ `browseOn:true`、`paneHidden:false`、`tabName=产品初版设计方案.md`、`kind=md`、`meta=Markdown · 12 KB · 只读预览`；`vscode-light-modern-color-system.xlsx` ⇒ `kind=xlsx`、`meta=表格 · 34 KB · 只读预览`。**同一枚页签复用**（未新增标签） | ✅ |
| ③ | `.r93-card--ctx` 内间距 16px | computed `padding` / `padding-top` | `16px` / `16px`；`min-height:150px`、`max-height:240px` 一字未动 | ✅ |
| ④ | `.zd-sec-h` 支持整行点击展开和折叠 | 点**行右侧死区**（`elementFromPoint` 命中 `.zd-sec-h`） | 3 个分区（`git`/`goal`/`todo`）全 `before:false → after:true`（折叠成功） | ✅ |
| ④b | 同上（去重判据） | 点标题按钮 `.zd-sec-t` 两次 | `true → false → true` —— **单次 toggle**，未被行那一份重复处理而抵消 | ✅ |

### 静态量测
- `.r93-att` ×3：`role=button`、`tabindex=0`、`cursor=pointer`、`h=40`（宽度 167 / 195 / 308）。
- `.zd-sec-h` cursor：`auto → pointer`（改前 / 改后）。
- 分区死区：`git` 234px、`goal` 256px、`todo` 256px（`rowW=302`）。

### 门禁
- `check-syntax.py pages/*.html` → **10/10 通过**。
- `verify-design.py ./pages` → **74 个问题 / 0 critical**（与 r109 第十一拍基线**一字不差**）；已 `git checkout -- pages/gaps.log`。
- `apply12.py` 连跑三遍：`8 / 0 / 0` 处替换，md5 恒为 `5d73f37fed10bbe4f018b2c6cc023e32`（conversation.html）。
- 快照：`ev/bak-r109-l13/`（含 `FINAL.md5`）。

### 未提交
**不 commit / 不 push**（仍属 r109 未交付期，同代就地返工）。

---

## 第三十五节 · r109 第十三拍（邵先生三条 · 2026-10-02）

**需求原话**：① `zd-host` 要在骨架屏加载完成后、和对话内容主体一起显示，不要提前显示；② `r93-card r93-card--edge` 这类卡片去掉前面的缩进；③ 写入记忆和铁律：聚焦任务主线，不过度发散。

**落地**（第 13 层 `ev/theme/apply12.py`，源 `make12.py`；EDIT 数 8 → 11）：

| # | EDIT | 内容 |
|---|---|---|
| ⑤ | `card-flush` | `.r93-card`：`width: calc(100% - 18px); margin-left: 18px` → `width: 100%; margin-left: 0` |
| ⑥ | `card-full` | `.r93-card--full` 规则降为注释（与 `.r93-card` 同值，选择器保留） |
| ① | `zdhost-ready` | 新增 `html[data-r93-app='ready'] .zd-host { display: flex; }`；先手叠成 `html:has(.r93-sk):has(.r93-sk) .zd-host { display: none; }` |

**真机取证**：
- 时序（`raw/l13/seq3.json`）：`+120~+420ms` = `sk:true / disp:none`（骨架屏期隐藏 ✅）；`+500ms` = `sk:false / disp:flex`（骨架屏移出 DOM 即显形 ✅）。
- 缩进（`raw/l13/static3-light.json`）：12 张 `.r93-card` 全 `margin-left: 0px` / `relX: 0`；`.r93-card--edge` = `w:860 / ml:0` ✅。
- 浅/暗双档量测均通过（`static3-light.json` / `static-dark.json`）。

**关键教训（PLAYBOOK P3.63）**：
1. 先手（隐藏）与后手（显示）**同特指度时后者无条件胜** ⇒ 先手必须显式提特指度，不能靠源码顺序。
2. 记忆断言「`.r93-card` 第三拍已改满宽」**与磁盘矛盾**（磁盘仍是 18px 缩进，第三拍只落了 `.r93-todocard`）⇒ 动手前先验磁盘。
3. `makeNNN.py` 注释中裸单引号提前闭合字符串（报错落在下一行）；脚本重写多行变量块须显式补 `\n`。

**门禁**：`check-syntax.py` **10/10**；`verify-design.py` **74 / 0 critical**（与基线一字不差）；`gaps.log` 已还原。
**幂等**：`apply12.py` 连跑三遍 = **3 / 0 / 0** 处替换；`conversation.html` md5 恒 **`2a7a7031be7883766093c17d1e53d8e9`**。
**影响面**：仅 `pages/conversation.html`（其余 9 页 md5 与上一拍逐字节一致）。
**快照**：`ev/bak-r109-l14/`（含 `FINAL.md5`）。
**铁律**：`PLAYBOOK.md` 新增「★ 项目铁律（standing rules）」区块，**#4 = 聚焦任务主线，不过度发散**。

**未提交 / 未 push。**

## 第三十六节 · r109 第十五拍（邵先生四条 · 2026-10-02）

**邵先生原话（逐字）**：

> 1、按照你倾向的路径恢复；
> 2、这个容器“r93-todocard”也要去掉缩进。
> 3、“任务产物”里的卡片文件也要支持点击后展开右栏浏览；
> 4、不同的文件在右栏浏览时，要分别打开独立的页签，不要都在一个页签里浏览。

### 36.1 ① 恢复右栏批注模块 —— 「又被弄没了」的**真相时间线**

**症状**：第十~十三拍精心调过的批注模块（`.td-elnote` 三稿 + 原点对齐 + 拖动 + Ctrl 快捷）在页面上消失，退回旧版（`.td-elnote-t`/`.td-elnote-f` 那一套）。

**定位**：比对 `ev/bak-l1/panel.js.before`（len 72191）与 `part109/panel.js`（权威源，88077）⇒ **权威源完好无损**。页面 21:09→21:26 之间文件体积 **-45KB**，即期间发生过一次 **`apply109.py` 整页重建**（把注入过的 `panel.js` 换回旧版快照）。

**方法论结论（已进 PLAYBOOK）**：`apply109.py` 是「整页重建」性质 ⇒ 任何后续注入层（`panel.js` / `part109/panel.css` 覆盖块）都可能被它冲掉 ⇒ **改完必须把整链跑到尾**，中途停 = 页面损坏态。

**恢复路径（用户选「按照你倾向的路径恢复」）**：不重跑整链（重跑会连带其他 9 页一起动，违反「不影响其他模块」），改用 **第 16 层增量补丁** `ev/theme/apply14.py`，只对 `pages/conversation.html` 补齐 5 段（`note-js` / `note-css` / `note-bar` / `blank-css` / `blank-html`）。
- `note-js`：旧 2394 字符 → 新 16123 字符（= `part109/panel.js` 抽段逐字搬）。
- `note-css`：旧 1305 字符 → 新 6797 字符（= `part109/panel.css` 的 31017..37955 段，len 6938）。

**真机取证（`raw/l15/annot*.json`）**：

| 项 | 值 | 判读 |
|---|---|---|
| 新版结构齐否 | `pin/card/input/hint/acts/okBtn/cancelBtn` 全 `true` | ✅ |
| 旧版残留 | `oldTitle` / `oldFoot` 全 `false` | ✅ |
| 点「标注」 | `is-annotating:true`，文案 → 「退出批注」 | ✅ |
| 提交后 | **`stillAnnotating:true`**（不退出批注态，锚点常驻） | ✅ |
| 锚点属性 | `role=button` / `tabindex=0` / `title=点击查看批注 · 拖动可挪位置` / `cursor:grab` | ✅ |
| 点已有锚点 | 进编辑态，`okText:“保存”` + 原文回填 | ✅ |
| Ctrl 按住 | `cardCtrl:true`，按钮仍保持「保存」（不误触「新增」） | ✅ |
| **l3 原点对齐** | **`clickContentX:30` / `noteLeftPx:30`** | ★★ **气泡左边缘 = 点击点，逐像素 ✅** |

### 36.2 ② `.r93-todocard` 去缩进

改前 / 改后（只动这两处，其余几何一字未动）：

```
.r93-todocard { position: relative; width: calc(100% - 18px); margin-left: 18px; box-sizing: border-box; ... }
.r93-todocard { position: relative;                                                       box-sizing: border-box; ... }
```

真机（浅/暗同值）：`w:860 / pw:860 / ml:0px / mr:0px / relX:0` ✅

### 36.3 ③ 「任务产物」卡片整卡可点

原委托锚点只认卡内的 `.td-diff-btn`（「预览」按钮）⇒ 点卡片空白处无反应。
改为 document 委托 `closest('[data-td-art]')` ⇒ **整张卡任意位置可点**，行为与点「预览」一致。
真机：点 A（右栏复刻方案.md）与点 B（sidepanel-metrics.xlsx）均触发右栏浏览 ✅

### 36.4 ④ 不同文件 ⇒ 独立页签

**根因**：`openTab(mod)` 用 `mod` 当唯一键，`activate(mod)` 也只认 `mod` ⇒ 所有文件共用一个 `preview` 页签。

**改法（页签 id 升为二元组 `(mod, file)`）**：

| # | 名称 | 改动 |
|---|---|---|
| ⑦ | `tab-open` | `openTab(mod, opts)` 新增 `opts.file`；已存在判据 = `[data-td-mod=m][data-td-file=f]`，无 file 时回落到 `:not([data-td-file])` |
| ⑧ | `tab-act` | `activate(mod, file)`；`file` 非空时 `on` 追加 `data-td-file` 相等判定 |
| ⑨ | `tab-fileattr` | 建页签时若 `file` 非空则 `t.setAttribute('data-td-file', file)` |
| ⑩ | `tab-bind` | click / keydown 两处 `activate(tab.getAttribute('data-td-mod'))` → `tabActivate(tab)` |
| ⑪ | `tab-activate` | 新增 `tabActivate(tab)` = 读 `data-td-mod` + `data-td-file` 调 `activate` |
| ⑫ | `prev-show` | `prevShow` 重写：抽出 `prevFill` / `prevKindOf` / `prevFiles{}` / `prevRemember` / `prevShowFile`；`openTab('preview', {name, ico, file:name})` |

**真机取证（`raw/l15/light.json` / `dark.json`）**：

- `tabsBefore`：仅 1 枚 `summary`。
- 点 A 后 `tabsAfterA`：新增 `preview + file="右栏复刻方案.md"`。
- 点 B 后 `tabsAfterB`：**再多一枚** `preview + file="sidepanel-metrics.xlsx"`（两枚并存 ✅）。
- `paneAfterA` / `paneAfterB` / `paneBackToA`：点回 A 页签 ⇒ 面板内容切回 A，且**仅 A 那枚激活** ✅（`tabsEl` click 委托 + `data-td-file` 回填 `prevShowFile`）。

### 36.5 幂等 / 门禁 / 影响面 / 快照

- **幂等**：`ev/theme/apply14.py`（10096 chars / 12 条 EDIT）连跑三遍 = **12 / 0 / 0**；`pages/conversation.html` md5 恒 **`e27eb0050591f0807477dced59f7e534`**。
- **门禁**：`check-syntax.py pages/*.html` = **10/10**；`verify-design.py ./pages` = **74 问题 / 0 critical**（与基线一字不差）；`git checkout -- pages/gaps.log` 已还原。
- **影响面**：仅 `pages/conversation.html`；其余 9 页与 `ev/bak-r109-l14/` 逐字节一致（md5 SAME）。
- **快照**：`ev/bak-r109-l15/`（含 `FINAL.md5`）；回滚点 `ev/bak-l15pre/conversation.html.before`（1152668 bytes / `2a7a7031be7883766093c17d1e53d8e9`）。
- **链序**：`make109 → splice109 → apply109 → apply-theme → apply-dark → apply-tokens → apply-literals → apply-popup → apply-border → apply-zcode → apply-menuwhite → apply-dots → apply12 → **apply14**`（现 14 层）。

### 36.6 本拍新增红线

- **P3.64**：右栏 / 浮层改动后，锚点中心与点击点数字对不上 ⇒ **先查有没有边界夹取**（`anchorPlace()` 把锚点夹进 `.td-view` 可视区：点击点距内容原点 30px、锚点宽 24 ⇒ `maxL = 0 + clientWidth - 24 ≈ 18`）。**不是 bug**。

**未提交 / 未 push。**
