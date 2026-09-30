# -*- coding: utf-8 -*-
"""把 r105 验收段追加进 mg-work/r102/acceptance.md（幂等：已存在 r105 段则不重复追加）。"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACC = os.path.normpath(os.path.join(HERE, '..', 'acceptance.md'))

MARK = '# r105 三条'

SEC = u'''

---

# r105 三条（2026-09-30 深夜 · 会话详情页 + 8 个独立页）—— **就地返工**

> **体位**：r102 / r103 / r104 **均未提交** ⇒ 本代**就地返工**，仍改 `mg-work/r102/apply102.py`
> （现 **163605 字符 / 220815 字节**），注入块 id **不变**（`r102-conv-css` / `r102-conv-js` / `r102-nav-js`），
> **不另起代数**、不新建 `apply105.py`。静态片段走**新增** `mg-work/r102/part105/` 四件
> （`browse.css` / `browse.html` / `browse.js` / `ctrl-conv.js`），在 `inject_tail` 里拼进同一次注入。
>
> **产物**：`pages/conversation.html` **691648 → 793028**（② **+2173**、③ **+99207**）；
> `pages/base.html` **472150（+0，本轮未变）**；其余 **8 页各 +714**（同一块 `r102-nav-js`）。
> **四查**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax pages/*.html` **10/10 ALL_OK**
> （conversation `script=9 style=16`）｜`verify-design ./pages` 与基线 `vd-r101e.txt`
> **逐字节相同**（17148 字符 / md5 `84f552c5b5a6`）⇒ **零新增**｜1440 + 2560 + 暗色实测 + 截图目视 ✓。

## 一、三条逐条实测

| # | 邵先生原话 | 落点 | 实测读数 | 判定 |
|---|---|---|---|---|
| ① | 在任何其他独立页面点击会话任务**都要能跳转到 `conversation.html`** | 把 `base.html` 里已有的 `r102-nav-js` 扩到**其余 8 页**（`nav_patch` → `invert_if_absent`） | 真鼠标点击：`base` / `avatar` / `automation` / `skills` 均 **`file:///…/conversation.html`** ✓。**负例**：点 aside **分组标题**、点**「新会话」按钮** → 两例均**留在原页** ✓。`task-detail` 的壳 `aside` 实为 `display:none`（rect `[0,0,0,0]`，可见左栏是 `.td-left` 任务面板、**无会话列表**）⇒ **无对象，非缺陷**；`kanban`（筛选面板）/ `settings`（设置导航）aside **无会话项**；`dev` / `req-kanban` **无 `<aside>`** —— 5 页均**无对象**。各页 nav 块**各 1 块**，`conversation.html` **0 块**（自身不需要） | ✓ |
| ② | `"r93-seg giencoder-radio-group giencoder-radio-group-button"` 切换要有**滑动动效** | 改用 **DS 官方滑块** `.giencoder-radio-button-slider`（DS `components.css` 本来就带 `transition: transform .28s, width .28s`，且**已在页面内联**）；HTML 加滑块 span、CSS 让滑块承担白底/描边、JS `r93SegMove()` 写行内几何 | **逐帧**（rAF 采样）：`0 → 38.79(82ms) → 49.58(148ms) → 51.75(215ms) → 51.999(282ms) → 52(348ms 稳定)`，**宽恒 52**；反向点回「对话」**镜像回 0** ✓。根因：当年页面把 `.giencoder-radio-button-checked` **自绘**成白底 + 描边 ⇒ **位移没有载体**、只能硬切 | ✓ |
| ③ | 「`r93-bar`」右侧按钮**替换为「全屏」和「打开侧栏」**，即数字分身的 `td-right-acts` | ①按钮本体逐字对齐 `.td-right-acts`（`giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon` + `.r93-baract`），原单枚 `.r93-morebtn`（⋯，**本来无任何行为**）**整枚退役**；②全屏 = `<html data-r93-full='1'>` ⇒ 左导航收拢 0、对话区吃满；③「打开侧栏」= 数字分身 **AV-BROWSE-SLOT v1** 三件套**整块移植** | **③a**：rect `[1359,57,64,28]`（两枚 28×28 + gap 8，右缘 1431 = bar 右缘 − 8）｜`border-color rgba(0,0,0,0)`、`border-radius 8px`（随 DS）、hover `rgb(247,247,247)`、图标 **14px**。**③b** 1440：`aside 256 → 0`、`main 1164 → 1420`、`icoMax none / icoMin flex`、`aria-label 全屏 → 退出全屏`；2560 **同构** ✓。**③c**：点开 ⇒ `aside 0 / main 779 / split [791,48,9,844] display block / pane 641`；右键菜单 rect `[1000,400,182,227]`、**12 项**、`data-td-ctx-open`；文件树 **28 行**、点目录 `is-closed` + **27 行 `is-hidden`**；拖分栏条 **641 → 701px** 并落盘 `{"panelW":701}`；关闭按钮**完全复原**。**③d** 暗色（源页没有，本模块**首次落到有暗色分支的页面**）：`panelBorder rgb(78,78,78)`、`codeKey rgb(86,156,214)`、`panelBg rgb(23,23,26)`；**浅色档逐字节不变** | ✓ |

## 二、三条的关键实现

### ① 扩展而非重写
同一块 `r102-nav-js`（**捕获阶段**委托 `document.addEventListener('click', …, true)` —— aside 是外壳 React 渲染的、拿不到它的 onClick，先例 r86/r88）。
`nav_patch` 统一走 `invert_if_absent`：**内容一致 ⇒ 一字不动、只保位置**；不同 ⇒ 原地替换；不存在 ⇒ 追加。
这正是修掉「两块都往 `</body>` 前追加、每遍报『改了』」那个幂等瑕疵的同一把刀。

### ② 三处手势 + 四处重定位
* **首帧不播动画**：`.r93-seg` 带 `data-r93-seg-init="0"` ⇒ 该态下 `transition: none`（否则滑块会从 **0 宽「长」出来**）；JS **两帧后**摘掉该属性放开过渡。
* **四处重定位**：页签 `click` / `document.fonts.ready` / `window.resize` / **1200ms 兜底**（字体晚到 ⇒ `offsetWidth` 会变）。
* 滑块几何 = `width: offsetWidth`、`translateX: offsetLeft − 1`；`checked` 改 `background: transparent; border: 0`（**只留文字色与字重**）。

### ③ 三层结构
1. **按钮**：⚠ `border-color: transparent` **必须写**（avatar 的 `.td-round-btn` 就是靠它去掉 DS 默认描边的）；**圆角不覆盖**，随 DS **8px**；图标三枚 `fsmax` / `fsmin` / `panel` **逐字取自 avatar**（24 网格 / stroke-width 2）。两枚图标**共用一枚按钮**，靠 `html[data-r93-full='1'] .r93-baracts .r93-ico-max/-min` 切显隐（选择器**带前缀**是为胜过 `.r93-iblk { display: inline-flex }`，避免同特异性靠顺序取胜）。
2. **全屏**：做法与浏览态**完全同款** —— `width: 0 !important; min-width: 0 !important; padding-*: 0 !important; opacity: 0; pointer-events: none`（外壳给 aside 的宽度是 React **内联** style ⇒ 必须 `!important`；它自带 `overflow: hidden`）。
3. **预览栏**：挂载 = `hostRow.insertBefore(splitMain, hostMain.nextSibling)` + `insertBefore(slot, splitMain.nextSibling)`（`hostRow` = `div:has(> main)`）。宽度变量 `--av-browse-w`（**默认 641**，`MIN_PANEL 561`、`MAIN_MIN 380`）；记忆 key 换成 **`giencoder:r105-browse:v1`**（与数字分身**分开**）。
   ▲ **Esc 裁决链**（本轮新增第 ③ 级）：右键菜单 → 预览栏 → **全屏**，每级 `stopImmediatePropagation`。
   ▲ 第 ③ 级**不直接改 `<html data-r93-full>`** —— 状态由 r102 主脚本持有（它还要翻按钮 `aria-pressed`/`title`/`aria-label` 并派发 `resize`）；控制器**比主脚本更晚注册**，直接调函数会**反序** ⇒ 走自定义事件 **`r93:fullscreen`**（主脚本 `document.addEventListener('r93:fullscreen', …)`）。

### ③-d 补的「暗色档」
`browse.css` 有 **7 个字面 hex**，全部是**自定义属性定义**。源页 avatar / task-detail **都没有**本模块暗色分支，但本模块**第一次落到有暗色分支的页面**（conversation r93 一族全量做了暗色）⇒ 按 PLAYBOOK 规则 5 **必须补**。
不补的实测后果：面板外缘线 `#ECEEF2` 成**亮框**、代码主色 `#0451A5` 对 `#17171a` 对比度 ≈ **2.0**（远低于 4.5）、激活行 `#ECF2FF` 成**整块白**。
修法只覆盖那 **7 个自定义属性**、**不动几何**（源件保持**逐字不动** ⇒ 同源校验仍成立）：`--td-panel-line: rgb(var(--gray-3))`；`--td-code-key/str/num: #569CD6 / #CE9178 / #B5CEA8`（VSCode **Dark+** 同位置三色）；激活行 `rgba(var(--blue-7), .20) / rgba(var(--blue-7), .38)`；`--td-crumb-line: var(--color-border-1)`。

### 注入体位与守卫
CSS 进 `r102-conv-css`、JS 进 `r102-conv-js`、**HTML 作为同一次 `inject_tail` 的静态片段**（与 avatar 同体位：样式表之后、脚本之前）。
`apply102.py` 新增守卫：三件里出现 `<script` / `</script` / `<style` / `</style` **一律 `sys.exit`**（会打乱 `<script>` 计数断言 / 提前闭合标签）。

## 三、四查终态

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍双「已是目标态」（`conversation.html` sha 不变） |
| JS/CSS 语法 | `python mg-work/check-syntax.py pages/*.html` ⇒ **10/10 ALL_OK**（conversation `script=9 style=16`） |
| 设计回归 | `python verify-design.py ./pages` 与 `ev/vd-r101e.txt` **逐字节相同**（17148 字符 / md5 `84f552c5b5a6`）⇒ **零新增** |
| 死代码 | `r93-morebtn` 全仓 **3 处、全在注释**（活规则 0 条） |
| 终态 | `pages/conversation.html` **793028** / sha `e67474395502`；`pages/base.html` **472150（+0）** |

## 四、本轮探针与裁片（`mg-work/r102/`）

* **探针** `ev/`：`extract105.py`（抽取三件套并与 r69 存档比对）｜`p105a/b.sh`（骨架 / avatar 侧栏几何）｜`p105c/d.sh`（跳转实测 / 9 页 aside 普查）｜`p105e/f.js` + `p105f.sh`（按钮 / 侧栏 / 全屏**五态**）｜`p105g1.js` + `p105g.sh`（**滑块逐帧** + 按钮态）｜`p105h.sh`（2560 + 暗色）｜`p105i.sh`（**逐页跳转 + 负例**）｜`p105j.sh`（预览栏自身交互：菜单 / 树 / 拖拽 / 关闭）｜`vd-r105a.txt` / `vd-r105b.txt`（均与基线 **IDENTICAL**）｜`p105-tokens.log`（浅暗两档色阶读数）。
* **裁片** `raw/`：`x105-0-init.png` / `x105-0b-init.png` / `y105-btn.png` / `y105-btn2.png` / `x105-1-browse.png` / `x105-2-both.png` / `x105-3-fsonly.png` / `x105-4-ctx.png` / `y105-ctx.png` / `z2560-browse.png` / `z2560-browse-fs.png` / `z2560-dark-browse.png` / `z1440-dark-105.png` / `y105-avatar.png` / `y105-avatar-btn.png`。
* **新增源件** `part105/`：`browse.css` **15937**｜`browse.html` **31688**（静态片段，3 行：头/主体/尾）｜`browse.js` **47410**（**只用前半段** 31498，切分点 `\\n(function () {\\n  var KEY`）｜`ctrl-conv.js` **15465**（本页控制器，**按本页布局改写**）。

## 五、待邵先生拍板

**r105 三条本身均已落地**，下面 3 条是**顺手替他做的判断**，请确认要不要改口径：
1. **全屏 = 收拢左导航**（`aside → 0`、对话区吃满整行），与数字分身全屏「让 main 让位」**同语义** —— 若希望全屏时保留一条**可点回来的窄条**（如 0 → 12px 抓边），说一声即改。
2. **预览栏默认宽 641**（沿用数字分身），本页内容更宽 ⇒ 若希望本页另给一个默认值（如 720），可单独调。
3. **预览栏与「全屏」可同时开**（实测 `x105-2-both.png`：aside 0 + 预览栏在右侧）—— 若希望二者**互斥**（开全屏自动收预览栏），说一声即改。

r103 遗留 2 条（③ 药丸透明度 0.60、④ 摘行后 44px 空档）与 r102 遗留 5 条仍见上文。

**状态**：🚫 **未提交**（r102 十一条 + r103 六条 + r104 四条 + r105 三条 = **同一次交付**；等邵先生发话 commit / push）。
'''

with io.open(ACC, encoding='utf-8') as f:
    txt = f.read()

if MARK in txt:
    print('SKIP: r105 段已在文件中，不重复追加')
    sys.exit(0)

if not txt.endswith('\n'):
    txt += '\n'

with io.open(ACC, 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + SEC)

print('OK: 已追加 r105 段')
