# PAGES · 页面事实 / token / 标准配方

> `MEMORY.md` 的详情卷（**按需 grep，不要整读**）。工作法见 `PLAYBOOK.md`。

---

## P1 设计系统 token 档位速查（权威 = DS `tokens.md`）

| 类别 | 档位 |
|---|---|
| 文字 | text-1 `#1F1F1F`（标题/正文，最深）→ text-2 `#4E4E4E`（次级语句）→ text-3 `#868686`（次要说明） |
| 填充 | fill-1 `#F7F7F7`（最浅/hover 底）→ fill-2 `#F2F2F2` → fill-3 `#E5E5E5` → fill-4 `#C9C9C9`（深） |
| 边框/分隔 | border-1 = `--td-hairline` `#F2F2F2`（太浅，列表间隔几乎不可见）→ **border-2 `#E5E5E5`（标准分隔档）** → border-3 `#C9C9C9` |
| **容器边缘线**（面板/工作区外框） | **`#ECEEF2`（常规页档）** ／ `#DAE3ED`（**仅 `dev` 路由**档） |
| 危险项 | 底 `--color-danger-light-1` `#FFECE8` + 前景 `--color-danger-6` `#F53F3F`（与 `.giencoder-tag-danger` 同源） |

- ⚠️ **外壳给 main 的边框色是按路由选的**：`` `… border bg-white`, i==='dev' ? `border-[#DAE3ED]` : `border-[#ECEEF2]` ``
  ⇒ **常规页（含 base / avatar / task-detail）的 main 都是 `1px solid #ECEEF2`，只有 dev 页是 #DAE3ED**
  （实测 base.html main：`1px solid rgb(236,238,242)`、radius 10、`box-shadow: none`）。
  页内 `--td-panel-line` **自 r70 起 = #ECEEF2**（r52 曾按详情页设计稿反解取到 #DAE3ED，那是 dev 档，属口径错配）。
  → **下次遇到"某处颜色和 X 不一致"，先去 diff 「外壳按路由给的颜色」+「页内 token 值」两个来源。**

- 「加深一级」= text-3→text-2；「应该是正文颜色」= **text-1**。
  ⚠️ text-1 已是最深正文色，把 hover 也设成 text-1 = 没有 hover（应直接删掉该 hover）。
- 「浅灰底深一级」= fill-1 → fill-2（真差异只有 5 级灰阶，视觉很微弱；要更明显直接提 fill-3）。
- **hover 底档位（r57 定稿）**：白底容器内的可点行（列表行、菜单项）hover 一律 **fill-2**
  （`.td-bf:hover` 与 `.giencoder-dropdown-item:hover` 均已由 fill-1 提到 fill-2；DS Dropdown 自身也是 fill-2）。
  ⚠️ 设计稿导出图的采样值受缩放/抗锯齿影响（r54 曾量到 #F7F7F7）→ 拿不准时以「DS 组件自身档位 + 用户眼睛」为准。
- **危险项 hover 配方**（r61，页内既有档，别新造色）：底 `--color-danger-light-1` + 前景 `--color-danger-6`。
  要点：① 选择器写 `.x.is-danger:hover`(0,4,0) 稳过通用 hover；② 子元素若自带 `color`（如 `.td-more-ico`）
  **继承拿不到**，必须单独覆盖；③ 行与图标都要补 `transition: color 120ms`。
- **滚动条三档（r47 定稿）**：全局在 `@media (pointer:fine)` 下用 `rgba(var(--gray-10), α)`，`--gray-10: 31,31,31`（亮色）；
  **但 task-detail / avatar 另有手写局部档** `--scrollbar-thumb-bg: rgba(0,0,0,.16)` / `-hover: rgba(0,0,0,.28)`。
  → **改滚动条必须同改 4 类锚点**：① 各页内联产物 3 档（`.08/.12/.16`）② `scrollbar-color`（Firefox 系）
  ③ 局部手写 hover 值 ④ DS 源（`colors_and_type.css` + `gienx-templates/_shared/tokens.css`）。
  口径：「默认加深一级」= `.08→.16`；「hover 浅一级」= `.28→.24`（不是把 hover 也加深）。
  ⚠️ DS 源替换**必须带选择器名做锚点**（`::-webkit-scrollbar-thumb:active {\n    background-color:`）；
  裸值替换会串味（`0.16→0.32` 与 `0.08→0.16` 互相污染，复跑再推进一档）。
- **分隔线取色**：列表行间隔线 → border-2（#E5E5E5）；区块级分隔 → `--td-line`（同 #F2F2F2）。

---

## P2 MasterGo 设计稿 → 页面

### P2.1 图标还原（已验证流程）
1. `get_selection_node(projectDir, targetNodeId="<图层ID>")` 拉节点 → 图标只会给
   `<img src="./asset/icons/svg_xxx.svg">`，**拿不到 path**。
2. 素材已自动落盘 `~/.mgmcp/artifacts/blobs/sha256/**`（文件名是 sha256，与 svg_xxx 无直接对应）。
3. **破局点**：blob 内含 `clipPath id="master_svg0_{nodeId}"` → `grep -l "master_svg0_622_08923" *.svg`
   可**精确反查节点 ↔ 文件**。
4. 清洗后用：剥 `<defs>/<clipPath>`、去 `clip-path` 引用；配色**不写死 hex** —— 单色改 `fill="currentColor"`，
   三色 `.md` 徽标走 `class="td-ico-md-body|-fold|-mark is-solid"`。
5. 验证：`agent-browser eval` 读 computedStyle + 放大 probe 截图对照设计稿 PNG
   （`get_screenshot` 可导出设计稿节点大图，落 `~/.mgmcp/resources/screenshots/`）。

### P2.2 量测口径 → **已提升为 skill `design-pixel-measure`**
（含 alpha 合成、非整数倍缩放比、结构量测、线条等效色反推、半倍合成色反解、文本墨迹定位、换行 shift 微扫、
容器总宽与 padding 的配对约束、`get_screenshot` 默认 2× 与 #E5E5E5 边框定位、border-box 差 1px、
圆角渲染标定法、对比图须先对齐锚点再裁）
👉 **接这类活儿之前先读该 skill**，本文件不再复述。

**本项目已定值（直接可用，不必重推）**
- 圆角：**面板 16 / 卡片与输入框 8 / 按钮 6**，与 Tailwind 默认档位无关。
- 图标：`viewBox="0 0 24 24"` 渲染进 16px 盒时 **1 逻辑 px = 1 viewBox 单位**（16/24 × 1.5 = 1 正好抵消）；
  锚点取图标最左/最上的描边中线。
- ⚠️ **同一份设计稿不同节点的缩放比可能不同**（`836:26404` = 3×、`1350:18310` = 1.5×）→ **不要跨节点套用**。
- ⚠️ 判定优先级永远：**DOM `getComputedStyle` 读数 > 设计稿像素反推**。

---

## P3 页面固定事实

### P3.1 task-detail 文件树（节点 1350:18310）几何配方
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

### P3.2 `.td-browse` 顶栏元素尺寸（r52 定稿）
| 元素 | 尺寸 | 说明 |
|---|---|---|
| `+`（`.td-browse-add`）/ X（`.td-browse-ico`，`data-td-browse-close`） | 容器 **28×28**，图标 **16px** | r51 曾放大到 32×32；r52 按用户要求回调 |
| crumb 行右侧两按钮（**同名** `.td-browse-ico`：list-tree / compass） | **24×24**，图标 16px | 被 `.td-browse-bar` 前缀规则排除在外 |
| `.td-browse-tab`（「摘要」） | 65×32，内含图标 **16px**，色 `--color-text-1` | 设计稿墨迹核心 RGB(31,31,31) = text-1 |
| `.td-browse-sep` | 1×20px，`--color-border-2` | ✓ 与设计稿一致 |

- **`.td-browse-ico` 是共享类名**：DOM 里第一个命中的其实是**顶栏的关闭 X**（不是 crumb 的 list-tree）
  → 量测/改样式前先按 `aria-label`（`收起侧栏` / `隐藏文件目录` / `在浏览器中打开当前文件`）或 `data-*` 确认对象。
- **图标盒尺寸的证法**：设计稿导出图里量墨迹 → 除以该图标自身的 ink 占比。
  Lucide plus（`M5 12h14` + `M12 5v14`，stroke 2）ink 占 24 格中的 16 格 ⇒ **盒 = 墨迹 × 24/16**。
- ⚠️ **未改的顺序差异**：设计稿是 `摘要 │ + … X`（分隔线在加号**之前**），实现是 `摘要 + │ … X`
  （DOM 顺序 = tab → add → sep → acts）。r51/r52 用户均未提次序，保留现状待拍板。
- ⚠️ `.td-bf-arrow` / `.td-bf-ico` / `.td-bf-guide` 的内容由 **`::before`** 承载（元素本体是空 span）
  → 探针量 `.td-bf-name` 的 `left` 与 `getComputedStyle(el,'::before').width`，不要直接 `getBoundingClientRect()`。

### P3.3 已复用的尺寸配方
- **AI 对话框（`.td-composer`）总高 128px** = 输入区 `min-height:70` + 工具条 32 + 卡片内距 12×2 + 边框 1×2；
  task-detail（r41）与 avatar（r45）同配方。
- 右栏标题留白 = `.td-right-bar { gap }`（8 → 48 即可满足"≥48px"，代价是标题可用宽度同步 −40px）。
- ⚠️ **avatar 页右栏是默认收起的抽屉**（`.td-right.av-chat-drawer`，width 0 / visibility hidden）：
  改这里的样式**截图看不到**，只能靠 `eval` 做 DOM 断言取证（inline `!important` 强设宽度也压不住）。
- **浏览态（`.is-browse`）隐藏某栏 = 纯 CSS 一行**（r60）：先全文件扫 `querySelector / getBoundingClientRect /
  classList / offsetWidth` 附近的类名确认**无 JS 依赖**，再追加 `.td-root.is-browse .td-side { display:none }`。
  不要挂 `.is-keep-left` 之类的条件类（窄视口下那栏本就 `display:none`，挂上是冗余）。
  r60 实测：浏览态正文列 332 → **598px**（1920），普通态零影响；退出浏览态自动恢复、无需 JS。
- **task-detail 浏览态三栏分配规则**（r58 定稿；改前是「左栏 `display:none`」）：
  `可给左栏 = rootW − AI会话栏 − 8px间隙 − 预览栏兜底(641 = MIN_TREE+1+MIN_CODE)`；
  ≥480 则保留（加 `.is-keep-left`，宽 = `min(600, 可给宽)`），<480 摘类回退 `display:none`。
  生效阈值 rootW ≥ 1609（≈视口 1625px）→ **1440 / 1600 视口维持旧行为是规则本身的结论，不是 bug**。
  保留态左栏必须自带 `margin-right: var(--td-gap)`（那 8px 平时由 `.td-gutter` 提供，浏览态它是 `display:none`）。
  ⚠️ **多栏布局「新增/恢复一栏」时，拖动换算的绝对坐标基准会静默失准**（r58 实踩：`setRight(x - root.left)`
  没改 → 拖 +420px 一步顶到钳位上限、光标与分隔条脱节）。修法三件套：
  ① 换算减去新栏占位；② 在 `pointerdown` **冻结**该占位（不冻结会"拖宽 A → B 自动收窄 → 基准漂移"正反馈）；
  ③ 给被拖栏加「不挤破左右保底」的上限，否则拖到临界点左栏会突然消失、分隔条跳变。

### P3.4 task-detail 里加弹层的固定套路（r54 右键菜单 / r59 更多菜单 / r65 模态弹窗）
① 自建弹层类名要**双类提权**（`.td-ctx.giencoder-dropdown-popup` / `.td-more.giencoder-dropdown-popup`）
   —— 本页产物里已有一条外壳自带的同名类（`min-width:168 / padding:6 / transform-origin:top / animation`），
   单类压不住，必须再显式 `animation: none`；
② 开合状态类统一用 `.giencoder-popup-open`（与 Select/Popover 同一套过渡参数）；
③ 新增的 `bind*()` 必须写在那**一个大 IIFE 内部**再挂进 `inject()` —— `tdToast` / `KB_HTML` / `ICON`
   都在那层作用域里，`window.tdToast` 是 `undefined`；
④ 同页弹层互斥靠自定义事件 + 根上的 `data-td-pop-open`（页尾 Esc 链据此派发 `td:close-popovers`）；
   新弹层 `show()` 时派发 `td:close-ctx` + `td:close-popovers`，并自己监听这两个事件；
⑤ 想「Esc 关闭 + 焦点回触发器」要挂**捕获段** `keydown`：页尾 Esc 链注册更早且在冒泡段，
   捕获段先手 `close()` + `focus()` + `stopPropagation` 最干净（否则链会继续跑到 `location.href='kanban.html'`）。
- **模态弹窗的增量注意点（r65，取消/终止任务两弹窗）**：
  · **惰性创建**：clean 加载时 `.td-modal` 计数应为 0，`open()` 时才 build DOM；
  · **焦点归还不能读 `activeElement`**：`run()` 里通常先 `close()` 菜单，焦点已移到菜单行/body
    → `open(key, trigger)` **显式传入触发按钮**；
  · **头部高度是隐含设计值**：关闭按钮 28×28 在 `align-items:flex-start` 下把 head 撑到 28px，
    而设计稿 title y20 / desc y48 ⇒ 中缝恰好 4px ⇒ `.td-modal-desc { margin: 0 }`；
  · **box-sizing 差 1px**：设计稿「宽 88 / 高 78」这类数字是**含描边**的 → 弹窗内局部覆盖
    `padding: 0 15px`（按钮）、`padding: 15px 20px`（卡片）才等于设计稿高度；
  · 遮罩直接用 `--color-mask-bg`、面板 `--shadow3-down`、`z-index: var(--z-index-modal)`（=1001）；
    **危险按钮复用 `.giencoder-btn-danger`**（实测底 `rgb(245,63,63)` 与设计稿完全一致，**不要新造色**）；
  · 打开期间锁滚动：`html.td-modal-lock, html.td-modal-lock body { overflow: hidden }`（加/摘类即可）。
- ⚠️ **多个 `document.addEventListener('keydown')` 的协作是「顺序相关」的**：同段同相时按**注册顺序**跑，
  「首次打开某面板时才注册」的监听必然排在后面。**任何靠读全局状态位（`data-xxx-open`）来让位的写法都会失败**
  → **让最先决策的那一环在事件对象上打标记**（`e.__xxxHandled = true`），其余监听判标记，才与顺序无关（r56 实测）。

### P3.5 kanban 固定事实（r63 定型）
- **泳道映射**（列名与卡内状态标签**不同名**）：`.kb-col--todo`=**待开始** / `--doing`=**进行中** /
  `--stop`=**已终止** / `--done`=**已完成**；卡内「执行中」是**状态标签** `.kb-running`，与列名「进行中」不是一个词。
  → 「进行中泳道」写 `.kb-col--doing`；「执行中卡片」写 `.kb-card:has(.kb-running)`。
- ⚠️ **本页主色真值不是 tokens.md 那个**：运行时 `--color-primary-6` = `rgb(55, 112, 247)` = **#3770F7**
  （走 `colors_and_type.css` 的 `--giencoderblue-*`），**不是** #0064FA（那来自 `gienx-templates/_shared/tokens.css`）。
  → **给配色方案前先 `eval` 读 `getComputedStyle(document.documentElement)`，不要照抄 tokens.md。**
- **标题字重约定**：`.kb-card-title` base **400**；`.kb-card:hover .kb-card-title` → **500**（r33，配 `padding-right: 8px`）；
  「进行中」列常驻 500（`.kb-col--doing .kb-card-title`，r63，特异性 (0,2,0)）。
  ⚠️ **可变字体加粗通常不改变行宽**：Mona Sans VF 下 14px / 11 个 CJK 字，`advanceWidth` 400/500/700 **都是 154px**，
  但墨迹像素 1081/1278/1332 → 「标题盒宽没变」**不等于**字重没生效。
- ⚠️ **单段扫描光带必然有「空白期」**（r65）：`width:42%` + `translateX(-100% → 250%)` + `alternate`
  ⇒ 光带约 **1/3 周期整个在容器外**，实机看像闪烁（定性结论用「按相位算交集宽度」验证，别靠肉眼看截图）。
  正解：**超宽元素 + 中心光带 + 窄幅平移** —— `left:-100%; width:300%`，渐变峰值落在元素 50%
  （左右各留 14% 透明边），`@keyframes { from { translateX(-16.7%) } to { translateX(+16.7%) } }`
  ⇒ 光带与容器**任何时刻都相交**（r65 20 相位扫描可见宽度 133~267px，最小 = 容器 42%）。
  同一口诀适用于「不确定进度条 / 描边流光 / 呼吸光」这类需要持续可见的动效。
- **「更多操作」菜单的尺寸真值**（r59 → r61 → r64 收敛）：`.td-more-ico` 图标框**恒 16px**，
  只改里面 svg 的尺寸：16px(r59) → 12px(r61) → **14px(r64，定稿)**。
  框宽决定文字起始 x ⇒ `labelLeftOffset` 恒 **37px**、菜单恒 **130×76**、项恒 **120×32**。

### P3.6 DS 没有 Search 组件 —— 搜索框的标准写法
`giencoder-design-system/components/` 里**没有 search.json**。官方标准搜索框 =
**Input 的 `prefix` 变体**：`div.giencoder-input-wrapper[data-variant="prefix"][data-size="medium"]`
`> span.giencoder-input-prefix > svg(放大镜) + input.giencoder-input[placeholder]`。
契约 `sizes`：mini 24 / small 28 / **medium 32** / large 36；
外观 = 白底 + 1px `--color-border-2` 边框 + `--border-radius-medium`。参照 `preview/component-input.html`。

### P3.7 右缘锚定触发器的弹层必须右对齐
DS `.giencoder-select-popup` 默认 `left: 0`（左缘对齐触发器）。当触发器被 `margin-left:auto` 钉在容器右缘、
且弹层宽（200px）> 触发器宽时，**弹层会向右冲出容器**。
**阈值规律**：溢出量 = `弹层宽 − 触发器宽 − 触发器右侧余量`；余量固定（本页 85px）时，
触发器窄于 `弹层宽 − 余量`（≈115px）就会翻正 → 要**用最窄档验证**。
修法（一行）：`.td-composer .mt-auto .flex.items-center.gap-2 > .giencoder-select > .giencoder-select-popup { left: auto; right: 0; }`

### P3.8 `.dot-bg` 是**外壳共用类**（7 页 · r67 查明）
`main` 的 class 由外壳统一生成：`min-w-0 flex-1 h-full overflow-hidden rounded-lg border bg-white dot-bg`
→ **7 页都有**：`base / dev / kanban / req-kanban / settings / task-detail`（`automation` / `avatar` / `skills` 没有）。
定义是各页**内联**一份（`radial-gradient(circle, rgba(var(--gray-7),.10) 1.5px, transparent 1.5px)` / `20px 20px`），
所以改一页不影响其它页 —— 但**改之前必须问范围**（用户说"基础工作台"时，实际是共用类）。
- ⚠️ 页内 r12 注释声明的意图是「点阵 + 4 个大半径软色团弥散色雾（5 层 background-image）」，**实现只落了点阵那一层**；
  暗色变体 `[giencoder-theme='dark'] .dot-bg` 与亮色**逐字相同** ⇒ 等于没生效。
- 可用色雾 token（base.html 内）：`--giencoderblue-*` / `--purple-*` / `--cyan-*` / `--pinkpurple-*`（各 6 档三元组）。
- ⚠️ **点阵是主体，色雾只能当氛围**：浓度 `.62/.40` 会把点阵整个盖住、观感从"波点"变"彩色背景" →
  定稿量级 **`.17/.12/.10`**（< .2）。

### P3.9 avatar（数字分身）r69 新增：AV-BROWSE-SLOT v1
- 从 `task-detail.html` 移植的 `.td-browse-slot`（预览栏）三件套：`<style id="av-browse-css">` +
  `<div class="td-browse-slot" id="av-browse-slot">` + `<script id="av-browse-js">`，
  插在 `<script id="av-chat-js">` **之前**（Esc 裁决靠注册顺序）。
- 位置链：`div:has(> main)` 行内 = `[左导航 aside] [main] [.av-chat-gutter] [#av-chat-drawer] [#av-browse-split] [#av-browse-slot]`。
- 宽度：`flex: 0 0 var(--av-browse-w, 641px)`（**本页独立变量**，不复用 `--td-browse-right-w` / `--td-right-w`）。
- 展开态 = 在 flex 行上挂 **`.av-browse-on`**（源页的 `.td-root.is-browse` 前缀已整段改写）；
  此时左导航 `.av-browse-on > aside:first-child { width:0 !important; min-width:0 !important; padding:0 !important; opacity:0; pointer-events:none }`
  —— 外壳自带 `transition-all duration-200` ⇒ 收缩天然有动画（实测 252→…→0 约 175ms）。
- 记忆键 `giencoder:av-browse:v1` → `{panelW, treeW}`。
- 同页另有既有的 `.td-right-time` 规则（已删元素，CSS 保留）。

**r70 起的四点变化**
- **展开/收起动效改「宽度过渡」**（原来是整栏 `translateX` 位移动画）：
  `.td-browse-slot { display:none; flex: 0 0 0px; min-width:0; overflow:hidden }`
  → `.td-browse-slot.av-slot-placed { display:flex; transition: flex-basis 200ms var(--av-browse-ease) }`
  （`--av-browse-ease: cubic-bezier(.22,1,.36,1)`，与左导航 aside 同值）
  → `.av-browse-on > .td-browse-slot { flex-basis: var(--av-browse-w, 641px) }`
  → `.td-browse-slot > .td-browse { flex: none; width: var(--av-browse-w, 641px) }`（面板不参与收缩，被裁切）
  → `.av-browse-on.is-col-dragging .td-browse-slot { transition: none }`（拖动跟手）。
  `.td-browse` 已改为**常驻 `display: flex`**；`is-closing` 降级为**纯 JS 防抖标记（无对应 CSS）**。
- **`.av-slot-placed`** 是 `place()` 挂好 slot 后打的标记；没有它 slot 保持 `display:none`
  （防止未定位时在 body 末尾露出 641 宽的栏）。
- **`.td-right` / `.av-chat-drawer` 是同一个元素**（aside 上同时挂两个类）。AI 对话框的
  **开合状态选择器 = `html[data-av-chat-open] .av-chat-drawer`**，写入点 `openChat()/closeChat()`，
  触发器 = `[data-av-chat-toggle]`（页内就是那个 `.giencoder-btn-secondary` 按钮）。
- **抽屉改 1px 描边后**：`.av-chat-drawer > .td-right-inner { width: calc(var(--av-chat-w) - 2px) }`
  （内层保持设计宽但扣掉描边，否则溢出内容盒 2px 被裁）；收起态 `border-width: 0`、展开态 `1px`
  ⇒ **闭合时箱宽真为 0**（否则 border-box 下最小 2px）。
  实测：内层 480 → **478**，`.td-composer` 440 → **438**（= 详情页同宽）。

**r71 起的四点变化**
- **让位逻辑拆成「期望宽 / 生效宽」**（修棘轮）：`wantPanel/wantTree`（只由 恢复记忆 / 拖动 / 键盘 / 双击 改写）
  + `panelW = clamp(wantPanel, MIN_PANEL, maxPanelW())`。持久化写期望宽。
  ⚠️ 调用点 3 处：`clampNow` / `setOpen` / 「显示文件目录」切换。
- **常量定稿**：`DEF_PANEL = 641`、`MIN_PANEL = **561**`（= `MIN_TREE 240` + 分栏条 1 + `MIN_CODE 320`；
  旧的 641 与「内部两栏最小宽之和」自相矛盾，等于把面板钉死在默认值）、`MAIN_MIN = **380**`。
  `maxPanelW() = max(MIN_PANEL, freeW() - chatW() - GAP(8) - MAIN_MIN)`。
- **容器查询 3 档，且整组必须排在 `<style>` 块末尾**（`@container` 与基础规则同特异性时后出现者胜）：
  `≤560`（头换行 / 头像 72 / 卡片单列 / 行卡自适应高 / 页脚自适应 / 行动作区独占一行）、
  `≤420`（卡片头 6px 14px、卡片体 14px 14px 12px、`.av-row` padding 14px）、
  `≤300`（头像 56、face 字号 22）。
  头像字形字号走自定义属性 `--av-face-size`（40 / 28 / 22，DS 字号 token 无这三档）。
- **实测几何**（1440 双开 = AI 会话栏 + 预览栏）：`[左导航 0][main 371][gutter 8][抽屉 480][split 9][预览栏 561]`
  → `.av-main 310` 单列；空窗放大到 1920 → 预览栏自动回 **641**、`.av-main 710` → 容器查询关闭、网格 2×2。
  视口 ≤1100 时 main 会被压到 ~0（预览栏 561 是硬下限，无法再让）。

---

### P3.10 base.html 波点涟漪（`.r74-ripple`）—— **r79 起已停用**（代码保留）

> ⚠️ **现状（r79 定稿）：欢迎态任何位置都不触发涟漪。** 脚本与样式**仍在文件里不删**，便于回退。

**真实 DOM 血缘（r79 实测，别按"块数"推断）**：
```
MAIN.dot-bg                                     [268,48,1164,844]
  └ DIV.relative flex h-full min-w-0 flex-col overflow-hidden  [269,49,1162,842]   ← children 只有这 1 个
      ├ DIV.flex flex-1 flex-col items-center justify-center px-6   [269,49,1162,759] ← 内容块
      └ DIV.pb-6 text-center text-xs leading-relaxed                [269,808,1162,82] ← 版权带
```
⇒ `main.dot-bg.children.length === 1`；两块是**外壳的子元素**，不是 main 的直接子元素。

**触发判定链（`<script id="r74-base-js">` 内 · 绑在 `document` 的 `pointerdown` 捕获段）**：
```js
if (!t.closest('main.dot-bg')) return;                        // 闸 1
if (t.closest('button, a, input, textarea, select, label, …')) return;  // 闸 2 交互控件
if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;  // 闸 3 (r78) 内容块
if (t.closest('div[class*="pb-6"][class*="text-center"]')) return;                // 闸 4 (r79) 版权带
```
**闸 3 + 闸 4 = main 内两块全覆盖 ⇒ 全页 0 触发**（r79 实测 1440×900 网格 96 点 `fired=0`）。

**关键实测值（r79 · 1440×900）**：
| 项 | 值 |
|---|---|
| `.r74-ripple` 点阵 | `background-size: 16px 16px`（与 `.dot-bg` **同值**，逐点对齐） |
| `.r74-ripple` 点色 | `rgba(43,43,43,0.14)` · 点径 `1.7px`（r78 由 0.28 减半而来） |
| `.dot-bg` 底色点 | `rgba(107,107,107,0.1)` · 点径 `1.5px` · `16px 16px` |
| `--r76-rip-cap` / 时长 / z-index | `480px` / `300ms` / `0` |

**⚠️ 点阵密度与底色耦合**：涟漪层与 `.dot-bg` 必须同 `background-size` 才能逐点对齐，
所以 r76 把底色从 20px 加密到 16px 时，涟漪点数一起 ×1.56 —— 削弱特效时若只降不透明度，
点数变多会抵消掉一部分减弱。见 PLAYBOOK P3.9 ③。

---

### P3.11 settings（设置页）r85 新增：导航 + 「系统设置」内容（节点 1389:18609 / 1389:18725）

> 块：`<style id="r85-set-css">` + `<script id="r85-set-js">`（`SHELL-R85-SET v1`），落地脚本 `mg-work/r85/apply85.py`。
> 宿主：`aside > div[class*="overflow-y-auto"]` 插导航、`main > div` 插内容；原 React 节点 `data-set-hidden` 隐藏。

**坐标系（写探针必看）**：`.r85-page-host { width:860px; margin:12px auto 0; padding:0 10px }`，
**内容盒左缘 = host + 10**；与设计稿同原点的元素是 **`.r85-page`（840 宽）**，探针基准用它，别用 host。

| 项 | 值 |
|---|---|
| 导航 | `.r85-nav-host` 232×268；`.r85-navi` 232×36 r8，图标 16×16 @(12,10)；常显底 `--color-fill-1`，选中底 `#ECEEF2` + 图标 `--color-primary-6`；分组标题 `.r85-gt` y=52 / 208 |
| 内容 | `.r85-title` 28 高（`--font-size-title-2` 20px / 500）；卡片 margin-top 16（首张 24），`padding:20px` r8 |
| **卡片描边** | ★ **必须 `outline:1px solid var(--color-border-1); outline-offset:-1px`**（设计稿内描边，不吃内容盒）。写 `border` ⇒ 行宽 798、卡片高 +2、整列推低 2–3px |
| 卡片高 | 首 230 / 中 **448**（`is-mid`：底内距 16 而非 20）/ 末 156；页高 918（设计 919） |
| 行 | `.r85-row` 800×42 @x20；`.r85-ic` 40×40 r8 底 `--color-fill-2`；`.r85-tx` margin-left 12（**末张卡片 `is-tail` = 16**）；行距 32；分割线 `::before` `top:-16` 用 `--color-fill-2` |
| 文本 | `.r85-t` 14px/22 `--color-text-1`；`.r85-d` 12px/16 `--color-text-3` |
| `.r85-ctl` | `gap:8px`；**`.r85-cb` 额外 `margin-right:4px`**（设计稿复选框→按钮间距 12）；右对齐 |
| `.r85-btn` | `min-width:104px; height:32px; padding:0 12px; border:1px solid --color-border-1; background --color-white`；`.is-danger` = `--color-danger` |
| `.r85-seg` | `gap:8px`，按钮 128×40 r8，选中 `border:2px dashed --color-border-3` |
| `.r85-sw` | 覆盖 DS switch：40×24 r12，开 `--color-success` / 关 `#6B6B6B`，手柄 20×20（开 left18 / 关 left2） |
| **`.r85-slider`** | 252×36。轨道 `.r85-sl-track` rel(6,6) 240×1；已选 `.r85-sl-done` rel(6,6) 宽 48；**6 档 `stops=[6,54,102,150,198,246]`**（当前 idx=1）；刻度 `.r85-sl-tick` 1×8 @rel y2 **挂 `.r85-slider`（不是 track）**，`is-on` 深色；拇指 4×12 @rel y0 `margin-left:-2px`；标签「小/默认/大」锚档 0/1/5（中心 rel 6/54/246） |

**禁区**：① 别把刻度挂 `track` 上（`top` 会叠加 track 的 6px）；② 内容盒宽靠 `padding:0 10px` 得来（host 860 → 内容 840）；
③ 其余菜单（模型/连接器/已归档任务）无设计稿 ⇒ `.r85-empty` 空态占位。

---

## P4 标准配方（r66 / r67 定稿）

### P4.1 蒙层（Modal / Drawer mask）—— 全站唯一口径
> **亮色罩色 `rgba(0,0,0,.4)`（= token `--color-mask-bg: #0006`）+ `backdrop-filter: blur(10px) saturate(100%)`**

- **范本在 `task-detail.html` 的 `.td-coop .giencoder-modal`** —— 遇到"要跟某处统一"的需求，
  **先去全仓搜那个特征值**（r66 搜 `rgba(255, 255, 255, 0.95)` 命中 `.td-coop`），别自己猜。
- 全站 13 处 mask 已统一：9 页 `.giencoder-modal-mask` + `.td-modal-mask` +
  kanban 的 `.kb-coop-mask` / `.kb-crt-mask` + task-detail 的 `.kb-crt-mask`。
  后三者走本地别名 `--kb-*-mask: var(--color-mask-bg)`（查口径时要**解析一层 `var()`**，
  否则静态扫描会误报"未 token 化"）。暗色变体 `--color-mask-bg: #0009` 是既有值，不动。
- ⚠️ `backdrop-filter` 不生效的两个经典原因：① 目标自身 `opacity: 0`（`opacity < 1` 会创建独立层且模糊不可见）
  → 蒙层必须自身动画 `0→1`，或放在**无 opacity 的 wrapper** 上；
  ② **`::before` / 伪元素上打 `backdrop-filter` 无效**（blur 的是容器自身背景而不是容器后面的内容）
  → 必须用独立 wrapper 子元素。

### P4.2 弹窗面板材质（`.td-modal-panel` / `.td-coop` 同款）
```css
background: var(--color-bg-2);                                          /* 不透明兜底 */
background: color-mix(in srgb, var(--color-bg-2) 95%, transparent);     /* = rgba(255,255,255,.95) */
-webkit-backdrop-filter: blur(12px) saturate(100%);
backdrop-filter: blur(12px) saturate(100%);
box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.12);                          /* DS 无对应 token，显式声明 */
border-radius: 16px;
```
DS 的 `--shadow3-down` 是 `0 8px 20px 10%`，**不是**这一档。保留不透明兜底行 → 不支持 `color-mix` 的环境自动回退。

### P4.3 「容器内纵向滚 + 标题栏固定」—— 不需要 `position: sticky`
前提：标题栏与滚动区是**兄弟节点**（`.kb-col-head { flex: none }` / `.kb-col-body { flex: 1 }`）。
```css
.kb-col-body {
  flex: 1; min-height: 0;                 /* ★ min-height:0 必需，否则 flex 子项不收缩，overflow 失效 */
  overflow-y: auto; overflow-x: hidden;   /* x 必须显式 hidden：卡片 translateX 会撑大 scrollWidth */
  scrollbar-gutter: stable;               /* ★ 所有泳道恒定预留滚动条槽 → 卡片永远等宽 */
}
```
- 头部因**位于滚动区之外**天然固定。渐隐提示要用**固定 px**（`calc(100% - 40px)`）而不是比例（`82%`），
  并按滚动位置动态切 `is-fade`（下方有内容）/ `is-fade-top`（上方有内容）。
- ⚠️ **`scrollbar-gutter: stable` 的意义**：不加时**只有溢出**的泳道被滚动条吃掉 6px，
  出现 `cardW = 307/307/318/318` 这种"泳道间卡片不等宽"，看起来像 bug。
- ⚠️ **headless Chrome 下 `::-webkit-scrollbar { width: 6px }` 完全不生效**（恒 11px）；
  可用杠杆只有 `scrollbar-width: none`（→0）与 `scrollbar-gutter: stable both-edges`（→22）。
  **真机 Electron 下自定义滚动条规则生效** —— 不要把 headless 的 11px 当验收指标。

### P4.4 折叠内容底部渐隐：用 mask 而非盖一层渐变
```css
.td-desc-body { --td-desc-fade: 56px;
  -webkit-mask-image: linear-gradient(to bottom, #000 calc(100% - var(--td-desc-fade)), transparent 100%);
  mask-image: linear-gradient(to bottom, #000 calc(100% - var(--td-desc-fade)), transparent 100%);
  transition: max-height 320ms …, mask-image 320ms …; }
.td-desc-body.is-open { --td-desc-fade: 0px; }
```
- 展开时变量归 0，两端 `calc` 结构一致 ⇒ `mask-image` 可随 `transition` 插值，不会在展开瞬间硬闪。
- **不要**用盖一层渐变 `::after`：展开后还得额外隐藏，且会挡住正文的点击/选词。
- ⚠️ `mask-image:` **不在** `verify-design.py` 的硬编码色检查属性白名单里（只查 `color|background|border*|boxShadow`），
  所以 `#000` 不会误报 TOKEN-GAP；但**别把 `background:` 和 `#000` 写在同一行**。
- 判定「是否真的截断」：`el.scrollHeight > el.clientHeight`。

### P4.5 微动效：`display` 不可过渡时的三件套
显示/隐藏靠 `display:none ↔ flex` 硬切的元素（`.td-browse`、各类弹层）想加动效时：
1. **外框做方向性抹开**：`clip-path: inset(0 0 0 40px round 0 8px 8px 0)` → `inset(0 0 0 0 round ...)`。
   ⚠️ **`round` 必须写、且要抄该元素的 `border-radius`** —— 不写就按 border-box 矩形裁，圆角会被切成直角。
2. **内层元素做跟手位移**：`.x > .x-bar, .x > .x-body { animation: … translateX(24px) → 0 }`，
   位移会被父级的 `overflow:hidden` 裁掉 ⇒ **零页面溢出**。
3. **收起**：加 `.is-closing` 播反向动画（180ms），**延迟到动画结束再摘状态类**（否则 `display:none` 会瞬间消失）。
   JS 里定时器挂元素上（`pane._browseT`）以便「收起途中又点开」时取消；
   `animationend` 监听要 `e.target !== pane` 过滤掉内层动画的冒泡。

**为什么不用整栏 `translateX`**：本页 `.td-browse` 右缘已贴外壳内缘，整栏位移会被外壳 `overflow:hidden` 裁出缺口；
内层位移 + 外框抹开是「滑出来」观感与「零溢出」的唯一交集。**时长档**：进 260ms / 出 180ms（craft.md 上限 300ms）。

### P4.6 ⚠️ `var()` 缺失会让整条声明「计算期静默失效」
自定义属性没定义且 `var()` 无 fallback 时，**不是回退该变量，而是整条属性作废**
（如 `background: conic-gradient(…, var(--color-primary-7), …)` → `backgroundImage` 变 `none`）。
症状极具迷惑性：**伪元素、动画、`getAnimations()` 全部正常，就是看不见**。
→ 排查口诀：**先读 `getComputedStyle(el,'::after').backgroundImage` 是不是 `none`**，
再核对该页 `:root` 里 `var()` 引用的每个 token 是否都有定义。
新建 demo/对比页时，**先把要用的 token 一次性抄全并逐个 eval 校验**，别边写边补。
（r69 移植预览栏时即补了 avatar 缺的 `--td-panel-line: #DAE3ED` / `--td-hairline: var(--color-border-1)`。）

### P4.7 「光斑跟随指针」标准配方（r67 定稿 · base.html 的 `.dot-bg`）
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
配套 JS（**必须文档级事件委托**，见 PLAYBOOK P3.1）：
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
最像 AI 产品登录页的动态波点做法。纯 CSS 巡游版把圆心写进 `@keyframes` 即可（见 r67 的 A+D 版）。

### P4.8 「折叠 / 展开 = 宽度舒展」标准配方（r70 定稿）
> 用户口径："要像左导航 aside 的折叠/展开那样" ⇒ **纯宽度过渡，不做位移、不做 clip-path、不靠 `display` 硬切**。
> 左导航那条曲线来自外壳的 Tailwind `ease-[cubic-bezier(0.22,1,0.36,1)]` + `duration-200`。

```css
/* 容器：自己过渡 flex-basis；min-width:0 必需（flex 项默认 min-width:auto 会被内容撑开，过渡直接失效） */
.panel-slot {
  --panel-ease: cubic-bezier(0.22, 1, 0.36, 1);
  display: none; flex: 0 0 0px; min-width: 0; overflow: hidden;
}
.panel-slot.is-placed { display: flex; transition: flex-basis 200ms var(--panel-ease); }
.on > .panel-slot { flex-basis: var(--panel-w, 641px); }
/* 面板以固定宽挂在里面、不参与收缩 ⇒ 被容器裁切，形成「从一侧长出来」的观感 */
.panel-slot > .panel { flex: none; width: var(--panel-w, 641px); }
.on.is-dragging .panel-slot { transition: none; }        /* 拖动跟手，必须关过渡 */
```

- **内层 `display` 不能再跟着状态类硬切**：`.panel { display:none } / .on .panel { display:flex }` 会让
  摘类的瞬间元素就消失，宽度过渡根本没机会跑 → 内层必须**常驻显示**，可见性完全交给容器宽度 + `overflow`。
- **JS 侧**：收起不再依赖 `animationend`，摘掉状态类后由过渡自然收拢；
  原来的 `is-closing` 状态类**降级为纯 JS 防抖标记**（或直接换成变量），并在定时器到期后再 `syncLayout()`。
- **边距/描边一并过渡**：若同一元素还带 1px 描边，把 `border-width` 也放进 transition、
  收起态写 `border-width: 0`（见 PLAYBOOK P1.5 的 border-box 陷阱）。
- **验收口径**：页内 rAF 一次性采样（`[t, flexBasis, slotW, 邻居W]`），确认曲线是**渐变**而非跳变，且邻居同步反向变化。
  r70 实测：展开 `0→220→383→490→555→616→636→641`（≈230ms），收起 `641→421→258→150→85→47→25→12→5→2→0`（≈208ms）。
