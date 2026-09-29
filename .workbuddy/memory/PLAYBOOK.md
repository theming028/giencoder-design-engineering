# PLAYBOOK · 工作法详解

> `MEMORY.md` 的详情卷（**按需 grep，不要整读**）。索引见 `MEMORY.md`；
> 页面事实 / token 档位 / 标准配方见 `PAGES.md`。
> 已沉淀 skill：`design-pixel-measure`、`css-pseudo-state-evidence`、`motion-primitives-port`、`mastergo-to-html`。

---

## P1 改页面的硬规则（补丁脚本 + 自检铁律）

### P1.1 结构与替换
- 页面 HTML 内联在 **JS 字符串数组**里，属性引号是 `\"` —— 正则按 `\\"` 写。写成真实引号会让**整页 bundle
  语法错误**（交互全失效、控制台 `Cannot read properties of null`），脚本自身不报错、极难定位
  → 打补丁后**必须核对 `<script` / `</script>` 计数**。
- ⚠️★ **反解 JS 字符串数组必须逐行 `json.loads`**（r69 血泪）：`l.encode('utf-8').decode('unicode_escape')`
  会把非 ASCII 按 Latin-1 逐字节解释 → **整段中文变 mojibake**（`aria-label="æä»¶é¢è§"`），
  而 `.td-browse-tab` 等"看起来正常"的文案会掩盖问题。做法：剥尾部逗号 → `json.loads(t)` →
  断言 `'文件目录' in html and '摘要' in html and 'æ' not in html`。
  **只有 string-array 解出的 HTML 受影响**；从 `<style>`/`<script>` 块直切的片段本来就是对的。
- 替换内联 SVG **禁止** `<svg.*?</svg>` + `re.S`（跨元素吞并）→ 用 `<svg(?:(?!</svg>).)*?</svg>` +
  结构计数自检（如 `.td-sec-head` / `.td-file` 计数不变）。分组标题类替换必须**回填尾部捕获组**。
- 压缩 bundle 里**删 JSX 子树**（如清空 `children:[...]`）：禁用正则 `.*?`；写**括号配平扫描** `match_bracket(s,i)`
  （跳过反引号/引号字符串）定位配对的 `]` —— 天然适配各页变量名（`N.`/`j.`/`A.`/`k.`），可一次批量改全站同构模块。
  **保留外层容器宽度**（如 240px 空容器）可避免头部布局塌陷。
- 压缩 bundle 里改 JSX 内联样式：CSS 覆盖必须 `!important` 才能压过行内 `style`；行内硬编码的"手算居中值"
  （如 `marginLeft:91` = `(240−58)/2`）在宽度可变时必然失效 → 换 `justify-content:center` + 钉右元素改 `position:absolute`。

### P1.2 幂等三要素
- 改动一律走 `mg-work/rNN/applyNN.py`（幂等 + 自检），不要手改大文件。
- ⚠️ **「NEW 超集」陷阱**（r52 实锤，一次差点把页面改坏）：当某条替换的 `NEW` 是 `OLD` 的**前缀超集**时
  （OLD=`… width:32px… }`、NEW=`… width:28px… }\n<新增注释>`），第二次 `s.count(OLD)` 仍可能是 1 → **重复追加**。
  **两条对策必须同时用**：① 循环里**先判 NEW 标记（newmark）命中就 skip**，再判 `count(OLD)==1` 否则 `sys.exit`；
  ② 跑完**立刻再跑一次**，确认输出 `应用: 0 项 | 跳过: N 项`。回滚：`cp /tmp/rNN-backup/<page>.html pages/<page>.html`。

### P1.3 自检断言铁律
- 只允许 ① 标签级计数（`<style>`/`</style>`/`<script>`/`</script>`）② 针对"被改对象"的**精确增减量**。
- **禁止**"全文件关键词总数不变/等于 N" —— 同一 token 在别处合法出现（`--color-border-2`、`--td-line`），
  新增选择器必然改变词频，都会误报。最干净落法：用注释锚点切出本轮新增区块
  （`a=s.find('/* ★ 第 NN 轮…')` → `b=s.find(下一条既有规则前缀, a)`），只断言"区块内"残留为 0。
  既有内容里的同类写法**不属本轮范围，不得擅改**。
- ⚠️ **新增的注释里不能出现被断言的 token / 标签名**（r67 **一轮踩 3 次**）：① JS 注释写「SHIMMER_SPREAD /
  bindShimmer 已移除」→ 四个残留断言当场全炸；② CSS 块注释写「见页尾 DOT-SPOT v1 块」→ **提前命中 JS 块的 newmark**，
  JS 块被误判"已存在"而跳过；③ JS 块注释写「本块在 `</body>` 前执行」→ `</body>` 计数断言直接失败。
  ⇒ **注释只描述"做了什么"，不复述被删/被改/被断言的标识符与标签名。**
- **护身符**＝给补丁脚本加**元守卫**：检查新增块常量里 `</body>`/`</html>`/`<body`/`<style`/`</style>`/`<div`/`</div>`
  出现次数是否等于允许值（见 `mg-work/r67/apply67b.py` 自检 E）。**只能放「应消失」的 token**，新增文案不属此列。
- ⚠️ **"有意新增"的标签要用「精确增减量」**（注入一个脚本块 ⇒ `<script>`/`</script>` 各 **Δ+1**）；
  **页内本就存在的同名词只断言"改前→改后差值"**；**沿用他处声明的 token 要在本块内断言为 0**；
  **断言锚点要带定界符**（`@keyframes shimmer` 会数进 `@keyframes shimmer-mask` → 写 `@keyframes shimmer{`；
  `.kb-running{` 实际是 `.kb-running {` 带空格）；**复跑不能断言"净字节减少"** → 断言 `len(s2) <= n0`。
- ⚠️ **注释污染断言**：断言前先 `re.sub(r'/\*.*?\*/', '', out, flags=re.S)` 剥掉注释再比（r69 复查）。
- ⚠️ **断言锚点用"精确串"而非类名**：`data-td-browse-toggle` 在 JS 控制器里也出现（计数 +1）→
  断言改 `data-td-browse-toggle="1"`。
- ⚠️★ **基线标签数本身可能不配平 —— 别写「配平」断言**（r72 实测）：`task-detail.html` 的
  `<script` = **9** / `</script` = **8**，这**不是**改坏了：React bundle 里有一段**转义的**
  `<\/script>` 字面量（`EREGISTRY` 一带的运行时源码拼接），`s.count()` 数真标签时把它一并计入。
  ⇒ 断言只能写「**与基线一致**」或「**Δ = 0**」（`s.count(tag) - before.count(tag)`），
  后者对任何基线形态都成立，最稳。r72 第一版写了配平断言 → 当场误报，白跑一轮。

### P1.4 作用域与归属
- 替换锚点**必须带上足够长的上下文前缀**（否则命中同页其它同色元素）。
  **删除类改动先问页面归属**：9 个外壳页各有一份同构顶栏模块，改动前先用 DOM 核实目标页现状，
  不凭字面推断（用户对"擅自修改未指明的对象"极敏感）。

### P1.5 CSS 落地的坑
- ⚠️ **不能"许愿"新类名**：产物只编译了构建期用过的类，手写 `rounded-[8px]` / `gap-[48px]` **不会生成 CSS**。
  改样式只有两条路：① 复用已编译的类（如 `rounded-full` → `rounded-md`）② 在该页 `<style>` 里自己写规则。
- ⚠️ **Tailwind 编译产物的圆角反直觉**：页面里 `--radius: .625rem`(=10px) ⇒ `.rounded-md` =
  `calc(var(--radius) - 2px)` = **8px**、`.rounded-lg` = **10px**、`.rounded-full` = 9999px。
  **不要**按 Tailwind 默认（md=6 / lg=8）推理，先 `getComputedStyle` 实测。
- **`overflow: visible` 外壳里做 `translateX` 入场**会溢出并撑出横向滚动条 → 包一层同尺寸**透明裁剪窗口**
  （`flex:1 1 auto; min-width:0; overflow:hidden`，几何零变化），位移只发生在窗口内（r54 `.td-browse-slot`）。
- ⚠️ **行内 style 与「激活态」互斥**：常态/激活态若都写在元素 `style="…"` 上，`:focus-within` / `onFocus`
  类选择器**永远赢不了** → 必须把**常态也搬到类上**、行内 style 整个删掉（r54）。同款模块（base / task-detail / avatar）三页一起改。
- ⚠️ **绝对定位的 `::before` 会盖住 in-flow 内容**（绘制顺序在内容**之后**）→ 给同级子元素加
  `position: relative; z-index: 1`。泛化：**任何用 `::before/::after` 做背景层、又要透出同级内容的场景，先想绘制顺序。**
- **自建菜单与外壳同名类冲突**：每页 React 产物里已有一份 `.giencoder-dropdown-popup`（`animation: .2s popup-in`，
  播完 `opacity` 回落 0）→ 自建弹层必须**双类提权**（`.td-ctx.giencoder-dropdown-popup`）+ `animation: none`。
  子菜单定位直接抄 DS：`.giencoder-dropdown-submenu-popup { left: calc(100% + 4px); top: 0 }`（越界翻左）。
- ⚠️ **改 DS 组件样式**：① **去掉自带投影必须覆盖 `:hover` / `:active`**（`.giencoder-btn-secondary:active`
  特指度 (0,2,0) 高于裸类）→ 写 `.x, .x:hover, .x:active { box-shadow: none }`；但**不要**把 `:focus-visible`
  纳进来（`0 0 0 2px var(--color-primary-light-2)` 是键盘焦点环，a11y 要保留）。② **共享类名改尺寸必须按上下文限定**
  （`.td-browse-ico` 同时挂顶栏与 crumb）→ 改前先 `grep` 该类名出现次数。
- **组件在页面里「没样式」→ 先查这条 CSS 有没有被内联**：`pages/*.html` 是 Vite 单文件产物，DS 的 CSS **按需内联**，
  根因通常**不是**优先级问题而是**压根没内联**。排查 `grep -c '\.giencoder-xxx {' pages/X.html` → 没有则去
  **`gienx-templates/ui-controls.css`**（Select/DatePicker/日历）+ `components.css`（基础组件）+ `components/{slug}.json`
  （契约）抄，用 token 重写进页面 `<style>` 并注明「DS 源文件 + 为何偏差」；再 `grep -o '\.giencoder-[a-z-]*'` 反查全页同类遗漏。
- ⚠️ **复用既有 localStorage 记忆机制时，新态要"独立变量名 + 更高特指度复位"**：旧态规则可能位于新增规则之后且
  记忆里残留脏值 → 新增态用**双类特指度**（`.is-browse.is-swapped`）压过；宽度用**新变量**（`--td-browse-right-w`）
  **绝不复用** `--td-right-w`。测隔离性：故意写脏记忆再开侧栏，逐项断言布局。
- ⚠️ **`box-sizing: border-box` 下给「会收起到 0」的元素加边框，静止箱宽最小 = 左右边框之和**
  （r70 实测：抽屉静止宽从 `0` 变成 **2px**，白占布局；元素本身 `opacity:0/visibility:hidden`，看不见、极易漏过）。
  对策：收起态 `border-width: 0` + 展开态 `border-width: 1px`，并把 `border-width` 放进同一个 transition
  ⇒ 描边随宽度一起长出/收回，静止时真为 0。
  **验证方法：改前后读 flex 行各子项的 `getBoundingClientRect().width` 数组逐个比**（比截图快且精确）。
- ⚠️ **给边加「看得见的线」有两条路，先想清楚要不要动布局**：
  ① 真描边 `border: 1px solid c` → 有 1px 布局代价（border-box 下内容区 −2px）；
  ② 环 `box-shadow: 0 0 0 1px c` → 零布局代价，但语义上仍是投影。
  本仓既有惯例是**真描边**（详情页 `.td-right`、`.td-browse` 都是），沿用可保持一致的外观与语义。
- ⚠️★★ **`@container` 块必须排在本节所有「被它覆盖的基础规则」之后**（r71 实锤，症状极隐蔽）：
  同特异性 (0,1,0) 时**后出现者胜** → 若容器查询插在中间，会出现**同一个 `@container` 块「部分生效、
  部分失效」**：r71 首次落地时 `@container(max-width:560px)` 里 `.av-main-avatar` 生效了（104→72），
  而 `.av-main-grid` 没生效（实测仍 `147px 147px`）——因为 avatar 的基础规则在 `@container` **之前**、
  avatar-grid 的在**之后**（卡片网格段 / 行卡段 / 页脚段）。
  ⇒ **正解：整组容器查询（含注释）搬到该 `<style>` 块末尾**（`</style>` 之前）。r36 注释里本就写着
  「必须写在本节之后」这条约定，是 r71 新增规则时没把新覆盖对象的基础规则位置一起核。
  **排查口诀：容器查询"没生效"时，先 `find()` 比一下被覆盖规则的基础选择器位置 vs `@container` 位置。**
- ⚠️★★ **clamp / 钳位逻辑必须区分「期望值」与「生效值」，否则出现「棘轮」**（r71 实锤）：
  原代码只有一个 `panelW`，既当用户期望宽又当生效宽；`window resize` 处理里 `setPanelW(panelW, false)`
  把**被压缩后的值**写回期望位 ⇒ 一旦缩过就永久缩，视口放大也不回弹。
  **改前不暴露**是因为那时 `MIN_PANEL = DEF_PANEL = 641`，`clamp(641,641,641)` 恒等 ——
  **降低下限的那一刻，棘轮就被激活了**（这类"调整常量"的改动务必连带审查钳位方向）。
  ⇒ 正解：`wantPanel`（只由**恢复记忆 / 拖动 / 键盘 / 双击复位**改写）+ `panelW = clamp(wantPanel, …)`；
  持久化写 `wantPanel`（用户意图）而不是生效值。
  ⚠️ **调用点往往不止一处**：r71 有 3 处（`clampNow` / `setOpen` / 「显示文件目录」切换），
  第一轮只改了 2 处 → **自检断言要覆盖"旧写法清零"**（`count('setPanelW(panelW, false)') == 0`）才能抓到。

- ★★ **`hidden` 开关型浮窗的「进 + 退」动画，用 CSS 原生即可，零 JS**（r73 定稿）：
  ```css
  .pop { opacity:1; translate:0 0; scale:1;
         transition: opacity .16s C, translate .16s C, scale .16s C, display .16s allow-discrete; }
  .pop[hidden] { opacity:0; translate:0 4px; scale:.97; }          /* 退场目标值 */
  @starting-style { .pop:not([hidden]) { opacity:0; translate:0 4px; scale:.97 } }  /* 进场起跑点 */
  ```
  · `transition-behavior: allow-discrete`（写在 transition 简写里，如 `display .16s allow-discrete`）
    ⇒ 关闭时**先把动画播完再真正落到 `display:none`**；`@starting-style` ⇒ 打开时先给出 from 值。
  · 实测判据（Chrome）：关闭瞬间 `getComputedStyle(el).display` **仍是 block/flex**，
    且 `el.getAnimations()` 里能看到 `display` 这条 transition。`CSSStartingStyleRule in window` = 支持。
  · **`!important` 不影响该机制**：既有 `.pop[hidden]{display:none !important}` 照旧生效，
    过渡跟踪的是 computed 值变化，与声明是否 `!important` 无关（r73 实测通过）。
  · ⇒ 不必改 `el.hidden = true/false` 的既有 JS，省掉状态机 / `transitionend` 兜底 / 连点竞态。
- ⚠️★ **元素位置被 `!important` 钉死时，要动它请改 `translate`，别去抢 `left/width`**（r73 定稿）：
  `task-detail.html` 有一条 `body:has(.td-wrap) [role="tablist"] > span[aria-hidden]
  { left:62px !important; width:124px !important }` 把滑块钉在 dev 位，
  内联 `style.left` 写不动它（`!important` > 内联）。**translate 不在那些规则的管辖范围内** ⇒
  用 `translate: dx 0` 做位移叠加：既能实现跨页接力滑动，又**一行都不用碰上一轮留下的钉位规则**。
  ⚠️ 顺带记住 **CSS 独立属性与 `transform` 是复合关系**（顺序 translate→rotate→scale→transform）：
  元素靠 `transform: translateX(-50%)` 居中时，加 `translate: 0 4px` 不会破坏居中，两者叠加。

### P1.6 跨页模块移植工作法（r69 定稿）
1. **抽取**：先写 `buildNN.py` 从源页切出 `<style>` 块 / HTML 片段 / JS 函数，落成 `part-*.{css,txt,js}`，
   每一步都带结构断言（标签配平计数）。HTML 走 **`json.loads` 逐行**（见 P1.1 的 mojibake 陷阱）。
2. **CSS 抽取用「顶层 chunk 扫描」+ 白名单正则**，显式列 `DROP_HEADS` 丢弃源页专用规则；
   命中无关模块（如 `.td-more`）**直接丢**，不要"顺手带过来"。
3. **状态前缀改写**：把源页的状态类（`.td-root.is-browse`）换成目标页自己的（`.av-browse-on`），
   挂在目标页真正承载该状态的节点上（本页 = shell 的 `div:has(> main)` flex 行）。
4. **变量独立**：`--av-browse-w` 不复用源页的 `--td-browse-right-w` / `--td-right-w`（避免布局记忆串味）。
5. **token 补齐**：目标页缺的 `:root` 变量（`--td-panel-line`、`--td-hairline`）必须显式补 —— 否则 `var()` 无 fallback
   会让整条声明作废（见 PAGES.md §9.6）。
6. **两个 MutationObserver 争抢终位**：抽屉脚本与预览栏脚本都会往 `hostRow` 末尾插节点 → 无限互踢。
   正解：`place()` 前四行「命中即早退」覆盖**完整形状**（`split.previousElementSibling === drawer && slot.previousElementSibling === split`），
   命中即 `return true` **不产生新变更**；未命中时**无条件 `insertBefore`**（幂等，不依赖相对位置）。
7. **Esc 分层裁决靠注册顺序**：捕获段同相时按注册顺序跑 → 后注入的脚本**必须插在更早的脚本之前**
   （r69：`#av-browse-js` 必须排在 `#av-chat-js` 之前），并用 `stopImmediatePropagation()` 吃掉自己那一层。
8. **React 内联宽度优先级最高** → 覆盖必须 `!important`（`.av-browse-on > aside:first-child { width:0 !important; … }`）。
   目标节点若自带 `transition-all duration-200 ease-[cubic-bezier(0.22,1,0.36,1)]`，收缩动画是**天然的**，无需自加。
9. **验收走三段式跨页 diff**：同一支探针在两页各跑一次，逐字段对照 ——
   容器宽度类差异是**必然的**（一个固定 641、一个撑满），只要**样式属性逐字节相同**即算对齐。

### P1.7 反解 bundle 时的取范围
- 从 string-array 里取一个 DOM 子树，**起点取到容器开标签、终点必须取到容器闭合那一行**
  （r69 教训：只截到 `</aside>` 会漏掉外层 `</div>`，片段标签不配平 → 必须 `assert html.count('<div') == html.count('</div>')` 等 7 个标签全配平）。

### P1.8 跨页同步改 DS 组件（9 页同构编译产物）工作法（r70 定稿）
DS 组件的 CSS 是**每页内联一份、内容逐字节相同**的编译产物（如 `.giencoder-btn-*` 全站各 28 处 `--btn-ring`）。
要动它就必须 9 页一起动，否则设计系统分叉。步骤：
1. **先摸分布**：`grep` 统计目标片段在 `pages/*.html` 的**出现次数**，确认"9 页各 N 处、内容相同"。
2. **抄出精确 OLD 串**（连空白一起），用 `s.count(OLD)` 在 9 页上预校验**必须恰好 1 次**
   （多一次少一次都说明串选窄了/选宽了）。
3. **一个脚本带三种 job 列表**：`AVATAR_JOBS` / `TD_JOBS` / `OTHER_JOBS`，同一份 `patch()` 引擎跑全站
   （见 `mg-work/r70/apply70.py`）。引擎固定四段：**元守卫 → newmark 命中即 skip → OLD 命中数校验 → 自检断言**。
4. **每个 job 必须有独立 newmark**（`★ 第 NN 轮第 M 项`）；没有新注释的 job 就**用 NEW 串自身当 newmark**。
   ⚠️ 同一轮里多个 job **不能用同一个 newmark**（否则第一个跑完就把后面的全"跳过"了）。
5. **断言要按页分档**：只有本页改过的项才断言，其余页只断言 job 自身的落地结果。
6. **收尾必做**：`verify-design.py ./pages` + 与**本轮改前基线**（`/tmp/rNN-backup/*.html` 覆盖回一份 pages 副本）
   **逐条 diff**；顺手 `git checkout -- pages/gaps.log`。
7. ⚠️ **本轮踩到的两个断言过宽**：① 断言某条 CSS 声明 `count == 1`，但该声明在**本轮之前**就已存在 1 处
   （`.td-browse` 也用同一条 `border: 1px solid var(--td-panel-line);`）→ 改成 `== 2` 或写成"含本轮的增减量"；
   ② 断言裸 hex `'#DAE3ED' not in s`，但它在外壳路由分支（`` i==='dev'?`border-[#DAE3ED]` ``）
   和 Tailwind 工具类里各有一份 → **断言必须用完整 token 对**（`--td-panel-line: #DAE3ED`）。

---

## P2 读懂需求措辞（用户会刻意区分）

> 「其实"td-browse-ico"和"td-browse-add"把**容器**尺寸调整为 28px**即可**」
> 「"td-right-acts"**容器内的几个图标本身**的尺寸调整 14px」

- 「**容器** … 即可」⇒ 只改外框（width/height），**图标尺寸不动**。
- 「**图标本身**」⇒ 只改 `<svg>` 的 width/height，**外框不动**。
- 「小两号 / 大一点 / 再加大点」= **只缩/放 svg，别动图标框**（框宽决定文字起始 x，动框会破坏逐像素对齐基线）。
  r61 实测：`.td-more-ico svg` 16→12px 后 label 起点仍是 **37px**、菜单仍是 130×76。
- 「**只加/只改** X」= **一次性单点改动**，不要连带改别的。
  r52 教训：我把容器 32→28 时"顺手"把 svg 也 16→14，属**过度修改**（依据是设计稿加号墨迹 10.7 ÷ (16/24) = **16px 盒**，
  且「即可」二字本身就在收窄范围）。
- **收尾自查口诀：改完把「我多做了什么」单独列一行。** 拿不准时只做字面要求那一项；
  想连带改的，先在汇报里列出「建议但未改」。

---

## P3 取证与验收

### P3.1 agent-browser eval 的静默失败
- 裸 `eval` 内写 `return` **非法** → 必须包成 `(()=>{ … return … })()`；不套时不报错、**静默返回空**。
  箭头函数简写 `f=s=>…` 会被误判为**组件** → 统一写 `const q=s=>…`。
- ⚠️ **`wait <ms>` 会丢页面状态**：点击后 `wait`，随后的 `eval` 读到的类名又回到初始。
  要"等一帧 / 等过渡"→ **拆成两次 `eval`**（各自新进程，天然隔 ~200ms），或手动补上
  `.giencoder-popup-open` / `.giencoder-panel-open` 再截图。
- ⚠️ **弹层开态取证必须确认 `opacity === 1`**：DS 在 `requestAnimationFrame` 里才加开态类，
  同一个 `eval` 里量必然还是 `opacity:0`（`getBoundingClientRect` 却完全正常）→ 截图会是空的。
  **弹层几何必须在动画结束后量**：`.td-more` 入场有 `scale: .96 → 1`，刚点开就量会得到
  130×0.96 ≈ **125×73**，误判成"尺寸被改小了"。
- ⚠️ **`display:none` 元素上 `.click()` 静默失效**：连续 toggle + 派发 `Escape` 后抽屉状态机会错位，
  后续 rect 全 0、误判"功能没生效"。→ **断言失败先重载 `<url>` 拿干净状态**，别在脏状态上继续推理。
- ⚠️ **验收脚本别混入会导航的操作**：同一个 eval 里触发 `location.href` 跳转会打断 CDP
  （`Inspected target navigated or closed`），整轮白跑。**分步 eval，每步只读状态。**
- **A/B 对照页别放在 `pages/` 里跑校验**：`verify-design.py ./pages` 会把它一并计入（76 → 97）
  → **跑校验前必须先删掉**。
- ⚠️ **页尾同步脚本取不到还没渲染的 DOM**（r67 血泪）：本页是 React 产物，注入的 `<script>` 在 `</body>` 前
  **同步执行**时外壳的 `main` 还不存在 → `document.querySelector('main.dot-bg')` 返回 **null**、监听器永远绑不上。
  症状极具迷惑性：CSS 全绿、`transitionProperty` 也对、伪元素 mask 也在，**就是不动、变量恒为初始值**。
  ⇒ 正解＝**文档级事件委托**（`document.addEventListener('pointermove', e => e.target.closest('main.dot-bg'))`），
  不必等渲染、也不必 `MutationObserver`；再配 rAF 节流（每帧至多写一次变量）。
- ⚠️ **同一 URL 可能并存多个 page target**（`?fresh=N` 的同名页、`chrome://newtab/`）：CDP 里模糊匹配会截到
  **错的标签页**（probe 报 `open=true` 但截图里没弹窗）→ 用 `p.url.endsWith('<文件名>')`；
  自查：attach 后**同一 session** 里读 `location.href` + `elementFromPoint(x,y).className` 与 agent-browser 侧比对。
- ⚠️ **Node 模板字符串里 `\b` 是退格符**：注入 JS 写 `` `/td-bf\b/` `` → `/td-bf<BS>/`，永不匹配且**不报错**。
  要词边界写 `\\b`，更稳是 `^td-bf(\s|$)`。`\d` / `\s` / `\w` 同理。
- ⚠️ **探针脚本必须全字段 null-safe**（r69）：`.td-bf-arrow` / `.td-bf-ico` 是 `::before` 承载的空 span
  （`getBoundingClientRect` 得 `[0,0]`），且部分节点可能为 null → 直接 `e.querySelector('svg')` 会抛 `TypeError`
  让整支探针白跑。写 `const R=e=>{if(!e)return null;…}` / `const S=(e,p)=>e?getComputedStyle(e,p):null`，
  伪元素尺寸改读 `getComputedStyle(el,'::before').width`。
- ⚠️★★ **真实按键 ≠ 合成 KeyboardEvent**（r71 纠错，推翻了 r70 的一个误判）：
  `document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape'}))` 造出的事件 **`isTrusted === false`**，
  页内按 `isTrusted` / 事件来源分支的逻辑（尤其**外壳自己的导航链**）行为可能完全不同。
  r70 据此断言「base 权限弹层按 Esc 会跳走」；r71 改用 **`agent-browser press Escape`（真实按键）** 实测 →
  **base 页面停在 base.html、弹层保持打开**（不跳）；而 task-detail 浏览态真实 Esc **确实跳 kanban**
  （改前基线同样跳 ⇒ 既有行为，非本轮引入）。
  ⇒ **凡是要验证"按键会不会触发导航/全局快捷键"的结论，一律用 `press <Key>`，不要用合成事件**；
  合成事件只适合验证"元素自己的 keydown 监听"。
  　↳ r72 已据此修复 task-detail 浏览态的 Esc 层级（见 P3.4 末条）。
- ⚠️ **`press` 单次调用本身耗 0.5–1s**（r72）：测「定时器延迟型行为」（收起动画 240ms 后
  `setTimeout(done, 240)` 才摘 `is-browse`）时，`sleep 0.7` 看着够，实测采样仍读到 `is-closing` 未摘，
  差点误判成"定时器没跑 / 功能没生效"。
  ⇒ **等定时器 / 动画时 `sleep` 给到 2.0s**。每次 `press` / `eval` 都是**新进程冷启动**，
  真实经过时间 ≈ 命令自身耗时 + `sleep`，不能只按 `sleep` 算。
- ⚠️★ **本机 `grep` 查中文一律返回空**（r71 一轮内复现 3 次）：`grep -n "push"` 能匹配 ASCII，
  但 `grep "第 71 轮"` / `grep "未推"` / `grep "中文"` **全部返回空、不报错、只在中文上失效**。
  症状极具迷惑性：会误判成「文件里没有这条」而绕远路（r71 查日志轮次、查 HANDOFF 的 push 表述都中招）。
  ⇒ **查含中文的内容一律用 `python3 -c "for i,l in enumerate(open(f,encoding='utf-8').read().split(chr(10)),1): …"` 读**；
  `grep` 只用于纯 ASCII（类名、hash、标签名、token 名）。这与 P1 的「按需 grep 记忆文件」并不矛盾 ——
  **grep 定位 ASCII 锚点，中文内容用 python 读**。

### P3.2 伪类态 / 拖动 → 见 skill `css-pseudo-state-evidence`
- 伪类态**没有 DOM 属性可改**，唯一可靠链路：`rect` 拿视口坐标（列表/树里要筛 `width>0` 的**可见**元素，
  隐藏副本 rect 全 0）→ CDP `Input.dispatchMouseEvent {type:'mouseMoved', x, y, buttons:0}` **发两次**（间隔 ~150ms）
  → **同一 session** 里读 computed **并**截图逐像素采样交叉验证。
- ❌ **别用 `agent-browser hover <sel>`**：本机实测落点偏到顶栏（`:hover` 链最深处是 HEADER），"成功返回"却不生效 —— 静默假阳性。
  ⚠️ **但它并非永远不可用**（r71 补测）：对侧边栏里的 `.new-chat-btn` 用 `hover` **是生效的**
  —— `getComputedStyle(b,'::after').animationName === 'ncGlassSheen'`、`duration 0.76s`、
  扫光中 `opacity 0.467`、动画结束后 `document.getAnimations()` 里同相动画归 0。
  ⇒ 口径改为：**`hover` 之后必须用 computed style / `getAnimations()` 交叉验证，不能只看命令返回码**；
  验证不通过再退回 P3.2 的 CDP `Input.dispatchMouseEvent`（发两次、间隔 ~150ms）。
- ⚠️ `matches(':hover')` 会连同**祖先**一起命中：从深到浅 pick 时会先中 `td-bf-name` 这类子 span（背景 transparent）
  → 误判"没生效"。正则必须**锚定元素本体**。
- **合成 PointerEvent 测不了依赖 `setPointerCapture` 的拖动条**（如 `.td-gutter`）：合成事件下拖动不生效。
  ⚠️ **最省事口径**：`eval` 里直接派发 `new PointerEvent('pointerdown'/'pointermove'/'pointerup',
  {clientX, clientY, bubbles:true, pointerId:1})` —— 驱动页面自定义 pointer 拖动逻辑的唯一稳路；
  `pointerdown` 的 `clientX` 必须取目标真实坐标（`el.left + 4`），不能给 0；
  `pointermove/up` 监在 `window`（捕获段）、`pointerdown` 监在 gutter 上 → 事件要**分开派发**。
- ⚠️ **`visibility: hidden` 祖先里的组件无法聚焦** → `ta.focus()` 静默失败、`:focus-within` 永不匹配
  （数字分身抽屉即此）。**破局 = 探针克隆法**：`createElement('div')` 打上同一个类名 → 挂 body →
  塞 `<input>` → 真实 focus/blur 读 `getComputedStyle`。全局规则共用，足以证明规则有效；再拿另一页做 A/B。

### P3.3 动效取证
- **相位钉定用 WAAPI，不要用 `animation-delay`**：`animation-delay` 只定**相对**相位（绝对相位还叠了已运行时长，
  不可复现）；正解 `el.getAnimations()[0]` → `pause()` + `currentTime = T`。
  ⚠️ **`document.getAnimations()` 包含伪元素**（`a.effect.pseudoElement === '::after'`），所以 `::after` 上的动画也能钉相位；
  但**逐个方案钉相位要筛同名动画**（`filter(a => a.animationName === 'v-bar')`），否则会把全页同相动画一起钉住。
- reduced-motion 用 CDP `Emulation.setEmulatedMedia({features:[{name:'prefers-reduced-motion',value:'reduce'}]})`
  或 `agent-browser set media light reduced-motion` 实测。
- 断言：`transitionProperty` / `animationName + effect.getTiming().duration`，同时读 `transform` 矩阵验证**位移方向**；
  用 `document.documentElement.scrollWidth === innerWidth` 证明没有横向溢出（比截图快一个数量级）。
- **动效中间帧取证**：`el.getAnimations()[0]` → `a.pause(); a.currentTime = 36;` **精确定格**再截图；
  直接"点了就截"几乎抓不到（截图耗时 > 280ms 动效，两帧 md5 会完全相同）。
- ⚠️ **页面 2× 截图必须走 CDP**：`agent-browser screenshot` **只出 1×**，与 2× 设计稿直接比会整体错位。
  用 `Emulation.setDeviceMetricsOverride{width,height,deviceScaleFactor:2}`（脚本 `mg-work/r65/shot2x.mjs`）。
  截图前先 `$AB eval 'location.href'` 取真 URL 再传给脚本（多 target 问题见 P3.1）。
- ⚠️ **验证"过渡是渐进的"必须用「页内一次性采样」**（r67 血泪）：`派发事件 → sleep → eval` 会误判 ——
  实测 agent-browser 每次 eval 的 CDP 往返有 50~150ms，足以吃掉 260ms 的过渡，读到的永远是终值。
  正解：**同一个 eval 里**派发事件 + 用 `setTimeout` 采 8 个点写进 `window.__s`，再另起一次 eval 取回。
- **「某一层零变化」的最强证明 ＝ 把它推到画布外再逐像素比**（r67）：把光斑圆心设成 `-500%` 让它彻底移出
  ⇒ 与改前对比 **目标容器内最大差异 = 0**；若剩余差异与"同页连拍两张"的对照实验**行数 / y 区间完全一致**，
  即可判定是页面自身噪声。
- **diff 热力图**（r67）：以"目标特效被移除"的那张为基线，对多个状态截图求 `ImageChops.difference`
  并**增强 N×**（`point(lambda v: min(255, v*7))`），一眼看出作用范围与位置是否跟随。

- ⚠️★ **`open <新URL>` 之后立刻 `screenshot` 可能拍到「上一张页面」**（r73 实锤，极隐蔽）：
  连发 `$AB open file:///tmp/r73d-backup/task-detail.html >/dev/null 2>&1 && $AB screenshot …` 时，
  得到的图与**上一张**（`pages/task-detail.html`）**逐字节相同**（`ImageChops.difference(...).getbbox() is None`）→
  差点据此得出"改前改后无差异"的结论。
  ⇒ 对策：① **别把 `open` 的输出重定向丢掉**，要确认它打印的 URL；
  ② 截图前**先 `$AB eval 'location.pathname'` 回读真 URL**（同 P3.1 的多 target 问题）；
  ③ **两张证据图必须做 `getbbox()` 差异校核**，`None` 就意味着有一张是废的（除非你本来就要证明"零差异"）。

### P3.4 验收口径
- `python3 verify-design.py ./pages`（**必须传目录**）；⚠️ 它会**重写 `pages/gaps.log`** →
  跑完 `git checkout -- pages/gaps.log`。
- 对比是否引入新问题：`git show HEAD:pages/X.html` 导出到临时目录，同口径跑两遍比汇总数。
  ⚠️ **「汇总数相同」不等于「零影响」**（可能一边修好一条、一边新引入一条）。**逐条 diff 才作数**：
  `... | grep '^│' | sed 's/:[0-9]*//' | sort | uniq -c | sort -rn > /tmp/base.txt`，两遍后 `diff` 为空才算真正零新增。
  ⚠️ **最精确的基线 = 用「本轮改前备份」替换单页**（r69）：`cp -r pages /tmp/rNN-base/pages && cp /tmp/rNN-backup/X.html /tmp/rNN-base/pages/X.html`
  → 只隔离本轮改动，避免被同工作区其它未提交轮次干扰。
  ⚠️ BSD `sed` 不支持 `\+` → 抹行号用 `sed 's/:[0-9]*//'`。
- ⚠️★ **多补丁轮次要「拼」基线**（r71）：一轮里如果分了好几个 `applyNNx.py`（原补丁 + 若干修正），
  基线目录要**按页取该页"最早那次改动之前"的备份** —— r71 的基线 =
  3 个改前页取 `/tmp/r71-backup/`（本轮起始）+ 6 个「只被 r71b 碰过」的页取 `/tmp/r71b-backup/`。
  混错了会把已修的项算成新增。
- ⚠️★ **verify-design 只有两条正则，可变数值用「自定义属性」承载才是正解**（r71）：
  · 字号：`font-?size[`:]*\s*(\d+)px`（**只看 `font-size` 属性本身**，且整行含 `var(--font` 才跳过）；
  · 动画：`(?:animation|transition)[^;}`]*?(\d+)ms`，>300ms 报警。
  本轮新增 3 条（`.av-main-avatar-face` 的 28/22px、扫光的 760ms）就是被这两条抓到的。
  ⇒ 正解**不是**把值藏起来，而是**把可变数值提到自定义属性上**（与同块已有的 `--nc-glass-ease` 同一写法）
  并在注释里写明依据：`--av-face-size: 40px / 28px / 22px`（DS 字号 token 无这三档）、
  `--nc-glass-dur: 760ms`（craft.md 的 ≤300ms 针对**状态反馈**动效，本键是装饰性环境动效，
  按 craft.md 自带的例外口径显式声明）。**顺带能把基线里同族的老告警也收掉**（r71 净 −1）。
- **「零影响」最佳证据 = 改前/改后同状态截图 md5 相同**（前提同视口 + 同 DPR + 状态已复位、无动画残留）。
- **「内层溢出节点」扫描要剔除省略号元素**：口径 `scrollWidth > clientWidth + 1 && overflowX !== 'visible'`；
  `text-overflow: ellipsis` + `nowrap` + `overflow:hidden` 的元素 scrollWidth **必然**大于 clientWidth
  （如 `.td-file-tx`），不剔除会误报"界面被挤坏"。
- 窄宽压测要压到**自动收窄的触底值**（r60：视口 1620 → 左栏恰好 480 = `LEFT_KEEP_MIN`），不能只测一个宽视口。
- ⚠️★ **`gaps.log` 的"改前基线"不能取仓库版**（r72）：仓库里那份是**上一次 commit 时**的快照，
  而每轮收尾都会 `git checkout -- pages/gaps.log` 还原 → 它停留在**更早的轮次**
  （r72 时它还是 r71 **之前**的），直接 `diff` 会把中间几轮的改动全算到本轮头上
  （r72 第一次 diff 就得出"新增 9 类"的假象，实际那些是 r71 的）。
  ⇒ **正解：把目标页临时换回本轮改前备份 → 跑一次 verify → 存下 `gaps.log`；
  再换回改后版本跑一次 → 两次**归一化**后 diff**（抹行号：`re.sub(r':\d+(-\d+)?', ':#', l)`，再 `Counter` 差集）。
- ★★ **一键重建「本轮改前基线」的最省事办法：反向剥离本轮注入块**（r73 定稿，比拼备份更稳）：
  本轮 4 个补丁都是**整块注入**（`<style id="r73-…-css">` ×2 + `<script id="r73-tab-relay">`），
  少数是块替换（`base.html`）→ 于是：
  ```
  /tmp/rNN-pre/pages/ = 当前 pages，逐页 find(<块头>)→find(块尾) 后切片删除；
                       块替换的那页直接 cp mg-work/rNN/before/<page>.html
  ```
  再 `verify-design.py /tmp/rNN-pre/pages` → 与改后那次跑**归一化 diff**（抹行号后 `Counter` 差集）。
  r73 结论：**新增 0 类 / 消失 0 类**，汇总同为 75 项 / 0 critical。
  ⚠️ 前提是「本轮改动全部带唯一 id 的整块」；若是**零散就地修改**（改既有规则里的数值），剥离法失效，
  要退回「多页拼备份」或 `git stash`。
  ⚠️ 剥离后要**断言块头残留为 0**，否则等于没剥干净。
- ⚠️ **「仓库版 `gaps.log`」这个坑 r74 又踩了一次** ⇒ 每次收尾必须走上面那条正解，别图省事直接
  `git show HEAD:pages/gaps.log` 当基线。r74 复核发现：`HEAD:pages/gaps.log` 只有 45 条，
  **连 avatar.html / task-detail.html 的条目都没有**（这两个文件在 HEAD 就存在）——
  即**提交进仓库的那份从来没跟页面同步过**。误用它 ⇒ 归一化后"新增 21 条"的假结论。
  实测真基线（由 `mg-work/r74/before/` 重建）：两边各 65 条、**新增 0 / 消失 0 / 计数零变化**。
  **根治建议**：把 `pages/gaps.log` 重新提交一份同步版，或加进 `.gitignore`。
- ⚠️ **`CRAFT-SLOP`「检测到 N 处渐变」会对**新增的遮罩/点阵**误报**（r74）：
  判据是纯正则 `len(re.findall(r'linear-gradient|radial-gradient|conic-gradient', content))>= 3`，
  **不区分用途** ⇒ 你写的 `mask-image: radial-gradient(...)`（环形遮罩）、
  `-webkit-mask-image: radial-gradient(...)`、`background-image: radial-gradient(...)`（画点阵）
  都会被计入"装饰性渐变"。r74 使 `base.html` 由 52 → 55。
  ⇒ 处理口径：先按用途判定（**几何基元 ≠ 装饰**），再看**该文件改前是否已越阈值** ——
  已越阈值 ⇒ 只是数字变化、门禁结论不变，**写进验收报告说明即可，不要为凑数去砍 `-webkit-` 前缀**（既降不到阈值下、又牺牲兼容性）。
  另外注意：`mask` / `mask-image` 是**浏览器一致性问题**，标准属性 + `-webkit-` 前缀**两个都得留**。
- ⚠️ **`verify-design.py` 只要存在 warning 就 `exit 1`**（r74）：`75 项 / 0 critical` 也照样退出码 1，
  别用 `cmd && next` 串接，会把后续步骤静默跳过（本轮踩过一次：脚本没跑、输出空、还以为是环境问题）。
  正确写法：`cmd; echo "exit=$?"` 或 `cmd >log 2>&1; rc=$?`。
- 💡 **门禁「逐条一致」必须用「剥行号 + 剥目录前缀」后再 diff**（r74）：行号必然因注入块而漂移，
  目录前缀（`./pages/` vs `./mg-work/r74/before/`）也必然不同。剥完只剩**真正的语义差异**（r74 只剩 1 行）。
  比"汇总数相同"强得多 —— 汇总数相同完全可能是「修好一条 + 新引入一条」。

### P3.5 位置 / 存在性断言：只看渲染值，不看内联值
- ⚠️★★ **绝不能用 `el.style.left` 判断"元素在哪"**（r73 血泪：据此报了一个**不存在的错位 bug**，白问用户一次）：
  内联样式会被样式表里的 **`!important`** 压掉 —— `task-detail.html` 的滑块
  `style.left = "2px"`（React 写的）但 `getComputedStyle().left = "62px"`、
  `getBoundingClientRect().x` 也确实在 dev 位（上一轮用 `left:62px !important` 钉过）。
  ⇒ **口径三件套**：`getBoundingClientRect()`（与祖先做差得相对位置）→ `getComputedStyle()`（拿最终值）→
  截图逐像素（交叉验证）。**`element.style.*` 只能证明"React 想写什么"，不能证明"渲染成什么"。**
  同一坑的另一种表现：`agent-browser eval` 里读 `inlineLeft=2px` 的 9 页对照表**看起来**"有 1 页不一致"，
  实际 9 页渲染位置**全都一致** —— 险些把"改前=改后"误判成"改动了 1 页"。
- **判断"我注入的脚本真的跑过"的确定性标记**：让脚本写一个**宿主从不写的属性**
  （r73 用 `span.style.translate`，React 的 style 对象里没有 `translate`）→
  落在 `"0px 0px"` 就说明接力路径命中；裸开页面时该值为**空串**，标记因此有意义。
  比"看视觉结果"更硬，且一条 `eval` 就能读。
- ⚠️ **PIL 合成证据图**：
  · **画布高度必须按公式算**：`Image.new('RGB',(W,H))` 的 `H` 少算时 `paste` **越界静默裁剪**（报错为零、
    出图看不出，但最后一行被切掉）→ 用「表头 + 行数 ×(标题+副标题+图高+说明+行距)」显式求和；
    跑完**回读 `Image.open(...).size` 与公式对一遍**。
  · ⚠️ **字体**：`/System/Library/Fonts/PingFang.ttc` **本机不存在** → `ImageFont.truetype` 抛错被吞 →
    回退 `load_default()` → 图注**全成乱码**。可用 `Hiragino Sans GB.ttc`（idx0=W3 / idx2=W6 粗）、
    `STHeiti Medium.ttc`（idx1=Heiti SC）。**写图前先用 `font.getname()` 断言字体真的加载成功。**
  · 定位"彩色高光带"**不能用亮度阈值**（白底本身最亮）→ 找**偏色通道差**（蓝光 `p[2] - p[0] > 50`）。
  · **文字色采样要打在笔画上**，不能打在留白上；先用 `getComputedStyle` 定案，像素采样只作交叉验证。
  · 证据图上**别在画板内叠加文字**（会压住泳道标题等内容）→ 在画布右侧留 250px gutter，
    只把红/蓝细竖条画在画板边缘，说明文字放 gutter 里。
- ★ **Esc 层级裁决**（r72 定稿 · `task-detail.html` 浏览态）：症状是「按 Esc 直接跳 `kanban.html`，
  预览栏关不掉」。根因不是"条件不满足"，而是两条监听**同在 document 冒泡段 ⇒ 执行顺序＝注册顺序**：
  页尾 Esc 链写在同步 `<script>` 里、**初始化即注册**（最早），链尾直接 `location.href` 触发导航；
  浏览侧栏的 `setOpen(false)` 是**懒注册**（首次开侧栏才挂）→ **永远轮不到执行**。
  ⇒ 修法**不必**新引入捕获段监听（同页虽有 `@685832`/`@691856` 先例，但那要求自己重排
  "谁是最高层浮层"：编辑弹窗／更多菜单／协作模态／转派浮窗／右键菜单／对话框弹层各占一条，漏一项就"一次 Esc 关两层"）。
  **正确解法＝复用页尾链既有的 `td:close-*` 派发模式**：新增 `td:close-browse` 一层，
  插在「**全屏分支之后、跳转分支之前**」—— 位置即优先级（链上浮层全关完才轮预览栏，再按一次才回看板），
  且全屏态既有语义一字未动；链上各分支同样只 `return`、不 `stopPropagation`（风格一致）。
  验收：非浏览态 Esc、全屏态 Esc 均未破坏（见 `mg-work/r72/ev/acceptance.md`）。
  ⚠️ 遗留（既有、非本轮引入）：**全屏 + 浏览态时 Esc#1 一次关两层**，等用户拍板。

---

### P3.6 动效取证的两个新坑（r74 定稿）

**坑 1：`:hover` 在多次独立 `agent-browser` 调用之间会丢失。**
`agent-browser hover X` 之后，**下一次**独立调用（`eval` / `screenshot`）里该元素的 `:hover` 常常已经不成立
（新 CDP session 会重置指针态）→ 于是：

- `document.querySelector(x).getAnimations()` 返回 **`[]`**（动画已随失焦被移除）
- 截图里**看不到任何位移/旋转**（看起来像"动效没生效"，其实只是 hover 没了）

⇒ 铁律：**伪类态证据必须在「单次调用内」闭环**（hover 与读取写进同一条命令做不到时，改用下面的替代法）。
替代法 = **常驻选择器探针**：临时注入一份**同一条 `@keyframes` + 同一条曲线**、但选择器不含 `:hover`
（如 `.r74-face-glyph{animation:…!important}`）的样式，然后 pause + seek 取帧。
探针只用来证明「关键帧的形状/幅度」，**触发链另用一次"hover 后立刻读 `animationName` + `duration`"证明**，两者合并 = 端到端。

**坑 2：CSS `transition` 无法 `pause()` + `currentTime = N` 冻结（`CSSAnimation` 可以）。**
对 `CSSTransition` 设 `currentTime` 实测**不生效**（读数停在被暂停时的中间值，冻结帧白做）。
⇒ 采 transition 的过程帧用**慢放法**：注入临时样式把时长放大 20×（`transition-duration: 4000ms !important`），
再按墙钟时间取帧；几何比例与曲线完全等价，且**不破坏过渡语义**。
（同一招也适用于太短的 `CSSAnimation`：300ms 的动画在"hover → 读取 → 截图"三次调用之间早就播完了。）

**附带一条读值经验**：`getComputedStyle(el).rotate` / `.transform` 在 Chrome 里对**动画中的独立属性**
可能恒报 `none`（即使画面明显在转）——**别用它判断"动效有没有生效"**；
改用 `el.getAnimations()[0].effect.getKeyframes()` 看**已解析的关键帧**（能直接看到 `0.18:-9deg` 这类值）
＋ 冻结帧截图做视觉交叉验证。

---

### P3.7 「快照克隆（ghost）」退场机制的两个系统性坑 + 一条提效（r75 定稿）

背景：r74 给 React 条件卸载型浮窗做了「点击捕获段拍快照 → `MutationObserver` 发现节点消失 →
克隆一份 `position:fixed` 的外壳播 WAAPI 退场」。r75 修它的两个缺陷，顺带查清机制边界。

**坑 1：★★ ghost 外壳会被「按内联样式特征写」的选择器误命中 —— 因为属性选择器匹配的是「序列化后」的 `style` 值。**

r74 给顶栏门户写的那条进场规则是**按内联样式特征**选元素：

```css
body > div[style*="position: fixed"][style*="z-index: 1000"] { animation: r74-pop-in … }
```

而 ghost 外壳**恰好也是**「挂在 `body` 下 + 内联固定定位」的容器（`g.style.cssText = 'position:fixed;…z-index:1000;…'`）
⇒ 被一并命中。**关键机制**：JS 里写的是 `z-index:1000`（**无空格**），
但浏览器会把 `style` 属性**序列化后回写**（`position: fixed; …; z-index: 1000`，**带空格**），
而 `[style*=…]` 匹配的正是这个序列化值 ⇒ 命中。
后果：外壳同时挂「进场淡入（CSS animation）」与「退场淡出（脚本 WAAPI）」两把动画、**都作用于 `opacity`**。

- **决定性实验（空壳对照，最干净）**：手工建两个空壳 `div[data-r74-ghost]`，一个 `z-index:1000`、一个别的值
  → 前者 `getAnimations().length === 1` 且 `animationName === 'r74-pop-in'`，后者 0。
  ⇒ 与「被克隆的内容」无关，纯粹是外壳自身命中选择器。
- **修法**：把外壳也纳入静止 —— `[data-r74-ghost] { animation: none !important; }`
  （原有的 `[data-r74-ghost] *` 只匹配**后代**，**不含自己**）。
- ⚠️ 判断「两条动画争同一属性」的现状：`el.getAnimations()` 会同时列出 CSSAnimation 与 WAAPI Animation，
  用 `a.effect.target === el` + `a.animationName` 逐条比对。**currentComputedValue 只能看最终值**
  （本例实测是纯退场曲线 ⇒ 脚本动画胜出），**不能只看"看起来对"就收工**。

**坑 2：★★「两件事同时发生」不等于因果 —— 先取证再归因。**

首版把「退场 ghost 不可见」归因成「克隆体的淡入 × 外壳的淡出相乘恒为 0」，
并把这个结论写进了补丁注释。实测证伪：外壳 `opacity` 一直是**纯退场曲线**
（`1 → 0.757 → 0.441 → 0.206 → …`，与"没有该动画"的场景**逐帧吻合**），根本不是乘积。
**真主因是两个独立缺陷叠加**：① 克隆体自带内联定位，塞进 fixed 外壳后**重新解析**、
被顶出外壳再被 `overflow:hidden` 裁掉；② 克隆体带着同一份内联样式，**又命中本页进场选择器**。
⇒ 教训：注释也要按证据写，**错误注释是负资产**（下一轮会照着错的前提推理）。

**一条提效（本轮最大）：`agent-browser eval` 支持 `await Promise`。**
把探针写成 `async` IIFE，就能在**一次调用内闭环**：点击 → `await wait(ms)` → 逐帧 `requestAnimationFrame` 采样
→ 直接 `return` 结果字符串。**彻底绕开「跨调用丢状态 / 需 `window.__X` 中转 / 需 `sleep` 拼时间」的绕路**
（对比：早期探针要 `eval 启动` + `sleep` + `eval 读 window.__V1` 三步，还怕被新 session 清掉）。
配套两个小坑：**`DOMRect` 不可迭代**（`[...el.getBoundingClientRect()]` 抛 `TypeError`，要逐字段取）；
**采样点别贴着状态切换的那一帧**（外壳刚 `appendChild` 的首帧可能读到 `opacity:0`，属采样边缘而非缺陷——
用 `MutationObserver` 等外壳出现、或先 `await wait(30~40)` 再开始逐帧，就干净了）。

**机制边界（一并记住，避免下一轮误判）**
- **「关闭时不移除节点」的浮层不走 ghost 通路**：原生 `.giencoder-select-popup` 关闭时 React 只给**祖先**加内联
  `display`，节点仍在 ⇒ `MutationObserver` 的 `removedNodes` 与 `attributes['style']`（`fire(m.target)` 里
  `SNAP.get()` 按**被拍快照的那个节点**查）都命中不了 ⇒ **无 ghost**，退场天然由设计系统的 `transition` 承担。
  ghost 只服务**React 卸载型**（如「默认权限」自研浮层）。
- **`live()` 的 `rect > 12px` 门槛会静默排除「高/宽为 0 的容器」**：顶栏门户 `height` 恒为 0
  ⇒ 从不被拍快照 ⇒ SEL 里那条 `body > div[style*="position: fixed"]` 实际是**防御性**的。
- **`display: block !important` 压过内联 `display:none` 是安全的**：元素本身绝对定位、不占文档流；
  关闭态仍由 DS 的 `visibility:hidden` + `opacity:0` 隐藏（不可见元素既不接收指针事件、也不进无障碍树），
  唯一差别是元素从此**常驻渲染** —— 而"常驻渲染"正是「过渡能有起点」的前提。

---

### P3.8 r76 定稿：四条新坑（渐变 mask / 门禁正则 / 视口污染 / 补丁链幂等）

**1. ★ CSS 渐变的「负 stop 位置」不报错，但会静默毁掉环形 mask**

用 `calc(r − Npx)` 做 `radial-gradient` 的 mask 内缘时，`r < N` 会让该 stop 落到负位置。
不报错、也不报 warning，结果是：**所有负位置 stop 折叠到 0，且同一位置最后一个 stop 胜出**
⇒ 圆心到 `r` 之间被填成不透明 ⇒ **环退化成实心圆盘**。
症状极具迷惑性：动画在跑、半径在变，只是"看起来像一大块暗点"而非一圈波纹
（r76 取帧 `t=100ms` 才暴露）。

✅ 正解 = 让内缘永不塌到圆心：

```css
transparent max(calc(var(--r) * 0.40), calc(var(--r) - 156px)),
rgba(0,0,0,.45) max(calc(var(--r) * 0.62), calc(var(--r) - 96px)),
...
#000 var(--r),
transparent calc(var(--r) + 20px)
```

小 r 走**比例**（内缘 `0.40r`，圆心恒留洞）、大 r 走**固定值**（内缘 `r − 156px`，带宽钉住不越扩越糊）。
前提：两分支的系数与偏移**各自单调递增** ⇒ 合成后的 stop 位置必单调不降，CSS 才合法。

**取证口径**：把「与基线的差分」**放大 N 倍**再拼成逐帧网格（r76：`×5`，7 帧 4×2），
环的**空心形态**与**单调扩张**一眼可见 —— 比看原图或看"差异像素计数"都直观。
（差异像素计数只能说明"变了多少"，说不清"变形成一个环还是一块斑"。）

**2. ★ 门禁 `CRAFT-ANIM` 的时长正则连 `animation-delay` 一起抓**

```python
dur_pattern = re.compile(r'(?:animation|transition)[^;}`]*?(\d+)ms', re.IGNORECASE)
```

它只要求「`animation` 或 `transition` 字样」与「数字 + ms」出现在**同一行**（中间无 `;`/`}`/反引号）。
⇒ `animation-delay: 325ms;` **同样触发 🟡**。
做**错峰（stagger）**动画时，**最后一段的 delay 也不能超过 300ms**
（r76 首版 10 段走到 325ms，成了整轮唯一一条门禁新增项）。
判据：错峰总跨度 ≤300ms；必要时压缩步长（r76：40/80/…/325 → 统一步进 32ms，末段 288ms）。

**3. ★ `agent-browser` 改视口做多档压测时，档与档之间必须重新 `open`**

`set viewport` 只改尺寸、**不清交互残留**。r76 实测：测完 900 档后用 Esc 关浮窗，
下一档 `set viewport 1440 720` 再量，读到的却是「关闭态的残壳」（`display:flex; h=0`），
差点被写成"720 档浮窗没渲染出来"的假缺陷。

⇒ 规矩：**每档 = `open` → `set viewport` → `sleep` → 测量**；
并且**同一档内的多步交互压进单次 `eval`**（`await` 可用，见 P3.7）。
另有两条老规矩并存：`set viewport` 必须排在 `open` **之后**；`zsh` 的 `set -- $V` **不做词分割**
（与 bash 不同）⇒ 循环里用 `${V%%x*}` / `${V##*x}` 显式切分。

**4. ★ 多版本补丁链的「已应用」判据必须用稳定标记，自检只在真正应用时跑**

一条链把同一个片段改了两遍时（r76：`apply76b` 改 mask → `apply76c` 再改同一段），
`apply76b` 若用**整串 `NEW_RIP in s`** 判"已应用"，会在 r76c 落地后**误判成未应用**，
再去找 `OLD_RIP`（也不存在）⇒ `sys.exit('锚点缺失')`。复跑幂等当场崩。

✅ 两条修法：
- 判据换 **r76b 引入、r76c 保留的稳定标记**（如 `rgba(var(--gray-9), 0.62) 1.8px`）；
- **自检块包在 `if changed:` 里** —— 否则用「本版专属 token」（如 `- 168px`）做断言，
  在"已应用但被后版覆盖"的终态里计数为 0，又会误报一次。

**5. 副作用观感要一并收口：`max-height` 夹出来的可滚列表会在半行处被切断**

夹 `max-height` 让浮窗塞进剩余空间，是**纯声明式**的好修法（`max-height` 天然压过内联 `height`，
被压掉的高度由内部滚动列表承载）。但它带来一个**新观感**：列表在半行处被切断，
而浮窗底多为 `rgba(255,255,255,.88)` + `backdrop-filter` ⇒ **那半行文字透出来像"串"到下方按钮条上**。

✅ 收口 = 给可滚列表加**底部渐隐 mask**，且**只在夹取生效的区间启用**：

```css
@media (max-height: 879px) {           /* 门槛 = 夹取开始生效的视口高 */
  [role="listbox"][aria-label="技能选择"] .skill-pop-list {
    -webkit-mask-image: linear-gradient(to bottom, #000 calc(100% - 52px), transparent 100%);
            mask-image: linear-gradient(to bottom, #000 calc(100% - 52px), transparent 100%);
  }
}
```

- 渐隐长度要**实测到位**：30px 时被切那行仍留 ~66% 不透明度、还看得出"串"；52px 降到 ~35% 才收干净，
  且末行**完整**技能的文字区仍保 ≥0.94（不误伤）。
- **作用域**：`.skill-pop-list` 的 CSS **9 页都有拷贝**，但 `[aria-label="技能选择"]` 节点**只在 base.html**
  ⇒ 选择器必须带 aria 祖先，否则会去动另外 8 页里根本不渲染的死代码。
- **零影响现证**：自然档读 `getComputedStyle(el).maskImage === "none"`（媒体查询不命中 ⇒ 规则不参与级联）。

---

## P3.9 注入位置 / 运行时脚本 / 密度耦合（r77 五坑）

### ① 新 `<style>` 块注入到哪，决定它压不压得住旧块

页面是**压缩单行 bundle + 若干注入块**。同一选择器、同特异性时**后者胜**，而"后者"由**块在文档里的位置**决定。

- 既有块（r74 的 `.r74-ripple`、r76 的两块）全部注入在 **`</body>` 前**。
- r77 第一版把新块注入到 **`</head>` 前** ⇒ 它在**文档序更早**的位置 ⇒ 同特异性的 `.r74-ripple` 规则
  **被页尾的 r76 块反向压回去**（实测 `zIndex` 仍是 10、点色仍是 `0.62/1.8px`，而 `.dot-bg` 那种
  "没人竞争"的属性却正常生效 —— 这种"一半生效一半不生效"极易误判成"选择器写错了"）。
- ✅ **纪律**：**注入位置与既有块对齐（一律 `</body>` 前）**；或显式提高特异性。
  排查时先 `s.find('<style id="rNN-...">')` 打印各块偏移，看**谁在谁后面**。

### ② 改 React 源码前，先查有没有**运行时脚本在改写同一段 DOM**

base.html 的 r74 页尾脚本①段抓的是「版权区**最后一个 `<p>`**」：把它覆盖成「© 2026 中电金信」
再 `appendChild` 一行「中电金信研究院 · …」。r77 需求要"把 AI 提示句挪到最下"，
只改 React 源码 `p` 顺序 ⇒ 脚本照旧抓"最后一个 p"（现在正是 AI 句）⇒ **整句被吃掉**，
渲染成三行重复版权。

✅ **纪律**：动某段可见文本前，先 `grep` **文本本身** + `data-rNN-*` 这类**运行时标记**，
确认没有被页尾脚本 `querySelector` 抓过；有则**同轮把脚本一起改**（改抓哪个节点 + 插在哪）。
标记属性（`data-r74-cr="1"`）就是当年留的幂等钩子，改逻辑时要一并沿用。

### ③ 背景点阵密度与"点阵型特效"的强度是**耦合**的

涟漪层（`.r74-ripple`）与底色波点必须**同一 `background-size`** 才能逐点对齐。
于是 `20px → 16px` 的加密会把**涟漪的点数一起 ×1.56** —— 削弱特效时若只降不透明度，
会被密度悄悄补偿掉（实测：α `0.62→0.28`（-55%）只换来净 **-54%**…再加上点径 1.8→1.7、mask 等因素，
最终环带亮度落在 **46%**）。

✅ **算法**：`净强度比 ≈ (α₂/α₁) × (g₁/g₂)² × (d₂/d₁)²`（g = 网格间距，d = 点径，面积按平方）。
先算出目标 α 再落地，别拍脑袋；落地后**用"环带亮度 Δ"复核**（见 ④）。

### ④ 量"特效强度"必须**页内基线**，不同页的基线不能混用

A/B 对比特效强度时，若拿 **A 页的无特效帧** 去减 **B 页的有特效帧**，差异里会混进**两页本身的差别**
（r77 就差过：20px vs 16px 网格 ⇒ 全画幅差异爆到 0.52，全是网格错位的贡献，数据全废）。

✅ **纪律**：**A 用 A 的基线、B 用 B 的基线**；再按同一区域口径比。
口径优先选**不受"可见面积"污染**的那个：
- 想表达"亮不亮" → **环带自身亮度 Δ**（取特效命中像素集合的平均灰阶差）；
- 想表达"铺多大" → 命中像素数 / 半径；
- **全画幅平均差**会被"可见面积变化"和"密度变化"双重影响，**只能当辅助**（r77 就出现"环带亮度 46%
  但全画幅 73%"的反直觉组合）。

### ⑤ `translate` / `scale` 是**独立变换属性**，`transform` 读不到

`@keyframes { from { translate: 0 4px; scale: .97 } }` 这类写在**独立属性**上的变换，
`getComputedStyle(el).transform` 返回 **`none`**（不是矩阵）。要读 `getComputedStyle(el).translate / .scale`。
`animation: X 160ms both` 播完后如需复现过程帧，`el.getAnimations()[0].pause()` + `.currentTime = T` 即可。

---

## P3.10 验证「点这儿该不该触发」（r78 三坑）

### ① 测"点击触发与否"必须 dispatch 到**真实命中元素**，不能 dispatch 到容器

给 `main.dot-bg` 这类**容器**挂 capture 监听时，判定链全部依赖 `e.target`：

```js
document.addEventListener('pointerdown', e => {
  const t = e.target;
  if (!t.closest('main.dot-bg')) return;                       // ① 必须在 main 内
  if (t.closest('button, a, input, …')) return;                // ② 不在控件上
  if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;  // ③ r78 新增的排除
  … 起涟漪
}, true);
```

❌ 若探针写 `host.dispatchEvent(new PointerEvent('pointerdown', …))`（host = `main.dot-bg`），
   **`e.target` 就是 main 本身** ⇒ `closest(…)` ③ 全返回 null ⇒ **整条排除链被绕过，测出来全是"会触发"**（假阳性）。

✅ 正解 —— 用 `elementFromPoint` 复刻真实 hit-test：

```js
const hit = document.elementFromPoint(cx, cy) || host;
hit.dispatchEvent(new PointerEvent('pointerdown', { clientX: cx, clientY: cy,
  bubbles: true, cancelable: true, pointerId: 1 }));
```

- 这样做还**自动覆盖 `pointer-events: none`**：`elementFromPoint` 会跳过着色层，
  返回真正接收事件的那个元素（r78 实测：LOGO 外层是 `pointer-events-none`，
  点到 LOGO 上返回的 target 是外层容器 —— 与真实点击一致）。
- 枚举多个点时，每个点之间要**清掉旧涟漪节点**（`host.querySelectorAll('.ripple').forEach(e=>e.remove())`），
  否则上一点残留会被算进下一点的计数。

### ② "点击前后整帧不变"不能只比 md5 —— 先做**噪声对照实验**

页面可能有**自有时间噪声**（r78：aside 内 `x236~249, y275~447` 一条窄竖带，帧间差 ~170 像素 / 峰值 165）。
直接比"操作前 vs 操作后"的 md5 必然不等 ⇒ 会误判成"改动有副作用"。

✅ **纪律**：同一次会话里**先连拍两张、不做任何操作**，算出噪声基线（差异像素数 + bbox）；
   再把操作后的差异与之对比 —— 量级相同、bbox 相同即可判为噪声。
   ⚠️ 噪声 bbox 若是**在目标容器之外**，基本可以立刻判定无关（r78 那条落在 aside，而 main 是改动面）。

### ③ 改 `<script>` **正文**时，标签级断言的口径与"插 style 块"不同

插 `<style>` 块的惯用断言是 `<style` / `</style>` **各 +1**；
而改脚本逻辑只动正文 ⇒ 断言应该是 `<script` / `</script>` 计数**不变**（delta 0）。
别把两套口径套错 —— 套错的话自检会通过"看起来正确"的假象，实测才发现页面被写坏。

```python
n_script = s.count("<script"); n_end = s.count("</script>")
s2 = s.replace(OLD_GUARD, NEW_GUARD, 1)
if s2.count("<script") != n_script or s2.count("</script>") != n_end:
    sys.exit("!! <script> 标签计数变化")
if s2.count("closest('.flex.flex-1") != 1:      # 新增判定恰 1 份
    sys.exit("!! 新判定重复/缺失")
if s2.count(OLD_GUARD) != 1:                    # 原判定仍在
    sys.exit("!! 原判定被误伤")
```

---

## P4 外壳路由与页面导航

- 路由变量（每页 bundle 内各一份，压缩成 `xt`/`St`/`Tt`）：`xt` route→文件名、`St` 文件名→route、`Tt()` 当前 route。
  → file:// 下按**文件名**解析（`St[filename]`），http 下按 **hash** 解析。`task-detail` **不在** `xt` 里，
  但 bundle 独立，直开正常；http 无 hash 会落回 base 壳。
- ⚠️ **两种预览协议渲染结果不同**：`file://` 直开 vs 内置预览 `http://127.0.0.1:<port>/static-html/<id>/<file>`。
  后者 URL **不带 hash** → 命中 React 外壳的协议分支（`Ct() = protocol==='file:'`）→ 渲染出错误的壳。
  排查"文件没改却显示异常"：**同一文件两种协议各开一次对比 DOM**。内置预览路径（实测）：
  `/static-html/791830df2f0ba958/` = 仓库根，`/static-html/22441530f7eeb388/` = `pages/`。
- **两块注入补丁**（每页各一份，`<!-- ... 勿手改此块 -->` 注释下，**新增页面必须带**）：
  · `SHELL-TABS-FIX v4`：捕获段接管**顶栏页签**点击 + 高亮纠偏（`DEV_PAGES` = 研发工作台名单）。
  · `SHELL-NAV-FIX v5`：监听 `hashchange`，把 `#/route` 还原成真实文件名跳转 → 修 http 下「侧栏/卡片点了没反应」
    （外壳 `navigate()` 在 http 只改 hash 且无人监听）。路由表取全站并集含 `/task-detail`；用**相对路径**赋值。
- 根 `index.html`（仓库根，非 pages/）＝ 页面导航页：16 卡分 4 组（研发工作台/基础工作台/设计系统/文档）。
  **改页面后若新增或改名，需同步更新此导航页。**
- file:// 已验证跳转链路：顶栏页签 base↔dev ✓、`.kb-card` → `task-detail.html` ✓、根导航页卡片 ✓、
  左栏导航（数字分身/自动化/技能/设置）✓。

---

## P5 git 与推送

- 仓库**已就地于** `/Users/shaoyuming/Documents/GienCoderDesignEngineering`（不再另建克隆）；
  `origin` = `theming028/giencoder-design-engineering`。仓库根在坚果云内，锁文件坑多。
- 🚫 **默认禁止自动 commit / push**（2026-09-28 用户要求）：任务完成后只汇报改动清单，推送由邵先生统一发起。
  **例外：用户显式要求推送时（如 r66）立即执行**，不再请示。
- 判定推送成功：`git ls-remote origin main` 与 `git rev-parse HEAD` 一致（`update_ref failed` 只是本地 ref 被锁，不代表失败）。
  ⚠️ 沙箱网络会拦 git 协议端点（`CONNECT tunnel failed, 502`）→ **重试 2~3 次**即可；
  `api.github.com` 返回 200 **不代表** git 端点可达（两者走的路径不同）。
- ⚠️ **本地可能积压很多轮未提交**（r66 时 HEAD 停在 r37，r38~r66 共 29 轮未提交）。
  用户说"全量推送" = 连 `mg-work/` 证据图 + 根 `index.html` 一起 `git add -A`；
  提交前先扫一遍敏感串（`ghp_` / `github_pat_` / `AKIA` / `PRIVATE KEY`）。仓库已跟踪 `mg-work`，属既有惯例。
- ⚠️ `git remote -v` 的 origin URL **内嵌 GitHub PAT（明文）** —— 汇报时不要打印完整 URL。

---

## P6 提速工作法（用户反馈"响应慢"后固化）

- ❌ **禁止整文件 Read `pages/*.html`**（单行压缩 bundle，340–620 KB，读一次即烧掉大量上下文）
  → 用 `python3 - <<'PY'` + `re.search(r'...', s)` 只**打印目标片段**（±200 字符上下文）。
- ✅ 独立探测**并行发**（同一条消息里多个 tool call），不要串行等待。
- ✅ 验证优先用 `agent-browser eval` 读 DOM 断言；**截图只在需要看视觉时用**（截图比 eval 慢一个量级）。
- ✅ 同一结论不二次复现；已知的环境事实（如 file:// 已验证通过）不重复测，只测本轮新增假设。
- ✅ 改大文件一律走 `mg-work/rNN/applyNN.py`（正则定位 + 幂等 + 结构计数自检），一次性跑通。
