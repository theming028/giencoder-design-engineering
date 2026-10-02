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

### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十二拍**）

> 补丁 = **`mg-work/r108/apply108.py`**（🚫 未提交 · 第十二拍；前身 `mg-work/r107/apply107.py` 已推送 `e9c9498`）；设计依据 = `docs/codex-sidepanel-research.md` + `docs/codex-refs/`。
> **只影响 `pages/conversation.html`**：`base.html` 与 8 个外壳页**逐字节不变**（nav 块沿用 `r106-nav-js` 不换名）。
> **十一拍要点**：① 三段式骨架 + 五模块 · ② 浮窗关不掉 / 侧聊对齐 · ③ 删侧聊 / 并排折叠 / 折叠全部 / 补 Codex 遗漏 ·
> ④ 摘要升默认 + 卡片式 / 补划词浮条 / 补右键菜单 / tab 14px / 下拉 DS 化 ·
> ⑤ 下拉 hover 补齐 + 下拉改挂 DS Dropdown（从「导航菜单 Menu」族改正过来）·
> **⑥ 底部统计行「框选不到」实为 CSS 生成内容 → 换真 DOM / `.r93-pre` 去字体族 / 内容列变窄时技能浮窗与 `.r93-alert` 自适应** ·
> **⑦ 右栏里的竞品名全换 GienCoder / 去掉下拉菜单的标题行与快捷键提示 / 选中项补底色 / 提交卡输入框拉通 / 右栏字体统一 / 全屏按钮联动** ·
> **⑧ 全局宽度不足出省略号（三类分治）/ 去掉「折叠此文件」/ `.td-sum-h` 15px / `.td-diff-path` 展开中粗 / `.td-diff-path` 与 `.td-diff-rows` 内 13px / `.r107-stats` 居中** ·
> **⑨ 全屏按钮图标随态切换（四角朝外 ⇄ 朝内，切 `<path d>`、不重建节点）/ 全屏态拖拽起点改读「实际渲染宽」（先停过渡再取几何）/ 拖拽事件改挂 `window` / 全屏态按下分栏条＝放弃全屏 / 收起侧栏也退全屏**
> **⑩ 三枚 `.td-rv-menu` 改为「按触发器现场摆位」** —— 原四枚共用一条 `top:42px`（钉在标签栏下方），
> 而这三枚的触发器在**审查工具条**里 ⇒ 菜单跑到**按钮上方** 34~36px（实测 dy = −35.0 / −34.0 / −36.0）；
> 新增 `placeRv()` 在打开瞬间按触发器**实际几何**摆位（垂直 +6px / 水平锚定触发器 / 右侧放不下 clamp 到面板内边），
> `.td-mod-menu` 一字不动
> **⑪ 对照 Codex 官方补缺（三件）+ 划词浮条正文黑 + 地址栏激活态 + 数字动效提速** ——
> ① `.td-selbar` 两枚 DS 文字按钮 **默认正文黑**（`.td-selbar .giencoder-btn{color:var(--color-text-1)}`；
> DS 的 `-btn-text` 基类默认是**主色蓝** `rgb(55,112,247)`）·
> ② `.td-url-pill` 补 **`:focus-within` 激活态**（底色转白 + **`inset` 1px** 主色 + 外 **2px** 浅主色环 + `transition 120ms`；
> ★ **用 `inset` 不用 `border`**，否则 26px 胶囊被撑高）·
> ③ 数字动效提速（骨架屏 `1100→380` + `duration .46→.30` / `delay 1.5s→calc(.44s+ni*26ms)`，空窗 **167ms → 0**）·
> ④ **补三件官方能力**：**终端多标签**（`.td-term-tabs` + `bindTerm()` 按块绑定 + `+` 真新建）/
> **浏览器截图**（`[data-td-brw-act="shot"]` + `.td-brw.is-shot::after` 快门 **260ms**，闪**整模块**而非滚动容器 `.td-view`）/
> **产物预览层**（`.td-sum-prev` 覆盖摘要 + `md`/`xlsx` 两套骨架 + **Esc 算一层**）
> **⑫（r108 第十二拍）`td-diff` 独立成小卡片（`1px` 描边 + `8px` 圆角 + `--color-bg-2` 底 + 容器 `gap:8px`）/ 「在文件树中定位」右侧新增「文件树」按钮 ⇒ 右侧弹**文件树抽屉**（`.td-tree` · `z-index:35` · 独立类名 `td-tf*` · Esc 算一层）**。
> （详见 `mg-work/r107/acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五** / **十六**节；r108 = `mg-work/r108/acceptance.md` 七节）。

**结构（三段式，全部挂在 `aside.td-browse` 里）**

```
td-split#av-browse-split → td-browse-slot#av-browse-slot
  └ aside.td-browse            ← ★ 本代给它补了 position: relative（模态的包含块）
      ├ header.td-browse-bar   ← ① 标签栏
      │   ├ .td-browse-tabs > .td-browse-tab[data-td-mod]（图标 + 名称 + .td-tab-x）
      │   ├ button.td-browse-add[data-td-add]  ＋
      │   ├ .td-mod-menu[data-td-open-mod=…]   ＋ 的五选一菜单（默认 hidden）
      │   ├ span.td-browse-sep
      │   └ .td-browse-acts > button[data-td-max] ＋ button[data-td-browse-close]
      ├ div.td-browse-body          ← 「文件」模块正文（**r105 原样，逐字未改**）
      ├ section.td-mod.td-mod-term[data-td-pane="terminal"]
      │   ├ .td-term-tabs（★ 第十一拍 ④a：zsh / npm run dev / ＋）
      │   └ .td-term[data-td-term-pane="t1|t2|…"] ×N
      ├ section.td-mod.td-rv      [data-td-pane="review"]
      ├ section.td-mod.td-brw     [data-td-pane="browser"]
      ├ section.td-mod.td-sum     [data-td-pane="summary"]  ← 摘要（任务侧栏：摘要 / 计划 / 来源 / 产物）
      └ div.td-tree[data-td-tree]   ← ★ r108：文件树抽屉（`z-index:35`；`.td-tree-panel` `min(296px,86%)` + `.td-tree-files` 内 10 行 `.td-tf*`，类名与「文件」模块的 `.td-bf*` **刻意分离**）
```

> ⚠ 四枚下拉菜单（`.td-mod-menu` / `.td-rv-scope-menu` / `.td-commit-menu` / `.td-rv-opts`）**都挂在各模块自己的工具条里**，
> 但定位参照是 `.td-browse`（有 `position: relative`）、`top: 42px` ⇒ 不会被 `.td-mod{overflow:hidden}` 裁掉。
> ★ 第五拍起这四枚 + 右键菜单 `.td-ctxmenu` **同挂 DS 的 `giencoder-dropdown-popup`**（双类提权：`.td-mod-menu.giencoder-dropdown-popup` …）。

**固定事实**

| 项 | 值 |
|---|---|
| 模块 id | `files`（= `.td-browse-body`）/ `review` / `terminal` / `browser` / **`summary`** ← 第三拍起 `side` 已删除 |
| **默认页签** | ★ **第四拍 ⑨ 起 = `summary`**（原 `files`）：`_head.html` 初始标签的 `data-td-mod` + `panel.js` 初始化 `activate('summary')` **两处同改**（缺一即不生效） |
| tabindex=0 的元素 | `.td-term`（终端正文，收键盘；★ 第十一拍 ④a 起**每块一份**，N 个） |
| 面板开关 | **不变**：`.r93-baract[data-r93-browse]` 切宿主 `.av-browse-on`（ctrl-conv.js 接管） |
| 宽度变量 | **不变**：宿主 `--av-browse-w`（默认 641 / MIN 561）；`⤢` 写它，还原时读 `localStorage['giencoder:r105-browse:v1'].panelW` |
| 单标签 | `.td-browse-tabs.is-single` ⇒ `×` 不显示（不许关到空） |
| `＋` 位置 | 紧跟最后一枚标签 ⇒ `.td-browse-tabs{flex:0 1 auto}` + `.td-browse-acts{margin-left:auto}` |
| Esc 层级 | window 捕获段：**划词浮条** → 模态 → 菜单 → 元素评论 → **产物预览层** →（再交给 ctrl-conv）关侧栏（★ 第十一拍 ④c 把预览层接进来，否则开着预览按 Esc 会**把整条侧栏关掉**）|
| **浮窗搜索根** | ★★ `closeMenus()` 与 Esc 裁决都用 **`pane`（= `.td-browse`）**，**不是 `bar`** —— `.td-rv-opts` 挂在模块工具条 `.td-mod-bar` 里、不在标签栏内（第二拍真 bug，见 PLAYBOOK P3.39⑧） |
| **审查工具条** | `对比范围 ⌄ +566 −228 4 个文件` + 右端 `复制 / 定位 / ⋯ / 提交⌄ / PR`（定位会真切到「文件」标签）|
| **审查显示选项** | `.td-rv-opts` **十项** = 统一 / 并排 + Codex 八项（刷新 / 自动换行 / 折叠·展开全部 / 不加载完整文件 / 富预览 / 词级差异 / 隐藏空白 / 复制 git apply）。**复选型点了不收菜单**；`is-wrap` / `is-worddiff` / `is-hidws` 三个真生效 |
| **折叠全部 ⇄ 展开全部** | `[data-td-rv-fold]` 单项双向：**只要还有折叠着的文件就显示「展开全部文件」**；文案 + 字形一起翻；单文件折叠后也会回同步 |
| **并排视图折叠** | ★★ 必须是 `.td-rv-body.is-split .td-diff.is-open .td-diff-split` —— **`.is-open` 不能省**（省了就与 `.td-diff:not(.is-open) .td-diff-rows` 同特异性、靠文档顺序取胜 ⇒ 并排态折不动；PLAYBOOK P3.39⑩）|
| **动作反馈** | `.td-toast`（绝对定位在 `.td-browse` 上，1.4s 自动收）；**动作类菜单项点了收菜单、复选开关不收** |
| **右栏快捷键** | `⇧⌘G` 审查 · `⇧⌘E` 文件 · `` ⌃` `` 终端（`⌘T` / `⌘P` 是浏览器级、拦不住 ⇒ 不绑；输入框聚焦时不触发）|
| diff 取色 | **加绿（`--color-success-light-1` / `-5`）/ 删红（`--color-danger-*`）** = GitHub 惯例（**不是**行情口径） |
| 暗色 | **零硬编码**：全部走 token，`gray/green/red/giencoderblue` 色阶在暗色档整体翻转 ⇒ 不需要 `[giencoder-theme='dark']` 分支 |
| **`.td-browse-tab` 字号** | ★ 第四拍 ⑫ = **14px**（`--font-size-body-3`，原 12px / `--font-size-body-1`）；标签高由 `min-height` 撑 ⇒ 仍是 28px |
| **摘要四模块卡片式** | ★ 第四拍 ⑨：`.td-sum-sec`（×4：摘要/计划/来源/产物）= `1px --color-border-1` 描边 + `8px` 圆角 + `--color-bg-2` 底 + `12px` 内距；容器 `.td-sum-body { padding:12px; gap:12px }`；**卡内**来源/产物降为**行式**（`bw:0`、`padding:6px 8px`、hover `--color-fill-1`）避免「卡中卡」 |
| **划词浮条** | ★ 第四拍 ⑩ 补回 `.td-selbar`（第三拍曾随 side chat 删）：两枚 **DS 文字按钮**（`giencoder-btn giencoder-btn-text giencoder-btn-size-small`）「添加到对话」（真写主 `textarea`）/「复制」（`execCommand('copy')`）；在 `.r93-scroll` 内 `mouseup` 选区 ⇒ 浮在选区上方；`mousedown` / `scroll` / `resize` / Esc 收起 |
| **右键菜单** | ★ 第四拍 ⑪：**九类目标共用一份表驱动容器 `.td-ctxmenu`**（`role=menu`）—— 标签 5 / 审查文件头 7 / 审查代码行 5 / 终端 6 / 浏览器元素 6 / 浏览器空白 5 / 摘要来源 3 / 摘要产物 3 / 计划条目 4；`is-danger` 红字；能复用既有 handler 的一律 `元素.click()`；**右栏内普通空白 / 右栏外都不接管** |
| **四枚下拉 = DS 组件** | ★ **第五拍 ⑮ 更正组件族**：`.td-mod-menu` / `.td-rv-scope-menu` / `.td-commit-menu` / `.td-rv-opts`（+ 右键 `.td-ctxmenu`）容器 = **`giencoder-dropdown-popup`**，条目 = **`giencoder-dropdown-item`**、分隔线 = **`giencoder-dropdown-divider`**、危险项 `.is-danger`；**hover = `--color-fill-2`**（`pad 5px 8px / radius 4 / h 32`）。选中态用「主色文字 + ✓」（Dropdown 无 `-selected` 类）。<br>⚠ 第四拍 ⑬ 曾挂 `giencoder-select-popup`（**Select 的弹层**）+ `giencoder-menu`（**导航菜单**，`mapsFrom: sidenav/topnav`）⇒ **串了两个族**，第五拍按 `dropdown.json` 契约改正（与**本页** r93 ⑦ `.r93-ctx` 同源）。<br>面板 `pad6 / gap2 / radius8 / bg-popup / border-2 1px / shadow3-down / min-width168`；条目 `pad 5px 8px / radius4 / lh calc(22px×ratio) / gap8 / h32 / hover --color-fill-2`；选中态 = **主色字 + `.td-mm-mark` ✓**（Dropdown **无** `-selected` 类，不虚构）；`giencoder-menu-group-title` 仅分组标题处**借用**（Dropdown 无此件）；`giencoder-menu-icon` 已撤（`.td-mm-ico` 收回自绘） |
| **底部统计行** | ★ **第六拍 ⑯**：它是 `main > div > div.flex-1.justify-center > div.mt-8::after` 的 **CSS 生成内容**（原 **不可框选**）⇒ 现由 `panel.js` 的 `statsBoot()` 注入**真节点 `.r107-stats`**（`MutationObserver` 兜 React 重渲染）；`panel.css` 用同选择器 `content:none` 关掉旧伪元素、并复刻版式（`12px` / 行高 `16×ratio` / `--r93-meta` / nowrap）。宿主 `div.mt-8` 是 `flex-col gap-2` ⇒ 间距仍是 8px |
| **`.r93-pre` 字体** | ★ **第六拍 ⑰**：`font-family: var(--font-family)`（= 全局默认，原为等宽族 `ui-monospace, …`）；**只覆写这一条**，字号 `14px` / 行高 `16px` / 换行策略不变 |
| **内容列变窄时自适应** | ★ **第六拍 ⑱**：技能选择浮窗 `html[data-r93-page='conversation'] .giencoder-select[role='listbox'][aria-label='技能选择'] { width: min(760px, 100%) !important }`（React **行内**写死 760 ⇒ 必须 `!important`；包含块 = 输入卡）；`.r93-alert` 由定高 44 改 `height:auto; min-height:44px; padding:8px 16px`（单行态**零变化**，折行才长高） |
| **下拉菜单的「标题行 / 快捷键」** | ★ **第七拍 ⑲⑳**：两者都**隐藏** —— `.td-browse .td-mm-cap, .td-browse .td-ctx-head { display:none }` 与 `.td-browse .td-mm-key, .td-browse .td-ctx-key { display:none }`。⚠ 各自都有**两类来源**（静态 HTML + `panel.js` 现场生成）⇒ 只改 HTML 治不全，一律用 CSS 关 |
| **选中项底色** | ★ **第七拍 ㉑**：`.td-…menu .giencoder-dropdown-item.is-checked { background: var(--color-primary-light-1) }` —— 原来只有主色文字 + ✓（实测 `rgba(0,0,0,0)`）；规则写在 `:hover` **之后** ⇒ 悬停选中项不翻成 hover 灰；**不补** 3px 左缘条（那是 Menu 族的表达） |
| **提交卡「目标分支」输入框** | ★ **第七拍 ㉑**：`.giencoder-input-wrapper.td-commit-in { display: flex }` —— DS 编译样式是 `inline-flex; width:auto; min-width:120px` ⇒ 原来只有 207（同卡 `.td-commit-h/-lb/-msg/-f` 都是 308） |
| **右栏字体族** | ★ **第七拍 ㉒**：`panel.css` 自己那 8 条写死的等宽族就地换 `var(--font-family)`（`.td-diff-path` / `.td-diff-stat` / `.td-dr` / `.td-dsc-c` / `.td-diff-more` / `.td-commit-num` / `.td-term` / `.td-url-pill input`）；「文件」模块代码区那条在 **r102 代已交付的 `part105/browse.css`** 里 ⇒ 用 `.td-browse .td-browse-pre { font-family: var(--font-family) }` 覆盖（153 个 `.td-code*` 靠继承） |
| **全屏按钮联动** | ★ **第七拍 ㉓**：`.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }` —— 右栏展开时隐藏、收起复现。**纯 CSS 即可**（实测 `.av-browse-on` 挂在 shell flex 行 = `main` 与预览栏的共同父级上，按钮在其内）；⚠ 只针对这一枚，别用 `.r93-baracts` 整组 |
| **右栏竞品名** | ★ **第七拍 ⑲**：右栏里**渲染成文字**的 8 处 + 两处悬停 `title` 全部换成 GienCoder；**三条 `td-sum-src` 外链 `href` 与历代设计来源注释有意保留**（URL 替换即 404、且不渲染） |
| **全局省略号口径** | ★ **第八拍 ①**：**三类分治** —— 单行文本容器 ⇒ 三件套截断（`min-width:0` + `overflow:hidden` + `text-overflow:ellipsis` + `white-space:nowrap`）；**代码 / 终端**与**多行正文** ⇒ 保持折行、**不截断**。白名单 17 类见 `panel.css` 第 14 节 |
| **`.td-sum-h` 字号** | ★ **第八拍 ③**：`calc(15px * var(--ui-fs-ratio))` —— 15px **无 title token**，故**不写裸 px**（裸 px 会被 `converge()` 压平、且不吃 `--ui-fs` 杠杆） |
| **`.td-diff-path` / `.td-diff-rows`** | ★ **第八拍 ④⑤**：path 13px；`is-open` 时 path `font-weight:500`；rows 容器 13 且 `.td-dr` / `.td-dsc-c` / `.td-diff-more` **逐条覆盖**（只改容器无效） |
| **`.r107-stats` 居中** | ★ **第八拍 ⑥**：`text-align: center` —— ⚠ `width/min-width/max-width` **全被页面级两条 `!important` 钉死**（盒宽恒等于输入卡 860/714/315），`fit-content + margin:auto` 那一版是**死代码** |
| **全屏按钮图标** | ★ **第九拍 ①**：`browse.html` 里写死的「四角朝外」SVG 是**静态 HTML** ⇒ 光翻 `aria-pressed` / `title` 不够，必须切 `<path d>`。MAX **从 DOM 读出来缓存**、MIN 硬编码（Lucide `minimize` 四条），只改属性、不重建节点 |
| **右栏拖拽起点** | ★ **第九拍 ②**：`ctrl-conv.js` 的拖拽起点一律读**实际几何**（先落 `.is-col-dragging` = `transition:none` 再取 rect ⇒ 拿到**终值**）。⚠ 宿主若**绕过控制器直接写 `--av-browse-w`**（「最大化」就是这样），内部缓存 `panelW` 必然脱节 ⇒ 「一按下就跳回记忆宽」。事件侧：`pointermove` / `pointerup` 挂 **`window`**（磁捕获不可靠） |
| **`.td-rv-menu` 摆位** | ★ **第十拍 ①**：**按触发器实际几何现场摆位**（`panel.js` 的 `placeRv()`，在 `toggleMenu()` 打开分支、**摘掉 `[hidden]` 之后**调用）。⚠ 原四枚共用基类 `{ position:absolute; top:42px }`（相对 `.td-browse`）—— 该值只对**触发器在标签栏**的 `.td-mod-menu` 成立，另三枚的触发器在**审查工具条**里 ⇒ 实测 dy（菜单 top − 触发器 bottom）= **−35.0 / −34.0 / −36.0**（跑到按钮**上方**）。量宽高用 `offsetWidth`（不受入场 `scale(0.96)` 影响） |
| **`.td-rv-menu` 的 clamp** | ★ **第十拍 ①**：`left = host.clientWidth − menu.offsetWidth − 4`（右侧放不下 ⇒ 向左收，贴住面板右内边）。★ 窄栏 315 实测三枚全部 `insideMod = true`（**没被 `.td-mod{overflow:hidden}` 裁**）。CSS 只留静态兜底 `top: 83px`；⚠ 写行内 `left` **必须同时 `right:'auto'`**，否则与基类的 `right` 一起把盒子拉宽 |
| **终端标签条** | ★ **第十一拍 ④a**：`.td-term-tabs`（`role=tablist`）+ N 块 `.td-term[data-td-term-pane]`，切换**只切 `hidden`**。`panel.js` 里 `bindTerm(el)` **按块绑定**（`echo` 收进各自闭包）；另有 `termPanes()` / `activeTerm()` / `showTerm(id, focus)` / `newTermTab()`。⚠ 全页 `.td-term` 的**单数选择器**一律改走 `termPanes()`（`ctxForTerm()` 也改 `activeTerm()`，否则永远只操作第一块） |
| **浏览器截图** | ★ **第十一拍 ④b**：`[data-td-brw-act="shot"]`（相机图标，插在「标注」与「缩放」之间）+ `.td-mod.td-brw{position:relative}` + `.td-brw.is-shot::after` 快门白闪 **260ms**。⚠ 闪**整模块**、不闪 `.td-view`（后者 `overflow:auto`，绝对定位子元素**跟着内容滚走**）；⚠ 动画必须 **≤300ms**（`verify-design.py` 的 `CRAFT-ANIM` 会数 >300ms 的） |
| **产物预览层** | ★ **第十一拍 ④c**：`.td-sum-prev`（`position:absolute; inset:0; z-index:6`，包含块 = `.td-mod.td-sum`）+ 两套骨架 `[data-td-prev-kind="md"/"xlsx"]`（**按扩展名**切）。⚠ 骨架自带 `display:flex` ⇒ **必须显式写 `[hidden]{display:none}`**；⚠ **Esc 层级多了一层**（预览层 → 元素评论 → 菜单 → 模态） |
| **地址栏激活态 / 浮条色** | ★ **第十一拍 ①②**：`.td-url-pill:focus-within`（底色转白 + `inset 0 0 0 1px` 主色 + 外 `0 0 0 2px` 浅主色环，`transition 120ms`）· `.td-selbar .giencoder-btn { color: var(--color-text-1) }`（DS `-btn-text` 默认主色蓝） |
| **diff 独立卡片** | ★★ **r108 ①**：`.td-rv-body { display:flex; flex-direction:column; gap:8px; padding:8px }` + `.td-diff { border:1px solid var(--color-border-2); border-radius:8px; background:var(--color-bg-2); overflow:hidden }` + `.td-diff-rows { border-top:1px solid var(--color-border-1) }`。`overflow:hidden` 让 `.td-diff-h:hover` 底色被圆角裁住；`border-top` 不会双线（折叠态 `-rows` 本就 `display:none`，统一 / 并排两个 `-rows` 同刻只有一个可见）。实测四张卡 `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`、**卡间距 `[8,8,8]`**；描边 `1px rgb(229,229,229)` / 圆角 `8px` / 底 `rgb(255,255,255)`；并排折叠 ⇒ 卡高 **40**、`rowsDisplay:none` |
| **文件树抽屉** | ★★ **r108 ②**：按钮 `[data-td-rv-act="tree"]`（folder-tree SVG，24 网格 / stroke 2 / 渲染 16px，插在「在文件树中定位」**右紧邻**）+ `.td-tree[data-td-tree]`（`position:absolute; inset:0; z-index:35`；**右栏下拉 30 < 抽屉 35 < 提交模态 40**）。开合 = `hidden` 属性 + `.is-open` 类（`removeAttribute('hidden')` → `void offsetWidth` **强制 reflow** → `add('is-open')`；关 = 摘 `is-open` → **240ms（过渡 220ms）后**挂 `hidden`）。`min(296px, 86%)` 面板 ⇒ 实测 **`panelBox=[1135,49,296,842]`**（右缘 1431 = `paneBox` 791+641−1）；**Esc 只关抽屉、不关侧栏**（裁决链：模态 → 抽屉 → 菜单）|
| **抽屉树独立类名** | ★★★ **r108 最关键的决定**：`ctrl-conv.js` 的 `pane = slot.querySelector('.td-browse')` 是**整个 aside**、`pane.querySelector('.td-browse-files')` **只绑第一棵**（`querySelectorAll('.td-bf')` 会扫到抽屉树）⇒ 抽屉树**必须用独立类名 `td-tf*`**（行 `.td-tf` / 箭头 `.td-tf-arrow` / 图标 `.td-tf-ico` / 名称 `.td-tf-name`；`.td-tf.is-dir` 的 `padding-left` 与 `.td-bf.is-dir` 同口径），否则两边互相打架、抽屉里的行点了没反应。实测：抽屉里点 `Controls.tsx` ⇒ 抽屉 `active` 变，而「文件」模块那棵树 `filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10 |
**⚠ 改这一块之前必看**

1. **`part107/browse.html` 是组装件**：`ev/splice107.py` = 从 `part105/browse.html` **剪出 Files 正文**（逐字）
   + 换头部（`_head.html`）+ 追加四个新模块（`_mods.html`）⇒ 改完 **必须先 `splice107.py` 再 `apply107.py`**。
2. **新模块的 section 类名必须与内部件不重名**（`td-mod-term` / `td-rv` / `td-brw`）——
   初版 `td-mod td-term` 与内部 `.td-term` 撞车，`querySelector('.td-term')` 取到 section（见 PLAYBOOK P3.39①）。
3. **不要重跑 `apply106.py`**（只认四代 ⇒ 会因「基线残留 `r107-conv-css`」自检失败退出）。
4. `.td-browse-bar` 高 **44px 是 r106 钉住的**（与 `.r93-bar` 同高）⇒ 标签高度按 `calc(28px * --ui-fs-ratio)` 派生，
   `--ui-fs > 22` 时会被顶满（站内档位实测 18 仍宽裕）。
5. ★★ **本代 panel.css 里带行高的规则，`font-size` 必须写 `var(--font-size-*)` token** ——
   否则 `converge()` 会把 `line-height: calc(Npx * ratio)` 压成裸 px（15px 档用两段式写法）。
   自查：`mg-work/r107/ev/scan-flatten.py mg-work/r107/part107/panel.css`。
   ⚠ 只在默认 `--ui-fs=14` 下量**发现不了**（`calc(Npx × 1) = Npx`）⇒ 判据要看 **`--ui-fs=18`** 的行高。
6. ★★ **`+` 菜单只有五项**（审查 / 终端 / 浏览器 / 文件 / 摘要）—— **没有「侧边聊天」**。
   第三拍已把它全链路删除 ⇒ 页面里 `td-side` / `AV_SVG` / 「侧边聊天」四个字**应全为 0**。
7. ★★ **「不该出现在右栏里的词 / 字体」三查**（第七拍）—— 改这一块之后跑一遍：
   · `TreeWalker(SHOW_TEXT)` 走 `.td-browse`，正则 `/codex|chat\s?gpt/i` ⇒ 渲染文字应为 **0**；
   · `panel.css` 里 `ui-monospace` 应只剩 **1 处**（第 11 节的说明注释，不是声明）；
   · `.td-browse *` 里 `getComputedStyle(el).fontFamily !== bodyFont` 的元素数应为 **0**。
   ⚠ 同名前缀的还有**别的页**：`grep -i codex pages/*.html` 扫一遍再决定（第七拍就在 `avatar.html` 挖到 1 处）。
8. ★★ **下拉菜单的「标题行 / 快捷键提示」各有两类来源**（静态 HTML + `panel.js` 现场生成）⇒
   只改 HTML 治不全 —— 一律用 CSS 的 `display:none` 关（column flex 里塌行不占位，与删节点视觉等价）。
   ★ 同理：**联动显隐（第七拍 ⑦）先量状态类挂在哪一级**，能 CSS 就别写 JS（见 PLAYBOOK P3.43④⑤）。
   ⚠ **但 `td-selbar` 不再是 0** —— 第四拍 ⑩ 按邵先生要求**把划词浮条补回并做成真功能**（现 4 处）。
7. ★★ **`verify-design.py` 会数「渐变处数」** —— 别在这块新增 `linear-gradient`（`+1` 就进回归 diff）；
   进度态用「**边色 + 实心 tint**」表达（例：计划项的进行中 = `--color-primary-6` 描边 + `--color-primary-light-2` 实心）。
8. ★★★ **页面级通配适配层会扫到「新挂 DS 类」的弹层** —— `html[data-r93-page='conversation'] .giencoder-select-popup
   { top:auto!important; bottom:calc(100% + 4px)!important }`（r93 ④ 给贴底 composer 写的「下拉向上弹」）
   会把右栏里**任何**新挂 `.giencoder-select-popup` 的弹层一起翻到锚点上方（实测 `rect.y = -170`，整排看不见）。
   ⇒ 在 `panel.css` 里用**更高特异性**（多一层 `.td-browse` ⇒ (0,3,1)）的同名适配翻回向下
   （`top:42px!important; bottom:auto!important; transform-origin:top`）。**判据必须是量 `getBoundingClientRect()`**。
   ★ **第五拍起本条对四枚下拉已不再触发**（它们改挂 `.giencoder-dropdown-popup`，页面里**没有**针对它的通配规则，
   全站 `grep` 只有 r93 `.r93-ctx` 与 task-detail `.td-ctx` 两处**双类提权**的显式规则）——
   但**下次再给右栏挂新 DS 弹层类之前，仍要先 `grep` 页面级通配**。
9. ★★★ **`!important` 连行内 `style.top/left` 也压得过** ⇒ 靠 JS 定位的浮层（右键菜单）**别写行内坐标**，
   改写 **`--td-ctx-x` / `--td-ctx-y` 自定义属性**，再由 `!important` 规则 `top:var(--td-ctx-y)!important` 落位。
10. ★★ **同一份 DS 弹层要开合 ⇒ 靠 `.giencoder-popup-open` 这唯一开关**（DS 弹层默认 `visibility:hidden`）；
    别写内联 `display`。⚠ 本页另有 r75 的 `.giencoder-select-popup{display:block!important}`（为过渡留起点）——
    **只对 select 族生效**；第五拍换到 `.giencoder-dropdown-popup` 后不再被它压 ⇒ `[hidden]` 的 `display:none`
    兜底**恢复可用**（实测关菜单 `afterCloseHidden:true`）。⚠ DS Dropdown 骨架还带一条
    `animation: giencoder-popup-in`（播完把 `opacity` 打回 0 ⇒「闪一下就不见」）⇒ 适配层必须显式 `animation:none`。
11. ★★ **`converge()` 行高压平**（第二拍坑，长期有效）：本块凡声明 `line-height`/`height`/`min-height` 的规则，
    `font-size` 一律写 `var(--font-size-*)` token（无 token 档用两段式）。自查 `ev/scan-flatten.py`。
12. ★★★ **同特异性 `background` 会「后者胜」，而 `!important` 之外的输赢全看文档序** ⇒ 给 DS 条目写 UA 兜底
    （`<button>` 宿主要压 `buttonface`）时，**基态与 `:hover` 必须写在同一块、基态在前**。
    - 第四拍踩过 **①选中底被抹**：`.td-mm-item{background:transparent}` (0,1,0) 抹掉 DS 选中态的
      `--color-primary-light-1` ⇒ 改成 `:not(.giencoder-menu-item-selected)`；
    - **第五拍踩过 ②hover 被抹（更隐蔽）**：改后的基态 `:not(...)` 是 (0,2,0)，与 DS 的
      `.giencoder-menu-item:hover` (0,2,0) **打平且文档序在后** ⇒ **四枚下拉 + 右键菜单 hover 全无**
      （真鼠标悬停 `matches(':hover')=true` 而 `bg` 仍 `rgba(0,0,0,0)`）⇒ 判据**必须用真鼠标 hover 后读
      `getComputedStyle`**，只看「类名挂没挂上」永远发现不了。
13. ★★★ **「框选不到」先怀疑「它是 CSS 生成内容」** —— `::before`/`::after` 的 `content:` 挂出来的字
    **不是 DOM 的一部分** ⇒ 选区落不进去（`Selection.toString()` 恒空、`caretRangeFromPoint` 退回宿主元素）。
    ★ 本页现存的例子：输入卡下方那行统计文字（r97 ④ 的 `div.mt-8::after`）——第六拍 ⑯ 已改成真节点。
    **判据配方**：① 拖行后读 `Selection.toString()`；② `caretRangeFromPoint` 看 `startContainer` 是不是文本节点；
    ③ ★ **必做隔离对照**（临时建一真一伪两块 DOM，同一次运行里同手法拖选）——否则「探针写错了」无法排除。
    ⚠ 改真节点时宿主是 React 的地盘 ⇒ 见下条。
14. ★★★ **往 React 渲染的容器里注入真节点 ⇒ 必须 `MutationObserver` 兜两件事**：
    ① 重渲染会把不认识的节点**摘掉**；② 重挂时 React 把自己的子节点插到**末尾**，我们要**再挪回末尾**
    （否则注入的节点会跑到 React 的节点**之前**，版面顺序错）。回调里只做「判存 + 不是最后一个就
    `appendChild`」⇒ 自己造成的 mutation 再进一次回调时判存即返回，**天然收敛**。
    实例 = `panel.js` 的 `statsBoot()` / `statsSync()`（观察 `document.body` 的 `childList + subtree`）。
15. ★★ **React 行内 `style` 写死的尺寸，只有 `!important` 能改** —— 例：技能选择浮窗行内
    `width:760`。⚠ 别只提特异性，行内样式优先级最高。
    且要在**正确的包含块**下换算：该浮窗的包含块是输入卡（`position: relative`）⇒ `100%` = 输入卡内宽。
16. ★★ **判「容器变窄要不要自适应」的判据 = 容器可用宽，不是视口分辨率**（右栏开合 / 左导航收拢都会改它）
    ⇒ 一律写 `min(原值, 容器宽)`，天然跟着容器走（同 ④b 的 `.r93-bub`）。
    改完必须**在窄档复量**：1440 全绿不代表 1280 / 1100 也全绿（第六拍两条都是窄档才暴露）。
17. ★★★ **给右栏加「与既有控件同构」的新件 ⇒ 一律换独立类名**（r108）：`ctrl-conv.js` 的 `pane` 是**整个 `aside.td-browse`**、`.td-browse-files` 用 `querySelector` **只绑第一棵** ⇒ 抽屉树用 `td-tf*` 才不打架（判据 = 操作抽屉后老模块的 `active` / `rows` / `hidden` 计数**一字未变**）。
18. ★★ **覆盖层会挡住它自己的触发器** —— 抽屉 `z-index:35` 的遮罩铺满面板 ⇒ 探针里想点工具条上的 `⋯` **必须先关抽屉**（否则点到遮罩、把抽屉关掉），否则会把「切并排视图失败」误判成 bug。
19. ★★ **带派生高度的新规则必须补 `var(--font-size-*)`** —— `.td-tree-h` 有 `height:calc(40px*ratio)` 但体里无 token ⇒ 被 `apply88b.converge()` 压平、`scan-flatten` 多报 1 条 ⇒ 补 `font-size: var(--font-size-body-3)` 回基线 2 条。

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
    ⚠ **★ r101 ③ 已改回** `background: var(--color-fill-2)`、**不要边框**（`box-shadow:none`）——此处以 r101 为准；
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

#### P3.11g ⑪ r101 十一条（会话详情页 · 2026-09-30）—— ★ **r93 代已提交 ⇒ 新建 `mg-work/r101/apply101.py`**

* **载体 / 注入块 id 换代**：`r93-conv-css|js` + `r93-nav-js` → **`r101-conv-css|js` + `r101-nav-js`**；
  脚本用 **`GENS` 逐代摘除表**（r93 + r101 一起摘、注入用本代 id）——细则见 **PLAYBOOK P3.32①**。
  ★ **页面级 CSS 选择器一个字未改**：`ATTR_HOST='r93-conv-host'` / `ATTR_PAGE='data-r93-page'` **跨代沿用**。
* **本页新增/修改的固定事实**：
  * `.r93-fh:hover` / `.r93-fc:hover` = **`background: transparent`**（**不再铺浅灰底**）；
    `.r93-fc:hover, .r93-fc:hover .r93-c3, .r93-fc:hover .r93-t14 { color: var(--color-text-1) }`、
    `.r93-fh .r93-cv { color: var(--color-text-1) }` ⇒ hover 只提前景色。
  * `.r93-t12l` 补 `color: var(--color-text-3)`（②「浅两级」= text-3，**DS 每级跨两个色阶**）；
    ⚠ 「深度思考」正文（`.r93-t12l` 无 `-fm`）因此由 text-1 变 text-3 —— **是主动下调，不是还原设计稿**
    （设计稿该处主笔画实测 **(31,31,31) = text-1**）。
  * `.r93-t12l.r93-fm.r93-ell, .r93-sumrow .r93-t12l { font-size: calc(13px * var(--ui-fs-ratio)) }`
    ⇒ 全页 `.r93-t12l` 直方图 **`{13px:17, 14px:1, 15px:1}`**（两个例外：「深度思考」正文 14px 由 `.r93-card` 钉死、
    「任务产物」标签 15px 由 `.r93-artlabel` 定）。
  * `.r93-ib:hover` = `background: var(--color-fill-2)`、**无边框**（覆盖 P3.11g ⑨ 的白底 + 内描边）。
  * `.r93-iblk.r93-cv > svg { width:10px; height:10px }` —— **只缩 svg，槽仍 14×14**（`slotW=14px` / `svgW=10px`）；
    这是为了保住 r99⑧「折叠前后零跳动」（实测 `dx=0`）。
  * `.r93-sb { box-shadow: 0 2px 9px rgba(0,0,0,0.07) }` —— **不是 DS token**：设计稿实测峰值 Δ≈11、10px 收干，
    DS `--shadow1-down` 强一倍以上 ⇒ 自造档（Σ\|Δ\|=3）。
  * `.r93-tbsticky::after`（新增）= 40px `linear-gradient(to bottom, transparent, var(--color-bg-2))`、
    `bottom:-44px`、`z-index:-1` ⇒ 滚动口底部渐隐；**挂 `.r93-tbsticky` 而非给 `.r93-scroll` 加 mask**
    （mask 是祖先级绘制效果，会把「滚动到底部」药丸一起淡掉）。
  * `.r93-ctx.giencoder-dropdown-submenu-popup { position:fixed }` + `.r93-ctx .giencoder-dropdown-submenu{position:relative}`
    + `.r93-ctx .giencoder-dropdown-arrow{...14×14}` —— ★ **本页产物里没有子菜单的编译样式**
    （conversation/task-detail 都查不到 `.giencoder-dropdown-submenu*`）⇒ 自补 3 条 `r93-` 适配层，**未改组件本体**。
  * `.r93-spin { animation: r93-spin 1.2s linear infinite; transform-origin: 50% 50% }`（「压缩上下文」图标常转；
    只要 hover 转 ⇒ 去掉类名即可）。
  * `.r93-pane { position: relative }` + `.r93-sk*`（骨架屏遮罩 z=9，复用 DS `giencoder-skeleton-line/-title/-avatar`，
    内层 `.r93-sk-in{width:calc(50% + 10px); min-width:860px}` 与内容列同宽同轴）。
* **⑦ 右键菜单**（「任务产物」）。**打开方式▸6 项** 子菜单的 13 枚 svg 直接从
  `mg-work/r69/part-ctx.js` 抽取（`load_ow_icons()`：线条 7 + 品牌 6 = 18,345 字符，数量不符即 `sys.exit`）——
  **别手抄**。菜单本体仍走 `.r93-ctx*` 适配层。
* **⑪ 骨架屏的时序**：`wire()` 里 `setTimeout(1100)` 加 `.is-out`、再 320ms 移除；
  ⚠ 1.1s 窗口 **CLI 截图抓不到**（`open` 本身耗时 ≈1~2s）⇒ 目视取证只能临时改大延时再还原（PLAYBOOK P3.32④）。
* ⚠ **验收 hover 类需求必须带 `matches(':hover')` 读数**（PLAYBOOK P3.32②）；本页三个 hover 目标已实测 `hov=true`。

#### P3.11h r101 第二批七条（同代就地返工 · 2026-09-30 19:50）—— ★ **本页现在的「浮层几何」变了**

⚠ **最重要的一条**：`.r93-bar` 从「`.r93-pane` 的流内兄弟」改成 **`position:absolute` 浮在滚动口之上**
（宿主 `.r93-conv-host` 补 `position: relative`）⇒ 本页所有「相对 pane 定位」的浮层都要按新基准重算：

* `.r93-bar { position:absolute; top/left/right:0; z-index:10; height:44px; background: var(--r93-glass);
  backdrop-filter: blur(12px) }` —— **毛玻璃标题栏**。`z-index:10 > .r93-sk 的 9` 是刻意的
  （原来标题栏在 pane 之外、骨架屏盖不到它，进 pane 之后必须压上去才能保住「加载中页头可见」）。
  底色走新变量 `--r93-glass`（浅色 `rgba(255,255,255,0.72)` / 暗色 `rgba(35,35,36,0.72)`，**无设计稿依据**）。
* `.r93-scroll { padding-top: 44px }` —— 与标题栏高度**成对**：不补这一档，首屏内容会整块上移 44px 钻到毛玻璃底下。
  补上后**静止态与改前逐像素一致**（实测真实内容首块仍 `[420,125,…]`），只有滚起来才看得到区别。
* `.r93-sk-in { padding: 76px 0 0 }`（= 44 + 32）—— 骨架屏的定位父级仍是 `.r93-pane`，跟着上移了 44px ⇒ 一起补。
* `.r93-sk-card { margin-top: 20px }` —— 原来那块**浅灰容器**（`--r93-card` 圆角底 + 12px 内距）**已撤**
  （第二批 ③）；3 条灰条现在与上面 3 条正文条同左缘（x=420）。
* `.r93-tbsticky::after` 高度 **40 → 56px**（第二批 ④，底边仍 `-44px`）⇒ 渐隐带 = 滚动口最下 56px。
  ⚠ 层级仍是「滚动内容 < 渐隐层 < 药丸」（A/B 裁片 `raw/r101-fadeab-crop.png` 可证药丸依旧清晰）。
* `.r93-fc .r93-fchev` —— 折叠头**右端的 hover 箭头**：复用子菜单那枚 `fright` 图标，
  **常驻占位 + `opacity` 淡入**（`display:none→flex` 会挤动标题）；基态带 `translateX(-2px)` 滑入
  ⇒ **间距要在 hover 态量**（父级 `gap:4` + `margin-left:4` = 8px；基态量到的是 6px）。
* `@keyframes r93-fold-in` + `.r93-fold[data-open='1'] > .r93-fb { animation: … .34s cubic-bezier(.34,1.56,.64,1) both }`
  —— 展开回弹（display 开关天然重播）；`.r93-cv` 过渡换同曲线。**收起刻意不动画**（理由见 PLAYBOOK P3.33⑤）。
* **菜单只剩一张**：第二批 ⑤ 把 r99 ⑦ 那张 `.r93-drow` 专用 4 项菜单**整段退役** ⇒
  汇总行右键 / 左键 / 「⋯」三处全接产物卡的 FMenu（6 项 + 「打开方式 ▸」6 项）；
  `runF('path')` 的名字来源 = `data-r93-artname` → `data-r93-file` 回落。**全页 `.r93-ctx` 恒 1 个**。

**★ 本页新增的「块级」注入**：`<style id="r101-hdr-css">` —— `header[class*="h-12"] { background-size: 70% }`
（压 r92 代的顶栏装饰图块）。**落 6 页**：base / conversation / avatar / skills / automation / settings
（= 所有带 `r92-hdr-css` 的页面）；研发工作台 4 页（dev / kanban / req-kanban / task-detail）本来没铺这张图 ⇒ 未动。
⚠ 注入/摘除的开关在该脚本里写作 `hdr_patch()` / `hdr_unpatch()`（`'r92-hdr-css' in text` 当判据）。

⚠ **本页首屏所有折叠块都是展开态**（`foldClosed=0`）⇒ 要验折叠头样式（hover 箭头、`.r93-fc` hover 色）
必须先**真点击一次**把某块折叠，`querySelector('.r93-fold[data-open="0"] > .r93-fc')` 首屏恒为 `null`。
⚠ **毛玻璃标题栏会接住点击**：滚动口最上 44px 的内容点不到 ⇒ 自动化取证用 `agent-browser click` 时要先
`scrollIntoView({block:'center'})`（否则目标被滚进那一条带，点击落在标题栏上、`eval` 读不到菜单）。

---

#### P3.11g ⑫ r102 十一条（会话详情页 · 2026-09-30 20:4x）—— ★ **r101 代已提交 ⇒ 新建 `mg-work/r102/apply102.py`**

> 完整版见 `mg-work/r102/acceptance.md`；脚本内 5 条新教训见 PLAYBOOK **P3.34**。

**① 体位**：r101 代**已提交**（`9f252e5`）⇒ 本代**新建脚本**，注入块 id 换代
`r102-conv-css` / `r102-conv-js` / `r102-nav-js`；`GENS` 逐代摘除表扩到**三代**（r93 / r101 / r102）。
★ `HDR_ID` **保持 `r101-hdr-css` 不换名**（顶栏图 70% 本轮无改动）；`RAWI_DIRS` **三级回落**；
宿主 `r93-conv-host` / `data-r93-page` 跨代沿用 ⇒ **页面级 CSS 选择器一字未改**。

**② 十一条**（实测见 acceptance 第一节；此处只记「本页固定事实」）：

| # | 落地 | 本页新固定事实 |
|---|---|---|
| ① | `.r93-t14` 字号 **15 → 13px** + 数字滑入动效（`.r93-num` odometer-lite） | 全页 `.r93-t14` 直方图 **`{13px:58, 14px:6}`** —— **卡内 6 处仍 14px**（被 `.r93-card.r93-card *` (0,2,0) 钉住，本规则 (0,1,0) 压不进去，**不是 bug**）；数字包出 **13 个 `.r93-num`**，`animation: r93-num-in .46s cubic-bezier(.22,1,.36,1) both`、`delay calc(1.5s + var(--r93-ni)*55ms)`（`--r93-ni` 按**每个 `.r93-t14` 内部**从 0 计） |
| ② | `.r93-fc .r93-fchev` 间距 **8 → 4px** | 靠父级 `gap: 4px`（箭头自身 `margin-left: 0`）⇒ 标题右缘 → 箭头左缘 = **4px** |
| ③ | **折叠收起补动效**（`max-height` 过渡） | `.r93-fb { margin-top:12px; max-height: var(--r93-fbh, 4000px); overflow:hidden; transition: max-height .32s cubic-bezier(.4,0,.2,1), margin-top 同曲线, opacity .26s ease }`；`.r93-fb.is-free { overflow: visible }`；`[data-open='0'] > .r93-fb { max-height:0; opacity:0; margin-top:0 }`。**删掉了原 `display:none` 分支** |
| ④ | `.r93-t12.r93-nm` **12 → 13px** | 2 处（改动汇总表头） |
| ⑤ | `.r93-iblk.r93-cv > svg` **10 → 12px** | 槽仍 `14×14`、`n=14`（覆盖 P3.11g ⑪ ④ 的 10px） |
| ⑥ | 折叠头 / 展开头 **hover 时 meta 也变正文色** | `.r93-fh:hover .r93-fm, .r93-fc:hover .r93-fm, .r93-fh:hover .r93-t12l, .r93-fc:hover .r93-t12l { color: var(--color-text-1) }`（`text-3 rgb(134,134,134)` → `text-1 rgb(31,31,31)`） |
| ⑦ | `.r93-asst` 底边线**浅一级** | `--color-border-2` → **`--color-border-1`**（`rgb(229,229,229)` → `rgb(242,242,242)`）⇒ **撤销 r99 ⑬** |
| ⑧ | `.r93-drow` padding → **`0 16px`** | 原 `0 13px 0 11px`；文件名左缘相对卡 = 16、「⋯」右缘 13 → 16；`gap: 17px`、行高 36 不变 |
| ⑨ | `.r93-dhead` 左内距 12 → **16px** | 原 `6 6 5 12` → **`6px 6px 5px 16px`**；图标槽相对 16；表头 40px 定高不变 |
| ⑩ | 「滚动到底部」药丸 → **毛玻璃** | `.r93-tobottom { background: var(--r93-glass); -webkit-backdrop-filter/backdrop-filter: blur(12px); border:1px solid var(--color-border-2) }`；**新增 hover 档 `--r93-glass-h`**（浅 `rgba(255,255,255,0.86)` / 暗 `rgba(35,35,36,0.86)`，**自造、无设计稿依据**）—— 原 hover 底色 `--color-fill-1` 不透明，一 hover 毛玻璃就没了 |
| ⑪ | `.r93-seg…radio-group-button` 总高 **28px** + 标题栏内**垂直居中** | `.r93-seg .giencoder-radio-button { height:26px; **min-height:26px**; padding:0 12px; border-radius:5px }` —— 1+26+1 = **28px**；`top:8px` 不动 = `(44−28)/2` ⇒ 基线「上 8 / 下 2」偏心一并修掉 |

**③ 两条与既有记录冲突的更正**：
* 本页 `.r93-seg` 的 **DS `min-height` 从未被覆盖**（一直顶 32px）⇒ 任何改本组件高度的需求，
  必须 `height` + `min-height` **两条一起改**（见 PLAYBOOK P3.34①）。
* P3.11h 里「**收起刻意不动画**」这条**已被 r102 ③ 推翻** —— 现在收起有动画了（靠精确 `--r93-fbh`）。

**④ 未闭环（待邵先生拍板，见 acceptance 第五节）**：`-m` / `-b` 变体仍 15px；数字动效覆盖全部
卡外数字串（含正文数字）；基础延迟 1.5s；`--r93-glass-h` 无设计稿依据；`.r93-fb` 常驻 `overflow:hidden`
（展开稳定后靠 `.is-free` 放行，将来新增「需长期溢出」的浮层会被裁 360ms）。

---

#### P3.11g ⑬ r103 六条（会话详情页 · 2026-09-30 20:5x）—— **就地返工**（r102 未提交）

> 完整版见 `mg-work/r102/acceptance.md` 的 **r103 段**；两条机制级教训见 PLAYBOOK **P3.35**。

**① 体位**：r102 **未提交** ⇒ 仍改 `mg-work/r102/apply102.py`，注入块 id **不变**（`r102-conv-*`）。
产物 `conversation.html` 683044 → **685465**（+2421）；`base.html` **472150（+0）**。

**② 六条**（本页固定事实）：

* ① **`.r93-t14` 回 15px**（**撤销 r102 ① 的字号部分**；数字动效 `.r93-num` 保留）。
  实测直方图 `{13:58,14:6}` → **`{15:58,14:6}`**（卡外 58 全 15；卡内 6 仍 14，被 `.r93-card.r93-card *` 钉住）。
* ② `.r93-t14.r93-ell`（35 处）与 `.r93-t14.r93-c1`（2 处）**全 15px** —— 这两个类**本身不含 font-size**
  （`.r93-ell` 只管截断、`.r93-c1` 只管颜色）⇒ 随 ① 自动生效，**没有第二条规则**。
* ③ 「滚动到底部」药丸**再透一档**：新增 `--r93-glass-pill`（浅 `rgba(255,255,255,0.60)` /
  暗 `rgba(35,35,36,0.60)`）与 `--r93-glass-pill-h`（0.74）。**标题栏仍走 `--r93-glass`（0.72）不动**。
  ⚠ 原来药丸与标题栏**共用** `--r93-glass` ⇒ 想单独调药丸必须新开变量。
* ④ **`.r93-agents` 那一行（4 张 agent 卡）整行退役**，连 `.r93-cp` 容器一起从 `TPL_BOTTOM` 摘掉。
  `.r93-bottom` `{y:593,h:112}` → **`{y:653,h:52}`**（子元素只剩 `.r93-sb`）；底部整块**上移 60px**。
  ⚠ 相关 CSS（`.r93-agents` / `.r93-agent*` / `.r93-cp`）**保留未删**：删掉会让
  `--r93-a1-bg…--r93-a4-bg` 变成「未使用的本地变量」、可能给门禁添新告警。要恢复只需把 TPL 那段贴回。
* ⑤ **底部对话框激活态的外发光顶部被截断 —— 已修**。真凶**不是** `overflow`，是**绘制顺序**：
  宿主 `.r93-conv-host` 在 r101 加了 `position: relative`（给毛玻璃标题栏当包含块）⇒
  它由「in-flow flex item（按 order-modified 顺序绘制）」变成「positioned descendant（按**树序**绘制）」，
  而它是 `appendChild` 追加的、排在 hero 之后 ⇒ **宿主画在 composer 之上**，盖掉那 3px 光。
  修法 = hero 补 `position: relative !important; z-index: 1 !important`（见 PLAYBOOK P3.35①）。
* ⑥ **折叠块开合两态统一 + 修闪动**：撤掉 `@keyframes r93-fold-in` 与 `[data-open='1'] > .r93-fb`
  那条**单向 animation**，改由 `.r93-fb` 的**四条 transition** 承担
  （`max-height` / `margin-top` / `opacity` 各 0.32s 标准曲线 + `transform` 0.34s back-out 回弹；
  收起态补 `transform: translateY(-8px)` 做镜像）。`setFold` 改
  「本帧 `refreshFbh` → `requestAnimationFrame` 里翻 `data-open`」。
  实测：14 块 `animationName !== 'none'` 的**数量 = 0**；收起 `opacity` 逐帧连续 `1→0.993→0.737→…→0`；
  展开 `transform` 末段超调 `+0.779px` 后落定 0 ⇒ **两态镜像**。

**③ 与既有记录的冲突更正**：
* P3.11g ⑫ 里「`.r93-t14` 13px」**已被 ① 撤销** —— 现在是 **15px**。
* P3.11h 与 P3.11g ⑫ 里关于「折叠收起」的描述以 ⑥ 为准（现在是 transition，且**没有 keyframes**）。
* `check-syntax` 的 `style=16` **不是回归**（HEAD 同口径也是 16）。

**④ 未闭环（r103 新增 2 条）**：③ 透明度取 0.60（想更透可一行调）；④ 摘行后状态条↔composer
之间为 44px 空档（= 12px 下内距 + 外壳 `div.mt-8` 的 32px），觉得松可再压。

#### P3.11g ⑭ r104 四条（会话详情页 · 2026-09-30 22:0x）—— **就地返工**（r102 + r103 均未提交）

> 完整版见 `mg-work/r102/acceptance.md` 的 **r104 段**；两条机制级教训见 PLAYBOOK **P3.36**。

**① 体位**：仍改 `mg-work/r102/apply102.py`，注入块 id **不变**（`r102-conv-css` / `r102-conv-js` / `r102-nav-js`）。
产物 `conversation.html` 685465 → **691648**（+6183；LF `sha 05b899bd4366`）；`base.html` **472150（+0）**。

**② 本页新增的固定事实（四条）**：

* ① **宿主 `.r93-conv-host` 现在是 `position: relative; z-index: 0`**（r104 新增 `z-index: 0`）。
  ⚠ **它与 hero 的 `position:relative; z-index:1` 是「成对」的**：hero 那条是 r103 ⑤ 为修外发光加的；
  宿主这条是 r104 ① 为把浮窗从 hero 的层叠上下文里「解放出来」加的。
  **单独改任何一条都会让另一个问题复发** —— 动之前先读 PLAYBOOK **P3.36①**。
  副作用（有意为之）：**宿主内元素不再能压到 hero / composer 之上**。
* ② **底部对话框（外壳 React 渲染的 `div.mt-8` 一行）首帧是隐形的**：
  `opacity: 0; pointer-events: none` 为默认，由 `<html data-r93-app="ready">` 放行。
  放行由注入 JS 在 **1100ms**（与骨架屏退场同一拍）写入，**刻意独立于骨架屏节点是否存在**。
  ⇒ 排查「对话框不出现」时，先查 `document.documentElement` 的 `data-r93-app`。
* ③ **页签状态是三处属性协同**（`r93SetTab()` 是唯一入口，`host.__r93tabId` 是防连点真相源）：
  `data-r93-app`（`null`→`ready`）× `data-r93-tab`（`chat` ⇄ `trace`）× 每个 pane 的 `data-r93-slide`
  （`out-l` / `out-r` / `in-l` / `in-r`，凭空出现/消失由它承载）。
  **只有 `ready + chat` 才显对话框**；轨迹页另把 hero 置 `display: none`（宿主 `flex:1 1 auto` 顺势长高）。
  ⚠ **`.r93-pane` 在消息列 `TPL` 里也有一份** ⇒ 滑动规则的 CSS 选择器**必须带 `>`**
  （`html[data-r93-page='conversation'] .r93-conv-host > .r93-pane`），否则会误伤消息列。
* ④ **折叠块开合点击委托没有缺陷**（`host` 上的事件委托 → `setFold`）。
  r104 全页 **14 块开合往返 `scrollHeight` 逐块比对 = 14/14 OK**（含嵌套块 #10 的实时重算）。
  ⚠ 若探针报「点不动」，先怀疑**标签选择器命中多个元素**（见 PLAYBOOK P3.36④），不要先改代码。

**③ 代码审查留下的痕迹（r104 ④）**：`audit104.py` 六组扫描 → **采纳 7 项**。
其中与本页固定事实有关的：
* `.r93-fold` 的开合属性现在是 **`data-r93-open`**（**不再是裸 `data-open`**，全页 23 处已命名空间化）——
  **写新探针/新规则时用 `data-r93-open`**。
* `:root` 里新增 `--r93-sh`（`0 4px 8px 0 rgba(0,0,0,0.08)`）与 `--r93-sbsh`（`0 2px 9px rgba(0,0,0,0.07)`）
  两条阴影变量；`--r93-warn-ic` / `--r93-ok` / `--r93-ioc2` 三点改为 `rgb(var(--orange-7))` /
  `rgb(var(--green-7))` / `rgb(var(--gray-7))`（**计算值不变**）。
* **暗色档已补 3 条**：`--r93-ioc: rgb(var(--gray-10))`（原 `#333333` 压在 `#232324` = **隐形图标**）、
  `--r93-dim: rgb(var(--gray-4))`、`--r93-tag-ic: rgb(var(--orange-6))`。
* **已删除**：僵尸变量 `--r93-blue` / `--r93-sb` / `--r93-glass-h`；**agent 死代码一族**
  （`.r93-agents` / `.r93-agent*` / `.r93-a*` 共 20 条规则 + 15 个变量，≈2.3 KB）。
  ⇒ **`.r93-agents` 那一行的 CSS 已不存在**（r103 ④ 只摘了 DOM）；要恢复该行**必须连同这套 CSS 一起写回**。

**④ 与既有记录的冲突更正**：P3.11g ⑬ 里「`.r93-agents` 相关 CSS **保留未删**」**已被 r104 ④ 推翻** —— 现在**整族已删**。

**⑤ 未闭环**：r104 **无新增待拍板**。r103 遗留 2 条（③ 药丸透明度 0.60、④ 摘行后 44px 空档）仍有效。

#### P3.11g ⑮ r105 三条（会话详情页 + 8 个独立页 · 2026-09-30 23:0x）—— **就地返工**（r102/r103/r104 均未提交）

> 完整版见 `mg-work/r102/acceptance.md` 的 **r105 段**；四条机制级教训见 PLAYBOOK **P3.37**。

**① 体位**：仍改 `mg-work/r102/apply102.py`，注入块 id **不变**（`r102-conv-css` / `r102-conv-js` / `r102-nav-js`）；
新增静态片段目录 **`mg-work/r102/part105/`**（`browse.css` / `browse.html` / `browse.js` / `ctrl-conv.js`）。
产物 `conversation.html` 691648 → **793028**（② +2173 → ③ +99207；LF `sha e67474395502`）；`base.html` **472150（+0）**；
**其余 8 页各 +714**。

**② 本页新增的固定事实（八条）**：

* ① ★ **`aside` 里的会话项跳转脚本 `r102-nav-js` 现在铺满 9 页**（base + 8 个独立页），
  `conversation.html` **不自带**（它自己就是目标）。
  ⚠ 判据是**捕获阶段委托** `document.addEventListener('click', …, true)` 里的
  `min-w-0 + flex-1`（会话项）⇒ `location.href = 'conversation.html'`；
  **分组标题（`rounded-md py-0`）/「新会话」按钮必须放行**。
  ⚠ 添加/修改这一块**只能改 `apply102.py` 的 `nav_patch` 一处**，别为单页另开补丁
  （`invert_if_absent` 保证第二遍**一字不动、只保位置**，见 PLAYBOOK P3.37②）。
  ⚠ **哪几页「有对象」是查出来的**：`task-detail` 的壳 `aside` 实为 **`display:none`**（可见左栏是 `.td-left` 任务面板，
  无会话列表）；`kanban`（筛选面板）/ `settings`（设置导航）的 aside 无会话项；`dev` / `req-kanban` **无 `<aside>`**。
* ② ★★ **`.r93-seg` 现在是「DS 官方滑块 + 自绘退位」**：
  容器首子元素 = `<span class="giencoder-radio-button-slider" aria-hidden="true">`（**DS 官方结构**），
  由它承担白底 + 描边（`top/left: 1px`、`height: 26px`、`border-radius: 5px`）；
  `.giencoder-radio-button-checked` 改为 **`background: transparent; border: 0`**（只留文字色 / 字重）。
  ⚠ 容器带 **`data-r93-seg-init="0"`** ⇒ 该态 `transition: none`（**首帧禁动画**，否则滑块从 0 宽「长」出来）；
  JS **两帧后**摘掉该属性。
  ⚠ 几何由 JS `r93SegMove()` 写**行内** `width` / `transform`，
  **四处重定位**：页签 `click` / `document.fonts.ready` / `window.resize` / **`1200ms` 兜底**。
  ⚠ 给这个容器**加子元素或改内距**前先读它的 `display/gap/padding` —— 滑块几何依赖 `offsetWidth` / `offsetLeft`，
  任何内距变化都会被「四处重定位」如实体现在滑块上（这是「设计如此」，不是 bug）。
* ③ ★ **`r93-bar` 右侧两枚按钮 = `.r93-baracts` > `.r93-baract`**（`.r93-morebtn` **已整枚退役**，CSS 活规则 0 条）。
  类名**逐字对齐** avatar 的 `.td-right-acts`：`giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon`
  + 本页前缀 `.r93-baract`。
  ⚠ 适配层**必须写 `border-color: transparent`**（avatar 的 `.td-round-btn` 就是靠它去掉 DS 默认描边）；
  ⚠ **圆角不覆盖**（随 DS 的 **8px**）；⚠ 图标 **14px**（`.r93-iblk.r93-i14`）。
  实测 rect `[1359,57,64,28]`（两枚 28×28 + gap 8，右缘 1431 = bar 右缘 − 8）。
* ④ ★ **全屏开关 = `<html data-r93-full="1">`**（**不是** class、不是 JS 闭包里的布尔）。
  打开时左导航 `aside` 收拢到 0、对话区吃满整行，做法与浏览态**完全同款**：
  `width / min-width / padding-*: 0 !important` + `opacity: 0` + `pointer-events: none`
  （外壳给 aside 的宽度是 React **内联** style ⇒ 必须 `!important`；它自带 `overflow: hidden`）。
  两枚图标**共用一枚按钮**，靠 `html[data-r93-full='1'] .r93-baracts .r93-ico-max / -min` 切显隐
  （选择器**带前缀**是为胜过 `.r93-iblk { display: inline-flex }`）。
  ⚠ **要程序化切全屏，请派发 `CustomEvent('r93:fullscreen', { detail: { on } })`，不要直接改 `<html>` 上的属性** ——
  状态由 r102 主脚本持有（它还要翻 `aria-pressed` / `title` / `aria-label` 并派发 `resize`）。见 PLAYBOOK P3.37④。
* ⑤ ★ **文件预览侧栏 = 数字分身「AV-BROWSE-SLOT v1」整块移植**，落点：
  `hostRow.insertBefore(splitMain, hostMain.nextSibling)` + `insertBefore(slot, splitMain.nextSibling)`
  （`hostRow` = `div:has(> main)`）。
  ⚠ 宽度变量 `--av-browse-w`（**默认 641**、`MIN_PANEL 561`、`MAIN_MIN 380`）；
  ⚠ **记忆 key = `giencoder:r105-browse:v1`**（与数字分身**分开**，别共用）；
  ⚠ 打开态类名 `av-browse-on`；开关按钮 = `.r93-baract[data-r93-browse]`。
* ⑥ ★ **暗色档已补（r105 ③-d）**：源页 avatar / task-detail **没有**本模块暗色分支，本页**必须有**（本页 r93 一族全量做了暗色）。
  `browse.css` 的 **7 个字面 hex 全是自定义属性定义** ⇒ 只覆盖这 7 个、**不动几何**（源件逐字不动 ⇒ 同源校验仍成立）：
  `--td-panel-line: rgb(var(--gray-3))`；`--td-code-key/str/num: #569CD6 / #CE9178 / #B5CEA8`；
  激活行 `rgba(var(--blue-7), .20) / rgba(var(--blue-7), .38)`；`--td-crumb-line: var(--color-border-1)`。
  ⚠ **要动这一块，先读 PLAYBOOK P3.37③**（不补的后果是不可读：代码主色对比度 ≈ 2.0、激活行整块白）。
* ⑦ ★ **Esc 裁决链现在是三级**：右键菜单 → 预览栏 → **全屏**，每级 `stopImmediatePropagation`。
  新加浮层若要参与 Esc，**插在链里的哪一级、以及是否拦下**都要显式决定（别默认「顺延」）。
* ⑧ ⚠ **`.r93-bar` 右侧原先是单枚 `.r93-morebtn`（⋯）且无任何行为** —— 换成两枚真按钮后，
  **`.r93-morebtn` 只可能出现在注释里**；写新 CSS 时别再去给它加规则。

**③ 未闭环**：r105 **三条待拍板**（全屏是否留 12px 抓边窄条 / 预览栏默认宽是否本页另给 720 / 预览栏与全屏是否互斥），详见 HANDOFF 第六节 41~43。

---

#### P3.11g ⑯ r106 六条（会话详情页 · 2026-10-01 08:2x 首拍 / 08:4x 返工 / 08:5x 第三拍）—— ★ **r102 代已交付（`87e2caa`）⇒ 新建 `mg-work/r106/apply106.py`**

> 完整版见 `mg-work/r106/acceptance.md`；机制级教训见 PLAYBOOK **P3.38**（六条）。
> ★ 本代**三拍**（同一代、`apply106.py` 就地返工三次，**始终未提交**）：
> 首拍 ①②③④；**返工拍** = ④ **口径更正** + 新增 ⑤；**第三拍** = 新增 **④b 用户消息块写死 `728px`**。
> 本页暂无新增「独立页」事实（**本代没有旁观页** —— 10 页全写，除 conversation 外均只是 nav 块 id 换代）。

**① 体位**：`GENS` 摘除表 = **四代**（`r93` / `r101` / `r102` / **`r106`**）；`CSS_ID/JS_ID/NAV_ID = GENS[-1][1:4]` ⇒ 自动取 r106。
⚠ **r103 / r104 / r105 从未单独占代**（都是 r102 的就地返工）⇒ **不入 `GENS` 表**。
脚本由 `mg-work/r106/ev/make106.py` 从 `apply102.py` **9 处精确替换**生成（每处命中 ≠ 1 即 `sys.exit`）。
`PART_DIRS` **双目录回退**（`r106/part106` → `r102/part105`）⇒ 三个移植件**沿用 r102 目录、不复制**。

**② 产物（★★ 口径 —— 首版曾算错；⚠ 2026-10-01 11:5x 二次校准）**：`conversation.html` **793028 → 799231 Unicode 字符（+6203）**
（`4d081ba` blob `67b443ca082c`，LF 归一 `sha1 9cdb19501a81`）；`base.html` **472150（+0）**（`3436a5e7857e`）；**另 8 页字符数均 +0**。
⚠ 本节旧记「**798613（+5585）/ blob `e17d227b58bf`**」是**提交前态**（该对象不在库中）⇒ **以 `git cat-file blob 4d081ba:pages/conversation.html` 实测为准**。
★ **三种数勿混用**（同一份文件）★ 校准后：Unicode 字符 **799231** ｜ UTF-8 字节（LF 归一）**870627** ｜ 工作区字节（CRLF）**875328**（= 870627 + 4701 个 `\r\n`）。
⚠ ★★ `len(bytes) − CRLF数` **不是字符数**（本页中文多、会虚高 ~6.8 万）⇒ 判内容增减**先归一化行尾、再比同一口径**（详见 PLAYBOOK P3.38①）。
★ 本仓 **`core.autocrlf=true`** ⇒ 仓库 blob 存 **LF**、工作区落盘 **CRLF** ⇒ `cat-file -s` / `wc -c` **天然差「行数」字节**，**不是内容改动**。

**③ 本页新增的固定事实（六条 + 两条连带）**：

* ① ★ **「上下文注入」「深度思考」默认折叠** = `fold()` 调用加 **`open: false`**（**零 CSS / 零结构**）。
  `fold()` 工厂**本就支持** `data-r93-open` 由 `(o.open === false ? '0' : '1')` 派生。
  实测：14 块里第 ①② 块 `open=0`、**h=22**（y=429 / y=467），**其余 12 块 `open=1` 逐块不变**。
  ⚠ `wire()` **只给「初始就展开」的块挂 `.is-free`**（放行卡内 popover）⇒ 收起态本就不挂。
* ② ★ **`.td-browse-bar` 高 44px**（与 `.r93-bar` 同高）= 本页适配层 **一行** `height: 44px`。
  ⚠ **源件 `part105/browse.css` 一字未动**（那份要与源页 `avatar.html` **逐字节同源**，校验 `ev/extract105.py` 在 r102 目录）；
  理由之二：`.r93-bar` **只存在于本页** ⇒ 没理由让 avatar / task-detail 跟着变高。见 PLAYBOOK P3.38③。
  实测两条栏 **h=44 / 44**、底线**同落 y=92**（改前 browse 40 / 底线 y=88）。
* ③ ★ **预览栏展开时 `main` 右上角改直角 + 接缝 1px**：
  `main { border-top-right-radius: 0; border-bottom-right-radius: 0; border-right-width: 0 }`。
  实测半径 `10px 10px 10px 10px → **10px 0 0 10px**`、`border-width → **1px 0 1px 1px**`；
  接缝**非白像素 2 → 1**（改前 x=790 `#ECEEF2`＝main 右框 + x=791 `#E5E5E5`＝面板左框；改后**只剩 x=791 `#E5E5E5`**）。
  ⚠ **那条线归面板** —— 面板左边线是设计稿**专门为「与 AI 会话栏接缝」另取的一档**（`part105/browse.css`「第 52 轮第 3 项」注释）。
  △ Tailwind `border` 按 **border-box** ⇒ `border-right-width:0` **只让内容盒宽 1px、边框盒仍 779** ⇒ 元素位置与拖拽手感不变。
* ④ ★★ **预览栏展开时内容列「空间不足才自适应、空间足够保持原逻辑」**（★ 返工拍口径更正；首版曾写成**无条件撑满**）：
  `.r93-wrap { width: min(calc(100% + 20px), max(calc(50% + 10px), 860px)); min-width: 0; margin: 0 calc((100% − 宽) / 2); }`
  ★ **1440 开 = 778**（left 13、`overRight 0`）；**2560 开 = 949**（left 488、居中 = 原逻辑）；**关态 860 / 1141 逐像素不变**。
  ⚠ **判据是「容器可用宽」而非视口分辨率**（预览栏开/关、左导航收拢都会改它）⇒ 别用 `@media` 断点。
  ⚠ **不能用 `margin: 0 auto`**：撑满时元素宽 > 包含块，`auto` 在溢出方向会退化成 0（实测原逻辑 `mL 0 / mR −102` 不对称）
  ⇒ 必须显式 `calc((100% − 宽) / 2)`（撑满时正好 = −10px）。
  ⚠ `.r93-wrap` 的 `50%` 基数比 `.r93-bottom` **少 20px**（父盒 `.r93-scroll` 带 gutter）⇒ 页内既有约定用 `+10px` 补偿、**不可省**（否则四列不同宽）。
  ⚠ **必须同时 `min-width: 0`** —— 原规则的 `min-width: 860px` 会把 `min()` 结果顶回去。
  ⚠ 原逻辑实测（`ev/p106e.js` 把覆盖摘掉读真值）：1440 开 **860**（右缘 883 > main 右缘 791 ⇒ 溢 92px = 「遮挡」）、2560 开 **949**。见 PLAYBOOK P3.38⑥。
* ④b ★★ **用户消息块 `.r93-bub` 写死 `width: 728px` → `min(100%, 728px)`**（★ 第三拍新增）：
  * **定位法**（邵先生只给了一个数「固定的 728px」）：① 先量他点名的 `.r93-wrap` —— 1440 关 860 / 开 778 / 1370 开 708 /
    1280 开 618 / 1920 开 860 / 2560 关 1141，**没有一档是 728** ⇒ 排除；② **全页扫描「宽度 700~760」的元素** ⇒ 揪出
    `.r93-bub` / `.r93-bubi` / `.r93-attrow`×2 / `.r93-umeta`，**四档情形一律 728**；③ **全仓 grep `728px`** ⇒ `pages/*.html` 里**仅此一处**。
  * **原规则**：`.r93-bub { margin-left: auto; width: 728px; display: flex; flex-direction: column; }`（r93 段「用户消息」）。
    蓝底气泡本体 **`.r93-bubi` 就宽 728**（`BG=rgb(229,237,254)`）。
  * **症状**：块 **右对齐** ⇒ 内容列窄于 728 就**向左溢出被裁** —— **1280 开（列 618）溢 110px**
    （气泡文字断在「…三个泳道，未」，chip 被切）、**1370 开（列 708）溢 20px**。
  * **改法**：`html[data-r93-page='conversation'] .r93-bub { width: min(100%, 728px) }` ⇒ **≥728 的 7 档全仍 728（逐像素不变）**，
    只有「列 < 728」才跟列收（618 / 708、溢出 0）。
  * ⚠ **唯一不带 `.av-browse-on` 的一条**：溢出只看「列 ↔ 728」的大小关系，**窄窗口关态同样会溢**。
  * ⚠ **1440 下不可见**（列 778/860 都 ≥728）⇒ 验它必须到 **1280 / 1370 开态**（`raw/m106b-1280-open.png` 是改前对照）。
  * ▲ `margin-left: auto` **保留**（列够时维持右对齐；列不够时 `width` 取 100%、`auto` 退化成 0 ⇒ 满行）。
    原规则**非 `!important`、特异性 (0,1,0)** ⇒ 本页适配层 **(0,2,1)** 压得住，**无需 `!important`**。
    `.r93-bub` 的父盒 `.r93-it` 是 `display:block` ⇒ **块级子元素 `min-width:auto` 本就是 0**，不用补 `min-width`。
* ⑤ ⚠ **连带三处同口径**（`.r93-bottom` / composer 外壳 / `.r93-sk-in`）：
  它们的父盒**没有 gutter** ⇒ 口径 = `min(100%, max(50%, 860px))`（+ `min-width: 0`）；
  **composer 外壳**原规则自带 `!important`、特异性 **(0,3,6)** 更高 ⇒ 靠 `html[data-r93-page='conversation'] .av-browse-on`
  前缀提到 **(0,5,6)** 才压得住，**同写 `!important`**。
  ⚠ `.r93-sk-in` 原式 `calc(50% + 10px)` 是按「有 gutter」写的、而它父盒**没有** ⇒ 会宽出 10px，本轮顺手对齐内容列。
* ⑥ ★ **产物卡文件名「默认不该是蓝、hover 才是」**（★ 返工拍新增）：
  模板对第 2 张卡（`spec-template.md`）写了**内联** `style="color:var(--color-primary-6)"` ⇒
  内联优先级最高，把 CSS 里「`.r93-artname` 默认 `text-1` / `.r93-artcard:hover .r93-artname` 才 `primary-6`」整条压死。
  **修法 = 只删那处内联**（连数据里的 `1` 一并去掉），CSS **一行未动**。
  实测：未 hover 时 5 张卡文件名全部 `rgb(31,31,31)`（`--color-text-1`）、`inline=(none)`；
  真鼠标 hover 第 2 张 ⇒ `rgb(55,112,247)`（`--color-primary-6`）；其余 4 张仍 text-1。
* ⑦ ⚠ **`.td-browse-bar` / 预览栏三件套的暗色档已在 r105 补好**（7 个自定义属性）；本代**未再动**。
  暗色实测：接缝 `rgb(78,78,78)`、面板底 `#17171a`、main 底 `#232324`。

**④ 三档同构 + 窄档 + 四查**：1440 / 2560 / 暗色 三档下 ①`open=0 h=22`、②`44/44`、③`10 0 0 10` + `1 0 1 1`、④**开 778 / 关 860**（2560 开 949 / 关 1141）**全部一致**；
**第三拍加验窄档** 1280 开 / 1370 开 的 ④b = **618 / 708**（跟列收、溢出 0）；
**开态与关态下 wrap / bottom / composer 三列同宽同左缘**（r97「全宽块等宽」保住）。
幂等 ✓（**三拍各连跑两遍**，第二遍双「已是目标态」）｜`mg-work/check-syntax.py` **10/10 通过**（conversation `script=9 style=16`）｜
`verify-design.py ./pages` 与 `ev/vd-r101e.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`；`vd-r106c.txt` 同 md5）⇒ **零新增**｜
代数核对：`r106-conv-css` / `r106-conv-js` 各 1（base 的 `r106-nav-js` 1）、**10 页历代别名零残留**。

**⑤ 🚫 状态**：**未提交**（r106 属新一轮，与已交付的 `87e2caa` 分开）；等邵先生发话。
