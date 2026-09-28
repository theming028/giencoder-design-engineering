# GienCoderDesignEngineering · 项目长期记忆

> 详情索引见每日日志 `.workbuddy/memory/YYYY-MM-DD.md`；本文件只记**跨会话可复用的约定与工作流**。

## 一、环境（macOS 本机）

- 页面**全自包含**（CSS/JS 内联、图片 base64），无 `serve.py`（那是 YuanqiDesignSystem 仓库的）。
- `python3 -m http.server 8866` 会被沙箱网络代理拦成 502 → **直接用 file:// 预览**：
  `agent-browser open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/<page>.html"`
- agent-browser 路径：`/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser`
  （`mg-work/*/shot*.sh` 里写的是 Windows 路径 `C:/Users/Administrator/...`，本机需替换）
  命令：`open <url>` / `set viewport W H` / `screenshot <path>` / `eval '<js>'`
- ⚠️ **两种预览协议渲染结果可能不同**（2026-09-28 踩坑，曾误判"复现不出"）：
  `file://` 直开 vs WorkBuddy/Electron 内置预览 `http://127.0.0.1:<port>/static-html/<id>/<file>`。
  后者 URL **不带 hash**，会命中 React 外壳的**协议分支**（`Ct()=protocol==='file:'`）→ 渲染出错误的壳
  （实例：dev.html 多出 base 的 aside 侧栏、顶栏 tabs 白胶囊指示器错位到最左）。
  排查"文件没改却显示异常"：**同一文件用两种协议各开一次对比 DOM**，先分离"文件问题"与"渲染环境问题"。
- ⚠️ **写 Python 探测脚本时避开 `sc` / `reg` / `wsl` 等 token**（变量名 `SC=1.5`、函数名含 `reg` 都会命中
  安全策略的"系统级工具"拦截，命令直接失败）。改用 `S`、`scl`、`scan` 等命名。
- ⚠️★ **`file://` 下「改前基线」文件名必须与原页面同名**（r66 实锤，白跑一轮像素 diff）：
  外壳按**文件名**查路由表（`St[filename]`），名字不在表里 → **落回 base 壳**（多出 260px aside 侧栏）。
  实例：把 HEAD 版存成 `mg-work/r66/kb-before.html` → 泳道宽 269（真值 334）、`.kb-col` 左沿 289（真值 29），
  被我误判成"布局变了"。
  **正解**：放到子目录但保持同名 —— `mg-work/r66/before/kanban.html`（页面全自包含，位置随意）。

## 二、MasterGo 设计稿 → 图标还原工作流（已验证）

1. `get_selection_node(projectDir, targetNodeId="<图层ID>")` 拉节点 → 图标只会给 `<img src="./asset/icons/svg_xxx.svg">`，**拿不到 path**
2. 素材已自动落盘：`~/.mgmcp/artifacts/blobs/sha256/**`（文件名是 sha256，与 svg_xxx 无直接对应）
3. **破局点**：blob 内含 `clipPath id="master_svg0_{nodeId}"`
   → `grep -l "master_svg0_622_08923" *.svg` 可**精确反查节点 ↔ 文件**
4. 清洗后用：剥 `<defs>/<clipPath>`、去 `clip-path` 引用；
   配色**不写死 hex** —— 单色改 `fill="currentColor"`（CSS 变量承担），三色 `.md` 徽标走
   `class="td-ico-md-body|-fold|-mark is-solid"`
5. 验证：`agent-browser eval` 读 computedStyle + 放大 probe 截图对照设计稿 PNG
   （`get_screenshot` 可导出设计稿节点大图，落 `~/.mgmcp/resources/screenshots/`）
6. **设计稿规格量测法**（2026-09-28 r48 定稿，可复用）：导出 PNG 常为整数倍外的缩放（实例 1190×1266
   = 节点 793.3×844 的 **1.5×**），且**带 alpha 通道** —— 直接 `convert('RGB')` 会把透明区变成纯黑，
   误判成"黑色色块"。正解：`Image.alpha_composite(纯白底, src)` 之后再逐像素扫描，坐标一律 `/缩放比` 换回节点坐标。
   - 只用 `/Users/shaoyuming/.workbuddy/binaries/python/envs/default/bin/python`（3.13.12 无 PIL）。
   - **结构量测**：逐行/逐列打印"颜色变化点"→ 分隔线位置、面板边界、内间距、缩进步长一次读全，比看图目测可靠得多。
   - **线条等效色反推**：1px 线在 1.5× 下摊到 2 行 → `C = 255 − (两行墨量合计)/1.5`
     （顶栏底线墨量 30 → 235 ≈ #EBEBEB，正合项目既有"结构发丝线"档 → 统一取 `--td-hairline`）。
   - **文本墨迹定位**：在某 x 区间内取暗像素的 min/max x = 文字盒起点（含字距），可反推 padding。
   - ⚠️ **设计稿说"内间距 N px"时，务必同时核对容器总宽**：padding 与内容宽是一对约束
     （树容器 296 = 20 + 内容 256 + 20）；只给 256 宽的容器加 20 padding 会把内容压到 216，
     与设计稿搜索框 256 明显不符。遇到这种歧义 → 按设计稿还原并**显式标注宽度也改了**，同时给回退口径。

## 三、改页面的硬规则

- 页面 HTML 内联在 **JS 字符串数组**里，属性引号是 `\"` —— 脚本替换时正则要按 `\\"` 写。
- 替换内联 SVG **禁止**用 `<svg.*?</svg>` + `re.S`（会跨元素吞并整个区块）；
  用 `<svg(?:(?!</svg>).)*?</svg>`，并在替换后做**结构计数自检**（如 `.td-sec-head` / `.td-file` 计数不变）。
- 分组标题类替换必须**回填尾部捕获组**（否则分组名文本被吃掉）。
- 改动一律走 `mg-work/rNN/applyNN.py`（幂等 + 自检），不要手改大文件。
- ⚠️ **幂等脚本的「NEW 超集」陷阱**（2026-09-28 r52 实锤，一次差点把页面改坏）：
  当某条替换的 `NEW` 串是 `OLD` 串的**前缀超集**（如 OLD=`… width: 32px… }`、NEW=`… width: 28px… }\n<新增注释>`），
  第二次运行时 `s.count(OLD)` 仍可能是 1 → **重复追加**，断言随即炸（r52 实测：收缩链 7→11、`#DAE3ED` 10→12）。
  两条对策，**必须同时用**：
  ① 循环里**先判 NEW 标记（newmark 正则），命中就 skip**，再判 `count(OLD)==1`，否则 `sys.exit` 报锚点数；
  ② 跑完**立刻再跑一次**，确认输出是 `应用: 0 项 | 跳过: N 项`（幂等验证）。
  回滚用改动前备份 `cp /tmp/rNN-backup/<page>.html pages/<page>.html`。

- 压缩 bundle 里**删 JSX 子树**（如清空 `children:[...]`）：禁用正则 `.*?`（跨元素吞并）；
  写**括号配平扫描** `match_bracket(s,i)`（跳过反引号/引号字符串）定位配对的 `]` —— 天然适配各页
  变量名差异（`N.`/`j.`/`A.`/`k.`），可一次批量改全站同名同构模块。**保留外层容器宽度**（如 240px 空容器）
  可避免头部布局塌陷。
- **删除类改动先问页面归属**：9 个外壳页各有一份 `flex w-60 items-center justify-end gap-1` 顶栏模块，
  改动前先用 DOM 核实目标页现状，不凭字面推断（用户对"擅自修改未指明的对象"极敏感）。
- **自检断言铁律**（2026-09-28 三次踩坑）：只允许断言 ① 标签级计数（`<style>`/`</style>`/`<script>`/`</script>`）②
  针对"被改对象"的**精确增减量**（如 `new-chat-btn` 词频 +2、`text-3` 恰好 −2）。
  **禁止**"全文件关键词总数不变/等于 N" 这类断言 —— 同一 token 在别处合法出现（`--color-border-2`、`--td-line`、
  `[color:var(--color-text-3)]`），新增 CSS 选择器也必然改变词频，都会误报。
  **最干净的落法**：用注释锚点切出本轮新增的区块（`a=s.find('/* ★ 第 NN 轮…')` → `b=s.find(下一条既有规则前缀, a)`），
  只断言"区块内"的硬编码/残留为 0。既有内容里的同类写法**不属本轮范围，不得擅改**（例：task-detail 基线本就有 2 处
  `font-size: 12px` 属 r41 下拉弹层规则）。
- 替换锚点**必须带上足够长的上下文前缀**（例：改 settings 的「返回」按钮要带 `flex w-fit items-center gap-1.5 …`），
  否则会命中同页其它同色元素（右上角图标按钮用了同一套 text-3 + hover 组合）。
- 压缩 bundle 里改 JSX 内联样式：CSS 覆盖必须 `!important` 才能压过行内 `style`；<br>
  行内硬编码的"手算居中值"（如 `marginLeft:91` = `(240−58)/2`）在宽度可变时必然失效 → 换成 `justify-content:center`
  + 把钉右元素改 `position:absolute`，可做到**改前改后像素一致**且自适应。
- **分隔线取色档位**（2026-09-28 实测）：`--color-border-1`/`--td-hairline` = #F2F2F2（太浅，列表间隔线几乎不可见）；
  `--color-border-2` = #E5E5E5（标准分隔档，页内 `.td-bar-sep` 用它）；`--color-border-3` = #C9C9C9（偏重）。
  列表行间隔线 → border-2；区块级分隔 → `--td-line`(同 #F2F2F2)。
- 文字色档位（DS `tokens.md` 权威）：`--color-text-1` = #1F1F1F（**标题 / 正文**，最高层级）→ text-2 = #4E4E4E（次级语句）
  → text-3 = #868686（次要说明）。「加深一级」= text-3→text-2；「应该是正文颜色」= **text-1**。
  注意 text-1 已是最深正文色，把 hover 也设成 text-1 等于没有 hover 效果（应直接删掉该 hover）。
- 填充色档位（`tokens.md`）：`--color-fill-1` #F7F7F7（最浅/hover 底）→ fill-2 #F2F2F2（浅）→ fill-3 #E5E5E5（中）→ fill-4 #C9C9C9（深）。
  「浅灰底深一级」= fill-1 → fill-2（真实差异只有 5 级灰阶，视觉很微弱；要更明显直接提 fill-3）。
  **hover 底档位（2026-09-28 r57 定稿）**：白底容器内的可点行（列表行、菜单项）hover 一律用 **fill-2**——
  r57 起 `.td-bf:hover` 与 `.td-ctx .giencoder-dropdown-item:hover` 均由 fill-1 提到 fill-2，
  且页面内外壳 DS Dropdown 自身也是 `hover:bg-[var(--color-fill-2)]`。
  ⚠️ 但 r54 曾把设计稿 2× 导出图的右键菜单 hover 量到 #F7F7F7（fill-1）—— **导出图的采样值会受缩放/抗锯齿影响**，
  拿不准时以「DS 组件自身档位 + 用户眼睛」为准。
- **滚动条三档取色**（2026-09-28 r47 定稿）：全局在 `@media (pointer:fine)` 下用 `rgba(var(--gray-10), α)`，
  `--gray-10: 31,31,31`（亮色主题）；**但 task-detail / avatar 另有手写局部档** `--scrollbar-thumb-bg: rgba(0,0,0,0.16)` / `-hover: rgba(0,0,0,0.28)`。
  → **改滚动条必须同改 4 类锚点**：① 各页内联产物 3 档（`.08/.12/.16`）② `scrollbar-color`（Firefox 系）③ 局部手写 hover 值 ④ DS 源（`colors_and_type.css` + `gienx-templates/_shared/tokens.css`）。
  口径区分：「默认加深一级」= `.08→.16`；「hover 浅一级」= `.28→.24`（不是把 hover 也加深）。设计稿 `1350:18310` 内滚动条实测 `rgba(0,0,0,0.16)` 6px，即"默认 .16"的佐证。
  ⚠️ DS 源替换**必须带选择器名做锚点**（`::-webkit-scrollbar-thumb:active {\n    background-color:`）；裸值替换会串味（`0.16→0.32` 与 `0.08→0.16` 互相污染，复跑再推进一档）。
- ⚠️ **Tailwind 编译产物的圆角反直觉**：页面里 `--radius: .625rem`(=10px) ⇒ `.rounded-md` = `calc(var(--radius) - 2px)` = **8px**、
  `.rounded-lg` = **10px**、`.rounded-full` = 9999px。**不要**按 Tailwind 默认（md=6 / lg=8）推理，先 `getComputedStyle` 实测。
- ⚠️ **不能"许愿"新类名**：产物只编译了构建期用过的类，手写 `rounded-[8px]` / `gap-[48px]` 之类的类名**不会生成 CSS**。
  改样式只有两条路：① 复用已编译的类（如 `rounded-full` → `rounded-md`）② 在该页 `<style>` 里自己写规则。
- 已复用的尺寸配方：**AI 对话框（`.td-composer`）总高 128px** = 输入区 `min-height:70` + 工具条 32 + 卡片内距 12×2 + 边框 1×2；
  task-detail（r41）与 avatar（r45）同配方。右栏标题留白 = `.td-right-bar { gap }`（8 → 48 即可满足"≥48px"，代价是标题可用宽度同步 −40px）。
- **avatar 页右栏是默认收起的抽屉**（`.td-right.av-chat-drawer`，width 0 / visibility hidden）：改这里的样式**截图看不到**，
  只能靠 `agent-browser eval` 做 DOM 断言取证（inline `!important` 强设宽度也压不住，别浪费时间试图展开）。
- **浏览态（`.is-browse`）隐藏某栏 = 纯 CSS 一行**（r60）：先全文件扫 `querySelector / getBoundingClientRect /
  classList / offsetWidth` 附近的类名确认**无 JS 依赖**，再追加 `.td-root.is-browse .td-side { display:none }`。
  不要挂 `.is-keep-left` 之类的条件类（窄视口下那栏本就 `display:none`，挂上是冗余）。
  r60 实测：浏览态正文列 332 → **598px**（1920），普通态零影响；退出浏览态自动恢复、无需 JS。
- **「图标小两号 / 大一点」这类需求 = 只缩 svg，别动图标框**（r61）：框宽决定文字起始 x，
  动框会破坏已有的逐像素对齐基线。`.td-more-ico svg` 16→12px 后 label 起点仍是 **37px**、
  菜单仍是 **130×76**，只是墨迹 14px → 10.5px。
- **危险项（删除/取消一类）hover 配方**（r61，页内既有档，别新造色）：
  底 `--color-danger-light-1`(#FFECE8) + 前景 `--color-danger-6`(#F53F3F)，
  与 `.giencoder-tag-danger` 同源。要点：① 选择器写 `.x.is-danger:hover`(0,4,0) 稳过通用 hover；
  ② 子元素若自带 `color`（如 `.td-more-ico`）**继承拿不到**，必须单独覆盖；
  ③ 行与图标都要补 `transition: color 120ms`。
- ⚠️ **弹层几何必须在动画结束后量**（r61）：`.td-more` 入场有 `scale: .96 → 1`，
  刚点开就量会得到 130×0.96 ≈ **125×73**，误判成「尺寸被改小了」。
- **移植 motion-primitives 组件**（r62）：源码不在文档页，去官方 registry 拿 verbatim ——
  `https://motion-primitives.com/c/<name>.json` → `files[0].content`。移植三坑：
  ① 原版元素多为 `inline-block`（背景贴字）；本地若是块级撑满，`background-size:250%` 的光带会
  大半时间扫在空白上 → 加 `width: fit-content` 让盒子贴字；
  ② 色值一律换 DS token（禁硬编码 hex，`#0000` 透明除外）；
  ③ 状态选择器用 `:has()`（`.kb-card:has(.kb-running)`），Chromium/Electron 均支持。
- **动画相位取证用 WAAPI，不要用 `animation-delay`**（r62）：`animation-delay` 只定**相对**相位
  （绝对相位还叠了已运行时长，不可复现）；正解 `el.getAnimations()[0]` → `pause()` + `currentTime = T`。
  reduced-motion 用 CDP `Emulation.setEmulatedMedia({features:[{name:'prefers-reduced-motion',value:'reduce'}]})` 实测。
  ⚠️ **`document.getAnimations()` 包含伪元素**（`a.effect.pseudoElement === '::after'`），所以 `::after` 上的
  动画也能钉相位；但**逐个方案钉相位要筛同名动画**（`filter(a => a.animationName === 'v-bar')`），
  否则会把全页同相动画一起钉住（r65 的对比页就是这样，是特性不是 bug）。
- ⚠️ **`var()` 缺失会让整条声明「计算期静默失效」**（r65 血泪）：自定义属性没定义且 `var()` 无 fallback 时，
  不是回退该变量，而是**整条属性作废**（如 `background: conic-gradient(..., var(--color-primary-7), ...)`
  → `backgroundImage` 变 `none`）。症状极具迷惑性：**伪元素、动画、`getAnimations()` 全部正常，就是看不见**。
  → 排查口诀：**先读 `getComputedStyle(el,'::after').backgroundImage` 是不是 `none`**，再核对该页 `:root` 里
  `var()` 引用的每个 token 是否都有定义（r65 漏了 `--color-primary-7`，A/B 两个方案全瞎）。
  新建 demo/对比页时，**先把要用的 token 一次性抄全并逐个 eval 校验**，别边写边补。
- ⚠️ **单段扫描光带必然有「空白期」**（r65）：`width:42%` + `translateX(-100% → 250%)` + `alternate`
  ⇒ 光带约 **1/3 周期整个在容器外**，实机看像闪烁（定性结论用「按相位算交集宽度」验证，别靠肉眼看截图）。
  正解：**超宽元素 + 中心光带 + 窄幅平移** —— `left:-100%; width:300%`，渐变峰值落在元素 50%
  （左右各留 14% 透明边），`@keyframes { from { translateX(-16.7%) } to { translateX(+16.7%) } }`
  ⇒ 光带与容器**任何时刻都相交**（r65 20 相位扫描可见宽度 133~267px，最小 = 容器 42%）。
  同一口诀适用于「不确定进度条 / 描边流光 / 呼吸光」这类需要持续可见的动效。
- ⚠️ **PIL 合成图的画布高度必须按公式算**（r65）：`Image.new('RGB',(W,H))` 的 `H` 少算时 `paste` **越界静默裁剪**，
  报错为零、出图看不出，但最后一行被切掉（r65 少算 80px，B 行整条没了）。
  → 用「表头 + 行数 ×(标题+副标题+图高+说明+行距)」显式求和；跑完**回读 `Image.open(...).size` 与公式对一遍**。
- **行内 style 与「激活态」互斥**：常态/激活态若都写在元素 `style="…"` 上，`:focus-within`/`onFocus` 类选择器**永远赢不了**
  → 必须把**常态也搬到类上**、行内 style 整个删掉（r54 对话框激活态即此路）。同款模块（base/task-detail/avatar）三页要一起改。
- **`overflow: visible` 外壳里做 `translateX` 入场**会溢出并撑出横向滚动条 → 包一层同尺寸**透明裁剪窗口**
  （`flex:1 1 auto; min-width:0; overflow:hidden`，几何零变化），位移只发生在窗口内（r54 `.td-browse-slot`）。
- **MasterGo `get_screenshot` 导出节点图默认 2×**：量测前先用**边框像素（#E5E5E5 = 229±3 灰阶）**定位卡片外框，
  不要用 `<250` 阈值（会把投影光晕算进去）。
  ⚠️ **口径陷阱**：量到的「白区宽」是**内容区**，而 CSS `width` 默认 `border-box` —— 1px 边框会让内容区各少 1px。
  实测值 180 的白区 → 要写 `width: 182px`（r54 首版写 180 导致 item 少 2px，r55 才修正）。
- **自建菜单与外壳同名类冲突**：每页 React 产物里已有一份 `.giencoder-dropdown-popup`（`animation: .2s popup-in`，
  播完 `opacity` 回落 0）→ 自建弹层必须**双类提权**（`.td-ctx.giencoder-dropdown-popup`）+ `animation: none`。
  子菜单定位直接抄 DS：`.giencoder-dropdown-submenu-popup { left: calc(100% + 4px); top: 0 }`（右侧弹出、越界翻左）。
- ⚠️ **`display:none` 元素上 `.click()` 静默失效**：连续 toggle + 派发 `Escape` 后抽屉状态机会错位，
  后续 rect 全 0、误判「功能没生效」。**断言失败先 `$AB open <url>` 重载拿干净状态**，别在脏状态上继续推理。
- ⚠️ **多个 `document.addEventListener('keydown')` 的协作是「顺序相关」的**：同段同相时按**注册顺序**跑，
  且「首次打开某面板时才注册」的监听必然排在后面。**任何靠读全局状态位（如 `data-xxx-open`）来让位的写法都会失败** ——
  先跑的那个会同步摘掉状态位，后跑的读到 false 就照旧执行。
  → **让最先决策的那一环在事件对象上打标记**（`e.__xxxHandled = true`），其余监听判标记，才与顺序无关（r56 实测）。
- **动效中间帧取证**：`el.getAnimations()[0]` → `a.pause(); a.currentTime = 36;` **精确定格**再截图；
  直接「点了就截」几乎抓不到（截图耗时 > 280ms 动效，两帧 md5 会完全相同）。
- ⚠️ **验收脚本别混入会导航的操作**：同一个 eval 里触发 `location.href` 跳转会打断 CDP
  （`Inspected target navigated or closed`），整轮白跑。分步 eval，每步只读状态。
- ⚠️ **多栏布局「新增/恢复一栏」时，拖动换算的绝对坐标基准会静默失准**（2026-09-28 r58 实踩）：
  task-detail 原是 `setRight(x - root.left)`（AI 栏从根左缘起算，因为左侧当时被 `display:none`）。
  r58 让浏览态左栏以 600px 保留后起始 x 右移 608px，换算没改 → 实测「拖 +420px」一步顶到钳位上限、光标与分隔条脱节。
  修法三件套：① 换算减去新栏占位；② 在 `pointerdown` **冻结**该占位（不冻结会「拖宽 A → B 自动收窄 → 基准漂移」正反馈）；
  ③ 给被拖栏加「不挤破左右保底」的上限，否则拖到临界点左栏会突然消失、分隔条跳变。
- **task-detail 浏览态（`.td-root.is-browse`）三栏分配规则**（r58 定稿；改前是「左栏 `display:none`」）：
  `可给左栏 = rootW − AI会话栏 − 8px间隙 − 预览栏兜底(641 = MIN_TREE+1+MIN_CODE)`；
  ≥480 则保留（加 `.is-keep-left`，宽 = `min(600, 可给宽)`），<480 摘类回退 `display:none`（旧行为）。
  生效阈值 rootW ≥ 1609（≈视口 1625px）→ **1440 / 1600 视口维持旧行为是规则本身的结论，不是 bug**。
  保留态左栏必须自带 `margin-right: var(--td-gap)`（那 8px 平时由 `.td-gutter` 提供，浏览态它是 `display:none`，
  不加会与 AI 会话栏贴死）。
- **拖动条几何取证的最省事口径**：`agent-browser eval` 里直接派发
  `new PointerEvent('pointerdown'/'pointermove'/'pointerup', {clientX, clientY, bubbles:true, pointerId:1})`
  —— 比 CDP 鼠标事件轻，且是驱动页面自定义 pointer 拖动逻辑的唯一稳路。`pointerdown` 的 `clientX`
  必须取目标真实坐标（`el.left + 4`），不能给 0。
- **task-detail 里加弹层的固定套路**（r54 右键菜单 / r59 更多操作菜单，两次同坑）：
  ① 自建弹层类名要**双类提权**（`.td-ctx.giencoder-dropdown-popup` / `.td-more.giencoder-dropdown-popup`）——
     本页产物里已有一条外壳自带的同名类（`min-width:168 / padding:6 / transform-origin:top / animation` 播完
     `opacity` 回落 0），单类压不住，必须再显式 `animation: none`；
  ② 开合状态类统一用 `.giencoder-popup-open`（与 Select/Popover 同一套过渡参数）；
  ③ 新增的 `bind*()` 必须写在那**一个大 IIFE 内部**再挂进 `inject()` —— `tdToast` / `KB_HTML` / `ICON`
     都在那层作用域里，`window.tdToast` 是 `undefined`；
  ④ 同页弹层互斥靠自定义事件 + 根上的 `data-td-pop-open`（页尾 Esc 链据此派发 `td:close-popovers`），
     新弹层 `show()` 时派发 `td:close-ctx` + `td:close-popovers`，并自己监听这两个事件；
  ⑤ 想「Esc 关闭 + 焦点回触发器」要挂**捕获段** `keydown`：页尾 Esc 链注册更早且在冒泡段，捕获段先手
     `close()` + `focus()` + `stopPropagation` 最干净（否则链会继续跑到 `location.href='kanban.html'`）。
- **task-detail 里加「模态弹窗」的增量注意点**（r65，取消/终止任务两弹窗）：
  ① **惰性创建**：clean 加载时 `.td-modal` 计数应为 0，`open()` 时才 build DOM（首次打开零成本、避免和页内产物冲突）；
  ② **焦点归还不能读 `activeElement`**：`run()` 里通常先 `close()` 菜单，此时焦点已移到菜单行/body
     → `open(key, trigger)` **显式传入触发按钮**；
  ③ **头部高度是隐含设计值**：关闭按钮 28×28 在 `align-items:flex-start` 下把 head 撑到 28px，
     而设计稿 title y20 / desc y48 ⇒ 中缝恰好 4px ⇒ `.td-modal-desc { margin: 0 }`（否则整体下移 4px）；
  ④ **box-sizing 差 1px**：设计稿「宽 88 / 高 78」这类数字是**含描边**的，DS 按钮 `padding:0 16px` + 1px 边框
     会渲染成 90/62 ⇒ 弹窗内局部覆盖 `padding: 0 15px`；卡片同理 `padding: 15px 20px` 才等于设计稿 78 高
     （r65 首轮实测：按钮 62/90、卡片 80，r65b 统一修正后逐项对齐）；
  ⑤ 遮罩直接用 `--color-mask-bg`、面板 `--shadow3-down`、`z-index: var(--z-index-modal)`（=1001），
     危险按钮复用 `.giencoder-btn-danger`（实测底 rgb(245,63,63) 与设计稿完全一致，不要新造色）；
  ⑥ 打开期间锁滚动：`html.td-modal-lock, html.td-modal-lock body { overflow: hidden }`（加/摘类即可）。
- **像素回归判据**（r65）：拿 2× 设计稿 PNG 与 2× 页面截图比时，
  ① **必须给容差（±4/通道）** —— 设计稿导出图底图常是 `rgba(255,255,255,.95)`（253/254），严格相等会造
     90%+ 的假阳性；
  ② **只比面板内部**（跳过 16px 圆角的弧线区），遮罩/投影区不要算；
  ③ **先做纵向 shift 微扫找最优偏移**再解读残差（r65 本页 1 行标题 vs 设计稿 2 行 ⇒ 卡片以下天然错位 16px，
     `sy=16` 是最优解）；④ 结论要落到「**哪个子区块**差多少」——
     r65 最终 C2 输入框区 0.77%、C4 按钮行**左侧空白 0.00%**（= 几何完美），差异全在字形光栅化
     （本页 Mona Sans VF vs 设计稿字体），这类残差**不是几何 bug，不要再去调数值**。
- **设计稿像素量测工作流已沉淀为 skill `design-pixel-measure`**（含 `scripts/measure.py`：外框轮廓 /
  圆角跨度 / 色阶跳变 / ink bbox / 逐列有墨分段）。核心口诀：**2× 导出要 ÷2**、**透明底比对前合成白底**、
  **设计节点 `width` 含内距不含描边（写 border-box 要 +2）**、**设计稿里的浅灰底很可能是「该项 hover 态」**、
  **别用 ASCII 图判文字偏位，要量 ink bbox + 逐列分段**。
- **全尺寸面板（弹窗级）量测更稳的一套口径**（r65 定稿，补上面几条）：
  ① **面板矩形用 alpha 通道切边**（导出图是 RGBA，`getchannel('A') > 200` 的极值即可，不吃阴影光晕）；
  ② **内部结构用「长横线枚举」**（卡片描边 / 分隔线 / 输入框描边 / 按钮底边一次列全），中间那些
     读不准的间距靠**对称性反推**（r65：卡片↔分隔线间距由页脚右对齐 + 面板内距联立求得）；
  ③ ⚠️ **圆角只能靠「渲染标定 + SSD 反查」定值**：先渲染已知半径（2/4/5/6/7/8/10/12/14/16）的
     fill+border / fill / panel+shadow 三种块做 2× 截图，再把设计稿角部区块与各标定块逐像素 SSD 取最小。
     实测**首行偏移法系统性偏小 0.5~0.9px、角部面积法在小半径完全失真**，两者都不可用于定值
     （r65 结论：面板 16 / 卡片与输入框 8 / 按钮 6，且与 Tailwind 默认档位无关）。
- ⚠️ **页面 2× 截图必须走 CDP**（r65）：`agent-browser screenshot` **只出 1×**，与 2× 设计稿直接比会整体错位。
  用 `Emulation.setDeviceMetricsOverride{width,height,deviceScaleFactor:2}` ⇒ 2880×1800（脚本 `mg-work/r65/shot2x.mjs`）。
- ⚠️ **同一 URL 可能并存多个 page target**（`task-detail.html` 与 `task-detail.html?fresh`）：
  CDP 里模糊匹配会截到**错的标签页**（probe 报 `open=true` 但截图里没弹窗）。
  → 必须用 `location.href` **精确匹配**；截图前先 `$AB eval 'location.href'` 取真 URL 再传给脚本。

## 四、校验

- `python3 verify-design.py ./pages`（必须传目录）
- ⚠️ 它会**重写 `pages/gaps.log`** → 跑完 `git checkout -- pages/gaps.log`
- 对比是否引入新问题：`git show HEAD:pages/X.html` 导出到临时目录，同口径跑两遍比汇总数
- ⚠️ **「汇总数相同」不等于「零影响」**（可能一边修好一条、一边新引入一条）。**逐条 diff 才作数**：
  `... | grep '^│' | sed 's/:[0-9]*//' | sort | uniq -c | sort -rn > /tmp/base.txt`，两遍同口径后 `diff`；
  diff 为空才算真正零新增（r65 结果：76 问题 / 0 critical，与 HEAD 逐条一致）。
- **「零影响」最佳证据 = 改前/改后同状态截图 md5 相同**（r60 实测 `bfdbba5a5144c27938f8f9734809070d`）：
  前提同视口 + 同 DPR + 状态已复位（无动画残留）。比肉眼比对强得多。
- **「内层溢出节点」扫描要剔除省略号元素**（r60 踩坑）：口径
  `scrollWidth > clientWidth + 1 && getComputedStyle(e).overflowX !== 'visible'`；
  且 `text-overflow: ellipsis` + `white-space: nowrap` + `overflow: hidden` 的元素 scrollWidth **必然**
  大于 clientWidth（如 `.td-file-tx`），不剔除会误报「界面被挤坏」。
- 窄宽压测要压到**自动收窄的触底值**（r60：视口 1620 → 左栏恰好 480 = `LEFT_KEEP_MIN`），
  不能只测一个宽视口。
- **`visibility: hidden` 祖先里的组件无法聚焦** → `ta.focus()` 静默失败、`:focus-within` 永不匹配（数字分身抽屉即此）。
  **破局＝探针克隆法**：`createElement('div')` 打上同一个类名 → 挂 body → 塞 `<input>` → 真实 focus/blur 读 `getComputedStyle`。
  全局规则共用，足以证明规则有效；再拿另一页做 A/B（base 页用行内 style，需按 `rounded-[16px]`+`transition-colors` 组合类名定位）。
- 微动效断言用 `el.getAnimations()` 读 `animationName + effect.getTiming().duration`，同时读 `transform` 矩阵验证**位移方向**；
  用 `document.documentElement.scrollWidth === innerWidth` 证明没有横向溢出（比截图快一个数量级）。
- ⚠️ **合成证据图的字体**（r66）：`/System/Library/Fonts/PingFang.ttc` **本机不存在** →
  `ImageFont.truetype` 抛错被吞 → 回退 `load_default()` → 图注**全是乱码**。
  可用：`Hiragino Sans GB.ttc`（idx0=W3 / idx2=W6 粗）、`STHeiti Medium.ttc`（idx1=Heiti SC）。
  **写图前先用 `font.getname()` 断言字体真的加载成功。**
- 证据图上**别在画板内叠加文字**（会压住泳道标题等内容）→ 在画布右侧留 250px gutter，
  只把红/蓝细竖条画在画板边缘，说明文字放 gutter 里。

## 五、git

- 仓库根在坚果云内，锁文件坑多（见 `~/.workbuddy/skills` 或 yuanqi SKILL 的"坚果云 git 锁"节）。
- 判定推送成功：`git ls-remote origin main` 与 `git rev-parse HEAD` 一致即可，`update_ref failed` 只是本地 ref 被锁。
- 🚫 **默认禁止自动 commit / push**（2026-09-28 用户要求）：任务完成后只汇报改动清单，推送由邵先生统一发起。
  **例外：用户显式要求推送时（如 r66「以上任务都完成后全量推送到 github」）立即执行**，不再请示；
  推送后用 `git ls-remote origin main` 与 `git rev-parse HEAD` 比对确认。
- ⚠️ `git remote -v` 的 origin URL 内嵌 GitHub PAT（明文）—— 汇报时不要打印完整 URL。
- ⚠️ **本地可能积压很多轮未提交**（r66 时 HEAD 停在 r37，r38~r66 共 29 轮未提交）。
  用户说"全量推送"时 = 连 `mg-work/` 证据图 + 根 `index.html` 一起 `git add -A`；
  提交前先扫一遍敏感串（`ghp_` / `github_pat_` / `AKIA` / `PRIVATE KEY`），实测无命中。
  仓库已跟踪 `mg-work`（1154 文件），未跟踪增量约 29MB，属既有惯例。

## 六、浏览入口与 file:// 自持约定（2026-09-28 定稿）

- **仓库已就地于** `/Users/shaoyuming/Documents/GienCoderDesignEngineering`（不再另建克隆）；`origin` = theming028/giencoder-design-engineering。
- **根 `index.html`**（新增，非 pages/ 内）＝ 页面导航页：16 张卡片分 4 组（研发工作台 / 基础工作台 / 设计系统 / 文档）。
  改页面后若新增或改名，需同步更新此导航页。
- **所有页面必须可 file:// 直接双击打开**，不依赖任何本地服务。已实测 10 页全部通过：
  `dev / kanban / req-kanban / task-detail / base / avatar / automation / skills / settings` 渲染正常。
- 外壳路由（每页 bundle 内各自一份，变量名被压缩成 `xt`/`St`/`Tt` 等）：
  `xt` = route→文件名，`St` = 文件名→route 的反向表，`Tt()` = 当前 route。
  → file:// 下按**文件名**解析（`St[filename]`），http 下按 **hash** 解析（`N()`）。`task-detail` **不在** `xt` 里，
  但因其 bundle 内容独立，直开仍正常；http 无 hash 时才会落回 base 壳。
- 顶栏页签跳转靠页面内注入块 `<!-- SHELL-TABS-FIX v4 ... 勿手改此块 -->`（捕获阶段接管点击 +
  高亮纠偏；`DEV_PAGES` 名单定义"哪些文件属于研发工作台"）。新增页面务必带上该块。
- file:// 下已验证的跳转链路：顶栏页签 base↔dev ✓、看板卡片 `.kb-card` → `task-detail.html` ✓、
  根导航页卡片 → 目标页 ✓、左栏导航（数字分身/自动化/技能/设置）✓。
- **外壳导航两块注入补丁**（每页各一份，都在 `<!-- ... 勿手改此块 -->` 注释下，新增页面必须带）：
  - `SHELL-TABS-FIX v4`：捕获阶段接管**顶栏页签**点击 + 高亮纠偏。
  - `SHELL-NAV-FIX v5`：监听 `hashchange`，把 `#/route` 还原成真实文件名跳转 →
    修 http 下「侧栏/卡片点了没反应」（外壳 `navigate()` 在 http 只改 hash 且无人监听）。
    路由表取全站并集，含 `/task-detail`（它不在任何单页的 `xt` 里，只有本兜底能接住）。
    用**相对路径**赋值，因此 file:// 与 http 预览（`/static-html/<id>/`）都能落到同目录。
- **Electron 内置预览服务端口/路径**（2026-09-28 实测）：
  `/static-html/791830df2f0ba958/` = 仓库根（可用子路径），`/static-html/22441530f7eeb388/` = `pages/` 目录（子路径 Forbidden）。
  统一浏览入口用**根 id**：`http://127.0.0.1:52574/static-html/791830df2f0ba958/index.html`。
  另：`lsof -iTCP:52574 -sTCP:LISTEN` 可见 Electron 进程。

## 七、提速工作法（2026-09-28 用户反馈"响应慢"后固化）

- ❌ **禁止整文件 Read `pages/*.html`**（单行压缩 bundle，340–620 KB，读一次即烧掉大量上下文）。
  改用：`python3 - <<'PY'` + `re.search(r'...', s)` 只**打印目标片段**（±200 字符上下文）。
- ✅ 独立探测**并行发**（同一条消息里多个 tool call），不要串行等待。
- ✅ 验证优先用 `agent-browser eval` 读 DOM 断言；**截图只在需要看视觉时用**（截图比 eval 慢一个量级）。
- ✅ 同一结论不二次复现；已知的环境事实（如 file:// 已验证通过）不重复测，只测本轮新增假设。
- ✅ 改大文件一律走 `mg-work/rNN/applyNN.py`（正则定位 + 幂等 + 结构计数自检），一次性跑通。

## 八、三个反复会踩的坑（2026-09-28 r49 实锤）

1. **JS 字符串数组里的 HTML 属性引号必须写 `\"`**。`pages/*.html` 的内联手写 HTML 是**每行一个 JS 字符串**（形如 `        "      <div class=\\"td-bf\\">",`）。
   写成真实引号 `class="td-bf-ico"` 会让**整页 bundle 语法错误**（症状：打开后所有交互失效、控制台 `Cannot read properties of null (reading 'click')`），且脚本本身不报错、极难定位。
   → 打补丁后**必须核对 `<script` / `</script>` 计数未变**（r49 中为 9 / 8）。
2. **绝对定位的 `::before` 会盖住 in-flow 内容**。激活高亮用 `.td-bf.is-active::before { background:… }` 时，因绘制顺序在大纲级内容**之后**，图标与文字会被整块遮住（像素实测深色像素 = 0）。
   → 给同级的 `.td-bf-arrow, .td-bf-ico, .td-bf-name` 加 `position: relative; z-index: 1;`（r49 中 `apply49f.py`）。
   泛化：**任何用 `::before/::after` 做背景层、又要透出同级内容的场景，都先想绘制顺序。**
3. **复用既有 localStorage 记忆机制时，新态要"独立变量名 + 更高特指度复位"**。r35 的 `.td-root.is-swapped { flex-direction: row-reverse }` 与 `.td-root.is-collapsed .td-right-inner { display: none }` 位于新增规则**之后**，且记忆里可能残留脏值。
   → 新增态用 `.td-root.is-browse`（**双类特指度** `.is-browse.is-swapped` 一起写）压过；浏览态宽度用新变量 `--td-browse-right-w/-tree-w` + 新字段，**绝不复用** `--td-right-w`。
   → 测"隔离性"：故意写脏记忆 `{swapped:true,collapsed:true,rightW:48}` 再开侧栏，逐项断言布局。

## 九、agent-browser eval 的两个静默失败

- 裸 `eval` 内写 `return` **非法** → 必须包成 `(()=>{ … return … })()`；不套时不报错、**静默返回空**（曾在 r49 造成"默认态 = 592"的假象）。
- 箭头函数简写 `f=s=>…` 会被误判为**组件**；统一写 `const q=s=>…`。
- **合成 PointerEvent 测不了依赖 `setPointerCapture` 的拖动条**（r35 `.td-gutter` 就是）：合成事件下拖动不生效、宽度纹丝不动。
  判定"是否回归"必须先拿**改动前备份**跑同口径对照，别直接下结论（r50 靠这招洗清了一次误判）。

## 十、设计稿 PNG 量测法（r49/r50 固化）

- 节点导出的 PNG 是 **1.5× 且带透明通道**：先 `alpha_composite(白底)`（否则透明区被 `convert('RGB')` 变黑，误判成黑色块）。
- **绝对逻辑坐标 = device / 1.5**。⚠️ 不要再"减 padding 再加 padding"——两者相差一个 1.5 倍系数，正好抵消但极易算错
  （r50 曾因此误判"文件图标比设计稿偏左 20px"，实际只差 1.3px）。
- 逐行量测法：按列统计墨量密度，**先剔除密度 > 0.45 的竖线列**（缩进引导线会贯通全高，导致所有行被并成一行），
  再按行做 run-length 分段，即可读出每行的"图标左缘 / 文字左缘 / 各段宽度"。
- 线条色反推：1px 线在 1.5× 下摊到 2 行 → `C = 255 − 墨量合计 / 1.5`。
- **`--color-border-*` 档位与"深一级"**：border-1 / `--td-hairline` = **#F2F2F2**（结构发丝线，列表间隔线上显得太浅）→
  **border-2 = #E5E5E5**（分栏衔接线、分隔线的标准档，用户说"深一级"基本都指这一档）→ border-3 = #C9C9C9（偏重）。
- ⚠️ **同一份设计稿里不同节点的导出图缩放比可能不同**（2026-09-28 r52 踩到）：
  `193158744355579` 里 `836:26404`（AI 消息组）导出是 **3×**，而 `1350:18310`（文件预览面板）是 **1.5×**。
  **不要跨节点套用缩放比**。判定方法：拿节点的已知逻辑尺寸（如 Link 836:27829 = 164×22）去除 PNG 像素
  → 商即为该图缩放比（r52 实测 492/164 = 3.000 ✓）。另可交叉验证：中文墨迹高 ÷ 缩放 = 字号
  （r52：42 device / 3 = 14px = body-3 ✓）。
- **半倍（0.5×）合成色反解**：低分辨率导出图上取色会与底色混合，`原色 = 合成读数 × 2 − 底色`。
  r52 例：面板描边在 0.5× 图上读 `rgb(223,232,241)`、底色白 `(255,255,255)` → 原色 ≈ `(191,209,227)`；
  再与实现页截图同口径比对得 `#DAE3ED`（DOM 实测 `rgb(218,227,237)`）。
  **判定优先级：DOM `getComputedStyle` 读数 > 设计稿像素反推**（前者永远是真值）。

## 十一、task-detail 文件树（节点 1350:18310）几何配方

> 内容左为 0 的逻辑坐标；缩进步长 20px；行内图标统一 **13px**（设计稿实测 12.7）。

| 元素 | 公式 |
|---|---|
| chevron 盒中心 | `14 + 20d`（= 缩进引导线的 x，必须重合） |
| 文件夹图标左缘 | chevron 中心 `+14` |
| 图标 → 文字间距 | `20`（13 图标 + 7 间距） |
| **文件图标左缘** | **该深度的 chevron 位置**（`8 + 20d`，文件行没有 chevron，图标顶替其位） |
| 缩进引导线 | 只在 **1~3 级**画（x = 34 / 54 / 74 绝对，即内容相对 14 / 34 / 54），第 4 级起不画 |
| 激活行 | 底 `#ECF2FF` + 1px 描边 `#D3E2FF` + 4px 圆角，高度 = 行高 − 2（上下各 1px） |

**改行高/图标尺寸时必须同步重算内距**，否则图标列与文字列会整体漂移：
`左内距 = 14 − 图标/2`、`图标右间距 = 20 − 图标宽`（例：图标 16→13 时，左内距 6→7.5、右间距 8→7.5）。

## 十二、DS 没有 Search 组件 —— 搜索框的标准写法

`giencoder-design-system/components/` 里**没有 search.json**。官方标准搜索框 =
**Input 的 `prefix` 变体**：`div.giencoder-input-wrapper[data-variant="prefix"][data-size="medium"]`
`> span.giencoder-input-prefix > svg(放大镜) + input.giencoder-input[placeholder]`。
契约 `sizes`：mini 24 / small 28 / **medium 32** / large 36；外观 = 白底 + 1px `--color-border-2` 边框 + `--border-radius-medium`
（设计稿里的搜索框实测正是 32px、白底浅边框，与之完全一致）。参照 `preview/component-input.html`。

## 十三、改 DS 组件样式的三个硬坑（r51 踩实）

1. **去掉 DS 组件自带投影，必须覆盖 `:hover` / `:active`**。
   `.giencoder-btn-secondary` 与 `.giencoder-btn-secondary:active` 都带 `box-shadow`，
   后者特指度 `(0,2,0)` 高于裸类选择器 `.td-round-btn` `(0,1,0)` —— 只写基础规则，
   一按下投影就回来了。正确写法：
   ```css
   .td-round-btn, .td-round-btn:hover, .td-round-btn:active {
     box-shadow: none; /* …其余声明 */
   }
   ```
   ⚠ **不要**把 `:focus-visible` 也纳进来 —— `.giencoder-btn:focus-visible` 的
   `0 0 0 2px var(--color-primary-light-2)` 是键盘焦点环（a11y），要保留。
   （`.giencoder-btn-icon` 场景下 `border-color: transparent` 已经把 `--btn-ring` 环抹掉，
   真正可见的只剩 `0 1px 2px #0f172a0a` 这一层浮起投影。）

2. **共享类名被多处复用时，改尺寸必须按上下文限定**。
   `.td-browse-ico` 同时挂在**顶栏「收起侧栏」**（14→16px 图标）和
   **crumb 右侧两个按钮**（16px 图标）上。改顶栏尺寸只能写
   `.td-browse-bar .td-browse-ico { … }`，直接改共享规则会把 crumb 的按钮一起放大。
   新增/修改样式前先 `grep` 该类名出现次数。

3. **"设计稿 vs 实现"对比图必须先对齐锚点再裁图**。
   正确流程：先量出被改对象在各自栅格里的同名锚点（如"文档盒左上角"），
   再以该锚点为中心、按**相同逻辑尺寸**各裁一块，最后缩放到同一像素尺寸。
   ❌ 错误做法：各自按"墨迹 bbox"裁图 —— 抗锯齿会把浅像素算进 bbox，
   两端膨胀量不同 → 两张图**宽高比不同** → 明明形状一致却看着"不一样"
   （r51 差点因此误判圆徽标的位置与半径）。

## 十四、设计稿逐像素回推 SVG 图标的换算法

设计稿导出图常是 1.5×（device px = 1.5 × 逻辑 px）。若图标最终以 `viewBox="0 0 24 24"` 渲染在 16px 盒里，
则 **1 逻辑 px = 1 viewBox 单位**（16/24 × 1.5 = 1，正好抵消）。所以：

```
viewBox_x = device_x − 锚点_device_x        # 锚点取图标最左/最上的描边中线
viewBox_y = device_y − 锚点_device_y
```

例（r51 的「摘要」图标）：文档盒 device x40..56.5 / y19.5..39.5 → viewBox x2.5..19 / y2..22。
读形方法：把目标区域用 ASCII 化打印（`#` < 150 / `+` < 210 / `.` < 243 / 空格 白），
比只看放大 PNG 精确得多 —— 斜切 vs 圆角、圆弧圆心、线段端点都能一次读准。

**圆角 vs 斜切**：把同一段对角线的 Δx、Δy 都量出来。Δx≈Δy ⇒ 圆角；Δx≠Δy（如 3:5）⇒ 直斜切。
r51 的 tab 图标右上角就是 3:5 的直斜切，一开始当圆角画，视觉上"开口"不够。

## 十五、`.td-browse` 顶栏元素尺寸（r52 定稿）

| 元素 | 尺寸 | 说明 |
|---|---|---|
| `+`（`.td-browse-add`）/ X（`.td-browse-ico`，`data-td-browse-close`） | 容器 **28×28**，图标 **16px** | r51 曾放大到 32×32；r52 按用户「容器调整为 28px 即可」回调 |
| crumb 行右侧两按钮（**同名** `.td-browse-ico`：list-tree / compass） | **24×24**，图标 16px | 被 `.td-browse-bar` 前缀规则排除在外，不受顶栏改动波及 |
| `.td-browse-tab`（「摘要」） | 65×32，内含图标 **16px**，色 `--color-text-1` | 设计稿墨迹核心 RGB(31,31,31) = text-1（不是 text-2） |
| `.td-browse-sep` | 1×20px，`--color-border-2` | ✓ 与设计稿一致 |

- **`.td-browse-ico` 是共享类名**：DOM 里第一个命中的其实是**顶栏的关闭 X**（不是 crumb 的 list-tree）。
  量测/改样式前先按 `aria-label`（`收起侧栏` / `隐藏文件目录` / `在浏览器中打开当前文件`）或
  `data-*` 属性确认对象，别凭类名猜语义。
- **图标盒尺寸的证法（r52 定稿）**：设计稿导出图里量墨迹 → 除以该图标自身的 ink 占比。
  Lucide plus（`M5 12h14` + `M12 5v14`，stroke 2）ink 占 24 格中的 16 格 ⇒ **盒 = 墨迹 × 24/16**。
  r52 实测顶栏加号墨迹 **10.7 逻辑px** → 盒 = 16.05 ≈ **16px** ✓（与「未改前」的 16px 一致）。
- ⚠ **未改的顺序差异**：设计稿是 `摘要 │ + … X`（分隔线在加号**之前**），
  实现是 `摘要 + │ … X`（DOM 顺序 = `td-browse-tab` → `td-browse-add` → `td-browse-sep` → `td-browse-acts`）。
  r51 / r52 用户均未提次序，故保留现状待拍板。

## 十六、读懂需求措辞：「容器」≠「图标本身」（2026-09-28 r52 定性）

同一轮里用户会**刻意区分**这两件事，写在一句话里的哪个词就是边界：

> 「其实"td-browse-ico"和"td-browse-add"把**容器**尺寸调整为28px**即可**」
> 「"td-right-acts"**容器内的几个图标本身**的尺寸调整14px」

- 「**容器** … 即可」⇒ 只改外框（width/height），**图标尺寸不动**。
- 「**图标本身**」⇒ 只改 `<svg>` 的 width/height，**外框不动**。
- r52 教训：第 4 项里我把容器 32→28 时"顺手"把 svg 也 16→14，属**过度修改**；
  依据是设计稿加号墨迹 10.7 逻辑px ÷ (16/24) = **16px 盒**（见十五节），且「即可」二字本身就在收窄范围。
  → 拿不准时**只做字面要求的那一项**；想连带改的，先在汇报里列出「建议但未改」。
- 收尾自查口诀：**改完把「我多做了什么」单独列一行**。r52b 就是靠这一步救回来的。

## 十七、右缘锚定触发器的弹层必须右对齐

DS `.giencoder-select-popup` 默认 `left: 0`（左缘对齐触发器）。当触发器被 `margin-left:auto`
钉在容器右缘、且弹层宽（200px）> 触发器宽时，**弹层会向右冲出容器**：

| 对话框宽 | 触发器宽 | 默认 `left:0` 溢出 | 改 `right:0` 后 |
|---|---|---|---|
| 360 | 134 | −23（未溢出） | −89 |
| 320 | 109 | **+2** | −89 |
| 300 | 97 | **+14** | −89 |
| 280 | 84 | **+27** | −89 |

（数值 = 弹层右缘 − 白框 border-box 右缘，负 = 在框内。）
**阈值规律**：溢出量 = `弹层宽 − 触发器宽 − 触发器右侧余量`；余量固定（本页 85px）时，
触发器窄于 **弹层宽 − 余量**（≈115px）就会翻正。所以要**用最窄档验证**，别只看默认宽度。

修法（一行）：`.td-composer .mt-auto .flex.items-center.gap-2 > .giencoder-select > .giencoder-select-popup { left: auto; right: 0; }`

⚠️ **DS 弹层"打开态"取证要等过渡**：开合靠 `.giencoder-popup-open` 类 + spring 过渡，
合成 `view.click()` 之后 **`getBoundingClientRect()` 立刻就对，但 `opacity` 仍是 0**（截图为空）。
必须 `agent-browser wait 400~500` 再截图，否则会误判"没打开"。
（r28 曾因用内联 `display` 代替该类而"实现了但看不见"，同类坑。）

## 十八、微动效：`display` 不可过渡时的三件套（2026-09-28 r53 定型）

显示/隐藏靠 `display:none ↔ flex` 硬切的元素（本页 `.td-browse`、各类弹层），想加动效时：

1. **外框做方向性抹开**：`clip-path: inset(0 0 0 40px round 0 8px 8px 0)` → `inset(0 0 0 0 round ...)`。
   ⚠️ **`round` 必须写、且要抄该元素的 `border-radius`** —— 不写就按 border-box 矩形裁，圆角会被切成直角。
2. **内层元素做跟手位移**：`.x > .x-bar, .x > .x-body { animation: ... translateX(24px) → 0 }`，
   位移会被父级的 `overflow:hidden` 裁掉 ⇒ **零页面溢出**。
3. **收起**：加 `.is-closing` 播反向动画（180ms），**延迟到动画结束再摘状态类**（否则 `display:none` 会瞬间消失）。
   JS 里定时器挂元素上（`pane._browseT`）以便「收起途中又点开」时取消；`animationend` 监听要 `e.target !== pane` 过滤掉内层动画的冒泡。

**为什么不用整栏 `translateX`**：本页 `.td-browse` 右缘已贴外壳内缘，整栏位移会被外壳 `overflow:hidden` 裁出缺口；
内层位移 + 外框抹开是「滑出来」观感与「零溢出」的唯一交集。

**时长档**：进 260ms / 出 180ms（craft.md 上限 300ms）。取证手法：`animationDelay='-0.09s' + animationPlayState='paused'` 定格截图。

## 十九、折叠内容底部渐隐：用 mask 而非盖一层渐变

```css
.td-desc-body { --td-desc-fade: 56px;
  -webkit-mask-image: linear-gradient(to bottom, #000 calc(100% - var(--td-desc-fade)), transparent 100%);
  mask-image: linear-gradient(to bottom, #000 calc(100% - var(--td-desc-fade)), transparent 100%);
  transition: max-height 320ms … , mask-image 320ms …; }
.td-desc-body.is-open { --td-desc-fade: 0px; }
```
- 展开时变量归 0，两端 `calc` 结构一致 ⇒ `mask-image` 可随 `transition` 插值，不会在展开瞬间硬闪。
- **不要**用盖一层渐变 `::after`：展开后还得额外隐藏，且会挡住正文的点击/选词。
- ⚠️ `mask-image:` 不在 `verify-design.py` 的硬编码色检查属性白名单里（只查 `color|background|border*|boxShadow`），
  所以 `#000` 不会误报 TOKEN-GAP；但**别把 `background:` 和 `#000` 写在同一行**。
- 判定「是否真的截断」：`el.scrollHeight > el.clientHeight`（本页 845 > 374，确证硬切）。

## 二十、组件在页面里「没样式」→ 先查页面有没有这条 CSS（2026-09-28 r53 第 7 项）

`pages/*.html` 是 Vite 单文件产物，**DS 的 CSS 是「按需内联」的** —— 页面用到哪块组件，才内联哪块。
所以「组件展开后完全没样式（`padding/radius` 都是 0）」的根因通常**不是**优先级问题，而是**这块 CSS 压根没被内联**。

排查顺序：
1. 在页面里搜该类名**是否有规则块**：`grep -c '\.giencoder-xxx {' pages/X.html`；
2. 没有 → 去 DS 源找参考实现：**`giencoder-design-system/gienx-templates/ui-controls.css`**（Select / DatePicker / 日历全在这）+
   `components.css`（基础组件）+ `components/{slug}.json`（契约）；
3. 逐条抄进页面自己的 `<style>`（用 token，别抄 px/hex），并注明「DS 源文件 + 为何偏差」；
4. 反查整个页面还有哪些同类遗漏：`grep -o '\.giencoder-[a-z-]*' 页面 | sort -u` 对照 DS 源。

实例：r53 第 7 项 —— `.giencoder-select-popup` 有样式、`.giencoder-date-picker-popup` 及 `.giencoder-calendar-*` 全无
⇒ 日历塌成一行纯文本。补齐 18 条规则后恢复正常卡片 + 7 列网格。
（同一块 CSS 在 `pages/kanban.html`、`pages/req-kanban.html` 也可能缺失，未查。）

## 二十一、agent-browser 取证的三个坑（2026-09-28 r53 补）

1. ⚠️ **`agent-browser wait <ms>` 会丢页面状态** —— 点击后 `wait`，随后的 `eval` 读到的类名又回到初始。
   要「等一帧 / 等过渡」：**拆成两次 `eval`**（各自是新进程，天然隔 ~200ms），或直接手动补上
   `.giencoder-popup-open` / `.giencoder-panel-open` 再截图。
2. **弹层开态取证必须确认 `opacity === 1`**：DS 在 `requestAnimationFrame` 里才加开态类，
   同一个 `eval` 里量必然还是 `opacity:0`（`getBoundingClientRect` 却完全正常）—— 截图会是空的。
   同理「关闭态」量到的 `scale: .96` 会让几何看起来「溢出 5px」，是假阳性（`width:200 × 0.96 = 192`）。
3. **A/B 对照页别放在 `pages/` 里跑校验**：临时把改动前的备份复制成 `pages/.xxx.html` 可以正常渲染相对资源，
   但 `verify-design.py ./pages` 会把它一并计入（76 → 97），**跑校验前必须先删掉**。

## 二十二、验证 CSS 伪类态（:hover/:active）：必须用 CDP 真实鼠标（2026-09-28 r57 定型）

伪类态**没有 DOM 属性可改**，`getComputedStyle` 在未悬停时读不到目标值。唯一可靠链路：
`rect` 拿视口坐标（列表/树里要筛 `width>0` 的**可见**元素，隐藏副本 rect 全 0）
→ CDP `Input.dispatchMouseEvent {type:'mouseMoved', x, y, buttons:0}` **发两次**（间隔 ~150ms）
→ **同一 session** 里 `Runtime.evaluate` 读 computed **并**截图逐像素采样交叉验证。

- ❌ **别用 `agent-browser hover <sel>`**：本机实测落点偏到顶栏（`:hover` 链最深处是 HEADER），"成功返回"却不生效 —— 静默假阳性。
- ⚠️ **CDP 要按 URL 精确选 target**：本机常同时挂着多个 page target（`?fresh=N` 的同名页、`chrome://newtab/`），
  `/名字/.test(p.url)` 会误命中 → 事件发到了别的文档。用 `p.url.endsWith('<文件名>')`；
  自查手法：attach 后**同一 session** 里读 `location.href` + `elementFromPoint(x,y).className`，与 agent-browser 侧读数比对。
- ⚠️ **Node 模板字符串里 `\b` 是退格符**：注入 JS 写 `` `/td-bf\b/` `` → `/td-bf<BS>/`，永不匹配且**不报错**（静默返回 null，最难查）。
  要正则词边界得写 `\\b`，更稳是 `^td-bf(\s|$)`。`\d` / `\s` / `\w` 同理。
- ⚠️ `matches(':hover')` 会连同**祖先**一起命中：从深到浅 pick 时会先中 `td-bf-name` 这类子 span（背景 transparent）→ 误判「没生效」。
  正则必须**锚定元素本体**。
- ℹ️ 页面若采用「激活行由 `::before` 覆盖整行」的写法，**激活行看不到 hover 色差**（右键行会顺带 `is-active`）—— 取证挑非激活行。

## 二十三、任务看板 kanban 的固定事实（2026-09-28 r63 定型）

### 泳道映射（列名与卡内状态标签**不同名**，别搞混）
`.kb-col--todo`=**待开始** / `.kb-col--doing`=**进行中** / `.kb-col--stop`=**已终止** / `.kb-col--done`=**已完成**；
卡内「执行中」是**状态标签** `.kb-running`，与列名「进行中」不是一个词。
→ 「进行中泳道」写 `.kb-col--doing`；「执行中卡片」写 `.kb-card:has(.kb-running)`。

### ⚠️ 本页主色真值不是 tokens.md 那个
`kanban.html` 运行时 `--color-primary-6` = `rgb(55, 112, 247)` = **#3770F7**（走 `colors_and_type.css` 的 `--giencoderblue-*`），
**不是** #0064FA（那来自 `gienx-templates/_shared/tokens.css`）。本页色阶：
primary-3 `rgb(180,201,252)` / primary-4 `rgb(142,174,250)` / primary-5 `rgb(102,146,249)` / primary-6 `rgb(55,112,247)`。
→ **给配色方案前先 `eval` 读 `getComputedStyle(document.documentElement)`，不要照抄 tokens.md。**

### 标题字重约定
- `.kb-card-title` base **400**；`.kb-card:hover .kb-card-title` → **500**（r33，配 `padding-right: 8px`）。
- **「进行中」列常驻 500**：`.kb-col--doing .kb-card-title { font-weight: 500; }`（r63，特异性 (0,2,0)）。
- ⚠️ **可变字体加粗通常不改变行宽**：本机 Mona Sans VF 下 14px / 11 个 CJK 字，
  `advanceWidth` 400/500/700 **都是 154px**，但墨迹像素 1081/1278/1332。
  所以「标题盒宽没变」**不等于**字重没生效 —— 别按「加粗必然变宽」推理。

### 文字流光配方（r63 新配色）
```css
.kb-card:has(.kb-running) .kb-card-title {
  --kb-shimmer-spread: 20px;        /* JS 按字数写：len × 2 px */
  width: fit-content;                /* 必须贴字，否则光带大部分周期扫在空白上 */
  background-image: linear-gradient(90deg, #0000 calc(50% - var(--kb-shimmer-spread)),
                    var(--color-primary-6), #0000 calc(50% + var(--kb-shimmer-spread))),
                    linear-gradient(var(--color-text-1), var(--color-text-1));
  background-size: 250% 100%, auto;
  background-clip: text; -webkit-background-clip: text;
  color: transparent; -webkit-text-fill-color: transparent;
  animation: kb-title-shimmer 2s linear infinite;
}
```
静置 `--color-text-1`（与其它卡标题同色，最清晰）· 高光 `--color-primary-6`（品牌蓝扫光）。
**教训**：原「灰底 `text-3` + 深灰光 `text-1`」被用户打回「文字看不太清晰」—— 静置色**不应弱于同区域其它静态文本**。

### 「更多操作」菜单的尺寸真值（r59 → r61 → r64 收敛）
`.td-more-ico` 图标框**恒 16px**，只改里面 svg 的尺寸：16px(r59) → 12px(r61) → **14px(r64，定稿)**。
框宽决定文字起始 x ⇒ `labelLeftOffset` 恒 **37px**、菜单恒 **130×76**、项恒 **120×32**。
危险项 hover 配方：底 `--color-danger-light-1`(#FFECE8) · 图标与文字 `--color-danger-6`(#F53F3F)。

## 二十四、两个标准配方（r66 定稿）

### 1. 蒙层（Modal / Drawer mask）—— 全站唯一口径
> **亮色罩色 `rgba(0,0,0,.4)`（= token `--color-mask-bg: #0006`）+ `backdrop-filter: blur(10px) saturate(100%)`**

- **范本在 `task-detail.html` 的 `.td-coop .giencoder-modal`** —— 遇到"要跟某处统一"的需求，
  **先去全仓搜那个特征值**（本轮搜 `rgba(255, 255, 255, 0.95)` 命中 `.td-coop`），别自己猜。
- 全站 13 处 mask 已统一：9 页 `.giencoder-modal-mask` + `.td-modal-mask` +
  kanban 的 `.kb-coop-mask`/`.kb-crt-mask` + task-detail 的 `.kb-crt-mask`。
  后三者走本地别名 `--kb-*-mask: var(--color-mask-bg)`（查口径时要**解析一层 `var()`**，
  否则静态扫描会误报"未 token 化"）。
- 暗色变体 `--color-mask-bg: #0009` 是既有值，不动。
- ⚠️ `backdrop-filter` 不生效的两个经典原因：① 目标自身 `opacity: 0`（蒙层必须自身动画 `0→1`，或放在无 opacity 的 wrapper 上）；
  ② **`::before`/伪元素上打 backdrop-filter 无效**（blur 的是容器自己）→ 必须用独立子元素。

### 2. 弹窗面板材质（`.td-modal-panel` / `.td-coop` 同款）
```css
background: var(--color-bg-2);                                          /* 不透明兜底 */
background: color-mix(in srgb, var(--color-bg-2) 95%, transparent);     /* = rgba(255,255,255,.95) */
-webkit-backdrop-filter: blur(12px) saturate(100%);
backdrop-filter: blur(12px) saturate(100%);
box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.12);                          /* DS 无对应 token，显式声明 */
border-radius: 16px;
```
DS 的 `--shadow3-down` 是 `0 8px 20px 10%`，**不是**这一档。

### 3. 「容器内纵向滚 + 标题栏固定」—— 不需要 `position: sticky`
前提：标题栏与滚动区是**兄弟节点**（`.kb-col-head { flex: none }` / `.kb-col-body { flex: 1 }`）。
```css
.kb-col-body {
  flex: 1; min-height: 0;                 /* ★ min-height:0 必需，否则 flex 子项不收缩，overflow 失效 */
  overflow-y: auto; overflow-x: hidden;   /* x 必须显式 hidden：卡片 translateX 会撑大 scrollWidth */
  scrollbar-gutter: stable;               /* ★ 所有泳道恒定预留滚动条槽 → 卡片永远等宽 */
}
```
- 头部因**位于滚动区之外**天然固定，改前改后 `headY` 都是 265（已实测）。
- 渐隐提示要用**固定 px**（`calc(100% - 40px)`）而不是比例（`82%`），并按滚动位置动态切
  `is-fade`（下方有内容）/ `is-fade-top`（上方有内容）—— 否则"滚到底最后一张卡还是糊的"。
- ⚠️ `scrollbar-gutter: stable` 的意义：不加时**只有溢出**的泳道被滚动条吃掉 6px，
  出现 `cardW = 307/307/318/318` 这种"泳道间卡片不等宽"，看起来像 bug。
- ⚠️ headless Chrome 下 `::-webkit-scrollbar { width: 6px }` **完全不生效**（恒 11px）；
  可用杠杆只有 `scrollbar-width: none`（→0）与 `scrollbar-gutter: stable both-edges`（→22）。
  **真机 Electron 下自定义滚动条规则生效** —— 不要把 headless 的 11px 当验收指标。
