# GienCoder 项目记忆索引

> **≤3.5K 字节**（超了会被截断注入 ⇒ 白写）。按需 grep，别整读：
> **`HANDOFF.md`** ★开局先读（状态/待办/接手，每轮覆盖）｜ **`PLAYBOOK.md`** 铁律/自检/取证/git（P3.21=r88｜P3.22=r89~r91 小图标网格｜P3.23=r92 改压缩 React 源 + 装饰背景图｜**P3.24=r93 字号特异性反噬 / 设计稿变体叠放 / ui-component 无字号 / 独立页 + 纯 CSS 复用外壳真组件**｜**P3.25=r94 内容盒守恒 / 「用户说的容器」未必是血统所在 / 门禁会扫注释**｜**P3.26=r95 「右侧撑满」= 固定宽改流式 / 滚动条占宽会让同页多列不同轴**｜**P3.27=r96 设计稿「HTML 导出」= 样式权威源 / 改工具类默认色先枚举使用点 / 别把相邻元素宽度当线宽**｜**P3.28=r97 ★`width:N%` 的基数=父盒（窄视口测不出）/ `*` 不贡献特异性 / 「等宽」先分清 A 列宽一致 vs B 每块满宽**）
> ｜ **`PAGES.md`** token/各页事实/配方（**P3.11b 全局字号（含 r93 反噬）**｜P3.11c DS Select｜P3.11d 已归档任务｜P3.11e 顶栏背景图｜P3.11f 设置页 r92｜**P3.11g 会话详情**（r93 ④ 后 = 独立页 `conversation.html`；**r94~r106 续改，共 ⑨~⑯ 八节**）｜**P3.11h 页面路由表 / 新开一页范式**）｜ `YYYY-MM-DD.md` 原始日志
> ｜ **续**：**P3.29=r98** 门禁对注释双重标准 / `:first-child` 撞装饰件 / `font:` 重置 shorthand｜**P3.30=r99** 图标 `transform="matrix"` 雷区 / 弹层量测时机 / DS 实例图标手写｜**P3.31=r100** 设计稿 HTML 丢实例底色 / hover「逐字照做」/ 层级连接线 / `!=null` 判空｜**P3.32=r101** 上一代已提交时新一代怎么接（`GENS` 逐代摘除）｜**P3.33=r101 第二批 七条**｜**P3.34=r102** `min-height` 顶更稳 / 同帧写变量+改属性会被合并 / hover 断言要选不被遮挡的目标｜**P3.35=r103** 加 `position` 会改绘制顺序 / `animation` 移除不触发 transition｜**P3.36=r104** 正 `z-index` 封顶后代浮窗（与宿主 `z-index:0` **成对**）/ 首帧守卫写进 CSS 默认值｜**P3.37=r105** 加动效前先查「官方实现是否已内联」/ 扩块到多页用 `invert_if_absent` 保位置 / 移植到有暗色分支的页必须补暗色档 / 更晚注册的脚本走自定义事件｜**P3.38=r106（六条）** ★★ **`core.autocrlf=true` ⇒ 工作区字节 ≠ 仓库 blob 字节；且 `len(bytes)−CRLF数` 不是字符数（判内容先归一化行尾、再比同一口径）** / 改通用部件「初始态」先 grep 工厂有没有现成开关 / 移植件的几何适配走**本页适配层**（源件逐字节不动保同源校验）/ ★★ **上限型 clamp `min(可用宽, 原逻辑式)`：原式整段照抄别换算、别忘 `min-width:0`、`margin:auto` 在溢出时不对称** / `border-width:0` 在 border-box 下**只缩内容盒**（≠「元素变宽 1px」）
> ｜ skill（用户级）：design-to-code-modular / svg-icon-pixel-grid / css-state-pixel-evidence / **compiled-bundle-jsx-patch**

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

> **r106（2026-10-01 08:2x 首拍 / 08:4x 返工 / 08:5x 第三拍 · 会话详情页六条）—— 🚫 未提交（新一轮，与 `87e2caa` 分开）**：
> ★ **体位**：r102 代已交付 ⇒ **新建 `mg-work/r106/apply106.py`**；`GENS` **四代**（r93/r101/r102/**r106**）；
> ⚠ **r103/r104/r105 从未单独占代 ⇒ 不入 `GENS` 表**。脚本由 `ev/make106.py` 从 `apply102.py` **9 处精确替换**生成
> （每处命中 ≠ 1 次即 `sys.exit`，不手抄 169 KB）。`PART_DIRS` 双目录回退（`r106/part106` → `r102/part105`）。
> ★ 本代**三拍**（同一代、`apply106.py` 就地返工三次、**始终未提交**）：首拍 ①②③④；
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
> **产物（★★ 口径 —— 首版曾算错，此为更正后）**：`conversation.html` **793028 → 798613 Unicode 字符（+5585）**（blob `e17d227b58bf`）；
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
