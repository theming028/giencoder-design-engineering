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

### P3.11 settings（设置页）r85 新增 / r86 四条 / r87 四条 / r88 两条 + 「已归档任务」页签 / r89 三条 / r90 三条 / r91 三条 / **r92 两条**：导航 + 内容（节点 1389:18609 / 1389:18725 / **1393:18344**）

> 块：`<style id="r88-set-css">` + `<script id="r88-set-js">`，落地脚本 `mg-work/r88/apply88.py`
> （`PRIOR` 同时摘 r85/r86/r87/r88 **四代**块 ⇒ 自愈）。更早：r87 = `apply87.py`，r86 = `apply86.py`，r85 = `apply85.py`。
> ⚠ **r89 / r90 / r91 / r92（②③）都是 r88 的就地返工**（r88 未提交 ⇒ 不另起代数，直接改 `apply88.py`）。
> 宿主：`aside > div[class*="overflow-y-auto"]` 插导航、`main > div` 插内容；原 React 节点 `data-set-hidden` 隐藏。
> 轮次属性仍是 `data-r85-set`（DOM 类名与挂载点未变，历代只换 CSS/JS 块）。
> ⚠ r87 第 1 条（全局界面字号）是**跨全站的机制**，不属本页专有 ⇒ 见 **P3.11b**；r87 第 2 条 select 全站 ⇒ **P3.11c**。
> ⚠ **每次改本页都要同时跑 `mg-work/r88/apply88b-fontsize.py`**（字号机制层，块 id 仍为 `r87-ui-css/r87-ui-js`）。

**坐标系（写探针必看）**：`.r85-page-host { width:860px; margin:12px auto 0; padding:0 10px }`，
**内容盒左缘 = host + 10**；与设计稿同原点的元素是 **`.r85-page`（840 宽）**，探针基准用它，别用 host。

| 项 | 值 |
|---|---|
| **aside（r86 改）** | ★ {宽度固定 **256px**（`!important` 压内联 style）+ **禁拖拽**}；把手 = 外壳的 `[role="separator"][aria-label="调整菜单宽度"]`（6px）⇒ `display:none` + 捕获阶段拦 `mousedown/pointerdown`。⚠ aside 是**外壳 React 渲染**的，源码里没有 `<aside>` |
| 导航 | ~~`.r85-nav-host` 232×268~~ ⇒ ★ **r90 改：宿主宽 `auto`（撑满内容盒 = **244**）、`margin:0`**（原 `width:232px; margin:0 auto` 在 244 里居中 ⇒ 左 6 / 右 18）；`.r85-nav` 同步 `width:100%`。**基准 = 基础工作台 `pages/base.html`**：`aside` 256 + 子滚动容器尾风类 `pr-3`（右内距 12、左 0）⇒ 会话项 `relL 0 / relR 12`。设置页改后**逐像素一致**。<br>`.r85-navi` 244×36 r8，图标 16×16 @(12,10)；~~常显底 `--color-fill-1`~~ ⇒ ★ **r91 ② 改为 `background: none`（默认无底）**，选中底 `#ECEEF2` + 图标 `--color-primary-6`；分组标题 `.r85-gt` y=52 / 208 |
| **导航 hover（r88 改 / r91 扩）** | `.r85-navi:hover` 与 `[aria-current='true']` **共用** `--r88-navi-active`（`:root{--r88-navi-active:#ECEEF2}`；暗色 `[giencoder-theme=dark]` → `#2E323A`）。★ **r91 ①：返回钮 `.r85-back:hover` 也接进同一变量**（原为 `--color-fill-2` #F2F2F2）⇒ 使用面 3 处：菜单 hover / 菜单选中 / 返回钮 hover。⚠ 该 hex **不在 DS 色板**；暗色选择器是 `body[giencoder-theme=dark],[giencoder-theme=dark]`（**不是** `[data-giencoder-theme]`） |
| **★ 默认底（r91 ②）** | `.r85-navi` 基类 `background: none`。⚠ 靠**特异性**保证 hover / 选中不被盖掉：基类 0,1,0 < `:hover` / `[aria-current='true']` 的 **0,2,0**。<br>实测 aside 自身底色 = **`#F4F5F6`**（`rgb(244,245,246)`）⇒ 「无底」的判据 = **取到的像素等于 aside 底色**。 |
| **导航选中文字（r87 新增）** | `.r85-navi[aria-current='true'] > span{color:var(--color-primary-6); font-weight:500}`（原为 `--color-text-1` / 400）。实测 `rgb(55,112,247)` / `500`；未选中 `rgb(31,31,31)` / `400` |
| 内容 | `.r85-title` 28 高（`--font-size-title-2` 20px / 500）；卡片 margin-top 16（首张 24），`padding:20px` r8 |
| **卡片圆角 / 描边** | ★ **内描边必须 `outline:1px solid var(--color-border-1); outline-offset:-1px`**（设计稿内描边，不吃内容盒）。写 `border` ⇒ 行宽 798、卡片高 +2、整列推低 2–3px。<br>★ **圆角走共用变量 `:root{--r88-card-radius:8px}`**（r89 提取）：`.r85-card` / `.r88-arch-list` / `.r88-arch-empty` 三处引用 ⇒ 改档位只动一行。（r89 前列表卡与空态是 6px） |
| 卡片高 | 首 230 / 中 **448**（`is-mid`：底内距 16 而非 20）/ 末 156；页高 918（设计 919） |
| 行 | `.r85-row` 800×42 @x20；`.r85-ic` 40×40 r8 底 **`--color-fill-3`（r86 改，原 fill-2）**；`.r85-tx` margin-left 12（**末张卡片 `is-tail` = 16**）；行距 32 |
| **行分割线（r86 改）** | `.r85-row + .r85-row::before` `top:-16` 用 **`--color-border-2`(#E5E5E5)**（原 `--color-fill-2` #F2F2F2；两者同色阶，用 border 语义更准）。实测 8 条全 `rgb(229,229,229)` |
| 文本 | `.r85-t` 14px/22 `--color-text-1`；`.r85-d` 12px/16 `--color-text-3` |
| **`.r85-ctl`（r86 改）** | `gap:8px`；**select 一律用内联的 DS `.giencoder-select*` 全套**（r85 手搓的 `.r85-sel`/`.r85-menu` 已删净）；`.r85-cb` 额外 `margin-right:4px`（设计稿复选框→按钮间距 12）；右对齐 |
| **DS select 几何（r87 改）** | 高 32；宽度 **自适应**（r86 的 `padding-right:8px` 适配层 + JS 写死 `wrap.style.width` **均已撤销**）。**实测自然宽 = 102 / 150.9 / 102 / 74**（r86 按设计稿写死的是 98 / 154 / 98 / 70，差 +4 / −3.1 / +4 / +4）。右对齐判据：`ctlRight === rowRight === 1330`。圆角 **8px**、**无 ring** |
| **`.r85-btn`（r87 改）** | 外观声明**整段删除**，改挂 DS Button：`giencoder-btn giencoder-btn-secondary giencoder-btn-size-default` ⇒ 实测 **104×32**、radius 8px；`is-danger`（退出登录）= 同档 + `color: var(--color-danger)`（**DS 无「带边框 + 危险色文字」组合** ⇒ 走适配层）。⚠ 该类由 JS 动态创建 |
| **`.r85-seg`（r87 改）** | `gap:8px`；按钮改挂 `giencoder-btn giencoder-btn-secondary giencoder-btn-size-large` ⇒ **128×40**、radius 8px；选中项适配层 `border:2px dashed var(--color-border-3)`（**DS 的 `-dashed` 是 primary 蓝虚线「添加」语义，不是这个灰虚线选中框**）。⚠ 该类由 JS 动态创建 |
| `.r85-sw` | 覆盖 DS switch：40×24 r12，开 `--color-success` / 关 `#6B6B6B`，手柄 20×20（开 left18 / 关 left2） |
| **`.r85-slider`（r87 改 / r88 交互重做）** | 252×36。轨道 `.r85-sl-track` rel(6,6) 240×1；已选 `.r85-sl-done` rel(6,6) 宽 48；**6 档 `stops=[6,54,102,150,198,246]`、`FS_LEVELS=[13,14,16,18,20,24]`**（默认 idx=1）；刻度 `.r85-sl-tick` 1×8 @rel y2 **挂 `.r85-slider`（不是 track）**，`is-on` 深色；拇指 4×12 @rel y0 `margin-left:-2px`；标签「小/默认/大」锚档 0/1/5（中心 rel 6/54/246）。**点击/拖拽 → `fsApply(idx,true)` 写 `localStorage['gi-ui-fs']` + 设 `<html>` 内联 `--ui-fs` + toast** |
| **★ 滑块交互（r88 重做）** | 根因：r87 的 `click` **挂在 1px 高的 `.r85-sl-track`** 上且**根本没有拖拽实现**。r88 改为：命中层 = 整块 `.r85-slider`(252×36) + `.r85-slider > *{pointer-events:none}`；`pointerdown/move/up/cancel` + `setPointerCapture` + `touch-action:none`；**★ move/up 挂 `window`**（挂元素时 capture 失败会让 `dragging` 永卡 `true`）+ `window` `blur` 兜底；拖动中只改视觉、**松手才落盘 + toast 一次**；键盘可达（`role=slider` / ↑↓←→·Home·End / `:focus-visible` 光圈） |

**禁区**：① 别把刻度挂 `track` 上（`top` 会叠加 track 的 6px）；② 内容盒宽靠 `padding:0 10px` 得来（host 860 → 内容 840）；
③ ~~其余菜单（模型/连接器/已归档任务）无设计稿 ⇒ `.r85-empty` 空态占位~~ ⇒ **r88 起「已归档任务」有设计稿**，已落地为 `buildArchPage()`（见 **P3.11d**）；模型/连接器仍是空态；
④ **别手搓新控件** —— 页面里早就内联了 DS 全套组件 CSS，先 grep 类名（见 PLAYBOOK P3.19 ②）；
⑤ **别把 `--ui-fs` / `--ui-fs-ratio` 写到 `:root` 以外**（会盖掉 `<html>` 上的内联值，字号开关失效）；
⑥ **DS select 的「可选子部件」必须判空**（`noClear` 时清空钮不存在 ⇒ `null.addEventListener` ⇒ 整页白屏，见 PLAYBOOK P3.21 ①）；
⑦ ★ **按钮一律挂 DS Button 类名，别自绘**（邵先生 r90 ② 定为**全局强制性要求**）：本页正解 = `giencoder-btn` + 变体（`-secondary` 中性描边 / `-size-small|large`）+ **适配层只补几何**（尺寸 / 内距 / DS 没有的语义色）。⚠ 动手前先看 **r73 全局块** `giencoder-btn:not(.giencoder-btn-size-small){border-radius:8px}` —— 「圆角」已有全站口径，**别再**按设计稿压 6px；
⑧ ★ **1px 描边的图标，中心线必须落 `.5`**（整数中心线会摊成两列 50% 灰 ⇒ 又细又虚，见 PLAYBOOK P3.22）。

### P3.11b ★★★ 全局界面字号机制（r87 新增 · **全站生效**，9 页各一份）

> 落地脚本：**每代一份副本**（`mg-work/r87/apply87b-fontsize.py` → `mg-work/r88/apply88b-fontsize.py` …），
> 块 id **刻意恒为 `r87-ui-css` / `r87-ui-js`**（常驻机制，**不随补丁代数改名**；插在 `</head>` 前）。
> 详细坑见 **PLAYBOOK P3.20**（增量：P3.21 ④「带 token 字号的规则里别写裸 `height`」）。用户答复采纳「变量等比缩放」（原话「我不太懂，使用你推荐的方式」）。

**★ 关键事实（写任何字号相关代码前必读）**

| 通道 | 事实 |
|---|---|
| 外壳（React 顶栏/侧栏） | 用**尾风 px 类**（`.text-sm{font-size:14px;line-height:20px}`）——**不是 rem** ⇒ `html{font-size}` 杠杆**不成立** |
| 页面自绘 + DS 组件 | 走 `var(--font-size-*)`，token 在 `:root` 里是**字面 px** |
| 全站文字类 | 只有 6 种：`text-xs`12/16、`text-sm`14/20、`text-lg`18/28、`text-2xl`24/32、`text-[13px]`、`text-[11px]` |

**机制**

```
:root{ --ui-fs:14; --ui-fs-ratio:calc(var(--ui-fs) / 14); }
      --font-size-{body,body-1,body-2,body-3,caption,title-1,title-2,title-3,display-1,display-2,display-3}
        : calc(<原px> * var(--ui-fs-ratio));          /* 11 个 token 全部派生 */
body .text-xs/.text-sm/.text-lg/.text-2xl/.text-\[13px\]/.text-\[11px\]{…}   /* 外壳 6 条逐条覆盖 */
body .giencoder-btn-size-{mini,small,default,large}{height:calc(Npx * R)}
body .giencoder-input-wrapper{[data-size=…]}{height:calc(Npx * R)}
body .giencoder-select-view{min-height:calc(32px * R)}
body .r85-{navi,back,btn,slider}{…} / body .r85-seg > button{height:calc(40px * R)} / body .r85-sl-lbls{…}
```

- **唯一旋钮 = `--ui-fs`**（px 无单位，14 = 默认档，可选 13/14/16/18/20/24）。
- 档位存 `localStorage['gi-ui-fs']`，`<head>` 引导脚本**首帧前**写成 `<html>` 内联 `style.setProperty` ⇒ 无闪烁。
- 覆盖规则**一律加 `body` 前缀** ⇒ 特异性高于任何后置普通规则，**与脚本执行顺序无关**。
- **图标盒与布局盒刻意不跟随**（本设置只缩放文字相关尺寸）。
- **行高/高度只在「自身声明了 token 字号」的规则内派生**（`scale_block` 判据 `var(--font-size-`），
  `height:Npx` → 成对 `height:calc(Npx*R);min-height:calc(Npx*R)`（可逆幂等）。
- ⚠ ★★ **与任意值工具类的特异性冲突（r93 需求 1 踩过，根因）**：`body .text-xs{…line-height…}` 特异性 **(0,1,1)**，
  会压掉 `.leading-\[32px\]` 的 **(0,1,0)**（aside 分组标题 `text-xs leading-[32px]` 行高 32→16）。
  机制层两条必备写法规避：① size 类的行高加 `:not([class*="leading-"])` **让位**；
  ② 对要支持的 `leading-[Npx]` 补一条**同特异性**派生规则、**写在 text-\* 之后**（`--ui-fs-ratio` 派生）。
  现 `apply88b-fontsize.py` 的 `LEADING_DERIVE = [19, 22, 32]` 三档。详见 PLAYBOOK P3.24 ①。
- ⚠ **带 `var(--font-size-*)` 的规则里不得声明裸 `height:Npx`**（会被 `scale_block` 一并按比例派生）⇒
  「尺寸」与「字号」拆成**两条规则**。例外：规则体不含 `var(--font-size-` 的（如 `.r93-todocard`）可安全写 height。

**实测（6 档等比断言，k = px/14）**

| 档 | 导航高(36k) | select 高(32k) | 分段高(40k) | 行高 | 页卡片高 |
|---|---|---|---|---|---|
| 13 | 33 | 30 | 38 | 42 | 230 |
| **14（默认）** | **36** | **32** | **40** | **42** | **230** |
| 16 | 41 | 37 | 46 | 43 | 234 |
| 18 | 46 | 41 | 51 | 49 | 250 |
| 20 | 51 | 46 | 57 | 54 | 266 |
| 24 | 62 | 55 | 69 | 65 | 299 |

**默认档零回归判据**：`.r85-page` = `[510,85,840,918]`、卡片高 `[230,448,156]`（与 r85/r86 **完全一致**）；
`.r85-page` 元素截图前后**像素 diff 仅 7 处**（全在右侧控件列）。

### P3.11c ★★ DS Select 全站固定事实（r87 定稿 · **有页面级适配层，改前先 grep**）

> 落地脚本 `mg-work/r87/apply87a-select.py`（`--revert` / `--dry`）。
> 「全站」= **三份 DS 源 + 9 页 + 契约 json**（三份源清单见 PLAYBOOK P3.20 ②）。

**r87 三条改动（全站）**

| 项 | 改前 | 改后 |
|---|---|---|
| `--select-ring` | `.giencoder-select-view` 内声明的**局部变量**（非 token），用于「外扩 1px 同色 spread 补齐表面」 | **删净**（变量 + `, 0 0 0 1px var(--select-ring)` 项）；**保留** 极淡 `0 1px 2px rgba(15,23,42,0.04)` |
| 圆角 | 4px（`--border-radius-medium`） | **8px**（`--border-radius-large`） |
| 宽度 | `.giencoder-select{width:100%}`（撑满容器） | `width:auto; max-width:100%`（`inline-flex` 按内容收缩）；容器要撑满时外部给 width |

**⚠ 5 处页面级适配规则也写死了圆角（r87 已一并抬到 8px，改 DS 时要连它们一起看）**

| 页 | 选择器 | 备注 |
|---|---|---|
| kanban | `.kb-boardhead .giencoder-select[data-size="small"] .giencoder-select-view` | 28 高的小号 |
| kanban | `.kb-coop-sel .giencoder-select-view, .kb-coop-date .giencoder-input-wrapper` | ★ **与日期输入框共用一条规则**（邵先生 r87 拍板「输入框同改」） |
| kanban | `.kb-coop-pageopt .giencoder-select-view` | 分页器 |
| req-kanban | `.rq-bh-filters .giencoder-select[data-size="small"] .giencoder-select-view` | 28 高的小号 |
| task-detail / avatar | `.select-view-ghost`（**内联** `border-radius:32px`） | ★ **胶囊芯片，刻意保留 32px 不动**（「标准模式 / DeepSeek-V4-Pro」模型切换；仅同步去掉 ring） |

**其他固定事实**

- `.giencoder-select-popup` r8；`.giencoder-select-option` r4（不是触发框，别看错）。
- **`.giencoder-select` 类名被 task-detail / avatar 当通用 flex 容器复用**（包「添加」按钮、`td-skill-pop` 技能弹层）
  ⇒ 扫全站 select 时这 2 处是**假阳性**（无 `.giencoder-select-view` 子节点）。
- 弹层定位在 `gienx-templates/ui-controls.css`（只做 opacity/translate/scale 动效，**无圆角与 ring**），
  静态结构在 `components.css`；开合唯一开关 `.giencoder-popup-open`。
- 定宽容器里 `.giencoder-select-view` 带 `box-sizing:border-box; min-width:0; flex-wrap:nowrap`（防 suffix 箭头被挤出）。
- ★ **`.giencoder-select-view` 自带 `gap:8px`**（r88 查明）⇒ 往里加前缀槽/图标时，文字与图标会被额外撑开 8px
  （设计稿往往只留 6px）⇒ 用 `margin-right:-2px` 之类抵消。**给 DS 组件加子元素前先读它的 `gap`。**
- ⚠ 大字号档：kanban 定宽日期框 `.giencoder-input.kb-date-val` 会截断（24px 时溢出 137px）—— 既存问题。

---

### P3.11d ★★ 「已归档任务」页签（r88 新增 / r89 三条 / r90 三条 / r91 一条 · 设计稿 `1393:18344`）

> 落地 = `mg-work/r88/apply88.py` 的 `buildArchPage()` / `buildArchRow()` / `archFilter()` / `ctlArchSearch()` / `ctlArchProj()`。
> 路由：`buildPage()` 顶部 `if (tabId === 'archived') return buildArchPage();`。数据 `ARCH_ROWS`（7 行）+ `ARCH_FILTER_ALL` + `ARCH_SUB`。

**量测口径**：设计稿 `GET …/api/getScreenshot?…&targetNodeId=1393:18344&scale=2` ⇒ PNG **1680×1316 device px**
= 画板 **840×658 design px** ⇒ **scale 恒 2.0**（画板尺寸是整数，直接定死，**别用 2.011**）。
⚠ RGBA 未绘制处 `alpha=0` ⇒ 量测前先 `alpha_composite` 白底。

**几何（design px，原点 = `.r85-page` 内容区左上）**

| 区 | 值 |
|---|---|
| 头部 | 块高 **48**：标题 `20px/28` 500（★ **r89 按指令与 `.r85-title` 统一取 `--font-size-title-2`**；设计稿实测为 16px）+ 副标题 `12px/20`；块底与清空钮底对齐（`align-items:flex-start` + 钮 `align-self:flex-end`） |
| 清空钮 `.r88-arch-clear` | `x 732..840, y 12..48` = **108×36**；DS **`giencoder-btn giencoder-btn-size-large`** + 适配层「浅底危险」（`--color-danger-light-1` 底 / `--color-danger-6` 字）。<br>★ r90：**去掉** `border` / `border-radius`（圆角交给 r73 全局规则 ⇒ **8px**）；**内距取 11**（DS 基类自带 `border:1px solid transparent` 占 2px ⇒ 11+1+84+1+11 = **108** 精确） |
| 工具条 `.r88-arch-bar` | `y 80..112`，`gap:8`；搜索 `.r88-arch-search` `flex:1`（**632**）×32；下拉 `.r88-arch-proj` **定宽 200**×32 |
| 列表卡 `.r88-arch-list` | `y 132..658` = 840×**526** = `padding:4px 0` + 7×74；底 `--color-fill-1` + **内描边** `outline:1px solid var(--color-border-1); outline-offset:-1px`；★ 圆角 **`var(--r88-card-radius)`（r89 起 = 8px，与 `.r85-card` 共用；原 6px）** |
| 行 `.r88-arch-row` | `padding:15px 20px` ⇒ 高 **74**；分隔线 `.r88-arch-row + .r88-arch-row::before` `left/right:20px`（**inset 20/20**）、色 ★ **`--color-border-2`（`#E5E5E5`，r89 按「深一级」由 `--color-border-1` 改）** |
| 行内文字 | `.r88-arch-t` `14px/22` `--color-text-1`；`.r88-arch-m` `12px/18` + `margin-top:4`，色 `--color-neutral-7`；元信息串 `[icon 12×12]4[项目名]8[· 4×4 r50%]8[归档于]6[时间]` |
| **★ 行内图标 `.r88-arch-mic`（r89 修）** | 用 **`i_folder12`**（`viewBox="0 0 12 12"`，**12 网格 1:1**，坐标全取 x.5，标签**直角台阶**、中部横线 `y=5.5`）。<br>⚠ **别拿 16 网格的 `i_folder` 缩到 12px**：墨迹会扁成 8.6×6.5（设计 10.5×10）＋斜边糊掉＋1.125px 描边落非整数像素发虚。见 **PLAYBOOK P3.22** |
| **★ 下拉前缀图标（r90 重画）** | `.r88-sel-prefix` 里的 `i_folder` 重画为 **16 网格 1:1**：`M1.5 2.5h5v2h8v9h-13z` + `M1.5 7.5h13`（**描边中心线全落 `.5`**、直角台阶、`stroke-width:1`，渲染 16px）。<br>旧版三重错：墨迹 14×11（设计 13×12，扁）＋标签斜边 `l1.3 1.6` 在 16px 下留亮缝＋**中心线落整数坐标（x=2.3/12.9）⇒ 1px 描边摊成两列 50% 灰像素（又细又虚）**。<br>墨迹取 **14×12**（设计 13×12）：16 盒里要左右对称对齐像素必须偶数宽，1px 差不可辨 |
| 行尾按钮 `.r88-arch-act`（r90 改 DS 组件 / r91 改图标色） | 类名 = **`r88-arch-act giencoder-btn giencoder-btn-secondary giencoder-btn-icon giencoder-btn-size-small`**。默认 **28×28** 图标钮 → 行 hover/focus-within **52×32** 文字钮。`28+8+28` 右贴 **820**（=840−20）；`52 = 1+11+14×2+11+1`。<br>适配层**只补几何**：`body[data-r85-set] .r88-arch-act{width:28px;padding:0}` + hover/focus-within `{width:auto;min-height:32px;padding:0 11px}`。<br>★ **展开态只写 `min-height` 不写 `height`**（DS 给了 `height:28px`，而 CSS 里 min-height 优先于 height ⇒ 默认 28 / 展开 32 两全）；★ 该规则**故意不带 `body` 前缀**（低特异性）好让 `apply88b` 的 `body …` 版派生接管成 `calc(32px * ratio)`。<br>⚠ 其余全随 DS：圆角 **4px**（small 档；r73 全局规则只把**非 small** 档提到 8px）、描边 **`border-2`(#E5E5E5)**。<br>★ **r91 ③ 图标色**：`--color-text-1`(#1F1F1F) → **`--color-text-2`(#4E4E4E)**，写法是 **`.r88-arch-act > svg { color: var(--color-text-2) }`** —— ★★ **刻意只落在 `> svg` 上**：展开态 svg 被 `display:none`、文字 `span` 仍继承按钮的 `text-1` ⇒ **图标变浅、hover 文字保持设计稿值**（这是本轮的关键技巧：**同一按钮里图标与文字要用不同深浅时，把 color 下移到 svg**）。<br>⚠ 设计稿图标逐像素实测 **`#6B6B6B`(=`--color-neutral-7`)**，比 `text-2` 再浅一档；要精确贴稿就换成 `--color-neutral-7` |
| 空态 `.r88-arch-empty` | ★ 用 **`padding:48px 0` 撑高**，**禁写 `height`**（带 token 字号的规则里裸 `height` 会被 `apply88b` 派生成 `calc(N×ratio)`）；圆角同 `--r88-card-radius` |

⚠ **既存问题（r89 实测，非该轮引入）**：`--ui-fs:24` 极限档下「全部项目」下拉内文需 218px > 定宽 200px ⇒ `.r88-arch-bar` 溢出 18px（默认档零溢出）。

**色值 → token（**零新增字面 hex**）**：★ **分隔线 r89 起用 `--color-border-2`（`#E5E5E5`）** —— 设计稿实测是 `#F2F2F2`，按邵先生「深一级」指令加深（与 r86 ② 同款；也顺带与本页 `.r85-row` 的分隔线同款）；
`#E5E5E5`（搜索/下拉描边，DS 默认档）→`--color-border-2`
｜`#1F1F1F`→`--color-text-1`｜`#868686`→`--color-text-3`｜**`#6B6B6B`→`--color-neutral-7`**（DS 无同值文字 token；★ **r91 起行尾按钮的「图标」用 `--color-text-2`(#4E4E4E)** —— 那是 `text-1` 的「文字阶浅一级」；按钮**文字**仍是 `text-1`；**行内元信息**仍用 neutral-7）
｜`#FFECE8`/`#F53F3F`→`--color-danger-light-1`/`--color-danger-6`｜卡底/卡描边沿用 r85 的 `--color-fill-1`/`--color-border-1`。

**圆角（r90 起分三路）**：① **卡片类** → `--r88-card-radius`（8px，r89 起与 `.r85-card` 共用）；
② **DS 按钮** → 组件自己的档位（r73 全局规则：**非 small 档 8px / small 档 4px**）⇒ 清空钮 8px、行尾钮 4px；
③ **其它控件**（搜索框 / 项目下拉）→ **6px**（设计稿实测 6~7px，DS 无 7px 档）。

**取证判据**：关键几何**逐项 0 差**（清空钮 732/12/108×36、搜索 632、下拉 640/200、卡片 132/840×526、行高 74、
分隔线 inset 20、默认钮组 756/792/820、hover 钮 52×32 右缘 820、hover 钮文字与页标题墨迹**完全一致**）；
★ r90 起「改了没改错」的判据 = **rNN 态 vs rNN+1 态同态元素截图逐行分组 diff**（脚本 `ev/diffgrp.py`）：
r88→r89 = 3.648%（16 组）、r89→r90 = 1.562%（10 组）、**r90→r91 = 0.554%（6 组 = 6 个非 hover 行 × 2 个图标），每组都能指到具体某条改动**。
» **r90→r91 的 6 组全落在 `y167..179  x764-774, 800-811`**（= 16×16 图标在 28×28 钮内的居中区），
且**被 hover 的那一行反而不在差异里**（展开态 svg 已 `display:none`）⇒ 反证「color 只落在 `> svg` 上」写法正确。
★ **aside 的改动不在 `.r88-arch` 元素截图范围内** ⇒ 这类改动必须另截 `aside` 元素图 + 逐像素取色（`ev/nav91.py`）。
整页像素差 **3.16%（r88）→ 3.29%（r90）→ 3.24%（r91）** 且**全部来自字形**（结构件无整块差异）⇒ **别用整页像素差当验收判据**。
⚠ 设计稿第 1 行文字整体右移 12px 是**设计稿笔误**（其余 6 行都是 20px 左内距，该列最低亮度恒 = 底色）⇒ 按统一 20px 还原。

### P3.11e ★ 外壳顶栏 `header` 装饰背景图（r92 新增 · **落基础工作台 5 页**）

> 块：`<style id="r92-hdr-css">`，落地脚本 `mg-work/r92/apply92.py`。
> 素材：`assets/images/bg-img-1.png`（邵先生提供）＝ **1580×134**、平底 `#F6F8FA`（占宽 67.5%）
> + 右侧 `#DDE3EB` 的 **4px 方点 / 8px 点距**密度递增点阵（起点 x=1067）。**不透明**。

```css
header[class*="h-12"] {                      /* ⚠ 不能用裸 header —— avatar 有 5 个、task-detail 有 4 个 <header> */
  background-image: url("../assets/images/bg-img-1.png");
  background-repeat: no-repeat;
  background-position: right center;         /* 不写 background-size = auto = 素材原尺寸 */
}
```

| 事实 | 值 |
|---|---|
| 落哪些页 | **base / settings / avatar / skills / automation**（基础工作台组）。路由判据 = 每页 bundle 里的 `DEV_PAGES`（`dev/kanban/req-kanban/task-detail` 属研发工作台） |
| 为什么不落研发 4 页 | 那 4 页顶栏底色是 `#E5EDF5`，素材平底是不透明 `#F6F8FA` ⇒ 会整块盖掉蓝调 |
| 顶栏自身颜色 | `bg-[#F4F5F6]`（基础组）/ `bg-[#E5EDF5]`（研发组），React 条件类 |
| 素材平底 vs 顶栏底色 | `#F6F8FA` vs `#F4F5F6` ⇒ **Δ=(2,3,4)** ⇒ 视口宽于 1580 时图片左缘留接缝（1920 视口实测 **x=340**） |
| 竖直裁切 | 素材 134 > 顶栏 48 ⇒ 居中取中段，顶/底各留 **2px 半格 DOT**（1x 不可辨） |
| 实测点色 | 顶栏截图右缘最暗 `(221,227,235)` = 素材点色，**逐通道相等** |

### P3.11f 设置页 r92 两条（就地改 `apply88.py`）

| # | 需求 | 落地 | 实测 |
|---|---|---|---|
| ② | 「返回」钮图标 + 文字**深一级** | `.r85-back`：`color: #6B6B6B`（gray-**7** / `--color-neutral-7`）→ **`var(--color-text-2)`**（gray-**8** `#4E4E4E`）。图标 `fill="currentColor"`、文案 `<span>` 继承 ⇒ 一处改两件同变 | 改前 `rgb(107,107,107)` → 改后 `rgb(78,78,78)`（`back` / `> svg` / `> span` **三处相等**） |
| ③ | `.r85-gt` 左间距 **12px** | `margin: 0 2px 8px` → `margin: 0 2px 8px 12px`（只改左值） | `margin-left` 2px → **12px**；标题视口 x 14 → **24**（与 `.r85-navi` 图标左缘 x=24 对齐，菜单项 `padding: 0 12px`） |

★ ② 顺带消掉本页**最后一处字面 hex**（`#6B6B6B`）⇒ 全页已零硬编码色值。

### P3.11g ★ 会话详情（r93 新增 / r94 五条 / **r95 两条「右侧撑满」** / **r96 五条** / **r97 四条「宽度基准」** / **r98 三条「内容区 15px / rateline 下 48px / 差分卡还原」** · 设计稿 `1393:18748`）—— **④ 后落在独立页 `pages/conversation.html`**

> 落地脚本 `mg-work/r93/apply93.py`（`--revert`）；验收档案 `mg-work/r93/acceptance.md`（含 ⑥ ④ 章）。
> 详细坑见 **PLAYBOOK P3.24**（变体叠加 / 字号三角验证 / 暗色 / **⑦ 独立页 + 纯 CSS 复用外壳真组件**）。
> ★ **④ 之后主载体 = `pages/conversation.html`（独立页，604806 字符）**：base.html 只留「点 aside 会话项 ⇒ `location.href='conversation.html'`」的 `r93-nav-js`；
> 根级判据由 `[data-r93-conv='1']` 改为 **`<html data-r93-page="conversation">`**；10 页 `ROUTE` 表各 +1 条 `'/conversation'`。**内容本体（25 块 + composer）两页通用。**

**挂载方式（关键：`<main>` 源码里 0 次 = React 运行时渲染）**

- **不动 React 源** ⇒ 只在 `mainInner`（`main > div.relative.flex.h-full.min-w-0.flex-col.overflow-hidden`）尾部追加 `.r93-conv-host`；
- ★ **④ 后的页面判据 = 根级 `<html data-r93-page="conversation">`**（页面级 CSS 全部挂 `html[data-r93-page='conversation'] …`）；
  ③ 时期那套「内层 `data-r93-conv='1'` 开关 + `> *:not(.r93-conv-host){display:none!important}` 藏空态」**已被页面级规则取代**（现由 hero 贴底 + 问候语/页脚 `display:none` 达成，见下「④ composer」）；
- **宿主挂载**（在 `conversation.html` 内）：`MutationObserver` + `DOMContentLoaded` + `setTimeout(800 / 1500)` 三重兜底，补回被 React 冲掉的宿主；
- **点击分流**（`document` **捕获阶段**，`closest('aside button')`）：`min-w-0 + flex-1`（会话项，13 个）⇒ 滚动置顶；`rounded-md + py-0`（分组标题，4 个）⇒ **只折叠、不切换**。
  源码里 `base.html` 侧只剩 `r93-nav-js`：同款捕获监听，命中会话项即 `location.href='conversation.html'`。

**几何账（实机 1440 视口 / main 内宽 1162）**

| 项 | 值 |
|---|---|
| wrap | **`width:calc(50% + 10px); min-width:860px`**（★ r97 ③；r93 曾是写死 840，r95 改 `50%`，r97 补 both-edges 的 +10 基准差） |
| 页头条 `.r93-bar` | 高 **44**，`border-bottom: 1px solid #EBEBED`；分段控件 `left:8 top:8` |
| 用户气泡 | **728** 宽（右对齐）+ 阴影 `#D0D7EA` |
| 卡 | **822** 宽（`margin-left:18`）；产物卡 414×56 |
| 内容总高（设计真机） | **4106px** = 实机实测 **4106px** ✅ |

**25 个块 + composer**：页头 44 / 用户气泡 / 助手头 / 上下文注入卡 **150** / 深度思考卡 **200** / AI 文本 ×2 / Bash 卡 **160** / 网页搜索卡 **184** / 需求采访卡 **208** / 更新任务清单卡 **220** / 文件写入卡 **244** / SKILL 卡 **64** / Tool call 卡 **132** / 重试卡 **64** / 调用 5 工具 / 压缩上下文 / 上下文已压缩 / 搜索资料 / 告警 ×2（44）/ 未知 surface 卡 **84** / 模型已切换 / 改动汇总卡 **300** / 任务产物 **230** / Token 速率行 24 + composer（状态条 + 4 张 agent 卡 + 输入框）。

**字号体系（`ui-component` 不带 font-size，三角验证得出）**

| 用途 | fs/lh | 工具类 |
|---|---|---|
| 折叠头标题 / 气泡正文 / 需求采访 | 14 / 22 | `.r93-t14` `.r93-t14m` `.r93-t14b` |
| 折叠头 meta | 12 / 22 | `.r93-t12l` |
| 卡内正文 / 代码 | 12 / 20 | `.r93-t12c` |
| 上下文注入卡正文 / Bash 卡代码 | 12 / 16 | `.r93-t12s` |
| 居中提示卡片下说明行 | 12 / 24 | `.r93-t12h` |
| 深度思考正文 | 12 / 22 | `.r93-t12l` |

**色**：设计稿实测色全进页面 `:root` 的 `--r93-*`（`--r93-line #EBEBED` / `--r93-card #F5F6F7` / `--r93-edge #ECEEF2` / `--r93-bubble #E5EDFE` / `--r93-tag-* #FFF3E8·#FDDDC3·#F77234` / `--r93-warn-* #FFF7E8·#FFE4BA·#D25F00` / `--r93-ok #30953B` / `--r93-a1-bd #E2D3F9` / `--r93-hov-*` …），**并补一整份 `[giencoder-theme='dark']` 档**；白底一律 `var(--color-bg-2)`。
分段控件复用 DS：`div.giencoder-radio-group.giencoder-radio-group-button > span.giencoder-radio-button-slider + label.giencoder-radio-button(+ -checked) > input.giencoder-radio-input + span.giencoder-radio-button-text`，并在 `.r93-seg` 内把 `height:32px` 压回 **24**。

**④ 底部 composer = 全要素复用外壳真实组件（纯 CSS、零复制、零重绘）**

- **真输入卡选择器**（邵先生点名的那个）：`div.relative.flex.w-full.flex-col.rounded-[16px].border.bg-white.p-3.transition-colors`，
  宿主外壳 = `main > div(hero 1162×760) > div.mt-8 > div.flex.w-[800px].flex-col.rounded-[16px].bg-[var(--color-fill-1)].px-3.py-3`（**860×214**）；
- **保留**：宿主 `.r93-sb`（状态条「执行 第 2/5 个待办」）+ 4 张 `.r93-agent` 卡；**删掉**宿主内自绘的 `.r93-input` 整段（textarea + 工具条 + 发送钮）；
- **5 条同页选择器改视觉顺序**：宿主 `order:-1` 前置 / hero `justify-content:flex-end` 贴底 / 问候语（`.pointer-events-none`）+ 页脚（`.pb-6`）`display:none` / `div.mt-8` `margin-top:0`
  ⇒ 实测最终顺序 = 内容 → Token 速率 → 滚动到底部 → 状态条 → agent 卡行 → **真输入卡** → 工作目录/权限行（= 设计稿）；
- **实测 rect（1440）**：host 1162×628（`order:-1`）/ hero 1162×214 / outer 860×214 / card **836×154** / `doc 900 = win 900`；
- **★ 下拉翻向**：`.giencoder-select-popup` 与 `[aria-label='权限选择']` 写 `top:auto!important; bottom:calc(100% + 4px)!important`
  （真组件默认**向下**弹，被 `overflow:hidden` 的 main 底部裁）；修后 4 个 popup 全部完整可见（标准模式 200×80 / 模型 194×207 / 工作目录 194×109 / 权限 280×126）；
- `.r93-cp` 只留 `margin-top:12px`（灰壳交给真组件）；`.r93-tbsticky` 保持 `bottom:44px`（实测按钮底 541 / 状态条顶 553 / 间距 12）。

**⑤ r94 五条微调（同日第四轮 · 就地返工 `apply93.py`）**

| # | 对象 | 现值 |
|---|---|---|
| ① | `.r93-seg-cap` | `left:50%; transform:translateX(-50%)` ⇒ 在 `.r93-bar` 内**精确居中**（实测 `capCenterDelta=0`；原 `left:396px` 是按设计稿 1168 面板量的固定值） |
| ② | `.r93-wrap` | `width:50%; min-width:860px; box-sizing:border-box; padding:32px 10px 24px`（1440 下生效 **860**；**内容盒仍 840** ⇒ 内容横向零位移）⚠ **r95 已改**：padding 只留纵向 `32px 0 24px` + 内容块全部流式 ⇒ 见下方 ⑥ |
| ③ | 真 composer 的 outer | 去灰壳（`background:none / padding:0 / border-radius:0`）+ 隐藏底排（`> div:not(:has(textarea))`）⇒ **只留输入卡本体**（输入卡随之 836 → **860** 宽） |
| ④ | 波点 | `main.dot-bg{background-image:none}` + `main.dot-bg::before{display:none}`（点阵真源＝`main`，**不在 `div.mt-8` 内**：实测该容器只有 1 个子元素） |
| ⑤ | `.r93-card--ctx` | `min-height:150px; max-height:240px; overflow-y:auto; overflow-x:hidden`；`.r93-vsb`（设计稿的假滚动条）**CSS 规则 + 5 处 DOM 全删** |

**⑥ r95 两条「右侧撑满」（同日第五轮 · 就地返工 `apply93.py`）**

动手前先量三组元素的右边界（原来**打架**）：内容块 **1265** / 底部 `.r93-sb`·`.r93-cp` **1270** / composer 输入卡 **1280**。
根因 = ① `.r93-scroll` 的**滚动条占宽**让内容列偏左 5px；② r94 给 wrap 加的 10px 内距。

| 类别 | 现值（r95 后） |
|---|---|
| 内容列同轴 | `.r93-scroll` 加 **`scrollbar-gutter: stable both-edges`**；`.r93-wrap` padding → **`32px 0 24px`** |
| 卡片类容器 | `.r93-card` / `.r93-todocard` → **`width: calc(100% - 18px)`**（**左缩进保留、右侧撑满**） |
| 整行块 | `.r93-card--full` / `.r93-note` / `.r93-ndesc` / `.r93-alert` / `.r93-diff` / `.r93-arts` → **`width:100%`** |
| 产物卡 | `.r93-artcard` `414px` → **`calc(50% - 6px)`**（两列等分撑满） |
| 底部列 | `.r93-bottom` → `width:50%; min-width:860px; box-sizing:border-box; margin:0 auto`；子项 → `width:100%; margin:0` |
| 对话框外壳 | `… > div.mt-8 > div` 补 `width:50% !important; min-width:860px !important` |

**刻意未动**：`.r93-bub`（728 气泡 —— 右对齐 ⇒ 自动跟随新右边界；设计稿语义本就是「不满宽」）、
`.r93-agent`（4 张 agent 卡按内容宽左对齐，属于设计稿固定排版、**不是「容器」**）。

**实测（`ev/p95b.js`，1440 / 1920 双档）**：`.r93-wrap` / `.r93-bottom` / `.r93-sb` / `.r93-cp` / composer `outer` / 输入卡
**均 `[420,860]`（1920 为 `[660,860]`）⇒ 右边界 1280**；`ctx`·`todocard` `[438,842]`、`bub` `[552,728]`、
`alert`·`diff`·`arts`·`note` `[420,860]` ⇒ **全部 Δ=0**；sticky 药丸中心 **850** = 内容列中心；`doc/win` 无双向溢出。

**⑦ r97 四条（同日第七轮 · 就地返工 `apply93.py`）**

| # | 需求 | 现值 |
|---|---|---|
| ① | 卡内字号**统一 13px** | 新增 **`.r93-card.r93-card, .r93-card.r93-card * { font-size: var(--font-size-body-2) }`**。r96 只把「卡内**裸文本**」的默认档调成 13px，卡内仍混着 12px（`.r93-t12*` / `.r93-pre` / `.r93-wlink` / `.r93-clink` / `.r93-diffstar`）与 14px（`.r93-t14`）⇒ 实测卡内 **42 处文本全落 13px**。**类名写两遍**是为了抬到 (0,2,0)（`*` 不贡献特异性，见 PLAYBOOK P3.28④） |
| ② | 「滚动到底部」= 胶囊 + 文字/图标同色 | `.r93-tobottom`：`border-radius:8px` → **`999px`**；前景色 → **`--r93-ioc2`**（#6B6B6B）；新增 `.r93-tobottom .r93-t14 { color: inherit }` ⇒ 实测图标与文案同为 **rgb(107,107,107)** |
| ③ | 对话框两端短一截 / 模块等宽 | ★ **三者宽度基准统一**：`.r93-scroll::-webkit-scrollbar{width:10px}`（钉死）+ **`.r93-wrap{width:calc(50% + 10px)}`** + hero `padding:0 0 8px 0!important`（清 `px-6`）⇒ wrap / `.r93-bottom` / composer **恒等 `max(50%×main 内宽, 860px)`**。**顺带** `.r93-agent` `flex:none` → **`flex:1 1 auto; min-width:0`**（设计稿该行第 4 张本就顶到右缘） |
| ④ | 输入卡**下方**那行小灰字 | `div.mt-8::after` 纯 CSS 补回：`content` = 「2 轮 · 27 步 · LLM 3m36s · 工具调用 7.2s · 首 token 平均 0.8s · 159 tok/s · 缓存命中 96% · 输入 1M tok · 输出 31.1K token」；**12px / lh16 / 新变量 `--r93-meta: rgb(var(--gray-5))`**（设计稿实测 #A9A9A9 = gray-5，**不是** text-4 的 #C9C9C9）。hero `padding-bottom` 12 → **8** |

**实测（`ev/p97d.sh`，1440 / 2560 双档）**：`wrap` / `bottom` / `sb` / `agents` / `composer` **右边界全等**
（1440 → **1280**；2560 → **1981**）；`.r93-card` `[438,842]`（2560 → `[858,1123]`，18px 左缩进保留）；
agent 行 `agentSpan` = `[420,1280]` / `[840,1981]`（**填满**）；`div.mt-8` 高 154 → **178**（补上统计行）；
`doc = win`（900）。用户 `:root` 新增 `--r93-meta`。
⚠ **仍按设计稿刻意未动**：`.r93-card` 的 18px 左缩进、`.r93-bub` 的 728px（见 HANDOFF 第六节 item 20）。

**⑧ r98 三条（同日第八轮 · 就地返工 `apply93.py`）**

| # | 需求 | 现值 |
|---|---|---|
| ① | 对话内容部分 **14px → 15px** | 新增 **`.r93-t14, .r93-t14m, .r93-t14b { font-size: calc(15px * var(--ui-fs-ratio)) }`**（写在三条定义**之后**、**只写 font-size**，行高仍由 r96 的 `line-height:22px` 经 apply88b 派生）。选择器保持 **(0,1,0)** ⇒ `.r93-card.r93-card *`（(0,2,0)）仍把**卡内**压回 13px ✓。DS 无 15px 档 ⇒ 用 `calc(15px * ratio)` 而非 `var(--font-size-*)`，**未动 token** |
| ② | rateline 模块**下间距 48px** | `.r93-wrap` `padding: 32px 0 24px` → **`32px 0 48px`**。rateline 是本轮最后一个 `.r93-it`（实测 `isLast=true`、无 `nextSibling`）⇒「下面间距」= 内容盒下内距；每块自带的 `--mt` 只管「上面」，不动 |
| ③ | `r93-diff` 逐像素还原 | 整卡重做（见下表）；顺手修掉 `.r93-alink` 的 12px bug（见下「★ bug」） |

**③ 差分卡「逐像素还原」对照（设计稿 `1393:18681`「容器 252」= 840×300，坐标卡内相对）**

| 部位 | 设计稿 | 旧 → 新 |
|---|---|---|
| 底 | 表头带 `#F5F6F7` + **列表纯白面板**（两层） | 整卡 `#F5F6F7` → `.r93-diff{bg-2}` + `.r93-dhead{--r93-card}` |
| 表头 | **40 高** + 底 1px `#ECEEF2`（`--r93-edge`） | `height:28` 无 line → `40 + border-bottom`，`padding:6px 6px 5px 12px` |
| 行 | 高 36、行线 `#F2F2F2`（`--color-border-1`）、**首行无上边线** | 7 行全带线 → `:first-of-type{border-top:0}`（★ 因 `r93-dsb` 是首子元素，改 `:first-of-type` 并把 `<i>` 挪到列表**尾部**，见 PLAYBOOK P3.29②） |
| 行内距 | **左 11 / 右 13**（文件名墨迹 x13；⋯ 盒 x801..825） | `0 36 0 8` → `0 13 0 11` |
| 数字列 | 与 ⋯ 间距 **17**、右沿距卡内右 **54** | gap 8 → `gap:17` |
| ⋯ | 字色 **(31,31,31)** = `text-1`；悬停 **白底 + 1px 描边盒** 24×24 | `text-2`/`fill-2` → `text-1` + `bg-2 + inset 0 0 0 1px border-2` |
| +800 | **(48,149,59)** = `--r93-ok` | `--color-success-6`(59,179,70) 偏亮 → `--r93-ok` |
| -125 | (245,63,63) ✓ | 保持 `--color-danger-6` |
| 按钮 | DS 次要 small，外框 **70×28** | 宽 72（基类 1px transparent 边框占 2） → `padding: 0 11px` ⇒ **70** |
| 表头图标槽 | 槽宽 **24**、字形左缩 2 ⇒ 标题落卡内 **36** | 图标盒 14 ⇒ 标题 39 → `.r93-dhead .r93-dh1 > .r93-iblk:first-child{margin-right:-3px}` ⇒ 标题 **456** ✓ |
| 表头数字组 | gap **8** | 全 12 → 新增 `.r93-dh2{gap:8}` 包 `+800`/`-125` |
| 滚动条 | `矩形 219` = **6×128**、rgba(0,0,0,.16)、r6、卡内右 4 / 顶 4 | 无 → `<i class="r93-dsb">` + 绝对定位（**静态装饰**，待拍板是否保留） |

**★ 修掉的真 bug —— `.r93-alink` 一直不是 12px**：`.r93-bt { font: inherit }`（第 412 行）与 `.r93-t12`（第 363 行）**同为 (0,1,0)** 但 shorthand **写在后面** ⇒ 后写者胜，把「任务完成，耗时28m12s」撑成 14px。设计稿墨迹 **160px ≈ 11 汉字 + 5 半角 @12px** ⇒ 在 `.r93-alink`（写在 `.r93-bt` 之后）补 `font-size: var(--font-size-body-1)`（见 PLAYBOOK P3.29③）。

**实测（`ev/p98b.js`，1440 / 2560 双档）**：内容区字号分布 **12×49 / 13×42 / 15×59 / 14×2**（残留 14 = `撤销`/`审查` 两个 DS small 按钮，设计稿本就 14 ⇒ 保留）；卡内 `.r93-t14` 仍 **13px**；`.r93-wrap` pb **48**；差分卡 `[420,3651,860,300]` bg 白 / 边框 `rgb(236,238,242)` / r8；`.r93-dhead` h**40** / bg `rgb(245,246,247)`；`.r93-dsb` 右距卡内右沿 **4**；`.r93-drow` h36 / gap**17** / pad `0 13 0 11` / 首行 btWidth **0**；右对齐账 **⋯−13 / 数字−54 / 名+11** 全对；`.r93-dh1` **209×22** = 设计稿尺寸、标题 x**456**、按钮 **70×28**。（2560 同构，卡内右 1980。）
⚠ 首跑门禁 **77（应 76）**：新增注释里写了裸字号写法 ⇒ **字号检查不跳注释行**（hex 检查会跳）⇒ 改措辞归零（见 PLAYBOOK P3.29①）。

### P3.11h ★★ 页面路由表（`SHELL-NAV-FIX v5` · **10 页各一份、逐字相同**）+ 新开一页的范式

- **每页都是自包含独立 html**（顶栏 + aside + 外壳各一份，**无共享布局、无真实客户端路由**）；
  页间跳转 = 每页内嵌 `ROUTE` 表 + `hashchange`：
  `'/'`·`'/base'`→base ｜ `'/dev'` ｜ `'/kanban'` ｜ `'/req-kanban'` ｜ `'/task-detail'` ｜ `'/avatar'` ｜ `'/automation'` ｜ `'/skills'` ｜ `'/settings'` ｜ **`'/conversation'`（r93 ④）**。
  ⚠ 外壳 `navigate()` **`file://` 下才真跳页**，`http://` 下只改 hash ⇒ 预览一律 `file://` 直开。
- 顶栏「工作台切换」= 另一段 `SHELL-TABS-FIX v4`（`FILE={base,dev}` / `DEV_PAGES={dev,kanban,req-kanban,task-detail}`）；
  **「某页属哪个工作台」grep 每页 bundle 里的 `DEV_PAGES`**，别凭页面名推断。（conversation 不在 `DEV_PAGES` ⇒ 在它上面点「基础工作台」是空操作，符合预期。）
- **新开一页**：由「源页净底」重建（**不复制**）→ 换 `<html data-rNN-page=slug>` + `<title>` → 页面级 CSS 挂 `html[data-rNN-page='slug']` → **全页 `ROUTE` 各插 1 条**（counted 断言）→ 需要跳转就在源页注入小 nav 脚本。细则见 **PLAYBOOK P3.24⑦**。
- ⚠ `file://` 下 localStorage **不跨页面共享** ⇒ 独立页拿不到「源页选中态」，要传参走 hash。

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


---

#### P3.11g ⑨ r99 十四条（会话详情页 · 2026-09-30）

* **设计稿权威坐标（新增，以后直接用）**：
  * `1393:18599 容器 247`（rateline，256×24，`left:164; top:4664`）——
    `容器 246` 图标组 0..56（两枚 24×24，gap 8）· `直线 46` left **68** / top 5 · `Link` left **80** / 142×24
    （`svg_bff3c9ce` 14×14 + `Token 速率：256/s` 14/24 MiSans #868686）· `直线 47` left **234** / top 5 · `icon-wrapper` 24×24。
    ⇒ 线高 14（24−5×2）；线1 68 / 线2 234 是本页验收锚点。
  * `1393:18477 容器 180`（umeta，95×24）—— `fw647:14502` 24×24（props 尺寸14，节点名「点击后变成绿色的勾勾图标」）、
    `fw647:14503 icon-wrapper` 24×24（尺寸14）、`fw647:14497` `15:26` 12/16 `#868686`。
    **位置/形状只能读 PNG**（祖先全 flex）：时间墨迹 910..938 / 按钮盒 950.5..974.5 / 980..1004 ⇒ 间距 **13 / 6**。
* **本页新增/修改的固定事实**：
  * `.r93-dlist` = `overflow-y:auto`（**删掉装饰件 `.r93-dsb`**，含模板里的 `<i>`）。
  * `.r93-tobottom` 默认 `--color-text-2`；★ r100 ③ 起 `:hover{ background: var(--color-fill-1);
    color: var(--color-text-1) }` —— **不再改边框色**。
  * `.r93-ib:hover` = **白底 + `box-shadow: inset 0 0 0 1px var(--color-border-2)`**（灰卡里不能用 fill-2，比卡底还深）；
    `[data-r93-copy]` 点后加 `is-copied` → `IC('ok')` 绿勾（`--r93-ok` #30953B）+ 0.18s 弹出，1.6s 还原。
  * `.r93-ctx*`（≈55 行）= `task-detail` 的 `.td-ctx` 范式移植：182 / padding 6 / gap 2 / 圆角 8 / `--shadow3-down` /
    双类提权 + `animation:none`（本页内联的 `.giencoder-dropdown-popup` 带 0.2s 入场动画，播完 opacity 落 0 ⇒ 菜单闪没）。
    **contextmenu 与 `.r93-dmore` 共用同一节点**；关闭途径 pointerdown / blur / resize / scroll / Esc（**刻意不做键盘 ↑↓ Enter**）。
  * `--r93-pillc:#3491FA`（暗色 `#6BA6FF`）—— 设计稿 `容器 25` 实测 (52,145,250) ≠ primary-6 #3770F7；
    `.r93-pill` 摘掉 `.r93-t12`、自写 15px/20px（盒高保 22）、投影保留。
  * `.r93-card` 默认字号 **14px**（r97 13 → r99 15 → **r100 14**）；`.r93-card--quiz{padding:20px}`（盒高实测 208 = 设计稿）。
  * `.r93-alink` / `.r93-artlabel` = 15px；`.r93-asst` 边线 = `--color-border-2`。
  * `IC('regen')` **重画为 14 栅格**：弧 `M13.9 9.4A5 5 0 0 0 4.1 8.9` + 实心箭头 `M1.05 7.85 4.4 7.95 2.95 10.6Z`。
* ⚠ **本页图标一律不要用「按坐标推算」的工具去改**（见 PLAYBOOK P3.30①）。

#### P3.11g ⑩ r100 八条（会话详情页 · 2026-09-30）

* **设计稿权威取数（新增）**：
  * `.r93-ndesc` 胶囊（**HTML 导出里查不到底色/圆角，只能读 PNG**；`board(x,y) → png(x+1,y+1)`）：
    `fw647:18372` 底 x195..972 / y3355..3378 = **778×24**（墨迹内距 13 / 13）；
    `fw647:18418` 底 x434..733 / y3433..3456 = **300×24**（墨迹内距 13 / 14）。
    ⇒ **盒宽 = 文字宽 + 两侧 12px 内距**；底色实测 **rgb(247,247,247) = `--color-fill-1`（gray-1）**；
    圆角由角部灰度剖面反解 = **12px = `--border-radius-xl`**（24 高取到上限 ⇒ 视觉全圆角）；两行在 840 列里居中。
  * `1393:18521 容器 221`（调用 5 个工具，840×404）**层级缩进**：折叠头 / 展开头 **left 0**；
    `容器 218`（内嵌 Tool call 块 822×200）**left 18**，其代码卡 `容器 217`（804×132）**left 36**；
    `容器 219`（4 行汇总清单 305×124 @ top 246）**left 18**。
    ⚠ **设计稿没有画连接线**（PNG 该 x 区间只有卡片底 `#F5F6F7` 与描边 `#ECEEF2`）——线是本轮新增要求。
  * `容器 218` 里两个 `Link`（`fw647:18138` 折叠态 424×22 带 14px tool 图标 / `fw647:18151` 展开态 424×22 带 chevron）
    是**同一节点的两态叠加**（又一次「变体叠加」陷阱）⇒ 实现里只留一份、由 `data-open` 切。
* **本页新增/修改的固定事实**：
  * 助手名 = **`GienCoder`**（r100 ① 更名；`task-detail.html` 的 `GienX端到端初始化…` 也已更名）。
  * `.r93-card` / `.r93-card.r93-card *` = **14px**（`calc(14px * var(--ui-fs-ratio))`）⇒ 卡内一律 14px。
  * `.r93-drow{cursor:pointer}` + `wire()` 里**整行左键 = 开同一张 `.r93-ctx` 菜单**（点 `⋯` 贴按钮左下角、
    点行内其余位置贴整行左下角）。7 行 `cursor` 全 `pointer`。
  * `.r93-agent:hover{ background: var(--color-fill-2) }` —— **不再改边框色**；`.is-on` 的紫描边不受影响。
  * `.r93-ndesc` = `width:fit-content; margin:8px auto 0; height:24px; padding:0 12px;
    border-radius: var(--border-radius-xl); background: var(--color-fill-1); color: var(--color-text-3)`。
  * `.r93-tree`（新增）= `margin:12px 0 0 6px; padding-left:12px` + `::before` **1px 竖导线**；
    子项（`.r93-fold` / `.r93-sumrow`）各挂一枚 **8px 横向肘节**（`left:-12px; top:11px`）。
    内嵌的 Tool call 层改走同一个 `fold()` 工厂（`ctmeta:true` 把元信息也放进折叠头）。
  * `.r93-nest` **已删除**（由 `.r93-tree` 取代）；`.r93-sumlist` 不再自己画线。
* ⚠ 本页 `fold()` 工厂的 `o.mt` 用 `!= null` 判空（`mt:0` 是合法值）；肘节必须 `position:absolute`
  （绝对定位伪元素不算 flex item）——详见 PLAYBOOK P3.31④⑤。
