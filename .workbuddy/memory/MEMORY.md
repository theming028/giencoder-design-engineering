# GienCoder 项目记忆索引

> **≤3.5K 字节**（超了会被截断注入 ⇒ 白写）。按需 grep，别整读：
> **`HANDOFF.md`** ★开局先读（状态/待办/接手，每轮覆盖）｜ **`PLAYBOOK.md`** 铁律/自检/取证/git（P3.21=r88｜P3.22=r89~r91 小图标网格｜P3.23=r92 改压缩 React 源 + 装饰背景图｜**P3.24=r93 字号特异性反噬 / 设计稿变体叠放 / ui-component 无字号 / 独立页 + 纯 CSS 复用外壳真组件**｜**P3.25=r94 内容盒守恒 / 「用户说的容器」未必是血统所在 / 门禁会扫注释**｜**P3.26=r95 「右侧撑满」= 固定宽改流式 / 滚动条占宽会让同页多列不同轴**｜**P3.27=r96 设计稿「HTML 导出」= 样式权威源 / 改工具类默认色先枚举使用点 / 别把相邻元素宽度当线宽**｜**P3.28=r97 ★`width:N%` 的基数=父盒（窄视口测不出）/ `*` 不贡献特异性 / 「等宽」先分清 A 列宽一致 vs B 每块满宽**）
> ｜ **`PAGES.md`** token/各页事实/配方（**P3.11b 全局字号（含 r93 反噬）**｜P3.11c DS Select｜P3.11d 已归档任务｜P3.11e 顶栏背景图｜P3.11f 设置页 r92｜**P3.11g 会话详情**（r93 ④ 后 = 独立页 `conversation.html`；**r94~r106 续改，共 ⑨~⑯ 八节**）｜**P3.11h 页面路由表 / 新开一页范式**｜**P3.11i 会话详情「侧栏模块标签化」= 复刻 Codex 右栏（r107 · 共十拍：三段式+五模块 / 浮窗关不掉 / 删侧聊 / 摘要升默认+卡片式·划词浮条·右键菜单·tab 14px·下拉 DS 化 / **下拉 hover 补齐 + 下拉改挂 DS Dropdown（从 Menu 族改正）** / **统计行「伪元素 → 真节点」（可框选）+ `.r93-pre` 去字体族 + 技能浮窗与 `.r93-alert` 随内容列自适应** / **右栏竞品名全换 GienCoder + 菜单标题行与快捷键隐藏 + 选中项补底色 + 提交卡输入框拉通 + 右栏字体统一 + 全屏按钮随右栏联动** / **全局宽度不足出省略号（三类分治）+ 去掉「折叠此文件」+ `.td-sum-h` 15px + diff path 展开中粗 + diff path/rows 内 13px + 统计行居中** / **全屏按钮图标随态切换（MAX⇄MIN）+ 全屏态拖拽起点修正（读实际几何）+ 拖拽与收起联动退全屏 / **三枚 `.td-rv-menu` 改为按触发器现场摆位（原跑到按钮上方 34~36px）**）**）｜ `YYYY-MM-DD.md` 原始日志
> ｜ **续**：**P3.29=r98** 门禁对注释双重标准 / `:first-child` 撞装饰件 / `font:` 重置 shorthand｜**P3.30=r99** 图标 `transform="matrix"` 雷区 / 弹层量测时机 / DS 实例图标手写｜**P3.31=r100** 设计稿 HTML 丢实例底色 / hover「逐字照做」/ 层级连接线 / `!=null` 判空｜**P3.32=r101** 上一代已提交时新一代怎么接（`GENS` 逐代摘除）｜**P3.33=r101 第二批 七条**｜**P3.34=r102** `min-height` 顶更稳 / 同帧写变量+改属性会被合并 / hover 断言要选不被遮挡的目标｜**P3.35=r103** 加 `position` 会改绘制顺序 / `animation` 移除不触发 transition｜**P3.36=r104** 正 `z-index` 封顶后代浮窗（与宿主 `z-index:0` **成对**）/ 首帧守卫写进 CSS 默认值｜**P3.37=r105** 加动效前先查「官方实现是否已内联」/ 扩块到多页用 `invert_if_absent` 保位置 / 移植到有暗色分支的页必须补暗色档 / 更晚注册的脚本走自定义事件｜**P3.38=r106（六条）** ★★ **`core.autocrlf=true` ⇒ 工作区字节 ≠ 仓库 blob 字节；且 `len(bytes)−CRLF数` 不是字符数（判内容先归一化行尾、再比同一口径）** / 改通用部件「初始态」先 grep 工厂有没有现成开关 / 移植件的几何适配走**本页适配层**（源件逐字节不动保同源校验）/ ★★ **上限型 clamp `min(可用宽, 原逻辑式)`：原式整段照抄别换算、别忘 `min-width:0`、`margin:auto` 在溢出时不对称** / `border-width:0` 在 border-box 下**只缩内容盒**（≠「元素变宽 1px」）
> ｜**P3.39=r107（第一~三拍 · 十二条）** ★★★ **跨代沿用的宿主标记不换名 ⇒ 换来「只改一页」** / 新模块 section 类名别与内部件撞车 / 绝对定位先查包含块 / Esc 挂 `window` 捕获段 / 组装件+生成器改序只能下→上 / 浮窗关不掉先查**搜索根** / ★★★ **`converge()` 会把 `line-height:calc(Npx*ratio)` 压成裸 px**（带行高的规则 `font-size` 必须写 token）/ 互斥态两条 `display` 特异性必须错开 / 探针三类假失败 / `verify-design.py` 会数渐变｜**P3.40=r107 第四拍（五条）** ★★★ **页面级通配适配层会扫到新挂 DS 类的弹层**（`html[data-r93-page=…] .giencoder-select-popup{top:auto!important;bottom:…!important}` 把右栏下拉全翻到锚点上方 ⇒ **只量样式属性看不出、必须量 `getBoundingClientRect()`**）/ ★★★ **`!important` 连行内 `style.top/left` 也压得过** ⇒ JS 定位浮层改走**自定义属性 + `!important` 规则** / 给 DS 条目做兜底**务必 `:not(...)` 提特异性**（否则抹掉选中态底）/ 「过渡中取值」假失败（打开与量测拆两次 `eval`）/ 「自绘→DS 组件」= 删自绘视觉、只留定位+槽位，开合兜底留页面级｜**P3.41=r107 第五拍（六条）** ★★★ **「挂错组件族」比「没挂组件」难发现**（字面核查全过、要**枚举 `components/*.json` 契约**：`menu`=导航 / `select`=选择器 / **`dropdown`=弹出菜单（含右键）才是正主**；且「DS 有没有某组件」要查**页面内联 bundle**（`giencoder-dropdown-popup` 在页面 53 处、在 DS 源 0 处））/ ★★★ **同特异性 + 文档序 ⇒ hover 被静默压掉**（P3.40③ 第四次犯；**判据必须「真鼠标 hover + 读 `getComputedStyle`」**）/ DS 骨架 **entry 动画播完把 `opacity` 打回 0** ⇒ 复用弹层前先 `grep` 它的 `animation` / **换族会让页面级连带副作用自行消失**（换完要重审旧适配）/ **换族 = 选中态表达重新协商**（Dropdown **无** `-selected` ⇒ 按契约用「主色字 + 勾选图标」，不虚构底色）/ 迁移自检要**剥掉 CSS 注释**再查残留｜**P3.42=r107 第六拍（三条）** ★★★ **「这段文字框选不到」先查它是不是 `::after` 的 `content`（CSS 生成内容不是 DOM）**（判据三条：拖选后 `Selection.toString()` 恒空 / `caretRangeFromPoint` 退回宿主 DIV 且 `offset 0` / `Range.selectNodeContents(宿主)` 少那一段；★ **隔离对照**：临时建 `#zzA::after` vs `#zzB` 真文本、同一次运行同一手法一比即定 —— 别先怀疑探针）+ 修法「同选择器关伪元素 + 注入真节点」，**宿主是 React 就得 `MutationObserver` 收敛**（回调只做「判存 + 不在 `lastElementChild` 就 append」⇒ 自收敛；⚠ 别拿 `<textarea>`/表单控件当对照） / 行内 `style` 写死的宽只有 `!important` 压得住（`width: min(760px, 100%) !important`，`100%` 基数 = 最近定位祖先进卡） / 定高容器改 `height:auto; min-height:原值; padding:原内距` 时 **竖内距要挑到「单行态完全等价」的值**（否则单行宽度也会变）｜**P3.43=r107 第七拍（六条）** ★★ **「渲染出来的字」与「渲染不出来的字」要分开判**（渲染成文字的必改 / 外链 `href` **不改**（替换域名段即 404、且不渲染）/ 历代**设计来源注释保留**；★ 顺手 `grep -i` 扫**别的页** —— 本拍在 `avatar.html` 又挖到 1 处；★ 自己新增的注释要避开被清理的词）/ ★★ **同一处改动先判「节点从哪来」：静态 HTML vs JS 现场生成**（菜单标题行 = `.td-mm-cap`（写死的）+ `.td-ctx-head`（`ctxBuild()` 里建的）⇒ 删 HTML 治不全 ⇒ **一段 `display:none` 把两类一起关**，column flex 里塌行不占位、与删节点视觉等价）/ ★ **DS 组件「宽度不拉通」先查它自己的 `display`**（`.giencoder-input-wrapper` 编译样式 = `inline-flex; width:auto` ⇒ 同卡别的行 308、它只有 207；修法 = **写双类** `.giencoder-input-wrapper.td-commit-in{display:flex}`，不赌文档序）/ ★★ **「统一字体族」要分清「本代自己的样式」与「跨代沿用的移植件」**（自己那 8 条就地改；「文件」模块代码区那条在 **r102 代已交付的 `part105/browse.css`** 里 ⇒ 页内**多一级类数覆盖**（`.td-browse .td-browse-pre`），153 个 `.td-code*` 靠继承；★ **这条是「改完第一遍量出来才补的」⇒ 判据要覆盖整棵子树，别只验自己改过的那些选择器**）/ ★★ **联动显隐先量「状态类挂在哪一级」**（`.av-browse-on` 实测挂在 shell flex 行 = `main` 与预览栏的共同父级 ⇒ **纯 CSS 可判**，省掉一整个 MutationObserver；⚠ 只写要隐藏的那一枚，别用 `.r93-baracts` 整组）/ 跨页文案替换的锚点用**带引号的整串**（不碰同名注释、天然幂等）+ **写回必须 `newline=''` / 走二进制**（本仓页面 CRLF，默认 `'w'` 会把整页翻成 CRLF ⇒ 内容没变却全变 `M`）｜**P3.44=r107 第八拍（六条）** ★★★ **「全局都要出省略号」这类「全局」需求先给对象**分三类**（单行文本⇒截断 / **代码·终端**与**多行正文**⇒保持折行、**不截断**；★ **容器自带 `display:flex / inline-flex` 时裸文本是「匿名 flex 项」** ⇒ 容器上的 `text-overflow` 对它无效） / ★★★ **「居中」改不动 ⇒ 先查「谁在管这个 `width`」**（`.r107-stats` 的 `fit-content + margin:auto` 被页面级两条 `!important` 盒宽规则**压死**；第一步用注入 `min-width:0` / `width:100%` **反证**看盒宽动不动；正解 = `text-align:center`；★ **真节点 ≠ 伪元素**：`::after` 是 shrink-wrap、真节点在满宽盒里默认靠左，`margin:auto` 会偏 32px；**判据 = `Range.selectNodeContents` 取「文字真实盒」的中心**） / ★★ **幂等补丁的「已应用」判据（mark）必须是「只有改后才存在」的串**（删列表中间一项时 mark 选了改前就有的邻接行 ⇒ **静默跳过**；**同一选择器改多稿别逐版字符串匹配** ⇒ 用「按选择器定位 + 找首个 `\n}\n` 作块尾 + 整块替换」） / ★★ **写进代码注释里的实测结论必须来自截图取值，不能凭「应该是这样」**（曾把「居中 + 溢出不落省略号」写反；实测是对齐**退化为 `start`**、省略号照落行尾） / **15px 无 token 档位 ⇒ 写 `calc(15px * var(--ui-fs-ratio))`**（裸 px 会被 `converge()` 压平） / **改字号改容器无效**（子规则各自写死了字号 ⇒ 逐条同值覆盖，且只换 token 档位以保住行高派生链）｜**P3.45=r107 第九拍（两条）** ★★ **宿主「绕过控制器直接写布局变量」⇒ 内层缓存必然脱节**（拖拽起点读缓存 ⇒ 一按下就跳回记忆宽；**第一帧读实际几何，且先停过渡再取 rect 才是终值**） / ★★ **拖拽 `pointermove`/`pointerup` 必须挂 `window`**（挂元素 + `setPointerCapture` 平时能跑、贴边/重挂即断；★ **判据配方 = 把 move 派发到 `document.body`** 看还响不响应） / **改跨代移植件走「本代同名覆盖件」**（`PART_DIRS` 顺序回退；⚠ 副本会漂移，头部写明来源与差异） / **别用 `MutationObserver` 盯「后插节点」的父级**（会绑在旧父级、永不触发；**搭已有确定性事件流** —— 如「收起必定 dispatch 一次 resize」） / **「独占态」要把退出路径列全**（按钮 / 拖拽接管 / 容器收起），退出用 **silent 变体**（只改状态不动尺寸）｜ skill（用户级）：design-to-code-modular / svg-icon-pixel-grid / css-state-pixel-evidence / **compiled-bundle-jsx-patch**

## 一、环境（Windows）

- 页面**全自包含**（CSS/JS 内联、图 base64），**无 `serve.py`**；预览 **`file://` 直开**。
  ⚠️ 内置预览 URL **不带 hash** → 壳错误；⚠️★ `file://` 下「改前基线」**文件名必须与原页面同名**。
- Python = `python`（Pillow/numpy 齐）。agent-browser（**不在 PATH**，走绝对路径，v0.27.0）=
  `C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js`
  （用 `C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe` 跑）。
- ⚠️★★ `set viewport`→`open`→`eval/click/screenshot` **整条链同一次调用**；**同时只允许一条链路**（并发必串味）。
- ⚠️ Windows 无 `/tmp`；沙箱 heredoc 吞反斜杠 ⇒ 复杂脚本用 Write 落盘；单行 bundle 上正则量词**必须有界**；
  `getComputedStyle(el)['--x']` 恒 undefined ⇒ 用 `getPropertyValue`；探测脚本避开 `sc`/`reg`/`wsl`（安全策略）。
- ★ 设计稿取数：PNG 首选 `GET http://127.0.0.1:30678/api/getScreenshot?…&scale=2`（**必须 GET+query**，POST 400；
  ⚠ 只回**当前画布选中**节点）。回退：MCP `get_screenshot` 传**裸 ID**；`get_selection_node` 只认**完整 goto 链接**。
  ⚠️★ PNG 是 **RGBA**：未绘制处 `alpha=0` → `convert('RGB')` 变**纯黑** ⇒ 先 `alpha_composite` 白底。
  结构树 `text/title` 是未展开 DS 实例 ⇒ 常常没文案，只能读图。（端口：MCP 20678 / 截图 HTTP 30678，细则见 PLAYBOOK P7）

## 二、五条硬规则

1. **改页面一律走 `mg-work/rNN/applyNN.py`**：体位「先 `strip_all(当前页)` 取净底 → 再注入」⇒ **改完直接重跑即自愈**；
   跑两遍验幂等。回滚 `cp mg-work/rNN/before/<page>.html pages/`。
   **例外**：上一轮未提交时的即时返工 ⇒ **就地改原补丁，不另起代数**（判据 `git status` 仍是 ` M`）。
2. **断言只允许**：① 标签级计数（`<style></style><script></script>`）**精确增减量** ② 被改对象的精确计数。
   禁「全文件关键词总数不变」；**新增注释里不得出现被断言的 token / 标签名**。
3. **改前先问范围**：同名同构模块多页各有一份，先用 DOM 核实现状再动 —— 用户对"擅自改未指明对象"极敏感。
4. **幂等脚本别把自己注入的块一起 `unscale`** ⇒ 会**永久损毁**块内无法重派生的声明（尾风 `line-height`、裸 `min-height`），
   而**「跑两遍 sha 不变」照样通过**（损毁发生在第一遍）！用 `converge()` + **逐条断言注入内容**（PLAYBOOK P3.20③）。
5. **收尾四件套**：`check-syntax.py pages/<页>`（JS 语法 + CSS 配平）→ `verify-design.py ./pages`（**必须传目录**）
   → 与 **HEAD 基线同口径**逐条归一化 diff（汇总数相同 ≠ 零影响）→ 覆盖更新 `HANDOFF.md`。
   跑完清理 `git checkout -- pages/gaps.log` + `git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`。
   ⚠ HEAD 里那份 `gaps.log` 常是**陈旧产物** ⇒ 必须同口径复跑再定性。

## 三、速记

- **禁止整文件 Read `pages/*.html`**（单行 bundle 340–830 KB）→ 只打印目标片段。本机 `grep` 查中文一律空 ⇒ 用 Python 读。
  ⚠ `pages/*.html` 是 **CRLF**：`ls`/`wc -c` = 含 CRLF 字节数，Python 文本模式转 LF ⇒ 字符数与字节数差异大，**勿混用**。
- ★★ **「可选子部件」一律判空**：`querySelector(…)` 拿不到时 `.addEventListener` 会抛 TypeError，
  冒泡出构建函数 ⇒ **整页白屏而且页签/导航都正常**（r88 踩过：DS select `noClear` 时的清空钮）⇒ 先 `if (el)`。
- ★★ **拖拽的 `pointermove/up` 挂 `window`（不是元素）** + `blur` 兜底：`setPointerCapture` 失败时挂元素会让
  `dragging` 永卡 `true`（之后划过就误拖）。命中层要够大（r88：1px 轨道 → 252×36 整块），装饰子元素 `pointer-events:none`。
- ★ **给 DS 组件加子元素前先读它的 `gap`**（`.giencoder-select-view` 自带 `gap:8px` ⇒ r88 文字右偏 9px）。
- ★ **设计稿取数 scale = 2.0**（画板整数尺寸直接定死，曾误用 2.011）；圆角只能靠「渲染候选 + SSD 拟合」定（DS 无 7px 档）。
- ★ **复用控件前先 grep 组件类名** —— 页面 bundle 里**早已内联 DS 全套组件 CSS**，照
  `giencoder-design-system/preview/component-<name>.html` 的官方 DOM 搭。⚠ 动态创建的元素要改 JS 侧类名。
- ★★ **按钮一律挂 DS Button 类名，禁自绘**（邵先生 r90 定为**全局强制性要求**）：`giencoder-btn` + 变体
  （`-secondary`/`-primary`/`-danger`/`-text`/`-icon` + `-size-small|default|large`）；适配层**只补几何 + DS 没有的语义色**。
  ⚠ 先查 **`r73-radius-css`** 全局块 ⇒ 圆角口径是 **large 8px / small 4px**，**别按设计稿压 6px**；
  ⚠ DS 基类自带 `border:1px solid transparent`（占 2px）⇒ 凑整数宽时内距减 1；⚠ 变化态高度**只写 `min-height`**（见 PLAYBOOK P3.22⑤）。
- ★★ **1px 描边的图标，中心线必须落 `x.5`/`y.5`**（整数中心线 ⇒ 1px 摊成两列各 50% 灰 ⇒ 又细又虚）；
  推论：**要左右对称且清晰，图形外沿尺寸必须偶数**（PLAYBOOK P3.22①）。
- ★★ **改 DS 组件要动三处源**：`components.css`（主源）+ `gienx-templates/_shared/components.css`
  （**模板层副本，极易漏**）+ `pages/*.html` 内联副本 + `components/<slug>.json` 契约；**改完全仓 grep 断言零残留**。
- ★★ **全站字号杠杆 = `--ui-fs`**，**不是 `html{font-size}`**（外壳用尾风 **px** 类不是 rem）。
  ⚠ `--ui-fs` **只允许在 `:root` 声明一次**；覆盖规则加 `body` 前缀。
- ★ **外壳（React）渲染的元素**（如 `<aside>`）源码里搜不到 ⇒ `!important` 压内联 `style.width` + 捕获阶段拦事件。
- ★ **改前/改后对照图用元素截图**（`screenshot "<sel>"` 自动裁到边界 ⇒ 同原点）；全页截图会因滚动/外壳高度整体位移。
  ⚠★★ **元素截图「超出视口的部分会渲染成空白」** ⇒ 截图前**必须** `set viewport 1440 900` 且 `eval window.innerHeight` 核对
  （r90 因此跑出 7.478% 假差异，真值 1.562%）。
- ★★ **在元素截图里取色，坐标 = 元素内相对坐标**（原点 = 元素左上角，不是视口）⇒ 先 `eval` 打 `el.rect − 容器 rect` 的差值。
  「无底/透明」的判据 = **取到的像素 == 容器自身底色**（aside = `#F4F5F6`）；量化「底色一致」= 同坐标三态**逐通道相等**（PLAYBOOK P3.22⑦）。
- ★★ **同一控件里图标要比文字浅一档 ⇒ 把 `color` 下移到 `> svg`**，别改按钮的 `color`（那会连文字一起改）。
  反证：逐行 diff 里「被 hover 的那一行」不该出现差异（该态 svg 已 `display:none`）。
- ★★ **想给 React 渲染的元素加新色 ⇒ 后置 CSS 有俩盲区**：① 尾风**任意类**是构建期产物（新增 `[color:var(--x)]` **不会进产物 CSS**）；
  ② **内联 style** 优先级最高。出路只有两条：挂**自定义类**（自己写样式）或**改 React 源**（三目里塞 `var(...)`，内联里用 `var()` 合法）。
  改源用幂等 `replace_once`（`mg-work/r92/apply92.py` 头部可抄）；⚠ 锚点三目加档要**保括号**：`X?A:B` → `新条件?新值:(X?A:B)`。
- ★★ **`inject_tail` 别断言 `count('</body>')==1`**：`base.html` 的 CSS 注释里也出现过一次 ⇒ 用 `rfind` + 距文件尾 <80 字符判定。
- ★★ **裸 `header` 标签选择器会误伤**（avatar 5 个 / task-detail 4 个 `<header>`）⇒ 外壳顶栏用 `header[class*="h-12"]`。
  ⚠ **探针先枚举再取值**：`.ws-dropdown-hover` 在 base.html 有 **2 个**（工作目录 / 默认权限），取第一个会得到「自洽但全错」的读数。
- ★ 装饰背景图**先量素材**（尺寸/平底/平底占比/点径点距/alpha）再定铺法；素材**不透明且平底 ≠ 元素底色** ⇒ 必留接缝（位置 = 元素宽 − 素材宽）。
- ★★★ **设计稿导出图里「状态变体是叠放的」**（r93）：同一折叠块容器内同时叠「折叠态」+「展开态」⇒
  **真机块高 = 容器高 − 变体偏移**（r93 恒 34，逐块固定不累积），**导出 PNG 的绝对 y 不可当设计坐标**；
  容器 top 的**差**（12/16/24）可直接信。⚠ 症状 = 实机每块恰好少同一个恒定值。见 P3.24②。
- ★★ **字号机制层 `body .cls`（0,1,1）会反噬**任意值工具类 `.leading-[32px]`（0,1,0）（r93 真 bug）⇒
  正解两步：**让位**（size 类行高加 `:not([class*="leading-"])`）+ **补齐**（`leading-[Npx]` 补同特异性派生、写在 text-\* 之后）。见 P3.24①。
- ★★ **`ui-component` 是不带 font-size 的纯框** ⇒ 字号靠「框高 × PNG 墨迹行距 × 文本宽度反推」**三角验证**（单看框高会把 12/20 误判成 14/22）；
  **私有区图标字符（U+F0xxx）实机无字形** ⇒ 变豆腐块并改折行；**字体度量差异会改折行数** ⇒ 用 `min-height` 保卡高。见 P3.24③④⑥。
- ★ **暗色适配**：新画面里字面 `#FFFFFF` 一律换 **`var(--color-bg-2)`**（浅 `#fff` / 暗 `#232324`，浅色视觉零变化）；
  其余设计稿实测色提页面级 `--rNN-*` 变量并**补一整份 `[giencoder-theme='dark']` 档**（r93 踩过 11 处白底 ⇒ 暗色白屏）。见 P3.24⑤。
- ★★ **本工程 `pages/` 下每页都是「完全自包含的独立 html」**（顶栏 + aside + 外壳各一份，**无共享布局、无真实路由**）⇒「某视图要不要独立成页」先看每页内嵌的 `ROUTE` 表（10 份逐字相同 + `hashchange`）；
  **新开一页 = 由源页净底重建**（**不复制**）+ 换根级 `data-rNN-page` + **全页 `ROUTE` 各 +1 条**。见 PAGES P3.11h。
  ⚠ 复用「外壳真实组件」= **纯 CSS 改视觉顺序**（宿主 `order:-1` + hero `justify-end` 贴底 + 问候语/页脚 `display:none`），**不给 React 源动刀、不抄 HTML**；
  ⚠ 钉在 `overflow:hidden` 容器底部的真组件，其**弹层要翻向** `top:auto; bottom:calc(100% + 4px)`（含 `%` ⇒ 不会被 `unscale()` 改坏）。见 P3.24⑦。
- ~~旧：改容器宽度先看「内容盒」~~（**已被下面 P3.26/P3.28 取代**）：
  ⚠ **用户说的「某容器内」的元素未必在该容器里**（r94：`div.mt-8` 内无波点，真源是 `main.dot-bg`）⇒ **先跑血统探针**；
  ⚠ **门禁会扫注释里的 CSS 关键词**（注释写 `radial-gradient` ⇒ `verify-design` 计数 +1）⇒ 注释别写字面关键词。见 P3.25。
- ★★ **「某某右侧要撑满」= 固定像素宽改流式**（r95 定论，**取代**上面的"内容盒守恒"）：子块写 `width:100%`、
  留左缩进就 `calc(100% - 18px)`，容器 padding 只留纵向 ⇒ 右侧自动顶满；**底部列 / 对话框外壳要一起改成同口径**
  （`.r93-bottom` 与 React 外壳都给 `width:50%; min-width:860px`）。
  ⚠ **`overflow` 容器的滚动条会占宽** ⇒ 同页「有滚动条的列」与「无滚动条的列」各自 `margin:auto` 居中会**差半个滚动条宽**
  （r95 实测 5px ⇒ 三组元素三条右边界打架）⇒ 用 **`scrollbar-gutter: stable both-edges`** 让内容恒同轴。
  ⚠ **不是所有同类卡片都要撑满**（右对齐的气泡 / 按内容宽左对齐的 agent 卡 ⇒ 不动）。取证 = 以锚元素右边界算 Δ，**全 0 才算过**。见 P3.26。
- ★★ **`width:N%` 的基数 = 父盒**（r97 定论）：同一页里「内容列 / 底部列 / 复用来的真组件」若**父盒不同宽**
  （滚动内容盒 vs pane vs 带 `px-*` 的 hero 子盒），`50%` 算出来**不是同一个数** —— 1440 下被 `min-width` 兜住看不出来，
  **视口一宽就露馅**（2560 实测输入卡比状态条**两端各短 12px**，用户原话「两端都短了一截」）。
  ⇒ **凡百分比定宽的元素必须测两个视口**（1440 + 2560）比右边界；修法优先**清掉父盒横向内距**（不引魔数），
  次选 `calc(50% + Δ)`（Δ 依赖滚动条宽时**先钉死** `::-webkit-scrollbar{width:10px}`）。见 P3.28。
- ★★ **`*` 通配符不贡献特异性**（r97）：`.r93-card *` 其实是 **(0,1,0)** ⇒ 会被**写在它后面**的同级规则反超
  （实测 37 处变 13px、唯独 5 处 `.r93-pre` 仍 12px）⇒ 类名写两遍 **`.a.a, .a.a *`** = (0,2,0)；**别用 `!important`、别靠挪到块末尾**。
  推论：`::after`（纯 CSS）是「给 React 容器补一行文案」的最优解 —— 挂在 `flex-col items-center gap-2` 上即天然居中且吃 gap。
- ★★ **门禁 `verify-design.py` 对注释行是「双重标准」**（r98 定论）：`check_hardcoded_hex` 命中注释会 `continue` **跳过整行**，
  但 **`check_hardcoded_px_fontsize` 没有任何注释豁免** ⇒ **新增注释里写被断言的 token 字面量会让计数 +1**
  （r94 踩 `radial-gradient`、r98 踩裸字号写法，两次都从 76 跳到 77）。⇒ **写注释时不得出现任何会被扫描的字面量**（字号 px / hex / 禁用关键词），
  举例改用措辞（「裸字号写法」「十六进制字面色」）。报「多 N 条」时**先在 HEAD 基线同口径复跑**再定性。见 P3.29①。
- ★ **`first-child` / `last-child` 会撞容器里的装饰元素**（r98）：`.r93-dlist` 首子元素是装饰滚动条 `<i class="r93-dsb">`
  ⇒ `.r93-drow:first-child` 永不命中（首行仍带边线）。⇒ 遇装饰子元素时**降级为 `:first-of-type` / `:last-of-type`**，
  并把装饰件挪到「不参与计数」的一端。见 P3.29②。
- ★ **`font:` 是重置型 shorthand，后写者胜**（r98）：`.r93-bt{font:inherit}`（写在后面）与 `.r93-t12` **同为 (0,1,0)**
  ⇒ 把同特异性的字号类压掉（「任务完成，耗时28m12s」一直被撑成 14px）。⇒ 修法 = 在 shorthand **之后**补一条同特异性规则，
  **不动 shorthand 本身**；字号真假用**墨迹宽反推**（160px ≈ 11 汉字 + 5 半角 @12px）。见 P3.29③。
- ⚠ 大文件（500KB 单行 bundle）上 `difflib.SequenceMatcher` 会跑到 **SIGTERM** ⇒ 用「摘已知注入块 + 公共前缀/后缀」定位窗口（等价更强断言）。
- 新知识**先进 `PLAYBOOK.md`/`PAGES.md`**，本文件只在"每次都必须知道"时才加一行。
- 🚫 默认**禁止自动 commit / push**（2026-09-28 起）：干完只汇报改动清单，推送由邵先生发起，
  走 `-c credential.helper=store -c http.proxy=http://127.0.0.1:7890`（env 的 `https_proxy` 对 github 稳定 502）。


- ★ **设计稿的 HTML 导出会丢掉 DS 实例「自身」的底色与圆角**（r100 定论，P3.17/P3.30 同族第三个面）：
  看起来「有底、有圆角」的小件（r100 的说明文字行 = 浅灰胶囊）在 `design-*.html` 里只有一个
  `ui-component` 的 `width/height/display`，**既无 `background` 也无 `border-radius`**。
  ⇒ 这类元素**只能回 PNG 逐像素扫**：按行扫非白像素定盒 → 按墨迹定内距 → **盒中心像素值回 token 表找同值档位**
  → 角部灰度剖面对表反解圆角（`inset(dy)=r−sqrt(r²−(r−dy−0.5)²)`，取值锚 token 不锚拟合值）。见 P3.31①②。
- ★ **hover 类需求「逐字照做，别顺手多撤」**（r100 定论）：用户点名「边框颜色不要变」就**只撤 `border-color`**，
  底色照旧；「底色变浅灰即可」就只加底色、边框照旧。**没被点名的属性默认保持原样**；
  两种读法都成立的，写进汇报让用户一句话定。见 P3.31③。
- ★ **画层级连接线**（r100）：「绝对定位伪元素不算 flex item」⇒ 挂在列向 flex 容器上的 `::before`
  必须写 `position:absolute` 才不会被当成 flex item 挤走兄弟；**画线的职责要放在共同祖先**
  （别留在某个子列表上，否则子块接缝处断线）；嵌套折叠块**复用同一个工厂函数**才不会两态错位。见 P3.31④。
- ★ **「0 是合法值」的数值参数一律用 `!= null` 判空**（r100）：`o.mt ? …` 会把 `mt:0` 当假值，
  内嵌层悄悄退化成默认 16px 上边距。见 P3.31⑤。


> **r101 ~ r105（2026-09-30 同日）**：`r86~r100`（`d7e2151`）、**`r101`（`9f252e5`）**、
> **r102 十一条 + r103 六条 + r104 四条 + r105 三条（`87e2caa`）** —— **全部已提交推送**，工作区**干净**。
> r103~r105 当时都是「未提交期就地返工」（仍改 `mg-work/r102/apply102.py`，注入块 id 不变、不另起代数）；
> **`r102` 代已交付 ⇒ 此后会话详情页的新改动要新建 `mg-work/r106/apply106.py`**。
> **r105 三条** = ① `r102-nav-js` 扩到其余 8 页（任一点会话任务 ⇒ 跳 `conversation.html`）② `.r93-seg` 改用 **DS 官方滑块**拿滑动动效
> ③ `r93-bar` 右侧换「全屏」+「打开侧栏」（= 数字分身 `td-right-acts`；侧栏 = AV-BROWSE-SLOT 三件套移植，key `giencoder:r105-browse:v1`）。
> 终态：`conversation.html` **793028**（sha `e67474395502`）｜`base.html` **472150（+0）**｜其余 **8 页各 +714**。
> 同批 `README.md` 已更新（补 `conversation.html` = 第 10 页 / 跳转条目 / 目录结构 / 工作方式 / 版本）。
> 新增定论见 PLAYBOOK **P3.32~P3.37**；各轮操作要点见 **PAGES P3.11g ⑪~⑮**；逐条实测见 `mg-work/r102/acceptance.md`（r102/r103/r104/**r105** 四段）。
> 🚨 **推送坑（r105 更正）**：本机 **`env …` 开头的命令会被「静默吞掉」**（exit 0 + 零输出 + 不执行，连 `GIT_TRACE` 都不打）
> ⇒ 推 GitHub **裸调 `git`**、**不要套 `env -u https_proxy …`**（当日 `env | grep -i proxy` 本就无命中）。详见 PLAYBOOK P5。
> ⚠ 历史尾注：r99 十四条见 P3.30 / PAGES ⑨；r100 八条见 P3.31 / PAGES ⑩（`transform` 雷区 / 弹层量测时机 / DS 实例图标手写）。

> **r106（2026-10-01 08:2x 首拍 / 08:4x 返工 / 08:5x 第三拍 · 会话详情页六条）—— 已提交 `4d081ba`（2026-10-01 09:4x 邵先生发话）**：
> ★ **体位**：r102 代已交付 ⇒ **新建 `mg-work/r106/apply106.py`**；`GENS` **四代**（r93/r101/r102/**r106**）；
> ⚠ **r103/r104/r105 从未单独占代 ⇒ 不入 `GENS` 表**。脚本由 `ev/make106.py` 从 `apply102.py` **9 处精确替换**生成
> （每处命中 ≠ 1 次即 `sys.exit`，不手抄 169 KB）。`PART_DIRS` 双目录回退（`r106/part106` → `r102/part105`）。
> ★ 本代**三拍**（同一代、`apply106.py` 就地返工三次、**交付前始终未提交**）：首拍 ①②③④；
> **返工拍** = ④ **口径更正** + 新增 ⑤；**第三拍** = 新增 **④b 用户消息块写死 `728px`**。
> **六条** = ① 「上下文注入」「深度思考」默认折叠（`fold()` 加 `open:false`，**零 CSS / 零结构**）
> ② `.td-browse-bar` **40 → 44px**（本页适配层一行，**源件 `part105/browse.css` 一字不动**、同源校验仍成立）
> ③ 预览栏展开时 `main` 右上/右下**改直角** + **接缝 1px**（`border-right-width:0`，**那条线让给面板**）
> ④ **内容列「空间不足才自适应、空间足够保持原逻辑」**（★ 口径更正；首版曾写成无条件撑满）：
> `.r93-wrap { width: min(calc(100% + 20px), max(calc(50% + 10px), 860px)); min-width: 0; margin: 0 calc((100% − 宽)/2); }`
> ⇒ **1440 开 778**（left 13、不溢出）/ **2560 开 949**（居中 = 原逻辑）/ **关态 860 / 1141 逐像素不变**。
> ④b **用户消息块 `.r93-bub` 写死 `width: 728px` → `min(100%, 728px)`**（★ 第三拍新增，**不带 `.av-browse-on`**）：
> 全仓唯一 `728px`；块 `margin-left:auto` **右对齐** ⇒ 列窄于 728 就**向左溢出被裁**（**1280 开列 618 溢 110px**、
> 1370 开列 708 溢 20px）⇒ 改后 **618 / 708 跟列收、溢出 0**；**≥728 的 7 档全仍 728、逐像素不变**。
> ⚠ **1440 下不可见**（列 778/860 都 ≥728）⇒ 验它必须到 **1280 / 1370 开态**。
> ⑤ **产物卡文件名默认不蓝、hover 才蓝**（★ 返工拍新增）：删模板里那处**内联** `style="color:var(--color-primary-6)"`，CSS 一行未动。
> **产物（★★ 口径 —— 首版曾算错（更正一）；2026-10-01 11:5x 二次更正）**：`conversation.html` **793028 → 799231 Unicode 字符（+6203）**（`4d081ba` blob `67b443ca082c`，LF 归一后 `sha1 9cdb19501a81`）；⚠ 原记「**798613 / blob `e17d227b58bf`**」经复核是**提交前态**（该对象已不在库中，`git cat-file` 报 `Not a valid object name`）⇒ **引用 r106 数值一律以 799231 为准**；
> `base.html` **472150（+0）**；**另 8 页字符数均 +0**（仅 nav 块 id `r102-*`→`r106-*` **等长换名**）⇒ **本代 10 页全写、没有旁观页**。
> ⚠ ★★ **三种数勿混用**：Unicode 字符 **798613** ｜ UTF-8 字节（LF 归一）**869581** ｜ 工作区字节（CRLF）**874274**；
> `len(bytes) − CRLF数` **不是字符数**（中文占多字节，会虚高 ~6.8 万）⇒ 判内容增减**先归一化行尾、再比同一口径**。
> **四查**：幂等 ✓（三拍各两遍）｜`check-syntax` **10/10 通过**（`script=9 style=16`）｜`verify-design` 与 `ev/vd-r101e.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜代数残留 **0**。
> ★★ **新增定论见 PLAYBOOK P3.38（七条）**（**`core.autocrlf=true` + 字节≠字符** / 改通用部件初始态先查工厂开关 /
> 移植件几何适配走本页适配层 / **上限型 clamp `min(可用宽, 原逻辑式)` 且别用 `margin:auto` 居中** / `border-width:0` 只缩内容盒 /
> ★★★ **用户只给一个数时「数字 → 元素」反查，别按类名字面改**）；
> 各条要点见 **PAGES P3.11g ⑯**；逐条实测见 **`mg-work/r106/acceptance.md`**。
> **待拍板 4 条**：折叠范围（下方 12 块仍默认展开；要不要「凡折叠块默认收 / 连 tool call 内嵌层一起收」）｜
> `r93-bar` 底线 `#EBEBED` 与面板底线 `#E5E5E5` **仍是两色**（本拍只对齐了高度，未统一颜色）｜
> ④ 的「空间足够」判据是**容器可用宽**（不是视口分辨率），若要用 `@media` 断点请发话｜
> ★ **④b 口径**：本代取 `min(100%, 728px)`（列够保持 728）；若要「用户消息块始终与内容列同宽」则是 `width: 100%`（一行改动，但 2560 下气泡会宽到 1141）。

> **r107（2026-10-01 09:3x ~ 13:1x · 会话详情页「侧栏模块标签化」= 复刻 Codex 右栏 · 十一拍）—— **已推送 `e9c9498`**（**已封板**；新一代，承接 r106 `4d081ba`；2026-10-01 14:2x 邵先生发话）**：
> ★ **体位**：r106 代**已交付** ⇒ **新建 `mg-work/r107/apply107.py`**（由 `ev/make107.py` 从 `apply106.py` 做 **13 处精确替换**生成，命中数不符即 `sys.exit`）。
> `GENS` = **五代**（`r93` / `r101` / `r102` / `r106` / **`r107`**）；`PART_DIRS` = `r107/part107` → `r102/part105` 双目录回退。
> ★★★ **本代最关键的决定 —— nav 块沿用 `r106-nav-js`（不换名）**：`GENS[-1] = ('r107','r107-conv-css','r107-conv-js','r106-nav-js')` + `NAV_TAG='r106'`
> ⇒ `apply107.py` 跑完打印「base.html 已是目标态（无改动）」⇒ **全代只改 `conversation.html` 一页**，另 9 页逐字节不变（硬规则「跨代沿用的宿主标记不换名」的收益兑现）。
> ★ 本代**十一拍**（同一代、`apply107.py` 就地返工十一次、**始终未提交**）：① 三段式骨架 + 五模块｜② 浮窗关不掉 / 侧聊对齐｜③ 侧聊全链路删 + 折叠修正 + 对照 Codex 补遗漏｜
> ④ 摘要默认 + 卡片式 + 划词浮条 + 右键菜单 + tab 14px + 全右栏下拉 DS 化｜⑤ hover 补齐 + **下拉换族**（`giencoder-menu` → **DS Dropdown**）｜
> ⑥ 统计行「伪元素 → 真节点」+ `.r93-pre` 去字体族 + 技能浮窗 / `.r93-alert` 随内容列自适应｜
> ⑦ 右栏竞品名全换 GienCoder（含 `avatar.html` 1 处）+ 菜单标题行与快捷键隐藏 + 选中项补底色 + 提交卡输入框拉通 + 右栏字体统一 + 全屏按钮随右栏联动。
> **第六拍三条** = ⑯ 输入卡下方统计小字「**框选不到**」根因是 **CSS 生成内容**（r97 ④ 的 `::after{content:…}`）⇒ 关伪元素 + `panel.js` 注入真节点 `.r107-stats`（+`MutationObserver` 自收敛）；
> ⑰ `.r93-pre { font-family: var(--font-family) }`（**不用 `inherit`**）｜⑱ 技能选择浮窗 `width: min(760px,100%) !important` + `.r93-alert { height:auto; min-height:44px; padding:8px 16px }`。
> **第七拍六条** = ⑲ 竞品名 → GienCoder（右栏**渲染成文字**的 8 处 + 2 处 `title`；三条外链 `href` 与历代注释**有意保留**；另清 `avatar.html` 1 处）；
> ⑳ 菜单标题行（`.td-mm-cap` + JS 的 `.td-ctx-head`）与快捷键（`.td-mm-key` + JS 的 `.td-ctx-key`）**一律 `display:none`**；
> ㉑ 选中项 `.is-checked` 补底色 `--color-primary-light-1`（原只有蓝字 + ✓）+ 提交卡 `.giencoder-input-wrapper.td-commit-in { display:flex }`（207 → 308）；
> ㉒ 右栏字体统一：`panel.css` 8 条就地改 + `.td-browse .td-browse-pre` 覆盖跨代移植件（判据 153 → 0）；
> ㉓ `.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }`（全屏按钮随右栏显隐，纯 CSS）。
> （第八拍产物段已并入下方「第十拍」段 —— 见 PLAYBOOK P3.39 ~ P3.46。）
> **第八拍（六条）** = ⑦ **全局「宽度不够 ⇒ 省略号」**（新增第 14 节，17 类单行文本容器挂三件套；★ **三类分治** ——
> 单行文本 ⇒ 截断；**代码 / 终端**与**多行正文** ⇒ 保持折行、**明确不截断**；⚠ flex / inline-flex 容器里的裸文本是
> **匿名 flex 项** ⇒ 容器上的 `text-overflow` 无效，文字在子 `<span>` 的要单独点）｜
> ⑧ **去掉「折叠此文件」**（`ctxForFile()` 整项删，右键文件菜单 = 6 项）｜
> ⑨ **`.td-sum-h` = 15px**（写 `calc(15px * var(--ui-fs-ratio))`，15px 无 title token）｜
> ⑩ **`.td-diff-path` 展开后中粗 500**｜
> ⑪ **`.td-diff-path` / `.td-diff-rows` 内一律 13px**（只换 token 档位；子规则逐条同值覆盖；`.td-dr` 行高 20 / `.td-diff-h` 38 未变）｜
> ⑫ **`.r107-stats` 文字居中**（★ 两处死胡同：`fit-content + margin:auto` 被页面级两条 `!important` 盒宽规则压死；
> 真节点不像 `::after` 自动 shrink-wrap ⇒ `margin:auto` 偏 **32px** ⇒ 正解 = **`text-align: center`**；
> ★ ① 与 ⑥ **可共存**（居中 + 溢出时 Chromium 退化为 `start`、省略号照落行尾））。
> **第九拍（两条）** = ⑬ **全屏后按钮图标不翻**（内联 SVG 是 HTML 写死的「四角朝外」，JS 只翻 `aria-pressed`/`title`/`aria-label`
> ⇒ 抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；MAX **从 DOM 读出来缓存**、MIN 硬编码（Lucide `minimize` 四条），只切 `d`、不重建节点）｜
> ⑭ **全屏后拖分栏条「一按就复位」**（两因：(a) `startPanel = panelW` 取**内部缓存**，而「最大化」绕过控制器直接写 `--av-browse-w`
> ⇒ 缓存 641 / 实际 1040 ⇒ 一按下猛跳 761；改读**实际渲染宽**（先 `.is-col-dragging` 停过渡再取几何）；(b) `pointermove`/`pointerup`
> 挂**元素** ⇒ 改挂 **`window`** + `blur`。★ 判据 = **把 move 派发到 `document.body` 仍能拖**（1040 → 960）。
> 另补两条退出路径：**全屏态按下分栏条 = 放弃全屏**（`setMax(false,true)` 不动宽）· **收起侧栏也退全屏**（搭 resize，不观察 DOM））。
> ★ **体位**：`part105/ctrl-conv.js` 是跨代资产 ⇒ 本代在 `part107/ctrl-conv.js` 放**逐字副本 + 一处修正**（`_read_part()` 双目录回退，part105 与 avatar 零影响）。

> （第九拍产物段已并入下方「第十拍」段 —— 见 PLAYBOOK P3.39 ~ P3.46。）

> **第十拍（一条）** = ⑮ **三枚 `.td-rv-menu`（对比范围 / 显示选项 / 提交·推送）跑到触发按钮上方** —— 四枚共用一条
> `{ position:absolute; top:42px }`（相对 `.td-browse`，42px = 标签栏下方），但 `.td-mod-menu` 的触发器在**标签栏**里、
> 另三枚的触发器在**审查工具条**里 ⇒ 实测 dy = **−35.0 / −34.0 / −36.0**。★ **一条 `top` 服务两种锚点高度 ⇒ 必然错一半。**
> 修法 = 新增 `placeRv(menu, trigger)`，在 `toggleMenu()` 打开分支（**摘掉 `[hidden]` 之后**）按触发器**实际几何**摆位：
> 垂直 = 下方 6px；水平 = 左缘对齐触发器、右侧放不下 clamp 到面板右内边；量宽高用 **`offsetWidth`**
> （不受入场 `scale(0.96)` 影响）。CSS 只拆共用规则 + 给 `.td-rv-menu` 静态兜底 `top: 83px`；**`.td-mod-menu` 一字不动**。
> ★ 实测三枚 dy 全 **+6.0**、dxLeft **0.0 / −0.1 / −14.1**（末者 = clamp 生效）；`.td-mod-menu` 回归不变；
> 窄栏 315 三枚全部 `insideMod=true`（**未被 `.td-mod{overflow:hidden}` 裁**）；Esc 关 / 点空白关 / **重开位置一致** /
> 右键菜单（`.td-ctxmenu`）不受影响 —— 全绿。
> 「为什么否决纯 CSS」= 静态算式依赖「标签栏高度（**跨代资产** browse.css 写死 40、**实测 44**）」+
> 「工具条高度（`calc(40px*ratio)`）」两个**来源不同**的魔法数 ⇒ 字号一缩放即脱节。
>
> **第十一拍（四条）** = ⑯ **划词浮条图标 / 文字应为正文黑**（DS `.giencoder-btn-text` 基类给的是**主色蓝**
> `rgb(55,112,247)` ⇒ 加 `.td-selbar .giencoder-btn{color:var(--color-text-1)}`；SVG 走 `currentColor` 自动跟）｜
> ⑰ **地址栏 `.td-url-pill` 补 `:focus-within` 激活态**（底色转白 + **`inset` 1px 主色** + 外 2px 浅主色环；
> ★ 用 `inset` 不用 `border`，否则 26px 胶囊被撑高；★ 取证坑：`focus()` 后**同步** `getComputedStyle`
> 读到的是**过渡起点**，必须等 400ms）｜
> ⑱ **数字动效提速**（根因两层：`delay 1.5s + fill:both` ⇒ 延迟期停在 `from`、**窗口是空的**；
> 而那 1.5s 是**为等骨架屏退场**。改前真机时间线 **2012 淡出 → 2326 移除 → 2493 首见**。
> 修法**两边一起动**：`apply107.py` 的 `wire()` 骨架屏 `1100→380` + CSS `duration .46→.30` /
> `delay 1.5s→calc(.44s + ni*26ms)` ⇒ 空窗 **167ms→0**）｜
> ⑲ **对照 Codex 官方补缺，落地三件**：**终端多标签**（`bindTerm()` 按块绑定 + 标签只切 `hidden` +
> `+` 真新建；⚠ 全页 `.td-term` 单数选择器一律改走 `termPanes()`）· **浏览器截图**（相机按钮 +
> `.td-brw.is-shot::after` 快门 **260ms**；★ 闪**整模块**而非滚动容器 `.td-view`；⚠ 动画 ≤300ms 因
> `verify-design` 的 `CRAFT-ANIM`）· **产物预览层**（`.td-sum-prev` 覆盖摘要 + `md`/`xlsx` 两套骨架 +
> **Esc 算一层**，否则开着预览按 Esc 会**关掉整条侧栏**）。
> （官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 ⇒ 静态演示页落不了地，**不做**。）
> ★ **体位**：本拍**首次动了 `_mods.html`** ⇒ 改序 = `_mods.html` → `ev/splice107.py`（重组 `browse.html`）
> → `apply107.py`；⚠ **`browse.html` 是 splice 的产物、不是手改对象**。
> **产物**：`conversation.html` **799231 → … → 934109 → 936625 → 958568 Unicode 字符**（十一拍合计 **+159337**）；
> UTF-8 字节（LF 归一）**1055517** ｜ 工作区字节（CRLF）**1063012** ｜ LF `sha1 5ce6b87f5150`；`base.html` **472150 逐字节不变**。
> **十查**：幂等 ✓（每拍连跑两遍）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
> `verify-design.py ./pages` 与 `vd-r107l.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜
> `scan-flatten.py` `panel.css` 仍 **2 条**（第十一拍**新增 0 条**）｜代数残留 **0**｜
> `git status` = `M pages/conversation.html`（`+2806 / −12` 行）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`。
> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.47**；各拍要点见 **PAGES P3.11i（共十一拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十六节）**。
> ⚠ **本代不要重跑 `apply106.py`**（GENS 只有四代 ⇒ 会把「基线残留 `r107-conv-css`」判成错误直接退出）；退 r107 = `git checkout -- pages/conversation.html`。
> **待拍板**：④b 用户消息块口径（`min(100%,728px)` vs `100%`）｜`r93-bar` 底线与面板底线**仍是两色**｜折叠默认范围｜官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 **不在静态页范围**（本轮已拍板不做）。

> **r108（2026-10-01 19:4x 起 · 会话详情页「diff 卡片化 + 文件树抽屉」+ 六条精修「含 ★ 复刻 ZCode 右上角任务信息面板」· **第十二拍 + 第十三拍补丁**）—— 🚫 未提交**（r107 已交付 `e9c9498`）：
> ★ **体位**：r107 **已交付** ⇒ **新建 `mg-work/r108/apply108.py`**（`ev/make108.py` 从 apply107 做 **7 处精确替换**）；
> `GENS` = **六代**（r93/r101/r102/r106/r107/r108）；`PART_DIRS` = `part108` → `part107` → `part105` **三级回落**
> （本代只覆盖 `_mods.html` / `panel.css` / `panel.js` 三件）。
> ★★★ **nav 块继续沿用 `r106-nav-js`（不换名）** ⇒ `base.html` + 8 外壳页**逐字节不变**，`git status` 只有 ` M pages/conversation.html`。
> ⚠ **但 CSS / JS 两块都改了 ⇒ 换名 `r108-conv-css` / `r108-conv-js`**（沿用同代名会把新内容一起摘掉）。
> **两条** = ① **`.td-diff` 独立成卡片**（`.td-rv-body` 改 flex 纵列 + `gap:8px` + `padding:8px`；
> `.td-diff` = 1px 描边 + 8px 圆角 + `--color-bg-2` 底 + `overflow:hidden`；头/体补 `border-top: 1px --color-border-1`）
> ⇒ 实测四张卡卡间距 **`[8,8,8]`**；
> ② **「在文件树中定位」右侧加「文件树」按钮 + 右侧文件树抽屉**（`data-td-rv-act="tree"` · `.td-tree` `z-index:35` ·
> 遮罩 + `min(296px,86%)` 面板 + `.td-tree-files` 10 行 · 开合 = `hidden` + `.is-open`
> （`removeAttribute` → `void offsetWidth` → `add`）· 关 = 摘类后 **240ms** 挂 `hidden`）
> ⇒ 实测 `panelBox=[1135,49,296,842]`（右缘贴右栏右缘）、**Esc 只关抽屉不关侧栏**。
> ★★★ **本拍最关键的技术决定 —— 抽屉树用独立类名 `td-tf*`**：`ctrl-conv.js` 的 `pane` 是**整个 aside**、
> `.td-browse-files` 用 `querySelector` **只绑第一棵** ⇒ 复用 `td-bf*` 会打架（抽屉里的行点了没反应）；
> 零干扰已实测（抽屉点文件后「文件」模块 `filesActive` / `filesRows 28` / `filesHidden 9` 一字未变）。
> 🔧 三处坑 = ① 「文件树」按钮被 `[data-td-rv-act]` 通用循环弹多余 toast（加 `if (kind === 'tree') return`，**保留 closeMenus**）；
> ② `.td-tree-h` 被 `scan-flatten` 多报 1 条（派生高度规则缺 `var(--font-size-*)` ⇒ 被 `converge()` 压平 ⇒ 补 token 回 2 条）；
> ③ 探针两处假失败（遮罩挡住自己的触发器 / `||` 短路表达式让动作没执行）。
> **产物**：`958568 → 978614` 字符（第十二拍 +20046）；LF bytes 1078406 / 工作区 1086146 / 7741 行 / LF `sha1_lf 7a1be6be9b76`；
> `base.html` **472150 逐字节不变**；`git diff --numstat` = `248  3`。
> **门禁四绿**：幂等 ✓｜`check-syntax` 10/10｜`verify-design` 与 `vd-r107l2.txt` **逐字节同**
> （md5 `3dbf654337559509110899e48bef1b1c`）｜`scan-flatten` 仍 **2 条**。
> ★★ **新增定论见 PLAYBOOK P3.48**；各拍要点见 **PAGES P3.11i（共十六拍）**；逐条实测见 **`mg-work/r108/acceptance.md`（二十九节）**。
> ⚠ **本代不要重跑 `apply107.py`**（GENS 只有五代 ⇒ 「基线残留 `r108-conv-css`」自检直接退出）；
> 退 r108 = `git checkout -- pages/conversation.html`。
> 🚫 未 commit / 未 push；提交时 `git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`。
>
> **★ r108 第十三拍（2026-10-01 20:2x · 六条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二拍**未提交** ⇒ 按硬规则「**未交付 ⇒ 就地返工**」，本拍 = 第十二拍的**第二层补丁**（叠加在 `r108/` 内）。
> ★ 新增脚本：`ev/patch108l2.py`（555 行，第 ①②③④⑥ 条）· `ev/patch108td.py`（85 行，第 ⑤ 条）；探针 `ev/p108n.js` + `probe108n{,2}.sh`；截图 `ev/shots108n{,2}.sh` + `raw/n-1440-*.png`（12 张）。
> **六条** = ① `.td-sum-sec:hover { border-color: var(--color-border-2) }`（基态 border-1 `rgb(242,242,242)` → hover **`rgb(229,229,229)`** = 深一档）；② `.td-sum-h` 内 4 枚标题 `<svg>` 删净 + 清 `.td-sum-h svg` 死规则（实测 `sumHSvg:0`）；③ `.td-diff-cv { width:13px; height:13px; color: var(--color-text-1) }`（原 `text-3`；实测 `rect [813,156,13,13]` / `rgb(31,31,31)`）；④ `data-td-art` 从内部「预览」按钮**上移到卡片本体**（2 处）+ `cursor:pointer`（点图标区即开预览层、按钮入口保留）；⑤ **任务详情页** `.giencoder-badge-status-text` → 13px（★ 真源在父级 `.giencoder-badge-status` 的 14px，文字节点自己不声明字号 ⇒ **补本页一条规则即可、不动 DS 源**；落点 `<style id="r108-td-css">`）；⑥ **★★★ 复刻 ZCode 右上角任务信息面板**。
> ★★★ **⑥ 最关键的坑 —— `.zd-host` 的 `top` 必须是 44px（不是 0）**：`<main>` 顶部有 `.r93-bar`（`position:absolute; height:44px; z-index:10`，r106 的**固定档**、不随 `--ui-fs` 变），右上角「全屏 / 打开侧栏」两枚按钮就在里面 ⇒ 面板从 `top:0` 起排会**把它盖住**（实测 `elementFromPoint` 命中的是面板自己的 `.zd-acts`，导致探针的 click 点到面板、右栏没开、下游 hover/click 全失效）。改 `top:44px` + `padding-top:12px` 后两枚按钮 `hitSelf:true`、`zdTop:93`。
> ★ ⑥ 落地：`.zd-host#av-zd-status`（`pointer-events:none`）+ `.zd-card`（`auto`）= 四分区 `git`「Git 工具」/ `goal`「目标」/ `plan`「计划」/ `todo`「进程」，trailing `+566 −228` / `2 分 18 秒` / `3/5`；折叠 = `classList.toggle('is-closed')`（不写内联 display）；面板 ⇄ 胶囊 = `hidden` 互斥。实测 `cardRect [455,105,320,512]` / `panelRightGap:16` / `panelTopGap:57` / 折叠后卡高 **512 → 503** / 胶囊 `[672,105,103,32]`。上游 = `zai-org/ZCode`（Apache-2.0）`ConversationStatusPanel.tsx`（2085 行）+ `i18n/locales/zh-CN.ts`（`chat.statusPanel.*`）。
> 🔧 另三坑 = ① `splice108.py` 守卫被**自己注释里的裸 `<aside>` token** 绊倒（第二次同型 ⇒ 注释改成「右栏容器 `aside.td-browse`」）；② `patch108td.py` 首版生成 `</style></style>`（锚点被整体替换 ⇒ 改为只代换 `{{BLOCK}}`）；③ ④ 的预览层 `x=792` 起、打开右栏后 `main` 只到 791 ⇒ 截 `main` **正好切掉预览层**（改截 `.td-sum-prev`）。
> **门禁四件套（在 `top` 修正之后复跑）全绿**：幂等 ✓（`patch108l2.py` 第二遍「应用 0 / 跳过 8」；`patch108td.py`「跳过」；`apply108.py`「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107l2.txt` **逐字节同**（md5 `3dbf654337559509110899e48bef1b1c`）｜`scan-flatten` 仍 **2 条**。
> **产物**：`conversation.html` 978614 → **995133 字符**（+16519；`git diff` **+582 / −11 行**）；`task-detail.html` 767428 → **767836 字符**（+408；**+7 / −0 行**）；`base.html` **472150 逐字节不变**。
> ★★ **新增定论见 PLAYBOOK P3.49**（四条：固定高工具条遮挡 / 注释绊倒守卫 / 锚点 token 回填 / 截图切掉覆盖层）；逐条实测见 **`mg-work/r108/acceptance.md` 八 ~ 十二节**（共十三节）。
>
> **★ r108 第十四拍（2026-10-01 20:5x · 四条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二 / 十三拍**未提交** ⇒ 同上规则，本拍 = **第三层补丁** `ev/patch108l3.py`（772 行 / **27 项**），全部围绕 **`.zd-card`**。
> **四条** = ① **Git 三行接交互**（「更改」复用右栏链路 `[data-td-open-mod="review"]` ⇒ `openTab('review')`；「分支」= `.zd-menu-branch` 5 项 + 行值 `.zd-row-v[data-zd-branch]` 更新 + `.zd-toast` 轻提示；「提交或推送」= `.zd-menu-commit` 2 项，两枚互斥；摆位 = 触发行下缘 + 6px、右对齐卡片右缘、**用 `offsetWidth`**；关闭三路径 = 外点 + **Esc（`window` 捕获段）** + 选完收起）；
> ② **删「计划」分区**（`secKinds ["git","goal","todo"]`）；③ **「目标」按上游校准**（lucide `goal` / 绿圈序号 / `pause`(24+14) / `minimize-2` / `padding 8px` + `radius 8px` + `leading-4` + `h-8 32px` + trailing `·`；★ **圆序号宽高同比** —— 本规则含字号 token ⇒ `scale_block` 只派生 `height` ⇒ 非默认字号下会成椭圆）；
> ④ **弹性微动效**（折展 = `grid-template-rows: 1fr ⇄ 0fr` + 内层 `opacity/translate/scale`，**替掉 `display:none`**；面板 ⇄ 胶囊 = 出场微缩上浮 + 入场 `zd-panel-in` 回弹；缓动 = `--transition-timing-function-spring`，**时长一律 ≤300ms**）。
> **六条坑** = **P3.50**（① 各层 `mark` 是「后一层替前一层保住」的契约 ② `drop_re` 的 `.*?` 必须 `(?s)` + 反判据 ③ 多处共用同一 mark = 静默漏改 ④ CRAFT-ANIM 300ms 上限 ⑤ 探针三类假失败 ⑥ **主题类结论先取色**）。
> **产物**：`conversation.html` → **1009968 字符**（+14835；对 `HEAD` 累计 +51400；`855 / 19` 行）、`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**。
> ⚠ **工作区 `MEMORY.md` 受 3000 字符限额** ⇒ 原 58 条铁律整表已迁入 PLAYBOOK 附录「工作区速览 69 条」（第十五拍重整为「Windows 速记 + 红线索引 + 最近拍」、**第十六拍补回被误顶掉的第 58 条并加到 69 条**，实测 **2982 字符**）。
>
> **★ r108 第十五拍（2026-10-01 21:1x · 六条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二 / 十三 / 十四拍**未提交** ⇒ 同上规则，本拍 = **第四层补丁** `ev/patch108l4.py`（**8 项**），全部围绕 **`.zd-card`** 的视觉精修 + 骨架屏门控。
> **六条** = ① **`.zd-sec-t` = 正文黑 + 中粗 500 + 14px**（去 `inherit`、显式 `font-size: var(--font-size-body-3)` + `font-weight: 500` + `color: var(--color-text-1)`；顺带删掉死规则 `.zd-sec-t:hover`）；
> ② **`.zd-ico` 补 hover**（照本页既有 `.td-browse-ico` 的**完整契约**：`inline-flex` / `24×24` / `padding:0` / `border:0` / `radius 4` / 透明底 / `text-2` + 同块内 `:hover { background: var(--color-fill-1); color: var(--color-text-1) }`，**基态在前**）；
> ③ **「目标」只留 1 条**（`drop_re` 删圆序号那行 ⇒ `.zd-it` 1 / `.zd-it-no` 0）；
> ④ **已完成进程加删除线 + 进行中转 loading**（`text-decoration: line-through` **不传播到绝对定位伪元素** ⇒ 只划文字；`::after` 实心弧 + `@keyframes zd-todo-spin`，★ 时长走 `--zd-spin-dur` **自定义属性**避开 CRAFT-ANIM 按行扫）；
> ⑤ **骨架屏期隐藏面板**（纯 CSS 门控 **`html:has(.r93-sk) .zd-host { display: none }`**，骨架屏一移除即自动失效）；
> ⑥ **`.zd-sec-x` 只在折叠态显示**（基态 `none` + `.zd-sec.is-closed .zd-sec-x { display: flex }`；**(0,1,0) vs (0,3,0)**，不打平）。
> **五条坑** = **P3.51**（① `mark` 撞车 ⇒ **静默跳过**（加硬断言 + `keep_anchor` 豁免位）② 持续旋转时长写进自定义属性 ③ `:has()` 纯 CSS 门控 + 探针要 `try/catch` ④ `text-decoration` 不传播伪元素 ⑤ 自检判据别用太短片段）。
> **产物**：`conversation.html` → **1012144 字符**（+2176；对 `HEAD` 累计 `896 / 19` 行）、`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**。

> **★ r108 第十六拍（2026-10-01 21:5x · 三条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二 / 十三 / 十四 / 十五拍**未提交** ⇒ 同上规则，本拍 = **第五层补丁** `ev/patch108l5.py`（**10 步**）：① 产物预览改挂侧栏**「预览」页签** ② `.zd-host` 折展动效改「收进右上角 / 从右上角展开」 ③ `.zd-host` 整容器改**毛玻璃**。
> **三条** = ① **产物 `td-sum-art` 卡片点击后的预览改挂 `td-browse-bar` 新页签** —— 旧浮层 `.td-sum-prev`（`position:absolute; inset:0`）**整体拆掉**（DOM + CSS + `.td-mod.td-sum{position:relative}` + **Esc 裁决链那一层**；残留 `zd-sum-prev` **0**），
> 新载体 `#av-browse-pane-preview[data-td-pane="preview"]`、点产物 `openTab('preview', {name, ico})`；★ 同一枚页签**复用**承载多产物（连点两个只改名换图标）+ 复用分支加 `if (opts)` 守卫；
> ② **`.zd-host` 折展动效** —— `transform-origin: 100% 0`（computed **`320px 0px`**）；收 ⇒ `scale 1→0.62` + `translate 0px→12px -12px` + `opacity→0`（186ms 到目标 / 203ms `hidden`）；展 ⇒ `@keyframes zd-panel-in` 260ms，**过冲** `scale 1.03715` 再回 1（453ms）；
> ③ **`.zd-host` 改毛玻璃** —— 视觉四件（`.zd-card` / `.zd-mini` / `.zd-menu`×2 / `.zd-toast`）底色 `color-mix` 取透 + `backdrop-filter: blur(18px) saturate(160%)` + `@supports not` 不透明兜底；
> ★★ **取证必须落像素**（只写 `backdrop-filter` 而底色不透明 = 看不出效果）：铺 320×180 纯红 ⇒ 卡面 `rgb(255,199,199)`（`0.78×白 + 0.22×红`），沿 y 衰减 `199`→`237`(y190，已越出红块下沿= **模糊外溢**) →`254`。
> **六条坑** = **P3.52**（① **删变量没删引用 ⇒ 按键抛 `ReferenceError`**（判据剥注释 + 保 `\b` 词界）② `openTab` 复用分支不更新页签名（加 `opts` 守卫）③ `.td-mod-bar` **内容驱动高度**（内容盒上限 = `min-height` − 上下 padding − border-bottom = 27px）④ 同页工具条**本就不齐**（fs14 40/41、fs18 41/49/46）⑤ `backdrop-filter` **必须落像素** ⑥ `verify-design` 重写 `pages/gaps.log` ⇒ 收尾 `git checkout --`）。
> **产物**：`conversation.html` → **1015095 字符**（+2951；对 `HEAD` 累计 **`1047 / 107`** 行；LF `sha1_lf da1acf6a091c` / 8436 行）、`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **二十九节**。
> ⚠ **PLAYBOOK 附录修错**：`doc108q.py` 的「追加 59~63」把 `old` 写成**第 58 条整行** ⇒ 58 被整条顶掉（附录实为 62 条、标题却写 63）⇒ 第十六拍**已补回 58 并加到 69 条**。

### 第十七拍（r108 第六层补丁 · 四条 · 2026-10-01 22:2x · 🚫 未提交）

> ① **`+` 菜单纳入 `placeRv()` 现场摆位** —— 根因是那句**显式放行** `.td-mod-menu` 的单族守卫
>（注释还写着「保持它原来的 CSS 落位不动」）⇒ 它一直吃基类写死的 `left: 64px`，而 `+` 的 x 随页签数量浮动。
> 改 `PLACE_ABS = ['td-mod-menu','td-rv-menu']` 白名单 ⇒ 实测 **dx 恒 0**（1 枚 `1505/1505`、4 枚 `1160/1160`、
> `--ui-fs=18` `1196/1196`）；修复前 3 枚页签 **dx = −218px**。
> ② **浏览器工具条瘦身** —— 删「截图到剪贴板 / 缩放 / 发送页面到对话」三枚（`brwActs = ["more"]` / `shotEls = 0`），
> 配套清 `BRW_TEXT` 三条 + `shotFlash()` + `panel.css` 18-② 快门与只为它存在的 `.td-mod.td-brw{position:relative}`；
> 右键菜单那条改为直接 `say(...)` 切断 `sb.click()` 死引用（有 `if (sb)` 守卫 ⇒ **不报错但「点了没反应」**）。
> ③ **文件树抽屉让开标题栏** —— `.td-tree` 由 `inset: 0` 改 `top: 44px`（44 = `.td-browse-bar` 实测高，
> 字号两档都是 44 ⇒ **不随字号杠杆变**）⇒ `treeRect.top − barRect.bottom = 0`（scrim 与 panel 一起下移）。
> ④ **diff 演示内容加长** —— 统一 +17 / +12 行、并排 +11 / +6 行 ⇒ 卡片1 **11→28** / **6→17**、
> 卡片2 **4→16** / **3→9**；`.td-rv-body` `scrollHeight == clientHeight == 757`（**正好填满、不溢出**）。
> **八条坑** = **P3.53**（① `mark` 别选在「改前就在」的那行上（`BRW_TEXT` 的 `more:` 真踩 ⇒ 断言 `sys.exit`），
> 要取「改完才形成的**相邻**关系」② `old` 被 `new` 原样保留 ⇒ 显式 `strict=False` ③ 自检别用「裸属性名计数」
> （`data-td-brw-act` 该有 2 处）④ **「位置不对」先分清「没跑到算法」还是「压根没进算法」**（根因是**显式放行**的守卫）
> ⑤ 删组件要清「借它力」的引用（`sb.click()` 不报错、只是「点了没反应」，更难发现）⑥ `.td-tree` 的包含块是
> **整条侧栏** ⇒ 判据用相对量 ⑦ **探针可见性盲区：量到了 ≠ 看得见**（侧栏在视口外时 dx 仍 0、截图却是空的）
> ⑧ `verify-design.py` 重写 `gaps.log`（第二次踩））。
> **产物**：`conversation.html` → **1024705 字符**（+9610；对 `HEAD` 累计 **`1146 / 142`** 行；工作区 bytes 1143754 / **8500 行** / LF `sha1_lf cc2105413d08`）、
> `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **三十四节**。
> 🚫 未 commit / 未 push。

### 第十八拍（r108 第七层补丁 · 四条 · 2026-10-01 22:4x · 🚫 未提交）

> ① **预览「在系统打开」拆两枚** —— `[data-td-prev-open]` → `[data-td-prev-save]`（另存为）+ `[data-td-prev-reveal]`（打开所在文件夹），
> `panel.js` 各挂一条轻提示；实测 `另存为` `[1223,100,69,26]` + `打开所在文件夹` `[1298,100,121,26]`、栏 `[792,93,639,40]`（**栏高仍 40**）。
> ② **去掉「最大化侧栏」** —— 按钮在 `.td-browse-acts`（**不在** `.td-mod-bar`），连同 `panel.js` 整段「最大化 / 还原」逻辑
>（`maxBtn`/`setMax`/`setIcon`/`applyMaxW`/`data-td-maxw` + `STORE_KEY`/`MIN_PANEL`/`DEF_PANEL`/`MAIN_MIN`）一起清（−4039 字符）；
> 实测 `browseActs = ["收起侧栏"]`、`maxBtn = 0`。
> ③ **`td-rv-body` 滚不动 → 已修** —— 根因 = **flex 纵列 + 子件默认 `flex: 0 1 auto`（可收缩）+ `.td-diff{overflow:hidden}`**
>⇒ 卡片被**压扁**（卡 1 实占 369 / 需 637）、溢出被**裁掉** ⇒ `scrollHeight === clientHeight` 恒真、约 489px 内容看不见；
> 修法 = `.td-rv-body > .td-diff { flex: none; }` ⇒ `bodySz [757,757] → [757,1212]`、`cardFlex "0 0 auto"`、
> `scrollTop 455`、**`pageScrollTopAfter = 0`**。
> ④ **`+` 菜单「摘要」置首** —— 5 项整块重排 ⇒ `摘要 / 审查 / 终端 / 浏览器 / 文件`（y 不变）。
> **九条坑** = **P3.54**（① 「存在性」断言抓不到「重复应用」⇒ 判据要 `count == 1`（mark 少写「★ 」⇒ 补丁重复应用两次、断言照样过）
> ② 注释正文里写 `*/`（`` `part*/` ``）**提前闭合块注释** ⇒ `check-syntax` FAIL ③ 纯删除/mark 要落「新形成的相邻串」·能整块重排就别拆两步
> ④ `old` 被 `new` 原样保留 ⇒ `strict=False`（第三次）⑤ **改了跨代资产 ⇒ 下游生成器要跟着改来源**（head P107→P108）
> ⑥ 下游守卫别写裸属性名（`data-td-max` 被 demo diff 转义文本误报）⑦ 重建「改前」对照页**三件必须齐上**（否则混合态）
> ⑧ **flex 纵列 + 可收缩子件 + 父级 `overflow:hidden` = 压扁 + 裁切 + 容器永不滚** ⑨ 探针自身也会假失败）。
> **产物**：`conversation.html` → **1022257 字符**（−2448；对 `HEAD` 累计 **`1186 / 239`** 行；工作区 bytes 1141453 / **8442 行** / LF `sha1_lf f3e0bcc1a8e2`）、
> `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **三十九节**。
> 🚫 未 commit / 未 push。

### 第十九拍（r108 第八层补丁 · 两条 · 2026-10-01 22:5x · 🚫 未提交）

> ① **整个右栏划词都弹浮条** —— 放行根由 `.r93-scroll` 扩到 **`.closest('.r93-scroll, .td-browse')`**
>（两者是并列 flex 兄弟、互不包含 ⇒ 不误判；主对话口原能力未动）；真机 CDP **真鼠标**拖选：审查 diff 代码 / 摘要散文 / 文件代码区
>改前 `selbarExists = false`（**浮条根本不弹**）→ 改后 `true`，浮条框 `[886,139,200,38]` 等、**在选区上方 8px**、`elementFromPoint` 命中浮条自身。
> ② **菜单入场不再硬切** —— 根因 = `toggleMenu()` 把「摘 `[hidden]`（`display:none`）」与「挂开态类」挤在**同一 tick**
>⇒ 浏览器拿不到「改前样式」⇒ `opacity/translate/scale` 过渡**被静默跳过**（契约里 0.2s spring 入场**从未运行过**）；
> 修法 = 开态拆四步 `removeAttribute('hidden')` → **`void menu.offsetWidth`** → `placeRv()` → `classList.add(POP_OPEN)`；
> 实测改前第 4 帧 `anims=-` / `op=1`（一帧到终态）→ 改后第 4 帧 `anims=opacity|scale|translate` / `op=0 / tr=0px 4px / sc=0.96`，
> 逐帧 `op` 0 → .188 → .426 → … → 1（≈12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039** 再回落、`off=(368,42)` **逐帧不变 = 零位移**。
> **六条坑** = **P3.55**（① ★★★ **「摘 `[hidden]` + 挂开态类」同一 tick ⇒ 过渡被静默跳过**（无报错、computed 直接给终态 ⇒ 入场动画可能是死代码；判据 = 逐帧 `getAnimations()` + 开帧 computed；修法 = 中间 `void el.offsetWidth`）
> ② 断言必须限定**函数体内**（全文计数被 `.zd-menu` 同形代码误报）③ 注释**不能插在被逐字断言的序列中间** ④ `old` 被 `new` 原样保留 ⇒ `strict=False`（**第四次**）
> ⑤ 判据要跟着事实走（探针选择器先核 DOM：正文是 `.td-browse-body` 而非 `.td-mod-body`）⑥ **「改前对照页」不能沿用上一轮 `bakNN/`**（混合态）⇒ 本代另立 `ev/bak19/`）。
> **产物**：`panel.js` 69623 → **72191 字符**；`conversation.html` → **1024825 字符**（+2568；对 `HEAD` 累计 **`1234 / 242`** 行；工作区 bytes 1145785 / **8487 行** / LF `sha1_lf 2c1ed815740e`）、
> `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **四十四节**。
> 🚫 未 commit / 未 push。
