# r93 验收报告 · 基础工作台会话详情 + aside 分组标题行高

> 需求来源：邵先生 2026-09-30 两条。
> 落地方式：`mg-work/r93/apply93.py`（幂等可复跑）+ `mg-work/r88/apply88b-fontsize.py`（需求 1 就地返工）。
> 设计稿：`https://mastergo.com/goto/WtK8bTCg?page_id=fw647:12809&layer_id=1393:18748&file=193158744355579`

---

## 一、需求 1 —— aside 分组标题行高 32px

**症状**：基础工作台左栏 aside 里 `flex items-center rounded-md px-2 py-0 hover:bg-[#E9ECEE]` 那几行
（「置顶任务 / 工作目录 / 自动化任务 / 通用会话」分组标题）被压成 **16px**。

**根因**：`<style id="r87-ui-css">` 里的全局字号块：

```css
body .text-xs { font-size: …; line-height: …; }      /* 特异性 (0,1,1) */
```

压过了尾风的 arbitrary 类 `.leading-\[32px\]{line-height:32px}`（特异性 **(0,1,0)**）
⇒ 行高从 32 掉到 16，整行高度腰斩。**这是 r87 字号机制引入的回归**。

**修法**（两步，都在 `apply88b-fontsize.py` 的 `build_css()`）：

1. `text-*` 的行高只在**该元素没有 `leading-*` 类**时才派生：
   `body .text-xs:not([class*="leading-"]){line-height:…}`
2. 给页面里真正用到的 arbitrary 类补一份派生行高，**写在 text-\* 规则之后**
   （同为 (0,1,1)，后写者胜）：

```python
LEADING_DERIVE = [
    (r'.leading-\[19px\]', 19),
    (r'.leading-\[22px\]', 22),
    (r'.leading-\[32px\]', 32),
]
```

⇒ 既修了冲突，又保留「字号跟随 `--ui-fs-ratio`」的能力。

**实测取证**（`mg-work/r93/ev/p93-lh-after.txt`）：4 个分组标题 `height 16 → 32`、`line-height 21px → 32px`；
顺带修正 textarea 20→22px、版权页脚 16→19.5px。

---

## 二、需求 2 —— 会话详情像素级还原

### 2.1 实现口径（自行拍板的三点）

| 分歧点 | 决定 | 理由 |
|---|---|---|
| 定位 | **居中**：`width:840px; margin:0 auto` | 设计稿内容列 L164 W840 落在 1168 面板里 ⇒ 164 = (1168−840)/2，是居中；实机 main 内宽 1162 ⇒ 左右各 161，不照搬 164 |
| 硬编码色 | 全部进本地 `:root` 变量 `--r93-*` + `[giencoder-theme='dark']` 暗色档 | `verify-design.py` 的 `!var(` 豁免保证零新增 TOKEN-GAP；规则 5 要求非 token 色入变量 |
| 字体 | 沿用页面 `Mona Sans VF`，不引 MiSans | 不因一份画稿换掉整页字体 |

**挂载方式**：不动 React 源，只在 `mainInner` 尾部追加 `.r93-conv-host`，
用 `[data-r93-conv='1'] > *:not(.r93-conv-host){display:none!important}` 纯 CSS 藏起「欢迎空态 + 版权页脚」；
会话点击在 `document` **捕获阶段**监听 `aside button`（`min-w-0 + flex-1` ⇒ 打开会话 /
`rounded-md + py-0` ⇒ 分组标题只折叠 / 其余 ⇒ 关回空态）；`MutationObserver` 兜底补回被 React 冲掉的节点。
轨迹页签切「暂无轨迹数据」空态。

### 2.2 ★ 关键发现：设计稿的「变体叠加」陷阱

导出图里**每个折叠块容器内同时叠放了「折叠状态」和「展开状态」两个变体**：

```
容器187 (上下文注入)  T358 H218
  ├─ fw647:14366 「折叠状态」  T0  H22      ← 变体 A
  └─ 1393:18485 「展开状态」    T34 H184    ← 变体 B（真机只有这个）
       ├─ fw647:15079 头       T0  H22
       └─ 1393:18483 卡片      T34 H150
```

⇒ **真机块高 = 容器高 − 34**，而**容器 top 差仍按 12/16/24 的间距序列排**。
⇒ `design-rgb.png` 里每块都被推低了 34px（**不累积**，逐块固定），所以**导出的 PNG 不能直接当"真机应长什么样"来量总高**。

去掉这层offset后逐块累加，设计真机内容总高 = **4106px**，与实机实测 **4106px 完全一致** ✅

### 2.3 ★ 字号体系（PNG 逐像素 + 节点框高双向验证）

设计稿源码里正文多为 `ui-component`（**不带字号属性**），只能靠两条独立证据交叉定：

1. 框高（`style="width:Wpx; height:Hpx"`）
2. PNG 墨迹行中心距 + 已知文本宽度反推每字符当量

| 用途 | 字号 | 行高 | 判据 |
|---|---|---|---|
| 折叠头标题 / 用户气泡正文 / 需求采访 | **14px** | 22px | 「你要把「任务看板」加到哪个左侧菜单？」252px ÷ 18 全角字 = 14 |
| 折叠头 meta（skill-catalog / 2s / deepwiki …） | **12px** | 22px | 源码 span 直标 `12/22` |
| **卡内正文 / 代码** | **12px** | **20px** | SKILL 64=24+2×20；网页搜索 184=24+8×20；重试 64=24+2×20；搜索资料 116=24+4×20+12gap；未知 surface 84=24+3×20 |
| **上下文注入卡正文** | **12px** | **16px** | 788×80 = 5 行；「取代先前的快照」84 ÷ 7 字 = 12 |
| **Bash 卡代码** | **12px** | **16px** | ui 780×96 = 6 行；PNG 实测行中心 Δ16.5/16/16/16/16 |
| 居中提示卡片下的说明行 | 12px | 24px | ui 778×24 / 300×24 |
| 深度思考正文 | **12px** | **22px** | 首行宽 342 ÷ 29.4 当量 ≈ 11.6px；14px 会折 9 行把卡撑到 222 |

> ⚠ **踩坑实录**：初版把卡内正文统一写成 `14px/22px` ⇒ 上下文注入卡 190（应 150）、SKILL 90（应 64）、
> 深度思考 222（应 200）、网页搜索 200（应 184）。改成上表后全部归位。

### 2.4 逐块几何核对（实机 1440×900 vs 设计稿）

| # | 块 | 实测块高 | 设计块高 | 实测卡高 | 设计卡高 | 判定 |
|---|---|---|---|---|---|---|
| 0 | 用户气泡 | 164 | 164 | 164 | 164 | ✅ |
| 1 | 助手头 | 74 | 74 | 74 | 74 | ✅ |
| 2 | 上下文注入 | 184 | 184 | **150** | **150** | ✅ |
| 3 | 深度思考 | 234 | 234 | **200** | **200** | ✅ |
| 5 | Bash | 194 | 194 | **160** | **160** | ✅ |
| 6 | 网页搜索 | 218 | 218 | **184** | **184** | ✅ |
| 7 | 需求采访 | 242 | 242 | **208** | **208** | ✅ |
| 8 | 更新任务清单 | 254 | 254 | **220** | **220** | ✅ |
| 9 | 文件写入 | 278 | 278 | **244** | **244** | ✅ |
| 10 | SKILL | 98 | 98 | **64** | **64** | ✅ |
| 11 | Tool call | 166 | 166 | **132** | **132** | ✅ |
| 12 | 重试 | 98 | 98 | **64** | **64** | ✅ |
| 14 | 压缩上下文 | 54 | 54 | — | — | ✅ |
| 15 | 上下文已压缩 | 54 | 54 | — | — | ✅ |
| 16 | 搜索资料 | 152 | 150 | 118 | 116 | Δ2 |
| 17/18 | 告警条 ×2 | 44 / 44 | 44 / 44 | 44 / 44 | 44 / 44 | ✅ |
| 19 | 未知 surface | 118 | 118 | **84** | **84** | ✅ |
| 20 | 模型已切换 | 22 | 22 | 22 | 22 | ✅ |
| 22 | 改动汇总卡 | 302 | 302 | 302 | 300 | Δ2 |
| 23 | 任务产物 | **230** | **230** | 230 | 230 | ✅ |
| 24 | Token 速率行 | 24 | 24 | — | — | ✅ |

**横向**：host 1162 / wrap 840 / 气泡 728 / 助手头 840 / 卡 822 / 产物卡 414×56 / diff 840 / 告警 840 — **全部严丝合缝**。

### 2.5 结构级修正（本轮发现的、非尺寸问题）

| 块 | 原实现 | 设计稿实际 | 处理 |
|---|---|---|---|
| 更新任务清单 | 带 40px 卡头 + 分隔线 | **无卡头**：分隔线在卡内 **y=181**（不是 40）；内容 = 16 + 9 行×16 + 线 + 输出 | 重写为 `.r93-todocard`（16/20/12 padding + 21px 间距线），JSON 改为设计稿的 **9 行截断式** |
| 网页搜索 | 一整块灰色普通文本 | 8 行，**整行是蓝色下划线链接**（`#3770F7`），序号同色；行高 20 | 重写为 `<a class="r93-wlink">` 列表 |
| 搜索资料 | 序号 + 蓝色 span（无下划线） | 蓝下划线标题 + 灰描述，组内 gap 3 / 组间 6 | 重写为 `.r93-srch / .r93-srchg` |
| 任务产物 | Token 速率行在卡内（`margin-top:20px`） | 速率行是**独立容器** 1393:18599（840×24 @ +20） | 拆成独立块 |
| 深度思考列表项 | 私有区图标字符 `󰀐`（实机缺字形 ⇒ 折行） | 导出图渲染为 **「1. 2. 3.」** | 改为有序列表纯文本 ⇒ 9 行回归 8 行 |
| 上下文注入滚动条 | `right:6px` | 卡内 (812,4) ⇒ **right 4px**、6×88 | 改 `right:4px` |
| agent 选中态边框 | 字面 `#E2D3F9` | PNG 实测 `#E2D3F9` ✓（正确但违规） | 提为 `--r93-a1-bd` + 暗色档 |

### 2.6 暗色适配

r93 画面里的字面白底（11 处 `background: #FFFFFF`）与 `#F5F6F7` 卡底在暗色下会整片白屏 ⇒
- 白底一律换成 DS token **`var(--color-bg-2)`**（浅色 `#fff` / 暗色 `#232324`）—— 浅色视觉零变化；
- `--r93-*` 全套（卡片底 / 描边 / 分隔线 / 气泡 / 滚动条 / 胶囊 / 告警 / agent 徽标 4 组 / hover）补 `[giencoder-theme='dark']` 档；
- 实测暗色截图 `mg-work/r93/raw/v2-dark.png`：面板 / 卡片 / 气泡 / composer **全部正常，无白屏**。

---

## 三、验收四查

| 项 | 结果 |
|---|---|
| `python mg-work/check-syntax.py pages/*.html` | **9/9 通过**（base.html `script=9 style=15`） |
| `python verify-design.py ./pages` | **75 个问题（66 warning / 9 info / 0 critical）** = r92 基线 **完全一致，零新增** ✅ |
| 幂等（`apply93.py` 复跑两遍） | 第二遍起「**已是目标态（无改动）**」✅ |
| 像素取证 | 明色 `v2-0/820/1640/2460/3020/end.png` + 暗色 `v2-dark.png` ✅ |

**清理**：`git checkout -- pages/gaps.log`；`mg-work/kanban/r13/chk/` 已 `checkout` + `clean`。

---

## 四、改动的文件

| 文件 | 变化 |
|---|---|
| `pages/base.html` | 470695（r92 末态）→ **605980 字符**：注入 `<style id="r93-conv-css">`(23168) + `<script id="r93-conv-js">`(112048，含 44+ 个内联 SVG 图标) + `r87-ui-css` 块 +480 字符（需求 1） |
| `mg-work/r93/apply93.py` | 本轮新建补丁（幂等：摘块 → 注入 → `fs.converge()` 字号派生） |
| `mg-work/r88/apply88b-fontsize.py` | 需求 1 就地返工（`LEADING_DERIVE` + `:not([class*="leading-"])`） |
| `mg-work/r93/raw/*` | 设计稿导出 + 解析脚本 + 取证裁剪图 |
| `mg-work/r93/ev/*` | 探针（dom / open / geo / geo2 / lh）+ 四查输出 |

---

## 五、遗留 / 待拍板

1. **Δ2 级微差**：搜索资料卡 118→116、改动汇总卡 302→300。前者是 `gap` 取整（组内严格值 3.5），后者是 border 计入方式，均不影响视觉节奏。
2. **字体度量差异**：上下文注入卡长文在 MiSans 下折 5 行、在 Mona Sans 下折 4 行 ⇒ 用 `min-height:150px` 保住卡高（内容自然排布、不裁切）。若日后引入 MiSans 可自然归位。
3. **「滚动到底部」按钮**：`position:sticky; bottom:44px` 的滚动中态（设计稿里它也是浮层，位于内容列底部）—— 滚动到顶/中时可见、接近底部时自动隐去，与设计稿一致。
4. 前几轮结转未拍板项（顶栏背景图范围/尺寸与 x=340 接缝、完全访问红色档位、r90 三处 DS 偏离、`#ECEEF2` 是否入 DS 色板等）见 `HANDOFF.md` 第六节。

---

## 六、r93 ④（同日第三轮答复）：会话详情独立成页 + composer 全要素复用

> 邵先生两条：①「当前这个 AI 对话的页面是否应该是一个独立的 html 页面？如果是，那么要注意与其他页面的跳转路由关系」；
> ②「AI 对话页面底部的对话框要完全的全要素复用基础工作台 main 容器里的那个对话框
> `relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors`」。
> 拍板结果：**做成独立页** / **保留状态条 + 4 张 agent 卡，只换输入卡**。

### 6.1 侦察结论（动手前实测，非推断）

**路由架构**：9 个页面各自都是**完全自包含**的独立 html（顶栏 + aside + 外壳在每个文件里各一份）；
跳转靠每页内嵌的 `SHELL-NAV-FIX v5` 里的 `var ROUTE = {...}`，实测 **9 页各 1 份、内容逐字相同**：

```
'/': base.html  '/base': base.html  '/dev': dev.html  '/kanban': kanban.html
'/req-kanban': req-kanban.html  '/task-detail': task-detail.html  '/avatar': avatar.html
'/automation': automation.html  '/skills': skills.html  '/settings': settings.html
```

**真实 composer 的 DOM 血缘**（1440 视口实测 rect）：

| 层 | 选择器 | rect |
|---|---|---|
| main | `main.min-w-0.flex-1.h-full.overflow-hidden.rounded-lg.border.bg-white.dot-bg` | (268,48) 1164×844 |
| mainInner | `main > div.relative.flex.h-full.min-w-0.flex-col.overflow-hidden` | (269,49) 1162×842 |
| ① hero | `div.flex.flex-1.flex-col.items-center.justify-center.px-6` | (269,49) 1162×760 |
| ② footer | `div.pb-6.text-center.text-xs.leading-relaxed` | (269,809) 1162×83 |
| hero[0] | `div.pointer-events-none.text-center`（LOGO + 问候语） | (701,268) 298×76 |
| hero[1] | `div.mt-8.flex.w-full.flex-col.items-center.gap-2` | (293,376) 1114×214 |
| └ outer | `div.flex.w-[800px].flex-col.rounded-[16px].bg-[var(--color-fill-1)].px-3.py-3` | (420,376) **860**×214 |
|   ├ **① 输入卡** | `div.relative.flex.w-full.flex-col.rounded-[16px].border.bg-white.p-3.transition-colors` ← **邵先生点名的那一个** | (432,388) **836**×154 |
|   │  ├ textarea（`min-h-[96px]`） | | 810×96 |
|   │  ├ 底排 `div.mt-auto.flex.items-center.justify-between` | 左簇：`[＋添加]` `[技能]` `[艾迪·数字分身]` `[标准模式▾]`；右簇：`[模型 DeepSeek-V4-Pro▾]` `[优化提示词⟳]` `[发送]` | 810×32 |
|   │  └ `div.giencoder-select[aria-label=技能选择]`（弹层宿主，未开时 h=0） | | 810×0 |
|   └ **② 底排** | `div.flex.items-center.gap-[8px].pt-[6px]` → `[📁 工作目录 (可选)▾]` `[🔒 默认权限▾]`（r92 需求 4「完全访问转红」就在这） | (432,376+154+…)=… **836×36** |

⇒ 之前 r93 自绘的那版 composer **要素与真实组件不同**：设计稿是「默认权限在卡内底排 + 发送红色 + 上方状态条 + 4 张 agent 卡」，
真实组件是「卡内 = 数字分身 + 标准模式；工作目录 + 默认权限单独一行；无状态条/agent 卡」。故「复用」必然带来形态变化。

### 6.2 落地方式

**① 独立页 `pages/conversation.html`（新建，604806 字符）**

不是「复制一份再改」，而是**每次由 base 净底重建**（`apply93.py` 的 main()）：

```
net  = base.html 摘掉 r93-conv-css / r93-conv-js / r93-nav-js     ← 唯一净底来源
net  = route_patch(net)                                           ← ROUTE 表 + '/conversation'
base = net + <script id="r93-nav-js">                             ← 只留「点会话 ⇒ 跳页」
conv = net + data-r93-page="conversation" + 标题 + r93-conv-css + r93-conv-js
其余 8 页：route_patch（幂等）
```

* base.html **减重 134536 字符**（605980 → 471444），会话详情的整块（CSS 23K + JS 112K）整体搬到新页。
* `r93-nav-js`（≈1.1KB）：捕获阶段监听 `aside button`，`min-w-0 + flex-1`（会话项，实测 13 个）⇒
  `location.href='conversation.html'`；分组标题（`rounded-md + py-0`，4 个）与导航项一律放行。
  **不 preventDefault / stopPropagation** —— 实测外壳对会话项没有自己的导航行为，放行可保留它的选中态。
* 路由：9 页 ROUTE 表各插一条 `'/conversation': 'conversation.html'`（conversation.html 由 net 继承，不再重复插）。
  ⚠ 顶栏「工作台切换」页签不受影响：`conversation.html` 不在 `DEV_PAGES` ⇒ `fileGroup='base'`，点「基础工作台」页签
  时 `groupOf()` 返回 `'base'` 而 `n===groupOf()` ⇒ 空操作（本页已在基础工作台内，合理）。
* `<title>` 改为「会话 · 基础工作台」，与基础工作台区分。

**② composer 全要素复用（纯 CSS，零复制、零重绘）**

```css
.r93-conv-host { display: none; }                                    /* base 里永不显示 */
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center {
  flex: 0 0 auto !important; justify-content: flex-end !important; padding-bottom: 12px !important; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > .pointer-events-none { display: none !important; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 { margin-top: 0 !important; }
html[data-r93-page='conversation'] main > div > div.pb-6 { display: none !important; }
html[data-r93-page='conversation'] .r93-conv-host {
  display: flex; flex-direction: column; flex: 1 1 auto; min-height: 0; order: -1; overflow: hidden; }
```

* **不动 DOM 血缘**：宿主用 `order:-1` 排到 hero 之前、hero 改贴底且只留 composer、问候语与页脚 `display:none`
  ⇒ 视觉顺序 = 详情（可滚，flex:1）在上、**真实 composer**（flex:none）在下。React 重渲染不会炸。
* 实测结果（1440×900）：host (269,49) **1162×628** `order:-1`；hero (269,677) 1162×**214**；
  outer (420,677) **860×214**；card (432,689) **836×154**；问候语与页脚 `display:none`；页面无纵向滚动（doc 900 = win 900）。
* 自绘输入卡整组退场（CSS 删 `.r93-input/.r93-ta/.r93-itools/.r93-ictl/.r93-perm/.r93-itools-r/.r93-model/.r93-send`；
  JS 删 `TPL_BOTTOM` 里的 `.r93-input` 与输入框自增高逻辑）。`.r93-cp` 的灰底/描边也去掉，
  灰壳只留真实 composer 那一层，避免两层灰壳叠罗汉。
* **交互实测可用**（证明「全要素」）：「＋添加」⇒ 菜单 180×92（添加本地文件 / 知识库）；
  「默认权限」⇒ 权限选择弹层 280×126（含完全访问）；「标准模式 / DeepSeek-V4-Pro / 工作目录」⇒
  三个 `.giencoder-select-popup` 均正常展开。这些全是外壳 React 自己的 handler，我们一行都没写。

**③ 页面级适配：composer 贴底后下拉必须向上弹（本轮新发现）**

真组件下拉默认 `top: calc(100% + 4px)`（向下）—— 欢迎态 composer 居中时没问题；
本页 composer 钉在 main 底部而 `main` 是 `overflow:hidden` ⇒ 向下的弹层被裁。
实测「默认权限」popup rect y **871..997**、main 底 **892** ⇒ 只剩 21px 可见。

```css
html[data-r93-page='conversation'] .giencoder-select-popup { top: auto !important; bottom: calc(100% + 4px) !important; transform-origin: bottom; }
html[data-r93-page='conversation'] [aria-label='权限选择']   { top: auto !important; bottom: calc(100% + 4px) !important; }
```

修后实测四个弹层全部完整可见（main 底 892）：
标准模式 (601,702,200×80) ／ DeepSeek-V4-Pro (1031,579,194×207) ／ 工作目录 (436,730,194×109) ／ 默认权限 (595,709,280×126)。

### 6.3 验收四查（同上口径）

| 项 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍 → 第二遍起两页均「已是目标态（无改动）」；`--revert --dry` 正常（base 471444→470692、9 页 ROUTE 各 -1 条、conversation 待删） |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（base `script=9 style=14`；conversation `script=9 style=15`） |
| 零影响 | 与「④ 前 9 页」基线同口径逐条 diff：**75 → 76**，**唯一差异 = conversation.html 新增 1 条 `CRAFT-SLOP`（info 级「检测到 N 处渐变」，每页各有一条的页面级统计，非缺陷）**；warning 66 条不变、critical 0 |
| 视觉/像素 | `raw/v3-conv-top.png`（详情顶部 + 底部 composer）/ `v3-conv-bottom.png`（滚到底）/ `v3-base.png`（base 回到欢迎态）/ `v3-perm-up.png`（权限弹层向上弹出）；跳转链实测 base 点会话 → `conversation.html`（attr=conversation、host 与真实 composer 均在） |

### 6.4 ⑥ 回滚

```bash
python mg-work/r93/apply93.py --revert     # 删 conversation.html + 摘 base 的 r93-nav-js + 9 页 ROUTE 各 -1 条
# 或逐页恢复到「④ 前」快照：
cp mg-work/r93/before/base-r93c.html pages/base.html         # ④ 前的 base（含页内版会话详情）
cp mg-work/r93/before/<page>-r93c.html pages/<page>.html      # 其余 8 页（差异仅在 ROUTE 行）
```

`mg-work/r93/ev/base04/` = 「④ 前 9 页」基线的同口径副本（仅供 diff，非产物）。

---

## 七、r94（同日第四轮）：会话详情页 5 条微调（**就地在 `apply93.py` 上返工**）

> ⚠ r93 未提交 ⇒ 按硬规则**就地改原补丁、不另起代数**（改 `mg-work/r93/apply93.py` 的 `r93-conv-css` / `r93-conv-js`）。

### 7.1 需求与落地

| # | 需求（原话要点） | 做法 |
|---|---|---|
| ① | `r93-seg-cap` 内容要在标题栏 `r93-bar` 内**居中** | `.r93-seg-cap`：`left:396px`（按设计稿 1168 面板量的**固定值**，换视口即偏）→ **`left:50%; transform:translateX(-50%)`**（垂直本就居中：10+24+10=44） |
| ② | 内容容器 `r93-wrap` 宽度 = **main 的 50%**、**最小 860px** | `.r93-wrap`：`width:840px` → **`width:50%; min-width:860px; box-sizing:border-box; padding:32px 10px 24px`**。★ 内容块（气泡 728 / 卡 822 / full 840）是设计稿固定宽 ⇒ 必须补左右各 10px 内距，才能让**内容盒仍是 840 并居中**（横向位置与 r93 口径 430..1270 逐像素一致） |
| ③ | 对话框**只显示输入卡本体**，外围元素都不要 | outer（`div.mt-8 > div`）**去灰壳**（`background:none; padding:0; border-radius:0`）+ **隐藏底排**（`> div:not(:has(textarea))` ⇒「工作目录 / 默认权限」行 `display:none`）。**不动 DOM 血缘**（React 重渲染安全） |
| ④ | `div.mt-8` 容器内的**波点元素**全部去掉 | ★ 侦查：该容器**只有 1 个子元素**（= composer 外壳），**并无波点子节点**；点阵真正来源 = `main.dot-bg` 自身的点阵 + `main.dot-bg::before` 的光斑层（全页仅这两处 `radial-gradient`）⇒ 页面级 `main.dot-bg{background-image:none}` + `main.dot-bg::before{display:none}` |
| ⑤ | `r93-card--ctx` 最大高 **240px**、溢出内滚；`r93-vsb` 假滚动条**去掉** | `.r93-card--ctx`：`min-height:150px` + **`max-height:240px; overflow-y:auto; overflow-x:hidden`**；**删** `.r93-vsb` CSS 规则 + **5 处 DOM**（ctx 卡 / Bash / diff / 改动汇总 / 任务产物） |

### 7.2 实测（1440 视口，探针 `ev/p94b~e.js`）

| 项 | 读数 |
|---|---|
| ① 居中 | `bar [269,49,1162,44]` / `cap [662,59,377,24]` ⇒ **capCenterDelta = 0**（精确居中） |
| ② wrap | `[415,93,860,4158]`（`width:860px` / `min-width:860px` / `padding-left:10px`）；内容 `bub [537,125,728,164]`、`card [443,441,822,150]` ⇒ 内容盒 **425..1265**，与 r93（`wrap 840` 时）**零位移** |
| ③ outer | `[420,725,860,154]`、`bg rgba(0,0,0,0)`、`padding 0px`、`border-radius 0px`；子① 输入卡 `display:flex` `[420,725,860,154]`（**860 宽**）、子② 底排 `display:none` |
| ④ 点阵 | `main.backgroundImage = none`、`main::before.display = none` |
| ⑤ ctx | `max-height:240px` / `overflow-y:auto`；当前内容 150 高不滚。**溢出取证**（运行时临时塞双份内容，测完移除、不落盘）：`scrollHeight 244 > clientHeight 240` ⇒ `scrollable:true`、`scrollTop` 可达 4 ✓；`.r93-vsb` 计数 **0** ✓ |
| 整页 | `doc [1440,900] = win [1440,900]`（无纵向溢出）；滚动口 `[269,93,1162,520]`（hero 因 outer 去壳变矮 60px ⇒ scroll 变高 60px），`滚动到底部` 浮层仍贴新滚动口底（按钮底 601 + 12 = 613） |

### 7.3 四查

| 项 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍 → 第二遍 base + conversation **双「已是目标态」** |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（base `script=9 style=14` / conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical），与 r93 基线 `vd-r93c.txt` **逐字节相同** |
| ★ 一次假阳性（已修） | 首跑 `vd-r94.txt` 曾出现 conversation 渐变计数 **62 → 63** —— 根因 = 我在新注释里写了「`radial-gradient`」这个词（被扫进渐变统计）⇒ 改措辞后**逐字节归零**。这正是「**新增注释里不得出现被断言的 token**」的实例 |

### 7.4 产物与口径

`pages/conversation.html`：**606073 字符**（字节 sha **`acb485be7385`**；r93 ④ 时 604806 ⇒ r94 **+1267**）。
`pages/base.html`：**471444 字符**（`b5dc55fe7594`，**未变**）。
`mg-work/r93/apply93.py`：CSS **5 改 1 删** + JS **删 5 处 `r93-vsb`**。
`mg-work/r93/ev/`：`p94b.js/.sh`（首查）、`p94c.js/.sh`（点阵来源 + 截图）、`p94d.js/.sh`（5 条实测）、`p94e.js/.sh`（sticky + 溢出取证）、`vd-r94.txt`（首跑·含假阳性）、`vd-r94b.txt`（修后 = r93 基线）。
`mg-work/r93/raw/`：`r94-hero.png` / `r94-full.png`（before 对照 `v4-hero.png` / `v4-full.png`）。

> ⚠ **口径提醒**：`open(fp,'rb').read().decode('utf-8')` 会把 CRLF 算成 **2 个字符**（本轮误得 608350 / 472690）；
> **权威口径 = Python text mode（LF）** ⇒ `606073` / `471444`，与 `apply93.py` 自报一致。

---

## 八、r95（同日第五轮）：会话详情页「右侧撑满」2 条（**就地返工 `apply93.py`**）

### 8.1 用户两条与解读

| # | 用户原话 | 落地含义 |
|---|---|---|
| 1 | 「类似这种容器 `r93-card r93-card--ctx` 的右侧要撑满」 | 卡片类容器**右边界顶到内容列右边界**（设计稿 18px 左缩进**保留** ⇒ 宽 = `calc(100% - 18px)`）；「类似这种」⇒ 所有整行块容器（card / full / todocard / alert / diff / note / ndesc / arts）统一改**流式** |
| 2 | 「底部对话框相关的内容模块也要自适应撑满」 | 底部列（状态条 / agent 卡行 / 对话框外壳）从「固定 840 居中」改为**与内容列同口径**（50% / min 860px）⇒ 三层一起撑满并与之对齐 |

★ 解读依据 = **动手前的实测**（不是推断）：见 8.2。

### 8.2 侦查：三组元素、三条右边界（1440×900，`ev/p95a.js`）

| 组 | 元素 | 实测 rect | 右边界 |
|---|---|---|---|
| 内容 | `.r93-wrap` 外沿 | `[415,93,860,·]` | 1275 |
| 内容 | `.r93-wrap` 内容盒（padding `32/10/24`） | 425..1265 | 1265 |
| 内容 | `.r93-card--ctx` | `[443,441,822,150]` | 1265 |
| 内容 | `.r93-bub` | `[537,125,728,164]` | 1265 |
| 内容 | `.r93-todocard` | `[443,1631,822,220]` | 1265 |
| 底部 | `.r93-sb`（`width:840px; margin:0 auto`） | `[430,613,840,40]` | 1270 |
| 底部 | `.r93-cp` | `[430,665,840,48]` | 1270 |
| 对话框 | composer `outer` / 输入卡 | `[420,725,860,154]` | **1280** |

⇒ **三条线打架（1265 / 1270 / 1280）**。两个根因：

1. **滚动条占位 ⇒ 不同轴**：`.r93-scroll` 出现滚动条后内容盒收窄，`margin:0 auto` 的 `.r93-wrap` 相对**没有滚动条**的底部列与 composer **左偏 5px**（实测 `offsetWidth 1162`，单侧滚动条 10px ⇒ 可用 1152 ⇒ `(1152−860)/2 = 146` ⇒ x=415，而底部为 430、composer 为 420）；
2. **wrap 的 10px 内距**：r94 ② 为「保住内容盒 840」而加，使内容块比 composer 窄 10px（每边 5px）。

### 8.3 落地（`mg-work/r93/apply93.py`，共 14 处）

| 类别 | 改动 |
|---|---|
| ① 居中同轴 | `.r93-scroll` 加 `scrollbar-gutter: stable both-edges`（两侧各让出等量 gutter ⇒ 内容恒居中，不再偏 5px） |
| ② 内容盒 | `.r93-wrap` padding `32px 10px 24px` → **`32px 0 24px`**（块改流式后不再需要内距） |
| ③ 卡片 | `.r93-card` / `.r93-todocard`：`width:822px` → **`calc(100% - 18px)`**（**左缩进保留、右侧撑满**） |
| ④ 整行块 | `.r93-card--full` `840px`→`100%`；`.r93-note` / `.r93-ndesc` / `.r93-alert` / `.r93-diff` / `.r93-arts` `840px`→`100%` |
| ⑤ 产物卡 | `.r93-artcard` `414px` → **`calc(50% - 6px)`**（两列等分撑满；原 414×2+12 恰 840，列一变宽右侧就留白） |
| ⑥ 底部列 | `.r93-bottom` 加 `width:50%; min-width:860px; box-sizing:border-box; margin:0 auto`；`.r93-bottom > *`：`width:840px; margin:0 auto` → **`width:100%; margin:0`** |
| ⑦ 对话框壳 | `… > div.mt-8 > div` 补 **`width:50% !important; min-width:860px !important`**（原先由 Tailwind 写死定值，不跟随内容列） |

⚠ **刻意未动**：`.r93-bub`（用户气泡 728px —— 右对齐 ⇒ 自动跟随新右边界，且设计稿语义本就是「不满宽」）；`.r93-agent`（4 张 agent 卡按内容宽左对齐，属设计稿固定排版，不是「容器」）。
⚠ **收敛安全**：`calc(100% - 18px)` / `calc(50% - 6px)` / `100%` / `50%` 均**不含「裸 `Npx` 结尾」**，不匹配 `apply88b` 的任何 `RE_*` ⇒ 不会被 `unscale()` 改坏（与既有 `calc(100% + 4px)` 同理）。

### 8.4 实测（`ev/p95b.js`，1440 / 1920 两档）

| 元素 | 1440 | 1920 |
|---|---|---|
| `.r93-scroll` | `clientWidth 1142 / offsetWidth 1162`，gutter `stable both-edges` | 1622 / 1642 |
| `.r93-wrap` | `[420, 860]` → 右 **1280** | `[660, 860]` → 右 1520 |
| `.r93-bottom` / `.r93-sb` / `.r93-cp` | `[420, 860]` → 右 **1280** | `[660, 860]` |
| composer `outer` / 输入卡 | `[420, 860]` → 右 **1280** | `[660, 860]` |
| `.r93-card--ctx` / `.r93-todocard` | `[438, 842]` → 右 1280（**Δ=0**） | `[678, 842]` |
| `.r93-bub` | `[552, 728]` → 右 1280（**Δ=0**） | `[792, 728]` |
| `.r93-alert` / `.r93-diff` / `.r93-arts` / `.r93-note` | `[420, 860]` → 右 1280（**Δ=0**） | `[660, 860]` |
| `.r93-artcard` | `[420, 424]`（两列 ⇒ 第二张右边界 1280） | `[660, 424]` |
| `.r93-tbsticky` 药丸 | `[790,·,120,·]` 中心 **850** = 内容列中心 | 中心 1090 |

⇒ **所有内容块 Δ=0**（与 composer 右边界严格对齐）；`doc/win` 在 1440 / 1920 下均**无横向溢出**。

### 8.5 四查

| 查 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍：第二遍 base + conversation 双「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical），与 r93 基线 `vd-r93c.txt` **逐字节相同** |
| 视觉 | `raw/r95-full.png` / `r95-hero.png`（对照 r94 的 `r94-full.png` / `r94-hero.png`） |

### 8.6 产物与回滚

`pages/conversation.html`：606073 → **606949 字符**（+876；字节 sha **`247c6c1e040e`**）。
`pages/base.html`：**471444 字符**（`c16308a00915`，**未变**）。
`mg-work/r93/ev/`：`p95a.js/.sh/.py`（侦察）、`p95b.js/.sh/.py`（实测）。
回滚：`python mg-work/r93/apply93.py --revert`（整代），或按 8.3 表逐条还原后重跑。


## 九、r96（同日第六轮）：会话详情页 5 条（**就地返工 `apply93.py`**）

### 9.1 五条需求与落地

| # | 用户原文 | 落地 |
|---|---|---|
| ① | `r93-bubi` 容器最大高度 240px，溢出就内滚 | `.r93-bubi` 加 `max-height:240px; overflow-y:auto; overflow-x:hidden`（只改「体」，不动 `.r93-bub` 气泡列） |
| ② | 类似 `r93-card` 的容器默认字号调整为 13px | `.r93-card` 加 `font-size:var(--font-size-body-2)`（= 13px）。⚠ 本规则不得声明裸 `height`（converge 约束），本规则无 height ✓。卡内 `.r93-pre` 等自带 12px 的不受影响 |
| ③ | `r93-t14` 的文字颜色要浅两级；`r93-t14 r93-c2` 用正文颜色 | `.r93-t14` 默认色 → `--color-text-3`；新增 `.r93-t14.r93-c2 { color: var(--color-text-1) }`（特异性 (0,2,0)，压过 `.r93-c2` 的 (0,1,0)，与书写顺序无关） |
| ④ | `r93-card r93-card--edge` 的宽度还没调整 | 嵌套 Tool call 卡拉丢内联 `w:804`（让它走 `.r93-card` 的 `calc(100% - 18px)`）；另两处 `style="width:840px"` 的 AI 文本块也一并改流式 |
| ⑤ | `r93-rateline` 各元素还原度很低，请对比设计稿精确还原 | 整行重写（见 9.2 / 9.3） |

### 9.2 ★ 需求 ⑤ 的设计稿取数（两份权威源，非目测）

**源 1：`raw/design-1393-18748.html`**（设计稿导出的带样式 HTML）—— 节点 `1393:18599`「容器 247」：

```
容器 247  256×24 @ (left 164, top 4664)
├ 1393:18598 容器 246  56×24 @ (0,0)   = 2 × icon-wrapper(24×24, 图标 14)   ← gap 8
├ fw647:19598 直线 46  @ left 68  top 5     <img svg_e6d49921.svg  color:#E5E5E5>
├ fw647:19591 Link     142×24 @ left 80 top 0  gap:4
│   ├ img 容器 14×14 color:#868686        ← 时钟（= 我们的 IC('rate')）
│   └ span「Token 速率：256/s」color:#868686; font-size:14px; line-height:24px
├ fw647:19599 直线 47  @ left 234 top 5
└ fw647:19681 icon-wrapper 24×24（导出时缺 left/top ⇒ 位置以 PNG 实测量为准）
```

`svg_e6d49921.svg` 的源是 `viewBox="0 0 2 14"` 的一条 `line` ⇒ **分隔线是 1px 宽 × 14px 高的竖线**。

**源 2：`raw/design-rgb.png`**（1x 整页导出，**色值已验证准确**：同一张图上量的前两枚图标 = (107,107,107) = #6B6B6B，与该 HTML 里其它 `style="color: #6B6B6B"` 完全一致）逐像素列扫描（y 4668..4686）：

| 元素 | 行内相对 x | 宽 | 备注 |
|---|---|---|---|
| 图标 1（复制） | 6..18 | 13 | 笔画色 #6B6B6B |
| 图标 2（分支） | 40..49 | 10 | 笔画色 #6B6B6B |
| **分隔线 1** | **68** | **1** | y 4670..4683 ⇒ **高 14** |
| 时钟 | 82..93 | 12 | #868686 |
| 「Token 速率：256/s」 | 99..221 | 123 | #868686 |
| **分隔线 2** | **234** | **1** | 高 14 |
| 省略号三点 | 240..249 | 10 | #868686（点中心 240.5 / 244.5 / 248.5，间距 4） |

⚠ **旧实现的两处硬错**：① 把「容器 246 的 56 宽」误当成**线宽** ⇒ 写成 `.r93-nline{width:56px}`，画出来是 56×1 的**横线**；② `gap:16`，而设计各段间距是 **12**（56→68→80→222→234）。

新实现（`.r93-rgrp`[gap 8] + `.r93-rline`[1×14] + `.r93-rrate`[gap 4] + `.r93-rbtn`[24×24 盒/图标 14 居中]）：

```css
.r93-rateline { display:flex; align-items:center; gap:12px; }
.r93-rgrp  { display:inline-flex; align-items:center; gap:8px; flex:none; }
.r93-rbtn  { width:24px; height:24px; color:var(--r93-ioc2); ... }   /* #6B6B6B */
.r93-rline { flex:none; width:1px; height:14px; background:var(--color-border-2); position:relative; z-index:1; }
.r93-rrate { display:inline-flex; align-items:center; gap:4px; color:var(--color-text-3); }
.r93-rateline > .r93-rline + .r93-rbtn { margin-left:-16px; color:var(--color-text-3); }
```

新色：`--r93-ioc2: #6B6B6B`（浅色）/ `#C9C9C9`（暗色档，DS 暗色色阶是反的 ⇒ gray-7）。
新图标 `branch`：设计稿里它是 DS 的 `icon-wrapper` 实例（**没有导出独立 svg**），按 `design-rgb.png`
的 14×14 点阵逐像素反推（三个**空心**圆节点 + 贯通主线 + 自右节点下沿并入主线的曲线），换算到 16 网格后写入 `ICON_INLINE`。

### 9.3 实测（1440×900，探针 `ev/p96a.js`（改前）/ `p96b.js`（改后）/ `p96c.js`（溢出取证））

| # | 改前 | 改后 |
|---|---|---|
| ① | `maxHeight:none` / `overflowY:visible` | `maxHeight:240px` / `overflowY:auto`；**溢出取证**：正文撑到 25 倍 ⇒ `scrollHeight 590 > clientHeight 240`、`scrollable:true`、`scrollTop` 可到 350；还原后 40/40 |
| ② | `.r93-card` 无 font-size；无类名文本 3 个 = 14px | `.r93-card` = **13px**；无类名文本（3 个 `.r93-pop` 里的 a）= **13px** |
| ③ | quiz 问题行 rgb(31,31,31) / 回答行 rgb(78,78,78) | 问题行 **rgb(134,134,134)** = #868686 / 回答行 **rgb(31,31,31)** = #1F1F1F ✔ 与设计稿实测一致 |
| ④ | edge 卡 4 个宽度 = 842 / 842 / 842 / **804**（右界 1280/1280/1280/**1260**）| 842 / 842 / 842 / **824**（右界 **全 1280**）；两处 AI 文本块也由 840 → 860（右界 1260 → 1280） |
| ⑤ | gap **16**；线 = **56×1 横线**；图标为 `artall`+`regen`；省略号色 #4E4E4E | gap **12**；线 = **1×14 竖线**（bg rgb(229,229,229)）；图标 = **复制 + 分支**（rgb(107,107,107)）；省略号 rgb(134,134,134) |

**⑤ 逐元素对位（行左 = 视口 420）**：

| 元素 | 实测 rel x | 设计 rel x | 差 |
|---|---|---|---|
| 图标 1 盒 / 图标视觉 | 0..24 / 5..19 | 0..24 / 6..18 | ✔ |
| 图标 2 盒 / 图标视觉 | 32..56 / 37..51 | 32..56 / 40..49 | ✔ |
| 分隔线 1 | **68**（1×14） | **68** | ✔ |
| 时钟 / 文字 | 81 / 99 | 80 / 99 | +1 |
| 分隔线 2 | 227 | 234 | −7 |
| 省略号盒 / 点 | 224..248 / 229..243 | 231.5..255.5 / 236.5..250.5 | −7.5 |

⇒ 前三段**逐像素对齐**；后两段整体左移 7px，**唯一原因是字体度量**（实机 Mona Sans 下
「Token 速率：256/s」宽 116，设计稿 MiSans 下 123 ⇒ Link 总宽 134 vs 142）。
**省略号相对第 2 根线的位置关系是一致的**（实测盒在线左 3px / 设计 2.5px）⇒ 是**同一套间距**在换字体后的自然位移，不是间距错。

### 9.4 四查

| 查 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍：第二遍 base + conversation 双「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical），与 r93 基线 `vd-r93c.txt` **逐字节相同** |
| 视觉 | `raw/r96-cmp2.png`（设计稿 vs 实机**同尺度上下对照**）· `r96-ratepage.png` · `r96-after-full.png` |

### 9.5 产物与回滚

`pages/conversation.html`：606949 → **609969 字符**（+3020；字节 sha **`e032e8913bf1`**）。
`pages/base.html`：**471444 字符**（`c16308a00915`，**未变**）。
`mg-work/r93/ev/`：`p96a.js/.sh`（侦查）· `p96b.js/.sh`（实测）· `p96c.js/.sh`（溢出取证 + 元素截图）· `p96d.js/.sh`（滚动取证）· `vd-r96.txt`。
`mg-work/r93/raw/`：`r96-ic12.png` / `r96-ic12big.png`（图标 18× 放大）· `r96-rate-ctx.png` · `r96-cmp2.png` · `r96-ratepage.png` · `r96-after-full.png`。
回滚：`python mg-work/r93/apply93.py --revert`（整代），或按 9.1 表逐条还原后重跑。

---

## 十、r97（同日第七轮）：会话详情页 4 条

> 邵先生四问：① 所有 `.r93-card` 容器内字号统一 13px；②「滚动到底部」应是胶囊按钮且文字色与图标色一致；
> ③ 底部对话框相对上方内容**两端各短一截**、要求所有内容模块等宽；④ 底部对话框**下方**还缺一行小灰字。
> r93 未提交 ⇒ 仍**就地返工 `mg-work/r93/apply93.py`**（不另起代数）。

### 10.1 四条改动

| # | 用户原文 | 落地 |
|---|---|---|
| ① | 所有 `r93-card` 容器内的字号统一调整为 13px | 新增 `.r93-card.r93-card, .r93-card.r93-card * { font-size: var(--font-size-body-2) }`。r96 只改了「卡内**裸文本**」的默认档，卡内仍混着 12px（`.r93-t12*` / `.r93-pre` / `.r93-wlink` / `.r93-clink` / `.r93-diffstar`）与 14px（`.r93-t14`）⇒ 同一张卡里 12/13/14 三档并存。实测卡内 **42 处文本全部落 13px** |
| ② | 「滚动到底部」应是胶囊按钮 + 文字色与图标色一致 | `.r93-tobottom`：`border-radius:8px` → **`999px`**；前景色 `--color-text-1` → **`--r93-ioc2`**；新增 `.r93-tobottom .r93-t14 { color: inherit }`。实测圆角 **999px**、图标与文案**同为 rgb(107,107,107) = #6B6B6B**（设计稿两者实测都是这个值） |
| ③ | 底部对话框相对上方内容两端都短了一截，所有内容模块要等宽 | 见 10.2：**三者宽度基准统一** + agent 卡行**撑满** |
| ④ | 底部对话框下面还有一行小灰色文字，请补充 | 见 10.3：`div.mt-8::after` 补回设计稿的统计行（640×16 / 12px / gray-5） |

### 10.2 ★ ③ 的根因与修法（宽度基准统一）

**侦查（`ev/p97c.sh`，同一份代码在两个视口各测一次）——「两端各短一截」只在宽视口出现**：

| 元素 | 1440 视口 | 2560 视口（改前） |
|---|---|---|
| `.r93-wrap`（内容列） | `[420, 860]` → 右 1280 | `[845, 1131]` → 右 1976 |
| `.r93-bottom` / `.r93-sb`（状态条） | `[420, 860]` → 右 1280 | `[840, 1141]` → 右 1981 |
| composer（输入卡） | `[420, 860]` → 右 1280 | **`[852, 1117]` → 右 1969** |

⇒ 1440 下**完全对齐**（`min-width:860px` 兜底，三者都取 860）；2560 下三者基准各不相同：
**输入卡比状态条两端各短 12px、比内容列短 6.5px** —— 这正是邵先生看到的「两端都短了一截」。

**根因**：三块都写的是**百分比**，但各挂在**宽度不同的父盒**上：

| 元素 | 父盒 | 与 main 内宽的差 |
|---|---|---|
| `.r93-wrap` | `.r93-scroll` 的**滚动内容盒** | `scrollbar-gutter: stable both-edges` ⇒ 左右各让 10px ⇒ **−20** |
| `.r93-bottom` | `.r93-pane` | **0**（基准正确） |
| composer | `div.mt-8`（hero 的 `w-full` 子盒） | hero 带 `px-6` ⇒ **−48** |

**修法（三条，使三者恒等于 `max(50% × main 内宽, 860px)`）**：

1. `.r93-scroll::-webkit-scrollbar { width: 10px }` —— 把滚动条宽度在本容器**显式钉死**（全站默认也是 10px），
   让下面的补偿有据可依；
2. `.r93-wrap { width: calc(50% + 10px) }` —— 补回 `both-edges` 两侧各 10px 的一半（+10 = 10×2÷2）；
3. hero `padding: 0 0 8px 0 !important` —— 清掉 `px-6`，使 `div.mt-8` = main 内宽（问候语已 `display:none`，无副作用）。

**实测（改后，同一份代码两档）**：

| 元素 | 1440 | 2560 |
|---|---|---|
| `.r93-wrap` / `.r93-bottom` / `.r93-sb` / `.r93-agents` | `[420, 860]` → 右 **1280** | `[840, 1141]` → 右 **1981** |
| composer（`div.mt-8 > div`） | `[420, 860]` → 右 **1280** | `[840, 1141]` → 右 **1981** |
| `doc` / `win` | 1440/1440 · 900/900 | 2560/2560 · 900/900（**无横向溢出**） |

**同时修掉的第二处「短一截」**：4 张 agent 卡原本 `flex:none`（按内容宽左对齐），
1440 下只铺到 `..1220`（右端留 60px），2560 下 `agentSpan [840, 1616]`（**右端留 365px**）。
设计稿 PNG 实测该行 4 张卡外框 = `x 171 | 361 ‖ 369 | 538 ‖ 545 | 742 ‖ 749 | 1004`
（第 4 张**顶到内容列右缘**）⇒ 设计稿本来就是**填满**的。改 `flex: 1 1 auto; min-width: 0`
（按内容宽成比例吃掉剩余空间，保住设计稿「四张不等宽」的比例，而不是平分）：
实测 1440 `229/205/217/191`（合计 842 + 3×6 gap = 860）、`agentSpan [420, 1280]` ✔；2560 `agentSpan [840, 1981]` ✔。

### 10.3 ★ ④ 的取数与做法

设计稿 **`raw/design-1393-18748.html` 里有这个节点**：`fw647:20893`「text/text」= **640×16**，
`text='{"中电金信":"2 轮 · 27 步 · LLM 3m36s · 工具调用 7.2s · 首 token 平均 0.8s · 159 tok/s · 缓存命中 96% · 输入 1M tok · 输出 31.1K token"}'`；
`raw/design-rgb.png` 逐像素：墨迹行 **y 5126..5136**、x **265..903**（中心 584 = 内容列 165..1004 的中心 ⇒ **居中**）。
色：笔画最深 **(169,169,169) = #A9A9A9 = DS 色阶 gray-5**（不是 `--color-text-4` 的 gray-4 #C9C9C9）。

**做法 = 纯 CSS 伪元素**（零 DOM 注入，React 重渲染拿不掉）：

```css
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8::after {
  content: '2 轮 · 27 步 · … · 输出 31.1K token';
  font-size: var(--font-size-body-1); line-height: 16px; color: var(--r93-meta); white-space: nowrap;
}
```
`div.mt-8` 是 `flex flex-col items-center gap-2` ⇒ 伪元素天然成为**第 2 个居中 flex 项**，
与输入卡的间距正好是容器的 `gap` = **8px**（设计稿实测 8.5px）。
新变量 `--r93-meta: rgb(var(--gray-5))` —— 直接引三元组，暗色档自动跟色阶翻转（暗色 gray-5 = #868686），
故**只在浅色档声明一次**。hero 的 `padding-bottom` 由 12 → **8**（设计稿 artboard 底 − 统计行底 ≈ 7px）。
实测 `mt8` 高 154 → **178**；伪元素 `font-size 12px / line-height 16px / color rgb(169,169,169)`；`doc` 仍 900 = `win` ✔。

### 10.4 ★ 踩到的坑：`*` 不贡献特异性

首跑实测「卡内 **37 处 13px，唯独 5 处 `.r93-pre` 仍是 12px**」——
根因：**通配符 `*` 的特异性为 0** ⇒ `.r93-card *` 其实只有 **(0,1,0)**，与 `.r93-pre` 同级；
而 `.r93-pre` 写在它**之后** ⇒ 后写者胜。（`.r93-t12c` 等恰因写在**之前**才被覆盖，掩盖了这个坑。）
修法：把类名写两遍抬到 **(0,2,0)** ⇒ `.r93-card.r93-card, .r93-card.r93-card *`，与书写顺序无关。

**另**：新增的 `--r93-meta` 与 `::after` 规则**都没有触发门禁**（见 10.5）。

### 10.5 四查

| 查 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍：第二遍 base + conversation **双「已是目标态（无改动）」** |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical），与 r93 基线 `vd-r93c.txt` **逐字节相同**（17148 字节，`equal: True`） |
| 视觉/几何 | `ev/p97d.sh` 在 **1440 / 2560** 各测一遍（见 10.2 表）＋ `raw/r97-cmp.png`（设计稿 vs 实机**同尺度上下对照**）＋ `raw/r97-pill2.png`（胶囊 6× 放大）＋ `raw/r97-bottom2.png`（统计行） |

**回归排除**：`ev/p97f.sh` 在实机临时把卡内字号强制回 12px 再测一次 ——
12 张 `.r93-card` 的高度与溢出量**逐项完全相同**（含 2 张 `scrollHeight−clientHeight = 2` 的 tool-call 卡）
⇒ 那 2px 是 r96 及更早就在的，**不是本轮字号统一引入的**。

### 10.6 产物与回滚

`pages/conversation.html`：609969 → **613441 字符**（+3472；字节 642788；**LF 文本 sha `481d929d89bd`**）。
`pages/base.html`：**471444 字符**（**未变**，LF 文本 sha `c16308a00915`）。
新增 `mg-work/r93/before/conversation-r96.html` · `base-r96.html`（本轮前置基线）。
新增 `mg-work/r93/ev/`：`p97a.js/.sh/.txt/.json`（字号分布 / 按钮 / 横向 / meta 侦查）· `p97c.sh`（宽视口对比）·
`p97d.js/.sh` + `p97d-1440.json` `p97d-2560.json`（实测）· `p97e.sh`（基线对照，未跑通）· `p97f.sh/.txt`（字号回归隔离）· `vd-r97.txt`。
新增 `mg-work/r93/raw/`：`r97-after-full.png` · `r97-grid2.png` · `r97-bottom2.png` · `r97-pill2.png` · `r97-pill.png`（设计稿胶囊 6×）· `r97-meta.png`（设计稿统计行）· `r97-cmp.png`（上下对照）· `r97-agentrow.png`（设计稿 agent 行）· `r97-bandA/B.png`。
回滚：`cp mg-work/r93/before/conversation-r96.html pages/conversation.html`（→ r96 态），或 `apply93.py --revert`（整代）。

---

## 十一、r98（同日第八轮）：会话详情页 3 条（**就地返工 `apply93.py`**）

### 11.1 三条需求 → 落地

| # | 邵先生原文 | 落地 |
|---|---|---|
| ① | 整个对话内容部分的 **14px 字号统一调整为 15px** | 新增 `.r93-t14, .r93-t14m, .r93-t14b { font-size: calc(15px * var(--ui-fs-ratio)) }`（写在三条定义**之后**、**只写 font-size**）⇒ 内容区 **59 处落 15px**；`.r93-card.r93-card *`（0,2,0）仍把卡内压回 13px ✓ |
| ② | 单轮末尾 `r93-rateline` 模块**下面间距 48px** | `.r93-wrap` `padding: 32px 0 24px` → **`32px 0 48px`**（rateline 是本轮最后一个 `.r93-it`：实测 `isLast=true`、无 `nextSibling` ⇒「下面间距」就是内容盒下内距） |
| ③ | `r93-diff` 样式还原不到位（颜色 / 间距…），对比设计稿像素级还原 | 整卡重做（下详） |

### 11.2 ③ 的设计稿取数（`1393:18681`「容器 252」= 840×300）

**双源**：`raw/design-1393-18748.html`（节点样式）+ `raw/design-rgb.png`（逐像素扫描，`ev/` 外的一次性脚本）。
坐标一律**卡内相对值**。

| 部位 | 设计稿 | 旧实现 | 本轮 |
|---|---|---|---|
| 卡底 | 表头带 `#F5F6F7` + **列表纯白面板**（实测 y42..299 = 255,255,255） | **整卡 `#F5F6F7`**（列表区偏灰） | `.r93-diff{background:var(--color-bg-2)}` + `.r93-dhead{background:var(--r93-card)}` |
| 表头 | **40 高**（`容器 238`=822×28 @(12,6)）＋**底部 1px `#ECEEF2` 分隔线**（实测 y41） | `height:28`、无分隔线、`padding:6px 12px 0` | `height:40; padding:6px 6px 5px 12px; border-bottom:1px solid var(--r93-edge)` |
| 行 | 高 36、分隔线 `#F2F2F2`、**首行无上边线** | 7 行全带上边线（首行多一条） | `.r93-drow:first-of-type{border-top:0}` |
| 行内距 | **左 11 / 右 13**（文件名墨迹 x13；⋯ 盒 x801..825） | `0 36px 0 8px` | `0 13px 0 11px` |
| 数字列 | 右沿距卡内右沿 **54**；与 ⋯ 之间 **17** | gap 8、右沿距 69 | `gap:17` |
| ⋯ 字色 | 实测最深像素 **(31,31,31)** = text-1 | `--color-text-2`(78,78,78) 偏浅 | `--color-text-1` |
| ⋯ 悬停 | **白底 + 1px 描边**（实测盒 24×24、描边 (229,229,230)） | `--color-fill-2` 底 | `background:var(--color-bg-2)` + `box-shadow: inset 0 0 0 1px var(--color-border-2)` |
| +800 | 实测 **(48,149,59)** = `--r93-ok` | `--color-success-6` = (59,179,70) **偏亮** | `color: var(--r93-ok)` |
| -125 | (245,63,63) ✓ | 同 | 保持 |
| 按钮 | DS 次要按钮 small，外框 **70×28** | 宽度 72（DS 基类 1px transparent 边框占 2px） | `padding: 0 11px` ⇒ **70** |
| 表头图标槽 | `容器 236` 图标槽宽 **24**、字形左缩 2（墨迹 x14..27）、标题 `容器 168` @24 ⇒ 标题盒落在卡内 **36** | 图标盒 14 + gap 12 ⇒ 标题在 39 | 补 `.r93-dhead .r93-dh1 > .r93-iblk:first-child{margin-right:-3px}`（视觉间隙 12−3=9）⇒ 标题 **456** = 卡外左 36 ✓ |
| 表头数字组 | `容器 167` gap **8** | `.r93-dh1{gap:12}` 全 12 | 新增 `.r93-dh2{gap:8}` 包住 +800/−125 |
| 滚动条 | `矩形 219` = **6×128**、rgba(0,0,0,0.16)、圆角 6、列表内 (830,4)（即**右 4 / 顶 4**） | 无 | 新增 `<i class="r93-dsb">` + `.r93-dsb`（**静态装饰**，见 11.4） |

**设计稿「叠了 hover 态」**：`app.json` 那一行是**同时叠出来的悬停态**（行底 `#F5F6F7` + 文件名 primary `#3770F7` + ⋯ 白底描边盒）。
本页保持**真 CSS `:hover`**（不静态写死那一行），与 r93 的「变体叠放」教训一致（PLAYBOOK P3.24②）。

### 11.3 实测（`ev/p98b.js`，1440 / 2560 双档）

| 项 | 1440 | 2560 |
|---|---|---|
| `.r93-t14/.t14m/.t14b` | 15px / lh22 | 15px / lh22 |
| 内容区字号分布 | 12×49 / 13×42 / **15×59** / 14×2 | 同 |
| 卡内 `.r93-t14` | **13px**（r97 ① 未被吃掉） | 13px |
| `.r93-wrap` padding-bottom | **48px**（rateline 下缘 == 内容盒下缘 ⇒ 下方间距 = 48） | 48px |
| `.r93-diff` | `[420,3651,860,300]` bg `rgb(255,255,255)` / 边框 `rgb(236,238,242)` / r8 / pad0 | `[840,3629,1141,300]` |
| `.r93-dhead` | h **40**、bg `rgb(245,246,247)`、bb `rgb(236,238,242)` 1px、pad `6/6/5/12` | 同 |
| `.r93-dlist` | bg 白、h258、margin 0 | 同 |
| `.r93-dsb` | `[1269,3696,6,128]` → 右距卡内右沿 **4** ✓ | `[1970,3674,6,128]` ✓ |
| `.r93-drow` | h36 / gap **17** / pad `0 13 0 11` / **first btWidth 0** / second 1 | 同 |
| 右对齐账 | 卡内右 1279：⋯ 右 **1266**(−13) ✓、数字右 **1225**(−54) ✓、名左 **432**(+11) ✓ | 卡内右 1980：1967 / 1926 / 852 ✓ |
| 表头 | `.r93-dh1` **209×22**（= 设计稿 `容器 236` 尺寸）✓、标题 x**456** ✓、按钮 **70×28**、dacts **148** 右距 **6** ✓ | 同 |

**残留 14px 仅 2 处** = `撤销` / `审查` 两个 **DS `giencoder-btn-size-small`**（设计稿也是 14px，且按 r90 约定「适配层不改组件字号」⇒ 保留）。

### 11.4 顺带修掉的一个真 bug：`.r93-alink` 一直不是 12px

`.r93-bt { font: inherit }`（第 412 行）与 `.r93-t12`（第 363 行）**同为 (0,1,0)**，但 `body` shorthand **写在后面** ⇒ 后写者胜，
「任务完成，耗时28m12s」一直被撑成 14px。**设计稿实测它是 12px**：墨迹 x166..325 = **160px** ≈ 11 汉字 + 5 半角 @12px
（@14px 要 189px）。修法 = 在 `.r93-alink`（写在 `.r93-bt` 之后）补 `font-size: var(--font-size-body-1)`。

### 11.5 验收四查

| 项 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍 → 第二遍 base + conversation 双「已是目标态」 |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical），与 `vd-r93c.txt` **逐字节相同**（21882 字节，`equal: True`） |
| ★ 假阳性 | 首跑 77 条：新增注释里写了裸字号写法（`font-size: 15px`）⇒ 扫描器按字面计数 +1（**hex 检查会跳过注释行，字号检查不会**）⇒ 改措辞后归零 |

### 11.6 产物与回滚

`pages/conversation.html`：613441 → **616773 字符**（+3332；字节 647842；**LF 文本 sha `6cbeff3a126c`**）。
`pages/base.html`：**471444 字符**（**未变**，LF 文本 sha `c16308a00915`）。
新增 `mg-work/r93/before/conversation-r97.html` · `base-r97.html`（本轮前置基线）。
新增 `mg-work/r93/ev/`：`p98a.js/.sh`（侦查：字号分布 / rateline / 卡片几何）· `p98b.js`（实测，1440 + 2560）· `vd-r98.txt`。
新增 `mg-work/r93/raw/`：`r98-design-diff.png`（设计稿卡 2×）· `r98-design-below-rateline.png` · `r98-live-diff.png`（实机卡）· **`r98-cmp.png`（设计 vs 实机上下对照）** · `r98-after-full.png` · `r98-rateline.png` / `r98-rateline-crop.png`。
回滚：`cp mg-work/r93/before/conversation-r97.html pages/conversation.html`（→ r97 态），或 `apply93.py --revert`（整代）。

### 11.7 待拍板

1. **`.r93-dsb`（那条 6×128 滚动条）是本轮唯一「静态装饰」** —— 设计稿确实画了它，但本页列表只有 7 行、不滚动
   （r94 ⑤ 曾按您的要求删掉 `r93-card--ctx` 的假滚动条）⇒ **若要一并去掉，删 `.r93-dsb` 那条规则 + 模板里的 `<i class="r93-dsb">` 即可**。
2. 15px 是**字号档位之外**的值（DS 只有 body-3=14 / title-1=16）⇒ 只在本页适配层用 `calc(15px * var(--ui-fs-ratio))`，**未动 token**。
3. 卡内文案（差分卡标题 / 文件名 / 表格名等）现在比设计稿**大 1px**（设计 14 → 本页 15）：这是 ① 的必然结果，③ 只覆盖颜色 / 间距 / 结构。


---

## 十二、r99（十四条 · 会话详情页线上宿主微调）

> 载体：`pages/conversation.html` 的 `.r93-conv-host`。**r93 代未提交 ⇒ 全部就地返工 `mg-work/r93/apply93.py`**（不另起代数）。
> 零字面 hex（新增色一律进 `:root` 的 `--r93-*` 本地变量 + 暗色档）；幂等可复跑。

### 12.1 十四条 → 依据 → 落地值 → 实测

| # | 邵先生原话 | 设计稿依据 | 落地 | 实测（1440） |
|---|---|---|---|---|
| ① | 去掉「r93-dsb」假滚动条，需要时显示真滚动条 | `容器 251` 列表 840×260；`矩形 219` 6×128 rgba(0,0,0,.16) 是静态装饰 | 删 `.r93-dsb` 规则 + 模板 `<i>`；`.r93-dlist` 改 `overflow-y:auto` | `dsbCount=0`、`overflow-y=auto`、7 行 258 = `scrollHeight`（**平时不出现滚动条**，需要时才出） |
| ② | `r93-tobottom r93-bt is-on` 默认图标/文字深一级 + 整钮 hover 底色 | `1393:18683` Button 120×32，图标与文字同为 (107,107,107) | `color: var(--color-text-2)`（gray-8 #4E4E4E）+ 新增 `:hover{background:--color-fill-1; border-color:--color-border-3}` | `color=rgb(78,78,78)`；hover 规则文本已进产物 |
| ③ | `r93-rbtn r93-bt` 与间隔线贴在一起 | `容器 247`（`1393:18599`）逐件坐标：图标组 0..56 / **直线 46 @68** / Link 80..222 / **直线 47 @234** / ⋯ 盒贴容器右沿 | `.r93-rrate + .r93-rline{margin-left:-2px}`；`.r93-rline + .r93-rbtn{margin-left:-14px}`（把 ⋯ 留在原位） | 线1 **68**、速率 81..224、线2 **234**、⋯ 盒 233..257（与设计稿 68 / 234 / 231.5 齐平） |
| ④ | `r93-iblk r93-i14` 图标异常 | `fw647:16336 → svg_1d5c65e3.svg`（SKILL，14×14，#868686） | ★ **删除 `fit_viewbox()` 假修正**（详见 12.3 踩坑一） | SKILL 折叠头渲出完整**扳手**字形；`.r93-i14` 的 viewBox 直方图 = `{14:27, 12:15, 16:21}`，**无异常值** |
| ⑤ | 页面底部点击还有波点涟漪 | — | `html[data-r93-page='conversation'] .r74-ripple{background-image:none!important}`（不改脚本：r74/r79 的 `document` 捕获段监听仍在跑，脚本仍会 `animationend` 自毁） | 探针插入 `.r74-ripple` 实测 `background-image = none` |
| ⑥ | `r93-artlabel r93-t12l` 字号也该是 15px | divider `fw647:19683`；墨迹 x558..611 = 54px / 字距 14 ⇒ 设计稿 14 档 | `.r93-artlabel` → `calc(15px * var(--ui-fs-ratio))` | `fs=15px`，墨迹宽 60 |
| ⑦ | `r93-drow` 行要支持右键菜单，且与右侧「更多」是同一个菜单 | 设计稿未画（交互态）⇒ 走 DS 下拉契约 + 本仓 `task-detail.html` 的 `.td-ctx` 已落地范式 | 新增 `.r93-ctx*` 约 55 行 CSS + `wire()` 内 `CTX_ITEMS`/`buildCtx`/`openCtx`/`closeCtx`；contextmenu 与 `.r93-dmore` **共用同一 DOM 节点** | 面板 182×153 / 4 项 + 1 分隔线 / `labelFs=14px` / `z-index=1000`；`viaMoreBtn=true`、`sameNode=true`、`Esc` 可关 |
| ⑧ | `r93-fc r93-bt` 点击展开/收起有跳动 | 展开头 `容器 161` 175×22、`direction/down` 14×14；`容器 163` gap 4 ⇒ 文字 @18 | 折叠头 chevron `r93-i12`→`r93-i14`；助手头 alink chevron 同改 | 三态（开/关/再开）：`headH` 恒 22、`icW/icH` 恒 14、`txX` 恒 18、`headTop` 恒 0、`reopenMatches=true` ⇒ **无跳动** |
| ⑨ | 复制按钮 hover 底色不对；点击后变绿色勾勾 | 悬停行里 ⋯ 盒 = 24×24 白底 + 1px (229,229,230) 描边；`fw647:14502` 节点名即「点击后变成绿色的勾勾图标」 | `.r93-ib:hover` 改「白底 + 内描边」（原 `--color-fill-2` 在灰卡里比卡底还深）；`data-r93-copy` 委托 + `is-copied` 换 `IC('ok')`，1.6s 还原 | `copied=true`、`color=rgb(48,149,59)`、图标换成勾、`is-copied` 带 0.18s 弹出动效 |
| ⑩ | `r93-t14 r93-c2` 顶部间距改 4px；`r93-card` 字号 15px | `容器 201` 822×208 = 20 + 3×(22+4+22) + 2×12 + 20；`容器 200` 252×48 @(20,20) | `.r93-card` 字号 → 15px；新增 `.r93-card--quiz{padding:20px}`；答行 8→4px、问行 14→12px | `c2MarginTop=4px`、`cardFs=c2Fs=15px`、`quizPad=20px`、**`quizH=208`（与设计稿一致）** |
| ⑪ | `r93-alink r93-bt r93-t12` 字号 15px | `fw647:14447` Link 164×22 gap2；墨迹 x166..311 = 145px（7 汉字 + 6 半角） | `.r93-alink` 12→15px | `fs=15px`、盒高 22 |
| ⑫ | `r93-pill r93-t12` 尺寸等细节与设计不符 | `容器 25`（`fw647:14402`）内距 1/6 + `box-shadow 0 1px 2px #D0D7EA` + 圆角 3 + 白底；PNG 文字 **(52,145,250)** | 新增 `--r93-pillc:#3491FA`（暗色 `#6BA6FF`）；`.r93-pill` 摘掉 `.r93-t12`，自写 `15px/20px`（盒高保 22）；投影保留 | 盒 158×22 / `fs=15px` / `pad=1px 6px` / `radius=3px` / 白底 / `color=rgb(52,145,250)` / shadow ✓ |
| ⑬ | `r93-asst` 底部线条深一级 | `直线 28` 实测 (242,242,242) ⇒ 按「深一级」 | `--color-border-1` → **`--color-border-2`**（gray-3 = 229） | `border=rgb(229,229,229)` |
| ⑭ | `r93-iblk r93-i14` 图标不对 + 与左侧时间间距不对 | `容器 180`（`1393:18477`）95×24：时间墨迹 0..28 / 按钮盒 **41..65** / **71..95**；PNG 14×14 盒逐像素分离 | **重画 regen 图标为 14 栅格**（旧件是 16 栅格小圆弧，压进 14px 盒只剩 9.4px）；umeta `margin-right:13px` + `+ .r93-ib{margin-left:6px}` | `regenVB=0 0 14 14`；`gapTB1=13`、`gapB1B2=6`；与设计稿并排对照形状一致（宽扁弧 + 左下箭头 vs 设计稿同款） |

### 12.2 本轮新增的设计稿权威取数（以后直接引这两处，别再靠目测）

* **`1393:18599`（容器 247，256×24，`left:164; top:4664`）—— rateline 的绝对真值**：
  子件 `1393:18598 容器 246`(0, 56×24，内含两枚 24×24 icon-wrapper，gap 8) · `fw647:19598 直线 46`(left **68**, top 5) ·
  `fw647:19591 Link`(left **80**, 142×24，内含 `svg_bff3c9ce` 14×14 + `Token 速率：256/s` 14/24 MiSans) ·
  `fw647:19599 直线 47`(left **234**, top 5) · `fw647:19681 icon-wrapper`(24×24)。
  ⇒ 线高 14（24−5×2）、图标组 0..56、线1 68、速率 80..222、线2 234。**这组数字本轮直接用于验收 ③。**
* **`1393:18477`（容器 180，95×24）—— umeta 的节点表**：`fw647:14502` 24×24(props 尺寸14，节点名「点击后变成绿色的勾勾图标」) ·
  `fw647:14503 icon-wrapper` 24×24(props 尺寸14) · `fw647:14497` `15:26` 12px MiSans/16 `#868686`。
  ⚠️ 导出里两枚按钮是 DS 实例、**没有内部图形**，且 `容器 180` 的祖先全是 flex（`left/top` 不累积）
  ⇒ **位置与形状只能靠 `raw/design-rgb.png` 逐像素反推**（1 design px = 1 png px，`board(x,y) → png(x+1,y+1)`，仅对**整页导出节点**成立）。
  PNG 实测：时间墨迹 x910..938 / 按钮盒 950.5..974.5 / 980..1004（右沿贴气泡右缘 1004）⇒ 间距 **13 / 6**。

### 12.3 ★ 两个踩坑（都写进了补丁注释）

**踩坑一（严重）：`fit_viewbox()` 是假警报，还把两枚正确图标改坏了。**
首版我按「字形包围盒落在声明框外 > 35%」自动重算 viewBox，`apply93.py` 报 `svg_1d5c65e3`（SKILL）越界 90%、`svg_e08b0fbd` 越界 92%，
于是把两者改成 `11.784 -0.05 14.225 14.225` / `11.955 -0.385 14.429 14.429`。
**真因**：这两个文件的 `<path>` 上挂着 `transform="matrix(-1,0,0,1,26,0)"`（x → 26−x 镜像），镜像后字形正好落在 x[1,13] / y[1,13]，
**原本就与 `viewBox="0 0 14 14"` 严丝合缝**；而 `glyph_bbox()` 只读 `d` 里的数字、**不认 transform** ⇒ 算出「越界 90%」，
一改反而把字形推出框外，渲出来只剩左沿一条 **1px 残片**（本轮目视取证时抓到，见 `raw/r99v-skillbig.png`）。
处置：**整段删除** `glyph_bbox` / `fit_viewbox` / `_r3`，并在原处留注释。
按 transform 感知重体检 78 个源文件：真正越界的只有 4 件 DS 组件内部结构图
（`svg_19c68c88` / `svg_38cbaeab` / `svg_b49ce54b` / `svg_31dd5c7e`，**全部未被引用**）。
⚠️ 本页共 **8 个** 源文件带 matrix（含 4 个 `matrix(0,1,-1,0,1,-1)` 的 90° 旋转）⇒ **按裸坐标推算几何必翻车**；
「自检脚本自己的假警报」老规矩：先在基线同口径复跑再定性（PLAYBOOK P3.15）。
> 教训：**改了「自检/自动修正」逻辑后，必须目视复核一个受影响的样本**——本轮如果只看探针数字（`vb` 已变成 14.225 之类），会以为修好了。

**踩坑二（低频）：`.r93-ctx` 量到 175px 不是 bug。**
`.r93-ctx.giencoder-dropdown-popup` 写死 `width:182px`（与 `task-detail` 的 `.td-ctx` 同参），但 `getBoundingClientRect()` 报 **174.72**。
原因是开合走 `scale: .96 → 1` 的 0.2s 过渡，**探针在过渡中取值**：`182 × 0.96 = 174.72` ✓ 分毫不差。
⇒ 量弹层尺寸必须**等过渡结束**（或 `transition:none` 后再量）。

### 12.4 验收四查

| 项 | 结果 |
|---|---|
| 幂等 | `apply93.py` 连跑两遍 → 第二遍 base + conversation 双「已是目标态」 |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical），与基线 `vd-r93c.txt` **逐字节相同**（21882 字节） |
| 双视口视觉 | 1440 + 1500 全页截图 + 逐区域滚动裁片（`r99v-*.png`）+ 设计稿并排对照（`r99-final-umeta-cmp2.png`） |

### 12.5 产物 / 探针 / 回滚

* 主改：`mg-work/r93/apply93.py`（icon 表 `regen` 重画；删 `fit_viewbox` 三函数；CSS 增 `.r93-ctx*` 与若干 r99 规则；`wire()` 增复制成功态 + 右键菜单两块）。
* 产物：`pages/conversation.html` 631381 → **631287 字符**（r99 起：616773 → 631381 → 631287；两次净变化 +14608 / −35 / −59）。`pages/base.html` 未变。
* 新增探针：`ev/p99a.js`（侦查）· `p99b.js/.sh`（14 条复查）· `p99c.js/.sh`（umeta 图标几何 + rateline 线↔⋯）· `p99d.js/.sh`（右键菜单展开截图）· `p99e.js/.sh`（全元素矩形）· `p99f.sh`（逐区域滚动截图）· `p99g/h/i/j`（SKILL 图标隔离渲染取证）· 读数 `vd-r99b.txt` / `vd-r99c.txt`。
* 新增裁片：`raw/r99-*.png`（before/after 全页、菜单、umeta、rateline、双视口、`r99v-m1~m3` 拼图、`r99v-icontest.png` 图标隔离测试页）。
* 新增隔离测试页：`ev/icontest.html`（把单个内联 SVG 抠出来渲染，断「是图标本身坏还是宿主 CSS 坏」——本轮靠它定位了镜像 transform）。
* 回滚：⚠️ **r99 是就地返工同一代（r93），`before/` 里没有 r98 终态快照**（该代只存了 `conversation-r96.html` / `conversation-r97.html`）。
  两条可用路径：① 定点删掉 `apply93.py` 里标 `★ r99` 的段落（脚本体位是「先 `strip_all(当前页)` 取净底再注入」⇒ 改完**直接重跑即自愈**）；
  ② `apply93.py --revert` 回到 r93c 快照（更早十拍，会一并丢掉 r94~r99 全部微调）。
  已补存本轮终态为下一轮基线：`mg-work/r93/before/conversation-r99.html`。

---

## 十三、r100（八条 · 会话详情页 · 就地返工 `apply93.py`）

邵先生原话（逐字）：

> 1、"GienX"改成"GienCoder"；
> 2、所有"r93-card"容器内的字号都改成14px；
> 3、"滚动到底部"按钮hover时边框颜色不要变化，图标和文字颜色再变为深一级的颜色即可；
> 4、"r93-dlist"的item整行都应该可点击，注意鼠标指针的形态；
> 5、"r93-agent r93-agent2 r93-bt"这种小卡片hover时加个浅灰底色即可，边框颜色不要变；
> 6、"r93-ndesc r93-t12h"这种文字行是有背景底色的，请对比设计稿；
> 7、"class="r93-fh r93-bt""这个折叠后前面的图标异常，请检查；
> 8、"调用 5 个工具"这个分组下面时分层级的，可以一级一级的点击展开和折叠，并且有层级连接线。

### 13.1 逐条落地与实测（1440，`ev/p100b.log`）

| # | 落地 | 实测 |
|---|---|---|
| ① | **文案更名**：`apply93.py` 模板里助手名 `<span class="r93-t14b">GienX</span>` → `GienCoder`、用户回话「这个 GienX 桌面 GUI 的左侧栏」→ `GienCoder`；`main()` 新增 `2b` 步把本仓最后一处可见文案（`task-detail.html` 的「来源需求」链接标题）一并更名，`--revert` 有对称逆操作 | `gienxCount=0` / `giencoderCount=4` / `ahdName="GienCoder"` / 回话=`"这个 GienCoder 桌面 GUI 的左侧栏"` |
| ② | `.r93-card` 与 `.r93-card.r93-card, .r93-card.r93-card *` 两条 **15px → 14px**（写法仍 `calc(14px * var(--ui-fs-ratio))` 以保住字号杠杆） | 卡内字号直方图 `{"14px":106}`（r99 是 `{"15px":106}`）；抽样 `.r93-pre` / `.r93-chead .r93-t12` 均 **14px** |
| ③ | `.r93-tobottom:hover` 撤掉 `border-color: --color-border-3`，前景色由默认 `--color-text-2` 再深一级到 `--color-text-1`；底色沿用 `--color-fill-1` | hover：`color=rgb(31,31,31)`（默认 rgb(78,78,78)；深一级 ✓）· **`border=rgb(229,229,229)` = 默认值（未变 ✓）** · `bg=rgb(247,247,247)` |
| ④ | `.r93-drow{cursor:pointer}`；`wire()` 的点击委托改成「命中整行即开菜单」——点 `⋯` 时菜单贴按钮左下角、点行内其余位置贴整行左下角（同一实例） | 7 行 `cursor` 全 `pointer`；点 `.r93-dname` ⇒ 菜单 `open=true`、**182×159**、4 项 + 1 分隔线；`Escape` ⇒ `open=false` |
| ⑤ | `.r93-agent:hover` 撤掉 `border-color`，改 `background: --color-fill-2` | hover：`bg=rgb(242,242,242)`（浅灰 ✓）· `border=rgb(229,229,229)` = 默认（未变 ✓） |
| ⑥ | `.r93-ndesc` 由「`width:100%` 居中文字」改成**浅灰圆角胶囊**：`width:fit-content; margin:8px auto 0; height:24px; padding:0 12px; border-radius:var(--border-radius-xl); background:var(--color-fill-1)` | 两行：`bg=rgb(247,247,247)` · `radius=12px` · `pad=0 12px` · `h=24` · `fs=12px`；盒 757 / 296，中心 x=849.5 / 850（内容列中心 850 ✓ 居中） |
| ⑦ | 「调用 5 个工具」展开层里的内嵌 `Tool call` 层**改成走同一个 `fold()` 工厂**（原来是手写静态头，chevron 槽写死 `.r93-i12` 且**没有折叠头** ⇒ 比全页其它折叠头小 2px、且折不起来）；工厂的 `col`（折叠头）补 `ctmeta` 选项，把设计稿 `fw647:18138` 里那截「• str_replace_editor · …」元信息一起渲染；`.r93-fc` 补 `max-width:100%` | 展开头槽 `r93-iblk r93-i14 r93-cv`、**slotW=14**（原 12）；折叠头槽 `r93-iblk r93-i14 r93-c3`、**slotW=14**，文案 `Tool call • str_replace_editor · …`；点一下 ⇒ 内层 `foldH 166→22`、`cardH 132→0`；再点 ⇒ 复原 `foldH=166`、`cardH=132` |
| ⑧ | 展开层包一层 `.r93-tree`：一条贯穿 L1 组的 **1px 竖导线**（`::before`）+ **每个 L1 子项一枚 8px 横向肘节**（`.r93-fold::before` / `.r93-sumrow::before`，`left:-12px; top:11px`）；`.`r93-sumlist` 的原竖线交给 `.r93-tree` 统一画 | 层级缩进 **L0=420 / L1=438 / L2=456**（相对 = 0 / 18 / 36；汇总行 438 = L1 ✓，与设计稿 `容器 163/220`@0、`容器 218/219`@18、`容器 217`@36 完全一致）；导线 `1px / rgb(229,229,229)`、肘节 `8px / -12px / top 11px / rgb(229,229,229)`（内层折叠块与 4 行各一枚）；一级一级点开收起见 ⑦ |

### 13.2 本轮新增的权威取数（已写入 PAGES P3.11g ⑩ / PLAYBOOK P3.31）

* **⚠️ 设计稿 HTML 导出**会**丢掉 DS 实例自身的背景/圆角**（`容器 225` 的两行 ndesc 在
  `raw/design-1393-18748.html` 里只有 `width/height`，没有底色也没有圆角）⇒ **必须回 PNG 逐像素扫**。
* `.r93-ndesc` 胶囊（PNG 逐像素，`board(x,y) → png(x+1,y+1)`）：
  `fw647:18372` 底 x195..972 / y3355..3378 = **778×24**，墨迹左内距 13 / 右内距 13；
  `fw647:18418` 底 x434..733 / y3433..3456 = **300×24**，墨迹左内距 13 / 右内距 14
  ⇒ **底 = 文字宽 + 两侧 12px 内距**；底色实测 **rgb(247,247,247) = `--color-fill-1`（gray-1）**；
  圆角由角部灰度剖面反解 ≈ **12px = `--border-radius-xl`**（24 高、取到上限 ⇒ 视觉全圆角）。
* `1393:18521 容器 221`（调用 5 个工具，840×404）的层级缩进：折叠头 / 展开头 **left 0**；
  `容器 218`（内嵌 Tool call 块 822×200）**left 18**、其代码卡 `容器 217`（804×132）**left 36**；
  `容器 219`（4 行汇总清单 305×124 @ top 246）**left 18**。**设计稿本身没有画连接线**
  （PNG 在该 x 区间只扫到卡片底 `#F5F6F7` 与卡片描边 `#ECEEF2`）⇒ 连接线是邵先生本轮新增要求。
* `容器 218` 内部两个 `Link` 是**同一节点的两种状态叠在一起**（`fw647:18138` 折叠态 424×22 带
  14px tool 图标 + 文案 + 点 + 元信息；`fw647:18151` 展开态 424×22 带 chevron + 文案 + 点 + 元信息）
  —— 又一次「变体叠加」陷阱 ⇒ 实现里只保留一个，由 `data-open` 切换。

### 13.3 本轮踩坑

1. **`fold()` 工厂的 `o.mt ? …` 会把 `mt:0` 当假值** ⇒ 内嵌层退化成默认 16px 上边距。
   已改 `o.mt != null`（既有调用全传真值，行为不变）。
2. **绝对定位伪元素不算 flex item**：`.r93-fold` 是列向 flex，肘节用 `::before + position:absolute`
   才不会被当成 flex item 把折叠头挤下去（已在 CSS 注释里留痕）。
3. **`.r93-sumlist::before` 原来是「局部」竖线**（只覆盖 4 行清单）⇒ 本轮把画线的职责上移到
   `.r93-tree`，`sumlist` 只留排布，避免两段线在接缝处断开。

### 13.4 验收四查

* **幂等**：`apply93.py` 连跑两遍 —— 第二遍 `base.html` / `conversation.html` 双「已是目标态（无改动）」✓
  （`task-detail.html` 的更名也已收敛：第二遍 `changes` 里不再出现）。
* **语法**：`python mg-work/check-syntax.py pages/*.html` ⇒ **10/10 通过**（conversation `script=9 style=15`）。
* **门禁**：`python verify-design.py ./pages` ⇒ 输出与基线 `ev/vd-r93c.txt` **二进制逐字节相同**
  （`cmp` 通过；21882 字节，66 🟡 / 10 🔵 / 0 🔴）。⚠ 跑完已 `git checkout -- pages/gaps.log`
  并 `git clean -fd mg-work/kanban/r13/chk/`。
* **实测**：1440 全量读数（`ev/p100b.log`）+ 真鼠标 hover 三处（滚动到底部 / agent2 / dlist 行）
  + 真鼠标点击（整行开菜单、内层折叠开合）+ 视觉取证裁片。

### 13.5 产物与回滚

* 主改：`mg-work/r93/apply93.py`（CSS 6 处 / 模板 4 处 / `wire()` 1 处 / `main()` 1 处新增更名步）。
* 产物：`pages/conversation.html` **631287 → 634719 字符**（+3432；LF 文本 `sha 60165e90308e`）；
  `pages/base.html` **471444 未变**；`pages/task-detail.html` **766710 → 766714**（+4，仅更名）。
* 新增探针：`ev/p100a.js/.sh`（侦查：ndesc / 树 / dlist / agent / 字号直方图）·
  `ev/p100b.js/.sh`（八条复查 + 三处真鼠标 hover + 整行点击开菜单 + 树开合）·
  `ev/p100h_top.js` / `p100h_agent.js` / `p100h_drow.js`（hover 读数）·
  `ev/p100ctx.js` · `ev/p100toggle.js` · `ev/p100shot.js/.sh` · `ev/p100shot2.js/.sh` · `ev/vd-r100.txt`。
* 新增裁片：`raw/r100-before-tools5*.png` · `r100-d-tools5.png` · `r100-d-note2.png`（设计稿）·
  `r100-tools5-open/-collapsed*.png` · `r100-tree-line-zoom.png` · `r100-ndesc*.png` ·
  `r100-agents.png` · `r100-menu-rowclick*.png` · `r100-full-1440.png`。
* 回滚：① 定点删掉 `apply93.py` 里标 `★ r100` 的段落（脚本体位是「先 `strip_all(当前页)` 取净底再注入」
  ⇒ 改完**直接重跑即自愈**）；② `apply93.py --revert` 回 r93c（会一并丢掉 r94~r100 全部微调）；
  ③ 页面级 `cp mg-work/r93/before/conversation-r99.html pages/conversation.html`（= r100 前置基线）。
* 已补存本轮终态为下一轮基线：`mg-work/r93/before/conversation-r100.html`。
