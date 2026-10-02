# HANDOFF · 下一轮接手卡

> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**
> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**
> 最后更新：2026-10-01 19:4x（**r107 已推送 `e9c9498`** + **r108「diff 卡片化 + 文件树抽屉」已落地（第十二拍）** → 门禁四查全绿 + 真机实测（卡间距 [8,8,8] / 抽屉 panelBox [1135,49,296,842] / 两棵树零干扰）→ **🚫 未提交**）
> ⚠️ **最新一拍 = r108「diff 卡片化 + 文件树抽屉」**（第十二拍；**r107 已交付 `e9c9498` ⇒ 本代是新一代**，
> **新建 `mg-work/r108/apply108.py`**（由 `ev/make108.py` 从 apply107 做 **7 处精确替换**生成），
> `GENS` 摘除表扩到**六代**（r93/r101/r102/r106/r107/r108），注入块 id = `r108-conv-css` / `r108-conv-js`；
> ★★★ **nav 块继续沿用 `r106-nav-js` 不换名**（`NAV_TAG='r106'`）⇒ **base + 8 外壳页逐字节不变、只改 `conversation.html` 一页**）：
> ① **`.td-diff` 独立成一张张小卡片 → 已做**：`.td-rv-body` 改 `flex` 纵列 + `gap:8px` + `padding:8px`；
>   `.td-diff` = `1px --color-border-2` 描边 + `8px` 圆角 + `--color-bg-2` 底 + `overflow:hidden`
>   （让 `.td-diff-h:hover` 的底色被圆角裁住）；头 / 体之间补 `border-top: 1px --color-border-1`。
>   实测四张卡 `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`、卡间距 **`[8,8,8]`**。
> ② **「在文件树中定位」右侧新增「文件树」按钮 ⇒ 右侧弹文件树抽屉 → 已做**：
>   按钮 `data-td-rv-act="tree"`（folder-tree SVG，24 网格 / stroke 2 / 渲染 16px），插在「定位」**右紧邻**；
>   抽屉 `.td-tree[data-td-tree]`（`position:absolute; inset:0; z-index:35`；**下拉 30 < 抽屉 35 < 提交模态 40**）
>   = 遮罩 + 右侧 `min(296px, 86%)` 面板 + 头部（`.td-tree-h` 40px）+ 搜索 + `.td-tree-files`（10 行）。
>   开合 = `hidden` 属性 + `.is-open` 类（**先 `removeAttribute('hidden')` → `void offsetWidth` 强制 reflow → 再 `add('is-open')`**；
>   关 = 摘 `is-open` → **240ms 后**挂 `hidden`）。实测 `panelBox=[1135,49,296,842]`（右缘 1431 = 右栏右缘）；
>   **三条关闭路径全通**（遮罩 / Esc / 头部 ✕），**Esc 只关抽屉、不关侧栏**（裁决链：模态 → 抽屉 → 菜单）。
> ★★★ **本拍最关键的技术决定 —— 抽屉树用「独立类名 `td-tf*`」**：`ctrl-conv.js` 的
>   `pane = slot.querySelector('.td-browse')` 是**整个 aside**、`pane.querySelector('.td-browse-files')` **只绑第一棵**
>   ⇒ 若复用 `td-bf*` 会两边互相打架、抽屉里的行点了没反应。零干扰已实测：
>   抽屉里点 `Controls.tsx` ⇒ 抽屉 `active` 变，而「文件」模块那棵树 `filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**。
> 🔧 **途中排掉三处坑（两个真问题 + 一处探针假失败）**：
>   ① **「文件树」按钮会弹一个多余的「已执行」toast** —— `panel.js` 那条 `[data-td-rv-act]` 通用循环把它也吃了
>     ⇒ 在 `closeMenus(null)` 之后加 `if (kind === 'tree') return;`（**保留 closeMenus**、只跳过 toast）。
>   ② **`.td-tree-h` 被 `scan-flatten` 多报 1 条**（基线 2 → 3）—— 该规则有 `height: calc(40px*ratio)` 但体里没有
>     `var(--font-size-*)` ⇒ 会被 `apply88b.converge()` 压平 ⇒ 补 `font-size: var(--font-size-body-3)` 回到 2 条。
>   ③ **探针两处假失败（产品没问题）**：抽屉遮罩挡住工具条点击（想切并排视图要先关抽屉）+
>     短路表达式 `q() || fn().click()` 让「并排」根本没切过去。
> ★ **门禁四件套全绿**：幂等 ✓（`patch108l1.py` 第二遍「应用 0 / 跳过 6」；`apply108.py` 第二遍「已是目标态」）｜
>   `check-syntax.py pages/*.html` **10/10**｜`verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**
>   （md5 `3dbf654337559509110899e48bef1b1c`，21882 字节 ⇒ 零新增、一处渐变都没引）｜
>   `scan-flatten.py part108/panel.css` 仍 **2 条**（`.td-mod-bar` / `.td-url`）。
> ★ 边界验证：并排视图 `isSplit=true` / 统一行 `display:none`；`--ui-fs=18` 杠杆 ⇒ 树行 **28 → 36**、头部 **40 → 51**；
>   窄档 620 ⇒ 面板仍 296（`min()` 的 `296px` 分支正确）。
> **产物**：`conversation.html` **958568 → 978614 字符（+20046）**，LF bytes **1078406** / 工作区 bytes **1086146** /
> **7741 行** / LF `sha1_lf 7a1be6be9b76`；`base.html` **472150 逐字节不变**；`git diff --numstat` = `248  3  pages/conversation.html`。
> 逐条实测见 `mg-work/r108/acceptance.md`（**七节**）；机制级教训见 PLAYBOOK **P3.48**；本页固定事实见 PAGES **P3.11i**。
> ⚠️ **上一拍 = r107「侧栏模块标签化」（已推送 `e9c9498`）**（复刻 Codex 右栏；**r106 已交付 ⇒ 本代是新一代**，
> **新建 `mg-work/r107/apply107.py`**（由 `ev/make107.py` 从 apply106 做 **13 处精确替换**生成），
> `GENS` 摘除表扩到**五代**（r93/r101/r102/r106/r107），注入块 id = `r107-conv-css` / `r107-conv-js`；
> ★★★ **nav 块刻意沿用 `r106-nav-js` 不换名**（`NAV_TAG='r106'`）—— 硬规则「跨代沿用的宿主标记不换名」）：
> ① **右栏从「单标签 + 文件树」升级成 Codex 三段式 Side Panel → 已做**：
>   ① 标签栏 `[图标]名称 ×` + `＋` + `⤢ 最大化` + `✕ 收起`；多开 / 切换 / 关闭 / **拖拽重排**；
>   `＋` = **五选一模块菜单**（审查 ⇧⌘G / 终端 ⌃\` / 浏览器 ⌘T / 文件 ⌘P / **摘要**）。
>   ⚠ 第三拍起 `⇧⌘G` / `⇧⌘E` / `` ⌃\` `` 是**真绑定**（`⌘T`/`⌘P` 是浏览器级拦不住 ⇒ 不绑）。
>   实测：四标签右缘 1138 / `＋` 左缘 **1142**（紧跟最后一枚）；把末枚拖到最前 ⇒ `[terminal,files,review]`；
>   关 browser ⇒ 邻居 terminal 激活；**只剩一枚时不显示 `×`**（`.td-browse-tabs.is-single`）。
> ② **新增四个模块 → 已做**：**审查**（工具条 = `对比范围 ⌄ +566 −228 4 个文件` + 右端 `复制 / 定位 / ⋯ / 提交⌄ / PR`；
>   4 张 diff 卡 = 两列行号 + 加绿删红 + `⋯ 折叠/展开 46 行未改动` + 行内评论 + 逐文件 `暂存 / 撤销`；
>   `⋯` 十项显示选项；**统一 ⇄ 并排**；`提交 ⌄` 下拉 ⇒ **模态**）/ **终端**（提示符 + **真按键回声**：`ls`/`pwd`/`npm run dev`/`clear`/未知命令）/
>   **浏览器**（URL 行 + 右端 `缩放/发送/更多` + **标注态**：元素虚线描边 + 点击出评论气泡 + 底部 `标注中` 条）。
> ③ **摘要（任务侧栏）→ 已做**：四段 = **摘要 / 计划 / 来源 / 产物**（对照 Codex 26.415）。
>   ⚠ 原「侧边聊天」已在**第三拍被彻底删除**（含 `.td-selbar` 划词浮条）—— 这一格由「摘要」接替。
> ④ **`⤢` 侧栏最大化 → 已做**：自算 `maxPanelW = freeW − 380` 写宿主 `--av-browse-w`；还原读回 localStorage 的 `panelW`。
>   实测 1440：641→**1040**（main 779→380）；2560：641→**2160**（main 1899→380）。⚠ 用**两层 rAF** 落定，避开 ctrl-conv 的单层 rAF。
> ⑤ **Esc 层级 → 已做**：`panel.js` 挂 **window 捕获段**（早于 ctrl-conv 的 document 捕获段）⇒ 一次 Esc 只关菜单，再按才关侧栏。
> 🔧 **期间修掉两个真 bug（都是量出来才现形）**：
>   ① 新模块 `<section class="td-mod td-term">` 与内部 `<div class="td-term">` **类名撞车** ⇒ `querySelector('.td-term')` 取到 section
>     （`tabindex` 为 null）⇒「点终端打字没反应」；且整套 `.td-term{}` 样式压在 section 上 ⇒ **section 改名 `td-mod-term`**。
>   ② `.td-commit{inset:0}` 的**包含块跑到视口**（源件 `.td-browse` 没写 `position`）⇒ 遮罩铺满整站、卡片居中屏幕
>     ⇒ 给 `.td-browse` 补 **`position: relative`**（`modalRect [418,211,250,246] → [792,49,639,842]` ≈ `panelRect [791,48,641,844]`）。
> ★★ **第二拍返工（邵先生 10:0x 反馈两条，见 `acceptance.md` 第七节 / PLAYBOOK **P3.39⑧⑨**）**：
>   ③ **「审查」的 `⋯` 显示选项浮窗点开后关不掉** —— 根因 = `closeMenus()` / Esc 裁决的**搜索根写成了标签栏 `bar`**，
>     而 `.td-rv-opts` 挂在**模块工具条 `.td-mod-bar`** 里 ⇒ 三条关闭路径全废（外点 ✗ / Esc ✗ / 选完不关 ✗），
>     且 Esc 会漏到 ctrl-conv **把整条侧栏关掉**。修法：搜索根 `bar` → **`pane`**。
>     实测：外点关 ✓ / Esc 只关浮窗、`panelOn` 仍 true ✓ / 选完自动关 + `is-split` ✓ / 再按 Esc 关侧栏 ✓。
>   ④ **「侧边聊天」样式对齐主对话 `r93-scroll`** —— 正文 13/20.43 → **15/22**；用户气泡 `--color-primary-1` `#F5F8FF`
>     → **`--r93-bubble` `#E5EDFE`** + 圆角 `8 8 2 8` + 内距 `9px 12px`；引用块 → **13/22**；输入框 → **14/22**；
>     助手消息**去灰底气泡**（主对话助手正文无底）；助手标记 → **24px 同源 GienX logo**（原来是个写死的「A」）。
>   ⚠ 顺带挖出一个**仓库级机制坑**：`apply88b.converge()` 的「跳过本代块」正则用的是**硬编码 `CSS_ID = 'r87-ui-css'`**
>     ⇒ 本代块从未被跳过 ⇒ `line-height: calc(Npx * ratio)` 被 unscale 压成裸 px、又因体里没有 `var(--font-size-*)`
>     而不再被重派生（**`--ui-fs` 杠杆静默失效**）。修法 = **带行高的规则，`font-size` 写 token**；15px 档用两段式写法。
>     自查脚本 `mg-work/r107/ev/scan-flatten.py`；判据必须看 **`--ui-fs=18`**（默认 14 下看不出来）。
> ★★ **第三拍返工（邵先生 10:2x 反馈四条，见 `acceptance.md` 第八节 / PLAYBOOK **P3.39⑩⑪⑫**）**：
>   ⑤ **「侧边聊天」彻底删除** —— 菜单项 / section / `panel.js`（`AV_SVG`·`pushMsg`·`sendSide`·logo 注入·**`.td-selbar` 划词浮条整段**）/ `panel.css` 两节，全清；
>     判据 = 页面里 `td-side` / `td-selbar` / `AV_SVG` / 「侧边聊天」四个字 **全部为 0**（连注释都清）。原第五格由 **「摘要」** 接替。
>   ⑥ **并排视图下折叠失效** —— `.td-diff:not(.is-open) .td-diff-rows`(0,3,0) 与 `.td-rv-body.is-split .td-diff-split`(0,3,0)
>     **特异性完全相同，后者写在后面 ⇒ 折叠路径整体失效**（统一视图正常，只在并排暴露）
>     ⇒ 后者加一层 `.is-open` 提到 **(0,4,0)**。四象限实测：统一展开 `block/–/block`｜统一折叠 `none/–/none`｜并排展开 `–/block/block`｜并排折叠 `–/none/none`。
>   ⑦ **「折叠全部文件」⇄「展开全部文件」** —— 同一枚菜单项双向切换（**文案 + 字形一起翻**）；
>     判据 =「**只要还有折叠着的文件就显示『展开全部文件』**」；手动折单个文件后也会回来同步。实测 2 开→4 开→0 开→手动 1 开，文案全程正确。
>   ⑧ **对照 Codex 官方补的遗漏（本轮主体）**：**对比范围下拉**（上一轮 / 本分支 vs main / 全部未提交）——原来那颗按钮带 `⌄` 却点不开 ·
>     **`⋯` 显示选项补齐八项**（自动换行 / 词级差异 / 隐藏空白 **真生效**；刷新 / 不加载完整文件 / 富预览 / 复制 git apply 命令）·
>     工具条**动作组**（复制 / 在文件树中定位（会真切到「文件」标签）/ `提交 ⌄` 含推送 / PR）· 逐文件 **暂存 · 撤销** ·
>     「N 行未改动」**真展开** · **新增「摘要」模块**（摘要/计划/来源/产物，对照 26.415）· **快捷键真绑定** · 轻提示 toast。
> ★★ **第四拍返工（邵先生 10:5x 反馈五条，见 `acceptance.md` 第九节 / PLAYBOOK **P3.40**）**：
>   ⑨ **「摘要」升为右栏默认页签 + 四模块卡片式** —— 初始标签 `data-td-mod` `files`→`summary`（`_head.html`）
>     + 初始化 `activate('files')`→`activate('summary')`（`panel.js`）两处同改；`.td-sum-sec` 加
>     `1px --color-border-1` 描边 + `8px` 圆角 + `--color-bg-2` 底 + `12px` 内距（容器 `gap:12px`）；
>     卡内来源/产物降级为**行式**（`bw:0`、`pad:6px 8px`、hover `--color-fill-1`）避免「卡中卡」。
>   ⑩ **补回划词浮条**（第三拍 ① 连 `.td-selbar` 一起删掉的那条）——**并做成真功能**：两枚 DS 文字按钮
>     （`giencoder-btn-text-size-small`）「添加到对话」（真把选中文本插进主 `textarea`，占位符「描述你的任务」）/
>     「复制」（`execCommand('copy')`）；选中 `.r93-scroll` 内文本 ⇒ 浮条出现在选区上方；Esc 只收浮条、不关侧栏。
>   ⑪ **补右栏右键菜单（先调查后落地）** —— **九类目标共用一份表驱动容器 `.td-ctxmenu`**（`role=menu`）：
>     标签 5 / 审查文件头 7 / 审查代码行 5 / 终端 6 / 浏览器元素 6 / 浏览器空白 5 / 摘要来源 3 / 摘要产物 3 / 计划条目 4；
>     危险项红字（`is-danger`）；能复用既有 handler 的一律 `元素.click()`。**反例**：右栏内普通空白 / 右栏外均**不接管**。
>   ⑫ **`.td-browse-tab` 字号 12 → 14px**（`--font-size-body-1` → `--font-size-body-3`）。实测 `tabFs 14px` / `tabH 28px`。
>   ⑬ **全右栏下拉改用 giencoder DS 组件** —— 四枚容器（`+` 菜单 / 对比范围 / 提交 / 显示选项）挂
>     `giencoder-select-popup + giencoder-menu`，条目 `giencoder-menu-item`、分组标题 `giencoder-menu-group-title`、
>     图标位 `giencoder-menu-icon`、选中 `giencoder-menu-item-selected`；`panel.css` **自绘那节整段删掉**、只留定位与槽位。
>   🔧 本拍四个坑（全在 PLAYBOOK **P3.40**）：(a) `.td-mm-item{background:transparent}` (0,1,0) 与 DS 选中态底**打平 + 后写** ⇒ 选中底被抹 ⇒ 改 `:not(.giencoder-menu-item-selected)`；
>     (b) ★★ **页面级通配适配层 `html[data-r93-page='conversation'] .giencoder-select-popup{top:auto!important;bottom:…!important}`（r93 ④）把右栏新挂的 DS 弹层一起扫到** ⇒ `rect.y=-170` 整排看不见（开合状态全对、就是位置错）⇒ 加 (0,3,1) 同名适配翻回向下；
>     (c) ★★ **`!important` 连行内 `style.top/left` 也压得过** ⇒ 右键菜单坐标改用 `--td-ctx-x/--td-ctx-y` 自定义属性 + `!important` 规则落位；
>     (d) 探针「过渡中取值」假失败（**第三次踩**）⇒ 打开与量测拆两次 eval（中间 `wait 600`）。
> ★★ **第五拍返工（邵先生 11:3x 反馈两条，见 `acceptance.md` 第十节 / PLAYBOOK **P3.41**）**：
>   ⑭ **四枚下拉 + 右键菜单 hover 全无 → 补齐**（真 bug）。根因：第四拍的基态
>     `.td-mm-item:not(.giencoder-menu-item-selected){background:transparent}` 是 (0,2,0)，
>     与 DS 的 `:hover` / `-selected` **同特异性但文档序在后** ⇒ 把两态一起压掉
>     （真鼠标悬停 `matches(':hover')=true` 而底色仍 `rgba(0,0,0,0)`）。⇒ 基态与 `:hover` 写同一块、基态在前。
>   ⑮ **下拉改挂 DS 的 Dropdown 组件**（邵先生点名 `.td-rv-opts`）—— 第四拍挂的
>     `giencoder-select-popup`（**Select** 的弹层）+ `giencoder-menu`（**导航菜单**，`mapsFrom: sidenav/topnav`）
>     是**串了两个族** ⇒ 换成 `giencoder-dropdown-popup` / `-item` / `-divider`（+ 契约态 `.is-danger`），
>     与**本页** r93 ⑦ 行右键菜单 `.r93-ctx` **同源同口径**。容器的 `[hidden]` 兜底随之恢复可用
>     （原被 r75 的 `.giencoder-select-popup{display:block !important}` 压死）。
>     ⚠ 选中态：DS Dropdown **没有** `-selected` 类（不虚构）⇒ 按契约取「主色文字 + 勾选图标 ✓」，
>       两枚 radio 项补 `.td-mm-mark`；原先那套浅蓝底 + 左缘 3px 条属 Menu 族，一并撤掉。
>     ⚠ 条目几何从「36 高 / hover fill-1 / max-height 280 出滚动条」换成 DS Dropdown 契约值
>       （`pad 5px 8px` / `radius 4` / `lh 22×ratio` / hover `--color-fill-2`）⇒ 10 项的 `.td-rv-opts`
>       **不再出滚动条**（`h:385`、`ovfY:visible`）。
>     ⚠ DS 骨架的 `animation: giencoder-popup-in` 播完把 `opacity` 打回 0 ⇒ 适配层显式 `animation:none`。
> ★★ **第六拍返工（邵先生 11:4x 反馈三条，见 `acceptance.md` 第十一节 / PLAYBOOK **P3.42**）**：
>   ⑯ ★★★ **输入卡下方那行统计小字「框选不到」= 它是 CSS 生成内容** —— 该行是 r97 ④ 用纯 CSS 的
>     `… > div.mt-8::after { content: '2 轮 · 27 步 · …' }` 挂出来的。**生成内容不是 DOM 的一部分**
>     ⇒ 选区落不进去（`Selection.toString()` 恒空、`caretRangeFromPoint` 退回宿主元素；
>     ★ **隔离对照**：临时建 `#zzA::after` 与 `#zzB`（真文本），同一手法一次运行里 `""` vs `"REAL-SELECT-ME"`）。
>     ⇒ 关掉伪元素 + `panel.js` 注入真节点 `.r107-stats`，版式逐项复刻（12px / 行高 16×ratio / `--r93-meta` / nowrap）。
>     ⚠ 宿主是 React 的 `div.mt-8` ⇒ `MutationObserver`（body/childList+subtree）兜两件事：
>       **重渲染摘掉要补回** + **重挂后被插到中间要挪回末尾**；回调只做「判存 + 不在末尾就 appendChild」⇒ 自收敛。
>     实测四档：`isLast:true` / 宿主 `gap:8px` / 计算样式与旧伪元素逐项相同 / **`selLen` 0 → 103**。
>   ⑰ **`.r93-pre` 去掉字体族** ⇒ `font-family: var(--font-family)`（= 站点默认档；**不用 `inherit`**，不赌祖先链）。
>     只覆写这一条：盒模型 / 字号（14px）/ 行高（16px）/ 换行策略一字不动；实测 `preFont === bodyFont`、全页只剩 1 种字体族。
>   ⑱ ★★ **内容列变窄时两条自适应**（判据 = **容器可用宽**，不是视口分辨率；写法同 ④b 的 `.r93-bub`）：
>     · **技能选择浮窗**（React **行内**写死 `width:760`）⇒ `width: min(760px, 100%) !important`
>       （行内样式只有 `!important` 压得住）；包含块是输入卡 ⇒ `100%` = 输入卡内宽。
>       实测 1440/1280/1100 溢出 **+23/+81/严重 → 恒 −23**（即浮窗内缩 23px，不再顶到滚动口裁剪边）。
>     · **`.r93-alert`** 定高 44 ⇒ `height:auto; min-height:44px; padding:8px 16px`。
>       `8px` 竖内距与单行态**完全等价**（内容 22+16=38 < 44 ⇒ 仍顶到 44、`align-items:center` 照样居中）
>       ⇒ 单行宽度零变化；折行时才长高（1280 `h62` / 1100 `h106`），`clientHeight === scrollHeight` ⇒ 不再溢出圆角盒。
> ★★ **第六拍体位**：仍是 r107 **就地返工**（`apply107.py` / `GENS` / 注入块 id / `NAV_TAG` 全不动）；
>   三条**全部落在本页适配层**（`panel.css` 第 10~12 节 + `panel.js` 的 `statsBoot`）—— 与 r106 ② 同体位，
>   源件与历代遗产块**一字未动** ⇒ `apply107.py` 是「apply106 + **13 处替换**」（第七拍新增 `2d)` 正 + 逆）的干净产物。
>   ⚠ `_head.html` / `_mods.html` 未动 ⇒ `splice107.py` 重跑后 `browse.html` **sha1 不变**（已验）。
>   ⚠ `fs.converge()` 会把 `<style id="r107-conv-css">` **整块 stash 跳过** ⇒ 新增的 `min-height` 不会被 unscale 吃掉。
>   `base.html` 仍**逐字节不变**（472150 字符）。第六拍产物 **921730 → 925776 字符（+4046；相对 HEAD +126545）**。
> ★★ **第七拍返工（邵先生 12:1x 反馈七条，见 `acceptance.md` 第十二节 / PLAYBOOK **P3.43**）**：
>   ⑲ ★★ **「渲染出来的字」与「渲染不出来的字」要分开判** —— 右栏里**可见**的竞品名共 8 处
>     （diff 文件名 / 三行代码 / 摘要描述段 / 三条来源标题）+ 两处悬停 `title`，全部换成 GienCoder；
>     **三条 `td-sum-src` 的外链 `href` 有意保留**（真实地址，替换域名段即 404，且不渲染成页面文字）；
>     前六拍写下的 7 处**设计来源注释**（CSS 5 / JS 2）同样保留。
>     ★ 本轮新增的注释一律避开被清理的词（我自己的第 13 节注释已改成「竞品名」中性表述）。
>     另补一处真·全局：`pages/avatar.html` 历史会话列表里那条示例标题（含竞品名的那条）
>     ⇒ 做法照 `apply106.py` 的 `2b)` 先例，`apply107.py` 新增 `2d)` 正 + 逆，EDITS **11 → 13 处**。
>   ⑳ ★★ **同一处改动要先判「节点从哪来」** —— 下拉菜单的标题行有两类来源：
>     静态 HTML（`.td-mm-cap`）与 **JS 现场生成**（`.td-ctx-head`，`ctxBuild()` 里建）⇒
>     删 HTML 治不了后者 ⇒ **一段 `display:none` 把两类一起关**（菜单是 column flex，塌行不占位 ⇒ 与删节点视觉等价）。
>     快捷键提示同理（静态 `.td-mm-key` ×10 + JS 的 `.td-ctx-key`）。
>   ㉑ ★ **DS 组件「宽度不拉通」先查它自己的 display** —— 提交卡的「目标分支」输入框挂
>     `.giencoder-input-wrapper`（编译样式 `display:inline-flex; width:auto; min-width:120px`）
>     ⇒ 实测**同卡其它行都是 308、它只有 207**；修法 = 双类
>     `.giencoder-input-wrapper.td-commit-in { display:flex }`（提高特异性，不赌文档序）。
>   ㉒ ★★ **「统一字体族」要分清「本代自己的样式」与「跨代沿用的移植件」** ——
>     `panel.css` 自己那 8 条**就地改**；「文件」模块代码区那条在 **r102 代已交付的 `part105/browse.css`** 里
>     （不回改历史代）⇒ 只能在本页**多一级类数覆盖**（`.td-browse .td-browse-pre`），
>     153 个 `.td-code*` 子树靠继承。⚠ 这条是**改完第一遍量出来才补的**。
>   ㉓ ★★ **联动显隐先找「状态类挂在哪一级」** —— 右栏的 `.av-browse-on` 实测加在
>     **shell 的 flex 行**上（`main` 与预览栏的共同父级），页头那枚按钮在 `main` 里 ⇒ 是它的后代
>     ⇒ **纯 CSS 可判，不必写 JS**：`.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }`。
> ★★ **第七拍体位**：仍是 r107 **就地返工**（`apply107.py` / `GENS` / 注入块 id / `NAV_TAG` 全不动）；
>   六条落在 `part107/panel.css`（新增第 13 节 + 第 1~5 节各自的 `font-family` 就地改），
>   一条落在 `part107/_mods.html` 文案 + `apply107.py` 的 `2d)`。改序照旧（下→上）。
>   `base.html` 仍**逐字节不变**（472150 字符）。第七拍产物 **925776 → 927464 字符（+1688；相对 HEAD +128233）**。
> ★★ **第五拍体位**：仍是 r107 **就地返工**（`apply107.py` / `GENS` / 注入块 id / `NAV_TAG` 全不动）；
>   改序 `part107/*` → `ev/splice107.py` → `ev/make107.py` → `apply107.py`（只能下→上）。
>   `base.html` 仍**逐字节不变**（472150 字符）。第五拍产物 **920259 → 921730 字符（+1471；相对 HEAD +122499）**。
> ⚠★ **两条最要紧的体位事实**：
>   1) `core.autocrlf = true` ⇒ 仓库 blob 存 **LF**、工作区落盘 **CRLF** ⇒ 原始字节天然差「行数」字节（**不是内容改动**）。
>   2) ★★ **口径**：`len(bytes) − CRLF数` **不是字符数**（本页中文多，会虚高 ~6.8 万）⇒ 判内容增减要**先归一化行尾、再比同一口径**。
>   本代 `conversation`：**799231 → 866988**（第一拍 +67757）→ **876008**（第二拍 +9020）→ **894916**（第三拍 +18908）
>   → **920259**（第四拍 +25343）→ **921730**（第五拍 +1471）→ **925776**（第六拍 +4046）→ **927464 Unicode 字符**（第七拍 +1688）；
>   **相对 HEAD 合计 +128233**。UTF-8 字节（LF 归一）870627 → 952672 → 976078 → 1004420 → 1006094 → 1012253 → **1015265**；工作区字节（CRLF）947490 → 958664 → 979610 → 1011192 → 1012899 → 1019153 → **1022207**；LF `sha1 79aa4533761b`。
> （r107 交付时）工作区：**干净**（仅剩 `?? mg-work/r107/ev/bak{7,8,9,10}/`）。已推送 `e9c9498`：`conversation.html` **958568 字符**。
>   —— **`base.html` 逐字节不变**；8 个外壳页里**只有 `avatar.html` 因第七拍文案动了 1 处**，其余 7 页不动
>   （nav 块沿用 `r106-nav-js`；`apply107` 跑完打印「base.html 已是目标态」）。
>   `origin/main` = **`e9c9498`**（本地 HEAD 仍 `e9c9498`；**r108 十二拍已在工作区落地、🚫 未提交**）。
> ⚠ **本代不要重跑 `apply106.py`**（它只认四代 ⇒「基线残留 r107-conv-css」自检直接退出）；
>   退 r107 只需 `git checkout -- pages/conversation.html`。
> ⚠ **r89 / r90 / r91 / r92 对设置页的改动、r93 需求 1 对字号机制的改动，全都是 r88 的就地返工**（r88 未提交 ⇒ 按硬规则不另起代数，直接改 `mg-work/r88/apply88.py` 与 `apply88b-fontsize.py`）。
> ⚠ **r94 ~ r100 全部是 r93 代就地返工**（落在 `mg-work/r93/apply93.py`）；**r101 起是新代**（`mg-work/r101/apply101.py`，承接 r93 代的产物）；
> **r102 又是新代**（`mg-work/r102/apply102.py`，承接 r101 代的产物 —— `GENS` 现在有 r93 / r101 / r102 三代）；
> **r103 是 r102 的「未提交期就地返工」**（仍改 `apply102.py`，注入块 id 不变）；
> **r104 / r105 同样是就地返工**（仍改 `apply102.py`）⇒
> **r102 十一条 + r103 六条 + r104 四条 + r105 三条是同一次交付**，已于 2026-09-30 23:5x 提交推送（**`87e2caa`**）。
> ★ **r103 / r104 / r105 从未单独占代**（都是 r102 的就地返工）⇒ **不入 `GENS` 表**。
> **r106 是新代**（`mg-work/r106/apply106.py`，承接 r102 代已交付的产物）—— 脚本由 `mg-work/r106/ev/make106.py`
> 从 `apply102.py` **9 处精确替换**生成（每处命中 ≠ 1 次即 `sys.exit`），不手抄 169 KB。
> ★★ **r107 又是新代**（`mg-work/r107/apply107.py`，承接 r106 代已交付 `4d081ba` 的产物）—— 同样用生成器
> `mg-work/r107/ev/make107.py`（从 `apply106.py` **13 处精确替换**）；`GENS` 现在 **r93 / r101 / r102 / r106 / r107 五代**，
> **但第五代的 nav id 刻意仍写 `r106-nav-js`**（见本卡开头 ★★★）⇒ base 与 8 页不换名、不改内容。
> ⚠ `part107/browse.html` 是**组装件**（`ev/splice107.py` = 原 Files 正文逐字剪出 + 换头部 + 追加四个新模块）
> ⇒ 改 `_head.html` / `_mods.html` 后**必须先重跑 `splice107.py` 再跑 `apply107.py`**，否则改不进页面。

> ⚠ **★ `pages/` 下每个页面都是「完全自包含」的独立 html**（顶栏 + aside + 外壳各一份，**没有共享布局、没有真实路由**）⇒ 新开一页 = **由源页净底重建（不复制）**；页面间跳转靠每页内嵌 `<!-- SHELL-NAV-FIX v5 -->` 的 `ROUTE` 表 + `hashchange`（见第十节）。

---

## 一、当前工作区状态

**r102 ~ r105 已全部提交推送**（**`87e2caa`**）；**r106 六条（`4d081ba`）+ Codex 右栏调研（`f13b3bf`）也已提交**（2026-10-01 09:4x，邵先生发话 commit）。
r86 ~ r100 于 18:2x 提交推送（`6a4b0ea..d7e2151`）；**r101 于 20:2x 提交推送**（`1d11fc9..9f252e5`）。

★★ **r108（diff 卡片化 + 文件树抽屉）＝本代新产物，🚫 未提交**（2026-10-01 19:4x，第十二拍）。工作区：
**` M pages/conversation.html`（978614 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。
> ★★★ 这是本代刻意设计的结果：nav 块**沿用 `r106-nav-js` 不换名**（硬规则「跨代沿用的宿主标记不换名」），
> 于是 `apply107.py` 跑完 `base.html` 打印「已是目标态（无改动）」⇒ 满足「不得改动其他不必涉及的模块」。
> ⚠ 工作区字节数比仓库 blob 大**「行数」个字节** = `core.autocrlf=true` 的行尾差，**不是内容改动**。
> ★★ 判据：**先把工作区 `\r\n` 归一成 `\n`、再比同一口径**（`len(bytes)−CRLF数` **不是**字符数！）。

⚠ ★ **本代不要重跑 `apply107.py`**：它的 `GENS` 只有五代，会把「基线里仍残留 `r108-conv-css`」判成错误直接退出。
  退 r108 只需 `git checkout -- pages/conversation.html`（只改了这一页）。


| 改动 | 内容 |
|---|---|
| `pages/conversation.html` | **634719 → 793028 字符**（r101 两批 +38126 → r102 +10199 → r103 +2421 → r104 +6183 → **r105 ② +2173 → ③ +99207**）；LF 文本 `sha e67474395502`（r101 交付态 `98140cc4bf8f`、r102 态 `249fbc984716`、r103 态 `a340b6a9e89f`、r104 态 `05b899bd4366`）；`script=9 style=16`（**16 与 HEAD 一致，旧记录写 15 是笔误**）；注入块 id 经 `r93-conv-*` → `r101-conv-*` → `r102-conv-*` → **`r106-conv-css` / `r106-conv-js`**（历代残留 0）；r102 十一条 + r103 六条 + r104 四条 + r105 三条见 `mg-work/r102/acceptance.md`，**r106 六条见 `mg-work/r106/acceptance.md`**。★ **r106 态（未提交）：793028 → 798613 字符（+5585）**，工作区 blob `e17d227b58bf`。★★ **r107 态（已交付 `e9c9498`）**：`799231 → 866988（一 +67757）→ 876008（二 +9020）→ 894916（三 +18908）→ 920259（四 +25343）→ 921730（五 +1471）→ 925776（六 +4046）`，**相对 HEAD +126545**；工作区字节 1019153（CRLF）/ UTF-8 1012253（LF 归一），LF `sha 6655f13a1afd`；注入块 id `r107-conv-css` / `r107-conv-js`（**`r106-*` / `r102-*` / `r101-*` / `r93-conv-*` 全 0**）；r107 十一拍见 `mg-work/r107/acceptance.md`（**十六节**）。★ **r108 态（🚫 未提交）**：958568 → **978614 字符**（第十二拍 +20046）；LF bytes 1078406 / 工作区 bytes 1086146 / 7741 行 / LF `sha1_lf 7a1be6be9b76`；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 十二拍见 `mg-work/r108/acceptance.md`（**七节**） |
| `pages/base.html` | **471444 → 472150 字符**（r101 +706，r102 ~ r105 **+0**）；LF 文本 `sha c406a60add16`（r101 态 `2ffe5f16d5c8`）＝ nav 脚本 id 由 `r101-nav-js` 换成 **`r102-nav-js`**（注释对同步换名，**长度相同**）+ **`r101-hdr-css`（顶栏图 70%）**。r106 态：仍 **+0**，nav id → `r106-nav-js`（等长），工作区 blob `3436a5e7857e`。★ **r107 态：仍 472150 字符 / 逐字节不变（nav id 刻意沿用 `r106-nav-js`）** |
| `pages/{avatar,skills,automation,settings,dev,kanban,req-kanban,task-detail}.html` | **各 +714**（r105 ① 注入同一块 `r102-nav-js`；这 8 页在 r101 已各 +703）；终态 `568086 / 361583 / 361696 / 459222 / 450205 / 568052 / 513791 / 767428` |
| `mg-work/r101/` | `apply101.py`（含 `--revert` / `--dry`）/ `acceptance.md`（**十三节**）/ `before/`（2 份前置基线）/ `ev/`（探针 + 终态取证 + `vd-r101*`）/ `raw/` —— **已提交**，仅供追溯 |
| `mg-work/r102/` | `apply102.py`（**163605 字符 / 220815 字节**；`cp` 自 r101 后大改；**r103 六条 + r104 四条 + r105 三条也在里面**，含 `--revert` / `--dry`）/ `acceptance.md`（**六节 r102 + r103 段 + r104 段 + 新增 r105 段**，39524 字节）/ `before/`（`conversation-r102.html` 721864 / `base-r102.html` 490294）/ **`part105/`**（`browse.css` 15937 / `browse.html` 31688 / `browse.js` 47410 / `ctrl-conv.js` 15465，r105 ③ 三件套 + 控制器）/ `ev/`（`p102a~p102f` + `p103a~p103k` + `p104a~p104q` + **`p105a~p105j` + `p105e/f/g1.js` + `extract105.py` + `write_acc105.py` + `.log`** + `audit104.py/.log` + `vd-r102a/b.txt` / `vd-r103a.txt` / `vd-r104b/c.txt` / **`vd-r105a/b.txt`**）/ `raw/`（基线 / 改后 1440+2560 / 折叠 / hover / `g103-*` ~ `k103-*` / `z104-*` `a104-*`~`z2560-*` `c2560-*` / **`x105-*` `y105-*` `z2560-browse*` `z2560-dark-browse` `z1440-dark-105` r105 裁片**）—— **已提交**（`87e2caa`）|
| `mg-work/r106/` | **已提交（`4d081ba`）**：`apply106.py`（含 `--revert` / `--dry`；第三拍新增 ④b 规则）/ `acceptance.md`（**六条 · 三拍**，含「④b 定位过程」节）/ `before/`（`conversation-r106.html` 865582 / `conversation-r106a.html` 870416 / **`conversation-r106b.html` 872270 = 第三拍前态** / `base-r106.html` / `base-r106a.html`）/ `ev/`（`make106.py` + `p106a~p106m` 探针与日志 + `vd-r106a/b/c.txt`）/ `raw/`（`b106-*` / `a106-*` / `a106v2-*` / `g106-*` + **`m106-{1280,1370,1440,1920,2560}-open.png` + `m106b-1280-open.png`**）|
| `mg-work/r107/` | **已推送（`e9c9498`）**：`apply107.py`（**由 `ev/make107.py` 从 apply106 做 13 处精确替换生成**；GENS 五代、nav 沿用 r106；含 `--revert` / `--dry`）/ `acceptance.md`（**十二节**：口径 / nav 不换名体位 / 五模块 / **两个真 bug** / 稳定性证明 / 取舍 / 取证 / **第二拍** / **第三拍** / **第四拍五条** / **第五拍两条** / **第六拍三条** / **第七拍七条**）/ **`part107/`**（第七拍后：`_head.html` 5270 · `_mods.html` 35916 · **`browse.html` 71578 = 组装件** · `panel.css` 39686 · `panel.js` 48583）/ `ev/`（`make107.py` · **`splice107.py`** · `probe107.sh` · `debug107.sh` · `debug107b.sh` · `final107.sh` · `shots107.sh` · `shots107d.sh` · `shots107e.sh` · `shots107f.sh` + `verify107e.sh` · **`shots107g.sh` + `verify107g.sh` + `probe107f.sh`（第六拍）** · **`p107d1~p107d9.js`（第四拍探针）** · **`p107e1/e2.js` + `fix107e1.py` + `fix107e2.py`（第五拍）** · **`p107f1~p107f7.js` + `p107g1.js`（第六拍探针）** · **`p107h1~h3.js` + `probe107h{,2,3}.sh` + `patch107h{,2}.py` + `doc107h{,2}.py`（第七拍）** · `scan-flatten.py` + `.log` + `vd-r107{,b,c}.txt`）/ `raw/`（`g1~g7` 出图 · `f1~f9` 功能 · `d1~d7` 诊断 · `h1~h3` 窄档/字号 · `s1~s12` 首轮 · `d1-summary` / `d2-modmenu` / `d3-ctxmenu` / `d4-selbar` / `d5-ctx-src` / `d6-ctx-file` / `d7-ctx-el`（第四拍裁片）· `e1~e6`（第五拍）· **`f1-composer` / `f3-alert1100` / `f4-skill1280`（第六拍改前）· `g1-stats` / `g2-skill1440` / `g3-skill1280` / `g4-alert1100` / `g5-alert1100`（第六拍改后）** · **`h2-{add-menu,opts-menu,commit}`（第七拍改前）· `h3-{add-menu,opts-menu,commit,ctxmenu}`（第七拍改后）**）。**无 `before/`** —— 前置态 = HEAD 的 conversation.html，`git show` 可取 |
| `mg-work/r108/` | **🚫 未提交（第十二拍）**：`apply108.py`（**由 `ev/make108.py` 从 apply107 做 7 处精确替换生成**；GENS 六代、nav 沿用 `r106-nav-js`）/ `acceptance.md`（**七节**）/ **`part108/`**（只覆盖改过的三件：`_mods.html` 52848 · `panel.css` 1090 → 1196 行 · `panel.js` 1335 → 1412 行；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）/ `ev/`（`make108.py` · `splice108.py` · `patch108l1.py` · `p108m.js` + `probe108m{,2,3,4,5,6}.sh` · `shots108m.sh` · `scan-flatten.py` · `vd-r108a/b.txt` · `m-raw.log` / `m2-raw.log`）/ `raw/`（`m-1440-{diff,diff-pane,diff-split,tree,tree-panel,tree-fold,rvbar}.png`）|
| `docs/codex-refs/` + `docs/codex-sidepanel-research.md` | **已提交（`f13b3bf`）**：12 张 Codex 右栏实机截图 + 十节调研速报（r107 的设计依据） |
| `.workbuddy/memory/2026-09-30.md` | 当日原始日志（含 r92 / r93 / **r93 ④** / r94~**r105** 各段；**2026-10-01.md 续记 r106 + r107（七拍）**） |

> 历史（已提交的那批，仅供追溯）：`settings.html` 457805 字符（r88~r93①）；`{avatar,skills,automation}` = 566669 / 360166 / 360279；
> `{dev,kanban,req-kanban,task-detail}` = 449491 / 567338 / 513077 / 766714；`assets/images/bg-img-1.png`（顶栏装饰）；`giencoder-design-system/components.css` + `.gienx-templates/_shared/components.css` + `components/select.json`（r87 select）。
> `?? mg-work/r92/` · `?? mg-work/r93/`（`apply93.py` + `acceptance.md` 十三节 + `before/` 25 份 + `ev/` + `raw/`）—— **均已提交**。

`origin/main` @ **`e9c9498`**（**r106 六条 + Codex 右栏调研 + r107 十一拍已全部推送**；**r108 十二拍 🚫 未提交**，工作区 ` M pages/conversation.html`；上一站 `9f252e5` = r101，再上一站 `d7e2151` = r86~r100，`1ecc7ee` = r80–r85）。**长期约定「默认不自动 commit / push」（2026-09-28 起）；邵先生显式说「commit and push」时才执行**。

⚠ `.gitignore`：`mg-work/r80/raw/sel_*.json`、`mg-work/*/gate/*/pages/`。`before/` 与 `raw/` **是**入库惯例。
⚠ **推送凭据**：PAT 已写入 `~/.git-credentials`，推送带 `-c credential.helper=store`（详见第九节）。
⚠ 🚨 **推送体位（r105 更正）**：一律**裸调 `git`** —— 本机 **`env …` 开头的命令会被「静默吞掉」**（exit 0 + 零输出 + 完全不执行，连 `GIT_TRACE` 都不打）；当日 `env | grep -i proxy` **无命中** ⇒ **不需要 `env -u`**。详见 PLAYBOOK P5。
⚠ **安全（r100 首推被拒时查明）**：该 PAT **就是当前在用的推送凭据**（与 `~/.git-credentials` 同一枚），它曾出现在对话记录里、
又被明文抄进 `mg-work/r87/acceptance.md:174` 的「安全备忘」（那行自己写着「建议 Revoke」，却从没执行）⇒ 首推被 **GitHub Push Protection** 拒。
已就地打码 + `commit --amend` + `reflog expire --all` + `gc --prune=now` 清干净（详见 PLAYBOOK **P5.1**）。
**⚠ 但「已泄露」打码是解决不了的 —— 请尽快 Revoke 该 token 并换发新 PAT**（换发后只需覆盖 `~/.git-credentials`，推送命令不用改）。

`.workbuddy/memory/` 两份：**仓库内（权威，随 git 走）** 与工作区 `E:/GienCoder/.workbuddy/memory/`（速记）。改记忆**以仓库内为准**。

---

## 二、★ r93 + r94 + r95 + r96 + r97 + r98 + r99 + r100（前情 · 需求 1 + 需求 2 + ④「独立页 + 全要素复用」+ r94 五条微调 + r95 两条「右侧撑满」+ r96 五条「字号/色/速率行」+ r97 四条「卡内字号统一 / 胶囊 / **宽度基准** / 统计行」+ r98 三条「内容区 14→15px / rateline 下 48px / **差分卡逐像素还原**」+ r99 十四条「假滚动条 / 按钮态 / 右键菜单 / 图标修复」+ **r100 八条「更名 / 卡内 14px / hover 口径 / 整行可点 / ndesc 胶囊 / 调用 5 个工具层级树」**）

零字面 hex（新色一律进 `--r93-*` 本地变量 + 暗色档）；幂等可复跑。
> 追记：需求 2 落地后邵先生又问了两件事（记为 **④**，见下）——「会话页面该不该是独立 html、要注意路由」「底部对话框要**完全全要素复用**基础工作台 main 里那个真组件」。用户拍板：**做成独立页** + **保留状态条/agent 卡、只换输入卡**。

### 需求 1 —— aside 分组标题行高被改坏（应 32px）

**根因**：`<style id="r87-ui-css">` 里 `body .text-xs{font-size;line-height}` 特异性 **(0,1,1)** > 尾风 `.leading-\[32px\]` 的 **(0,1,0)** ⇒ 行高 32→16、整行腰斩。**r87 字号机制引入的回归**。

修法（`mg-work/r88/apply88b-fontsize.py` 就地返工）：
1. `text-*` 的行高**只在无 `leading-*` 类时**派生 → `body .text-xs:not([class*="leading-"]){line-height:…}`；
2. 新增 `LEADING_DERIVE = [(.leading-\[19px\],19), (.leading-\[22px\],22), (.leading-\[32px\],32)]`，**写在 text-\* 之后**（同 (0,1,1)，后写者胜）。

实测 4 个分组标题 `h 16→32`、`lh 21px→32px`；顺带 `textarea` 20→22、页脚 16→19.5。

### 需求 2 —— 点 aside 会话标题 ⇒ main 展示该会话的用户/AI 对话详情（设计稿 `1393:18748`）

> ④ 之后**主载体从 base.html 搬到 `pages/conversation.html`**（独立页），注入机制**逐字不变**（同一份 CSS/JS 只是换了承载文件 + 判据由 `[data-r93-conv='1']` 改为根级 `<html data-r93-page="conversation">`）。下面这段描述的是内容本体，两页通用。

**`<main>` 在 base.html 里出现 0 次**（React 运行时渲染）⇒ **不动 React 源**，只在 `mainInner` 尾部追加 `.r93-conv-host`，用 `[data-r93-conv='1'] > *:not(.r93-conv-host){display:none!important}` 藏掉「欢迎空态 + 版权页脚」。

* **点击分流**：`document` **捕获阶段** 监听 `aside button`：
  `min-w-0 + flex-1`（会话项）⇒ 打开；`rounded-md + py-0`（分组标题）⇒ 只折叠、不切换；其余 ⇒ 关回空态。
* `MutationObserver` 兜底补回被 React 冲掉的节点。
* **25 个块**：页头 44 / 用户气泡 / 助手头 / 上下文注入 / 深度思考 / AI 文本 ×2 / Bash / 网页搜索 / 需求采访 / 更新任务清单 / 文件写入 / SKILL / Tool call / 重试 / 调用 5 工具 / 压缩上下文 / 上下文已压缩 / 搜索资料 / 告警 ×2 / 未知 surface / 模型已切换 / 改动汇总 / 任务产物 / Token 速率行 + composer（状态条 + 4 张 agent 卡 + 输入框）。
* 用户拍板：**全量还原** / 所有会话都渲染这一份设计稿内容 / 轨迹页签切**统一空态** / 折叠可点 + 关键 hover·popover 做。

**三点自行拍板**（用户未回，按工程判断）：
| 项 | 结论 |
|---|---|
| 定位 | **居中**：`width:840px; margin:0 auto`（实机 main 内宽 1162 ⇒ 左右各 161，**不照搬设计稿 164**） |
| 硬编码色 | 全部进页面 `:root` 的 `--r93-*` 变量，并补 `[giencoder-theme='dark']` 档 |
| 字体 | 沿用页面 `Mona Sans VF` |

**★ 变体叠加陷阱**：导出图里**每个折叠块容器内同时叠放了「折叠态(T0 H22)」与「展开态(T34 H184)」两个变体** ⇒ **真机块高 = 容器高 − 34**（逐块固定，不累积）⇒ **导出 PNG 的绝对 y 不可当设计坐标**。去掉 offset 逐块累加 ⇒ 设计真机内容总高 **4106px** = 实机实测 **4106px** ✅

**★ 字号体系**（`ui-component` 不带 font-size，靠「框高 × 墨迹行距 × 文本宽度反推」三角验证）：

| 用途 | fs/lh |
|---|---|
| 折叠头标题 / 气泡正文 / 需求采访 | 14 / 22 |
| 折叠头 meta（skill-catalog / 2s / deepwiki） | 12 / 22 |
| **卡内正文 / 代码** | **12 / 20** |
| 上下文注入卡正文 | 12 / 16 |
| Bash 卡代码 | 12 / 16 |
| 居中提示卡片下说明行 | 12 / 24 |
| 深度思考正文 | 12 / 22 |

> 初版统一写 `14/22` ⇒ 上下文注入 190(应150)、SKILL 90(应64)、深度思考 222(应200)、网页搜索 200(应184)，全错。已建 `.r93-t12c` / `.r93-t12s` / `.r93-t12h` 工具类逐块替换。

**逐块几何核对**（实机 1440×900）：块高 0/1/2/3/5/6/7/8/9/10/11/12/14/15/16/17/18/19/20/22/23/24 全一致；仅 2 处 Δ2（搜索资料 152→150、改动汇总 302→300）。横向全对齐（host 1162 / wrap 840 / 气泡 728 / 卡 822 / diff 840 / 告警 840）。

**结构级修正**（尺寸对不上只是表象）：
* **更新任务清单**：设计稿**没有 40px 卡头**，1px 分隔线在卡内 `y=181` ⇒ 重写 `.r93-todocard`（padding 16/20/12），JSON 改 9 行截断式。
* **网页搜索**：8 行**整行是蓝色下划线链接**（`#3770F7` = `--color-primary-6`），不是灰文本。
* **搜索资料**：蓝下划线标题 + 灰描述，组内 gap 3 / 组间 6。
* **任务产物**：Token 速率行是**独立容器**（840×24 @ +20），不在卡内。
* **深度思考列表项**：导出图渲染为 **「1. 2. 3.」**，不是私有区图标 `󰀐`（实机缺字形 ⇒ 会变豆腐块并多折 1 行）。

**暗色适配**：r93 画面 CSS 里 11 处字面 `background:#FFFFFF` + `#F5F6F7` 卡底在暗色下会「白屏」⇒ 白底一律换 `var(--color-bg-2)`（浅 `#fff` / 暗 `#232324`，浅色视觉零变化），`--r93-*` 全套补暗色档。

### ④ 会话详情**独立成页** + 底部 composer **全要素复用**外壳真组件

**邵先生两问 + 拍板**：① 「这个 AI 对话页该不该是独立 html？若是，注意与其它页的跳转路由」→ 答：**应是**（理由见 PLAYBOOK P3.24⑦），用户拍板**做成独立页**；② 「底部对话框要**完全全要素复用** main 里那个 `relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors`」→ 用户拍板**保留状态条 + agent 卡、只换输入卡**。

**① 独立页落地（`pages/conversation.html`，604806 字符）**

- **体位**：`conversation.html` **每次从 base 净底重建**（`net = base 摘掉 r93 三块` ⇒ 换 `<html>`/`<title>` ⇒ 尾部注入 `r93-conv-css`+`r93-conv-js`），**不靠复制**；`base.html` 只留 `<!-- r93-nav --><script id="r93-nav-js">`（点 aside 会话项 ⇒ `location.href='conversation.html'`）。
- **根级判据**：`<html lang="zh-CN" data-r93-page="conversation">` ⇒ 页面级 CSS 全部挂 `html[data-r93-page='conversation'] …`（不再用 `[data-r93-conv='1']`）。
- **路由（10 页各 1 条，含新页自身）**：每页 `ROUTE` 表尾插 `, '/conversation': 'conversation.html'`（+38 字符/页）。顶栏「工作台切换」页签（`SHELL-TABS-FIX v4`）**不受影响** —— conversation 不在 `DEV_PAGES`，在它上面点「基础工作台」是空操作（实测确认）。
- **点会话 ⇒ 跳页**：`r93-nav-js` 在 `document` **捕获阶段**拦 `aside button`，只认 `min-w-0 + flex-1`（会话项），**不拦分组标题/导航项**。

**② composer 全要素复用（纯 CSS，零复制、零重绘）**

不动 React 源，靠 5 条同页选择器改**视觉顺序**，让真组件自己长在会话详情底部：

```css
/* 宿主前置于 hero 之前 */
html[data-r93-page='conversation'] .r93-conv-host { display:flex; flex-direction:column; flex:1 1 auto; min-height:0; order:-1; background:var(--color-bg-2); overflow:hidden; }
/* hero 贴底、去掉顶住的 mt-8、藏掉问候语与版权页脚 */
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center { flex:0 0 auto!important; justify-content:flex-end!important; padding-bottom:12px!important; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > .pointer-events-none { display:none!important; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 { margin-top:0!important; }
html[data-r93-page='conversation'] main > div > div.pb-6 { display:none!important; }
```

- **保留**：状态条 `.r93-sb`（「执行 第 2/5 个待办」）+ 4 张 `.r93-agent` 卡（在**我们的宿主 DOM** 内，hover popover 也仍在宿主内）；**删掉**宿主里自绘的 `.r93-input`/`.r93-ta`/`.r93-itools`/`.r93-perm`/`.r93-model`/`.r93-send`（整段）。
- **实测最终视觉顺序** = 设计稿：内容 → Token 速率 → 滚动到底部 → 状态条 → agent 卡行 → **输入卡（真组件）** → 工作目录/默认权限行。
- **实测 rect（1440）**：host 1162×628（`order:-1`）/ hero 1162×214 / outer **860×214** / card **836×154** / 问候语 + 页脚 `display:none` / `doc 900 = win 900`（无纵向滚动）。
- **★ 真组件下拉「必须翻向」**：真 select 默认**向下**弹（`top:calc(100% + 4px)`），composer 钉在 main 底部（`main` 是 `overflow:hidden`）⇒ 被裁（实测「默认权限」popup y **871..997** 而 main 底 **892**，只剩 21px）。页面级适配翻成向上：

```css
html[data-r93-page='conversation'] .giencoder-select-popup { top:auto!important; bottom:calc(100% + 4px)!important; transform-origin:bottom; }
html[data-r93-page='conversation'] [aria-label='权限选择'] { top:auto!important; bottom:calc(100% + 4px)!important; }
```

  修后 4 个 popup 全部完整可见：标准模式 200×80 / 模型 194×207 / 工作目录 194×109 / 默认权限 280×126；「＋添加」（180×92）与三个 select 全部走外壳自己的 handler（实测可点）。
- **`.r93-cp` 简化**：由「灰底 + 描边 + padding」改为只有 `margin-top:12px`（灰壳交给真组件，避免两层灰壳）；`.r93-tbsticky` 保持 `bottom:44px`（壳体 bottom = 滚动口底 − 药丸底边 − 32，实测按钮底 541 / 状态条顶 553 / 间距 12px）。
- ⚠ **`apply88b-fontsize.py` 的 `unscale()` 正则只认 `calc(<数字>px * var(--ui-fs-ratio))` 或裸 `Npx` 结尾** ⇒ 我们的 `calc(100% + 4px)`（含 `%`）**安全**；且 `converge()` 会把整个注入 `<style>` 块原样跳过 ⇒ **新块 id 必须唯一**（`r93-conv-css` / `r93-conv-js` 不与旧块同名）。

**★ 独立页由 base 净底重建的判据（④ 幂等体位）**

`python mg-work/r93/apply93.py` 把「**base 摘块后的净底**」当作**两页的唯一来源** ⇒ 第二遍任何一页都「已是目标态（无改动）」（实测连跑两遍均如此）。`--revert` = 删 `conversation.html` + 摘 base 的 `r93-nav-js` + **10 页 `ROUTE` 各 −1 条**。

### r94（同日第四轮）—— 会话详情页 5 条微调（**就地返工 `apply93.py`**）

> r93 未提交 ⇒ 就地在 `mg-work/r93/apply93.py` 的 `r93-conv-css` / `r93-conv-js` 上改（不另起代数）。

| # | 需求 | 做法 |
|---|---|---|
| ① | `r93-seg-cap` 在 `r93-bar` 内**居中** | `left:396px`（设计稿 1168 面板的固定值，换视口即偏）→ **`left:50%; transform:translateX(-50%)`**；实测 `capCenterDelta = 0` |
| ② | `r93-wrap` 宽 = **main 的 50%**、**min 860px** | `.r93-wrap { width:50%; min-width:860px; box-sizing:border-box; padding:32px 10px 24px; }` ★ 内容块固定宽（728/822/840）⇒ 靠**左右各 10px 内距**把内容盒保持 840 ⇒ 横向位置与 r93 口径（425..1265）**零位移** |
| ③ | 对话框**只留输入卡本体** | outer 去灰壳（`background:none; padding:0; border-radius:0`）+ 隐藏底排（`> div:not(:has(textarea))` ⇒ 工作目录/默认权限行）；**DOM 血缘不动** |
| ④ | `div.mt-8` 内的**波点**全去 | ★ 侦查：**mt-8 里只有 1 个子（composer 外壳）**，没有波点子节点；点阵真源 = **`main.dot-bg` 本体 + `::before` 光斑层** ⇒ 页面级 `main.dot-bg{background-image:none}` + `::before{display:none}` |
| ⑤ | `r93-card--ctx` **max-height 240 + 内滚**；`r93-vsb` 假滚动条去掉 | `.r93-card--ctx` 加 `max-height:240px; overflow-y:auto; overflow-x:hidden`；**删** `.r93-vsb` 规则 + **5 处 DOM**（ctx / Bash / diff / 改动汇总 / 任务产物） |

**实测**：`wrap [415,93,860,…]`（原 840）、outer `[420,725,860,154]`（bg 透明 / pad 0 / br 0，子② `display:none`）、`main.backgroundImage=none`、`::before` display none、`.r93-vsb` 计数 **0**、ctx 溢出取证 `scrollHeight 244 > clientHeight 240 ⇒ scrollable`（运行时临时塞内容、测完移除、不落盘）。

**★ 踩到的一次假阳性**：首跑 `verify-design` 时 conversation 的渐变计数 **62→63** —— 根因是我在**新注释里写了被扫描的关键词**（`radial-gradient`）⇒ 改措辞后与 r93 基线**逐字节相同**。**这是「新增注释里不得出现被断言的 token」的又一次实例。**

**产物**：`pages/conversation.html` **604806 → 606073**（字节 sha `acb485be7385`）；`pages/base.html` **471444 未变**；`ev/p94b~e.js` + `.sh` + `vd-r94*.txt`；`raw/r94-hero.png` `r94-full.png`。

### r95（同日第五轮）—— 会话详情页 2 条「右侧撑满」（**就地返工 `apply93.py`**）

> 需求：① 「类似 `r93-card r93-card--ctx` 这种容器的**右侧要撑满**」；② 「**底部对话框相关的内容模块也要自适应撑满**」。

**侦查（`ev/p95a.js`，1440 实测）—— 三组元素三条右边界打架**：

| 组 | 元素 | rect | 右边界 |
|---|---|---|---|
| 内容 | `.r93-wrap` 外沿 / 内容盒 / `--ctx` 卡 / `bub` / `todocard` | `[415,93,860]` / 425..1265 / 1265 / 1265 / 1265 | **1265~1275** |
| 底部 | `.r93-sb` / `.r93-cp`（`width:840px; margin:0 auto`） | `[430,·,840,·]` | **1270** |
| 对话框 | composer `outer` / 输入卡 | `[420,725,860,154]` | **1280** |

根因两条：**(a) 滚动条占位** —— `.r93-scroll` 出现滚动条后内容盒收窄（单侧 10px），`margin:0 auto` 的 wrap 相对「无滚动条」的底部/composer **左偏 5px**；**(b) r94 给 wrap 加的 10px 内距**（为保内容盒 840）让块比 composer 窄 10px。

**落地（14 处）**：

| 类别 | 改动 |
|---|---|
| ① 居中同轴 | `.r93-scroll` 加 **`scrollbar-gutter: stable both-edges`**（两侧各让等量 gutter ⇒ 内容恒居中，不再偏 5px） |
| ② 内容盒 | `.r93-wrap` padding `32px 10px 24px` → **`32px 0 24px`**（块改流式后不需要内距） |
| ③ 卡片 | `.r93-card` / `.r93-todocard`：`width:822px` → **`calc(100% - 18px)`**（**左缩进保留、右侧撑满**） |
| ④ 整行块 | `.r93-card--full` / `.r93-note` / `.r93-ndesc` / `.r93-alert` / `.r93-diff` / `.r93-arts`：`840px` → **`100%`** |
| ⑤ 产物卡 | `.r93-artcard` `414px` → **`calc(50% - 6px)`**（两列等分撑满） |
| ⑥ 底部列 | `.r93-bottom` 加 `width:50%; min-width:860px; box-sizing:border-box; margin:0 auto`；`.r93-bottom > *` `840px + auto` → **`100% + 0`** |
| ⑦ 对话框壳 | `… > div.mt-8 > div` 补 **`width:50% !important; min-width:860px !important`**（原先 Tailwind 写死） |

⚠ **刻意未动**：`.r93-bub`（728px 气泡 —— 右对齐 ⇒ 自动跟随新右边界；设计稿语义本就是「不满宽」）；`.r93-agent`（4 张 agent 卡按内容宽左对齐，属设计稿固定排版，**不是「容器」**）。
⚠ **收敛安全**：`calc(100% - 18px)` / `calc(50% - 6px)` / `100%` / `50%` 都不含「裸 `Npx` 结尾」⇒ 不匹配 `apply88b` 任一 `RE_*`，不会被 `unscale()` 改坏。

**实测（`ev/p95b.js`，1440 / 1920 双档）—— 全块 Δ=0**：

```
.r93-scroll    clientWidth 1142 / offsetWidth 1162（gutter stable both-edges）
.r93-wrap      [420,860] → 右 1280        .r93-bottom/[sb]/[cp] [420,860] → 右 1280
composer outer [420,860] → 右 1280        inputCard     [420,860] → 右 1280
ctx/todocard   [438,842] → 右 1280 Δ=0    bub [552,728] → 右 1280 Δ=0
alert/diff/arts/note [420,860] → 右 1280 Δ=0   artcard [420,424]（两列 ⇒ 第二张右边界 1280）
tbsticky 药丸 [790,120] 中心 850 = 内容列中心          doc/win 双 1440/1920（无横向溢出）
```

**产物**：`pages/conversation.html` **606073 → 606949**（+876；字节 sha `247c6c1e040e`）；`pages/base.html` **471444 未变**（`c16308a00915`）；`ev/p95a.js/.sh`（侦察）+ `ev/p95b.js/.sh`（实测）+ `vd-r95.txt`（= r93 基线）；`raw/r95-full.png` `r95-hero.png`。

### r96（同日第六轮）—— 会话详情页 5 条（**就地返工 `apply93.py`**）

| # | 用户原文 | 落地 |
|---|---|---|
| ① | `r93-bubi` 容器最大高度 240px，溢出就内滚 | `.r93-bubi` 加 `max-height:240px; overflow-y:auto; overflow-x:hidden`（只改「体」，不动 `.r93-bub` 气泡列） |
| ② | 类似 `r93-card` 的容器默认字号调整为 13px | `.r93-card` 加 `font-size: var(--font-size-body-2)`（= **13px**）。⚠ 该规则**不得**声明裸 `height`（converge 约束）—— 本规则无 height ✓；卡内 `.r93-pre` 等自带 12px 的不受影响 |
| ③ | `r93-t14` 文字颜色浅两级；`r93-t14 r93-c2` 用正文颜色 | `.r93-t14` 默认色 → `--color-text-3`；**新增** `.r93-t14.r93-c2 { color: var(--color-text-1) }`（(0,2,0) 压过 `.r93-c2` 的 (0,1,0)，与书写顺序无关） |
| ④ | `r93-card r93-card--edge` 的宽度还没调整 | 嵌套 Tool call 卡**拉丢内联 `w:804`**（改走 `.r93-card` 的 `calc(100% - 18px)`）；另两处 `style="width:840px"` 的 AI 文本块一并改流式 |
| ⑤ | `r93-rateline` 各元素还原度很低，请对比设计稿精确还原 | 整行重写（下详） |

**★ ⑤ 的设计稿取数（两份权威源，非目测）**：
- **源 1** `raw/design-1393-18748.html`（设计稿导出的带样式 HTML）：节点 `1393:18599`「容器 247」= 256×24 @ (164,4664)；
  `1393:18598`「容器 246」56×24 = **2 个 24×24 `icon-wrapper`（图标 14，gap 8）**；两根「直线」是
  `viewBox="0 0 2 14"` 的 svg ⇒ **1px × 14px 竖线**（#E5E5E5）；`fw647:19591` Link 142×24 @80 `gap:4` =
  时钟 14×14 + 「Token 速率：256/s」（**14px / lh24 / #868686**）。
- **源 2** `raw/design-rgb.png`（1x 整页导出，**色值已验证准确**：同一张图上量的前两枚图标 = (107,107,107) = #6B6B6B，
  与该 HTML 里其它 `style="color:#6B6B6B"` 逐字一致）逐像素列扫描：图标1 x 6..18 · 图标2 x 40..49 ·
  线1 **@68**（y 4670..4683 ⇒ 高 14）· 时钟 x 82..93 · 文字 x 99..221 · 线2 **@234** · 省略号三点 x 240..249（点间距 4）。
- ⚠ **旧实现两处硬错**：① 把「容器 246 的 **56 宽**」误当成**线宽** ⇒ `.r93-nline{width:56px}` 画出 **56×1 横线**；
  ② `gap:16`，而设计各段间距是 **12**（56→68→80→222→234）。

**⑤ 新实现**（`.r93-rgrp`[gap8] + `.r93-rline`[1×14 竖线] + `.r93-rrate`[gap4] + `.r93-rbtn`[24×24 盒 / 图标 14 居中]）：
```css
.r93-rateline { display:flex; align-items:center; gap:12px; }
.r93-rgrp  { display:inline-flex; align-items:center; gap:8px; flex:none; }
.r93-rbtn  { width:24px; height:24px; color:var(--r93-ioc2); border-radius:4px; }
.r93-rline { flex:none; width:1px; height:14px; background:var(--color-border-2); position:relative; z-index:1; }
.r93-rrate { display:inline-flex; align-items:center; gap:4px; color:var(--color-text-3); }
.r93-rateline > .r93-rline + .r93-rbtn { margin-left:-16px; color:var(--color-text-3); }
```
新变量 `--r93-ioc2: #6B6B6B`（浅）/ `#C9C9C9`（暗色档 —— DS 暗色色阶是反的，gray-7 取 #C9C9C9）。
新图标 **`branch`**：设计稿里它是 DS `icon-wrapper` 实例（**没有导出独立 svg**）⇒ 按 `design-rgb.png` 的
14×14 点阵逐像素反推（三个**空心**圆节点 + 贯通主线 + 自右节点下沿并入主线的曲线），换算到 16 网格写入 `ICON_INLINE`。

**⑤ 逐元素对位（行左 = 视口 420）**：图标1 盒 0..24 / 图标2 盒 32..56 / **线1 @68** 均**逐像素对齐**；
线2 实测 227 vs 设计 234（−7）、省略号盒 224 vs 231.5（−7.5）—— **唯一原因是字体度量**
（实机 Mona Sans 下「Token 速率：256/s」宽 116，设计稿 MiSans 下 123 ⇒ Link 总宽 134 vs 142）；
**省略号相对第 2 根线的位置关系一致**（实测盒在线左 3px / 设计 2.5px）⇒ 同套间距的自然位移，不是间距错。

**实测（1440×900，`ev/p96a~c`）**：① `maxHeight 240px / overflowY auto`，**溢出取证**正文撑 25 倍 ⇒
`scrollHeight 590 > clientHeight 240`、`scrollable:true`、`scrollTop` 可到 350 ｜② `.r93-card` = **13px**（3 个无类名文本同落 13px）｜
③ 问题行 **rgb(134,134,134)** / 回答行 **rgb(31,31,31)** ✔ ｜④ 4 张 edge 卡 **842/842/842/824**，**右界全 1280**（改前第 4 张 804/右界 1260）｜
⑤ 线 = **1×14 竖线**（bg rgb(229,229,229)）、图标 = 复制+分支（rgb(107,107,107)）、省略号 rgb(134,134,134)、gap **12**。

**产物**：`pages/conversation.html` **606949 → 609969**（+3020；字节 sha `e032e8913bf1`）；`pages/base.html` **471444 未变**（`c16308a00915`）；
`ev/p96a~d.js|.sh` + `vd-r96.txt`；`raw/r96-ic12big.png`（图标 18× 放大）· `r96-rate-ctx.png` · **`r96-cmp2.png`（设计 vs 实机同尺度上下对照）** · `r96-ratepage.png` · `r96-after-full.png`。

### r97（同日第七轮）—— 会话详情页 4 条（**就地返工 `apply93.py`**）

| # | 用户原文 | 落地 |
|---|---|---|
| ① | 所有 `r93-card` 容器内的字号统一调整为 13px | 新增 **`.r93-card.r93-card, .r93-card.r93-card * { font-size: var(--font-size-body-2) }`** —— 实测**卡内 42 处文本全落 13px**（r96 只调了「裸文本」的默认档，卡内仍混 12px/14px） |
| ② | 「滚动到底部」应是胶囊按钮 + 文字色与图标一致 | `.r93-tobottom`：圆角 `8px` → **`999px`**（DS 无胶囊半径 token，最大 xl=12px）；前景色 → **`--r93-ioc2`**（#6B6B6B）+ 新增 `.r93-tobottom .r93-t14 { color: inherit }` ⇒ 图标与文案同色（设计稿实测两者都是 #6B6B6B） |
| ③ | 底部对话框相对上方内容两端都短了一截，要求等宽 | ★ **三者宽度基准统一** + agent 卡行撑满（下详） |
| ④ | 底部对话框下面还有一行小灰色文字 | `div.mt-8::after` 纯 CSS 补回（`content` = 「2 轮 · 27 步 · … · 输出 31.1K token」，12px / lh16 / 新变量 **`--r93-meta: rgb(var(--gray-5))`** = #A9A9A9）；hero `padding-bottom` 12 → 8 |

**★ ③ 的根因（「两端各短一截」只在宽视口出现）**：三块都写百分比，却挂在**宽度不同的父盒**上 ——

| 元素 | 父盒 | 与 main 内宽的差 | 2560 实测（改前） |
|---|---|---|---|
| `.r93-wrap` | `.r93-scroll` 滚动内容盒 | `both-edges` 左右各让 10 ⇒ **−20** | `[845,1131]` |
| `.r93-bottom` | `.r93-pane` | **0**（基准正确） | `[840,1141]` |
| composer | `div.mt-8`（hero `w-full` 子盒） | hero `px-6` ⇒ **−48** | **`[852,1117]`** |

⇒ 1440 下三者都取 `min-width:860` 看不出问题；2560 下**输入卡比状态条两端各短 12px**。修法三条：
① `.r93-scroll::-webkit-scrollbar { width: 10px }`（把滚动条宽度**显式钉死**，全站默认也是 10）
② `.r93-wrap { width: calc(50% + 10px) }`（补回 both-edges 的一半）③ hero `padding: 0 0 8px 0 !important`（清掉 `px-6`）。
⇒ 三者恒等于 `max(50% × main 内宽, 860px)`。**实测 1440 / 2560 双档 wrap / bottom / sb / composer 右边界全等**（1280 / 1981）。
**顺带**：4 张 agent 卡 `flex:none` → **`flex: 1 1 auto; min-width:0`**（设计稿 PNG 实测该行第 4 张**顶到内容列右缘** ⇒ 本来就该填满；改前 2560 右端空 365px）。

**★ `*` 不贡献特异性（本轮踩到）**：首跑「卡内 37 处 13px、唯独 5 处 `.r93-pre` 仍 12px」——
`.r93-card *` 其实只有 **(0,1,0)**，`.r93-pre` 与它同级且写在**后面** ⇒ 后写者胜。修法：类名写两遍抬到 (0,2,0)。

**产物**：`pages/conversation.html` **609969 → 613441**（+3472；字节 642788；**LF 文本 sha `481d929d89bd`**）；`pages/base.html` **471444 未变**；
新增 `ev/p97a`（侦查）· `p97c.sh`（宽视口）· `p97d`（实测，1440/2560）· `p97f`（字号回归隔离）· `vd-r97.txt`；
新增 `raw/r97-cmp.png`（设计 vs 实机上下对照）· `r97-pill2.png` · `r97-bottom2.png` · `r97-agentrow.png` · `r97-after-full.png`；
新增 `before/conversation-r96.html` · `base-r96.html`。详见 `mg-work/r93/acceptance.md` 第十章。

### r98（同日第八轮）—— 会话详情页 3 条（**就地返工 `apply93.py`**）

| # | 用户原文 | 落地 |
|---|---|---|
| ① | 整个对话内容部分的 **14px 字号统一调整为 15px** | 新增 `.r93-t14, .r93-t14m, .r93-t14b { font-size: calc(15px * var(--ui-fs-ratio)) }`（写在三条定义**之后**、**只写 font-size**）⇒ 内容区 **59 处落 15px**；`.r93-card.r93-card *`（0,2,0）仍把卡内压回 13px ✓ |
| ② | 单轮末尾 `r93-rateline` 模块**下面间距 48px** | `.r93-wrap` `padding: 32px 0 24px` → **`32px 0 48px`**（rateline 是本轮最后一个 `.r93-it`：实测 `isLast=true`、无 `nextSibling` ⇒「下面间距」就是内容盒下内距） |
| ③ | `r93-diff` 样式还原不到位（颜色 / 间距…），对比设计稿像素级还原 | 整卡重做（下详） |

**★ ③ 差分卡逐像素还原（设计稿 `1393:18681`「容器 252」= 840×300；双源 = `raw/design-1393-18748.html` + `raw/design-rgb.png` 逐像素扫描；坐标一律卡内相对值）**：

| 部位 | 设计稿 | 旧实现 → 本轮 |
|---|---|---|
| 卡底 | 表头带 `#F5F6F7` + **列表纯白面板** | 整卡 `#F5F6F7` → `.r93-diff{bg-2}` + `.r93-dhead{--r93-card}` |
| 表头 | **40 高** + **底部 1px `#ECEEF2` 分隔线** | `height:28` 无分隔线 → `40 + border-bottom` |
| 行 | 高 36、**首行无上边线** | 7 行全带边线 → `:first-of-type{border-top:0}` |
| 行内距 | **左 11 / 右 13** | `0 36 0 8` → `0 13 0 11` |
| 数字列 | 与 ⋯ 之间 **17**、右沿距卡内右 **54** | gap 8 → `gap:17` |
| ⋯ 字色 / 悬停 | **(31,31,31)** = text-1；悬停 **白底 + 1px 描边** | text-2 / fill-2 → `text-1` + `bg-2 + inset 描边 border-2` |
| +800 | **(48,149,59)** = `--r93-ok` | `--color-success-6`(59,179,70) 偏亮 → `--r93-ok` |
| 按钮 | **70×28** | 72 → `padding: 0 11px` |
| 表头图标槽 | 槽宽 **24**、标题落卡内 **36** | 图标盒 14 ⇒ 标题 39 → `margin-right:-3px` ⇒ **456** ✓ |
| 表头数字组 | gap **8** | 全 12 → 新增 `.r93-dh2{gap:8}` |
| 滚动条 | `矩形 219` = **6×128**、rgba(0,0,0,.16)、r6、卡内**右 4 / 顶 4** | 无 → 新增 `<i class="r93-dsb">` + `.r93-dsb`（**静态装饰**，见待拍板） |

★ 设计稿那行 `app.json` 是**叠出来的 hover 态**（行底 + 文件名 primary + ⋯ 白底描边盒）⇒ 本页保持**真 CSS `:hover`**，不静态写死（同 r93「变体叠放」教训）。

**★ 顺带修掉的真 bug —— `.r93-alink` 一直不是 12px**：`.r93-bt { font: inherit }`（第 412 行）与 `.r93-t12`（第 363 行）**同为 (0,1,0)** 但**写在后面** ⇒ 后写者胜，把「任务完成，耗时28m12s」撑成 14px。设计稿墨迹 x166..325 = **160px ≈ 11 汉字 + 5 半角 @12px**（@14px 要 189px）⇒ 在 `.r93-alink`（写在 `.r93-bt` 之后）补 `font-size: var(--font-size-body-1)`。

**★ 踩坑 —— 门禁对注释的双重标准**：`check_hardcoded_hex` 遇到 `<!--` / `/*` 会 `continue` **跳过注释行**，但 `check_hardcoded_px_fontsize` **不跳** ⇒ 我在新增注释里写了裸 `font-size: 15px` 导致门禁 **77（应 76）**，改措辞后归零（`vd-r98.txt` 与 `vd-r93c.txt` 逐字节相同）。**另**：`.r93-drow:first-child` 失效（`.r93-dlist` 首子元素是 `<i class="r93-dsb">`）⇒ 改 `:first-of-type` + 把 `<i>` 从列表头挪到尾部（双保险）。

**★ r98 复查（同日第八轮）**：全绿 —— 幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（21882 字节 `equal:True`，`vd-r98.txt`）｜实测 `ev/p98b.js` **1440 / 2560** 双档（内容区字号分布 12×49 / 13×42 / **15×59** / 14×2；wrap pb **48**；差分卡右对齐账 ⋯−13 / 数字−54 / 名+11 全对）＋ `raw/r98-cmp.png`（设计 vs 实机对照）。

**产物**：`pages/conversation.html` **613441 → 616773 字符**（+3332；字节 647842；**LF 文本 sha `6cbeff3a126c`**）；`pages/base.html` **471444 未变**（sha `c16308a00915`）；
新增 `ev/p98a.js/.sh` · `p98b.js` · `vd-r98.txt`；新增 `raw/r98-design-diff.png` · `r98-design-below-rateline.png` · `r98-live-diff.png` · **`r98-cmp.png`** · `r98-after-full.png` · `r98-rateline.png` / `r98-rateline-crop.png`；
新增 `before/conversation-r97.html` · `base-r97.html`。详见 `mg-work/r93/acceptance.md` 第十一章。

### r99（同日第九轮）—— 会话详情页 14 条（**就地返工 `apply93.py`**）

邵先生原话十四条（`.r93-conv-host`）：①去掉 `r93-dsb` 假滚动条、需要时显示真滚动条；②`r93-tobottom r93-bt is-on` 默认图标/文字深一级 + 整钮 hover 底色；③`r93-rbtn r93-bt` 与间隔线贴在一起；④`r93-iblk r93-i14` 图标异常；⑤底部还有波点涟漪；⑥`r93-artlabel` 字号也是 15px；⑦`r93-drow` 行要支持右键菜单、且与右侧「更多」是同一个菜单；⑧`r93-fc r93-bt` 开合有跳动；⑨复制按钮 hover 底色不对 + 点击后变绿勾；⑩`r93-t14 r93-c2` 顶距 4px + `r93-card` 字号 15px；⑪`r93-alink` 15px；⑫`r93-pill` 尺寸细节不符；⑬`r93-asst` 底线深一级；⑭`r93-iblk r93-i14` 图标不对 + 与左侧时间间距不对。

**逐条落地与实测（1440）**：①`dsbCount=0` / `overflow-y:auto` / 7 行 258 不溢出 ②`rgb(78,78,78)` + `fill-1/border-3` ③线1 **68** / 速率 81..224 / 线2 **234** / ⋯ 盒 233..257 ④SKILL 渲出完整**扳手**（见下「踩坑一」）⑤`.r74-ripple` `background-image:none` ⑥`fs=15px` ⑦面板 182×153 / 4 项 + 1 分隔线 / `viaMoreBtn=true`、`sameNode=true`（**同一点击节点**）/ `Esc` 可关 ⑧三态 `headH` 恒 22、`icW/H` 恒 14、`txX` 恒 18、`headTop` 恒 0、`reopenMatches=true` ⑨`color=rgb(48,149,59)` 绿勾 ⑩`c2MarginTop=4px` / `cardFs=15px` / `quizPad=20px` / **`quizH=208` = 设计稿** ⑪`fs=15px` ⑫盒 158×22 / `pad=1px 6px` / `radius=3px` / `color=rgb(52,145,250)` ⑬`rgb(229,229,229)` ⑭**regen 图标重画为 14 栅格** / `gapTB1=13` / `gapB1B2=6`。

**★ 踩坑一（本轮最大，已写进补丁注释 + PLAYBOOK P3.30①）**：我先写了 `fit_viewbox()`（按「字形 bbox 越出 viewBox > 35%」自动重算），
它报 `svg_1d5c65e3`（SKILL）越界 90%、`svg_e08b0fbd` 越界 92% ⇒ 我把两者的 viewBox 改成 `11.784 -0.05 14.225 14.225` 等。
**真相是假警报**：这两个文件的 `<path>` 挂着 `transform="matrix(-1,0,0,1,26,0)"`（x → 26−x 镜像），镜像后字形正好落在 x[1,13]，
**原 `viewBox="0 0 14 14"` 本来就对**；我的 `glyph_bbox()` 只读 `d` 数字、不认 transform ⇒ 一改反而把字形推出框外，**只剩左沿 1px 残片**。
处置：**整段删除** `glyph_bbox`/`fit_viewbox`/`_r3`（原处留复盘注释）。按 transform 感知重体检 78 个源文件 ⇒ 真越界的只有 4 件未引用的 DS 内部结构图。
⚠️ **本页共 8 个源文件带 matrix**（含 4 个 `matrix(0,1,-1,0,1,-1)` 的 90° 旋转）⇒ **以后别用「按裸坐标推算」的方式改图标几何**。
★ 元教训：**改了「自动修正/自动体检」逻辑后，必须目视复核一个受影响的样本** —— 只看探针数字会以为修好了（我这次就是靠肉眼才发现）。
判「图标本体坏 or 宿主 CSS 坏」的利器 = 隔离测试页 `mg-work/r93/ev/icontest.html`。

**★ 踩坑二**：`.r93-ctx` 探针报 175px（应 182）—— 是 `scale(.96→1)` 的 0.2s 过渡中取值（`182×0.96=174.72`），**不是 bug**。

**★ r99 复查（全绿）**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（21882 字节）｜双视口 1440 + 1500 全页 + 逐区域滚动裁片 + 设计稿并排对照（`raw/r99-final-umeta-cmp2.png`）。

**产物**：`pages/conversation.html` 616773 → 631381 → **631287 字符**（r99 两拍：+14608 / −35 / −59）；`pages/base.html` **未变**。
新增 `ev/p99a~j`（14 条复查 / umeta 几何 / 菜单截图 / 全元素矩形 / 逐区域滚动 / 图标隔离渲染）· `vd-r99b/c.txt`；
新增 `raw/r99-*.png` 与 `raw/r99v-*.png`（含 `r99v-m1~m3` 拼图）；新增隔离测试页 `ev/icontest.html`。
**回滚**：`before/` 里**没有 r98 终态快照**（该代只存了 r96/r97）⇒ 只能①定点删 `apply93.py` 里标 `★ r99` 的段落（改完直接重跑即自愈）或②`apply93.py --revert` 回 r93c 快照。
已补存 **`before/conversation-r99.html`**（= 本轮终态，作为下一轮基线）。详见 `mg-work/r93/acceptance.md` 第十二章。

### r100（同日第十轮 · **最新**）—— 会话详情页 8 条（**就地返工 `apply93.py`**）

邵先生原话八条：①「GienX」改成「GienCoder」；②所有 `r93-card` 容器内的字号都改成 14px；③「滚动到底部」hover 时**边框颜色不要变化**，图标和文字颜色再**深一级**即可；④`r93-dlist` 的 item **整行都应该可点击**、注意鼠标指针形态；⑤`r93-agent` / `r93-agent2` 这类小卡 hover **加个浅灰底色即可、边框颜色不要变**；⑥`r93-ndesc r93-t12h` 这种文字行**是有背景底色的**、对比设计稿；⑦`class="r93-fh r93-bt"` 这个**折叠后前面的图标异常**；⑧「调用 5 个工具」这个分组下面**是分层级的**、可以**一级一级**点击展开折叠、并且有**层级连接线**。

**逐条落地与实测（1440，`ev/p100b.log`）**：①`gienxCount=0` / `giencoderCount=4` / 助手名 `GienCoder`（另把 `task-detail.html` 那处 `GienX端到端初始化` 一并改掉）②卡内字号直方图 `{"14px":106}` ③hover `color=rgb(31,31,31)`（默认 78）；**`border` 与默认完全一致 rgb(229,229,229) ✓** ④7 行 `cursor` 全 `pointer`；点整行 ⇒ 菜单 182×159 开、`Escape` 关 ⑤hover `bg=rgb(242,242,242)`、**`border` 未变 ✓** ⑥`bg=rgb(247,247,247)` / `radius=12` / `pad=0 12px` / `h=24`，两行中心 x=849.5 / 850 居中 ✓ ⑦⑧内层 Tool call 改真折叠（展开头/折叠头槽**都是 i14**；点一下 `foldH 166→22`、`cardH 132→0`）；层级缩进 **L0=420 / L1=438 / L2=456**（相对 0 / 18 / 36，与设计稿一致），竖导线 1px + 每个 L1 子项 8px 横向肘节。

**★ 本轮新增权威取数（已写入 PAGES P3.11g ⑩ / PLAYBOOK P3.31）**：
- ⚠️ **设计稿 HTML 导出会丢掉 DS 实例自身的底色与圆角**（`容器 225` 的两行 ndesc 只有 `width/height`）⇒ **必须回 PNG 逐像素扫**。
- `.r93-ndesc` 胶囊 = **文字宽 + 两侧 12px 内距**、**24 高**、底 **rgb(247,247,247) = `--color-fill-1`**、圆角 **12px = `--border-radius-xl`**（两行实测 778×24 / 300×24，墨迹内距 13/13 与 13/14）。
- `1393:18521 容器 221` 缩进：折叠/展开头 **0**；`容器 218`（内嵌 Tool call 822×200）**18**、其代码卡 `容器 217`（804×132）**36**；`容器 219`（4 行清单 305×124 @top246）**18**。**设计稿没有画连接线** ⇒ 连接线是本轮新增要求。
- `容器 218` 内两个 `Link`（`fw647:18138` 折叠态 / `fw647:18151` 展开态）是**同一节点的两态叠加**（又一次「变体叠加」陷阱）。

**★ 本轮三个坑**：①`fold()` 工厂的 `o.mt ? …` 把 `mt:0` 当假值 ⇒ 已改 `o.mt != null`；②**绝对定位伪元素不算 flex item** ⇒ 肘节必须 `::before + position:absolute` 才不会把列向 flex 的折叠头挤下去；③`.r93-sumlist::before` 原来是**局部**竖线 ⇒ 本轮把画线职责上移到 `.r93-tree`，避免接缝断线。

**★ r100 复查（全绿）**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 输出与 `ev/vd-r93c.txt` **二进制逐字节相同**（`cmp` 通过，21882 字节）｜1440 全量读数 + 真鼠标 hover×3 + 真鼠标点击（整行开菜单 / 内层折叠）+ 视觉裁片。

**产物**：`pages/conversation.html` 631287 → **634719 字符**；`pages/base.html` **471444 未变**；`pages/task-detail.html` 766710 → **766714**。
新增 `ev/p100a` ~ `p100shot2` 探针 + `vd-r100.txt`；新增 `raw/r100-*.png`（含 `r100-tree-line-zoom.png` 连接线放大、`r100-tools5-open/-collapsed-crop.png` 两态、`r100-d-note2.png` 设计稿对照）。
补存 **`before/conversation-r100.html`**（本轮终态，作为下一轮基线）。详见 `mg-work/r93/acceptance.md` 第十三章。

**待拍板**：③ 底色（`--color-fill-1`）**保留** —— 邵先生只点了「描边」与「前景色」两条，未要求撤底色；若要「连底色也不要」改 1 行。⑧ 的**横向肘节是新增的**（设计稿没画线），若只想要一条竖线、不要 `├─` 肘节，删 2 条选择器即可。

### 执行顺序

```bash
python mg-work/r88/apply88.py             # 设置页（含 PRIOR 四代，自动 converge）
python mg-work/r88/apply88b-fontsize.py   # 字号机制层（含 r93 需求 1 的 LEADING_DERIVE）
python mg-work/r92/apply92.py             # ① 五页顶栏图 + ④ base 权限红
python mg-work/r93/apply93.py             # 需求 2 + ④（**必须最后跑**：写 base + conversation + 9 页 ROUTE，尾部调 apply88b 做 converge）
# 顺序无关的部分：apply88 / apply92 互不影响；apply93 收尾统一过一遍 apply88b
```

---

## 二·b ★ r101（最新一拍 · 会话详情页十一条 · 2026-09-30）—— **新一代，非就地返工**

> 完整版见 `mg-work/r101/acceptance.md`；细则见 PLAYBOOK **P3.32**、PAGES **P3.11g ⑪**。

**① 体位变化（最要紧）**：r93 代**已提交**（`d7e2151`）⇒ 本代**新建** `mg-work/r101/apply101.py`，
注入块 id 换代 `r93-conv-*` → **`r101-conv-css` / `r101-conv-js` / `r101-nav-js`**。
页面里仍留着 r93 的三块注入物 ⇒ 脚本引入 **`GENS` 逐代摘除表**（r93 + r101 一起摘、注入用本代 id），
自检改两层循环。★ `ATTR_HOST='r93-conv-host'` / `ATTR_PAGE='data-r93-page'` **跨代沿用** ⇒ 页面级 CSS 选择器**一字未改**。

**② 十一条**（实测见 acceptance 第一节）：

| # | 落地 | 关键实测 |
|---|---|---|
| ① | `.r93-fh:hover` / `.r93-fc:hover` → `background:transparent` + 前景提到 text-1 | `hov=true` / `bg=rgba(0,0,0,0)` / `color=rgb(31,31,31)` |
| ② | `.r93-t12l` 补 `color:var(--color-text-3)` | 「深度思考」正文 text-1 → text-3（**主动下调**，设计稿实测是 text-1） |
| ③ | `.r93-ib:hover{background:var(--color-fill-2)}`、无边框（撤 r99⑨） | `bg=rgb(242,242,242)` / `sh=none` |
| ④ | `.r93-iblk.r93-cv > svg{10px}`（**槽仍 14×14**） | `slotW=14` / `svgW=10`；折叠前后 `dx=0` |
| ⑤ | Bash 卡头删绿勾 | `.r93-okc` 2→1（「上下文已压缩」保留） |
| ⑥ | `.r93-tbsticky::after` 40px 渐隐（`bottom:-44px` / `z:-1`） | `bg=linear-gradient(rgba(0,0,0,0), rgb(255,255,255))` |
| ⑦ | 产物卡右键菜单（r69 `part-ctx.js` 那套 + 打开方式▸6 项） | 主菜单 6 项 + 1 分隔线 + 子菜单 6 项（彩色品牌图标） |
| ⑧ | `@keyframes r93-spin` 1.2s linear infinite | `state=running` |
| ⑨ | `.r93-fm.r93-ell` + **`.r93-sumrow .r93-t12l`** = 13px | 直方图 `{13px:17, 14px:1, 15px:1}` |
| ⑩ | `.r93-sb` 补 `box-shadow:0 2px 9px rgba(0,0,0,0.07)`（**自造档**） | 剖面 vs 设计稿 **Σ\|Δ\|=3** |
| ⑪ | 骨架屏 Skeleton（复用 DS `giencoder-skeleton-*`，1.1s 后淡出移除） | t≈350ms `n=1`（8 线/1 标题/1 头像）；t≈2000ms **`n=0`** |

**③ 本轮新沉淀的三条规矩**（PLAYBOOK P3.32）：
- **hover 类需求必须带 `matches(':hover')` 读数** —— 只看 `backgroundColor` **不可判定**（透明既可能是命中规则、也可能是默认态）。
- **脚本内注释会原样注入页面** ⇒ 别在 `applyNN.py` 的 `CSS/JS_TMPL/docstring` 里写裸 `<style>`（打爆计数自检）、
  裸 hex（TOKEN-GAP）、裸 `linear-gradient` / 裸字号（页面级计数 +1）。
- **1.1s 级的骨架屏 CLI 截图抓不到**（`open` 本身耗时 ≈1~2s）⇒ 目视取证只能临时改大延时、截完立即还原（并 grep 核对还原）。

**④ 产物**：`conversation.html` 634719 → **671386**（+36667；`sha 544ed8156a78`）；`base.html` 471444 → **471447**（+3，仅 nav id 换名）；
`task-detail.html` **未改**。回滚：`python mg-work/r101/apply101.py --revert` 或 `cp mg-work/r101/before/conversation-r101.html pages/conversation.html`。

**⑤ 待拍板 3 条 + 需复核 0 条**：见第六节 #32~#35（⑤ 删哪枚绿勾 / ⑧ 是否常转 / ⑩ 投影档位；r99 遗留的「hover 无法直证」已闭环）。

---

## 二·c ★ r102（会话详情页十一条 · 2026-09-30 20:4x）—— **已提交（`87e2caa`）**

> 完整版见 `mg-work/r102/acceptance.md`（六节）；脚本内新教训见 PLAYBOOK **P3.34**（五条）；本页固定事实见 PAGES **P3.11g ⑫**。

**① 体位**：r101 **已提交**（`9f252e5`）⇒ 本代**新建** `mg-work/r102/apply102.py`，
注入块 id 换代 `r101-conv-*` → **`r102-conv-css` / `r102-conv-js` / `r102-nav-js`**。
`GENS` 逐代摘除表**扩到三代**（r93 / r101 / r102，三条剥离正则各摘三支、注入只用 r102）。
★ `HDR_ID` **保持 `r101-hdr-css` 不换名**（顶栏图本轮无改动）；`RAWI_DIRS` **三级回落**；
宿主 `r93-conv-host` / `data-r93-page` 跨代沿用 ⇒ 页面级 CSS 选择器**一字未改**。

**② 十一条**（实测见 acceptance 第一节）：

| # | 落地 | 关键实测 |
|---|---|---|
| ① | `.r93-t14` 15 → **13px**；数字滑入动效 `.r93-num`（CSS + JS） | 直方图 `{13px:58, 14px:6}`（卡内 6 处仍 14，被 `.r93-card.r93-card *` 钉住）；`num n=13`、`delay 1.5s`；真实时间轴两拍：骨架屏在时 `op=0/translateY(9.8px)` → +1.4s `op=1/none`；**包装 A/B `dx=dy=0`** |
| ② | `.r93-fc .r93-fchev` 间距 8 → **4px** | 靠父级 `gap:4`；标题右缘→箭头左缘 = **4px** |
| ③ | **折叠收起补动效**（`max-height` 精确高度过渡） | 收起曲线 `222→220→188→…→2→0`（0.32s 平滑）；展开反向同长；终态 `overflow:visible` / `.r93-fb.is-free` |
| ④ | `.r93-t12.r93-nm` 12 → **13px** | 2 处全 13px |
| ⑤ | `.r93-iblk.r93-cv > svg` 10 → **12px** | `slotW=14` / `svgW=12` / `n=14` |
| ⑥ | 折叠头/展开头 hover 时 meta 也变正文色 | `hovFc=true` / `metaColor=rgb(31,31,31)`（原 `rgb(134,134,134)`） |
| ⑦ | `.r93-asst` 底边线浅一级（**撤 r99 ⑬**） | `rgb(229,229,229)` → **`rgb(242,242,242)`** |
| ⑧ | `.r93-drow` padding → **`0 16px`** | 文件名左缘相对卡 16、「⋯」右缘 16；`gap 17` / 行高 36 不变 |
| ⑨ | `.r93-dhead` 左内距 12 → **16px** | `pad="6px 6px 5px 16px"`；图标槽相对 16 |
| ⑩ | 「滚动到底部」药丸 → 毛玻璃（+ hover 档 `--r93-glass-h`） | `bg rgba(255,255,255,.72)` / `bf blur(12px)`（原 `rgb(255,255,255)` / `none`）；裁片见背后文字被洗淡 |
| ⑪ | `.r93-seg` 总高 **28px** 且垂直居中 | 基线 **34px**（上 8 / 下 2）→ **28px**（上 8 / 下 8）；根因 = DS `min-height` 没被覆盖 |

**③ 本代新沉淀（PLAYBOOK P3.34）**：`min-height` 比 `height` 更能顶住 · 同帧「写 CSS 变量 + 改属性」会被合并
（必须**提前维护**，`void offsetHeight` 强制 flush 无效）· `max-height` 收起必须用**精确高度** ·
断言 hover 要用**不被遮挡的**目标 · `.r93-num` 基线用 `vertical-align:bottom` + 同 `line-height`；
动效基础延迟必须 ≥ 骨架屏完整生命周期（**1.42s ⇒ 取 1.5s**）。

**④ 产物**：`conversation.html` 672845 → **683044**（+10199；LF `sha 249fbc984716`）；
`base.html` 472150 → **472150**（+0，仅 nav id 换名；`sha c406a60add16`）；其余 4 页**未动**。
回滚：`python mg-work/r102/apply102.py --revert` 或 `cp mg-work/r102/before/conversation-r102.html pages/conversation.html`。

**⑤ 四查**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 与 r101 终态
`vd-r101e.txt` **逐字节相同**（21882 字节 / `diff_exit=0`，**零新增**）｜1440 + 2560 双视口实测一致 + 视觉裁片目视 ✓。
**代数标记**：真·注入块 `r102-*` 各 1；**历代 id 残留 0**。

**⑥ 待拍板 5 条**：`-m`/`-b` 变体仍 15px ｜数字动效覆盖「全部卡外数字串」（含正文数字）｜基础延迟 1.5s ｜
`--r93-glass-h` 无设计稿依据 ｜`.r93-fb` 常驻 `overflow:hidden`（展开稳定后 `.is-free` 放行，新浮层会被裁 360ms）。

---

## 二·d ★ r103（会话详情页六条 · 2026-09-30 21:1x）—— **就地返工，与 r102 同批（已提交 `87e2caa`）**

> 完整版见 `mg-work/r102/acceptance.md` 的 **r103 段**；机制级教训见 PLAYBOOK **P3.35**；本页固定事实见 PAGES **P3.11g ⑬**。

**① 体位**：r102 **未提交** ⇒ **就地改 `mg-work/r102/apply102.py`**，注入块 id 不变（`r102-conv-*`）、**不另起代数**。
产物 `conversation.html` 683044 → **685465**（+2421；LF `sha a340b6a9e89f`）；`base.html` **472150（+0）**。

**② 六条**（实测见 acceptance r103 段第一节）：

| # | 落地 | 关键实测 |
|---|---|---|
| ① | `.r93-t14` 13 → **15px**（**撤销 r102 ① 字号**；数字动效保留） | 直方图 `{13:58,14:6}` → **`{15:58,14:6}`**；`.r93-num` 仍 13 个 |
| ② | `.r93-t14.r93-ell` / `.r93-c1` 也 15px | 35 处 + 2 处**全 15px**（两类本身不含 font-size ⇒ 随 ① 自动生效） |
| ③ | 药丸毛玻璃**再透一档** | 新增 `--r93-glass-pill` **0.60** / `-h` 0.74（暗色同口径）；**标题栏仍 `--r93-glass` 0.72 不动**；A/B 像素均值 **235.5 < 236.2** |
| ④ | **`.r93-agents` 整行退役**（连 `.r93-cp`） | 两元素均不存在；`.r93-bottom` `{y:593,h:112}` → **`{y:653,h:52}`**（子元素只剩 `.r93-sb`），底部整块**上移 60px**；CSS 一族**保留未删** |
| ⑤ | 底部对话框激活态**外发光顶部截断 → 已修** | 5 组 A/B 定性：宿主 `overflow:visible` **无效** / 宿主 `position:static` **有效** / hero 提层 **有效** ⇒ 根因 = **绘制顺序**（宿主 `position:relative` 后按**树序**画在 hero 之后）；修法 hero 补 `position:relative; z-index:1`；中轴 y702-704：`255,255,255` → **`230,237,253`/`231,238,254`/`231,238,254`** |
| ⑥ | 折叠开合**两态统一** + 修**闪动** | 撤掉 `@keyframes r93-fold-in` + 单向 animation ⇒ **14 块 `animationName!=='none'` 数 = 0**；统一四条 transition（`max-height`/`margin-top`/`opacity` 0.32s + `transform` 0.34s back-out）；`setFold` 改错帧翻属性。收起 `opacity` **逐帧连续** `1→0.993→0.737→…→0`（旧版一帧 `1→0`）；展开 `transform` 超调 `+0.779px` 后落定 0 ⇒ **镜像** |

**③ 两条机制级教训（PLAYBOOK P3.35）**：
* **给宿主加 `position: relative` 会连带改变绘制顺序** —— `order` 决定的次序在提升为 positioned descendant 后
  **退回树序**，后 `appendChild` 的宿主反而压在 hero 之上（⑤ 的真凶）。凡是加 `position`/`z-index`/`transform`/`filter`
  这类会新建包含块或层叠上下文的属性，都要重算「浮动层 vs 兄弟宿主」的次序。
* **`animation` 被移除不会触发 transition**（CSS Transitions 例外：属性被运行中的动画影响时不启动过渡）
  ⇒ 「展开用 keyframes、收起用 transition」的混合写法**必然有一向硬切**（⑥ 的真凶）。要么两态都 animation，
  要么两态都 transition（本轮选后者，顺带把「单向」变成「镜像」）。
* 附带：`--r93-fbh` 在**嵌套折叠**后会陈旧（实测 fold#10 `314px` vs 真实 170px）⇒ 每次开合都要**重新量**。

**④ 四查**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=16`，
**16 与 HEAD 一致、旧记录写 15 是笔误**）｜`verify-design` 与 r101 终态 `vd-r101e.txt` **逐字节相同**
（17148 字符 / md5 `84f552c5b5a6` / `diff_exit=0`，**零新增**）｜**2560 + 1440 暗色**双档复核一致 + 视觉裁片 ✓。

**⑤ 待拍板 2 条（r103 新增）**：③ 透明度取 0.60（想更透可一行调 `--r93-glass-pill`；要让标题栏一起变只需改一行）；
④ 摘行后状态条↔composer 之间为 **44px** 空档（= 12px 下内距 + 外壳 `div.mt-8` 的 32px），觉得松可再压。

---

## 二·e ★ r105（会话详情页 + 8 个独立页三条 · 2026-09-30 23:0x）—— **就地返工，与 r102/r103/r104 同批（已提交 `87e2caa`）**

> 完整版见 `mg-work/r102/acceptance.md` 的 **r105 段**；机制级教训见 PLAYBOOK **P3.37**（四条）；本页固定事实见 PAGES **P3.11g ⑮**。
> （r104 四条无独立章节，要点见本页头部 + acceptance r104 段 + PLAYBOOK P3.36。）

**① 体位**：r102 / r103 / r104 **均未提交** ⇒ **就地改 `mg-work/r102/apply102.py`**，注入块 id 不变、**不另起代数**。
新增静态片段目录 **`mg-work/r102/part105/`**（四件），在 `inject_tail` 里拼进**同一次**注入。
产物 `conversation.html` 691648 → **793028**（② **+2173**、③ **+99207**）；`base.html` **472150（+0）**；
其余 **8 页各 +714**（同一块 `r102-nav-js`）。

**② 三条**：

| # | 落地 | 关键实测 |
|---|---|---|
| ① | 把 `base.html` 已有那块 `r102-nav-js`（**捕获阶段委托**识别 aside 会话项）**扩到其余 8 页**；`nav_patch → invert_if_absent`（一致 ⇒ 一字不动、只保位置） | 真鼠标点击：`base`/`avatar`/`automation`/`skills` 均落 **`conversation.html`** ✓；**负例**：点分组标题 / 点「新会话」均**留在原页** ✓；`task-detail` 壳 aside **`display:none`**、`kanban`/`settings` aside 是筛选/设置导航、`dev`/`req-kanban` **无 aside** ⇒ **5 页无对象**；各页 nav 块**各 1**，conversation **0** |
| ② | 改用 **DS 官方滑块** `.giencoder-radio-button-slider`（DS 自带 `transition: transform .28s, width .28s` 且**已内联**）；滑块接管白底/描边、`checked` 改 `transparent`、JS `r93SegMove()` 写行内几何 | **逐帧** `0 → 38.79(82ms) → 49.58(148) → 51.75(215) → 51.999(282) → 52(348ms 稳定)`，宽恒 **52**；反向点回「对话」**镜像回 0** ✓。根因 = 当年**自绘**取代了 DS 滑块 ⇒ **位移无载体**、只能硬切 |
| ③ | `r93-bar` 右侧换成 **全屏 + 打开侧栏**（= 数字分身 `td-right-acts`）：按钮本体逐字对齐 + `<html data-r93-full='1'>` + **AV-BROWSE-SLOT v1 三件套整块移植** | **按钮** rect `[1359,57,64,28]`（28×28 + gap 8，右缘 1431 = bar 右缘 − 8）、`bd rgba(0,0,0,0)`、`br 8px`、hover `rgb(247,247,247)`、图标 **14px**；**全屏** 1440 `aside 256→0` / `main 1164→1420` / `aria-label` 翻转，2560 同构；**侧栏** `aside 0 / main 779 / split [791,48,9,844] / pane 641`、右键菜单 **12 项**、文件树 **28 行**（点目录 `is-closed` + 27 行 `is-hidden`）、拖分栏 **641→701** 落盘 `{"panelW":701}`、关闭**完全复原**；**Esc 三档**逐层（菜单 → 侧栏 → 全屏） |

**③ r105 新增的第 ③-d「暗色档」**（源页没有，本模块**首次落到有暗色分支的页面**）：
`browse.css` 7 个字面 hex **全是自定义属性定义** ⇒ 只覆盖这 7 个、**不动几何**（源件逐字不动、同源校验仍成立）。
暗色实测 `panelBorder rgb(78,78,78)` / `codeKey rgb(86,156,214)` / `panelBg rgb(23,23,26)`，**浅色档逐字节不变**。

**④ 四查**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax pages/*.html` **10/10 ALL_OK**（conversation `script=9 style=16`）｜
`verify-design ./pages` 与 `vd-r101e.txt` **逐字节相同**（17148 字符 / md5 `84f552c5b5a6`）⇒ **零新增**｜
**1440 + 2560 + 暗色**三档实测 + 裁片目视 ✓。死代码：`r93-morebtn` 全仓 **3 处全在注释**（活规则 0）。

**⑤ 待拍板 3 条（r105 新增，均是「顺手替他做的判断」）**：
1. **全屏 = 收拢左导航**（同数字分身全屏语义）—— 若想保留一条**可点回来的窄条**（0 → 12px 抓边），说一声即改。
2. **预览栏默认宽 641**（沿用数字分身）—— 本页内容更宽，若想本页另给默认值（如 720）可单独调。
3. **预览栏与「全屏」可同时开**（`x105-2-both.png`：aside 0 + 侧栏在右）—— 若想**互斥**，说一声即改。

---

## 二·f ★ r106（会话详情页六条 · 2026-10-01 08:2x 首拍 / 08:4x 返工 / 08:5x 第三拍）—— **已提交 `4d081ba`**

> 完整版见 `mg-work/r106/acceptance.md`；机制级教训见 PLAYBOOK **P3.38**（六条）；本页固定事实见 PAGES **P3.11g ⑯**。
> ★ 本代**三拍**（同一代 r106、`apply106.py` **就地返工三次**，**始终未提交**）：
> 首拍 ①②③④；**返工拍** = ④ **口径更正** + 新增 ⑤；**第三拍** = 新增 **④b 用户消息块写死 728px**。
> 返工理由：r106 未提交 ⇒ 按硬规则**就地改 `apply106.py`、不另起代数**（判据 `git status` 仍 ` M`）。

**① 体位**：r102 代**已交付**（`87e2caa`）⇒ **新建 `mg-work/r106/apply106.py`**（**不就地返工**）。
`GENS` 摘除表 = **四代**（`r93` / `r101` / `r102` / `r106`），`CSS_ID/JS_ID/NAV_ID = GENS[-1][1:4]` ⇒ 自动取 r106；
四条剥离正则由 `'|'.join(...)` 派生。⚠ **r103/r104/r105 从未单独占代 ⇒ 不入表**。
脚本由 **`ev/make106.py`** 从 `apply102.py` 做 **9 处精确替换**生成（E1 顶部 docstring｜E2 用法块｜E3 GENS｜
E4 `PART105`→`PART_DIRS`｜E5 插入 `R106_CSS`｜E6 `build_css` 拼 `R106_CSS`｜E7/E8 两处 `fold` 调用｜E9 文末用法行），
每处命中 ≠ 1 次即 `sys.exit`。
`PART_DIRS` **双目录回退**（`r106/part106` → `r102/part105`）⇒ 三个移植件**沿用 r102 目录、不复制**。

**② 产物（★★ 字符口径 —— 首版曾算错；⚠ 2026-10-01 11:5x 二次校准见下）**：
`conversation.html` **793028 → 799231 Unicode 字符（+6203）**（`4d081ba` blob `67b443ca082c`，LF 归一 `sha1 9cdb19501a81`）。
⚠ 本节旧记「**798613（+5585）/ 工作区 blob `e17d227b58bf`**」是**提交前态**（该对象已不在库中，`git cat-file` 报 `Not a valid object name`）⇒
**一律以 `git cat-file blob 4d081ba:pages/conversation.html` 实测为准**（该 blob 内 `r106-conv-css` / `r106-conv-js` 各 **1**、`r107-*` 为 **0** ⇒ 确认为 r106 交付态）；
`base.html` **472150（+0）**、blob `3436a5e7857e`；**另 8 页同因 nav 块 id 换代而改、字符数均 +0**
（`r102-*` 与 `r106-*` **等长**）⇒ **本代 10 页全写，没有旁观页**。
⚠ **三种口径勿混用**（同一份文件）★ **校准后**：Unicode 字符 **799231** ｜ UTF-8 字节（LF 归一）**870627** ｜ 工作区字节（CRLF）= UTF-8 字节 + `\r\n` 个数（**4701**）＝ **875328**。（旧记的 `798613 / 869581 / 874274` 是**提交前态**，勿再引用。）
⚠ ★★ `len(bytes) − CRLF数` **不是字符数**（本页中文多，会虚高 ~6.8 万）⇒ 判内容增减要**先归一化行尾、再比同一口径**。
⚠ 工作区字节比仓库 blob 大「行数」字节 = **`core.autocrlf=true`** 的行尾差，**不是内容改动**（详见 PLAYBOOK P3.38①）。

**③ 六条**：

| # | 落地 | 关键实测 |
|---|---|---|
| ① | 「上下文注入」「深度思考」默认折叠 —— `fold()` 调用**加 `open: false`**（**零 CSS / 零结构**） | 14 块：第 ①② 块 `data-r93-open=0`、**h=22**（y=429 / y=467）；**其余 12 块 `open=1` 逐块不变**。`fold()` 工厂**本就支持** `(o.open === false ? '0' : '1')` |
| ② | 本页适配层 `html[data-r93-page='conversation'] .td-browse-bar { height: 44px }` | `r93-bar` **h=44** / `td-browse-bar` **40 → 44**；两条底线**同落 y=92**。**源件 `part105/browse.css` 一字未动**（同源校验 `extract105.py` 仍成立） |
| ③ | `main { border-top-right-radius: 0; border-bottom-right-radius: 0; border-right-width: 0 }` | 半径 **`10 10 10 10 → 10 0 0 10`**、`border-width **1 1 1 1 → 1 0 1 1**`；接缝**非白像素 2 → 1**（改后只剩 x=791 `#E5E5E5`）；右上/右下 10px 阶梯缺口消失 |
| ④ | ★ **口径更正**：`width: min(可用宽, 原逻辑值)`。`.r93-wrap { width: min(calc(100% + 20px), max(calc(50% + 10px), 860px)); min-width: 0; margin: 0 calc((100% − 宽) / 2); }`；`.r93-bottom` / composer 外壳 / `.r93-sk-in` = `min(100%, max(50%, 860px))` | **1440 开 = 778**（left 13、`overRight 0`）；**2560 开 = 949**（left 488、居中 = 原逻辑）；**关态 860 / 1141 逐像素不变**。原逻辑实测（`ev/p106e.js`）：1440 开 860（右溢 92px = 遮挡）、2560 开 949 |
| ④b | ★ **第三拍新增**：`.r93-bub { width: min(100%, 728px) }`（**不带 `.av-browse-on`**）。原规则 `.r93-bub { margin-left: auto; width: 728px; … }` 在 r93 段「用户消息」，**全仓唯一 `728px`** | 改前：**1280 开（列 618）块 728 溢 110px**（气泡文字断在「…三个泳道，未」+ chip 被切）、1370 开（列 708）溢 20px。改后：**618 / 708 跟列收、溢出 0**；**≥728 的 7 档（1280/1370 关 + 1440/1920/2560 × 关·开）仍是 728、逐像素不变**。★ **1440 下不可见** ⇒ 验它必须到 1280/1370 开态 |
| ⑤ | ★ **返工拍新增**：删产物卡模板里那处**内联** `style="color:var(--color-primary-6)"`（CSS 一行未动） | 未 hover：5 张卡文件名全部 `rgb(31,31,31)`（text-1）、`inline=(none)`；真鼠标 hover 第 2 张 ⇒ `rgb(55,112,247)`（primary-6） |

**④ 三档同构**：1440 / 2560 / 暗色 三档下 ①`open=0 h=22`、②`44/44`、③`10 0 0 10` + `1 0 1 1`、④**开 778 / 关 860**（2560 开 949 / 关 1141）**全部一致**；
**第三拍加验窄档**：1280 开 / 1370 开 的 ④b = **618 / 708**（跟列收、溢出 0）；
开态与关态下 **wrap / bottom / composer 三列同宽同左缘**（r97「全宽块等宽」保住）；
暗色接缝 `rgb(78,78,78)`、面板底 `#17171a`、main 底 `#232324`（浅色档逐字节不变）。

**⑤ 四查（三拍各跑一遍，全绿）**：幂等 ✓（每拍连跑两遍，第二遍双「已是目标态」；第三拍 `797333 → 798613 (+1280)`）｜
`mg-work/check-syntax.py pages/*.html` **10/10 通过**（conversation `script=9 style=16`）｜
`verify-design.py ./pages` 与 `ev/vd-r101e.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`，
`vd-r106c.txt` 同 md5）⇒ **零新增**｜
**代数核对**：conversation 的 `r106-conv-css` / `r106-conv-js` 各 **1**、base 的 `r106-nav-js` **1**、`r102-*`/`r101-*`/`r93-conv-*` **全 0**、**10 页历代别名零残留**。
收尾清理：`git checkout -- pages/gaps.log`（`verify-design` 会改它，必须还原）。

**⑥ 待拍板 4 条**：见第六节 **44 / 45 / 46 / 47**（**47 = 第四拍待定**：④b 要不要改成 `width: 100%` 让用户消息块与内容列同宽）。

---

## 二·g ★★ r107（上一拍 · 会话详情页「侧栏模块标签化」＝复刻 Codex 右栏 · 2026-10-01 09:3x 起，共**十一拍**）—— **新一代（r106 已交付 `4d081ba`），已推送 `e9c9498`**

> 完整版见 `mg-work/r107/acceptance.md`（**十六节**，含第二 ~ 十一拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.47**；
> 本页固定事实见 PAGES **P3.11i**；设计依据 = `docs/codex-sidepanel-research.md` + `docs/codex-refs/`（`f13b3bf`）。

**① 体位**：r106 代**已交付** ⇒ **新建 `mg-work/r107/apply107.py`**（**不就地返工**），
由 **`ev/make107.py`** 从 `apply106.py` 做 **13 处精确替换**生成（每处命中数断言，不符即 `sys.exit`、不写盘）。
`GENS` 扩成**五代**，四条剥离正则各摘五支、注入只用 r107。

**★★★ 本代最关键的决定 —— nav 块沿用 `r106-nav-js`（不换名）**：
`GENS[-1] = ('r107','r107-conv-css','r107-conv-js','r106-nav-js')` + `NAV_TAG='r106'`
（`build_nav_js()` 与「摘块后残留自检」都改用它）。理由 = 硬规则「**跨代沿用的宿主标记不换名**」：
nav 跳转脚本本代一字未改 ⇒ 换名会让 base + 8 页**凭空进 diff** ⇒ 违背邵先生「不得改动其他不必涉及的模块」。
**实测收益：`apply107.py` 跑完打印「base.html 已是目标态（无改动）」，`git status` 只有 conversation.html 一个 ` M`。**

**② 产物**：`conversation.html` **799231 → 866988（第一拍 +67757）→ 876008（第二拍 +9020）→ 894916（第三拍 +18908）→ 920259（第四拍 +25343）→ 921730（第五拍 +1471）→ 925776（第六拍 +4046）→ 927464（第七拍 +1688，合计 +128233）**；
UTF-8 字节（LF 归一）870627 → 952672 → 976078 → 1004420 → 1006094 → 1012253 → **1015265**；工作区字节（CRLF）958664 → 979610 → 1011192 → 1012899 → 1019153 → **1022207**。**另 8 页逐字节不变**（仅 avatar.html 文案动了 1 处）。
⚠ **三种口径勿混用**（沿用 PLAYBOOK P3.38① 的教训）。

**③ 落地（三段式 + 五模块）**：
- **① 标签栏**：`[图标]名称 ×` 多标签 + `＋` + `⤢ 最大化` + `✕ 收起`；`is-active` 高亮；
  hover/active 才显 `×`；**只剩一枚时不显示 `×`**（`is-single`）。`＋` **紧跟最后一枚标签**
  （`.td-browse-tabs{flex:0 1 auto}` + `.td-browse-acts{margin-left:auto}`，实测标签右缘 1138 / ＋左缘 1142）。
  **多开 / 切换 / 关闭 / 拖拽重排**：拖拽 `pointerdown` 起手、`pointermove`/`pointerup` **挂 window**、位移 >5px 才进拖动、
  按各标签中线求插入位（实测把末枚拖到最前 ⇒ `[terminal,files,review]`）。
  `＋` 菜单 = **五选一**（审查 ⇧⌘G / 终端 ``⌃` `` / 浏览器 ⌘T / 文件 ⌘P / **摘要**）；
  ★ 第三拍起 `⇧⌘G` / `⇧⌘E` / `` ⌃` `` **真绑定**（`⌘T`/`⌘P` 是浏览器级快捷键，网页拦不住 ⇒ 不绑）。
- **`⤢` 最大化**：自算 `maxPanelW = freeW − 380` 写宿主 `--av-browse-w`；还原读回 localStorage 的 `panelW`。
  实测 1440 / 2560 = 641→**1040**（main 779→380）/ 641→**2160**（main 1899→380）。⚠ 用**两层 rAF** 落定，避开 ctrl-conv 的单层 rAF。
- **②③ 五个模块**：**文件**（原正文**逐字未改**，由 `ev/splice107.py` 从 part105 剪出）/
  **审查**（工具条 `对比范围 ⌄ +566 −228 4 个文件` + 右端 `复制 / 定位 / ⋯ / 提交⌄ / PR`；4 张 diff 卡含两列行号 + 加绿删红 +
  `⋯ 折叠/展开 46 行`（**真展开出行**）+ 行内评论 + 提交模态 + 逐文件 `暂存 / 撤销`；`⋯` **十项**显示选项；**统一 ⇄ 并排**）/
  **终端**（提示符 + 真按键回声：`ls`/`pwd`/`npm run dev`/`clear`/未知命令）/
  **浏览器**（URL 行 + 右端 `缩放 / 发送 / 更多` + **标注态**：元素虚线描边 + 点击出评论气泡 + 底部 `标注中` 条）/
  **摘要**（任务侧栏四段：摘要 / 计划 / 来源 / 产物）。
- **④ 划词浮条**：~~原为「划词 → 在侧边聊天中提问」的入口~~ ⇒ **第三拍随「侧边聊天」一并删除** ⇒
  **第四拍 ⑩ 按邵先生要求补回并做成真功能**（「添加到对话」真写主 `textarea` / 「复制」真复制；两枚 DS 文字按钮）。
- **⑤ Esc 层级**：`panel.js` 挂 **window 捕获段**（早于 ctrl-conv 的 document 捕获段）⇒ 一次 Esc 只关菜单，再按才关侧栏（实测）。

**④ 期间修掉的两个真 bug（第一拍 · 都是量出来才现形）**：
1. ★ **新模块 section 类名与内部件撞车**：`<section class="td-mod td-term">` vs 内部 `<div class="td-term">`
   ⇒ `querySelector('.td-term')` 取到 section（`tabindex` 为 null、`tabIndex=-1`）⇒「点终端打字没反应」；
   且 `.td-term{}` 整套样式**同时压在 section 上**。修法：section 改名 **`td-mod-term`**。
2. ★★ **绝对定位子件包含块跑到视口**：`.td-commit{inset:0}` 而**源件 `.td-browse` 没写 `position`**
   ⇒ 遮罩铺满整站、卡片居中屏幕。修法：`panel.css` 给 `.td-browse` 补 **`position: relative`**。
   实测 `modalRect [418,211,250,246] → [792,49,639,842]` ≈ `panelRect [791,48,641,844]` ✓。

**④b 第二拍返工（邵先生 10:0x 反馈两条 · 就地改 `apply107.py`，不另起代数）**：

> 原话：① 「审查」的 `td-rv-opts` 浮窗**点开后就不能关闭**；② 「侧边聊天」的样式与 `r93-scroll` **不一致**（字号、各种颜色等）。

- **③ 浮窗关不掉 = 一个搜索根写错** —— `closeMenus()` 与 Esc 裁决的根写的是**标签栏** `bar = .td-browse-bar`，
  而 `.td-rv-opts` 挂在**模块工具条** `.td-mod-bar` 里 ⇒ 三条关闭路径全废：
  外点 ✗ / Esc ✗（且漏到 ctrl-conv **把整条侧栏关掉**）/ 选完不关 ✗。修法：根 `bar` → **`pane`**。
  实测：外点 `hidden:true` ✓｜Esc 后 `hidden:true` 且 `panelOn:true` ✓｜选「并排」自动关 + `is-split:true` ✓｜再按 Esc 关侧栏 ✓。
- **④ 侧边聊天逐值对齐主对话**：正文 **15/22**（`.r93-t14`）· 用户气泡 **`--r93-bubble` `#E5EDFE`** + `9px 12px` + `8px 8px 2px 8px`（`.r93-bubi`）
  · 引用块 **13/22**（`.r93-t12l`）· 输入框 **14/22**（composer `text-sm leading-[22px]`）· 助手消息**去灰底气泡**（`.r93-asst` 无底）
  · 助手标记 → **24px 同源 GienX logo**（原来是写死的「A」+ 淡蓝圆片），由 `panel.js` 的 `AV_SVG` 注入。
  实测（`ev/verify107b.log`）：侧 ✕ 主**逐值相同**；暗色两侧同为 `rgb(36,49,76)`；`--ui-fs=18` 两侧同为 `19.2857 / 28.2857`。
- **★★★ 顺带挖出仓库级机制坑**：`apply88b.converge()` 的「跳过本代块」正则用**硬编码 `CSS_ID='r87-ui-css'`
  （r87 遗留）** ⇒ 本代块**从未被跳过** ⇒ `line-height: calc(Npx * ratio)` 被 `unscale()` 压成裸 px、
  又因规则体内没有 `var(--font-size-*)` 而**不再被 `scale_block()` 重派生** ⇒ **`--ui-fs` 杠杆静默失效**。
  修法：**带行高/高度的规则，`font-size` 写 `var(--font-size-*)` token**；15px 这种无 token 档用**两段式**
  （token 规则挂行高 + 只覆盖 `font-size` 的第二条，正是 `.r93-t14` 的真实写法）。
  自查脚本 `mg-work/r107/ev/scan-flatten.py <css…>`。⚠ **判据必须看 `--ui-fs=18`**（默认 14 下 `calc(Npx×1)=Npx`，看不出来）。
  本代 5 条中招：3 条 line-height 已修，2 条 `min-height`（`.td-mod-bar` / `.td-url`）**无害**（内容会撑开盒子）。
- 第二拍门禁复跑：幂等 ✓｜`check-syntax` **10/10**｜`verify-design` 与基线**逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）｜
  改动面仍只有一页、`base.html` **+0 字符**｜`r107-conv-css`/`r107-conv-js` 各 1、`r106-*`/`r102-*` 全 0。

**④c 第三拍返工（邵先生 10:2x 反馈四条 · 仍就地改 `apply107.py`，不另起代数）**：

> 原话：① 彻底去掉「侧边聊天」；② 「审查」的「并排视图」下代码文件不能正常展开和折叠；
> ③ 「折叠全部文件」对应「展开全部文件」；④ 对照 Codex 官方原版右栏还有哪些功能被遗漏了，请补充。

- **① 侧边聊天全链路删除**：`_head.html` 菜单项 · `_mods.html` 整个 `td-side` section ·
  `panel.js`（`AV_SVG` / `pushMsg` / `sendSide` / `.td-side-av` logo 注入 / **`.td-selbar` 划词浮条整段** / Esc 里的 `selOpen`）·
  `panel.css` 6. / 7. 两节。**划词浮条一并删**（它存在的前提就是 side chat；另一枚「添加到对话」在初版是空壳）。
  判据：`td-side` / `td-selbar` / `AV_SVG` / 页面里「侧边聊天」四个字（连注释）**全 0**。原第五格由 **「摘要」** 接替。
- **② 并排视图折叠失效 = 同特异性规则的「位置」问题**：`.td-diff:not(.is-open) .td-diff-rows`(0,3,0) 与
  `.td-rv-body.is-split .td-diff-split`(0,3,0) **特异性完全相同、后者写在后面 ⇒ 折叠路径整体失效**
  （统一视图正常，所以只在并排下暴露）⇒ 后者加一层 `.is-open` 提到 **(0,4,0)**。
  四象限实测：统一展开 `block/–/block`｜统一折叠 `none/–/none`｜并排展开 `–/block/block`｜并排折叠 `–/none/none`。
- **③ 折叠全部 ⇄ 展开全部**：同一枚菜单项双向切换（**文案 + 字形一起翻**）；
  判据 =「**只要还有折叠着的文件，这一项就是『展开全部文件』**」；手动折单个文件后也会回来同步。实测 2 开→4 开→0 开→手动 1 开，全程正确。
- **④ 对照 Codex 官方补的遗漏（本轮主体）**：对比范围下拉 · `⋯` 显示选项**补齐八项**（自动换行 / 词级差异 / 隐藏空白 **真生效**）·
  工具条动作组（复制 / 在文件树中定位 / `提交 ⌄` 含推送 / PR）· 逐文件 **暂存 · 撤销** · 「N 行未改动」**真展开** ·
  **新增「摘要」模块** · **快捷键真绑定** · 轻提示 toast。详见本卡开头 ⑧ 与 `acceptance.md` 第八节。
  ⚠ 两条口径：**`⌘T` / `⌘P` 是浏览器级快捷键，网页 `preventDefault()` 拦不住 ⇒ 不绑**（只绑 `⇧⌘G` / `⇧⌘E` / `` ⌃` ``）；
  **`verify-design.py` 会数「渐变处数」** —— 为「进行中」计划项画的 `linear-gradient` 半填充圆点让回归 **+1（63→64）**
  ⇒ 改「边色 + 实心 `--color-primary-light-2`」后回到基线（PLAYBOOK P3.39⑫）。

**④d 第四拍返工（邵先生 10:5x 反馈五条 · 仍就地改 `apply107.py`，不另起代数）**：

> 原话：① 将「摘要」作为右栏默认页签，且摘要 / 计划 / 来源 / 产物四个模块要**卡片式**设计风格；
> ② **划词功能没有了？要补充**；③ 新右栏里有些模块或对象是支持**对应的右键菜单**的，请调查后补充；
> ④ `.td-browse-tab` 的字号应该是 **14px**；⑤ 整个新右栏的**所有下拉菜单**（如 `td-mod-menu`）都要用 **giencoder 设计系统已有组件**。

- **⑨ 摘要升默认页签 + 四模块卡片式**：`_head.html` 初始标签 `data-td-mod` `files`→`summary`（图标换列表字形 /
  `aria-controls` / `aria-label` 同步）+ `panel.js` 初始化 `activate('files')`→`activate('summary')` **两处同改**。
  `.td-sum-sec` 加 `1px --color-border-1` 描边 + `8px` 圆角 + `--color-bg-2` 底 + `12px` 内距（容器 `gap:12px`）；
  卡内来源/产物降级为**行式**（`bw:0`、`pad:6px 8px`、hover `--color-fill-1`）—— 避免「卡中卡」。
- **⑩ 补回划词浮条（并做成真功能）**：第三拍 ① 删它是因为当时它只服务 side chat、另一枚是空壳；
  本拍**补回并做实** —— 两枚 **DS 文字按钮**（`giencoder-btn giencoder-btn-text giencoder-btn-size-small`）：
  「添加到对话」把选中文本追加进主 `textarea`（按 placeholder「描述你的任务」定位），「复制」走 `execCommand('copy')`。
  实测：选区上方 `barRect[18,89,200,38]`、`above:true`；`taBefore 0 → taAfter 17`、tail `"> /awesome-desig"`；
  两条 toast 正确；**Esc 只收浮条**（`hiddenAfterEsc:true` + `panelStillOn:true`）。
- **⑪ 补右栏右键菜单（先调查后落地）**：**九类目标共用一份表驱动容器 `.td-ctxmenu`**（`role=menu`）——
  标签 5 / 审查文件头 7 / 审查代码行 5 / 终端 6 / 浏览器元素 6 / 浏览器空白 5 / 摘要来源 3 / 摘要产物 3 / 计划条目 4；
  危险项红字（`is-danger`，如「撤销此文件的改动」）；能复用既有 handler 的一律 `元素.click()`。
  **反例**：右栏内普通空白 / 右栏外**均不接管**（证明不越界）。
- **⑫ `.td-browse-tab` 字号 12 → 14px**（`--font-size-body-1` → `--font-size-body-3`）。实测 `tabFs 14px` / `tabH 28px`。
- **⑬ 全右栏下拉改用 giencoder DS 组件**：四枚容器（`+` 菜单 / `.td-rv-scope-menu` / `.td-commit-menu` / `.td-rv-opts`）
  挂 `giencoder-select-popup + giencoder-menu`，条目 `giencoder-menu-item`、分组标题 `giencoder-menu-group-title`、
  图标位 `giencoder-menu-icon`、选中 `giencoder-menu-item-selected`；`panel.css` **自绘那节整段删掉**、只留定位与槽位。
  实测菜单 `{r:8, shadow rgba(0,0,0,.1) 0 8px 20px, maxH:280, pad:4}`、条目 `{h:36, r:4, pl:12, fs:14, gap:10}`、
  选中底 `rgb(245,248,255)`、分组标题 `fs:12 pl:16 pt:8 color:rgb(134,134,134)`。
- **🔧 本拍四个坑（PLAYBOOK P3.40）**：(a) `.td-mm-item{background:transparent}` (0,1,0) 与 DS 选中态底**打平 + 后写**
  ⇒ 选中底被抹 ⇒ 改 `:not(.giencoder-menu-item-selected)`；(b) ★★ **页面级通配适配层
  `html[data-r93-page='conversation'] .giencoder-select-popup{top:auto!important;bottom:calc(100% + 4px)!important}`（r93 ④）
  把右栏新挂的 DS 弹层一起扫到** ⇒ `rect.y = -170` 整排看不见（**开合状态全对、就是位置错**）⇒ 加 (0,3,1) 同名适配翻回向下；
  (c) ★★ **`!important` 连行内 `style.top/left` 也压得过** ⇒ 右键菜单坐标改用 `--td-ctx-x/--td-ctx-y` **自定义属性** + `!important` 规则落位；
  (d) 探针「**过渡中取值**」假失败（**第三次踩**）⇒ 打开与量测**拆两次 eval**（中间 `wait 600`）。
- 第四拍门禁复跑：幂等 ✓｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107c.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）｜
  改动面仍只有一页、`base.html` **+0 字符（472150）**｜`r107-conv-*` 各 1、`r106-*`/`r102-*`/`r101-*`/`r93-conv-*` 全 0。
  新增件：`td-ctxmenu` **8** · `td-selbar` **4** · `activate('summary')` **1** · `giencoder-menu-item` **48** · `giencoder-select-popup` **20** · `giencoder-menu-group-title` **4**。
  产物 **894916 → 920259 字符（+25343；相对 HEAD +121028）**。
  裁片 `raw/d1-summary` · `d2-modmenu` · `d3-ctxmenu` · `d4-selbar` · `d5-ctx-src` · `d6-ctx-file` · `d7-ctx-el`；探针 `ev/p107d1~d9.js` + `ev/shots107d/e.sh`。

**④e 第五拍返工（邵先生 11:3x 反馈两条 · 仍就地改 `apply107.py`，不另起代数）**：

> 原话：① 目前新右栏的**所有下拉菜单都少了 hover 效果**，需补充；
> ② `td-rv-menu giencoder-select-popup giencoder-menu td-rv-opts giencoder-popup-open`
> **这个菜单还没有应用设计系统的组件**，需改造。

- **⑭ hover 全无 → 补齐（真 bug）**：根因是第四拍那条基态
  `.td-mm-item:not(.giencoder-menu-item-selected){background:transparent}`（(0,2,0)）与 DS 的
  `.giencoder-menu-item:hover{background:--color-fill-1}`（同 (0,2,0)）**打平、但本块文档序在后** ⇒
  把 hover 底与选中底**一起压掉**（真鼠标悬停 `matches(':hover')=true` 而 `bg` 仍 `rgba(0,0,0,0)`）。
  修法：基态与 `:hover` 写**同一块、基态在前**（(0,3,0) 语境，顺序自洽），不再赌「DS 的 `:hover` 能不能活」。
  实测 `+` 菜单第 2 项 `hover:true / bg:rgb(242,242,242)`（= `--color-fill-2`），其余仍透明。
- **⑮ 下拉改挂 DS Dropdown 组件（邵先生点名 `.td-rv-opts`）**：先核字面 —— 页面里 `td-rv-opts` **只 1 处**、
  class 串与邵先生给的**完全一致**、DS 类名一个不缺 ⇒ 问题**不在「有没有挂」而在「挂错族」**。再枚举
  `giencoder-design-system/components/`：`menu.json` 是**导航菜单**（`mapsFrom: sidenav/topnav`）、
  `select.json` 是**选择器**（`.giencoder-select-popup` 是它的弹层）、**`dropdown.json`** 才是
  「点 / 悬停 / **右键**触发的**弹出菜单**，项可含图标与快捷键」（`variants.contextMenu`、
  `states.selected` = 主色文字**或勾选图标**、`hover` = `--color-fill-2`）⇒ **正主是 Dropdown**。
  改挂 `giencoder-dropdown-popup` / `-item` / `-divider`（+ 契约态 `.is-danger`），与**本页** r93 ⑦
  行右键菜单 `.r93-ctx` **同源同口径**（`task-detail` 的 `.td-ctx` 用 fill-1，注释写明「以视觉稿为准」——
  取**本页**口径保持同页自洽）。
  - **条目几何**：`pad 5px 8px / radius 4 / lh calc(22px × --ui-fs-ratio) / gap 8 / h 32`（原 36 高 / pad 0 12 / gap 10）；
  - **面板**：`pad 6 / gap 2 / radius 8 / bg-popup / border-2 1px / shadow3-down`，`min-width:168px`（DS 原生）；
  - **选中态**：DS Dropdown **没有** `-selected` 类（不虚构）⇒ 按契约取「**主色文字 + 勾选图标 ✓**」，
    两枚 radio 项补 `.td-mm-mark`；原先「浅蓝底 + 左缘 3px 条」属 Menu 族，一并撤掉；
  - **分隔线**：`<span class="td-mm-line">` → **`td-mm-line giencoder-dropdown-divider`**（DS 子部件，`1px + --color-border-1`）；
  - **分组标题** `td-mm-cap giencoder-menu-group-title` **保留**（Dropdown 无此件，借 Menu 的 DS 类；左内距 16→8 与条目对齐）；
  - **图标位** `giencoder-menu-icon` 撤掉（Dropdown 无 icon 子部件）⇒ `.td-mm-ico{display:inline-flex; flex:none}` 收回自绘；
  - **无滚动条**：原先 `max-height:280px` 把 10 项的 `.td-rv-opts` 截到 280 出滚动条 ⇒ 现在 `h:385 / ovfY:visible`；
  - **两件附带修复**：① DS 骨架 `animation: giencoder-popup-in` 播完把 `opacity` 打回 0（菜单「闪一下就不见」）
    ⇒ 适配层显式 `animation: none`；② r75 的 `.giencoder-select-popup{display:block !important}` 通配不再扫到本菜单
    ⇒ **`[hidden]` 兜底恢复可用**（实测关菜单 `afterCloseHidden:true` / `afterClosePopOpen:false`）。
- **实测（agent-browser 真机）**：`+` 菜单 `w:168 h:214 x:856 y:91`、`anim:none`；
  条目 5 项全 `pad:5px 8px / rad:4px / lh:22px / h:32`；`.td-rv-opts` `w:172 h:385`、3 条 divider（`h:1 bg:rgb(242,242,242)`）、
  选中项 `is-checked` + `✓ opacity:1`；`.td-rv-scope-menu` 3 项 / `.td-commit-menu` 2 项；
  `.td-ctxmenu` `pos:fixed x:980 y:320 w:186.52 h:144` 3 项、`head.h:28`、首项「复制链接」；
  **全页残留断言：`giencoder-select-popup` 0 · `giencoder-menu-item` 0 · `giencoder-menu-icon` 0**
  （反面 `dropdown-popup` 5 · `dropdown-item` 23 · `dropdown-divider` 3）。
- 第五拍门禁复跑：幂等 ✓｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107c.txt` **逐字节相同**
  （21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜改动面仍只有一页（`+2107 / −3` 行）、
  `base.html` **472150 字符逐字节不变**。产物 **920259 → 921730 字符（+1471；相对 HEAD +122499）**。
  裁片 `raw/e4-mod-hover` · `e5-ctx-hover` · `e6-opts-new`；探针 `ev/p107e1/e2.js` + `ev/fix107e1/e2.py` + `ev/verify107e.sh`。

**★ 第六拍三条（邵先生 11:4x）—— 全部落在本页适配层，源件一字未动**：
- **⑯ 输入卡下方那行统计小字「框选不到」= 它是 CSS 生成内容**（本轮最值钱的一条）：
  宿主不是邵先生点名的那串 class（那是**输入卡**），而是它**下面一行** —— 由 r97 ④ 用纯 CSS
  `… > div.mt-8::after { content: '2 轮 · 27 步 · …' }` 挂出来的。**生成内容不是 DOM 的一部分**
  ⇒ 选区落不进去。**判据三条**：① 拖行后 `Selection.toString()` **长度 0**；
  ② `caretRangeFromPoint` 的 `startContainer` 是 `DIV`、`offset 0`（没有可落的文本节点）；
  ③ `Range.selectNodeContents(宿主)` 只给 131 字符（= 卡内文案），**不含那 111 字的统计行**。
  ★ **隔离对照（决定性）**：`ev/p107f4.js` 临时建两块 DOM ——
  `#zzA::after{content:"PSEUDO-SELECT-ME"}` vs `#zzB` 真文本，**同一次运行、同一套拖选手法**：
  前者 `picked:""`、后者 `picked:"REAL-SELECT-ME"` ⇒ 排除「探针写错了」。
  ⇒ **修法**：同选择器 + 文档序在后的 `content: none` 关掉伪元素 → `panel.js` 注入真节点
  `.r107-stats`（文案逐字照搬），`panel.css` 第 10 节复刻版式（`12px` / 行高 `16×ratio` / `--r93-meta` / nowrap）。
  ⚠ **宿主是 React 的地盘** ⇒ `MutationObserver`（`document.body` / `childList + subtree`）兜两件事：
  ① 重渲染会把不认识的节点**摘掉**；② 重挂时 React 把输入卡插到**末尾**，我们要**再挪回末尾**
  （否则统计行跑到输入卡上面）。回调只做「判存 + `lastElementChild !== el` 就 `appendChild`」
  ⇒ 自己造成的 mutation 再进一次回调时判存即返回，**天然收敛**。
  实测四档（1440 关 / 1440 开 / 1280 开 / 1100 开）：`statsFound:true` · `isLast:true` · 宿主 `gap:8px` ·
  计算样式与旧伪元素**逐项相同** · rect `[420,867,860,16]`（卡底 859 + gap 8 = 867，与伪元素版同一行）·
  **`selLen` 0 → 103/103/90/62**。
- **⑰ `.r93-pre` 去掉字体族** ⇒ `font-family: var(--font-family)`（= 站点默认档，定义在页面 @332458）。
  **不写 `inherit`** —— 语义直白、不赌祖先链上没人另设字体。只覆写这一条：
  盒模型 / 字号（`14px`）/ 行高（`16px`）/ 换行策略一字不动。实测 `preFont === bodyFont`、全页 `.r93-pre` 只剩 **1 种**字体族。
- **⑱ 内容列变窄时两条自适应**（判据 = **容器可用宽**，不是视口分辨率；写法同 ④b 的 `.r93-bub`）：
  - **技能选择浮窗**（React **行内** `style` 写死 `width:760`）⇒ `width: min(760px, 100%) !important`。
    ⚠ `!important` 是**必需**的：行内样式优先级最高，靠特异性不够（这是本页的已知盲区之一）。
    包含块是输入卡（`position: relative`）⇒ `100%` = 输入卡内宽，浮窗恒居中、不越界。
    实测溢出 **1440 +23/+23 → −23/−23**；**1280 +81/+81 → −23/−23**；1100 同样。
  - **`.r93-alert`** 定高 `44` ⇒ `height:auto; min-height:44px; padding:8px 16px`。
    `8px` 竖内距与**单行态完全等价**（内容 22+16 = 38 < 44 ⇒ 仍顶到 44，`align-items:center` 照样居中）
    ⇒ **单行宽度零变化**；折行时才真正长高（1280 `h:62` / 1100 `h:106`），
    且 `clientHeight === scrollHeight`（`60/60`、`104/104`）⇒ **不再把描述文字挤出圆角盒**。
    改前读数（右栏开）：1440 `42/42` ✓｜1280 `42/43`｜1100 `42/65`｜1024 `42/87`。
- 第六拍门禁复跑：幂等 ✓（第二遍「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107c.txt`
  **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜改动面仍只有一页（`+2202 / −3` 行）、
  `base.html` **472150 字符逐字节不变**。产物 **921730 → 925776 字符（+4046；相对 HEAD +126545）**；
  增量归属已核：**+4046 = panel.css +2723 + panel.js +1324**（差 1 字节 = 注入时 `.strip()` 去掉的尾换行）。
  ⚠ 体位要点：`_head.html` / `_mods.html` 未动 ⇒ `splice107.py` 重跑后 `browse.html` **sha1 不变**（已验）；
  `fs.converge()` 会把 `<style id="r107-conv-css">` **整块 stash 跳过**（`RE_OWN_STYLE`）⇒ 新增的 `min-height` 不会被 unscale 吃掉。
  裁片 `raw/f1-composer`（改前底排）· `f3-alert1100`（改前 alert 溢出）· `f4-skill1280`（改前浮窗被裁）·
  `g1-stats`（改后统计行**可框选**）· `g3-skill1280` · `g5-alert1100`；
  探针 `ev/p107f1~f7.js` + `p107g1.js` + `probe107f.sh` + `verify107g.sh`。

**★ 第七拍七条（邵先生 12:1x）**：
- ① **竞品名 → GienCoder**：右栏里**渲染成文字**的 8 处（`.td-diff-path` 文件名 / `.td-dr-t` ×3 /
  `.td-sum-p` 描述段 / `.td-sum-src b` ×3）+ 两处悬停 `title`。判据 = `TreeWalker(SHOW_TEXT)` 走 `.td-browse`，
  `/codex|chat\s?gpt/i` **8 → 0**（四档一致）；属性扫描（排除 `href`）**2 → 0**。
  **有意保留**：三条 `td-sum-src` 外链 `href` + 前六拍的 7 处设计来源注释。
  **另清一处（真·全局）**：`pages/avatar.html` 历史会话列表那条示例标题 ⇒ `git diff --numstat` = `+1 / −1`；
  `make107.py` 的 EDITS **11 → 13 处**（E12 正向 / E13 逆向，锚点用带引号的整串 ⇒ 不碰同名注释）。
- ② **去掉下拉菜单的标题行** ⇒ `.td-browse .td-mm-cap, .td-browse .td-ctx-head { display:none }`
  （静态 + JS 现场生成两类一并关）。实测 `capDisp:"none"`、`getBoundingClientRect()` 归零。
- ③ **选中项常显底色** ⇒ 改前 `rgba(0,0,0,0)`、改后 `rgb(245,248,255)`（= `--color-primary-light-1`，
  口径取自 DS Menu 的 `.giencoder-menu-item-selected`；**不补**那枚 3px 左缘条 —— 第五拍已认定那是 Menu 族的表达）。
  规则写在 `:hover` 之后 ⇒ 悬停选中项不翻成 hover 灰。
- ④ **去掉快捷键** ⇒ `.td-browse .td-mm-key, .td-browse .td-ctx-key { display:none }`
  （静态实测 10 处：⇧⌘G / ⌃` / ⌘T / ⌘P / ⌘I / ⌥⌘C / ⌥⌘P / ⌘1 / ⌘2 / ⌘R）。
- ⑤ **提交卡输入框拉通** ⇒ 改前 `207 / 可用 308`（同卡 `.td-commit-h/-lb/-msg/-f` 都是 308）⇒
  `.giencoder-input-wrapper.td-commit-in { display:flex }` ⇒ 改后 `308 / 308`、`gap:0`。
- ⑥ **右栏字体统一** ⇒ `panel.css` 自己那 8 条就地换 `var(--font-family)`
  （`.td-diff-path` / `.td-diff-stat` / `.td-dr` / `.td-dsc-c` / `.td-diff-more` / `.td-commit-num` /
  `.td-term` / `.td-url-pill input`）；「文件」模块代码区那条在 r102 代已交付的 `part105/browse.css` 里
  ⇒ 末尾用 `.td-browse .td-browse-pre { font-family: var(--font-family) }` 覆盖（153 个 `.td-code*` 靠继承）。
  判据：`.td-browse *`（1137→1149 个元素）里 `fontFamily !== bodyFont` 的**计数 153 → 0**。
- ⑦ **全屏按钮联动** ⇒ `.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }`（**纯 CSS**）。
  实测右栏关 `display:flex`（`rect [1359,57,28,28]`）/ 开 `display:none`（rect 归零）。
- 第七拍门禁：幂等 ✓（第二遍「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107c.txt`
  **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜改动面 = `M conversation.html`（`+2244 / −3`）
  + `M avatar.html`（`+1 / −1`）；`base.html` **472150 字符逐字节不变**。
  产物 **925776 → 927464 字符（+1688；相对 HEAD +128233）**；
  资产 `_mods.html 35916 · browse.html 71578 · panel.css 39686`（`panel.js 48583` / `_head.html 5270` 未动）。
  裁片：改前 `raw/h2-{add-menu,opts-menu,commit}`、改后 `raw/h3-{add-menu,opts-menu,commit,ctxmenu}`；
  探针 `ev/p107h1~h3.js` + `probe107h{,2,3}.sh`；动手前备份 `ev/bak7/`。

**⑤ 七查（全绿 · 七拍各跑一遍）**：幂等 ✓（**每拍连跑两遍**，第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10 通过**（conversation `script=9 style=16`，七拍不变）｜
`verify-design.py ./pages` 与 `mg-work/r101/ev/vd-r101a.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增**｜
**改动面 = 只有 `pages/conversation.html`**（`git status` 实证）。另验：文件模块回归（树 28 行 / 开合 / 选中 / 隐藏目录全通）、
暗色档（加行底 `rgb(18,60,25)`、标注条 `rgb(84,151,255)` = 纯 token 自动翻转）、
`--ui-fs=18`（标签 28→36、字 13→16.71，栏内溢出 0）、1280 五标签（`scrollWidth 444 == clientWidth 444`，溢出 0）。

**⑥ 已知取舍 7 条**见 `mg-work/r107/acceptance.md` 第五节（中文标签 / 终端标签名 / 末枚不给关 /
`⤢` 口径 = 侧栏最大化而非窗级全屏 / diff 取加绿删红 / `--ui-fs>22` 时栏高要跟着 ratio 长 / ＋菜单无键盘导航）。

**⚠ 本代不要重跑 `apply106.py`**（它的 GENS 四代 ⇒ 会把「基线残留 r107-conv-css」判成错误退出）。
退 r107 只需 `git checkout -- pages/conversation.html`。

**⑧ 第八拍（邵先生 2026-10-01 12:3x 返工 · 六条）** —— 六条全落 `part107/panel.css` + `panel.js`，
`_mods.html` / `browse.html` 一字未动（不必重跑 splice / make）：
1. **全局「宽度不够 ⇒ 省略号」**（新增第 14 节，17 类单行文本容器挂三件套）；★ **三类分治** ——
   单行文本 ⇒ 截断；**代码 / 终端**与**多行正文** ⇒ 保持折行、**明确不截断**（截断即丢信息）。
   ⚠ flex / inline-flex 容器里的裸文本是**匿名 flex 项** ⇒ 容器上的 `text-overflow` 无效，文字在子 `<span>` 的要单独点。
2. **去掉「折叠此文件」**（`ctxForFile()` 整项删；右键文件菜单 = 6 项，尾为「展开全部文件」）。
3. **`.td-sum-h` = 15px**（写 `calc(15px * var(--ui-fs-ratio))`，15px 无 title token；行高随 22.5）。
4. **`.td-diff-path` 展开后中粗 500**。
5. **`.td-diff-path` / `.td-diff-rows` 内一律 13px**（只换 token 档位；子规则逐条同值覆盖；
   `.td-dr` 行高 20 / `.td-diff-h` 38 未变 ⇒ converge 派生链完好）。
6. **`.r107-stats` 文字居中** ⇒ ★ **两处死胡同**：`fit-content + margin:auto` 被页面级两条 `!important`
   盒宽规则压死（盒宽恒等于输入卡 860/714/315）；真节点不像 `::after` 自动 shrink-wrap ⇒ `margin:auto` 偏 **32px**
   ⇒ 正解 = **`text-align: center`**。★ ① 与 ⑥ 可共存（居中 + 溢出时 Chromium 退化为 `start`、省略号照落行尾）。

**第八拍门禁**：幂等 ✓（`应用 0 / 跳过 8`）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107h.txt`
**逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜`scan-flatten` 改前改后均 2 条（无新增压平）。
产物 **927464 → 930384 字符（+2920；相对 HEAD +131153）**；工作区字节 1026880 / UTF-8（LF 归一）1019883 / LF `sha1 c8b5e944e2de`。
资产 `panel.css 42788`（CRLF 889 行）· `panel.js 48401`（LF 1127 行）。探针 `ev/p107i1~i5.js` + `probe107i{,2,3,4,5}.sh`；
出图 `raw/i{1,2,3}-*.png`。动手前备份 `ev/bak8/`。

**⑨ 第九拍（邵先生 2026-10-01 13:1x 返工 · 两条）** —— 两条都在右栏「全屏」这条线上：
1. **全屏后按钮图标不翻**（真 bug）—— 内联 SVG 是 `browse.html` 写死的「四角朝外」，
   `panel.js` 只翻了 `aria-pressed` / `title` / `aria-label`，`<path d>` 一字未动。
   ⇒ 抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；MAX **从 DOM 读出来缓存**、MIN 硬编码
   （Lucide `minimize` 四条），只切 `d`、不重建节点。
   ★ 目视复核：`raw/j3-bar-1440-{max,min}.png` 两枚字形方向相反。
2. **全屏后拖分栏条「一按就复位」**（真 bug，两个因）——
   (a) `ctrl-conv.js` 的 `startPanel = panelW` 取的是**内部缓存**，而「最大化」绕过控制器直接写
       `--av-browse-w` ⇒ 缓存停在 641、实际 1040 ⇒ 一按下拖动宽度猛跳到 **761**（实测）；
       改读**实际渲染宽**（先 `.is-col-dragging` 停过渡再取几何）并同步缓存。
   (b) `pointermove` / `pointerup` 挂**元素**、只靠 `setPointerCapture` 兜 ⇒ 改挂 **`window`** + `blur`。
   ★ 判据 = 把 `pointermove` **派发到 `document.body`** 仍能拖动（1040 → 960 ✓）。
   另补两条退出路径：**全屏态下按下分栏条 = 放弃全屏**（`setMax(false, true)`，不动宽）；
   **收起侧栏也退全屏** —— 搭 ctrl-conv `setOpen()` 必定 dispatch 的 resize，
   **别用 MutationObserver 盯后插节点的父级**（本拍第一版就这么坏的：观察挂在旧父级、永不触发
   ⇒ `data-td-maxw` 残留、按钮仍是「还原」态）。
★ **体位**：`part105/ctrl-conv.js` 是**跨代资产**（源页 `avatar.html` 的移植源）⇒ 本代按
   `_read_part()` 的双目录回退，在 `part107/ctrl-conv.js` 放**逐字副本 + 一处修正**，
   part105 与 avatar 零影响（⚠ 副本漂移已在文件头写明）。适配层**零 CSS 改动**。
   门禁全绿（幂等 / `check-syntax` 10/10 / `verify-design` 逐字节同 / `scan-flatten` 仍 2 条），
   产物 **930384 → 934109 字符**（+3725），`+2373 / −8` 行。

**⑩ 第十拍（邵先生 2026-10-01 13:2x 返工 · 一条）** —— **`.td-rv-menu` 菜单跑到触发按钮上方**：
1. 四枚下拉共用一条基类规则 `{ position:absolute; top:42px }`（相对 `.td-browse`，42px = 标签栏下方）。
   但 `.td-mod-menu` 的触发器（`+`）在**标签栏**里、另三枚（`.td-rv-scope-menu` / `.td-rv-opts` /
   `.td-commit-menu`）的触发器在**审查模块的工具条**里 ⇒ 后者实测 dy = **−35.0 / −34.0 / −36.0**
   （在按钮**上方** 35px 左右）。★ **一条 `top` 服务两种锚点高度 ⇒ 必然错一半。**
2. 修法 = 新增 `placeRv(menu, trigger)`，在 `toggleMenu()` 打开分支（**摘掉 `[hidden]` 之后**）
   按触发器的**实际几何**现场摆位：垂直 = 下方 6px；水平 = 左缘对齐触发器，右侧放不下就
   clamp 到面板右内边。量宽高用 `offsetWidth`（不受入场 `scale(0.96)` 影响）。
   CSS 只把共用规则拆两条 + 给 `.td-rv-menu` 一个静态兜底 `top: 83px`；**`.td-mod-menu` 一字不动**。
3. ★ 实测三枚 dy 全 **+6.0**、dxLeft **0.0 / −0.1 / −14.1**（末者 = clamp 生效）；`.td-mod-menu`
   回归不变；窄栏 315 三枚全部 `insideMod=true` 未被 `.td-mod{overflow:hidden}` 裁；
   Esc 关 / 点空白关 / 重开位置一致 / 右键菜单不受影响 —— 全绿。
   门禁：幂等 ✓ / `check-syntax` 10/10 / `verify-design` 与上轮逐字节同 / `scan-flatten` 仍 2 条。
   产物 **934109 → 936625 字符**（+2516），`+2419 / −8` 行。适配层**零字号改动**。

**⑪ 第十一拍（邵先生 2026-10-01 13:4x 返工 · 四条）**：
1. **`.td-selbar` 图标 / 文字应为正文黑** —— DS `.giencoder-btn-text` 基类给的是**主色蓝**
   （实测 `rgb(55,112,247)`）⇒ 加 `.td-selbar .giencoder-btn { color: var(--color-text-1) }`
   （SVG 走 `currentColor` 跟着变）。实测两枚按钮 `color` / SVG `stroke` 全变 **`rgb(31,31,31)`**。
2. **`.td-url-pill` 补「输入中激活态」** —— 原来 `input:focus{outline:none}` 且只有灰底 ⇒ **聚焦零变化**。
   照 DS `.giencoder-input-wrapper:focus-within` 写「底色转白 + `inset` 1px 主色 + 外 2px 浅主色环 +
   `transition 120ms`」；★ **用 `inset` 不用 `border`**（border 会把 26px 胶囊撑高）。
   ★ 取证坑：`focus()` 后**同步** `getComputedStyle` 读到的是**过渡起点** ⇒ 必须等 400ms 再读。
3. **数字动效太慢** —— 根因两层：`delay 1.5s + fill:both` ⇒ 延迟期窗口是空的；而 1.5s 是
   **为等骨架屏退场**（`.r93-sk` 不透明 `inset:0`）。改前真机时间线 **2012 淡出 → 2326 移除 → 2493 首见**。
   修法**两边一起动**：`apply107.py` 的 `wire()` 骨架屏 `1100→380`（保留 320）+
   CSS 数字 `duration .46→.30` / `delay 1.5s→calc(.44s + ni*26ms)` ⇒ 空窗 **167ms → 0**。整体 ~1.66s。
4. **对照 Codex 官方补缺，落地三件**：**终端多标签**（`.td-term-tabs` + `bindTerm()` 按块绑定 +
   `+` 真新建；右键那条也从「只弹 toast」改成真新建）· **浏览器截图**（相机按钮 + `.td-brw.is-shot::after`
   快门 **260ms**，闪**整模块**而非滚动容器 `.td-view`）· **产物预览层**（`.td-sum-prev` 覆盖摘要 +
   `md`/`xlsx` 两套骨架 + **Esc 算一层**）。官方 SSH / 多窗口 / 托盘不在静态页范围 ⇒ 不做。
   门禁：幂等 ✓ / `check-syntax` 10/10 / `verify-design` 与上轮**逐字节同** / `scan-flatten` 仍 2 条。
   产物 **936625 → 958568 字符**（+21943），`+2806 / −12` 行。★ 本拍**首次动了 `_mods.html`**
   ⇒ 改序 = `_mods.html → ev/splice107.py → apply107.py`（`browse.html` 是 splice 的产物）。

## 二·h ★★ r108（最新一拍 · 会话详情页「diff 卡片化 + 文件树抽屉」· 2026-10-01 19:4x 起，共**十二拍**）—— **新一代（r107 已交付 `e9c9498`），🚫 未提交**

> 完整版见 `mg-work/r108/acceptance.md`（**七节**）；机制级教训见 PLAYBOOK **P3.48**；本页固定事实见 PAGES **P3.11i**。

**① 体位**：r107 **已交付 `e9c9498`** ⇒ **新建 `mg-work/r108/apply108.py`**（**不就地返工**），
由 **`ev/make108.py`** 从 `apply107.py` 做 **7 处精确替换**生成
（E1 标题 / E2 ×5 路径 / E2b ×2 段号 / E3 `GENS` 加第六代 / E4 `PART_DIRS` 加 `part108` / E5 注释目录名 / E6 docstring 加第十二拍块；
每处命中数断言，不符即 `sys.exit`）。`GENS` 扩成**六代**（r93/r101/r102/r106/r107/r108）。

**★★★ nav 块继续沿用 `r106-nav-js`（不换名）**：`GENS[-1] = ('r108','r108-conv-css','r108-conv-js','r106-nav-js')` + `NAV_TAG='r106'`
⇒ `base.html` 与 8 个外壳页**逐字节不变**，`git status` 只有 `conversation.html` 一个 ` M`。
⚠ **但 CSS / JS 两块都改了 ⇒ 必须换名 `r108-conv-css` / `r108-conv-js`**（否则「摘块」正则会连本代新内容一起摘掉）。

**② `PART_DIRS` 三级回落**：`(part108, part107, part105)` —— 本代只覆盖改过的三件
（`_mods.html` · `panel.css` · `panel.js`），`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 继续从 part107 / part105 取。

**③ 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_mods.html`（44246 → 52848 字节） | ① 工具条 `.td-mod-bar-acts` 里「在文件树中定位」**右紧邻**插 `data-td-rv-act="tree"` 按钮（folder-tree SVG）；② `</aside>` 前追加 `.td-tree[data-td-tree]` 抽屉（`.td-tree-scrim` / `.td-tree-panel` / `.td-tree-h` / `.td-browse-search` / `.td-tree-files` 10 行 `.td-tf*`） |
| `part108/panel.css`（1090 → 1196 行） | **新增第 18 节**（`/* r108-l1 */` 幂等标记）：18.1 diff 卡片化 · 18.2 文件树抽屉 · `.td-tf*` 行几何逐条对齐 `browse.css` 的 `.td-bf` |
| `part108/panel.js`（1335 → 1412 行） | 抽屉控制器（`treeRefresh()` / `treeShow()` / `treeHide()` + 点击委托 + document 点击收抽屉）；Esc 裁决链**加抽屉一层**（`if (treeOpen) { treeHide(); return; }` 插在 `modal` 之后、`menuOpen` 之前）；`[data-td-rv-act]` 通用循环加 `if (kind === 'tree') return;` |
| `ev/make108.py` · `ev/splice108.py` · `ev/patch108l1.py` | 生成器（7 处替换）/ 组装器（头部取 part107、新模块取 part108、Files 正文从 part105 剪出）/ 补丁（6 步，`mark = new` 幂等） |

**★★★ 独立类名隔离**：`ctrl-conv.js` 的 `pane = slot.querySelector('.td-browse')`（**整个 aside**）、
`rows = pane.querySelectorAll('.td-bf')`、`files = pane.querySelector('.td-browse-files')`（**只绑第一个**）
⇒ 抽屉树**必须用独立类名 `td-tf*`**，否则两边互相打架且抽屉里的行点了没反应。
★ 实测零干扰：抽屉里点 `Controls.tsx` ⇒ 抽屉 `drawerActive` 变，而「文件」模块那棵树 `filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**。
★ 抽屉树自身折叠：点 `games` ⇒ `visibleRows 10 → 3`，再点回 10。

**④ 真机实测（1440）**

* diff：四张卡 rect `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`，**卡间距 `[8,8,8]`**；
  卡描边 `1px solid rgb(229,229,229)` / 圆角 `8px` / 底 `rgb(255,255,255)` / `overflow:hidden`；
  头 / 体分隔线 `1px rgb(242,242,242)`；并排下折叠 ⇒ 卡高 **40**、`rowsDisplay:none`（**无残留分隔线**）。
* 按钮位置（`raw/m-1440-rvbar.png`）：工具条右端 = 复制 · **定位** · **文件树** · `⋯` · 提交⌄ · PR ⇒ **在「在文件树中定位」右紧邻** ✓。
* 抽屉：`hidden:true→false`、`is-open` 同步、`btnAria false→true`、**`panelBox=[1135,49,296,842]`**、`transform:none`、`scrim opacity 1`；
  与右栏 `paneBox=[791,48,641,844]` ⇒ 面板右缘 `1135+296 = 1431 = 791+641−1` = **紧贴右栏右缘** ✓。
* 关闭路径：点遮罩 ⇒ `hidden=true` + `paneOpen=true`（**侧栏没被误关**）；**Esc** ⇒ `hidden=true` / `paneOpen=true` / `paneHidden=false`（**只关抽屉**）；重开 ⇒ `panelBox` 不变（无残留污染）。
* 边界：`.td-tree-h` h=**40** fs=14px；`.td-tf` h=**28** fs=13px；并排 `isSplit=true` / 统一行 `display:none` / 并排行 `display:block` + `border-top:1px`；
  **`--ui-fs=18`** ⇒ 树行 **28 → 36**、头部 **40 → 51**、行字号 13 → 16.71px（**杠杆生效、没被压平**）；窄档 620 ⇒ 面板仍 296。

**⑤ 途中排掉三处坑**（详见 PLAYBOOK **P3.48**）

1. **「文件树」按钮弹多余「已执行」toast** —— `panel.js` 的 `[data-td-rv-act]` 通用循环（`say(ACT_TEXT[kind] || '已执行')`）把它也吃了 ⇒
   在 `closeMenus(null)` 之后加 `if (kind === 'tree') return;`（**保留 closeMenus**、只跳过 toast）。
   复测：点「文件树」⇒ `toastShown=false`；再点「在文件树中定位」⇒ `toastText="已在「文件」标签中定位该文件"` + `activeTab="文件"` ⇒ **老动作没被带坏** ✓。
2. **`.td-tree-h` 被 `scan-flatten` 多报 1 条（3 条 > 基线 2 条）** —— 该规则有 `height/min-height: calc(40px * var(--ui-fs-ratio))` 但体里
   **没有 `var(--font-size-*)`** ⇒ 会被 `apply88b.converge()` 压平成裸 40px ⇒ 补 `font-size: var(--font-size-body-3)`（`patch108l1.py` 的 `CSS_NEW` 同步）⇒ 回到 **2 条** ✓。
3. **探针两处假失败（产品代码没问题）** —— ① 抽屉开着时遮罩 `z-index:35` 挡住工具条点击 ⇒ 想点 `⋯` 切「并排视图」必须先关抽屉；
   ② 上一版探针写 `document.querySelector(...) || (fn)().click()` 这种**短路表达式** ⇒ 左侧 `querySelector` 命中（哪怕元素 hidden）就短路，
   「并排」根本没切过去。修：`probe108m6.sh` **先确认抽屉关闭**再点 ⇒ `isSplit=true` ✓。

**⑥ 产物与门禁**：`conversation.html` **958568 → 978614 字符**（+20046）；LF bytes **1078406** / 工作区 bytes **1086146** / **7741 行** / LF `sha1_lf 7a1be6be9b76`；
`base.html` **472150 逐字节不变**；`git diff --numstat` = `248  3  pages/conversation.html`。
幂等 ✓（`patch108l1.py` 第二遍「应用 0 / 跳过 6」；`apply108.py` 第二遍「已是目标态」）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
`verify-design.py ./pages` 与 `mg-work/r107/ev/vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`，21882 字节 ⇒ 零新增）｜
`scan-flatten.py part108/panel.css` ⇒ **2 条**（`.td-mod-bar` / `.td-url`）。

**⑦ 交接**：🚫 **未 commit / 未 push**（等邵先生显式发话）。提交时注意 `git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`（返工期的临时三源快照、不入库）。

---

## 三、r88 ~ r92 做了什么（前情提要）

| 轮 | 需求 | 落地要点 |
|---|---|---|
| r88 | 导航 hover 底 = 选中底；字号滑块重写；新增「已归档任务」页签 | 共享变量 `--r88-navi-active`(#ECEEF2，暗色 #2E323A)；滑块换成整块命中层 + pointer 事件（move/up 挂 **window**）；新页签按 `1393:18344` 还原 |
| r89 | 标题字号与 `.r85-title` 一致；列表卡圆角共用；分隔线深一级 + 图标重画 | `--r88-card-radius:8px` 三处共用；`i_folder12`（12 网格 1:1、坐标 x.5） |
| r90 | aside 内距与基础工作台一致；容器内按钮**必须用 DS 按钮组件**；下拉前缀图标不对 | `.r85-nav-host` 撑满内容盒（244）；行尾钮换 `giencoder-btn -secondary -icon -size-small`；`i_folder` 16 网格重画 |
| r91 | 返回钮 hover 底 = 菜单 hover 底；菜单默认无背景；行尾图标浅一级 | `.r85-back:hover` 共用 `--r88-navi-active` + 补 transition；`.r85-navi` 基类 `background:none`；**`.r88-arch-act > svg`** 单独给 `text-2` |
| r92 | 顶栏装饰背景图；返回钮深一级；`.r85-gt` 左距 12px；「完全访问」转红 | 见 `## 二` 与 `PLAYBOOK P3.23`；④ 只能改 React 源（尾风任意类 + 内联 style 两个盲区） |

★ **r73 全局规则**：`.giencoder-btn:not(.giencoder-btn-size-small){border-radius:8px}` ⇒ 全站按钮口径 **large 8px / small 4px**，别再按设计稿压 6px。
★ **展开态只写 `min-height` 不写 `height`**：DS 给 `height:28px`，min-height 优先 ⇒ 默认 28 / 展开 32 两全；该规则**刻意不带 `body` 前缀**，好让 apply88b 派生 `calc(32px * ratio)`。

---

## 四、★★ 已修掉的真 bug / 陷阱（PLAYBOOK P3.21 ~ P3.24 有细则）

1. **`noClear` 的 DS select** ⇒ `suf.querySelector('.giencoder-select-clear')` 为 null ⇒ TypeError ⇒ 内容区整块空白。**修法：凡"可选子部件"一律判空。**
2. **拖拽的 `pointermove/up` 必须挂 `window`**（挂元素时 `setPointerCapture` 失败就永远收不到 up）。
3. **1px 描边中心线必须落 `.5`** ⇒ 落整数会摊成两列 50% 灰像素（肉眼=又细又虚）。
4. **元素截图超出视口的部分渲染成空白** ⇒ 截图前必须 `set viewport` 并在同链路 `eval window.innerHeight` 核对。
5. **元素截图内取色的坐标 = 元素内相对坐标** ⇒ 先 `eval` 拿「元素 rect − 容器 rect」。
6. ★ **`inject_tail` 别断言 `count('</body>') == 1`**：`base.html` 的 r76 CSS 注释里也出现过一次 ⇒ 改用 **`rfind`** 并要求它就在文件尾部。
7. ★ **裸 `header` 标签选择器在多页会误伤**：avatar 5 个 / task-detail 4 个 ⇒ 用 `header[class*="h-12"]`。
8. ★ **尾风任意类 `[color:var(--x)]` 是构建期产物** ⇒ 新增类名不会进产物 CSS ⇒ 想给 React 渲染元素加新色，要么挂自定义类（自己写样式），要么改 React 源。
9. ★ **`.ws-dropdown-hover` 这类混用类名会重名**（工作目录 / 默认权限各一个）⇒ 探针先枚举，或用 `:has(<独有特征>)`。
10. ★★ **改字号机制后要防「特异性反噬」**：`body .text-xs` 是 **(0,1,1)**，会压掉所有 **单类** arbitrary 工具类（`.leading-[32px]` = (0,1,0)）⇒ 机制层给 size 类派行高时，必须 `:not([class*="leading-"])` 让位，并对要支持的 `leading-[Npx]` **补一条同特异性的派生规则写在后面**（r93 需求 1 根因）。
11. ★★ **导出设计稿的「状态变体」是叠放的** ⇒ 真机块高 = 容器高 − 变体偏移（r93 = 34）；**导出 PNG 的绝对 y 不可当设计坐标**，量总高必须先去掉这层 offset。
12. ★★ **`ui-component` 是不带字号的纯框** ⇒ 字号只能「框高 × 墨迹行距 × 文本宽度反推」三角验证；单看框高会把 12/20 误判成 14/22。
13. ★ **私有区图标字符（U+F0xxx）在实机无字形** ⇒ 退化成豆腐块并改变折行；导出图里的「图标」可能只是 Nerd Font 渲染的数字/符号，**先裁图看清再决定用不用**。

---

## 五、四查（全绿，详见 `mg-work/r93/acceptance.md` 第三 / 六 / 七 / 八 / **九**节）

> ★ 下表是 **r93 ④ 之后**、按官方顺序复跑实测（日志 `mg-work/r93/ev/rerun-④.log` + `vd-r93d.txt`）。

**★ r94 复查（同日第四轮）**：`apply93.py` 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 r93 基线 `vd-r93c.txt` **逐字节相同**（首跑曾因我在新注释里写了被扫描的关键词而 +1，改措辞后归零）；读数 `vd-r94.txt`（含假阳性）/ `vd-r94b.txt`（修后）。

**★ r95 复查（同日第五轮）**：同上口径全绿 —— 幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（`vd-r95.txt`）｜视觉/几何 `ev/p95b.js` 全块 **Δ=0**。

**★ r96 复查（同日第六轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 `vd-r93c.txt` **逐字节相同**（`vd-r96.txt`）｜视觉 `raw/r96-cmp2.png`（设计 vs 实机同尺度上下对照，前三段逐像素对齐）。

**★ r97 复查（同日第七轮）**：同上口径全绿 —— 幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（17148 字节，`equal: True`，`vd-r97.txt`）｜几何 `ev/p97d.sh` 在 **1440 / 2560** 双档实测（wrap/bottom/sb/composer 右边界全等）＋ `raw/r97-cmp.png`。**回归排除**：`ev/p97f.sh` 把卡内字号临时强制回 12px 再测，12 张卡的高度与溢出量逐项相同 ⇒ 那 2px 溢出是 r96 及更早就有的。

**★ r98 复查（同日第八轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 `vd-r93c.txt` **逐字节相同**（21882 字节，`equal: True`，`vd-r98.txt`）｜几何 `ev/p98b.js` 在 **1440 / 2560** 双档实测（内容区 **15px × 59**、卡内 `.r93-t14` 仍 13px、wrap pb **48**、差分卡右对齐账 ⋯−13 / 数字−54 / 名+11）＋ `raw/r98-cmp.png`。⚠ 首跑曾 **77 条**：新增注释里写了裸字号写法（`font-size: 15px`）⇒ **字号检查不跳注释行**（hex 检查会跳）⇒ 改措辞后归零。

**★ r99 复查（同日第九轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 `vd-r93c.txt` **逐字节相同**（21882 字节，`equal: True`，`vd-r99b.txt` / `vd-r99c.txt`）｜探针 `ev/p99b.js` 复测十四条（读数见上）+ `ev/p99c.js` 量 umeta 图标几何与 rateline 线↔⋯ + `ev/p99d.sh` 右键菜单展开截图 + `ev/p99f.sh` 逐区域滚动裁片 + **隔离测试页 `ev/icontest.html`**（定位 SKILL 图标的镜像 transform）。

**★ r100 复查（同日第十轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」，`task-detail` 更名也已收敛）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（`vd-r100.txt`）｜探针 `ev/p100b.js` 八条逐条复测 + 三处**真鼠标 hover** + 整行点击开菜单 + 层级树开合。

**★ r101 复查（同日第十一轮 · 最新）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**，与 `vd-r93c.txt` **逐行 diff 只剩 1 条**（conversation 渐变 `62 → 63` = ⑥ 的渐隐层，info 级页面统计）｜★ **新增决定性探针 `ev/p101hov.js`**（连查 `matches(':hover')`）⇒ 三个 hover 目标全部 `hov=true`｜**终态一次性取证 `ev/p101fin.sh` + `p101fin.log`**（骨架屏两拍 / 11 条静态读数 / 3 个 hover / dx=0 / 右键菜单）｜双视口 1440 + 2560｜像素：投影剖面 Σ\|Δ\|=3、渐隐带 `r101-fin-fadezoom.png`。

**★ r102 ~ r105 复查（同日第十二~十五轮 · 已全部落地并提交 `87e2caa`）**：同一口径全绿 ——
幂等 ✓（第二遍双「已是目标态」，r105 后 `conversation.html` sha **不变**）｜`check-syntax pages/*.html` **10/10 ALL_OK**
（conversation `script=9 style=16` —— **16 与 HEAD 一致，旧记录写 15 是笔误**）｜`verify-design ./pages` 与 **`vd-r101e.txt`
逐字节相同**（**17148 字符** / md5 `84f552c5b5a6` / `diff_exit=0`）⇒ **零新增**｜
代数标记：真·注入块 `r102-conv-css` / `r102-conv-js` 各 1（conversation）、`r102-nav-js` 1（base）+ 1×8（其余 8 页，**conversation 为 0**）；
**历代 id 残留 0**（`r93-*` / `r101-*` 全清）｜
r105 死代码：`r93-morebtn` 全仓 **3 处全在注释**（活规则 0 条）。逐条见 `mg-work/r102/acceptance.md` 的 r102 / r103 / r104 / **r105** 段。

| 查 | 结果 |
|---|---|
| 幂等 | `apply88.py` `457805 → 457805 (+0)`（**且未摘掉 settings 的 ROUTE 条目**）；`apply88b` **10 页全「已是目标态」**（含新页 `conversation.html`）；`apply92.py` **应用 0 / 跳过 8**；`apply93.py` 第二遍起 **base + conversation 双「已是目标态（无改动）」**；**`apply101.py` 第二遍「已是目标态（无改动）」**；`base` / `conversation` 字节 sha 复跑前后一致 |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（base `script=9 style=15` / **conversation `script=9 style=16`**） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical）；r101 与 `vd-r93c.txt` **逐行 diff 只剩 1 条**（渐变 62→63）；④ 前 9 页 = **75 条**（`vd-r93c-base.txt`）⇒ **唯一新增 = `conversation.html` 的 1 条 `CRAFT-SLOP`**（info 级页面级统计，非缺陷），**warning 66 / critical 0 不变**；base 原有 2 条 `TOKEN-GAP`（`#E2D3F9`/`#30953B`）随块搬到新页（同型同量、只换文件名） |
| 代数标记 | r102 起必查残留：`conversation` 的 `r102-conv-css`/`r102-conv-js` 各 **1**、`base` 的 `r102-nav-js` **1**、其余 8 页各 **1**；**`r93-conv-*` / `r101-conv-*` 必须 0** |
| 路由 | 10 页 `ROUTE` 表各含 `'/conversation'` **恰好 1 次**（counted 断言） |
| 视觉/像素 | 会话详情 `raw/v3-conv-top.png` `v3-conv-bottom.png`（+ `v3-base.png` 对照）；composer 复用 `raw/q-real-composer.png`(真组件 1114×214) vs `raw/q-design-composer.png` / `q-design-bottom.png`；下拉翻向取证 `raw/v3-perm-up.png`；r101 新增 `raw/r101-fin-*.png`（骨架屏 / 右键菜单 / 渐隐带 2× / 全页） |

⚠ 跑完必须还原工作区：`git checkout -- pages/gaps.log` + `git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`。

---

## 六、待拍板 / 待确认（邵先生）

1. ★ **r92 ① 的范围**：现落**基础工作台 5 页**。若「全站 9 页」也要，需同时决定研发页顶栏底色（`#E5EDF5`）是否一起换掉。
2. ★ **r92 ① 的尺寸**：现为素材原尺寸（点径 4px）+ 视口 >1580 时 x=340 接缝。
3. **r92 ④ 的红色档**：现 `--color-danger-6`（`#F53F3F`）；嫌艳可降 `--color-danger-5`。
4. **r90 三处「按 DS 组件口径、偏离设计稿」**：行尾钮圆角 6→4px、清空钮 8px、行尾钮描边 `border-2`。
5. ★ **r91 行尾图标色**：现 `text-2`(#4E4E4E)，设计稿实测是 `#6B6B6B`（`--color-neutral-7`）⇒ 要精确贴稿就改 `.r88-arch-act > svg` 一行。
6. **r89 遗留**：24px 极限字号档工具条溢出卡片右缘 18px（默认档无此问题）。
7. **返回钮与菜单项几何不一致**：`.r85-back` 高 32 / 圆角 4px，`.r85-navi` 高 36 / 圆角 8px（r91 只统一了底色）。
8. **`#ECEEF2` 是否提到 DS 色板**：现为页面级变量，使用面已扩到 3 处。
9. **「清空归档任务」无二次确认**；**全站 Input 圆角是否统一 8px**；**r90「全局强制用 DS 按钮」是否贯彻到全站**。
10. **r93 结转 —— Δ2 级微差**：搜索资料卡 152→150、改动汇总卡 302→300（均在 1 行行高内，疑似字体度量）。
11. **r93 结转 —— 字体度量差异**：上下文注入卡设计稿（MiSans）5 行 vs 实机（Mona Sans）4 行 ⇒ 现用 `min-height:150px` 保高；若要严格 5 行需换字体或调 `letter-spacing`。
12. **r93 ④ 新页上下文丢失**：`conversation.html` 是**整页重载** ⇒ 从 aside 点会话项跳过去后，**选中态/滚动位置回到默认**（React 重新渲染）。要不要「hash 带会话 id + 落地后回高亮该会话」？
13. **r93 ④ 新页标题**：现 `<title>会话 · 基础工作台</title>`；是否要跟「会话名」联动（需外壳暴露会话数据）。
14. **r95 结转 —— `.r93-agent` 那 4 张 agent 卡要不要也「均分撑满」**：现按内容宽**左对齐**（设计稿固定排版），
    r95 只把它们的**容器**（`.r93-bottom > *`）改成撑满；若要求 4 张卡 `flex:1` 平分 860，说一声即可（一行 CSS）。
15. **r95 结转 —— `.r93-bub`（用户气泡 728px）要不要也撑满**：现**右对齐不满宽**（设计稿语义）。
16. **r95 结转 —— 超宽视口的理论 10px 差**：`.r93-wrap` 的 `50%` 基数是**滚动容器内容盒**（带 `both-edges` gutter ⇒ 1142），
    而 `.r93-bottom` / composer 的基数是 **1162** ⇒ **仅当 `50% > 860px`（视口 ≈2000px 以上）**时两者会差 ~10px；
    1440 / 1920 实测**完全一致**。要彻底消掉需给 wrap 补 `calc(50% + 10px)`（依赖滚动条宽度常量，**脆**，暂不做）。
17. **r96 结转 —— 「调用 5 个工具」汇总清单（`.r93-sumrow`）标题色**：设计稿 `fw647:16189`「更新任务清单」= **#1F1F1F（text-1）**，
    而我们 `.r93-sumrow` 给的是 `text-3` ⇒ 4 行标题偏浅。**本轮刻意未动**（用户只提了 `.r93-t14` 的默认色与 `.r93-t14.r93-c2`），
    要不要按稿改成 text-1？
18. **r96 结转 —— rateline 后两段 −7px**：因实机字体比设计稿窄 7px（Link 134 vs 142）。
    若要**逐像素钉死**就必须写死 `width:142px`（但会 `overflow:hidden` 截断长字），**不建议**。
19. **r96 结转 —— `.r93-dmore`（任务产物区右上「更多」）色 / 盒**：现 24×24 + `text-2`，与 rateline 新按钮（`text-3`）不一致；
    设计稿该处未核。要不要统一成 `.r93-rbtn` 口径？
20. ★ **r97 结转 —— 「整个内容的模块元素等宽」还剩两处按设计稿**：现在**全宽块**（wrap / 状态条 / agent 行 / 输入卡 / 告警 / 改动汇总 / 产物区）已全部等宽；仍**刻意未动**两处（都是设计稿的固定排版）：
    ① `.r93-card` / `.r93-todocard` = `calc(100% - 18px)` + `margin-left:18px`（设计稿 `容器 185` = `width:822px; left:18px`，右缘贴齐、左侧缩进 18）；
    ② `.r93-bub` 用户气泡 = `728px` 右对齐不满宽（设计稿语义如此）。
    若邵先生要「连卡带气泡也全部拉到 860」，分别改 2 行 / 1 行即可 —— 但那会**偏离设计稿**，故等发话。
21. **r97 结转 —— `.r93-pre--tight`（Bash 卡代码）现为 13px / 行高 16px**：统一字号后代码行高与字号之比 1.23，偏紧（卡高不变、不裁切，仅观感）。若嫌挤，给 `.r93-pre` 单独留 12px（改 1 行）。
22. **r97 结转 —— agent 卡宽度比例**：现 `flex:1 1 auto` 按内容宽比例吃余量（实测 1440 = 229/205/217/191）；设计稿是 190/169/197/**255**（第 4 张明显更宽）。若要逐张对齐设计稿宽度需写死 basis（脆），暂不做。
24. ✅ **[r99 已解决]** ~~`.r93-dsb`（差分卡里那条 6×128 滚动条）是本轮唯一「静态装饰」~~ ⇒ **r99 ① 已按邵先生要求删掉**（规则 + 模板 `<i>` 双删），`.r93-dlist` 改 `overflow-y:auto`。
25. **r98 结转 —— 15px 是字号档位之外的值**：DS 只有 body-3=14 / title-1=16，15px 只在本页适配层用 `calc(15px * var(--ui-fs-ratio))`，**未动 token**。
26. **r98 结转 —— 卡内文案比设计稿大 1px**（设计 14 → 本页 15）：这是 ①「内容区统一 15px」的必然结果，③ 只覆盖颜色 / 间距 / 结构。
27. **r99 结转 —— 差分卡行的右键菜单「刻意不做键盘导航」**：只实现 `pointerdown` / `blur` / `resize` / `scroll` / `Escape` 关闭，**未做** ↑/↓/Enter 移动焦点与 focus trap（与 `task-detail` 的 `.td-ctx` 保持一致）。若要无障碍完整版，说一声即可（约 20 行）。
28. **r99 结转 —— `regen`（重新生成）图标是手写 14 栅格**：设计稿 `1393:18477` 里该图标是 DS 实例（`fw647:14503`），**源文件里没有可复用的 path**（结构树只给节点名）⇒ 按 `design-rgb.png` 逐像素分离后手写（弧 + 左下实心箭头）。若 DS 后续产出官方图标，替换即可。
29. **r100 ③ 结转 —— 「滚动到底部」hover 的底色**：本轮只按原话撤掉了**描边**变化并把前景色深一级，`--color-fill-1` 底色**保留**（原话没提底色）。若要「连底色也不变」，把 `.r93-tobottom:hover` 里的 `background` 删掉即可（1 行）。
30. **r100 ⑧ 结转 —— 层级树的横向肘节是新增的**：设计稿 `1393:18521` 没有画连接线（PNG 该区间只扫到卡片底与描边）⇒ 竖导线 + `├─` 肘节都是本轮按原话补的。若只要一条竖线：删 `.r93-tree > .r93-fold::before, .r93-tree > .r93-sumlist > .r93-sumrow::before` 那条规则。
31. **r100 ① 结转 —— 更名范围**：`task-detail.html` 的「来源需求」示例标题也一并改了（`GienX端到端初始化…` → `GienCoder端到端初始化…`）；该文件里另两条**历史注释**中的 `GienX` 字样**刻意保留未动**（不进产物）。若要全库抹净说一声。
32. ★ **r101 ⑤ 结转 —— 删的是哪一枚绿勾**：全页 `.r93-okc` 共 2 处，本代删的是 **Bash 卡头**那枚（判据：它无文案可指、且与 ④ 的箭头同块相邻）；
    **「上下文已压缩」行首那枚保留**（带文案「已压缩 24 条历史记录」）。若指的是后者，一行改。
33. ★ **r101 ⑧ 结转 —— 图标是否要常转**：现**常转**（`r93-spin` = `1.2s linear infinite`）。若只要 hover 时转，去掉模板里的 `r93-spin` 类即可（CSS 留着无害）。
34. ★ **r101 ⑩ 结转 —— 投影档位**：现 `0 2px 9px rgba(0,0,0,0.07)`（像素剖面 Σ\|Δ\|=3，与 10px 档打平，选 9px 因上方外溢更小）。这是唯一的旋钮。
35. ✅ **[r101 已闭环]** ~~r99 ① 结转：折叠头 hover 色无法运行时直证~~ ⇒ **r101 新增 `matches(':hover')` 决定性探针**，展开头 / 折叠头 / 图标按钮三个 hover 目标全部 `hov=true` 且读数正确。
36. ★ **r101 第二批 ⑤ 结转 —— 菜单是「替换」不是「合并」**：r99 ⑦ 那张 4 项菜单（查看文件 / 查看改动 / 复制文件路径 /
    撤销此文件改动）**已整段删除**，现在汇总行右键 / 左键 / 「⋯」三处与产物卡共用同一张 6 项菜单。若其实想要**并集**，说一声即可。
37. ★ **r101 第二批 ⑦ 结转 —— 折叠动效只做了单向**：展开有 0.34s 回弹，**收起仍是瞬收**（反向要高度动画 + `overflow:hidden`，
    会剪掉卡内向上翻的 `.r93-pop`）。若要反向也动，说一声。
38. ★ **r101 第二批 ① 结转 —— 毛玻璃参数 + 一个副作用**：`--r93-glass` = `rgba(255,255,255,0.72)` / 暗色 `rgba(35,35,36,0.72)` + `blur(12px)`；
    **无设计稿依据**（设计稿没有「滚动时标题栏压住内容」这一帧）。嫌重/嫌轻改这一处即可。
    副作用：标题栏盖住的滚动口**最上 44px** 里界面元素**点不到**（滚过去的内容能滚、但点击被标题栏接住）——判定可接受，写进验收了。
39. ★ **r101 第二批 ② 结转 —— 70% 落在 6 页**：base / conversation / avatar / skills / automation / settings
    （= 所有带 `r92-hdr-css` 的页面）；研发工作台 4 页（dev / kanban / req-kanban / task-detail）本来没铺这张图 ⇒ 未动。
40. **`.r93-dmore:hover`（灰卡上那枚「⋯」）仍是「白底 + 1px 描边」**（r99 ⑨ 的设计稿实测值）：本批只点了「菜单内容一致」，
    没点按钮的 hover ⇒ 与 `.r93-ib:hover`（浅灰底、无边框）**仍不统一**。要统一说一声（一行）。
23. 更早遗留：r86 三处 DS-vs-设计稿差异；r84 avatar 确认态按钮组是否再挪 8px；r83 三条；r81 三条；r79 `r74-ripple` 死代码；r77 滚动条 hover；r74 动效 300ms 上限；`pages/gaps.log` 与页面不同步。

### r105 新增（3 条，均为「顺手替他做的判断」）

41. ★ **r105 ③b —— 全屏 = 收拢左导航**（`aside → 0`、对话区吃满整行），与数字分身全屏「让 main 让位」**同语义**。
    若要保留一条**可点回来的窄条**（如 `0 → 12px` 抓边），说一声即改（一处 CSS）。
42. ★ **r105 ③c —— 预览栏默认宽 641**（沿用数字分身 `--av-browse-w`）。本页内容更宽 ⇒ 若想本页另给默认值（如 720）可单独调一行。
43. ★ **r105 ③c —— 预览栏与「全屏」可同时开**（`x105-2-both.png`：aside 0 + 侧栏在右）。
    若要**互斥**（开全屏自动收侧栏，或反），说一声即改。

### r106 新增（4 条，均为「随手替他做的判断」）

44. ★ **r106 ① 的范围 —— 只收了点名的两块**：「上下文注入」+「深度思考」现默认折叠；下方 **12 块仍默认展开**
    （BashInspect / 网页搜索 / 需求采访 / 任务清单 / 文件写入 / SKILL / Tool call ×2 / 重试 / 调用 5 个工具 / 搜索资料 / 未知 surface 事件）。
    若想「**凡折叠块默认收**」或「**连 tool call 内嵌层一起收**」，说一声即改（一行参数 → `fold()` 调用）。
45. ★ **r106 ② 只对齐了高度、没统一底线色**：`r93-bar` 底线 `#EBEBED` 与面板底线 `#E5E5E5` **仍是两色**。
    若要统一，指定取哪一档即可（一处 CSS）。
46. ★ **r106 ④ 的「空间足够」判据 = 容器可用宽**（预览栏开/关、左导航是否收拢都会改它），**不是视口分辨率**。
    若希望改用**视口宽度断点**（`@media …1920px`），说一声即改 —— 但那会在「开了预览栏的 2560」上误判成「空间不足」。
47. ★★ **r106 ④b 的「自适应」口径（第三拍最需要邵先生点头的一条）**：本代取 **`min(100%, 728px)`**
    —— 列 ≥728 保持 **728**（设计原样）、列 <728 跟着收。**代价：1440 开（列 778）/ 1440 关（列 860）下这个块仍是 728、
    看不出变化**，只有 **列 < 728** 的窄档（1280 开 618 / 1370 开 708）才看得到。
    若他要的是「**用户消息块始终与内容列同宽**」（1440 关 860 / 开 778、2560 关 1141），那是 `width: 100%`（去上限）
    —— **一行改动**，但 2560 下气泡会宽到 1141、行长偏长 ⇒ **需他先点头**。

---

## 七、下一轮接手清单（按顺序）

1. 读本卡 → `git status` → 复跑补丁确认幂等：
   `mg-work/r88/apply88.py` → `mg-work/r88/apply88b-fontsize.py` → `mg-work/r92/apply92.py` → `mg-work/r93/apply93.py`
   → `mg-work/r101/apply101.py` → `mg-work/r102/apply102.py`
   → **`mg-work/r108/apply108.py`**
   → `mg-work/r87/apply87a-select.py` → `mg-work/r86/apply86.py`（**后两个被 r88 的 PRIOR 涵盖，重复跑也是 `+0`**）。
   ⚠ ★★ **`apply102` / `apply106` / `apply107` / `apply108` 都作用于 `conversation.html`**：前几代的块**已被 apply108 的 `GENS` 涵盖**，
     所以**只需跑 `apply108` 一条即可自愈到 r108 态**（历代块会被整块剥离再重注）。
     反过来**绝不要**跑到 r108 之后再跑 `apply107`（它只认五代 ⇒ 「基线残留 r108-conv-css」自检会直接退出）。
   ⚠ 另：`partNNN/browse.html` 是**组装件** ⇒ 改 `_head.html` / `_mods.html` 后必须重跑本代 `ev/spliceNNN.py` 再跑 `applyNNN.py`。
     本代 `part108/` 只覆盖改过的三件，其余从 `part107` / `part105` **三级回落**。

2. 改页面**一律走 `mg-work/rNN/applyNN.py`**，体位 = 「先 `strip_all(当前页)` 取净底 → 再注入」⇒ **改完直接重跑即自愈**。
   **例外**：上一轮尚未提交时的即时返工 ⇒ **就地修订原补丁、不另起代数**（判据：`git status` 里仍是 ` M`）。
   ★ 现状（**2026-10-01 19:4x**）：`r86 ~ r100`（`d7e2151`）、**`r101`（`9f252e5`）**、
   **`r102~r105`（`87e2caa`）**、**`r106` 六条（`4d081ba`）**、**Codex 右栏调研（`f13b3bf`）**、
   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` 十二拍 🚫 未提交**（工作区 ` M pages/conversation.html`）。
   ★ **r108 尚在未提交期 ⇒ 可就地返工**：若还要改**会话详情页 / 右栏**，**直接改 `mg-work/r108/`**
   （改序 = `part108/_mods.html` → `ev/splice108.py` → `apply108.py`；⚠ `apply108.py` 由 `ev/make108.py` 生成、**禁手改**）。
   **不要**再把改动落回 `apply107.py` —— 它已是交付态（`e9c9498`）。
   ⚠ 若 r108 已交付后再改，则新建 `mg-work/r109/`（照抄六代 `GENS`、扩成七代；nav 脚本仍未改则可继续沿用 `NAV_TAG='r106'`）。
   若针对**设置页 / 字号机制 / 其它页**，回到 `apply88.py` / `apply88b-fontsize.py`。
   ⚠ **r105 ① 的产物落在 8 个「独立页」上**（各 +714）⇒ 复跑补丁时这 8 页会**同样被扫到**；改动只在 `nav_patch` 一处，
   不要为它们单开补丁（`invert_if_absent` 保证第二遍一字不动、**只保位置**）。
   ⚠ **nav 块 id 换代会让 10 页全变 ` M`**（r102 → r106 等长换名）⇒ 别把「10 页都 M」误判成「脚本改坏了别的页」；
   判据：**先把工作区 `\r\n` 归一成 `\n` 再比长度**（除目标页外应逐页 +0）。
3. 收尾四件套：`check-syntax.py` → `verify-design.py ./pages`（**必须传目录**）→ 与上一轮读数**逐条 diff** → 清理 → 覆盖更新本卡 + `mg-work/rNN/acceptance.md`。
4. 🚫 **默认不 commit / 不 push**：干完只汇报改动清单。

---

## 八、回滚与取证

```bash
# ★ r108 回滚（本代 · 只改了一页 ⇒ 一行即退（推荐））
git checkout -- pages/conversation.html
# ★ r106 回滚（首选：脚本自带 --revert）
python mg-work/r106/apply106.py --revert   # 摘 r106-conv-css/js + 10 页 nav 块 id 由 r106-* 回 r102-*（= r105 交付态）
# 或按文件回滚（文件名必须与原页面同名，otherwise 外壳按名查路由表会落回 base 壳）
cp mg-work/r106/before/conversation-r106.html pages/conversation.html   # → 865582 字节（CRLF，r105 交付态）
cp mg-work/r106/before/base-r106.html         pages/base.html
git checkout -- pages/{automation,avatar,dev,kanban,req-kanban,settings,skills,task-detail}.html  # 这 8 页只换了 nav 块 id
# ★ r93 回滚（首选：脚本自带）
python mg-work/r93/apply93.py --revert     # ④：删 pages/conversation.html + 摘 base 的 r93-nav-js + 9 页 ROUTE 各 −1 条（base 回到「需求 2 后」= 608256）
# 或按文件回滚（④ 前的快照，文件名必须与原页面同名）
cp mg-work/r93/before/base-r93c.html      pages/base.html        # base → ④ 前（608256）
cp mg-work/r93/before/settings-r93c.html  pages/settings.html    # 其余 8 页 → ④ 前（各少 1 条 ROUTE）；同型还有 avatar/dev/kanban/req-kanban/skills/automation/task-detail 的 *-r93c.html
rm -f pages/conversation.html                                     # 摘掉 ④ 新建页
# 再回到 r93 需求 2 之前
cp mg-work/r93/before/base-r93pre.html    pages/base.html        # base → r92/r93① 态（471920）
cp mg-work/r93/before/base.html           pages/base.html        # base → r92 收尾态（含 r87-ui-css 块 r92 态）
# ★ r102 ~ r105 回滚（本批 = r102 十一条 + r103 六条 + r104 四条 + r105 三条，已提交 87e2caa —— 回滚属应急，须自重）
python mg-work/r102/apply102.py --revert   # conversation → r101 交付态；8 页摘 nav 块；base 摘 nav id 换名（长度相同）
cp mg-work/r102/before/conversation-r102.html pages/conversation.html   # conversation → r102 前（= r101 交付态 721864）
# r92 回滚
cp mg-work/r92/before/<page>.html pages/<page>.html        # base/settings/avatar/skills/automation
# r88 系回滚（设置页 → r87 态）
cp mg-work/r88/before/settings.html pages/settings.html
# 其余 8 页的 r88 增量（仅 r87-ui-css 块内高度跟随）→ 用 r87 脚本收敛回 r87 态
python mg-work/r87/apply87b-fontsize.py
# ⚠ 若只想回滚 r93 需求 1（不动需求 2/④）：把 apply88b-fontsize.py 里的 LEADING_DERIVE 与 :not([class*="leading-"]) 撤掉后重跑
# r86 / r85 / r84 / r82 回滚
cp mg-work/r86/settings.before.html pages/settings.html
cp mg-work/r85/settings.before.html pages/settings.html
cp mg-work/r84/avatar.before.html   pages/avatar.html
cp mg-work/r82/before/<page>.html   pages/<page>.html
```

| 目录 | 关键内容 |
|---|---|
| `mg-work/r102/apply102.py` | ★ **r102 十一条 + r103 六条 + r104 四条 + r105 三条**全量（`GENS` 三代逐代摘除：r93 / r101 / r102；`HDR_ID` 保持 `r101-hdr-css`；含 `--revert` / `--dry`）；r105 ③ 从 `part105/` 读四件、CSS 进 `r102-conv-css`、JS 进 `r102-conv-js`、HTML 作静态片段，**并守卫四件里不得出现 `<script`/`<style`** |
| `mg-work/r102/part105/` | ★ r105 ③ 三件套 + 本页控制器：`browse.css`(15937) / `browse.html`(31688) / `browse.js`(47410，只用前半) / `ctrl-conv.js`(15465) |
| `mg-work/r102/acceptance.md` | ★ 六节 r102 + r103 段 + r104 段 + **r105 段**（39524 字节） |
| `mg-work/r93/apply93.py` | ★ 需求 2 + ④ 全量（25 块 + composer + 44 内联 SVG；**④**：独立页 `conversation.html` 由 base 净底重建 + 9 页 `ROUTE` 各 +1 + base 的 `r93-nav-js` + 下拉翻向 + `--revert`）；需求 1 在 `r88/apply88b-fontsize.py` |
| `mg-work/r93/acceptance.md` | ★ r93 验收档案（需求 1 根因/修法/实测；需求 2 三点拍板/变体叠加/字号体系表/逐块几何核对/结构级修正/暗色；**⑥ r93 ④：侦察结论 / 落地方式 / 四查 / 回滚**；改动文件；遗留） |
| `mg-work/r93/before/` | **r93 前置基线 10 页** + **9 个 `*-r93c.html`（④ 前快照）** + `base-r93pre.html` |
| `mg-work/r93/ev/` | `p93-dom/open/geo/geo2/click/lh`（需求 2 探针）/ **`p94-dom.js` `p94-outer2.js` `p94-conv.js`**（④ 侦察）/ `vd-r93.txt` `vd-r93c-base.txt`(75) `vd-r93c.txt`(76) `vd-r93d.txt`(复核) `rerun-④.log` / `base04/` |
| `mg-work/r93/raw/` | ★ 设计稿导出（`design-1393-18748-s1.png` `design-rgb.png` `spec.json` `sel-1393-18748.json` `asset/`）+ 8 个量测脚本（`parse-spec` `flatten-spec` `extract-text` `scan-type` `scan-lines` `measure-pad` `list-icons`）+ 取证裁剪图（`q-*.png` `crop-band*` `d9-s2..s9`）+ `v2-*.png` 实机分段截图 |
| `mg-work/r92/apply92.py` | ① 五页顶栏图 + ④ base 权限红；含可复用的 `replace_once` / `inject_tail`（`rfind('</body>')` 版） |
| `mg-work/r92/acceptance.md` | r92 验收档案（四条 / 素材实测 / 改前改后表 / 5 态表 / diff / 四查 / 待拍板） |
| `mg-work/r92/before/` `ev/` `raw/` | r92 基线 5 页 / 21 个探针与脚本 / 汇报三图 |
| `mg-work/r88/apply88.py` `apply88b-fontsize.py` | 设置页全量（r88~r93 需求 1 六代标记 + `PRIOR` + select 判空）+ **全局字号机制层** |
| `mg-work/r88/ev/` `raw/` | r88~r91 的 50+ 探针与截图；`diffgrp.py`（逐行分组 diff）通用 |
| `mg-work/r85/raw/design_1389-18725.png` | 设置页内容设计稿（2x / 1680×1838 / RGBA） |

⚠ `mg-work/r80/raw/` 里的设计素材（`svg/`）**别删**，是取不到数时的唯一退路。
⚠ `assets/icons/*.svg` 是仓内 DS 图标库；`assets/images/` 是画面素材。
⚠ 页面 bundle 里**早已内联 DS 全套组件 CSS** ⇒ **新增控件前先 grep 组件类名**。

---

## 九、环境速记（Windows，逐条都是踩过的）

- 预览一律 **`file://` 直开**（内置预览面板不带 hash ⇒ 渲染出错误的壳）；改完带 `?v=<ts>` 防缓存。
- ⚠ `file://` 下「改前基线」**文件名必须与原页面同名**（否则外壳按名查路由表落回 base 壳）—— `mg-work/rNN/before/*.html` 已按此命名。
- ⚠ **同一时刻只能有一个 agent-browser 链路**（共用标签页，并发必串味：症状「元素不存在 / url=blank / probe 缺失」）。
  整条链路（`set viewport` → `open` → `wait` → `eval/screenshot`）**要在一次 bash 调用里跑完**；长脚本 `run_in_background`。
- ⚠ ★ **鼠标"按住"跨 bash 调用 / `batch` / 长链会 SIGTERM 掉 daemon** ⇒ 拖拽用「单次 `eval` 内合成 PointerEvent 序列」。
- ✅ `screenshot <选择器> <路径>` = **元素截图**（位置参数；`--selector` 不认；`""` = 全页）。**`--full-page` 会静默失败，别用**。
- ⚠ **元素截图超出视口部分渲染成空白** ⇒ 先 `set viewport 1440 900` 并 `eval window.innerHeight` 核对。
- ⚠ **元素截图内取色 = 元素内相对坐标**（先减容器 rect）；**截浮层要全页截图再 Pillow 裁**（元素截图会裁到元素边界）。
- ⚠ **程序化 `el.click()` 的 `detail === 0` 会被当键盘触发**（按 `detail` 分流焦点的逻辑会因此飘出焦点光圈）⇒ 取证一律用真鼠标 `agent-browser click <sel>`。
- ⚠ `agent-browser eval` 返回**双层 JSON 字符串**（`json.loads` 两次）；**每次量测前必须重新 `open`**。
- ⚠ `eval "$(cat probe.js)"` **路径写错会静默返回 null** —— 链路照跑却几何全 0，**先查脚本文件在不在**。
- ⚠ **`getComputedStyle(el)['--custom-prop']` 恒为 `undefined`** ⇒ 用 `getPropertyValue('--x')`。
- ⚠ **沙箱 heredoc 会吞反斜杠** ⇒ 复杂正则/脚本一律**用 Write 工具落文件再跑**（本代又踩）。
- ⚠ Python 里 `/tmp` **不存在**（Windows）⇒ 临时文件写仓内或 `mg-work/rNN/ev/`。
- ⚠ **超长链式 bash 命令会报 `sandbox-center cmd decisionRecord missing actual resource subject`** ⇒ 拆成单条命令。
- ⚠ **大文件上 `difflib.SequenceMatcher` 会跑到 SIGTERM**（500KB 单行 bundle）⇒ 改用「公共前缀/后缀」或「按注入块 id 摘掉」定位窗口。
- 禁整文件 Read `pages/*.html`（单行 bundle 600+ KB）→ 用 Python 只打印目标片段。
- ⚠ 本机 `grep` 查中文一律返回空 → 中文用 Python 读（`grep` 只用于纯 ASCII 锚点）。
- ⚠ **`pages/*.html` 是 CRLF**：`wc -c` 报字节数、Python 文本模式读转 LF ⇒ 字符数与字节数差异巨大（本轮 base.html 字节 629434 / 字符 605980，**勿混用**）。
- 收尾跑 `check-syntax.py` / `verify-design.py` 会**污染工作区**（`mg-work/kanban/r13/chk/*.js`、`pages/gaps.log`）
  ⇒ 跑完必须 `git checkout -- pages/gaps.log && git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`。
  ⚠ `chk/*.js` 是**被跟踪的文件**，别 `rm -f` 一把梭。
  ⚠ `verify-design.py` 在**仓库根**（不在 `mg-work/`），且**必须传目录** `./pages`。
- **推 GitHub**（三步）：
  ① `env | grep -i proxy` **现查** —— 注入代理端口每轮会变（实测 53395 / 62399），对 `github.com:443` 稳定 502 ⇒ 先清掉 `env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY`；
  ② 出口 `http://127.0.0.1:7890`；③ 认证：PAT 在 `~/.git-credentials`（`icacls` 收紧过），推送带 **`-c credential.helper=store`**：

  ```bash
  env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY \
    git -c credential.helper=store \
        -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 \
        -c http.version=HTTP/1.1 push origin main
  ```

  判据：出现 `main -> main`。⚠ 认证缺失时报 `could not read Username … terminal prompts disabled`（非交互不弹窗）—— **别误判成网络问题**。
- agent-browser CLI 绝对路径：`C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js`
  （用 `C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe` 跑；**不在 PATH**）。
- ★ **容器宽度：先分清「要流式」还是「要保内容盒」**（★ r95 定论，取代 r94 旧做法）
  - **要流式（首选）**：子块写 `width:100%`、要留左缩进就 `calc(100% - 18px)`，容器 padding 只留纵向 ⇒ **右侧自动撑满**；
  - （旧·r94）子元素固定像素宽时用 `box-sizing:border-box` + 左右对称 padding 把「内容盒」保回原宽 ——
    ⚠ 这只在容器宽**恰等于设计稿**时才对，**容器一变宽右侧就留白**（r95 用户就是为此提的需求）。
  - ⚠ **`overflow` 容器的滚动条会占宽** ⇒ 同一页里「有滚动条的列」与「无滚动条的列」各自 `margin:auto` 居中会
    **差半个滚动条宽**（r95 实测 5px ⇒ 三组元素三条右边界 1265/1270/1280 打架）
    ⇒ 用 **`scrollbar-gutter: stable both-edges`**（两侧各让等量 gutter，内容恒同轴）。
  - 取证口径：**以不会被改动的锚元素**（本页 = composer 外壳）右边界为基准，逐块算 Δ ⇒ **全块 Δ=0 才算对齐**（`ev/p95b.js`）。
- ⚠ **容器里的「同类卡片」要分清是不是「容器」**：本页 `.r93-bub`（728 气泡，右对齐）与 `.r93-agent`
  （4 张按内容宽左对齐）**不属于**「右侧要撑满」的容器 ⇒ r95 **刻意未动**（它们是设计稿固定排版）。
  反之：把「设计稿里的**假滚动条**」（绝对定位色条 `.r93-vsb`）换成真 `overflow-y:auto` 时，⚠ **只给纯文本卡加**
  （`.r93-card--ctx`）；`.r93-card` 基类**刻意不写 overflow**（卡内路径 popover 要溢出卡片）。
- ⚠ **门禁会把注释里的 CSS 关键词也算进去**（r94 实测：新注释里写 `radial-gradient` ⇒ `verify-design` 的「渐变处数」+1，
  以致与基线 diff 非零）⇒ **新注释别写** `gradient` 这类被扫描的字面（同「断言 token 不进注释」）。
- ★ **把外壳真实组件（React 渲染）钉在容器底部复用时，它的下拉/弹层要「翻向」**（r93 ④）：
  真 select 默认**向下**弹（`top:calc(100% + 4px)`），容器若是 `overflow:hidden` 的 `main` 底部 ⇒ 弹层被裁
  （实测「默认权限」popup y 871..997 而 main 底 892，只剩 21px）⇒ 页面级适配写
  `top:auto!important; bottom:calc(100% + 4px)!important`（`.giencoder-select-popup` + `[aria-label='权限选择']`）；
  ⚠ `calc(100% + 4px)` **含 `%`** ⇒ 不会被 `apply88b` 的 `unscale()` 正则改坏（它只认 `calc(<数字>px * var(--ui-fs-ratio))` 或裸 `Npx`）。
- MasterGo：MCP 在 **20678**；**截图 HTTP 接口在 30678**（详见 PLAYBOOK P7）。设计稿取数 scale 用 **2.0**。
  ⚠ **导出 PNG 是 RGBA，未绘制处 `alpha=0`** ⇒ 取色前先 `alpha_composite` 白底（否则 `convert('RGB')` 变纯黑，误判成"标签条盖住内容"）。
  ⚠ ★ **设计稿导出图里「状态变体」是叠放的**（r93 实测每块 +34px）；`ui-component` **不带 font-size**；私有区图标字符实机**无字形**。
- ★★ **设计稿取数有两个源，别只会用 PNG**（r96 ⑤ 的重大提速）：
  1. **`raw/design-1393-18748.html`（设计稿导出的带样式 HTML）＝ 权威源**：`data-node-id` / `data-name` /
     `style="width;height;left;top;gap;color;font-size;line-height"` 全是**精确值**，还有 `props='{"尺寸":"14"}'` 这类
     DS 实例参数 ⇒ **先 grep 它**（`S.find('Token 速率')` / 按 `data-name` 搜），比逐像素扫图快一个数量级。
  2. **`raw/design-rgb.png`（1x 整页导出）＝ 校验源**：只用来①**验色值**（该图色值准确，r96 实测图中图标 = (107,107,107)
     与该 HTML 里其它 `#6B6B6B` 逐字一致）②**反推形状**（`ui-component` 这种**没导出独立 svg** 的实例只能靠点阵还原）
     ③量**渲染后的实际位置**（导出时缺 `left/top` 的元素）。
  ⚠ 两者**必须交叉验证**：只信 HTML 会漏掉「导出缺 left/top」的元素；只信 PNG 会把「相邻元素宽度」当成「线宽」
  （r96 ⑤ 就是把「容器 246 的 56 宽」当成了分隔线宽度 ⇒ 画出 56×1 横线）。
- ★ **改「工具类的默认色」前先枚举它的全部使用点**（r96 ③）：`.r93-t14` 在 14 处被用、其中 9 处由**别的类**
  （`.r93-ft` / `.r93-nt` / `.r93-dname` / `.r93-c1` / `.r93-fc` / `.r93-sumrow` …）给色 ⇒ 改默认值只影响「裸用」的那几处。
  做法：跑一个探针**按 `computed color + className` 分组计数**（`ev/p96a.js` 的 `t14dist`）⇒ 一眼看出改动波及面。
  ⚠ 同特异性 (0,1,0) 的规则**后定义者胜** ⇒ 新默认值要写在所有覆盖类**之前**（或直接提高特异性，如 `.r93-t14.r93-c2`）。
- ⚠ **给基类加 `font-size` 的波及面 = 「无类名文本」**（r96 ②）：`.r93-card { font-size:13px }` 后，
  卡内自带 `--font-size-*` 的（`.r93-pre` 12px、`.r93-t12*`、`.r93-t14*`）**统统不受影响** ⇒ 只有裸文本会变。
- ★★ **`*` 的通配符不贡献特异性**（r97 ①）：`.r93-card *` 看着像 (0,1,1)，其实是 **(0,1,0)**，与
  `.r93-pre` 同级 ⇒ **被写在它后面的同级规则反超**（实测：37 处变 13px，唯独 5 处 `.r93-pre` 仍 12px）。
  想「后代通配 + 压过所有单类」就把类名写两遍：**`.r93-card.r93-card, .r93-card.r93-card *`** = (0,2,0)。
  （不用 `!important`；也不要靠「把它挪到块末尾」—— 那正是「后写者胜」的脆弱写法。）
- ★★ **`width: N%` 的基数 = 父盒**（r97 ③）：同一页里想让「内容列 / 底部列 / 复用来的真组件」等宽，
  只要它们**父盒不同宽**（滚动内容盒 vs pane vs 带 `px-*` 的 hero 子盒），`50%` 算出来就**不是同一个数**
  —— 1440 下被 `min-width` 兜住看不出来，**视口一宽就露馅**（2560 实测差 24px，用户看到的是「两端各短一截」）。
  排查口径：在**两个视口**（如 1440 + 2560）各测一遍 `getBoundingClientRect()`，看右边界是否全等。
  修法二选一：① 把父盒的基准差补回去（`calc(50% + Δ)`；Δ 依赖滚动条宽时要**先把滚动条宽显式钉死**）
  ② 清掉父盒的横向内距（`padding-left/right: 0`）让父盒 = 目标基准。**优先 ②**（不引入魔数）。

---

## 十、★ 页面路由表 / 新开一页的范式（r93 ④ 查明）

**`pages/` 下每一个页面都是完全自包含的独立 html**（顶栏 + aside + 外壳在**每份文件里各有一份**）——
**没有共享布局文件、没有真实的客户端路由**。页间跳转靠每页内嵌 `<!-- SHELL-NAV-FIX v5 -->` 脚本里的 `ROUTE` 表 + `hashchange`：

```js
var ROUTE = { '/': 'base.html', '/base': 'base.html', '/dev': 'dev.html', '/kanban': 'kanban.html',
              '/req-kanban': 'req-kanban.html', '/task-detail': 'task-detail.html', '/avatar': 'avatar.html',
              '/automation': 'automation.html', '/skills': 'skills.html', '/settings': 'settings.html',
              '/conversation': 'conversation.html' /* ← r93 ④ 新增，10 页各一份、逐字相同 */ };
```
> 外壳自己的 `navigate()` 在 **`file://`** 下才真跳页；**`http://`** 下只改 hash（⇒ 预览用 `file://` 直开）。

- **顶栏「工作台切换」页签**由另一段 `<!-- SHELL-TABS-FIX v4 -->` 管（`FILE={base,dev}`、`DEV_PAGES={dev,kanban,req-kanban,task-detail}`）；「某页属哪个工作台」**grep 每页 bundle 里的 `DEV_PAGES`**，别凭页面名推断。
- **新增一页的范式**（r93 ④ 即是）：
  1. **由某页净底重建**（`base.html` 摘掉本代注入块后的净底 = 新页的唯一来源），**不要手工复制**；
  2. 换 **根级判据**：`<html lang="zh-CN" data-rNN-page="<slug>">` + 改 `<title>`；
  3. 页面级 CSS 全部挂 `html[data-rNN-page='<slug>'] …`；
  4. 在**全部页**（含新页自身）的 `ROUTE` 表尾插一条 `'/slug': 'slug.html'`（幂等 `replace_once` + counted 断言）；
  5. 若「从 X 页跳过去」是交互需求 ⇒ 在 **X 页**注入一个小 nav 脚本（捕获阶段拦目标 widget ⇒ `location.href`）。
- ⚠ **`file://` 下 localStorage 不跨页面共享**（独立页天然拿不到「源页的选中状态」）⇒ 需要传参就用 hash。
- ⚠ `--revert` 必须把「新页文件 + 源页 nav 脚本 + N 页 ROUTE 条目」**一起**退掉（`apply93.py --revert` 即如此）。
