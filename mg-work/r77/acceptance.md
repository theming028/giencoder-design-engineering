# r77 验收报告 · 六项需求

> 日期：2026-09-29 ｜ 范围：9 页 HTML + DS 2 源 ｜ 补丁：`mg-work/r77/apply77.py`、`apply77b.py`（均幂等）
> 基线：`mg-work/r77/before/*.html`（9 页）+ `mg-work/r77/before/ds/*.css`
> 口径：全部**实机取证**（`file://` 直开 + `agent-browser`），无一处凭推断。

---

## 一、逐项结论

### 需求 1 · aside「更多」图标的下拉菜单补动效 ✅

**取证定位**：aside 里唯一的「更多」图标 = 会话项行 hover 时出现的 `⋯`
（`.session-menu-trigger`，点击后 `createPortal` 弹出 `[role="menu"][aria-label="会话操作"]`）。
9 页的 aside 都有它，但 **只有 base.html 有进场动效**（第 74 轮配的 `r74-pop-in`），
其余 4 页（automation / avatar / skills / task-detail）**完全没有** —— 弹出是「啪」地出现。

| 页 | 改前 | 改后 |
|---|---|---|
| base.html | `r74-pop-in` ✓ | 不动（已具备） |
| automation / avatar / skills / task-detail | `animationName: none` | `r77-pop-in / 0.16s` ✓ |

**实测**（4 页，点击后 25ms）：
```
automation   r77-pop-in/0.16s | op=0.242 | translate=0px 3.03px | scale=0.977
avatar       r77-pop-in/0.16s | op=0     | translate=0px 4px    | scale=0.97
skills       r77-pop-in/0.16s | op=0.243 | translate=0px 3.03px | scale=0.977
task-detail  r77-pop-in/0.16s | op=0.243 | translate=0px 3.03px | scale=0.977
```
参数与 base 的 `r74-pop-in` **完全一致**（淡入 + 下移 4px 复位 + 0.97 微缩放，160ms，
`cubic-bezier(0.34,0.69,0.1,1)`）。关键帧另起名 `r77-pop-in`：这 4 页没有 r74 段，重名会让
「本页已应用」的判据与其它轮次混淆。

### 需求 2 · td-left / td-right 描边色 = #DAE3ED ✅

- **改前**：`border: 1px solid var(--td-panel-line)` ⇒ `--td-panel-line: #ECEEF2`
  （第 70 轮为了「与主区那一档色一致」把两处原本的 #DAE3ED 改掉了）
- **改后**：新增本页 token `--td-pane-line: #DAE3ED`，`td-left` / `td-right`（含浏览态右缘两条端点规则）改走它
- **实测 computed**：`.td-left` / `.td-right` 四边 **`rgb(218, 227, 237)`** = #DAE3ED，宽度 1px ✓
- `--td-panel-line` 仍是 `#ECEEF2`（**未动**）⇒ `.td-browse`（文件预览栏，浏览态才出现）保持原样

**DS 无该色 token**（全库 grep `#DAE3ED` / `rgb(218,227,237)` 零命中）⇒ 按本页既有惯例
（同 `--td-appbar`、`--td-ico-gray`）落成本页 token，不硬编码在规则里。

### 需求 3 · 版权区「内容由 AI 生成…」放最下面 ✅

**这里踩到一个隐藏机制**：第 74 轮为了把版权区改成三行，用了**运行时脚本**（`<script id="r74-base-js">` ①段）——
它抓版权区**最后一个 `<p>`**，把它覆盖成「© 2026 中电金信」再 `appendChild` 一行「中电金信研究院 · …」。
r74 当时 React 源码顺序是 `[AI 提示句, © 一整行]`，所以拆完正好三行。

我第一版只改了 **React 源码顺序**（→ `[© 一整行, AI 提示句]`），结果脚本仍抓「最后一个 p」——
那正是 AI 提示句 ⇒ **整句被吃掉**，实测渲染成「© … 版本：1.2.5 / © 2026 中电金信 / 中电金信研究院 · …」三行重复版权。

**修法**（`apply77b.py`）：把脚本①段改成抓**第一个 `p`**（© 那一整行）来拆，
新行用 `insertBefore(p2, first.nextSibling)` 插在它紧后面 ⇒ 提示句自然落到最下，
r74「© 拆两行」的版式保持不变。

**实测 DOM**（`file://` + React 渲染 + 脚本执行后）：
```
0: "© 2026 中电金信"                                      [data-r74-cr]
1: "中电金信研究院 · 数字构建平台实验室（PAA） · 版本：1.2.5"  [data-r74-cr]
2: "内容由 AI 生成，请核实重要信息"
```

### 需求 4 · 波点密度「稍微密一点」 ✅

网格间距 **20px → 16px**（密度 400px²/点 → 256px²/点，点数 ×1.56）。
波点由**三层**构成，必须同改才能保持点阵逐点对齐：
① `.dot-bg` 浅点阵（浅色主题 + `[giencoder-theme='dark']` 各一条）；
② `.dot-bg::before` 深一档点阵（指针光斑照亮那层）；③ `.r74-ripple` 涟漪点阵层。

**实测**：
- computed `background-size`：`main.dot-bg` = **16px 16px**、`.dot-bg::before` = **16px 16px** ✓
- 深色主题（`giencoder-theme='dark'`）同样 **16px 16px** ✓（该条选择器特异性 0-2-0，必须原样带前缀才压得住）
- 截图上「一行像素里相邻暗点的间距」**中位数：20.00px → 16.00px** ✓（逐像素量化，非目测）
- 点径（1.5px）与点色（`gray-7@0.1` / `gray-8@0.22`）**一律未动** —— 只收紧间距

### 需求 5 · 涟漪「不置于对话框之上」+「至少减半」 ✅

两个独立子项，分别取证。

**(a) 层级：对话框最高。** 第 76 轮把涟漪提到 `z-index: 10`（画在内容之上）；
本轮还原成 **`z-index: 0`**（第 74 轮原值）。涟漪由页尾脚本 `insertBefore(el, host.firstChild)`
插在 `main` 最前 ⇒ 与内容同属 `z-index:auto` 组时按 tree order 天然压在内容之下。

**实测（点对话框正中心）**：

| 区域 | ≥6 变化像素 | 峰值 | 平均差 |
|---|---|---|---|
| 对话框区（420,376–1280,590） | **0** | 1 | 0.0003 |
| 对话框外 | 5545 | 105 | 0.1693 |

⇒ 涟漪**完全被对话框盖住**，一点都没透上来 ✓

**(b) 强度减半。** 点色 α `0.62 → 0.28`（gray-9 不变），点径 `1.8 → 1.7px`；
环带形态（第 76 轮那套 `max(比例×r, r−固定值)` 的整流 mask）与 300ms 时长不动。

**A/B 同口径实测**（同一脚本 / 同一点击点 `main 左80·下60` / 同一 t=160ms / 1440×900；
A = `mg-work/r77/before/base.html`（r76 版），B = 当前 `pages/base.html`）：

| 口径 | A（r76 版） | B（r77 版） | B/A |
|---|---|---|---|
| **环带自身亮度 Δ**（对话框外环带像素） | 76.8 | **35.5** | **46.2%** |
| 环上逐点 Δ | 79.2 | 37.6 | 47.4% |
| 全画幅平均差 | 0.1430 | 0.1045 | 73.1% |

⇒ **环带本身的明暗对比降到 46%（恰好减半）** ✓ 满足「至少减半」。

⚠️ **「全画幅平均差」只有 73% 是错觉**：需求 4 把波点网格从 20px 收到 16px，
涟漪点阵**同步加密**（三层同改是对齐的前提），单位面积亮点数量 ×1.56，
把 α 的削弱抵消掉一部分 ⇒ 总**覆盖像素更多**、但**每点更淡**。
「亮不亮」看环带亮度（46%），「铺多大」看环带半径（cap 仍 480px，未动）。

### 需求 6 · 滚动条 hover 再浅一级 ✅

`.20 → .16`，**4 类锚点全改**：

| 锚点 | 位置 | 改动 |
|---|---|---|
| ① 全局内联规则 | 9 页 `::-webkit-scrollbar-thumb:hover{...rgba(var(--gray-10), .20)}` | → `.16` |
| ② task-detail 局部变量 | `--scrollbar-thumb-bg-hover: rgba(0,0,0,0.20)` | → `0.16` |
| ③ avatar 卡内规则 | `.av-card .giencoder-card-body::-webkit-scrollbar-thumb:hover` | → `0.16` |
| ④ DS 源 2 文件 | `colors_and_type.css`（规则 + 变量）、`tokens.css`（规则） | → `0.16` |

**级联现证**（base 页，`sb.js`）：
```
默认档（::-webkit-scrollbar-thumb）        rgba(var(--gray-10), .16)   ← 未动
hover 档（@media (pointer:fine)）
   胜出者 ::-webkit-scrollbar-thumb:hover  rgba(var(--gray-10), .16)   ← 胜出
```

**⚠️ 按邵先生拍板**：默认档 `.16` **保持不变** ⇒ hover 与常态同色、**悬停不再有视觉反馈**
（这是我提的两个选项里的第二项，用户明确选择「只降 hover，保留默认」）。
`:active` 档 `.32` 未动（用户未提）。

---

## 二、回归与门禁

**门禁零新增**：`verify-design.py ./pages` **75**（66🟡 / 9🔵 / 0🔴）= `./mg-work/r77/before` **75** ✓
逐条 diff 后唯一差异：
1. base.html `🔵 CRAFT-SLOP` 渐变 `60 → 61`（来自新注入块里涟漪点阵那 1 处 `radial-gradient`；🔵 info、非阻断）
2. task-detail.html 的 `TOKEN-GAP` / `CRAFT-ANIM` **行号整体 +7~+8**（因为 `--td-pane-line` 定义处插了几行注释，
   条目数 **21 → 21 不变**）

**幂等**：`apply77.py`（25 项）+ `apply77b.py`（2 项）复跑两遍 = **应用 0 / 跳过 27**，页面 md5 不变 ✓

**回归检查项**：
- 滚动条**默认档 `.16` 未动** ✓（9 页 + DS 均确认）
- `:active` 档 `.32` 未动 ✓
- `--td-panel-line: #ECEEF2` 未动、`.td-browse` 未被波及 ✓
- base.html 的 `r74-pop-in`（顶栏空间下拉 / 添加内容菜单 / 技能选择面板 / 权限选择）未受影响 ✓
- 涟漪「点控件不起涟漪」（脚本的 `closest('button, a, input...')` 判定）未动 ✓
- 涟漪 `prefers-reduced-motion` 降级（只压时长、保证 `animationend` 能自毁）未动 ✓
- 波点三层网格原点一致（同 `inset:0` + 同 `background-size`）✓

---

## 三、改动文件清单

```
pages/automation.html     需求 1（r77-pop-css）+ 需求 6
pages/avatar.html         需求 1（r77-pop-css）+ 需求 6（全局 + 卡内）
pages/base.html           需求 3（版权区源码 + r74 脚本）+ 需求 4+5（r77-base-css）+ 需求 6
pages/dev.html            需求 6
pages/kanban.html         需求 6
pages/req-kanban.html     需求 6
pages/settings.html       需求 6
pages/skills.html         需求 1（r77-pop-css）+ 需求 6
pages/task-detail.html    需求 1（r77-pop-css）+ 需求 2（--td-pane-line）+ 需求 6（全局 + 局部变量）
giencoder-design-system/colors_and_type.css                    需求 6
giencoder-design-system/gienx-templates/_shared/tokens.css     需求 6
```

**注入块**：`<style id="r77-pop-css">`（4 页）、`<style id="r77-base-css">`（base 1 页）
—— **全部注入在 `</body>` 前**（详见第四节坑 1）。

**未 commit / 未 push**（按默认约定）。

---

## 四、本轮新踩的坑（已写进 PLAYBOOK P3.9）

1. **注入位置决定 CSS 胜负**：r76 的两块注入在 `</body>` 前，我的 r77 块第一版注入在 `</head>` 前 ⇒
   同特异性的 `.r74-ripple` 规则**被页尾的 r76 块反向压回去**（实测 `zIndex` 仍是 10、点色仍是 0.62/1.8px）。
   **修正 = 注入位置与既有块对齐（`</body>` 前）**，让「后者胜」的自然顺序成立。
2. **改 React 源码顺序前，先查有没有运行时脚本在改写同一段 DOM**：base.html 的 r74 脚本抓「版权区最后一个 `p`」
   ⇒ 只改源码顺序会被脚本吃掉整句。**先 grep 目标文本 + `data-rNN-*` 标记**。
3. **波点密度与涟漪强度是耦合的**（涟漪点阵必须与底色点阵同网格才能对齐）⇒ 加密波点会**同步增强**涟漪，
   调整强度时要把密度的 ×1.56 算进去（α 0.62→0.28 才换到净 46%）。
4. **跨页基线不能混用**：拿 A 页的「无涟漪帧」去减 B 页的「有涟漪帧」，差异里会混进两页本身的差别
   （本轮就差过：20px vs 16px 网格），算出来的「强度比」全是废数 ⇒ **A/B 必须各用各页的基线**。
5. **`element.style.*` 读不到真实值**（旧坑，本轮又验证）：`translate`/`scale` 这类独立变换属性
   要用 `getComputedStyle(el).translate / .scale` 读，`transform` 会是 `none`。

---

## 五、材料索引

- **补丁**：`mg-work/r77/apply77.py`（需求 1/2/3/4/5/6）、`apply77b.py`（r74 脚本适配）
- **改前基线**：`mg-work/r77/before/*.html`（9 页）+ `before/ds/*.css`
- **探针**：`mg-work/r77/ev/rip77.js`（涟漪取帧，`__MODE=card|gap` + `__T` 可控帧）
- **证据图**：
  - `ev/dots-cmp.png`（波点密度 20px ↔ 16px 并排，×2 放大）
  - `ev/ripple-cmp.png`（涟漪 A/B 并排：r76 版 ↔ r77 版，同点同帧）
  - `ev/ripple-card-crop.png`（点对话框中心——涟漪被完全盖住）
  - `ev/rip-{base,card,gap}.png` / `ev/ripA2-{base,gap}.png`（原始帧）
- **门禁输出**：`ev/gate-before.txt` / `ev/gate-after.txt`
- **回滚**：`cp mg-work/r77/before/<page>.html pages/<page>.html`（⚠️ 文件名必须与原页面同名）
