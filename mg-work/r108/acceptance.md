# r108 验收 · 会话详情页右栏「diff 卡片化 + 文件树抽屉」

> 需求（邵先生 2026-10-01 19:3x，逐字）：
> ① 「`td-diff` 要独立成一个个的小卡片」；
> ② 「需要在『在文件树中定位』按钮的右边再加一个『文件树』的图标按钮，点击后会在右侧弹出一个文件树的抽屉」。
>
> ★ 沿用长期硬约束：**绝对不得改动其他不必涉及的模块**；**完全确保整体产品的稳定性不被破坏**；**只落地静态交互**。
> ★ 本代**是新一代**（r107 十一拍已于 14:2x 交付并推送 `e9c9498`，工作区已干净）⇒ 按硬规则「已交付才新建 rNN+1」
>   开 `mg-work/r108/`，**不再就地返工 `apply107.py`**。

---

## 零、产物与口径（★ 三种口径勿混用）

| 项 | 读数 |
|---|---|
| 前置 | r107 十一拍 → **`e9c9498`**（已推送；`HEAD == origin/main == 9c09afa`，工作区干净） |
| 本代补丁 | **新建** `mg-work/r108/apply108.py`（3628 行 / 189273 字符）—— 由 `ev/make108.py` 从 `apply107.py` 做 **7 处精确替换**生成，每处命中数断言 |
| 资产 | `part108/{_mods.html 52848 / panel.css 66952 / panel.js 62447 / browse.html 88405}`（`browse.html` 由 `ev/splice108.py` 拼出；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 沿用 part107 / part105 ⇒ **不在 part108 存第二份**） |
| `pages/conversation.html` | **958568 → 978614 Unicode 字符（+20046）**；UTF-8 字节（LF 归一）1056903 → **1078406**；工作区字节（CRLF）**1086146**；行 7741 |
| **其余 9 页** | **`base.html`（472150，逐字节不变）+ 8 个外壳页 —— 一页都没动**（`git status` 里只有 `conversation.html` 一个 ` M`） |
| 幂等 | ✓ `patch108l1.py` 第二遍「应用 0 / 跳过 6」；`apply108.py` 第二遍「已是目标态（无改动）」 |
| JS/CSS 语法 | `python mg-work/check-syntax.py pages/*.html` ⇒ **10/10 通过**（conversation `script=9 style=16`，与 r107 一致） |
| 设计回归 | `python verify-design.py ./pages` 与 `mg-work/r107/ev/vd-r107l2.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增、一处渐变都没引** |
| 字号压平 | `python mg-work/r108/ev/scan-flatten.py mg-work/r108/part108/panel.css` ⇒ **2 条**（= 基线 `.td-mod-bar` / `.td-url`，与 r107 同） |
| 代数核对 | conversation 的 `r108-conv-css` / `r108-conv-js` 各 **1**；`r107-*` / `r106-conv-*` / `r102-*` / `r101-*` / `r93-*` **全 0**；**base 的 nav 块仍是 `r106-nav-js`（本代刻意不换名）** |

> ⚠ 工作区字节 − blob 字节 = 「行数」个字节 = `core.autocrlf=true` 的行尾差，**不是内容改动**。
> ⚠ 本页字符数**必须**先归一化行尾再比。

---

## 一、★ 本代体位：`GENS` 扩到六代，nav 继续沿用 `r106-nav-js`

```python
GENS = (('r93',…), ('r101',…), ('r102',…),
        ('r106', 'r106-conv-css', 'r106-conv-js', 'r106-nav-js'),
        ('r107', 'r107-conv-css', 'r107-conv-js', 'r106-nav-js'),
        ('r108', 'r108-conv-css', 'r108-conv-js', 'r106-nav-js'))   # ← 沿用
NAV_TAG = 'r106'      # build_nav_js / 残留自检都用它
```

★ **CSS / JS 两块必须换名成 `r108-conv-*`**（本代两块都改了；不换名的话「摘块」正则会连本代自己的新内容一起摘掉），
但 **nav 块一字未改 ⇒ 按硬规则「跨代沿用的宿主标记不换名」继续用 `r106-nav-js`** ——
收益：`base.html` + 8 个外壳页**逐字节不变**，本代仍只有 `conversation.html` 一页进 `git diff`。

```
   base.html            已是目标态（无改动）
   conversation.html    958568 → 978614 (+20046)  应用
```

★ `PART_DIRS` 也扩成三级回落：`part108` → `r107/part107` → `r102/part105`（本代只覆盖改过的三件）。

---

## 二、落地 ① `.td-diff` 独立成小卡片

**改前**：`.td-rv-body { padding: 4px 0 16px }` + `.td-diff { border-bottom: 1px solid --color-border-1 }`
⇒ 四张 diff 首尾相接、只靠一条 1px 线分隔，视觉上是「一整块长列表」。

**改后**（`panel.css` 第 18.1 节）：

```css
.td-rv-body { display: flex; flex-direction: column; gap: 8px; padding: 8px; }
.td-diff {
  border: 1px solid var(--color-border-2);
  border-radius: 8px;
  background: var(--color-bg-2);
  overflow: hidden;
}
.td-diff-rows { border-top: 1px solid var(--color-border-1); }
```

- ★ `overflow: hidden` 是**必需的**：`.td-diff-h:hover { background: --color-fill-1 }` 是既有规则，色块铺满整行，
  不裁的话四个圆角处会露出直角。代价 = `.td-diff-toggle:focus-visible` 的 `outline`（offset 2px）被裁掉一点（可接受）。
- ★ 头 / 体之间补 `border-top`：折叠态 `.td-diff-rows` 本就是 `display:none`（第 3 节那条），
  而统一 / 并排两个 `-rows` 同刻**必然只有一个可见** ⇒ **不会出现双线**（见第五节实测）。
- ⚠ 两条都是**同特异性、本块文档序在后** ⇒ 不用 `!important`。

**真机实测（1440，`mg-work/r108/ev/m-raw.log` → `phase:"diff"`）**：

| 读数 | 值 |
|---|---|
| `.td-rv-body` | `display:flex` / `gap:8px` / `padding:8px` |
| 四张卡 rect | `[800,142,623,299]` `[800,449,623,213]` `[800,670,623,40]` `[800,718,623,40]` |
| **卡间距** | **`[8, 8, 8]`**（142+299+8=449 → 449+213+8=670 → 670+40+8=718，逐段吻合） |
| 卡描边 / 圆角 / 底 / overflow | `1px solid rgb(229,229,229)` / `8px` / `rgb(255,255,255)` / `hidden` |
| 头/体分隔线 | `1px rgb(242,242,242)`（= `--color-border-1`） |

---

## 三、落地 ② 文件树抽屉

### 3.1 按钮

在审查工具条 `.td-mod-bar-acts` 里、**「在文件树中定位」（`[data-td-rv-act="reveal"]`）右紧邻**插一枚：

```html
<button class="td-browse-ico" type="button" aria-label="文件树" title="文件树"
        aria-haspopup="dialog" aria-expanded="false" data-td-rv-act="tree">
  <svg …folder-tree（24 网格 / 渲染 16px / stroke-width 2）…></svg></button>
```

实测工具条右端顺序 = 复制 · **定位** · **文件树** · `⋯` · 提交⌄ · PR（见 `raw/m-1440-rvbar.png`）。

### 3.2 抽屉

`_mods.html` 末尾（`</aside>` 之前）追加一层 `.td-tree`：

```html
<div class="td-tree" data-td-tree="1" role="dialog" aria-modal="true" aria-label="文件树" hidden>
  <div class="td-tree-scrim" data-td-tree-x="1"></div>
  <div class="td-tree-panel">
    <div class="td-tree-h"><span class="td-tree-t">文件树</span>…关闭…</div>
    <div class="td-tree-body">…搜索框… <div class="td-tree-files" role="tree">…10 行…</div></div>
  </div>
</div>
```

CSS（`panel.css` 第 18.2 节）要点：

- `.td-tree { position:absolute; inset:0; z-index:35 }` —— 包含块 = `.td-browse`（r107 第七拍已补 `position:relative`）。
  **z-index 35 刻意夹在「右栏下拉菜单 30」与「提交模态 40」之间**，Esc 裁决链的顺序与此同序。
- `.td-tree-panel { width: min(296px, 86%) }` —— 与「文件」模块的树 `--td-browse-tree-w: 296px` **同宽**。
- 开合 = `hidden` 属性 + `.is-open` 类**两条一起用**：`hidden` 管「不在渲染树 / 不吃点击」，
  `.is-open` 管过渡目标态；JS 里 `removeAttribute('hidden')` → **`void el.offsetWidth` 强制 reflow** → `classList.add('is-open')`。
- 关闭 = 摘 `is-open` → **等 240ms（过渡 220ms）再挂 `hidden`**，否则关闭动作是「瞬间消失」。

**真机实测（1440）**：

| 场景 | 读数 |
|---|---|
| 打开前 | `hidden=true` / `is-open=false` / `btnAria="false"` / `panelBox` 全 0 |
| 点按钮（同一次 eval 内） | `btnAria="true"` |
| 打开后（+400ms） | `hidden=false` / `is-open=true` / **`panelBox=[1135,49,296,842]`** / `transform:none` / `scrim opacity 1` |
| 与右栏的关系 | `paneBox=[791,48,641,844]` ⇒ 面板右缘 **1135+296 = 1431 = 791+641−1** ⇒ **紧贴右栏右缘** |
| 点遮罩（+400ms） | `hidden=true` / `panelBox` 全 0 / `paneOpen=true`（**侧栏没被误关**） |
| 重新打开 | `panelBox` **仍是 `[1135,49,296,842]`**（无残留污染） |
| **Esc** | `hidden=true` / `paneOpen=true` / `paneHidden=false` ⇒ **只关抽屉、不关侧栏** ✓ |

### 3.3 抽屉里的树：★★ 独立类名 `td-tf*`（本拍最关键的技术决定）

抽屉树的**内容从 part105 的原树按白名单提取**（`patch108l1.py` 的 `extract_tree_rows()`，10 行：
`.giencoder-x` / memory / games / snake-game / dist / public / src / Controls.tsx / useSnakeGame... / package.json），
**零手抄**；随后把 `td-bf*` → `td-tf*`、去掉引导线。

**为什么必须换名**：`ctrl-conv.js` 里

```js
var pane = slot.querySelector('.td-browse');     // ← 整个 aside
var rows  = pane.querySelectorAll('.td-bf');      // ← 会连抽屉里的行一起抓
var files = pane.querySelector('.td-browse-files'); // ← 只绑**第一个** ⇒ 抽屉里的行点了没反应
```

⇒ 复用同名类会让两边**互相打架**（`refresh()` / `selectFile()` 抢同一批行）。

**实测的零干扰证明**（`m2-raw.log` → `phase:"regress"`）：

| 操作 | 「文件」模块那棵树 | 抽屉树 |
|---|---|---|
| 在抽屉里点 `Controls.tsx` | `filesActive` 仍 = `useSnakeGame...`（28 行 / 9 行 hidden **一字未变**） | `drawerActive` = **`Controls.tsx`** |

⇒ 两棵树的**选中态、折叠态完全独立** ✓。

抽屉树自己的展开 / 折叠 / 选中由 `panel.js` 新增的一小段 `treeRefresh()` / 点击委托实现（**与 ctrl-conv 同一套语义、
作用域锁在 `.td-tree-files` 内**）；`_mods.html` 里的静态 `is-hidden` 就是初始折叠态（幂等，打开时会再算一遍）。

实测：点 `games` ⇒ `visibleRows 10 → 3`（`.giencoder-x` / memory / games）、`closedDirs` 多出 `games`；
再点 ⇒ 回到 10。

---

## 四、途中排掉的三处坑

1. **「文件树」按钮会弹一个多余的「已执行」toast** —— `panel.js` 里那条 `[data-td-rv-act]` **通用循环**
   （`AC_TEXT` 查表 + `say(ACT_TEXT[kind] || '已执行')`）把我的新按钮也吃了（表里没有 `tree` 这一项）。
   修：`closeMenus(null)` 之后加 `if (kind === 'tree') return;`（**保留 closeMenus**，只跳过 toast）。
   复测：点「文件树」⇒ `toastShown=false`；再点「在文件树中定位」⇒ `toastText="已在「文件」标签中定位该文件"`、
   `activeTab="文件"` ⇒ **老动作没被带坏** ✓。
2. **`.td-tree-h` 被 `scan-flatten` 多报 1 条**（有 `height: calc(40px * --ui-fs-ratio)` 但体里没有 `--font-size-*` token
   ⇒ `apply88b.converge()` 会把高度压平成裸 40px、字号杠杆失效）。修：给该规则补 `font-size: var(--font-size-body-3)`。
   复测 ⇒ 回到基线 **2 条**。
3. **`splice108.py` 的守卫误报** —— 「抽屉树必须用独立类名」这条判据原本写的是裸词 `td-browse-files`，
   而 `_mods.html` 的**注释里**为了解释原因恰好提到了这个名字 ⇒ 组装时被自己的注释绊倒。
   修：判据改成**属性形式** `class="td-browse-files"`。

---

## 五、边界验证（`probe108m4/m5/m6.sh`）

| 项 | 读数 | 结论 |
|---|---|---|
| 抽屉头部几何 / 字号 | `.td-tree-h` h=**40** fs=**14px**；`.td-tree-t` 14px；`.td-tf` h=**28** fs=**13px**；panelW=**296** | 与设计一致（body-3 / body-2） |
| **并排视图** | `isSplit=true` / 统一行 `display:none` / 并排行 `display:block` + `border-top:1px`；卡 `radius 8` / `gap 8` | 卡片化在并排下同样成立 |
| **并排 + 折叠** | `is-open=false` / 卡高 **40**（只剩头部）/ `rowsDisplay:none` | **无残留分隔线** ✓ |
| **`--ui-fs = 18` 杠杆** | 树行 **28 → 36**、头部 **40 → 51**、行字号 13 → 16.71px、`--ui-fs-ratio: calc(18 / 14)` | **字号杠杆生效**（没被压平） |
| 窄档 | 视口 620 ⇒ 右栏仍 561、面板 296（`86%` 分支要右栏 < 344px 才触发） | `min()` 的 `296px` 分支正确 |

> ⚠ 探针踩的两个假失败（**不是产品问题**）：① 抽屉开着时遮罩 z-index 35 会**挡住工具条的点击** ⇒
> 想点 `⋯` 切并排必须先关抽屉（否则点到了遮罩上、抽屉被关）；② 上一版探针用
> `A || (fn)().click()` 写短路表达式 ⇒ 左侧 `querySelector` 命中（哪怕元素 hidden）就短路，**并排根本没切过去**。

---

## 六、改动清单

| 文件 | 改动 |
|---|---|
| `mg-work/r108/ev/make108.py` | **新建**：从 `apply107.py` 精确替换 7 处 → `apply108.py` |
| `mg-work/r108/apply108.py` | **生成**（3628 行）；`GENS` 六代、`NAV_TAG='r106'`、`PART_DIRS=(part108, r107/part107, r102/part105)` |
| `mg-work/r108/ev/splice108.py` | **新建**：源 part105 + `part107/_head.html` + `part108/_mods.html` → `part108/browse.html` |
| `mg-work/r108/ev/patch108l1.py` | **新建**：改三件（`_mods.html` / `panel.css` / `panel.js`），含树的**白名单提取** |
| `mg-work/r108/part108/{_mods.html,panel.css,panel.js}` | **手改**（+ 组装产物 `browse.html`） |
| `pages/conversation.html` | **唯一进 `git diff` 的页面**（`+248 / −3` 行） |

**门禁四件套**：幂等 ✓ / `check-syntax` **10/10** / `verify-design` **与上轮逐字节相同** / `scan-flatten` **2 条** /
工具污染 `pages/gaps.log` 已 `git checkout` 清理。

---

## 七、交接

- 🚫 **未 commit / 未 push** —— 等邵先生显式发话。
- ★ **r107 已封板**：若还要改**会话详情页 / 右栏**，**继续在 `mg-work/r108/` 里就地返工**（判据 = `git status` 里
  `conversation.html` 仍是 ` M`、且 `r108-*` 块已存在）；**不要**新建 r109、也**不要**回头改 `apply107.py`。
- ★ 改序（本代首次动了 `_mods.html`）：`part108/_mods.html` → `ev/splice108.py` → `apply108.py`。
  `part108/browse.html` 是**组装件**，不是手改对象。

---

# r108 · 第十三拍（六条 / **就地返工**，未另起代数）

> 需求（邵先生 2026-10-01 20:0x，逐字）：
> ① 「当卡片 `td-sum-sec` hover 时，边框的颜色会变成深一级的颜色」；
> ② 「把 `td-sum-h` 这种标题前面的图标都去掉」；
> ③ 「`td-diff-toggle` 的图标颜色浅了，需使用正文颜色，并且将图标的字号调整为 13px」；
> ④ 「产物卡片 `td-sum-art` 要整体可点击预览」；
> ⑤ 「任务详情页的 `giencoder-badge-status-text` 的字号改成 13px」；
> ⑥ 「完成上述任务后，请你调研智谱 AI 的 zcode 这个产品，我需要将其对话界面右上角的那个实时任务信息卡片的内容（Git tools、Goal、Progress 等）**完全的复刻**到 `conversation.html` 页面的右上角的同样位置」。
>
> ★ 代数体位：第十二拍**尚未提交**（判据 `git status` 里 `conversation.html` 仍是 ` M`）⇒ 按硬规则「**未交付 ⇒ 就地返工**」，
> **不另起 r109**。本轮 = 第十二拍的**第二层补丁**，叠加在 `r108/` 内。
> ★ 第 ⑤ 条落在 **`pages/task-detail.html`** —— 那是另一页、另一条血脉（r42→…→r92 建成后只被 r101/r102/r106 改过文案），
> 既不参与 `splice108` 也不参与 `apply108` ⇒ 单独脚本 `ev/patch108td.py` 直接对页面落盘。

## 八、逐条落地

### ① `.td-sum-sec` hover 边框加深一级

```css
.td-sum-sec:hover { border-color: var(--color-border-2); }
```

- 基态 `border: 1px solid var(--color-border-1)`（`rgb(242,242,242)` / gray-2）；hover 升到 `--color-border-2`（**`rgb(229,229,229)`** / gray-3）= **深一级，正好一档**。
- 挂在既有的 `.td-sum-sec` 基态规则之后、**同特异性 + 本块文档序在后** ⇒ 不用 `!important`。

**真机实测（1440）**：

| 时刻 | 读数 |
|---|---|
| 基态 | `borderTopColor: rgb(242,242,242)`；卡 rect `[804,145,615,123]` |
| 真鼠标移入 +450ms | **`rgb(229,229,229)`** / `secHover: true` / rect 不动 |

### ② 去掉 `.td-sum-h` 标题前的图标

- `part108/_mods.html` 里 4 处 `<h4 class="td-sum-h"><svg …>…</svg>标题</h4>` ⇒ 用正则把 `<svg>` 元素整段删掉（`expect=4`）。
- 同时删掉 `.td-sum-h svg` 的**死规则**（`flex:none; color: var(--color-text-3)`）。

**真机实测**：`sumHCount: 4` / **`sumHSvg: 0`** / 文字 `["摘要","计划","来源","产物"]` ✓
（目视见 `raw/n-1440-sum.png`：四个标题前全部无图标，而「产物」两条卡片的「预览」按钮仍在。）

> ⚠ 删除类改动**没有**「改完才出现」的 `mark` ⇒ 幂等判据只能改用「**模式不再命中**」（`drop_re` 的 `expect` 命中数第二遍为 0）。

### ③ `.td-diff-toggle` 图标改正文色 + 13px

```css
/* 改前 */ .td-diff-cv { flex: none; color: var(--color-text-3); transition: transform 160ms; }
/* 改后 */ .td-diff-cv { flex: none; width: 13px; height: 13px; color: var(--color-text-1); transition: transform 160ms; }
```

- `--color-text-3`（`rgb(134,134,134)`）→ **`--color-text-1`（`rgb(31,31,31)`）= 正文色**；
- 尺寸**显式写死 13px**：图标 svg 的 `width/height` 属性虽是 16，但 `.td-diff-cv` 自身没框 ⇒ 补 `width/height` 才是真正的「字号 13px」。
- ⚠ 该规则体内**不含** `line-height/height/min-height` ⇒ **不触发 `apply88b.converge()` 的压平路径**（`scan-flatten` 仍 2 条）。

**真机实测（可见几何）**：`rect [813,156,13,13]` / `color: rgb(31,31,31)` / `w: 13px` / `h: 13px`；
外层 `.td-diff-toggle` `color rgb(10,10,11)` / `display: flex`；`cardCount: 4`；
首卡 `rect [800,142,623,299] / radius 8px / border rgb(229,229,229) / bg rgb(255,255,255)`
⇒ **第十二拍的卡片化没被带坏** ✓

### ④ `.td-sum-art` 整体可点击预览

- `data-td-art="1"` 从**内部「预览」按钮**上移到**卡片本体**（`.td-sum-art`，2 处）；
- 内部按钮的 `data-td-art` 卸掉 ⇒ 视觉与键盘入口保留、但不再参与整卡点击语义；
- 新增 `.td-sum-art[data-td-art] { cursor: pointer; }`。

**真机实测**：卡上 `artHasData: true` / `artCursor: "pointer"` / `artRect [817,755,589,50]`；
卡内按钮 `artBtnHasData: false` / `artBtnRect [1356,768,42,22]`；
**点「图标区」（`.td-sum-arti`）而非「预览」按钮** ⇒ 预览层 `pvHidden: false` / `pvRect [792,93,639,798]` /
`pvName: "右栏复刻方案.md"` / `pvMeta: "Markdown · 12 KB · 只读预览"` / `pvKind: "md"` ✓（目视见 `raw/n-1440-art-pane.png`）

### ⑤ 任务详情页徽章字号 → 13px

- ★ 关键发现：`.giencoder-badge-status-text` 的文字节点**自己不声明字号**（继承父级），
  真正的字号在 `.giencoder-badge-status { font-size: var(--font-size-body-3) }`（14px）上
  ⇒ 给**本页**补一条 `…-text { font-size: var(--font-size-body-2) }`（13px）即可，**无需特异性竞争、不动 DS 源**。
- 落点：`<style id="r108-td-css">`，插在 `</style>` 与 `<script id="r81-ws-js">` 之间。
- ⚠ 该规则无 `line-height/height` ⇒ 不会触发压平。

**实测**：`pages/task-detail.html` 767428 → **767836 字符（+408）**；`<style id="r108-td-css">` 已落位；
`</style></style>` 出现 **0** 次；第二遍「跳过（已应用）」✓

### ⑥ 复刻 ZCode 右上角任务信息面板（★ 本拍最大件）

**上游调研**（权威依据 = 源码，非截图）：`zai-org/ZCode`（Apache-2.0，2026-09-24 开源，7272 stars，default branch `main`）

| 文件 | 行数 | 作用 |
|---|---|---|
| `packages/ui/src/v4/ConversationStatusPanel.tsx` | 2085 | 右上角状态面板本体 |
| `packages/ui/src/v4/conversationStatusPanelModel.ts` | 385 | 数据模型（注释明写「构造**右上角**逐轮摘要」） |
| `packages/ui/src/v4/conversationGoalSummaryModel.ts` | — | 目标迭代摘要 |
| `packages/ui/src/i18n/locales/zh-CN.ts` | 6497 | 全部文案（逐字取 `chat.statusPanel.*` / `chat.summaryPanel.*`） |

**上游体位**：容器 `pointer-events-none absolute top-0 right-4 z-20 pt-4`；卡片 `pointer-events-auto relative overflow-hidden rounded-2xl border shadow-md`；
`panel` 档 = `w-80 max-h-[min(64dvh,32rem)]`；`mini` 档 = `inline-flex max-h-8.5`；
分区头 `h-8 min-w-0 shrink-0 items-center gap-1.5 px-2 pr-8`，标题按钮里的 chevron **默认 `opacity-0`、hover/focus 才显形**（展开 ChevronDown / 收起 ChevronRight）。

**落地**（`_mods.html` 末尾 + `panel.css` 第 19 节 + `panel.js` 末段 IIFE）：

- 分区 4 个（`data-zd-sec`）：`git`「Git 工具」/ `goal`「目标」/ `plan`「计划」/ `todo`「进程」；
  逐字文案 = `Git 工具` / `更改` / `分支` / `提交 / 推送` / `目标` / `计划` / `进程` / `状态` / `收起为胶囊`。
- 内容：Git 三行（`更改 +566 −228` / `分支 main` / `提交 / 推送`）+ trailing `+566 −228`；
  目标两条迭代（`3/3` / `3/4`）+ trailing `2 分 18 秒` + 暂停钮；计划一行 `右栏复刻方案.md`；进程 `3/5` 五条待办（3 done / 1 doing / 1 todo）。
- 折叠 = 分区头点击 `classList.toggle('is-closed')`（**不写内联 display**）；面板 ⇄ 胶囊 = `hidden` 属性互斥。
- 6 枚 SVG 逐条对应上游 lucide 图标（24 网格 / `stroke-width 2` / 渲染 16px）：`FileDiff` / `GitBranchSwitcher` / `GitActionMenu` / `Goal` / `ListChecks`，另备 `ChevronDown` / `Minimize2` / 暂停。

**★ `.zd-host` 的 top 必须是 44px（不是 0）**：

```css
main { position: relative; }
.zd-host {
  position: absolute; top: 44px; right: 16px; z-index: 20;
  display: flex; justify-content: flex-end;
  box-sizing: border-box; padding-top: 12px;
  pointer-events: none;                 /* 容器不吃点击，只有卡片 auto */
  max-width: calc(100% - 32px);
}
```

`<main>` 顶部有一条 `.r93-bar`（`position:absolute; height:44px; z-index:10`，r106 定的**固定档**），
右上角那两枚「全屏 / 打开侧栏」按钮就在里面 —— 面板若从 `top:0` 起排就会**把它盖住**。

**真机实测（1440×900，右栏关闭）**：`hostInMain: true` / `mainRect [12,48,779,844]` / `hostRect [455,93,320,524]` / `hostPE: "none"` /
**`cardRect [455,105,320,512]`** / 卡片 `border rgb(229,229,229)` / `radius 8px` / `bg rgb(255,255,255)` / `maxH 512px` / `w 320px` / `pe "auto"`；
`panelRightGap: 16`、`panelTopGap: 57`（= 44 栏 + 12 间距 + 1 边框）。

| 项 | 读数 |
|---|---|
| 结构 | `secs: 4` / `secTitles: ["Git 工具","目标","计划","进程"]` |
| trailing | `secX: ["+566−228","2 分 18 秒","3/5"]` |
| 行 | `rows: ["更改 +566 −228","分支 main","提交 / 推送","右栏复刻方案.md"]` |
| 目标迭代 | `1 拆出侧栏骨架… 3/3`（绿圈）· `落地审查、终端、浏览器、摘要四个面板 3/4`（Goal 图标） |
| 待办 | `todoAll: 5 / todoDone: 3 / todoDoing: 1` |
| 初始态 | `miniHidden: true` / `secBodyDisplay: "block"` |
| 折叠「Git 工具」 | `closed: true` / `bodyDisplay: "none"` / `aria: "false"` / 卡高 **512 → 503** |
| 收胶囊 | `cardHidden: true` / `cardDisplay: "none"` / `miniHidden: false` / `miniRect [672,105,103,32]` / `miniText: "进程 3/5"` |
| 点胶囊摊回 | `cardHidden: false` / `miniHidden: true` / 卡高 503（**保留折叠状态**） |

**边界与回归**（`ev/probe108n2.sh` → `n2-raw.log`，五组全绿）：

| 组 | 读数 |
|---|---|
| **[A] 遮挡回归** | `elementFromPoint` 命中「全屏」`[1359,57,28,28]` 与「打开侧栏」`[1395,57,28,28]` 均 **`hitSelf: true`**；`zdTop: 93` ✓ |
| **[B] diff 折叠图标** | `rect [813,156,13,13]` / `rgb(31,31,31)` / `13px`；首卡 `[800,142,623,299]` / `8px` / `rgb(229,229,229)` / `#fff` |
| **[C] 暗色档** | 卡 `bg rgb(35,35,36)` / `border rgb(78,78,78)` / 名 `rgb(247,247,247)` / 分区色 `rgb(169,169,169)` / 胶囊 `rgb(35,35,36)` + `rgb(78,78,78)` / 待办 `rgb(169,169,169)` ⇒ **全部 token 派生，零硬编码色** |
| **[D] `--ui-fs = 18`** | `--ui-fs-ratio: calc(18 / 14)`；头部 **36 → 46**（fs 16.7143px）、分区头 **28 → 36**（fs 15.4286px）、行 **32**（fs 16.7143px）、卡 `[320, 512]` ⇒ **没被压平** |
| **[E] 窄档 620** | `mainR [12,48,39,844]` / `cardR [29,105,6,512]` / `overflowRight: -16` ⇒ `max-width: calc(100% - 32px)` 生效、无右溢 |

## 九、第十三拍排掉的四处坑

1. ★★ **面板遮挡了 main 顶部工具条**（探针第一次 [B]/[C] 全废）：`.zd-host` 原本 `top:0`，与 `.r93-bar` 右上角两枚按钮重叠，
   `elementFromPoint(1410,71)` 命中的是**面板自己的 `<span class="zd-acts">`** ⇒ 探针的 `click` 点到了面板、右栏始终没开、
   `.td-sum-sec` 停在 `x=1445`（视口外）⇒ hover / 点击**静默失效**。修 = `top: 44px` + `padding-top: 12px`。
   **教训**：新浮层必须先做 `elementFromPoint` 自检，且要避开既有**固定高**工具条（`--ui-fs` 杠杆对它无效）。
2. ★★ **`splice108.py` 的守卫被自己的注释绊倒**（第十二拍「注释绊倒判据」的**同型复现**）：
   `PANEL_HTML` 的说明注释里写了 `` `<aside class="td-browse">` 内只是为了… `` ⇒ `out.count('<aside')` 变成 **2** ⇒ 守卫 `!= 1` 报错。
   修：注释改成「右栏容器 `aside.td-browse` 内只是为了」（**不出现 `<aside` 这两个 token**）。
3. ★★ **`patch108td.py` 首版生成双 `</style>`**：锚点 `'</style><script id="r81-ws-js">'` 被**整体**替换 ⇒ 变了的是
   `</style>` → `BLOCK`，插入点前面本来就有的 `</style>` 与新块自己的 `</style>` 撞成 `</style></style>`
   （DOM 解析时该 CSS 会被当 HTML 文本，**真 bug**）。修：`REPLACEMENT = '</style>' + '{{BLOCK}}' + '<script id="r81-ws-js">'`，
   替换时只代换 `{{BLOCK}}` ⇒ 两个 token 各出现各一次；复测 `</style></style>` **0** 次。
4. **截图框错了目标**：④ 的预览层 `rect x = 792` 起 —— 打开右栏后 `main` 只到 `x = 791`
   ⇒ `screenshot "main"` **正好把预览层切在画面外**（拍照成功但内容缺失，比报错更隐蔽）。
   修：改截 `.td-sum-prev` / `.td-browse`。

## 十、第十三拍门禁（在 `top` 修正之后复跑一遍）

| 门禁 | 读数 |
|---|---|
| 幂等 | ✓ `patch108l2.py` 第二遍「**应用 0 / 跳过 8**」；`patch108td.py` 第二遍「跳过（已应用）」；`apply108.py` 第二遍「已是目标态（无改动）」 |
| JS/CSS 语法 | `check-syntax.py pages/*.html` ⇒ **10/10 通过**（conversation `script=9 style=16`、task-detail `script=12 style=13`） |
| 设计回归 | `verify-design.py ./pages` 与 `mg-work/r107/ev/vd-r107l2.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增** |
| 字号压平 | `scan-flatten.py mg-work/r108/part108/panel.css` ⇒ **2 条**（`.td-mod-bar` / `.td-url`，= 基线） |
| 工具污染 | `pages/gaps.log` 已 `git checkout --` 清理 |
| 代数核对 | `r108-conv-css` / `r108-conv-js` 各 **1**；`r107/r106/r102-conv-*` **全 0**；base 的 nav 块仍是 `r106-nav-js`（**没换名**） |

**产物口径**：

| 文件 | 读数 |
|---|---|
| `pages/conversation.html` | 978614 → **995133 字符（+16519）**；`git diff` **+582 / −11 行**（第十二拍 +248/−3 ⇒ 本拍净 +334/−8） |
| `pages/task-detail.html` | 767428 → **767836 字符（+408）**；`git diff` **+7 / −0 行** |
| `pages/base.html` + 8 个外壳页 | **472150，逐字节不变** |

## 十一、第十三拍改动清单

| 文件 | 改动 |
|---|---|
| `mg-work/r108/ev/patch108l2.py` | **新建**（555 行）：第 ①②③④⑥ 条，7 步 `drop_re/edit_all/tail/del_once/edit` |
| `mg-work/r108/ev/patch108td.py` | **新建**（85 行）：第 ⑤ 条，锚点 `</style><script id="r81-ws-js">`，支持 `--revert` |
| `mg-work/r108/part108/_mods.html` | 4 枚标题图标删净 / 2 处 `data-td-art` 上移到卡 / `PANEL_HTML` 追加（51798 → 59186 字符） |
| `mg-work/r108/part108/panel.css` | 第 280 / 1203 / 1206 行小改 + 末尾第 19 节 + 幂等标记 `/* r108-l2 */`（65976 字符） |
| `mg-work/r108/part108/panel.js` | 末尾追加面板控制器 IIFE（折展 / 胶囊 / 搬进 `main`）（64682 字符） |
| `mg-work/r108/ev/p108n.js` + `probe108n.sh` / `probe108n2.sh` | **新建**：多相位探针（`fix/hover0/hover1/art/zd0/zd1/zd2`）+ 边界回归 |
| `mg-work/r108/ev/shots108n.sh` / `shots108n2.sh` + `raw/n-1440-*.png`（12 张） | **新建**：目视取证 |
| `mg-work/r108/ev/doc108o.py` | **新建**：记忆同步（18 步；`patch()` 加了 `neg` **反判据**开关） |
| `mg-work/r108/ev/bak13/` | 临时备份（5 份记忆文档 + 2 份 skill 快照）—— **不入库** |
| `pages/conversation.html` / `pages/task-detail.html` | 产物（本拍唯一进 `git diff` 的两页） |

## 十二、第十三拍交接

- 🚫 **仍未 commit / 未 push** —— 等邵先生显式发话（届时 `git reset -q -- mg-work/r107/ev/bak*`；`raw/` 照旧入库）。
- ★ r108 仍是**未交付的工作代**：若还要改**会话详情页 / 右栏 / 任务详情页**，**继续在 `mg-work/r108/` 就地返工**
  （判据 = `git status` 里对应页仍是 ` M`、且 `r108-*` 块已存在）；**不要**新建 r109、**不要**回头改 `apply107.py`。
- ★ 改序仍是下→上：`part108/_mods.html` → `ev/splice108.py` → `apply108.py`；`part108/browse.html` 是组装件，不是手改对象。
- ★ 第 ⑤ 条走的是**独立血脉**（`pages/task-detail.html`），只有 `ev/patch108td.py` 一个入口，**不要**把它塞进 `apply108.py`。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*`，还要 **`git reset -q -- mg-work/r108/ev/bak13/`**
  （第十三拍的临时备份 = 5 份记忆文档 + 2 份 skill 快照，**不入库**）；`mg-work/r108/raw/` 照旧入库。
- ★ **记忆同步（第十三拍）**：`ev/doc108o.py`（18 步 + 1 步**反判据**步）三遍幂等
  （应用 18/跳过 1 → 1/18 → **0/19**）—— 更新 `.workbuddy/memory/{HANDOFF,PAGES,PLAYBOOK,MEMORY,2026-10-01}.md` + 工作区日志；
  并顺手修掉 HANDOFF 首部一处**历史遗留的重复行**（这正是「反判据」那一踩）。
- ★ **skill 反思**：新教训已回写 `compiled-bundle-jsx-patch`（+4.7KB：变短替换的反判据 / 锚点 token 回填 / 注释绊倒守卫 / 浮层避开固定高工具条）
  与 `css-state-pixel-evidence`（+3.5KB：11.5 截图目标别选布局容器 / 11.6 浮层与工具条重叠 + 坑表两行）。

---

# r108 · 第十四拍（四条 / **就地返工**，仍未另起代数）

> 邵先生四条（逐字）：
> 1、『zd-card』里的git工具的三个item（更改、分支、提交/推送）点击都无响应，需继续实现交互功能；
> 2、『zd-card』里的『计划』模块不需要，可以去掉；
> 3、『zd-card』里的『目标』的页面UI细节还原不到位，比如图标、间距等元素；
> 4、『zd-card』的折叠和展开都需要点弹性微动效。

**体位**：`HEAD == origin/main == 9c09afa`，r108 **仍未 commit** ⇒ 按硬规则「未交付期内返工就地改原补丁、不另起代数」，
本拍作为 `mg-work/r108/ev/patch108l3.py` 的第**三**层补丁叠加（l1/l2/l3 三层各带独立 `mark`，互不干扰）。

**上游依据**（本拍新增入库）：`zai-org/ZCode`（Apache-2.0）
`packages/ui/src/v4/ConversationStatusPanel.tsx`（2085 行）+ `conversationStatusPanelModel.ts`（385 行）
已落盘 `mg-work/r108/up/`；另从 `raw.githubusercontent.com` 直取 `z-GitActionMenu.tsx` / `z-GitBranchSwitcher.tsx` /
`z-collapsible.tsx` / `zcode-zh.ts` 作现场比对；图标一律取 `lucide-static@1.49.0` 原路径（`-L` 跟 302）。

---

## 十三、第十四拍逐条落地

### ① Git 工具三行接上交互（★ 本拍最大件）

| 行 | DOM | 动作 | 真机实测 |
|---|---|---|---|
| **更改** | `[data-zd-git="review"]` | **复用右栏既有链路**：`[data-td-open-mod="review"]`.click() → `openTab('review')` → `ensureOpen()`（兜底点 `.r93-baract[data-r93-browse]`） | `rev0`：`browseOn:false` / `tabs:["summary ✓"]` / `reviewHidden:true` ⇒ `rev1`：**`browseOn:true`** / `paneRect [791,48,641,844]` / **`tabs:["summary","review ✓"]`** / `reviewHidden:false` / `reviewRect [792,93,639,798]`；卡片随 main 收窄让位 `cardRect [455,105,320,512]` |
| **分支** | `[data-zd-git="branch"]`（`aria-haspopup="menu"`） | `.zd-menu-branch`（`.td-mm-cap`「分支」+ 4 条 `data-zd-br`（`main` / `feature/right-panel` / `fix/zd-card` / `release/0.9`）+ divider + `data-zd-br-new`「创建并检出新分支...」）；点条目 = radio 切换 + 行值更新 + 轻提示 | `br1`：`hidden:false` / `open:true` / `display:flex` / `visibility:visible` / `opacity:1` / `rect [1223,252,192,225]` / `pe:auto` / `bg #fff` / `border rgb(229,229,229)` / `minW 168px` / `pad 6px` / **`dy:6`**（= 触发行下缘 + 6）/ **`inView:true`** / `cap:"分支"` / `divider 1px`；条目 `pad "5px 8px"` / `radius 4px`；选中项 `color rgb(55,112,247)` + `mark opacity 1`，其余 `rgb(31,31,31)` + `opacity 0` |
| **提交或推送** | `[data-zd-git="commit"]`（文案取上游 `git.actionMenu.trigger` = **「提交或推送」**） | `.zd-menu-commit`：`data-zd-commit="commit"`「提交」`⌥⌘C` / `data-zd-commit="push"`「提交并推送」`⌥⌘P`（文案同上游 zh-CN） | `cm1`：`rect [1247,284,168,80]` / **`dy:6`** / `inView:true` / 条目 `[1254,291,154,32]` 与 `[1254,325,154,32]` / **`branchMenuHidden:true`（互斥）** |

- **选完／提交后**：`br2` ⇒ 菜单 `hidden:true`、`branchText:"feature/right-panel"`、选中项 `feature/right-panel ✓`、
  `rowAria:"false"`、轻提示 `toastText:"已切换到 feature/right-panel（视觉演示）"`；
  `cm2` ⇒ `menuHidden:true`、`toastText:"已提交并推送到 origin/main（视觉演示）"`、`rowAria:"false"`。
- **关闭三路径齐全**：外点（`document` 级「点空白收起」）/ **Esc**（`window` **捕获段**，且**只有真关掉了菜单才** `preventDefault`）/ 选完自动收起。
  `cm3` ⇒ 两菜单均 `hidden:true`，**`browseOn:false`**、**`zcardHidden:false`** ⇒ **没顺带关侧栏、也没关面板**（硬规则 23 分层）。
- **摆位**：包含块 = `.zd-host`（`position:absolute`）；`panel.js` 在打开瞬间写 `--` 自定义属性 + 行内坐标，
  垂直 = 触发行下缘 + `ZD_GAP(6)`；水平 = 右对齐卡片右缘（`left = host.clientWidth - menu.offsetWidth`，`<0` 夹到 0）。
  ⚠ 用 `offsetWidth` 而非 `getBoundingClientRect().width` —— 后者会把入场 `scale(0.96)` 乘进去（实测会偏 ~7px）。
- **轻提示**：`.zd-toast`（面板自带一份 —— 右栏收起时 `.td-browse` 那份看不见），`position:absolute; right:0; top:100%; margin-top:8px`，
  `bg var(--color-bg-popup)` / `border var(--color-border-2)` / `shadow2-down` / `body-1` 字号 / `pointer-events:none`。

### ② 「计划」分区删净

`static` ⇒ `secs:3` / `secKinds:["git","goal","todo"]` / **`planGone:true`** / `secTitles:["Git 工具","目标","进程"]`；
`_mods.html` 里 `data-zd-sec="plan"` **不再命中**、`data-zd-sec=` 计数 **3**。
（`list-checks` 图标由「进程」分区与胶囊继续复用 ⇒ 无孤儿规则。）

### ③ 「目标」分区按上游逐项校准

| 项 | 上游（ZCode tsx） | 本页实测（1440） |
|---|---|---|
| 未完成项图标 | `GoalIcon` = lucide `goal` | `icoPaths:["M12 13V2l8 4-8 4","M20.561 10.222a9 9 0 1 1-12.55-5.29","M8.002 9.997a5 5 0 1 0 8.9 2.02"]`（**3 条子路径，原路径逐字**；不再是自绘旗子）；`icoColor rgb(134,134,134)`（= `--color-text-3` ↔ 上游 `--color-foreground-subtle`）；`icoRect [1112,383,16,16]` |
| 已完成项 | `flex size-4 … rounded-full border border-success text-ui-xs` | `hasNo:true` / `noRect [1112,335,16,16]` / `border`+`color = rgb(59,179,70)`（= `--color-success-6`） |
| 迭代行 | `gap-2 rounded-lg px-2 py-2 hover:bg-hover` | `pad "8px/8px/8px/8px"` / `radius 8px` / `gap 8px` / `align flex-start` / `bg rgba(0,0,0,0)` |
| 标题 | `line-clamp-3 text-ui-base leading-4` | `titleLH:"16px"` / `titleFS:"13px"` |
| 计数 | `text-ui-sm tabular-nums foreground-subtle` | `.zd-it-c` 13px→12px 档（`--font-size-body-1`） |
| trailing | `elapsed` + `·` + `control` | `sepText:"·"` / `sepColor rgb(134,134,134)` / `secX[1]="2 分 18 秒·"` |
| 暂停钮 | `Button size="icon-sm" className="size-6"` + `PauseIcon size-3.5` | `pauseRect [1364,299,24,24]` / `pauseSvgRect` **14×14** / lucide `pause`（`14,3,5,18,rx=1` + `5,3,5,18,rx=1`） |
| 分区头 | `mb-0.5 flex h-8 … px-2 gap-1.5` | `secH.h:"32px"` / `pad "0px 8px"` / `gap 6px` / `fs 12px` |
| 折叠箭头 | `ChevronDown/Right size-3.5 opacity-0 group-hover:opacity-100` | `cv` 14×14 / `rect [1159,159,14,14]` / `opacity 0` / `transition "opacity, transform 0.14s, 0.3s"` |
| 头部「收起为胶囊」 | `Minimize2Icon size-3.5` | `minBtn.rect [1386,112,24,24]` / `svgRect` 14×14 / lucide `minimize-2`（`m14 10 7-7` / `M20 10h-6V4` / `m3 21 7-7` / `M4 14h6v6`） |
| 图标体量类 | 上游 `size-6` / `size-3.5` | **新挂 `.zd-ico`（24 / 14）** —— ❌ 不能改 `.td-browse-ico`（那是右栏工具条的 28/16，会连带动右栏） |

★ **本拍补修的一处边界缺陷**：`.zd-it-no`（绿圈序号）原写 `width:16px; height:16px`，而本规则含 `var(--font-size-*)`
⇒ `apply88b` 的 `scale_block` **只派生 `height`**、`width` 不跟 ⇒ 在 `--ui-fs` ≠ 14 时**变成椭圆**（18 档实测 16 × 20.57）。
按 `apply108.py` 头注释的约定（「带字号 token 的规则不得写裸 `height:Npx`」）两边都显式写
`calc(16px * var(--ui-fs-ratio))` ⇒ 任意字号下恒为正圆（18 档复测 **20.5625 × 20.5625**，`itNoRound:true`）。

### ④ 折展 + 面板⇄胶囊的弹性微动效

上游机制 = Radix `CollapsibleContent` 的 `grid-template-rows: 0fr ⇄ 1fr` + 透明度
（ZCode 产物里可直接读到 `.grid-rows-[0fr]` / `.grid-rows-[1fr]` / `.transition-\[grid-template-rows\]`）⇒ 本页照同一机制用**纯 CSS 过渡**表达，
缓动换成 DS 的 `--transition-timing-function-spring`（`cubic-bezier(.34, 1.56, .64, 1)`，**y1 = 1.56 ⇒ 天然过冲**）。

**A. 分区折展**（`foldStart` 装 rAF 采样器 → 点分区标题 → `foldRead`，**33 帧 / 522ms**）：

| 采样量 | 轨迹 | 结论 |
|---|---|---|
| `gridTemplateRows` | `0 → 5.45 → 18.75 → 36.25 → 54.94 → 72.66 → 87.94 → 96（终）` | 真的是 `0fr → 1fr` 连续过渡，**不再是 `display:none` 硬切** |
| 内层 `opacity` | `0 → 0.071 → 0.221 → … → 1` | 淡入 |
| 内层 `translate` | `0px -4px → … → 0px 0.39px → 0px 0.34px → 0` | **越过终点后回坐 ⇒ spring 过冲的直接证据** |
| 内层 `scale` | `0.98 → … → 1.00195 → 1.0003 → 1` | 同上过冲 |

折叠那一拍：`closed:true` / `aria:"false"` / **`bodyDisplay:"grid"`**（不再出现 `display:none`）。

**B. 面板 ⇄ 胶囊**：

- **出场**（21 帧 / 323ms）：`opacity 1 → 0.909 → 0.714 → … → 0`；`scale 1 → 0.9858 → … → 0.934162`；
  `translate 0 → 0px -1.42px → … → 0px -6.58px`（微缩 + 上浮）；约 **180ms** 处才切件
  （`cardHidden:true` / `miniHidden:false` / `miniRect [1312,105,103,32]` / `miniText:"进程 3/5"` / `miniRadius "999px"`）。
- **入场**（39 帧）：`~198ms` 处卡片摘 `hidden`（起于 `[1105,114,301,481]`），随后
  `scale 0.94 → … → 1.00123 → 1.00377 → **1.00584（峰值过冲）** → 回落 1`；
  `translate 0px -6px → … → **+0.583779px（峰值）** → 回落`；卡片 rect 回摆到 **`[1095,105,320,512]`**；
  终态 `cardHidden:false` / `miniHidden:true` / `settledScale:"none"`（静止无变换）。
- **时长一律 ≤ 300ms**（见 §十四·④）：弹性来自缓动曲线的过冲，不是靠拉长时长。

---

## 十四、第十四拍排掉的六处坑

| # | 坑 | 判据 / 症状 | 修法 |
|---|---|---|---|
| ① | ★★ **各层 `mark` 是「后一层必须替前一层保住」的契约** —— l3 的 `CSS_TAIL` 把 l2 的标记 `/* r108-l2 */` **覆盖掉** | 紧接着复跑 `patch108l2.py` 判「第 19 节还没写过」⇒ **把整节 CSS 又追加一份**（panel.css 涨到 78431 字符、`19. 任务信息面板` 与 `.zd-card {` 各出现 **2** 次） | `CSS_TAIL + '/* r108-l2 */\n'` **原样接回**；l3 的 mark 改 `/* r108-l3 */`；`main()` 末尾加**跨层标记兜底断言**（5 个标记必须存活 + 第 19 节不得重复），失败即 `sys.exit` |
| ② | `drop_re` 的 `.*?` **不跨行**（缺 `(?s)`） | 「删『计划』分区」永远命中 0 次 ⇒ 被静态判成「已应用」而**静默跳过** | 加 `(?s)`，并补反判据「删完 `data-zd-sec="plan"` 不再命中 **且** `data-zd-sec=` 计数 = 3」写入前 `sys.exit` |
| ③ | **八处 `GROUP_EDITS` 共用同一个 mark**（`.zd-menu.giencoder-dropdown-popup {`） | 第一处一落地，后七处全被判「已应用」而**静默漏改** | 每处自带**独立的完整选择器行**作 mark（4 元组） |
| ④ | **`verify-design.py` 的 CRAFT-ANIM 上限 = 300ms** | 初稿 `grid-template-rows 340ms` + `animation: zd-panel-in 360ms` 让 md5 从基线 `3dbf6543…` 变 `bd9f423b…`、汇总 76 → 78 条 | 全部压到 ≤300ms（340/360/320 → **300**）；注释里写明「弹性来自 spring 的 y1 = 1.56，不是靠拉长时长」 |
| ⑤ | ★ **探针自身的三类假失败**（本轮新增两条） | ⓐ `ev()` 裁 `tail -1` ⇒ 探针自身 TypeError 只剩 `at <anonymous>:215:3`（无信息量）；ⓑ `S(el).color` 不判空（**分支菜单没有 `.td-mm-key`**）⇒ TypeError 冒到 IIFE 收尾行，栈指向完全无关的位置；ⓒ rAF 末帧落在入场类被摘掉之后时 `scale` 的 computed 值是 **`none`** ⇒ `parseFloat` → NaN ⇒ `lastScale` 误报 **0** | ⓐ `ev()` 改为全量输出；ⓑ 加 `C()/BG()` 安全取值；ⓒ 过滤 NaN + 另报 `settledScale`（静止态 `"none"` 与「峰值过冲 1.0058」明确分开） |
| ⑥ | ★★ **「暗色截图看起来是浅底」是假象** | `p-1440-dark.png` / `n-1440-zd-dark.png` 在预览里看着是浅灰底，**取色实测 rgb(35,35,36) `#232324`（lum 35.3）** ⇒ 主题一直是生效的，是肉眼/预览器骗人 | 新增 `ev/pix.py`（截图取色核验）；**任何「暗色 / 对比度 / 底色」结论先取色、再下判断** |

---

## 十五、第十四拍边界与回归（`probe108p2.sh`，落 `p2-raw.log` 8777 字节）

| 组 | 主题 | 实测 |
|---|---|---|
| `[A]` | **面板不遮挡 `.r93-bar` 两枚按钮** | `actsRect [1359,57,64,28]`；两枚按钮 `visible:true`、`hitSelf:true`（`elementFromPoint` 命中自身）；`overlap:false`、`cardTop 105 > actsBottom 85`（`.zd-host` 从 `top:44px` 起排 + 12px 内距）；`hexLeak:[]` |
| `[B]` | **暗色档全部 token 派生** | 卡片 `bg rgb(35,35,36)` / `border rgb(78,78,78)` / `color rgb(247,247,247)`；胶囊同；两枚下拉 `bg rgb(95,95,96)` / 选中文字 `rgb(84,151,255)` / divider `rgb(43,43,43)`；`.zd-toast bg rgb(95,95,96)`；绿圈 `rgb(93,194,100)`；**§19.x 全量 hex 扫描 = 0 命中**；`cardIsLight:false` / `menuIsLight:false` |
| `[C]` | **`--ui-fs = 18` 杠杆** | `ratio:"calc(18 / 14)"`；`secH 41.1406px`（32×1.2857）/ `headH 46.2812px`（36×）/ `itTitleLH 20.5714px`（16×）/ `itTitleFS 16.7143px`（13×）/ `todoLH 28.2857px`（22×）/ `miniH 41.1429px`；**圆序号 20.5625 × 20.5625 ⇒ `itNoRound:true`**；卡片仍 `[1095,105,320,512]`（不被压平）；内距 `8px` 固定 |
| `[D]` | **窄档 620** | `vw:620` / `mainRect [268,48,344,844]` / `cardRect [285,105,310,512]` / `cardW 310px` / **`overflowRight:-17`** / `inView:true`（`max-width: calc(100% - 32px)` 生效） |
| `[E]` | **右栏四枚 `.td-rv-menu` 回归**（`.zd-menu` 加入第 1 节选择器组后一字未变） | `.td-rv-scope-menu` / `.td-commit-menu` / `.td-rv-opts` / `.td-mod-menu` 骨架与扩员前**逐字一致**：`minW 168px` / `pad 6px` / `radius 8px` / `shadow3-down` / `origin 0% 0%` / `anim none` / 条目 `"5px 8px"` + `radius 4px` + `lh 22px` + `fs 14px` / `dy 6` / `inView:true`；真鼠标 hover 底色 **`rgb(242,242,242)`**（= `--color-fill-2`，契约值）；互斥 `openCount:1` / `zdOpen:0` |

---

## 十六、第十四拍门禁（产物定稿后复跑）

| 门禁 | 结果 |
|---|---|
| 三层幂等 | `patch108l1.py` **全跳过** / `patch108l2.py` **0/8** / `patch108l3.py` **0/27**（+1 是圆序号那条）+ `4/4 跨层标记兜底断言`「全部存活 ✓」 |
| 生成链幂等 | `apply108.py` 第二遍「已是目标态（无改动）」 |
| 语法 | `mg-work/check-syntax.py pages/*.html` ⇒ **10/10 通过**（`conversation.html script=9 style=16`） |
| 设计规范 | `verify-design.py ./pages` 与 `mg-work/r107/ev/vd-r107l2.txt` **逐字节相同**（md5 **`3dbf654337559509110899e48bef1b1c`** / **21882 字节**）⇒ 零新增 |
| 字号压平 | `mg-work/r108/ev/scan-flatten.py mg-work/r108/part108/panel.css` ⇒ **2 条**（`.td-mod-bar` / `.td-url` = 基线） |
| 真机（主链） | `probe108p.sh` ⇒ `p-raw.log` **13520 字节**，八组全绿 |
| 真机（边界） | `probe108p2.sh` ⇒ `p2-raw.log` **8777 字节**，五组全绿 |
| 目视 | `shots108p.sh` ⇒ `raw/p-1440-*.png` **16 张** |
| 工具污染 | `pages/gaps.log` 已 `git checkout --` 清理 |

---

## 十七、第十四拍改动清单

| 文件 | 改动 |
|---|---|
| `mg-work/r108/ev/patch108l3.py` | **新建**（772 行 / 27 项）：①②③④ 四条 + 跨层兜底断言；四步（`drop_re` / `edit_all` ×8 / `edit` ×17 / 断言） |
| `mg-work/r108/part108/_mods.html` | 删「计划」分区；三行接交互；图标全换 lucide 原路径；`.zd-cv` 14px；追加 `.zd-menu-branch` / `.zd-menu-commit` / `.zd-toast`（**挂在 `.zd-mini` 之后、`.zd-host` 内** —— 不能在 `.zd-card` 内，卡片 `overflow:hidden` 会裁掉 DS 弹层） |
| `mg-work/r108/part108/panel.css` | 就地改 6 处（分区头 28→32 / 折叠箭头 12→14 + spring / 删 `display:none` / 迭代行内距圆角 hover / 标题行高 20→16 / **圆序号宽高同比**）+ 末尾 `19.1`/`19.2`/`19.3` 三小节 + **G1~G8 八处选择器组各加 `.zd-menu`** |
| `mg-work/r108/part108/panel.js` | 末尾 IIFE 从「立刻 `hidden` 硬切」换成「Git 三行 + 两枚下拉 + `zdSwap` 弹性场次」 |
| `mg-work/r108/up/` | **新建**：上游 `ConversationStatusPanel.tsx` + `conversationStatusPanelModel.ts`（权威依据入库） |
| `mg-work/r108/ev/p108p.js` | 主链多相位探针（16 相位；`foldStart`/`miniOutStart`/`miniInStart` 三个相位**在同一 eval 内装 rAF 采样器再触发点击**） |
| `mg-work/r108/ev/p108p2.js` + `probe108p2.sh` | **新建**：边界与回归多相位探针（`bar`/`dark`/`fs`/`narrow`/`rv0`/`rvs`/`rvsh`/`rvc`/`rvo`/`rvall`/`final`） |
| `mg-work/r108/ev/pix.py` | **新建**：截图取色核验（防「目视误判明暗」，§十四·⑥） |
| `mg-work/r108/ev/shots108p.sh` + `raw/p-1440-*.png`（16 张） | **新建**：目视取证（含暗色 / `--ui-fs=18` / 窄档 620 三个边界档） |
| `mg-work/r108/ev/bak14/` · `bak14b-panel.css` | 临时备份（跑 l3 前的三个产物 + 补丁后快照）—— **不入库** |
| `pages/conversation.html` | 产物（本拍唯一进 `git diff` 的差异页之一） |

**产物口径**：

| 文件 | 读数（字符数 = LF 归一后 `len`） |
|---|---|
| `pages/conversation.html` | 995133 → **1009968（本拍 +14835）**；对 `HEAD` 累计 **+51400**；`git diff` **+855 / −19 行**（第十三拍 +582/−11） |
| `pages/task-detail.html` | **767836，本拍未动**（`git diff` 仍是 `7 / 0`） |
| `pages/base.html` + 8 个外壳页 | **472150，逐字节不变** |
| `part108`：`_mods.html` 62859 / `panel.css` 70729 / `panel.js` 71160 / `browse.html`（splice 产物）98521 | 与 splice 输出「前缀 247 + 头部 5270 + Files 正文 30130 + 新模块 62859 = 总 98521」**逐个对齐** |

> ⚠ **读数口径提醒**（本轮自查踩过一次）：`wc -c` 是**字节**，工程里说的「字符」一律是
> **`io.open(...,'rb').decode('utf-8')` 后 `\r\n → \n` 的 `len()`**。本仓文件含大量中文注释，
> `panel.css` 是 `88709 字节 / 72217 字符 / 70729（LF 归一）` —— **三个数都对**，别互相当成异常。

---

## 十八、第十四拍交接

- 🚫 **仍未 commit / 未 push** —— 等邵先生显式发话。
- ★ r108 仍是**未交付的工作代**：若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**
  （判据 = `git status` 里对应页仍是 ` M` 且 `r108-*` 块已存在）；**不要**新建 r109、**不要**回头改 `apply107.py`。
- ★ 改序仍是下→上：`part108/_mods.html` / `panel.css` / `panel.js` → `ev/splice108.py` → `apply108.py`。
  ★★ **l3 之后若再叠一层，`CSS_TAIL` 要把 `/* r108-l3 */` 也原样接回**（否则 l3 复跑会整块重挂，§十四·①）。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*`，还要 **`git reset -q -- mg-work/r108/ev/bak1[34]/ mg-work/r108/ev/bak14b-panel.css`**；
  `mg-work/r108/raw/` 与 `mg-work/r108/up/` 照旧入库。
- ★ **记忆同步（第十四拍）**：`ev/doc108p.py` 更新 `.workbuddy/memory/{HANDOFF,PAGES,PLAYBOOK,MEMORY,2026-10-01}.md` + 工作区日志；
  PLAYBOOK 新增：① **各层 `mark` 是「后一层必须替前一层保住」的契约**；② `drop_re` 的 `.*?` **必须 `(?s)`**；
  ③ **多处替换共用同一 mark = 静默漏改**；④ `verify-design.py` 的 CRAFT-ANIM **300ms 上限**；
  ⑤ 「弹性」靠缓动曲线过冲而非拉长时长；⑥ **带字号 token 的规则不得写裸 `height:Npx`**（否则 `width` 不跟 ⇒ 圆变椭圆）；
  ⑦ **主题类结论先取色再下判断**（`ev/pix.py`）。

## 十九、第十四拍记忆同步（`ev/doc108p.py`，实测读数）

**口令**：`WHEN = u'2026-10-01 20:5x'`（沿用 `HH:Mx` 约定，与 `doc108n/o.py` 一致）。

### 19.1 脚本自身的两处 `SyntaxError`（★ 本轮新增的教训）

首跑 `--check` 直接崩在 `SyntaxError: invalid syntax. Perhaps you forgot a comma?`，
**`ast.parse` 报的是第 266 行，而那一行完全合法**（就是普通的 `u'...'` 相邻拼接）。
真凶（用 **tokenize 找 `STRING` 紧跟 `NAME`** 定位，一行命中）：

| 行 | 原文 | 症状 |
|---|---|---|
| 270 | `u'> 　① …（\`[data-td-open-mod="review"]\` ⇒ \`openTab('review')\` …）\n'` | **单引号字面量里嵌了单引号** ⇒ 字符串在 `openTab(` 处提前闭合 |
| 404 | `u'> **四条** = ① … \`openTab('review')\` … \n'` | 同型 |

⇒ 修法 = 转义成 `openTab(\'review\')`（**渲染后文本一字不变**）。
⚠ **「按行数 `'` 的奇偶」扫描抓不到**（那行有 4 个 `'`，偶数）—— 必须用 token 判据。

### 19.2 三跑实测

| 跑次 | 结果 |
|---|---|
| `--check` | **锚点异常 0 处**（HANDOFF 3 处 + PAGES 1 + PLAYBOOK 1 + MEMORY 1 + 两日志各 1） |
| 第 1 遍（写） | **应用 13 项 / 跳过 0 项**；六份文件全部变形 |
| 第 2 遍（幂等） | **应用 0 项 / 跳过 13 项**，六份 md5 **全部未变** ★ |

六份文件体积（字符）：

| 文件 | 前 | 后 |
|---|---|---|
| `.workbuddy/memory/HANDOFF.md` | 131897 | **137591** |
| `.workbuddy/memory/PAGES.md` | 103152 | **104794** |
| `.workbuddy/memory/PLAYBOOK.md` | 186053 | **194098** |
| `.workbuddy/memory/MEMORY.md` | 31160 | **32468** |
| `.workbuddy/memory/2026-10-01.md` | 55769 | **58387** |
| 工作区 `…/memory/2026-10-01.md` | 38214 | **40832** |

### 19.3 落点核验（Python 读，非 shell —— 本机 `grep` 查中文返回空）

- `HANDOFF.md` 第 4 行 = `最后更新：2026-10-01 20:5x`；第 5 行 = `⚠️ **最新一拍 = r108 第十四拍（四条 · ★★ 就地返工、未另起代数）**`。
- `PAGES.md` L636 = `### P3.11i … **共十四拍**`；L649 = `> **⑫ r108 第十四拍（四条 · 全部围绕 \`.zd-card\`）**`；
  L657 = `padding 8px`（★ 复核项：**未被截断**，确认是 `padding` 而非 `pad ding`）。
- `PLAYBOOK.md` L4209 = `## P3.50 …`；L4253 = 附录「工作区速览 58 条」。
- `MEMORY.md`（仓库）L295 / 两份日志 L851 / L601 各含「第十四拍」。

### 19.4 工作区 `E:/GienCoder/.workbuddy/memory/MEMORY.md`

**2987 字符 / 44 行**（< 3000 限额）= 三段：① Windows 速记 ② 红线速览（精选 18 条，全表 58 条已迁 PLAYBOOK 附录）
③ 最近拍。★ 会话开头注入的是**压缩前的旧快照**（故仍报「超长被截断」），磁盘上已是精简版。

### 19.5 工作区状态（收尾定格）

```
 M .workbuddy/memory/{2026-10-01,HANDOFF,MEMORY,PAGES,PLAYBOOK}.md   ← 记忆同步（本节）
 M pages/conversation.html      （1009968 字符）
 M pages/task-detail.html       （767836，第十四拍未动，仍是 prev 代的 7 0）
?? mg-work/r108/                 + mg-work/r107/ev/bak{7,8,9,10}/
```
`pages/base.html` **逐字节不变**；**未 commit / 未 push**。

## 二十、第十五拍逐条落地（r108 第四层补丁 · 六条 · 全部围绕 `.zd-card`）

落点：`mg-work/r108/ev/patch108l4.py`（8 项）→ `_mods.html` 1 项（DOM 删行）+ `panel.css` 6 项 + l4 标记。
`panel.js` **一字未动**。改序 = `patch108l4.py` → `ev/splice108.py` → `apply108.py`（**无需** `make108.py`，
它在运行时才从 `part108/` 读三件）。

| # | 需求 | 落地 | 真机读数（1440×900） |
|---|---|---|---|
| ① | `.zd-sec-t` 正文黑 / 500 / 14px | 去掉 `font-size/color: inherit`，显式 `font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1)`；顺带删掉已成**死规则**的 `.zd-sec-t:hover { color: text-1 }` | 三个分区标题（Git 工具 / 目标 / 进程）**全部** `fs 14px` / `fw 500` / `color rgb(31,31,31)`；`lh 21px`（未声明、由行盒给出） |
| ② | `zd-card` 里的操作图标补 hover | `.zd-ico` 由「只有宽高」改成照本页既有 `.td-browse-ico` 的完整契约（`inline-flex` / 24 盒 / `padding:0` / `border:0` / `radius 4` / 透明底 / `text-2`）+ 同块内 `:hover { background: fill-1; color: text-1 }`（硬规则 28：基态在前） | 真鼠标 hover「收起为胶囊」：`bg rgba(0,0,0,0) → **rgb(247,247,247)**`（= `--color-fill-1`）、`color rgb(78,78,78) → **rgb(31,31,31)**`（= `--color-text-1`）；`matches(':hover')` 同步为 true。两枚 `.zd-ico` **都**拿到了这套规则 |
| ③ | 「目标」只留一条 | `_mods.html` 删掉带圆序号那条（`drop_re`，连前导换行一起删、不留空行） | `.zd-it` **1** 行 / `.zd-it-no` **0** / `.zd-it-i` **1** / 文案「落地审查、终端、浏览器、摘要四个面板」/ 计数「3/4」 |
| ④ | 已完成加删除线 + 进行中转 loading | `.zd-todo li.is-done { … text-decoration: line-through }`；`.zd-todo li.is-doing::before` 压到 `opacity:.28`（仍是 `primary-6`）、`::after` 画一段 `primary-6` 的实心弧 + `@keyframes zd-todo-spin` | `is-done`（3 条）`deco: **line-through**` / `color rgb(134,134,134)`；`is-doing::after` `animationName **zd-todo-spin**` / `duration **0.82s**` / `iterationCount **infinite**` / `borderTopColor **rgb(55,112,247)**` / `radius 50%`；**两次采样 320ms 间隔的 `transform` 矩阵不同**（atan2 角度 81° → 12°）⇒ 确实在转 |
| ⑤ | 骨架屏显示时不应显示 `zd-card` | `html:has(.r93-sk) .zd-host { display: none }`（纯 CSS 开关，骨架屏一从 DOM 移除即自动失效） | `CSS.supports('selector(html:has(.r93-sk))')` = **true**；注入假 `.r93-sk` ⇒ `display **none**`（cardRect 全 0）→ 移除 ⇒ 回到 `flex`。★ **真实加载期时序**：`open` 后立刻装 rAF 采样器，时间线 `[[0,"none",true],[144,"flex",false]]`（= 骨架屏在文档里时面板 none，骨架屏一移除 +144ms 立刻 flex） |
| ⑥ | `.zd-sec-x` 只有折叠态才显示 | 基态 `display: none`，补 `.zd-sec.is-closed .zd-sec-x { display: flex }`（两者特异性 (0,1,0) / (0,3,0) 不同 ⇒ 不涉硬规则 24 的「打平」） | 默认（全展开）三个分区 trailing **全 `display:none`**；折叠「目标」后该分区 `display **flex**`（可见「2 分 18 秒 · ⏸」）且 `bodyRows 0px`；再展开回 `none` |

### ② 的一处伴生变化（记录在案）

`.zd-ico` 原来**没有任何 `color` 声明** ⇒ 头部那枚继承 `.zd-card` 的 `text-1`、分区头那枚继承
`.zd-sec-h` 的 `text-3`，两枚深浅不一致。改成 `.td-browse-ico` 那套后**基态统一为 `text-2`**、
hover 统一到 `text-1`。这是「同一份卡片里同类控件同口径」的必要代价，也是本页既有那套按钮的口径。

## 二十一、第十五拍排掉的坑（五条）

1. ★★ **`mark` 撞车 ⇒ 整条改动被静默跳过。** ① 的 `mark` 初稿取的是改后的声明串
   `font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);` —— 它与上文
   `.td-sum-prev-t b` 那条声明**逐字相同** ⇒ 首跑判「已应用」、**整条①根本没写进去**，而末行照样打印
   「应用 N 项 / 跳过 0 项」。⇒ 本轮给 `edit()` 加了**「mark 歧义」硬断言**：
   `old` 与 `mark` **同时**存在于同一份文件里就 `sys.exit`（mark 的语义是「只有改完才出现」）。
   ⚠ 并给它留了一个 `strict=False` 豁免位 —— 本层末尾那条「**插在 `/* r108-l3 */` 之前、并把该标记
   原样接回**」的写入天然会让两者共存（锚点**必须**留下来当下层的契约）。
   （初跑当场被这条断言逮到，回滚 `ev/bak15-{panel.css,_mods.html}` 重来。）
2. ★★ **`verify-design.py` 的 CRAFT-ANIM 是「按行扫 `animation|transition … <数字>ms`」。**
   `:has()` 那条无关，但 ④ 的 loading 若直接写 `animation: zd-todo-spin 820ms …` 会**新增 1 条 warning**
   ⇒ 门禁 md5 就不再等于 r107 基线。⇒ 把时长写进**自定义属性** `--zd-spin-dur: 820ms`、
   规则里写 `animation: zd-todo-spin var(--zd-spin-dur) …`；并把解释性注释也拆成「不含 `ms` 数字」的行，
   免得注释把自己扫进去。（craft 那条规则针对的是**交互动效**；持续旋转的不确定进度指示器不在其适用范围。）
3. **自检判据自己写错两处**：`.zd-sec-x {` 会被同一层新加的 `.zd-sec.is-closed .zd-sec-x {` 一起命中；
   `zd-todo-spin` 天然出现 2 次（`animation-name` + `@keyframes`）。⇒ 判据一律取**「块首那几行」的更大片段**
   （`.zd-sec-x {\n  flex: 1 1 auto` / `@keyframes zd-todo-spin {`）。
4. **探针里 `document.querySelector('html:has(.r93-sk)')` 在不支持 `:has()` 的环境会抛 `SyntaxError`**
   ⇒ 整条探针挂死、看起来像「产品坏了」。⇒ 必须 `try/catch` 并把结果标成 `unsupported:<ErrName>`。
5. **`agent-browser` 没有 `move` 命令** ⇒ 想取消 hover 只能 hover 一个**中性兄弟元素**
   （本轮用 `.zd-name`），不能「把鼠标挪到空白处」。

## 二十二、第十五拍门禁（产物定稿后复跑）

| 门禁 | 结果 |
|---|---|
| `check-syntax.py pages/*.html` | **10/10 通过** |
| `verify-design.py ./pages` | **21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`** —— **逐字节等于 r107 基线**（未新增 CRAFT-ANIM） |
| `scan-flatten.py part108/panel.css` | **2 条**（`.td-mod-bar` / `.td-url`，与基线一致；本轮新增的三条规则都不含裸 `height/min-height`） |
| 四层幂等 `patch108l1 / l2 / l3 / l4` | l1 全跳过 / **0-8** / **0-27** / **0-8**（l4 为 `应用 0 项 / 跳过 8 项` ×2） + 跨层兜底断言「全部存活 ✓」 |
| `apply108.py` 第二遍 | `conversation.html` / `base.html` **已是目标态（无改动）** |
| 边界回归 | 暗色（card `rgb(35,35,36)` / 标题 `rgb(247,247,247)` / done `rgb(169,169,169)` / 弧 `rgb(84,151,255)` / **`hexLeak: []`**）、`--ui-fs=18`（标题 `18px`/`fw 500`、分区头 `41.14px`、图标盒仍 `24px`、卡片 `[1095,105,320,512]`）、窄档 620（`overflowRight -17` / `inView true`） |
| **关键类判据** | ② 的 hover 走**真鼠标 + 「另起一次 eval 读 `getComputedStyle().backgroundColor`」**（只查类名 / 规则存在性发现不了）；④ 的旋转走**两次采样比 `transform` 矩阵**；⑤ 走**注入式判据 + 真实加载期 rAF 时间线**双证 |

## 二十三、第十五拍改动清单

| 文件 | 变化 |
|---|---|
| `mg-work/r108/ev/patch108l4.py` | **新建**（8 项；含「mark 歧义」硬断言 + `strict=False` 豁免位） |
| `mg-work/r108/ev/p108q.js` / `p108q2.js` / `probe108q.sh` | **新建**（六条真机探针 / 加载期时序采样器 / 执行链） |
| `mg-work/r108/ev/bak15-panel.css` / `bak15-mods.html` | **新建**（首跑翻车后的回滚基线；提交前 `git reset`） |
| `mg-work/r108/part108/_mods.html` | 62859 → **62701** 字符（删「目标」圆序号那一行） |
| `mg-work/r108/part108/panel.css` | 70729 → **73063** 字符（6 处就地改 + l4 标记） |
| `mg-work/r108/part108/panel.js` | **71160 字符，一字未动** |
| `mg-work/r108/part108/browse.html` | 98521 → **98363**（splice108 重建，产物不是手改对象） |
| `pages/conversation.html` | 1009968 → **1012144**（+2176；对 HEAD 累计 `896 19`） |
| `pages/task-detail.html` | **767836 未动**（仍 `7 0`） |
| `pages/base.html` | **472150 逐字节不变** |

★ 代数核对：`r108-conv-css` / `r108-conv-js` 各 **1**；`r107-conv-*` / `r106-nav-js` 仍 **0**。

## 二十四、第十五拍交接

- 🚫 **仍未 commit / 未 push** —— 等邵先生显式发话。
- ★ r108 仍是**未交付的工作代**：再改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
  **不要**新建 r109、**不要**回头改 `apply107.py`。
- ★ 改序仍是下→上：`part108/{_mods.html,panel.css,panel.js}` → `ev/splice108.py` → `apply108.py`。
  ★★ **l4 之后若再叠一层（`patch108l5.py`），`CSS_TAIL` 必须把 `/* r108-l4 */` 也原样接回**
  （四层各自复跑都要能命中自己的标记，§二十一·1）。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*`，还要
  **`git reset -q -- mg-work/r108/ev/bak1[345]*`**；`part108/` 与 `raw/`、`up/` 照旧入库。
- ★ **记忆同步（第十五拍）**：`ev/doc108q.py`。PLAYBOOK 新增 P3.51，要点 =
  ① `mark` 撞车 ⇒ 静默跳过（加「old 与 mark 共存即报错」的硬断言 + 类外豁免位）；
  ② 「持续旋转」类动效的时长写进自定义属性以避开按行扫的门禁；
  ③ 只有 `:has()` 才能做「某元素在 DOM 里 ⇒ 隐藏另一处」的纯 CSS 门控（且必须 try/catch 探测支持性）；
  ④ `text-decoration` 不传播到绝对定位伪元素 ⇒ 删除线与自定义标记可以共存；
  ⑤ 自检判据别用太短的片段（会被同层新加的同类选择器一起命中）。


## 二十五、第十六拍逐条落地（r108 第五层补丁 · 三条）

| # | 邵先生原话 | 落地体位 | 真机读数（1440×900，`--ui-fs=14`，`ev/r5-raw.log`） |
|---|---|---|---|
| ① | 「改变一下产物 `td-sum-art` 卡片点击后的预览方式，在 `td-browse-bar` 作为一个新页签显示」 | 旧浮层 `.td-sum-prev`（`position:absolute; inset:0` 盖住 `.td-mod.td-sum`）**整体拆掉** —— DOM 一块 + CSS 全套 + `.td-mod.td-sum{position:relative}` + **Esc 裁决链里占的那一层**；新载体 = `#av-browse-pane-preview[data-td-pane="preview"]`（与「审查 / 终端 / 浏览器 / 摘要」同级）。点产物 → `openTab('preview', {name, ico})`。 | 点第 1 个产物：页签 `[摘要, 预览]`，`preview.name='右栏复刻方案.md'`、`ico=true`、`aria-controls=av-browse-pane-preview`、`md=flex / xlsx=none`、**barH 40**。点第 2 个：**页签仍 1 枚**（复用），name 换成 `sidepanel-metrics.xlsx`、图标换成表格字形、`md=none / xlsx=flex`。页签 `×`：页签消失、`preview` 回 `hidden`、`summary` 回 40px。切「摘要」→ 预览 hidden；切回「预览」→ 40px 复现。 |
| ② | 「`zd-host` 的展开折叠动效换一种，最好是那种折叠时收进右上角，展开时从右上角向左下角方向展开」 | `transform-origin: 100% 0`（= 面板右上角，正是头部那枚「收起为胶囊」按钮所在的角）；出场 `opacity 160ms / scale+translate 170ms`，入场 `@keyframes zd-panel-in` 260ms spring。位移只做同向补强（`12px -12px`，小于到视口右缘的 16px）。 | **同一次 eval 内「点 + rAF 采样」**（`recN=50/50`）：收 → `scale 1→0.62`、`translate 0px→12px -12px`、`opacity 1→0` 单调，t=186ms 到目标、t=203ms 卡片 `hidden` / 胶囊 shown。`transform-origin` 量到 **`320px 0px`**（卡宽 320 ⇒ 就是「100% 0」）。展 → t=186ms 首次出现即 `scale 0.62 / translate 12px -12px / opacity 0` 且 `animationName=zd-panel-in`，随后**过冲**到 `scale 1.03715 / translate -1.173px` 再回 `1 / 0px`（t=453ms）。胶囊自己是 `103.094px 0px`（= 它的 100% 0）。 |
| ③ | 「尝试把 `zd-host` 整个容器设计为模糊背景效果」 | `.zd-host` 是**定位壳**（无底色 / `pointer-events:none`）⇒ 视觉表面=它里面的四件：卡片 `.zd-card`、胶囊 `.zd-mini`、两枚下拉 `.zd-menu`、轻提示 `.zd-toast`，**四件一起换**。底色 `color-mix` 就地取透（不新增 hex）+ `backdrop-filter: blur(18px) saturate(160%)`；另给不支持 `backdrop-filter` 的引擎留 `@supports not (...)` 不透明兜底。 | computed：卡片/胶囊/轻提示 `color(srgb 1 1 1 / 0.78)`、`backdrop-filter: blur(18px) saturate(1.6)`；两枚下拉 `color(srgb 1 1 1 / 0.82)`（各自沿用 `--color-bg-popup`）；暗色档卡片 `color(srgb 0.137255 0.137255 0.141176 / 0.78)` = #232324 的 78%。**逐像素**（`ev/pix.py`）见 §二十六·5。 |

**① 的一处设计取舍（可一句话翻转）**：同一枚「预览」页签**复用**承载多个产物（与 VS Code 的 preview tab 同口径）⇒ 连点两个产物只更新页签名 + 正文，不会开出第二枚标签。若要「每个产物一枚标签」，只需去掉 `openTab` 复用分支里的 name/ico 同步，并把 `mod` 改成 `preview:<文件名>`。

## 二十六、第十六拍排掉的坑（六条）

1. ★★★ **删一个变量只删「定义」、不删「引用」⇒ 按一次键就抛 `ReferenceError`**（本拍真踩，跨层自检逮到）。
   `prevEl` / `prevHide` 定义在**摘要模块**那一段，却被**下面**的 Esc 裁决链引用
   （`var prevOpen = prevEl && !prevEl.hasAttribute('hidden')`）。浮层一删，这个标识符就悬空了
   —— 而它在一个 `window` **捕获段**的 keydown 处理器里 ⇒ 按一次 Esc 整条处理器抛错，
   顺带把「关整条侧栏」也带坏。
   配方：**删组件时全仓 grep 该变量名**（含引用点），并且判据要**剥掉注释再搜**
   —— 本层注释里为了留痕主动写了 `prevEl` / `if (prevOpen) prevHide();` ⇒ 裸串搜索必误报；
   同时**别把 `\b` 词界丢掉**（`prevOpenBtn` 会把 `prevOpen` 命中，本层为此白跑一轮）。
2. ★★ **`openTab` 的「已存在 ⇒ activate」分支不会更新页签名/图标**（本拍真踩，截图肉眼可见）。
   连点两个产物 ⇒ **页签写着 `右栏复刻方案.md`、正文已经是 `sidepanel-metrics.xlsx` 的表格**；
   探针里 `tabs[].name` 与 `prev.name` 对不上就是判据。
   修：复用分支加 `if (opts) { 同步 name / ico / aria-label }`，★ **必须带 `opts` 守卫**
   —— `+` 模块菜单与右键菜单那几处**不传 `opts`**，不守卫就会顺手改掉「文件 / 审查 / 终端」的页签名。
3. ★★ **`.td-mod-bar` 的高度不是「40px」，而是「内容驱动」**。
   它的 `min-height: calc(40px * var(--ui-fs-ratio))` 被 `apply88b.converge()` **压平成裸 `40px`**
   （=`scan-flatten` 那 2 条之一，见 PLAYBOOK P3.4x）⇒ 真实高度 = `6 + max(内容高) + 6 + 1(border)`。
   28px 的图标砖或 28px 的按钮都把它顶成 **41px**（首轮实测 41 ⇄ 摘要 40）。
   ⇒ 本模块内两件各收到 26px（`.td-pv .td-sum-arti` 只收本模块的，产物行那两个保持 28px）。
   ★ 通用判据：**内容盒上限 = `min-height` − 上下 padding − border-bottom**。
4. ★★ **同一页里工具条本来就不齐，别默认「基线是齐的」**。
   实测 `--ui-fs=14`：摘要 **40** / 审查 **41**；`--ui-fs=18`：摘要 **41** / 审查 **49** / 预览 **46**。
   根因同 3（`min-height` 被压平 ⇒ 谁内容高谁高）。所以「预览 40 = 摘要 40」已经是**本页最对齐**的一种取法
   （预览页签是从摘要点出来的，两条 40 互换时工具条不跳）；fs18 下与摘要差 5px 是**既有结构**带来的，
   不是本层引入的（审查差 8px）。
5. ★ **「只写 `backdrop-filter`、底色仍是不透明 token」= 完全看不出效果**，
   而这正是「量一下 computed 有 `backdrop-filter` 就以为成了」的陷阱（本层第一版就差点这么收货）。
   ⇒ 必须落到**像素**：在卡片正下方临时铺 320×180 **纯红**，再 `ev/pix.py` 取色 ——
   实测卡片像素 `rgb(255, 199, 199)` = `0.78×白 + 0.22×红`（与解析解逐位吻合），
   且沿 y **平滑衰减**：`199`(y40) → `211`(y170) → `237`(y190，**已越出红块下沿却仍带红**：模糊外溢) → `254`(y470)；
   正常页面底同点位 `rgb(246, 248, 253)`。
   ⇒ **半透明（底色被染）与模糊（边缘外溢、无锐利分界）各得一条互不替代的证据**。
6. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（内容是 `file:line — 描述`，行号会随**任何**改动漂移）
   ⇒ 本轮它就凭空多了 `64 / 44` 行 diff。**收尾一律 `git checkout -- pages/gaps.log`**。

## 二十七、第十六拍门禁（产物定稿后复跑）

| 门禁 | 期望 | 实测 |
|---|---|---|
| `mg-work/check-syntax.py pages/*.html` | 10/10 | **10/10 通过** |
| `verify-design.py ./pages` | md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节 | **逐字节相等** ✓ |
| `scan-flatten.py part108/panel.css` | 2 条（`.td-mod-bar` / `.td-url`） | **2 条，未变** ✓ |
| l1 复跑 | 全跳过 | 退出码 0 ✓ |
| l2 复跑 | `应用 0 / 跳过 8` | ✓ |
| l3 复跑 | `应用 0 / 跳过 27` | ✓ |
| l4 复跑 | `应用 0 / 跳过 8` | ✓ |
| **l5 复跑** | `应用 0 / 跳过 10` | ✓ + 跨层「全部存活 ✓」 |
| `apply108.py` 第二遍 | 已是目标态 | ✓（`base.html` 无改动） |
| `git status` | 只动 `conversation.html` + `task-detail.html` | ✓（`gaps.log` 已还原） |

## 二十八、第十六拍改动清单

| 文件 | 变化 | 关键落点 |
|---|---|---|
| `mg-work/r108/part108/_mods.html` | 62701 → **62454** 字符（441 行） | 删浮层块（268~305 行）；摘要 `</section>` 之后新增 `#av-browse-pane-preview` |
| `mg-work/r108/part108/panel.css` | 73063 → **74888** 字符（1569 行） | 18-③ 段重写（页签版）；`@keyframes zd-panel-in` 与 `.zd-card/.zd-mini` 过渡段重写；文件尾新增 19.5（毛玻璃）；`/* r108-l5 */` |
| `mg-work/r108/part108/panel.js` | 71160 → **72477** 字符（1670 行） | `openTab`（`opts.ico` + 复用分支同步）；`prevShow` 改开页签；Esc 裁决链删预览那一层 |
| `mg-work/r108/part108/browse.html` | 98363 → **98116**（splice108 重建） | 前缀 247 + 头部 5270 + Files 正文 30130 + 模块 62454 |
| `pages/conversation.html`（产物） | 1012144 → **1015095** 字符 / **8436** 行 | `git diff --numstat` = **`1047 107`** |
| `pages/task-detail.html` | **767836 字符，本拍未动**（`7 0` 是与 HEAD 的存量差） | — |
| `pages/base.html` | **472150 字符，逐字节不变** | — |

产物度量：工作区 bytes **1132584** / LF bytes **1124149** / 字符 **1015095** / 行 **8436** /
`sha1_lf` **`da1acf6a091c`**；`r108-conv-css`·`r108-conv-js` 各 1；`r108-l5` 1；`zd-sum-prev` **0**。

取证产物：`ev/p108r.js`（相位探针）、`ev/probe108r.sh`（全链）、`ev/probe108r2.sh` + `ev/on.js`（复测 + 工具条对照表）、
日志 `ev/r-raw.log` / `r2-raw.log` / `r3-raw.log` / `r4-raw.log` / `r5-raw.log`；
截图 `raw/r-1440-pv-md.png`（预览页签 + Markdown 骨架）、`r-1440-pv-xlsx.png`、`r2-tabs-after-pvB.png`（复用页签已改名换图标）、
`r-1440-pv-tabs1.png` / `r-1440-tabs-summary.png` / `r-1440-pv-back.png`（页签三态：开预览 / 回摘要 / 再回预览）、
`r-card-over-red.png` / `r-card-over-page.png`（毛玻璃像素取证：红块 / 正常页底）、
`r-1440-dark.png`（暗色档毛玻璃）、`r-1440-fs18-tabs.png` / `r-1440-fs18-pv.png`、
`r2-bars-fs14-terminal.png` / `r2-bars-fs18-preview.png` / `r2-bars-fs18-terminal.png`（五模块工具条对照表）、`r2-pv-xlsx.png`。

## 二十九、第十六拍交接

- 本拍 = **r108 第五层补丁 `ev/patch108l5.py`**（10 步）。r108 **仍未提交**（`HEAD == origin/main == 9c09afa`）。
- ★ 改序仍是下→上：`part108/{_mods.html,panel.css,panel.js}` → `ev/splice108.py` → `apply108.py`；
  `part108/browse.html` 是 splice 的产物、不是手改对象。
- ★★ **l5 之后若再叠一层（`patch108l6.py`），`CSS_TAIL` 必须把 `/* r108-l5 */` 也原样接回**
  （五层各自复跑都要能命中自己的标记，§二十七）。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*`，
  还要 **`git reset -q -- mg-work/r108/ev/bak1[3-6]*`**；`part108/`、`raw/`、`ev/` 照旧入库。
- ★ **别忘 `git checkout -- pages/gaps.log`**（§二十六·6）。
- ★ 记忆同步（第十六拍）= `ev/doc108r.py`；PLAYBOOK 追加 P3.52，要点见 §二十六 六条。

## 三十、第十七拍逐条落地（r108 第六层补丁 · 四条）

邵先生四条：① `+` 下拉菜单位置没跟着触发器走；② 浏览器「截图到剪贴板 / 缩放 / 发送页面到对话」三枚图标按钮去掉；
③ 审查模式的文件树蒙层要留出标题栏 `td-browse-bar`；④ `td-diff-rows` 里的代码要更多更长。

| # | 落地 | 关键判据（真机实测） |
|---|---|---|
| ① | `.td-mod-menu` 纳入 `panel.js` 的 `placeRv()`（原被 `!menu.classList.contains('td-rv-menu')` **显式放行**，一直吃基类写死的 `left: 64px`） | 侧栏就位后 **dx 恒 0**：1 枚页签 `add=1505 / menu=1505`；4 枚页签 `1160 / 1160`（inline `left:368px`）；`--ui-fs=18` `1196 / 1196`（inline `left:404px`）。修复前 1440 三枚页签实测 **dx = −218px** |
| ② | `_mods.html` 三枚 `data-td-brw-act="shot\|zoom\|send"` 整块移除；配套清掉 `panel.js` 的 `BRW_TEXT` 三条 + `shotFlash()` + 调用点、`panel.css` 的 18-② 快门（`is-shot::after` + `@keyframes td-shot-flash`）与只为它存在的 `.td-mod.td-brw{position:relative}` | `brwActs = ["more"]`、`shotEls = 0`；`panel.css` 剥注释后 `is-shot` / `td-shot-flash` **各 0 处**；截图 `t-url-after.png` 只剩 后退/前进/刷新/地址栏/标注/更多 |
| ③ | `.td-tree` 的 `inset: 0` → `top: 44px; left/right/bottom: 0` | `treeRect.top − barRect.bottom = **0**`、`scrimTopVsBarBottom = 0`、`treeTop: "44px"`；截图 `t-tree-open.png` 标题栏（摘要/终端/浏览器/审查/`+`）完整露出 |
| ④ | 两张展开卡片的统一视图 +17/+12 行、并排视图 +11/+6 行（真实 HTML/CSS diff 文本） | 行数：卡片 1 统一 **11→28**、并排 **6→17**；卡片 2 统一 **4→16**、并排 **3→9**；`.td-rv-body` `scrollHeight == clientHeight == 757`（**正好填满、不溢出**） |

★ **① 的一句话取舍**：菜单左缘对齐 `+` 左缘（VS Code 同口径）；若想改成「右缘对齐」或「居中」，改
`placeRv()` 里 `left = tr.left - ox` 这一行即可（右侧放不下时仍会自动向左收、贴住面板右内边）。

## 三十一、第十七拍排掉的坑（八条）

1. ★★★ **`mark` 选在「改前就存在的串」上** ⇒ `edit()` 抛「mark 歧义」并 `sys.exit`。本轮真踩：
   `BRW_TEXT` 里 `more: '…'` 那条**改前就在**（它本来就是最后一条）⇒ 不能当 mark。
   正解 = 取**「改完才形成的相邻关系」**：`var BRW_TEXT = {` **紧跟** `more:` 只在删掉三条之后才成立。
2. ★★ **`old` 会被 `new` 原样保留 ⇒ 复跑时 `old` 仍命中**（本轮：`.td-mod-menu { left: 64px; right: auto; }`
   只在它**上方补了一段注释**）⇒ 必须显式 `strict=False`。与 l5「插在锚点前 + 把锚点接回」同类。
3. ★★ **自检判据别用「裸属性名计数」**：`panel.js` 里 `data-td-brw-act` 保留 **2** 处才是对的
   （`querySelectorAll('[data-td-brw-act]')` + `getAttribute('data-td-brw-act')`）⇒ 判据改成
   「**带 kind 的**引用为 0」（`data-td-brw-act="`）。与「判据要剥注释」同族 —— **先想清楚这个计数该等于几**。
4. ★★★ **「位置不对」先分清「算法没跑到」还是「压根没进算法」**：`+` 菜单的漂移根因**不在** `placeRv`
   的算式里，而是它上面那句 `if (!menu.classList.contains('td-rv-menu')) return;` —— **显式放行**，
   注释还写着「保持它原来的 CSS 落位不动」。⇒ 排查浮层位置问题的第一问是「这个元素进算法了吗」。
5. ★★ **删掉一个组件要连带清「借它力」的引用**：右键菜单那条「截图到剪贴板」原来靠
   `sb.click()` 借工具条按钮的力（虽有 `if (sb)` 守卫不会报错，但**点了没反应**）⇒ 改成直接给轻提示。
   判据 = 全页 grep 被删元素的**所有**引用点（DOM / 类名 / 属性选择器 / 事件）。
6. ★★ **`.td-tree` 的包含块是 `.td-browse`（整条侧栏）而不是某个模块** ⇒ 改它的 `inset` 会**同时**
   把 scrim 与 panel 下移。判据要用**相对量**：`treeRect.top − barRect.bottom === 0`。
   ⚠ `44` 是实测值，`--ui-fs` = 14/18 两档量出来都是 44 ⇒ **不随字号杠杆变**，故写裸 px。
7. ★★ **探针的「可见性」盲区**：侧栏初始 `translateX` 把整条 `.td-browse` 推到视口右外
   （实测 `browse.left = 1432`、`+` 在 `1505` > 视口宽 1440）。这时量 dx 仍是 0（两边同处栏外、
   一起偏移），**但截图是空的**。⇒ 要看菜单外观必须走「先点一枚页签 ⇒ 侧栏滑入」那条路径
   （`probe108t2.sh` 里 `openTabs` 那步）。**量到了 ≠ 看得见**。
8. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（行号随任何改动漂移）⇒ 收尾
   `git checkout -- pages/gaps.log`。（与第十六拍同坑，第二次踩 ⇒ 已写进 PLAYBOOK P3.53。）

## 三十二、第十七拍门禁（产物定稿后复跑）

| 门禁 | 命令 | 结果 |
|---|---|---|
| 设计门禁 | `verify-design.py ./pages` | **21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`** —— 与基线**逐字节相同** ✓ |
| 语法 | `check-syntax.py pages/*.html` | **10/10 通过** ✓ |
| 字号压平 | `scan-flatten.py mg-work/r108/part108/panel.css` | **2 条**（`.td-mod-bar` / `.td-url`，与基线一致）✓ |
| 六层幂等 | `patch108l1..l6.py` | l1 退出 0 / l2 `0/8` / l3 `0/27` / l4 `0/8` / l5 `0/10` / **l6 `0/15`** + 跨层「全部存活 ✓」 |
| 产物 | `git status` | 只剩 `conversation.html`（`1146 142`）+ `task-detail.html`（`7 0` 存量）+ 5 份 `.workbuddy/memory/*` + 未跟踪 `mg-work/r10*`；`gaps.log` 已还原 |

## 三十三、第十七拍改动清单

| 文件 | 变化 |
|---|---|
| `part108/_mods.html` | 62454 → **70783** 字符（−三枚按钮 + diff 补 46 行） |
| `part108/panel.css` | 74888 → **75956** 字符 |
| `part108/panel.js` | 72477 → **72690** 字符 |
| `part108/browse.html` | 102564 → **106445**（`splice108.py` 产物，非手改） |
| `pages/conversation.html` | 1015095 → **1024705** 字符（`+9610`）／`1146 142` 行／**8500** 行／`sha1_lf` **`cc2105413d08`** |
| `pages/base.html` | **472150 逐字节不变** ✓ |
| `pages/task-detail.html` | **767836 未动** ✓ |

标记核查（`conversation.html` 内）：`r108-conv-css` 1 / `r108-conv-js` 1 / `r108-l5` 1 / `r108-l6` 10（含注释）/
`is-shot` 1、`td-shot-flash` 1（**均在注释里**，代码 0 处）/ `PLACE_ABS` 4 / `av-browse-pane-preview` 3。

取证产物：`ev/p108t.js`（六相位探针）、`ev/probe108t.sh`（全链）+ `ev/probe108t2.sh`（菜单目视）、
日志 `ev/t-raw.log`；截图 `raw/t-menu-4tabs-browse.png`（**菜单左缘对齐 `+`** 的主证据）、`t-menu-full.png`、
`t-menu-1tab.png` / `t-menu-4tabs.png` / `t-menu-fs18.png`（三场景 bar 截图）、
`t-url-after.png` / `t-brw-after.png`（工具条只剩「更多」）、
`t-tree-open.png` / `t-tree-bar.png`（抽屉让开标题栏）、`t-rv-rows.png`（diff 加长后的审查全貌）、
现状基线 `ev/s-raw.log` + `raw/s-menu-before.png` / `s-menu-after.png`（**偏移 218px 的复现证据**），
回滚基线 `ev/bak17/`。

## 三十四、第十七拍交接

- 本拍 = **r108 第六层补丁 `ev/patch108l6.py`**（15 步）。r108 **仍未提交**（`HEAD == origin/main == 9c09afa`）。
- ★ 改序仍是下→上：`part108/{_mods.html,panel.css,panel.js}` → `ev/splice108.py` → `apply108.py`；
  `part108/browse.html` 是 splice 的产物、不是手改对象。
- ★★ **l6 的 `CSS_TAIL` 把 `/* r108-l6 */` 插在 `/* r108-l5 */` 之前并把 l5 原样接回** ⇒ 若再叠 l7，
  同样要「插在 `/* r108-l6 */` 之前 + 把它接回」（六层各自复跑都要能命中自己的标记，§三十二）。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*`，
  还要 **`git reset -q -- mg-work/r108/ev/bak1[3-7]*`**；`part108/`、`raw/`、`ev/` 照旧入库。
- ★ **别忘 `git checkout -- pages/gaps.log`**（§三十一·8）。
- ★ 记忆同步（第十七拍）= `ev/doc108s.py`；PLAYBOOK 追加 P3.53，要点见 §三十一 八条。

## 三十五、第十八拍逐条落地（r108 第七层补丁 · 四条）

邵先生原话（逐字）：

> 「1、"td-mod-bar"右侧的按钮"在系统打开"需要拆分为两个按钮，分别是：另存为、打开所在文件夹；
>   2、把"td-browse-bar"栏的"最大化侧栏"按钮去掉；
>   3、"td-mod-body td-rv-body is-worddiff"容器不能滚动页面，需修复；
>   4、把菜单"td-mod-menu giencoder-dropdown-popup giencoder-popup-open"里的"摘要"放在第一个」

代数体位：`HEAD == origin/main == 9c09afa`，r108 **仍未提交** ⇒ **就地返工、不另起代数**，
本拍 = **第七层补丁 `ev/patch108l7.py`**（9 步）。

### ① `在系统打开` → `另存为` + `打开所在文件夹`

- 落点：`part108/_mods.html`（preview 模块 `.td-mod-bar-acts`）+ `part108/panel.js`（处理器）。
- 原一枚 `data-td-prev-open="1"` **语义过载**（分不清「另存一份」还是「在文件管理器里定位」）
  ⇒ 按邵先生给的命名拆成两枚 `.td-prev-btn`。仍是**静态演示**（各给一句轻提示），不引入真实文件调用。
- **实测（1440）**：`barActs = [["button","td-prev-btn","另存为",…,"1",null],
  ["button","td-prev-btn","打开所在文件夹",…,null,"1"]]`
  · 另存为 `[1223,100,69,26]`、打开所在文件夹 `[1298,100,121,26]`
  · 栏 `[792,93,639,40]` ⇒ 右缘 1419 = 栏内容右缘（12 内距）**正好贴齐**；两枚间距 6（继承 `.td-mod-bar-acts` 的 gap）
  · **栏高仍 40**（未把工具条顶高）；两枚同为 26px 高 ✓
- 改前对照：`barActs = [["button","td-prev-btn","在系统打开","1",null,null]]`，盒 `[1324,100,95,26]`。

### ② 去掉 `td-browse-bar` 的「最大化侧栏」按钮

- 落点：`part108/_head.html` —— ★ 该文件原是 **r107 的资产**，按硬规则「要改跨代资产 ⇒ 放**本代同名覆盖件**」，
  先 `cp part107/_head.html part108/_head.html` 再改；**`part107/_head.html` 一字未动**。
  同时 `ev/splice108.py` 的头部来源由 `P107` 改到 `P108`（并加硬失败保护，避免「静默用了旧头部」）。
- **顺带清掉整段不可达 JS**：按钮是唯一入口 ⇒ 删掉后 `panel.js` 的「最大化 / 还原」整段
  （`freeW` / `maxPanelW` / `applyMaxW` / `storedPanelW` / `setMaxIcon` / `setMax` + 按钮 click +
  分栏条 `pointerdown` 捕获 + `resize` 两条监听，删 4039 字符）全部不可达 ⇒ 一并删除；
  只为它声明的 `DEF_PANEL / MIN_PANEL / MAIN_MIN / STORE_KEY` 也清掉。
- **判据支撑（删前先查全仓）**：`data-td-maxw` **只有本文件**读 —— `pages/`、各 `part` 目录、
  全部 css / js / py 里都没有第二个消费者。★ 另确认 `ctrl-conv.js` 自己也有一份
  `freeW / maxPanelW / MIN_PANEL / DEF_PANEL`，但它在**自己的 IIFE 里**、与此无关 ⇒ 删本文件那份不影响它。
- **实测**：`browseActs = ["收起侧栏"]`、`maxBtn = 0`、`aria-label="最大化侧栏"` 0 处；
  目视 `raw/u-before-bar.png`（`[⤢][×]`）→ `raw/u-after-bar.png`（只剩 `[×]`）。

### ③ 修 `td-mod-body td-rv-body is-worddiff`「不能滚动」

- **根因（先取证再下结论）**：`.td-rv-body` 是 `display:flex; flex-direction:column`，而卡片
  `.td-diff` **没写 `flex`** ⇒ 吃默认 `flex: 0 1 auto`（**可收缩**）⇒ 装不下时浏览器**先压扁卡片**
  而不是让它溢出；而 `.td-diff { overflow: hidden }` 又把压扁后多出来的部分**裁掉**。两个后果：
  1. `scrollHeight` 恒等于 `clientHeight` ⇒ **容器永远不滚**；
  2. 被裁掉的部分（合计约 **489px**）**永久看不见**，也没法滚出来。
- **改前实测（1440×900，四张卡片全展开）**：`bodySz = [757,757]`、`bodyScrollable = 0`；
  逐卡 `[实占高, clientHeight, scrollHeight]` = `[371,369,637] / [264,262,451] / [41,39,67] / [41,39,67]`
  ⇒ 卡 1 内容实需 637 却只占 369。`document.scrollingElement` 溢出 0（整页本来就没滚，
  问题是**容器也不滚 + 内容被裁**）。
- 修法：`.td-rv-body > .td-diff { flex: none; }`（只命中审查模块的直接子件，不动其它 `.td-mod-body`）。
- **改后实测**：`bodySz = [757, 1212]`（**scrollHeight 1212 > clientHeight 757**）；
  `cardFlex = "0 0 auto"`（grow 0 / shrink 0）；逐卡 `[639,637,637] / [453,451,451] / [40,38,38] / [40,38,38]`
  ⇒ `clientHeight == scrollHeight`（**不再压扁**）；`body.scrollTop = 9999` ⇒ 落到 **455**
  （= 1212 − 757，真滚到底）；同刻 **`pageScrollTopAfter = 0`**、`docOverflow = 0`（**整页纹丝不动**）。
- 目视：`u-before-rv-top.png` 与 `u-before-rv-scrolled.png` **逐字节完全相同**（滚不动）；
  `u-after-rv-top.png` vs `u-after-rv-scrolled.png` **不同**（能滚）；改后底部截图能看到此前
  被裁掉的尾部（卡片 1 的 106~138 行、卡片 2 全部 15 行、卡片 3/4）。

### ④ 菜单里「摘要」放到第一项

- 落点：`part108/_head.html`（`.td-mod-menu` 的 5 条 `[data-td-open-mod]`）。
- **实测**：改前 `["审查","终端","浏览器","文件","摘要"]`（y 98/132/166/200/234）
  → 改后 `["摘要","审查","终端","浏览器","文件"]`（y 98/132/166/200/234）。
- 目视：`raw/u-before-menu.png`（摘要在最下）→ `raw/u-after-menu.png`（摘要在最上）；
  菜单盒 `[1160,91,168,182]` 不变（高度没变，只是顺序变了）。

## 三十六、第十八拍排掉的坑（九条）

1. ★★★ **注释正文里写 `part*/` ⇒ 那个 `*/` 提前闭合块注释**，后面的注释正文被当成 JS 代码 ⇒
   `check-syntax` 直接 FAIL（报在「注释行」上，看起来不可能出错）。本轮真踩：
   「已 `grep` 过 `pages/` / `part*/` …」。与硬规则 6「CSS 注释禁嵌 `/* */`」同族。
   ⇒ **判据：`/*` 与 `*/` 计数必须配平**（多出来的那一个 `*/` 就是元凶），已写进 l7 的收尾自检。
2. ★★★ **「存在性」断言抓不到「重复应用」** —— ③ 的 `mark` 写成 `/* r108-l7 ③`，
   而实际注释是 `/* ★ r108-l7 ③`（中间多了个「★ 」）⇒ mark **永不命中** ⇒ 补丁被**重复应用**
   （`panel.css` 多出整整一份 799 字符的重复块），而当时的「存在 `flex: none`」断言**照样通过**。
   ⇒ 同一条判据一律写成 **`count == 1`**（本轮改成 count 后立刻抓到）。
3. ★★ **纯删除类改动的 mark 必须「终态里仍在、中间态才有」两头都算清** —— ④ 第一版拆成
   「先摘掉那一行、再插到标题后」两步：单跑没问题，**复跑直接 `mark` 歧义**（终态里
   mark「标题紧跟摘要」与第 (a) 步的 `old`「摘要那一行」**同时存在**）。⇒ **能一次整块重排就别拆两步**；
   拆了就必须保证「中间态才成立的 mark 在终态消失」。
4. ★★ **`old` 被 `new` 原样保留时必须 `strict=False`** —— ③ 的 `new` = 原 `.td-rv-body{...}` 块
   原样接回 + 追加新规则 ⇒ 复跑时 `old` 必然仍在、与 mark 同时命中。与 l5、l6 同类豁免（第三次了）。
5. ★★★ **改了跨代资产的下游生成器要跟着改来源** —— `_head.html` 原本由 `splice108.py` 从
   **part107** 读；若只 `cp` 覆盖件而不改读取路径，本代的两处改动**根本不会进产物**（且不报错）。
   ⇒ 同时加「缺覆盖件就硬失败」的保护，避免静默退回旧件。
6. ★★ **删组件后「整段被删的功能」要连带清** —— 但**删除范围要有判据**：先证「`data-td-maxw`
   全仓只有本文件读」，再删；并显式区分「本文件那份」与「宿主 `ctrl-conv.js` 自己 IIFE 里的那份同名
   函数」（同名不代表同物）。
7. ★★ **下游守卫的判据别写裸属性名** —— `splice108.py` 里 `'data-td-max' in out` 被
   `_mods.html` 的 **demo diff 文本**（逐字展示 `&lt;button … data-td-max="1"&gt;`）误报。
   ⇒ 判据取「真按钮」的整段特征（`<button class="td-browse-ico" … aria-label="最大化侧栏"`）。
   与硬规则「判据要剥注释」同族：**先想清楚这个串会不会出现在「示例文本 / 注释」里**。
8. ★★ **重建「改前」页面做对照时，三件必须齐上** —— 只换 `browse.html` 而留着新版 `panel.css`/`panel.js`，
   得到的是**混合态**（1022451），不是真 pre-l7（1024705）；`gaps.log` 的对照也会因此失效。
   ⇒ 真 pre-l7 = `browse.html` + `panel.css` + `panel.js` 三件一起换回（本轮三件齐上后**精确复现 1024705**）。
9. ★ **截图前必须先把侧栏滑进视口** —— 侧栏初始 `translateX` 收在视口右外，此时几何量「正确」但
   截图全空（`u-after-bar.png` 第一版只有 276 字节的空白图）。⇒ 先 `openTabs`（开一个模块）
   再截。与「量到了 ≠ 看得见」同族。

## 三十七、第十八拍门禁（产物定稿后复跑）

| 门禁 | 结果 |
|---|---|
| `check-syntax.py pages/*.html` | **10/10 通过** ✓（第一版因坑 1 曾 9/10） |
| `verify-design.py ./pages` | 76 个问题（66 warning / 10 info / **0 critical**）；与第十七拍**同为 76** ✓ |
| `gaps.log` 真 pre-l7 vs 真 post-l7 | **逐字节相同**（md5 `81fb5522ffd1f97524c21819df7770fc`）⇒ **l7 零 token 缺口回归** ✓ |
| `scan-flatten.py part108/panel.css` | **2 条**（`.td-mod-bar` / `.td-url`，与基线一致）✓ |
| `patch108l7.py` 幂等 | 第一遍 **应用 9 / 跳过 0**；复跑 **应用 0 / 跳过 9** ✓ |
| 画质自检（新增） | `panel.js` `/*` 94 / `*/` 94、`panel.css` `/*` 141 / `*/` 141 **配平** ✓ |
| 全链可复现 | 以 `ev/bak18pre/`（pre-l7）重跑 l7 → 四件 md5 与 `ev/bak18/` **逐字节一致** ✓ |
| 版面回归 | pre-l7 页面 **精确复现 1024705** → post-l7 **1022257**（Δ = −2448）✓ |

## 三十八、第十八拍改动清单

| 文件 | 体积 | 改动 |
|---|---|---|
| `part108/_head.html`（**新建**，由 `part107/_head.html` 逐字拷贝后打两处） | 5416 → **4918 bytes** | ② 删「最大化侧栏」按钮；④ 菜单 5 项整块重排（摘要提前） |
| `part108/_mods.html` | 70783 → **71067 字符** | ① 一枚「在系统打开」→ 两枚（`data-td-prev-save` / `data-td-prev-reveal`）+ 留痕注释 |
| `part108/panel.css` | 75956 → **76769 字符** | ③ `.td-rv-body > .td-diff { flex: none; }` + 19 行说明注释；`/* r108-l7 */` 插在 l6 之前并接回 |
| `part108/panel.js` | 72690 → **69623 字符** | ① 两枚处理器（替换原一枚）；② 删「最大化 / 还原」整段（−4039 字符）+ 留痕注释 + 头注释同步 + 清 4 个宽度常量 |
| `part108/browse.html`（splice 产物） | 106445 → **106251 字符** | 头部 5270 → 4792；模块 70783 → 71067 |
| `ev/splice108.py` | — | 头部来源 `part107` → `part108/_head.html`（缺则硬失败）+ 两条第十八拍守卫（真按钮特征 / 菜单顺序） |
| `ev/patch108l7.py`（**新建**，约 430 行 / 9 步） | — | 四条落地 + 跨层兜底 + 注释配平自检 |
| `pages/conversation.html`（产物） | 1024705 → **1022257 字符**（−2448）/ **8442 行** | 对 `HEAD` 累计 **`1186 / 239`** 行；工作区 bytes 1141453 / `sha1_lf` **`f3e0bcc1a8e2`** |
| `pages/base.html` | **490294 bytes 逐字节不变** ✓ | — |
| `pages/task-detail.html` | **831606 bytes 未动**（`7 0` 存量差）✓ | — |

标记核查（`conversation.html` 内）：`r108-l7` 7 / `r108-l6` 10 / `r108-conv-css` 1 / `r108-conv-js` 1 /
`PLACE_ABS` 4 / `data-td-prev-save` 2 / `data-td-prev-reveal` 2 / **`data-td-prev-open` 0** /
`.td-rv-body > .td-diff { flex: none; }` 1 / 真按钮 `aria-label="最大化侧栏"` **0**。
⚠ `data-td-max` 在页面里仍有 **2** 处 —— 都在 **demo diff 文本**里（转义后的示例代码，按「不改不必涉及」
保留；见 §三十九 交付说明）。

取证产物：`ev/p108u.js`（十相位探针：base / menuOpen / menuRead / menuClose / openTabs / rvOpen /
rvRead / rvScroll / pvOpen / pvRead）、`ev/p108u2.js`（压扁假设专项）+ `ev/probe108u3.sh` + `ev/chk18{,b,c}.py`（落盘复核）、
`ev/probe108u.sh` / `ev/probe108u2.sh` / `ev/probe108u3.sh` / `ev/shots108u.sh`、
日志 `ev/u-raw.log`（改前）/ `ev/u-after-raw.log`（改后）/ `ev/tmp/g-{pre,post}.log`；
截图 `raw/u-{before,after}-{menu,bar,pvbar,rv-top,rv-scrolled}.png` + 各自的 `.td-browse` 全侧栏版；
回滚基线 `ev/bak18/`（post-l7）+ `ev/bak18pre/`（pre-l7，由 `bak17` + 重跑 l6 精确重建）。

## 三十九、第十八拍交接

- 本拍 = **r108 第七层补丁 `ev/patch108l7.py`**（9 步）。r108 **仍未提交**（`HEAD == origin/main == 9c09afa`）。
- ★ 改序仍是下→上：`part108/{_head.html,_mods.html,panel.css,panel.js}` → `ev/splice108.py` → `apply108.py`；
  `part108/browse.html` 是 splice 的产物、不是手改对象。
- ★★ **l7 的 `CSS_TAIL` 把 `/* r108-l7 */` 插在 `/* r108-l6 */` 之前并把 l6 原样接回** ⇒ 若再叠 l8，
  同样要「插在 `/* r108-l7 */` 之前 + 把它接回」。七层各自复跑都要能命中自己的标记。
- ★★ **`_head.html` 现在是本代的覆盖件**：`ev/splice108.py` 只认 `part108/_head.html`（不存在直接 `sys.exit`）。
  下次改头部 → 直接改这个覆盖件；**别再回头看 `part107/_head.html`**（那已是历史快照）。
- ★ 遗留（**本拍有意保留、未动**）：demo diff 里那两行把「最大化」按钮当**新增行**展示
  （`+ <button … data-td-max="1">`）—— 按钮已删，这两行演示文本与新状态不一致。按「不得改动不必涉及的
  模块」保留；邵先生若要演示自洽，说一声就改成一行删除态。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*`，还要 **`git reset -q -- mg-work/r108/ev/bak1[3-8]*`**
  （含本拍新增的 `bak18/`、`bak18pre/`）；`part108/`、`raw/`、`ev/` 照旧入库。
- ★ **别忘 `git checkout -- pages/gaps.log`**（`verify-design.py` 每跑必重写它）。
- ★ 记忆同步（第十八拍）= `ev/doc108t.py`；PLAYBOOK 追加 **P3.54**（九条教训）。


## 四十、第十九拍逐条落地（r108 第八层补丁 · 两条）

邵先生原话：

> 「1、整个右栏"td-browse"所以的文本（含代码）被鼠标框选后，都要在上方显示浮动工具条（添加到对话、复制）；
> 2、菜单"td-mod-menu giencoder-dropdown-popup giencoder-popup-open"出现的瞬间会有闪烁或跳动或位移现象，不够自然；」

两者都落在 `part108/panel.js`（**本拍唯一改动的源件**）。

### ① 整个右栏划词都弹浮动工具条

**根因**：划词浮条的放行判据写死了主对话口 ——
`if (!e.target.closest('.r93-scroll')) { selHide(); return; }` ⇒ 右栏里划词**浮条根本不弹**。

**改法**（1 行有效改动 + 注释）：放行根改成「`.r93-scroll` ∪ `.td-browse`」：

```js
var selHost = (e.target && e.target.closest)
  ? e.target.closest('.r93-scroll, .td-browse') : null;
if (!selHost) { selHide(); return; }
```

⚠ 两者是**并列的 flex 兄弟**、互不包含（1440 实测 `.r93-scroll` [13,49,778,604] 与
`.td-browse` [791,48,641,844]）⇒ 不会互相误判；主对话口原有能力一字未动。

**真机取证**（1440×900，CDP 真实鼠标 `move/down/move×3/up`，**不是**合成事件）：

| 模块 | 选中内容（`Selection.toString()`） | 改前 `selbarExists` | 改后 `selbarExists` | 浮条框 | 浮条在选区上方 | 在最上层 | 按钮 |
|---|---|---|---|---|---|---|---|
| 审查（diff 代码） | `'   <aside class="td-browse" aria-label="文件预览">\n89\n−     <span class="td'` | **false** | **true** | `[886,139,200,38]` | **8px** | true | 添加到对话 / 复制 |
| 摘要（散文小字） | `'4 轮 · 12 次工具调用 · 2 分 '` | **false** | **true** | `[835,59,200,38]` | 8px | true | 同上 |
| 文件（代码区 JSON） | `'"snake-game'` | **false** | **true** | `[1120,113,200,38]` | 8px | true | 同上 |

- 「在最上层」= 在浮条中心做 `elementFromPoint()`，命中的是浮条自己的 `SPAN`（没被右栏盖住）。
- 点「复制」后：浮条收起（`selbarHidden = true`）、选区清空 ⇒ 按钮真能用。
- 目视：`raw/w-before-selbar.png`（代码有蓝色选区、**无浮条**）→ `raw/w-after-selbar.png`（选区上方出现两枚按钮）。
- 页签名（`.td-browse-tab`）与文件树行名（`.td-bf`）本来就带 `user-select: none`（它们是「控件」不是「内容」）
  ⇒ 那两处仍拖不出选区，属**既有口径、本拍不动**。

### ② `+` 菜单的入场不再硬切

**根因（本拍最硬的一条）**：`toggleMenu()` 把「摘 `[hidden]`」与「挂开态类」挤在**同一个 tick**。
`[hidden]` 生效时元素是 `display:none` ⇒ 浏览器**拿不到「改前样式」**，于是紧随其后的
`display:none → flex` 那次样式变更里，`opacity / translate / scale` 的过渡被**静默跳过**：

> **契约里那条 0.2s spring 入场从未运行过** —— 菜单是**硬切弹出来**的（用户看到的「闪烁 / 跳动 / 不够自然」）。

真机 rAF 逐帧采样（关态采 4 帧 → 第 5 帧点开 → 再采 30 帧），改前：

```
 4 click  disp=flex  vis=visible  op=1  tr=0px  sc=1  off=(368,42)  anims=-
 5..33    （此后全程恒等于终态，getAnimations() 恒为空）
```

**改法**（开的那一侧拆四步；`placeRv` 挪到挂类**之前** ⇒ 零位移）：

```js
menu.removeAttribute('hidden');   /* ① display:flex + 基态（op 0 / vis hidden / tr 0 4px / sc .96） */
void menu.offsetWidth;            /* ② 强制重排 —— 逼浏览器把「改前样式」记账 */
placeRv(menu, trigger);           /* ③ 位置在「第一帧可见」之前定好 ⇒ 零位移 */
menu.classList.add(POP_OPEN);     /* ④ 过渡正常起跑 */
```

**改后同一条采样链**：

```
 4 click  disp=flex vis=visible op=0        tr=0px 4px    sc=0.96  off=(368,42)  anims=opacity|scale|translate
 5 post                          op=0.188273 tr=0px 2.6225px sc=0.973775        anims=opacity|scale|translate
 6 post                          op=0.425908 tr=0px 1.54521px sc=0.984548
 …
11 post                          op=0.96233  tr=0px -0.390444px sc=1.0039   ← spring 过冲
15 post                          op=0.999054 tr=0px -0.0353153px sc=1.00035
16 post                          op=1        tr=0px        sc=1      off=(368,42)   anims=-
```

- **零位移**：`off=(368,42)` 从「点开那一帧」到最后一帧**逐帧不变**。
- 入场自然：约 12 帧 ≈ 0.2s，带 spring 回弹（`scale` 到 `1.0039`、`translate` 到 `−0.39px` 再回落）。
- 关态语义未变：仍是 `[hidden]` ⇒ `display:none`（Esc 分层、连点重开这些路径都靠它当**唯一状态位**）。

同页 A/B 对照（`ev/r108v3.js`，两例只差那一行强制重排）：

| | `getAnimations()` | 首帧 computed |
|---|---|---|
| A 旧写法 | **`[]`** | `opacity:1 / translate:0px / scale:1`（一帧到终态） |
| B 两步写法 | `opacity:running · scale:running · translate:running` | `opacity:0 / translate:0px 4px / scale:0.96` |

**四枚下拉一起生效**（同一条代码路径、同一段 CSS 过渡）——「点开即读」实测（同一 eval 内点开 + 读）：

| 菜单 | `getAnimations()` | 打开帧 `opacity` | 触发器下缘 → 菜单上缘 |
|---|---|---|---|
| `.td-mod-menu`（`+`） | `opacity\|scale\|translate` | 0（`scale` 0.96） | **7px** |
| `.td-rv-scope-menu`（对比范围） | `opacity\|scale\|translate` | 0 | 6px |
| `.td-commit-menu`（提交·推送） | `opacity\|scale\|translate` | 0 | 6px |
| `.td-rv-opts`（显示选项） | `opacity\|scale\|translate` | 0 | 6px |

⇒ 位置口径（触发器下方 6px，`.td-mod-menu` 因取整为 7）与 l6 / 第十拍完全一致，**没有被这次时序改动带偏**。

### 回归重测（改了 `toggleMenu` 的时序 ⇒ 依赖它的旧路径全量重跑）

| 路径 | 结果 |
|---|---|
| Esc 分层 | Esc 前 `openMenus=["td-rv-menu"]` + `sidebarOn=true`；Esc 后 `openMenus=[]` + **`sidebarOn=true`**（侧栏**未**被连坐关掉）✓ |
| `+` 菜单选「终端」 | `activeTab="terminal"`、`visiblePanes=["terminal"]`、`allMenusClosed=true` ✓ |
| 右键菜单 `.td-ctxmenu` | 仍可开（`box [841,194,168,193]`、`visibility: visible`）✓ —— 走的是另一个函数 `ctxShow()`，本拍未动 |
| 收起侧栏 | `sidebarOn=false`、`.td-browse` 回到 `[1432,48,641,844]` ✓ |
| 页签切换 / 四枚下拉能开能关 | ✓（`closeAll` 后 `.giencoder-dropdown-popup` 开着的有 **0** 枚） |


## 四十一、第十九拍排掉的坑（六条）

1. ★★★ **「摘 `[hidden]`（`display:none`）+ 挂开态类」同一 tick ⇒ CSS 过渡被静默跳过**。
   `display:none` 时浏览器**没有「改前样式」可比** ⇒ 那一次样式变更里的过渡**不会跑**，
   而且**不报任何错**（`getComputedStyle` 直接给终态，看着"一切正常"）。
   ⇒ 声明的入场动画完全可能是**死代码**。判据 = ① 逐帧 `getAnimations()`（空 = 没跑）；
   ② 打开那一帧读 computed（拿到终态 = 没跑）。修法 = 中间**加一次强制重排**（读 `offsetWidth`）。
2. ★★ **断言必须限定在「函数体内」**：`      menu.setAttribute('hidden', '');` +
   `      menu.classList.remove(POP_OPEN);` 这个形状在 `panel.js` 里出现 **2 次**
   （另一处是 `.zd-menu` 的 `placeZdMenu()`）⇒ 全文计数会把「本拍有意保留的另一处」
   误报成「结构被改动」。**同型：** `      menu.removeAttribute('hidden');` +
   `      menu.classList.add(POP_OPEN);` 也是 2 处。
3. ★★ **注释不能插在「被逐字断言的代码序列」中间**：第一版把 ② 的长注释放在
   `menu.removeAttribute('hidden');` 与 `void menu.offsetWidth;` **之间** ⇒
   「四步连续序列」的断言必然落空（而补丁本身是对的）。
   ⇒ 要么把注释整体挪到序列**之前**，要么断言改成「四步分四条各查一次」。
4. ★★ **`old` 被 `new` 原样保留 ⇒ `strict=False`**（文件头第 ⑥ 条那一行原样接回 + 追加第 ⑦ 条）。
   这是**第四次**踩「原样接回」（l5 / l6 / l7 各一次）。**只要 `new` 里含 `old` 就必须显式放开**，
   否则复跑时 `old` 与 `mark` 同时命中 → 被误判「mark 歧义」→ 直接 `sys.exit`。
5. ★★ **判据要跟着事实走**：文件模块的正文**不叫** `.td-mod-body`，而是从 r105 逐字剪出来的
   `.td-browse-body`（左「文件树」+ 右「代码区」`.td-browse-code` / `.td-browse-pre` / `.td-code-tx`）
   ⇒ 探针选择器写错只得到 `pick: null`，看着像「拖不出选区」的**假失败**。**先核 DOM 再写探针**。
6. ★ **「改前对照页」不能沿用上一轮的 `bak18/`**：它是**混合态**（`browse.html` 是 pre-l7、
   `panel.js` 却是 l7 改到一半的版本）。本轮另立 `ev/bak19/`（四件 part + `conversation-pre-l8.html`）
   当唯一基线；**对照基线要"整代快照"，不要"能跑就行"**。


## 四十二、第十九拍门禁（产物定稿后复跑）

| 门禁 | 结果 | 基线 |
|---|---|---|
| `check-syntax.py pages/*.html` | **10/10 通过** | 同基线 |
| `verify-design.py ./pages` | **76 个问题**（66 warning / 10 info / **0 critical**） | 与 l7 完全一致 |
| `pages/gaps.log` | md5 **`81fb5522ffd1f97524c21819df7770fc`** | **= l7 基线 ⇒ 零 token 缺口回归** |
| `patch108l8.py` 幂等 | 第一遍 **4 应用 / 0 跳过**；复跑 **0 应用 / 4 跳过** | ✓ |
| 注释括号配平 | `panel.js` `/*` **96** / `*/` **96** | ✓（l7 真踩过：注释正文里的 `*/` 会提前闭合块注释） |
| 源件未牵连 | `part108/{panel.css,_mods.html,_head.html,browse.html}` md5 与 `ev/bak19/` **逐个相同** | ✓ |

`gaps.log` 收尾已 `git checkout` 还原（`verify-design.py` 每跑必重写它）。


## 四十三、第十九拍改动清单

| 文件 | 变化 | 说明 |
|---|---|---|
| `mg-work/r108/part108/panel.js` | 69623 → **72191 字符**（LF；1595 → **1639** 行） | **本拍唯一改动的源件**：① 放行根 + 段落头 + 文件头第 ⑦ 条；② 开态四步 |
| `mg-work/r108/part108/panel.css` | **一字未动** | 本层不碰 CSS ⇒ 不新增 `/* r108-l8 */` 标记 |
| `mg-work/r108/part108/{_head.html,_mods.html,browse.html}` | **一字未动** | ⇒ 无需重跑 `ev/splice108.py` |
| `pages/conversation.html`（产物） | 1022257 → **1024825 字符**（+2568）/ **8487 行** | 对 `HEAD` 累计 **`1234 / 242`** 行；工作区 bytes 1145785 / `sha1_lf` **`2c1ed815740e`** |
| `pages/base.html` | **逐字节不变** | `apply108.py` 报「已是目标态」 |
| `pages/task-detail.html` | **未动** | 仍是存量 `7 0` |
| `mg-work/r108/ev/patch108l8.py` | 新增 | 第八层补丁（4 步 + 跨层断言） |
| `mg-work/r108/ev/{r108v-recon.js,r108v2.js,r108v3.js,p108w.js,p108x.js}` | 新增 | ② 逐帧采样 / A-B 对照 + ① 真鼠标拖选 + 回归重测 |
| `mg-work/r108/ev/probe108v{,2,3}.sh` · `probe108w.sh` · `probe108x.sh` · `shots108v.sh` | 新增 | 探针与截图驱动 |
| `mg-work/r108/ev/bak19/` | 新增 | **pre-l8 整代快照**（四件 part + `conversation-pre-l8.html`） |

标记核查（`conversation.html` 内）：`★ r108-l8 ①（邵先生：` **1** / `★★ r108-l8 ②（邵先生：` **1** /
`★ r108-l8 ① 扩容` **1** / `⑦ 通用：划词浮条` **1** / `void menu.offsetWidth;` **1** /
`.closest('.r93-scroll, .td-browse')` **1** / **`.closest('.r93-scroll')` 0** /
`r108-l7` 7 / `r108-l6` 10 / `data-td-prev-save` 2。

取证产物：`ev/r108v-recon.js`（侦察）、`ev/r108v2.js` + `ev/probe108v2.sh`（② rAF 逐帧，改前/改后各一轮）、
`ev/r108v3.js` + `ev/probe108v3.sh`（② A/B 对照：现状写法 vs 两步写法）、
`ev/p108w.js` + `ev/probe108w.sh`（① CDP 真鼠标拖选，改前/改后各一轮）、
`ev/p108x.js` + `ev/probe108x.sh`（回归重测：四枚下拉 / Esc 分层 / 切模块 / 右键菜单 / 收侧栏 / 切页签）、
日志 `ev/{v-before-raw.log,v2-before-raw.log,v2-after-raw.log,v3-raw.log,w-before-raw.log,w-after-raw.log,x-after-raw.log}`；
截图 `raw/w-{before,after}-selbar.png` · `raw/w-after-files-selbar.png` · `raw/v-after-menu.png` ·
`raw/x-after-{after-esc,ctx}.png`。


## 四十四、第十九拍交接

- 本拍 = **r108 第八层补丁 `ev/patch108l8.py`**（4 步）。r108 **仍未提交**（`HEAD == origin/main == 9c09afa`）。
- ★ **本层只改 `panel.js` 一件**（不改 CSS / 不改 HTML）⇒ **不必重跑 `ev/splice108.py`**，
  直接 `python mg-work/r108/apply108.py` 即可落盘（`part108/browse.html` 里没有 panel.js 的内容）。
- ★ 本层**不新增 CSS 标记**（没碰 `panel.css`）；层痕迹是 `panel.js` 里的
  `★ r108-l8 ①（邵先生：…` / `★★ r108-l8 ②（邵先生：…` 两条留痕注释。
  若将来再叠 l9，同样「注释留痕 + 标记插在上一代之前」的体位。
- ★★ **关的那一侧本拍有意不动**：仍是「摘 `POP_OPEN` + 置 `[hidden]`」⇒ 立即 `display:none`（无退场动画）。
  理由：`[hidden]` 是 Esc 分层、连点重开这些路径的**唯一状态位**，加退场延迟会与它们抢时序。
  若邵先生要「退场也淡出」，那是一次**独立**的会话（要给 `hidden` 加 token + `setTimeout` 兜底 + 连点竞态处理）。
- ★ 遗留（**本拍有意保留、未动**）：另有两处**同型入口缺陷**——右键菜单 `ctxShow()` 与
  `.zd-menu` 的 `placeZdMenu()`，同样是「摘 `[hidden]` + 挂类」同一 tick ⇒ 它们的入场也仍是硬切。
  按「不得改动不必涉及的模块」保留；要对齐说一声即可（各 1 行强制重排）。
- ★ 上拍遗留仍在：demo diff 里那两行把「最大化」按钮当**新增行**展示（`data-td-max="1"`）。
- ★ 提交时除 `git reset -q -- mg-work/r107/ev/bak*` 与 `mg-work/r108/ev/bak1[3-8]*`，
  还要 **`git reset -q -- mg-work/r108/ev/bak19`**。
- ★ **别忘 `git checkout -- pages/gaps.log`**（`verify-design.py` 每跑必重写它）。
- ★ 记忆同步（第十九拍）= `ev/doc108u.py`；PLAYBOOK 追加 **P3.55**（六条教训）。

