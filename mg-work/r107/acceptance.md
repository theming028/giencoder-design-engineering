# r107 验收 · 会话详情页「侧栏模块标签化」（复刻 Codex 右栏）

> 需求（邵先生 2026-10-01 09:3x）：① `conversation.html` **就地扩右栏**；② 先**提交 r106 六条**；
> ③ 按建议顺序落地（`Review(diff)` → `Terminal` → `Browser` → 标签多开/拖拽 → `Side chat`），
> **前提 = 绝对不得改动其他不必涉及的模块、完全确保整体产品稳定性不被破坏、只做静态交互**。
>
> 调研依据 = `docs/codex-sidepanel-research.md` + `docs/codex-refs/`（12 张实机截图，已提交 `f13b3bf`）。

---

## 零、产物与口径（★ 三种口径勿混用）

| 项 | 读数 |
|---|---|
| 提交（前置） | r106 六条 → **`4d081ba`**；Codex 调研文档 → **`f13b3bf`** |
| 本代补丁 | **新建** `mg-work/r107/apply107.py`（由 `ev/make107.py` 从 `apply106.py` 做 **11 处精确替换**生成，每处命中数断言） |
| 资产 | `part107/{_head.html 5285 / _mods.html 18493 / browse.html 54400 / panel.css 24681 / panel.js 24222}`（`browse.html` 由 `ev/splice107.py` 拼出） |
| `pages/conversation.html` | **799231 → 866988 Unicode 字符（+67757）**；UTF-8 字节（LF 归一）870627 → **941565**；工作区字节（CRLF）**947490** |
| **其余 9 页** | **`base.html` + 8 个外壳页 —— 逐字节不变（`git status` 里只有 conversation.html 一个 ` M`）** |
| 幂等 | ✓ 连跑 **四遍**，第二 / 三 / 四遍双「已是目标态（无改动）」 |
| JS/CSS 语法 | `python mg-work/check-syntax.py pages/*.html` ⇒ **10/10 通过**（conversation `script=9 style=16`，与 r106 一致） |
| 设计回归 | `python verify-design.py ./pages` 与 `mg-work/r101/ev/vd-r101a.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增** |
| 代数核对 | conversation 的 `r107-conv-css` / `r107-conv-js` 各 **1**；`r106-*` / `r102-*` / `r101-*` / `r93-conv-*` **全 0**；**base 的 nav 块仍是 `r106-nav-js`（本代刻意不换名）** |

> ⚠ 工作区字节 − blob 字节 = 「行数」个字节 = `core.autocrlf=true` 的行尾差，**不是内容改动**。
> ⚠ 本页字符数**必须**先归一化行尾再比（`len(bytes)−CRLF数` 不是字符数，本页中文多会虚高约 6.8 万）。

---

## 一、★★ 本代最关键的体位：**nav 块沿用 r106 的名字** ⇒ 只改一页

`apply107.py` 的 `GENS` 扩成**五代**，但第五代的 nav id **刻意仍写 `r106-nav-js`**：

```python
GENS = (('r93',…), ('r101',…), ('r102',…),
        ('r106', 'r106-conv-css', 'r106-conv-js', 'r106-nav-js'),
        ('r107', 'r107-conv-css', 'r107-conv-js', 'r106-nav-js'))   # ← 沿用
NAV_TAG = 'r106'      # build_nav_js / 残留自检都用它
```

理由 = PLAYBOOK 硬规则「**跨代沿用的宿主标记不换名**」：本代根本没碰 nav 跳转脚本，
若照惯例换成 `r107-nav-js`，`base.html` + 8 个外壳页会**全体进 diff（虽然内容等长）**——
那就违背了邵先生本轮「不得改动其他不必涉及的模块」。

实测（`--dry` 与正式跑都打印）：
```
   base.html            已是目标态（无改动）
   conversation.html    799231 → 866988 (+67757)  应用
```
⇒ **`git status --porcelain` 只有 ` M pages/conversation.html` + `?? mg-work/r107/`**。

---

## 二、落地内容（三段式骨架 + 五模块）

### ① 标签栏（Codex 骨架第①段）

- `.td-browse-bar` 内改成 `[标签条] + [＋] + [│] + [⤢ 最大化][✕ 收起]`。
- 标签 = `[模块图标] 名称 ×`；`is-active` 高亮；hover / active 才显 `×`；
  **只剩一枚标签时不显示 `×`**（`.td-browse-tabs.is-single`，关掉就没侧栏了）。
- **`+` 紧跟最后一枚标签**：`.td-browse-tabs { flex: 0 1 auto }`（不 grow），
  剩余空间由 `.td-browse-acts { margin-left:auto }` 吃掉。
  实测（1440，四标签）：标签右缘 **1138**、「＋」左缘 **1142**。
- **多开 / 切换 / 关闭 / 拖拽重排**：
  - 拖拽 = `pointerdown` 起手，`pointermove` / `pointerup` **挂 window**（与站内其它拖拽同口径），
    位移 > 5px 才进拖动；按「各标签中线」求插入位，直接 `insertBefore` 重排 DOM。
    实测：`[files,review,terminal]` 把末枚拖到最前 ⇒ **`[terminal,files,review]`** ✓。
  - 关闭后激活「原索引处的邻居」；实测 `[files,review,terminal,browser*]` 关 browser ⇒ **terminal 激活** ✓。
- **`+` 菜单**（复刻 Codex 右上角那枚面板菜单）= 五选一：审查 `⇧⌘G` / 终端 ``⌃` `` / 浏览器 `⌘T` / 文件 `⌘P` / 侧边聊天 `⌃⌥S`。
  实测 `items = ["review","terminal","browser","files","side"]` ✓。
- **`⤢` 最大化 / 还原**：自算 `maxPanelW() = freeW() − MAIN_MIN(380)`，写宿主 `--av-browse-w`；
  还原时读回 `localStorage['giencoder:r105-browse:v1'].panelW`（不破坏用户拖过的宽度）。
  实测 1440：641 → **1040**（main 779 → 380）；2560：641 → **2160**（main 1899 → 380）；还原回 641 ✓。
  ⚠ ctrl-conv 的 resize 处理走**单层 rAF** ⇒ 本处**退两层 rAF** 再落定最大化宽，保证不被它覆盖。

### ② 模块工具条 + ③ 正文

| 模块 | 工具条（②） | 正文（③） | 静态交互（实测） |
|---|---|---|---|
| **文件**（原有） | —（沿用 crumb 右侧两钮） | **原 Files 正文逐字未改** | 目录开合 / 选文件 / 隐藏文件目录 全部回归通过 ✓ |
| **审查** | `上一轮 ⌄  +566 −228  4 个文件  ⋯  [⑀ 提交 ⌄]` | 3 张 diff 卡（两列行号 + 加绿/删红块 + `⋯ 折叠 46 行未改动` 按钮 + 行内评论气泡）+ 提交模态 | 卡片开合 / `⋯` 显示选项（统一 ⇄ 并排）/ 折叠全部 / 提交模态 全通 ✓ |
| **终端** | — | 提示符行 + vite 输出 + 光标行 | 真按键回声：`ls` ⇒ 打印目录列表；`pwd` / `npm run dev` / `clear` / 未知命令 各有分支 ✓ |
| **浏览器** | URL 行（后退/前进/刷新 + URL 药丸 + **标注**药丸） | 静态 mock 页面（hero + 3 卡片 + 页脚）+ 元素评论气泡 + 底部 `标注中…` 条 | 开标注 ⇒ 元素虚线描边 + 点击出评论气泡（`评论元素 卡片`）✓；Esc / 完成 退出 ✓ |
| **侧边聊天** | `[侧边聊天] 不打断主对话` | 引用块 + 用户气泡 + AI 气泡 + 底部输入框 | **在 main 里划词 ⇒ 浮条**「在侧边聊天中提问 / 添加到对话」；点第一项 ⇒ 开标签 + 引用原文 + 聚焦输入框；发消息 ⇒ 回一条「这条只在这个分叉里讨论」✓ |

### ④ 划词浮条（Codex 的 side chat 入口）

- 监听 `mouseup`（文档级），只在**选中文本落在 `main` 内**、长度 1–300 且**可见**
  （`getBoundingClientRect()` 有面积）时弹出；滚动 / 再按鼠标 / resize / Esc 收起。
- 定位：选区上沿 − 浮条高 − 8，出屏则翻到选区下方；左右钳在视口内。
- 实测：选中 `.r93-bub`（127 字）⇒ 浮条出现在 `left:290px top:79px` ✓。

### ⑤ Esc 层级（★ 关键）

`panel.js` 的 Esc 挂在 **`window` 捕获段**，比 ctrl-conv 的 **`document` 捕获段**更早 ⇒
能「先关菜单、再关侧栏」，不会一次 Esc 关两层。实测：
一次 Esc ⇒ `menuOpen:false, panelOn:true`；再一次 ⇒ `panelOn:false` ✓。

---

## 三、期间查出并修掉的两个真 bug（都是「肉眼看不见、量出来才现形」）

### bug 1 ★ 新模块 section 的类名与内部件**撞车**

初版写 `<section class="td-mod td-term">`，而内部正文是 `<div class="td-term">`。
后果：`document.querySelector('.td-term')` 取到的是**外层 section**（`tabIndex=-1`、`tabindex` 属性为 null），
所以「点终端 → 拿焦点 → 打字」看起来像没反应；且 `.td-term{...}` 那一整套样式**同时压在 section 上**
（section 与内层各吃一份 `padding:12px 14px`）。

证据：`{ti:-1, attr:null, html:'<section class="td-mod td-term"…'}` + `.td-term` 匹配数 = **2**。
修法：section 改名 **`td-mod-term`**（其余两个 section 的 `td-rv` / `td-brw` 与内部件**不重名**，已核对无恙）。

### bug 2 ★★ 绝对定位子件的**包含块**跑到视口上

`.td-commit { position: absolute; inset: 0 }`，而**源件 `.td-browse` 没写 `position`** ⇒
包含块落到视口：遮罩铺满整站、卡片居中在屏幕，而不是在侧栏里。

证据：`modalRect = [418,211,250,246]`（视口居中）→ 修后 `[792,49,639,842]` ＝ `panelRect [791,48,641,844]` ✓。
修法：`panel.css` 里给 `.td-browse` 补 **`position: relative`**（`position` 不改 flex 项的布局尺寸）。

---

## 四、稳定性证明（邵先生的硬约束逐条对照）

| 约束 | 判据 | 读数 |
|---|---|---|
| 不得改动其他不必涉及的模块 | `git status --porcelain` | **只有 `pages/conversation.html`**（`base.html` + 8 个外壳页零改动） |
| 整体产品稳定性不被破坏 | `verify-design.py ./pages` 与上轮**逐字节相同** | md5 `3dbf654337559509110899e48bef1b1c` ⇒ **零新增设计回归** |
| 同上 | `check-syntax.py pages/*.html` | **10/10 通过**，conversation `script=9 style=16`（与 r106 同） |
| 原「文件」模块不许被碰 | 文件树回归探针 | `rows 28 / closed 6 / hidden 9`；折叠 `snake` ⇒ `visible 4`；点文件 ⇒ `is-active: package-lock.html`；隐藏/显示文件目录 ⇒ `is-no-tree` true/false ✓ |
| 只做静态交互 | 全模块操作均为前端本地行为 | 终端不发请求、审查不改真文件、浏览器不真跳转、侧边聊天只往 DOM 追加气泡 |
| 幂等 / 可自愈 | 连跑四遍补丁 | 第二遍起双「已是目标态」 |
| 暗色档 | `[giencoder-theme='dark']` 下取色 | 加行底 `rgb(18,60,25)`（green-1 暗）、标注条 `rgb(84,151,255)`（blue-6 暗）⇒ **纯 token，自动翻转**，无需另写暗色分支 |
| 字号杠杆 | 置 `--ui-fs:18` | 标签高 28→**36**、菜单字 13→**16.71**（= 13×18/14 ✓）；`barOverflow = 0`（44px 栏仍容得下） |
| 窄档 | 1280 视口 5 标签 | 标签条 `scrollWidth 444 == clientWidth 444`、`panel 溢出 0`、`bar 溢出 0` |

---

## 五、已知取舍（均为「替他做的判断」，可一行改）

1. **标签文案用中文**（文件 / 审查 / 终端 / 浏览器 / 侧边聊天）—— 与面板内既有中文（文件目录 / 收起侧栏）一致；
   要英文（Files / Review / Terminal / Browser / Side chat）改 `_head.html` 的 `td-mm-name` 即可。
2. **终端标签名 = 「终端」**（Codex 用 cwd 缩写）—— 想跟 Codex 就把标签文案改成 `giencoder-design-eng…`（CSS 已备 ellipsis）。
3. **只剩一枚标签时不给关**（`is-single` 隐藏 `×`）—— Codex 允许关到空（等于关面板）；本代取更稳的一档。
4. **`⤢` 的实现口径 = 「侧栏最大化（对话区压到 380）」**，不是窗级全屏 ——
   调研未能确认 Codex 的原义（见 `docs/codex-sidepanel-research.md` 第五节「未覆盖」）。
5. **diff 取「加绿 / 删红」**（GitHub 惯例）—— 与项目做金融视觉时的「涨红跌绿」冲突，此处按**代码语义**取色。
6. **`--ui-fs` 的理论上限**：标签高 = `28 × ratio`，44px 栏在 **ratio > 1.571（`--ui-fs` > 22）** 时会被标签顶满 ——
   站内字号档位实测 18 仍宽裕；若将来放开到 22 以上，此处要改成「栏高跟着 ratio 长」。
7. **`+` 菜单没有做「键盘导航 / 焦点圈定」**（只做了 Esc 与点外关闭）。

---

## 六、取证与裁片（`mg-work/r107/`）

```
apply107.py            本代补丁（含 --revert / --dry）
acceptance.md          本文件
part107/               _head.html（新头部）· _mods.html（四个新模块）· browse.html（组装件）
                       panel.css（新增样式 24681 字节）· panel.js（控制器 24222 字节）
ev/make107.py          由 apply106.py 生成 apply107.py（11 处替换 + 命中数断言）
ev/splice107.py        由 part105/browse.html 剪出 Files 正文 + 换头 + 追加新模块 → part107/browse.html
ev/probe107.sh         首轮链路（14 步）
ev/debug107.sh         诊断①（选区 / 显示选项 / 终端）
ev/debug107b.sh        诊断②（选区 → 侧边聊天 → 终端 → Esc 层级）
ev/final107.sh         收尾综合（文件回归 / 四模块 / 暗色 / 2560 / 最大化）
ev/shots107.sh         出图
ev/probe107.log · debug107b 输出 · final107.log · final107b.log · vd-r107.txt
raw/                   g1~g7（最终出图）· f1~f9（功能）· d1~d7（诊断）· h1~h3（窄档/字号）
                       s1~s12（首轮）
before/                （本代未存前置基线 —— 前置态 = HEAD 的 conversation.html，可直接 git show 取）
```

回滚：
```bash
# ★ 本代首选（只改了一页，直接还原那一页）：
git checkout -- pages/conversation.html

# ⚠ apply107.py --revert 是「**整代回滚**」（严格沿用历代体位）——实测它会：
#   · 删掉 pages/conversation.html
#   · 剥掉 base + 8 页的 ROUTE 表条目 / r101-hdr-css / 会话跳转脚本
#   ⇒ 退到 **r93 之前**的态，不是「只退 r107」。只在本代整体不要了的时候才用它。
python mg-work/r107/apply107.py --revert --dry   # 先看清楚它会动哪些页

# ⚠ **不要**用「重跑 apply106.py」来退 r107：apply106 的 GENS 只有四代，
#   它的「摘块后基线仍残留 r107-conv-css」自检会直接 sys.exit。
```

---

## 七、第二拍（邵先生 2026-10-01 10:0x 返工）

> 原话两条：① 「审查」的 `td-rv-opts` 浮窗**点开后就不能关闭**；
> ② 「侧边聊天」的样式与 `r93-scroll` **不一致**（字号、各种颜色等）。
>
> 体位：r107 **尚未提交** ⇒ 按硬规则「未提交期一律就地返工」，**就地改 `apply107.py`**、不另起代数。
> 源头改序（双层产物，只能下→上）：`part107/{_mods.html, panel.css, panel.js}` → `ev/splice107.py`
> → `ev/make107.py` → `apply107.py`。

### 第二拍 ① 浮窗关不掉 = **一个搜索根写错**，连坐三条关闭路径

`.td-rv-opts` 挂在**审查模块自己的工具条** `.td-mod-bar`（在模块 pane 内），
而 `closeMenus()` 与 Esc 裁决的搜索根写的是**标签栏** `bar = .td-browse-bar` ⇒ 永远查不到它。

| 关闭路径 | 改前 | 改后（实测） |
|---|---|---|
| 点浮窗外的空白 | `hidden` 仍 `false` ✗ | `true` ✓ |
| 按 Esc | 浮窗不关；且事件落到 ctrl-conv ⇒ **把整条侧栏也关掉** ✗ | 浮窗关、`panelOn` 仍 `true` ✓ |
| 选完「统一 / 并排」 | 浮窗留着 ✗ | 自动关 + `is-split` 生效 ✓ |
| 再点一次 `⋯` | 能关（当时唯一通路） | 仍能关 ✓ |

**修法**：`closeMenus()` 与 Esc 裁决的搜索根 `bar` → **`pane`**（= `.td-browse`，两枚浮窗的共同祖先）。

> ★ 这同时解释了第一拍验收里的一个「假失败」：当时点 `[data-td-rv-view="split"]` 得到 `split:false`
> —— 不是并排没实现，而是**前一步的 Esc 已经把整条侧栏关了**，按钮随之不可见 ⇒ 真鼠标点了个空。

### 第二拍 ② 侧边聊天 → 逐值对齐主对话（`r93-scroll`）

| 元素 | 改前 | 改后 | 对齐谁 |
|---|---|---|---|
| 消息正文 | 13px / 20.43 | **15px / 22px** | `.r93-t14` |
| 用户气泡底 | `--color-primary-1` `#F5F8FF` | **`--r93-bubble` `#E5EDFE`** | `.r93-bubi` |
| 用户气泡圆角 | `8px` | **`8px 8px 2px 8px`** | `.r93-bubi` |
| 用户气泡内距 | 8px 10px | **9px 12px** | `.r93-bubi` |
| 引用块 | 12px / 1.6 | **13px / 22px** | `.r93-t12l` |
| 输入框 | 13px / 1.5715 | **14px / 22px** | composer `text-sm leading-[22px]` |
| 助手消息 | `--color-fill-1` 灰底气泡 | **无底裸文本** | `.r93-asst` 助手正文 |
| 助手标记 | 20px 淡蓝圆片 + 写死的「A」 | **24px 同源 GienX logo、无底盘** | `.r93-ahd > .r93-i24` |

实测（`ev/verify107b.log` B1/B2）：侧聊 ✕ 主对话**逐值相同**；暗色档用户气泡两侧同为
`rgb(36,49,76)`；`--ui-fs=18` 时两侧同为 `19.2857px / 28.2857px`。

> ⚠ 助手消息去气泡是**判断**（主对话助手正文从不套气泡），不是测量结论；要回退就把
> `panel.css` 里 `.td-side-bub` 的底色/内距搬回去（一行）。

### 第二拍 ③ ★★★ 返工中挖出的**仓库级机制坑**：`converge()` 把行高压平了

第一次改完，`line-height: calc(22px * var(--ui-fs-ratio))` 在页面上变成裸 **`line-height:22px`**
（源件 `part107/panel.css` 里明明是 `calc`）。根因：

```
applyNN.py 收尾跑  fs.converge(整页)
  converge() 想「原样跳过本代块」，靠的是 apply88b 里的
      RE_OWN_STYLE = '<style id="%s">' % CSS_ID ，而 apply88b.CSS_ID 硬编码 = 'r87-ui-css'
  ⇒ 本代块叫 r107-conv-css，**从未被跳过**
  ⇒ unscale() 把 line-height: calc(Npx * ratio) 还原成裸 Npx
  ⇒ scale_block() 只在「规则体内含 var(--font-size-*)」时才重派生
  ⇒ 体里只写 calc 字号的规则 = **永久压平**（--ui-fs 杠杆失效）
```

**判据**：`--ui-fs=18` 时侧聊正文行高卡在 22px，而主对话 `.r93-t14` 长到 28.29px —— 又「不一致」。
**修法（仓库既有体位）**：凡声明 `line-height` / `height` / `min-height` 的规则，`font-size` 一律写
`var(--font-size-*)` token；15px 这种无 token 的档位用**两段式**（token 规则挂行高 + 只覆盖 font-size 的第二条）。
**自查脚本**：`mg-work/r107/ev/scan-flatten.py <css…>`（模拟这个往返、列出会被压平的规则）。
⇒ 本代 5 条中招：3 条有害（line-height）已修；2 条 `min-height`（`.td-mod-bar` / `.td-url`）**无害**
（`min-height` 只是下限，内容会撑开盒子）。

### 第二拍 ④ 门禁（复跑）

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` ⇒ **10/10**（conversation `script=9 style=16`） |
| 设计回归 | `verify-design.py ./pages` 与 `vd-r101a.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增 |
| 改动面 | `git status` 仍只有 `M pages/conversation.html`；`base.html` **+0 字符** |
| 代数 | `r107-conv-css` / `r107-conv-js` 各 **1**；`r106-*` / `r102-*` 全 **0** |

**产物**：`pages/conversation.html` **866988 → 876008 字符**（第二拍 **+9020**；相对 HEAD **+76777**）。
**裁片**：`raw/z1-opts-open.png` · `z2-opts-split.png` · `z3-esc-scoped.png` · `z4-sidechat-new.png`
· `z5-sidechat-dark.png` · `z6-sidechat-fs18.png`。
**探针**：`ev/diag-user.sh` · `ev/diag107b.sh/.log` · **`ev/verify107b.sh/.log`** · **`ev/scan-flatten.py`** · **`ev/patch107b.py`**。

---

## 八、第三拍（邵先生 2026-10-01 10:2x 返工 · 四条）

> 原话：**① 彻底去掉「侧边聊天」这个功能；② 「审查」的「并排视图」模式下，代码文件不能正常展开和折叠；
> ③ 「折叠全部文件」对应「展开全部文件」；④ 再对照 Codex 官方原版右栏还有哪些功能被遗漏了，请补充。**
>
> 体位：r107 **仍未提交** ⇒ 按硬规则「未提交期一律就地返工」**就地改 `apply107.py`**、不另起代数。
> 源头改序（双层产物，只能下→上）：`part107/{_head.html, _mods.html, panel.css, panel.js}`
> → `ev/splice107.py` → `ev/make107.py` → `apply107.py`。

### 第一拍 ① 侧边聊天 → 全链路删除（含划词浮条）

| 层 | 删掉的东西 |
|---|---|
| `_head.html` | `+` 菜单里的 `data-td-open-mod="side"` 项 |
| `_mods.html` | 整个 `<section class="td-mod td-side" data-td-pane="side">`（工具条 + 消息流 + 输入区）|
| `panel.js` | `AV_SVG` 常量 · `pushMsg`/`sendSide`/`sideQuote`/`sideBody` · `.td-side-av` logo 注入 · **`.td-selbar` 划词浮条整段**（mouseup 选词监听 + mousedown/scroll/resize 收起）· Esc 裁决里的 `selOpen` 分支 |
| `panel.css` | 6. 侧边聊天 · 7. 划词浮条 两节 |

**划词浮条为何一并删**：它存在的前提就是「划词 → 在侧边聊天中提问」，另一枚按钮「添加到对话」在初版里是**空壳**（只收起浮条、什么都不做）。留着就是一枚装饰性假按钮 ⇒ 一并去掉。
> 若之后想要「划词 → 引用到主输入框」，那是**另一个功能**（Codex 也有），可一行加回 —— 需要显式拍板。

探针：`sideMod/sideSec/selbar/sideTab` 四项全 **0**；页面里连「侧边聊天」四个字都搜不到（含注释，已清零）。

### 第一拍 ② 并排视图下折叠失效 = **一条同特异性规则的位置问题**

```css
.td-diff:not(.is-open) .td-diff-rows { display: none; }        /* (0,3,0) —— 写在前面 */
.td-rv-body.is-split .td-diff-split { display: block; }        /* (0,3,0) —— 写在后面 ⇒ 胜出 */
```
两条**特异性完全相同**（都是 3 个类选择器），后者靠文档顺序压过前者 ⇒ 并排态下**折叠后并排行照样显示**
（统一视图正常，所以只在「并排」下暴露）。修法：把 split 那条加一层 `.is-open` 提到 **(0,4,0)**：

```css
.td-rv-body.is-split .td-diff.is-open .td-diff-split { display: block; }
```

实测（`ev/verify107c.log` B / `verify107c2.log` H）：

| 场景 | 统一行 | 并排行 | 行内评论 |
|---|---|---|---|
| 统一 + 展开 | `block` | `none` | `block` |
| 统一 + 折叠 | **`none`** ✓ | `none` | **`none`** ✓ |
| 并排 + 展开 | `none` | **`block`** ✓ | `block` |
| 并排 + 折叠 | `none` | **`none`** ✓ | **`none`** ✓ |

### 第一拍 ③ 「折叠全部文件」⇄「展开全部文件」

同一枚菜单项双向切换，**文案 + 字形一起翻**。判据：
**只要还有折叠着的文件，这一项就是「展开全部文件」**（用户此刻想看全部）；4 个全展开时才是「折叠全部文件」。
手动点某个文件夹头后也会回来同步（`syncFoldBtn()` 挂在单文件折叠处理里）。

| 步骤 | 文案 | 已展开文件数 |
|---|---|---|
| 初始（2 开 2 折） | 展开全部文件 | 2 |
| 点一次 | 折叠全部文件 | **4** |
| 再点一次 | 展开全部文件 | **0** |
| 单独点开第 3 个 | 展开全部文件 | 1 |

### 第一拍 ④ 对照 Codex 官方原版补的遗漏（★ 本轮主体）

依据：`docs/codex-sidepanel-research.md` §3.1 / §3.6 / §4 + 2026-10 官方文档复核
（关键一条：**「The desktop review panel can stage, revert, commit, push, and open a pull request」**）。

| 补的东西 | Codex 出处 | 落点 | 是否真生效 |
|---|---|---|---|
| **对比范围下拉**（上一轮 / 本分支 vs main / 全部未提交改动） | §3.1 `Last turn ⌄` | 工具条最左那颗按钮（原来带 `⌄` 却点不开） | 选中态 + 按钮文案同步 ✓ |
| **`⋯` 显示选项补齐八项** | §3.1 `⋯` 菜单全表 | 原只有「统一/并排 + 折叠全部」两项 ⇒ 现 10 项 | — |
| ↳ 刷新 diff | Refresh | `⋯` | 触发 `.is-refreshing` 淡出淡入 |
| ↳ **自动换行** | Enable word wrap | `⋯` | ✓ `.is-wrap` → `white-space: pre-wrap` |
| ↳ 折叠/展开全部 | Collapse all diffs | `⋯` | ✓ 见 ③ |
| ↳ 不加载完整文件 | Don't load full files | `⋯` | 复选态（纯演示） |
| ↳ 富预览 | Enable rich preview | `⋯` | 复选态（纯演示） |
| ↳ **词级差异** | Enable word diffs | `⋯` | ✓ `.is-worddiff` → `mark` 上 `success/danger-light-2` |
| ↳ **隐藏空白** | Hide white space | `⋯` | ✓ `.is-hidws` → 空白 span `opacity .22` |
| ↳ 复制 git apply 命令 | Copy git apply command | `⋯` | toast 反馈 |
| **工具条动作组** | §3.1 右端那一排 | 复制 / 在文件树中定位 / `⋯` / `提交 ⌄` / `PR` | 定位会**真的切到「文件」标签** ✓ |
| **`提交 ⌄` 下拉两项** | §3.1 `Commit ⌄` → `Commit` / `Push` | 提交到本地 → 提交模态；提交并推送 → toast | ✓ |
| **Open PR** | §3.1 `◐ Open PR` | 工具条最右 | toast 反馈 |
| **逐文件 暂存 / 撤销** | 「can stage, revert…」 | 每个文件夹头右侧 | ✓ `is-staged` 绿态 / `is-reverted` 划线降透明 |
| **「N 行未改动」真展开** | §3.1 `41 unmodified lines` | 折叠条可展开出被藏的行 + 文案翻 | ✓ 统一 4 行 / 并排 2 行，两个互不干扰 |
| **「摘要」模块**（摘要 / 计划 / 来源 / 产物 四段） | §3.6「26.415 起计划、来源、产物、摘要统一进任务侧栏」 | 新增第 5 个模块，填掉 side chat 空出的那一格 | 静态展示 + 复制反馈 |
| **右栏快捷键（真绑定）** | §5 | `⇧⌘G` 审查 · `⇧⌘E` 文件 · `` ⌃` `` 终端 | ✓ 派发即切标签 |
| **轻提示 toast** | （Codex 无此件，为本轮动作类反馈新增） | 面板底部居中，1.4s 自动收 | ✓ |

⚠ **只绑了三个快捷键**：`⌘T` / `⌘P` 是**浏览器级**快捷键，网页 `preventDefault()` 拦不住 ⇒ 不绑，
改由 `+` 菜单承担（菜单里的键位提示照旧显示）。`⇧⌘G` 在 Chrome 是「查找上一个」，可拦 ✓。

### 第一拍 ⑤ 门禁（复跑）

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` ⇒ **10/10**（conversation `script=9 style=16`） |
| 设计回归 | `verify-design.py ./pages` 与 `vd-r101a.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增 |
| 改动面 | `git status` 只有 `M pages/conversation.html`；`base.html` / `avatar.html` **各 +0 字符** |
| 代数 | `r107-conv-css` / `r107-conv-js` 各 **1**；`r106-*` / `r102-*` 全 **0**；`td-side` / `td-selbar` **0** |
| 溢出 | 1440 下工具条 `scrollWidth 639 == clientWidth 639`；`--ui-fs=18` 时工具条与标签栏溢出均 **0** |

> ⚠ 设计回归第一次跑出 **+1 处渐变**（63 → 64）：为「进行中」计划项画的 `linear-gradient` 半填充圆点。
> 该脚本对渐变处数敏感 ⇒ 改为「边色 + 实心浅蓝」（`--color-primary-light-2`），复跑回到基线。

**产物**：`pages/conversation.html` **876008 → 894916 字符**（第三拍 **+18908**；相对 HEAD **+95685**）；
工作区字节（CRLF）**979610**；UTF-8 字节（LF 归一）**976078**。
**裁片**：`raw/y1-modmenu5.png`（菜单五项）· `y2-summary.png` / `y14-summary-dark.png`（摘要浅/暗）·
`y3-split-collapsed.png` · `y4-fold-all.png` · `y5-opts-full.png`（⋯ 十项）· `y6-scope-menu.png` ·
`y7-commit-menu.png` · `y9-fs18.png` · `y10-split-all-hidden.png` · `y11-stage-toast.png` ·
`y12-more-expanded.png` · `y13-more-split.png`。
**探针**：`ev/verify107c.sh/.log` · `ev/verify107c2.sh/.log` · `ev/verify107c3.sh/.log` · `ev/probe-bar.sh/.log`。

---

## 九、第四拍（邵先生 2026-10-01 10:5x 返工 · 五条）

> 原话：**① 将「摘要」作为右栏默认页签，且摘要 / 计划 / 来源 / 产物四个模块要卡片式设计风格；
> ② 划词功能没有了？要补充；③ 新右栏里有些模块或对象是支持对应的右键菜单的，请调查后补充；
> ④ `.td-browse-tab` 的字号应该是 14px；⑤ 整个新右栏的所有下拉菜单（如 `td-mod-menu` 之类的）都要使用 giencoder 设计系统已有的组件。**
>
> 体位：r107 **仍未提交** ⇒ 按硬规则「未提交期一律就地返工」**就地改 `apply107.py`**、不另起代数。
> 源头改序（双层产物，只能下→上）：`part107/{_head.html, _mods.html, panel.css, panel.js}`
> → `ev/splice107.py` → `ev/make107.py` → `apply107.py`。

### 第四拍 ① 摘要设为默认页签 + 四模块卡片式

| 点 | 落点 | 实测 |
|---|---|---|
| 默认页签 | `_head.html` 初始标签 `data-td-mod` `files` → **`summary`**（图标换列表字形 / `aria-controls` / `aria-label` 同步）+ `panel.js` 初始化 `activate('files')` → **`activate('summary')`** | `activeTab="summary"`、可见 pane = `av-browse-pane-summary` |
| 四模块卡片 | `.td-sum-sec` 加 `1px --color-border-1` 描边 + `8px` 圆角 + `--color-bg-2` 底 + `12px` 内距；容器 `gap:12px`、`padding:12px` | `secCount=4`、`sec={bw:1px,r:8px,bg:rgb(255,255,255),pad:12px}`、`secGap=12px` |
| 卡内条目 | 来源 / 产物降级为**行式**（`border-width:0`、`padding:6px 8px`、hover `--color-fill-1`），避免「卡中卡」 | `srcRow/artRow={bw:0px,pad:6px}`、hover 底 `--color-fill-1` |

### 第四拍 ② 补回划词浮条（第三拍被整段删的那条）

第三拍 ① 之所以删它，是因为当时它只服务「划词 → 在侧边聊天中提问」，另一枚「添加到对话」是**空壳**。
本拍按邵先生要求**补回并做成真功能**：两枚都是 **DS 文字按钮**（`giencoder-btn giencoder-btn-text giencoder-btn-size-small`）——
「添加到对话」把选中文本追加进主输入框（占位符「描述你的任务」的那个真 `<textarea>`），「复制」走剪贴板。

| 检查 | 读数 |
|---|---|
| 弹出 | 在 `.r93-scroll` 内选中 ≥1 字 ⇒ `bar:true`、`barRect [18,89,200,38]`、`above:true`（浮在选区上方）、`selRect [63,135,110]` |
| 按钮 | `["添加到对话","复制"]`、`btnCls "giencoder-btn giencoder-btn-text giencoder-btn-size-small"` |
| 添加到对话 | `taBefore 0 → taAfter 17`、`taTail "> /awesome-desig"`、toast「已添加到对话」 |
| 复制 | toast「已复制所选内容」 |
| Esc | 只收浮条：`hiddenAfterEsc:true` 且 `panelStillOn:true`（不关整条侧栏） |

### 第四拍 ③ 补右栏右键菜单（先调查、再表驱动一份容器）

调查结论：右栏里**可右键的对象共九类**，共用同一份表驱动容器 `.td-ctxmenu`（`role=menu`），按目标类型取菜单定义。
能复用既有 handler 的项一律 `元素.click()`，不重写逻辑。

| 目标 | 选中器 | 项数 | 首项 |
|---|---|---|---|
| 标签栏标签 | `.td-browse-tab` | 5 | 关闭 ⌘W |
| 审查文件头 | `.td-diff-h` | 7 | 暂存此文件 |
| 审查代码行 | `.td-dr` | 5 | 在此行添加评论 |
| 终端 | `[data-td-term]` | 6 | 复制 ⌘C |
| 浏览器元素 | `[data-td-el]` | 6 | 标注此元素 |
| 浏览器空白 | `.td-view` | 5 | 后退 ⌘[ |
| 摘要来源 | `.td-sum-src` | 3 | 复制链接 |
| 摘要产物 | `.td-sum-art` | 3 | 预览 |
| 计划条目 | `.td-sum-plan li` | 4 | 标记为已完成 |

实测：九类**全部** `open:true` + `afterShut:true`、`item0h 36px`；含危险项（「撤销此文件的改动」**红字**）。
**反例**（证「不越界」）：右栏内普通空白 `.td-sum-body` **不接管**（`open:false`）、右栏外 `.r93-scroll` **不接管**（`outsideOpen:false`）。

### 第四拍 ④ `.td-browse-tab` 字号 → 14px

`.td-browse-tab { font-size: var(--font-size-body-1) }`（12px）→ **`var(--font-size-body-3)`（14px）**。
实测 `tabFs "14px"`、`tabH "28px"`（标签高由 `min-height` 撑，不随字号变）。

### 第四拍 ⑤ 全右栏下拉改用 giencoder DS 组件

四枚下拉容器（`+` 模块菜单 / `.td-rv-scope-menu` 对比范围 / `.td-commit-menu` 提交 / `.td-rv-opts` 显示选项）
统一挂 **`giencoder-select-popup` + `giencoder-menu`**；条目 = **`giencoder-menu-item`**、
分组标题 = **`giencoder-menu-group-title`**、图标位 = **`giencoder-menu-icon`**、选中 = **`giencoder-menu-item-selected`**。
`panel.css` 自绘那节（`height` / `padding` / `border-radius` / hover 底 / 投影 / 字号）**整段删掉**，
只留定位与槽位（`position/top/left/right/z-index/min-width/max-width` + 子槽 flex）。

实测（四枚全部带 `giencoder-popup-open`）：

| 对象 | 读数 |
|---|---|
| 菜单 | `{r:8px, shadow:"rgba(0,0,0,0.1) 0px 8px 20px 0px", maxH:280px, pad:4px, border:1px rgb(229,229,229)}` |
| 条目 | `{h:36px, r:4px, pl:12px, fs:14px, gap:10px, border:0px}` |
| 选中 | `background:rgb(245,248,255)`（`--color-primary-light-1`）+ 蓝字 + 左缘 3px 条 |
| 分组标题 | `fs:12px, pl:16px, pt:8px, color:rgb(134,134,134)` |
| 项数 | `+` 菜单 **5** · `.td-rv-opts` **10** · `.td-rv-scope-menu` **3** · `.td-commit-menu` **2** |

### 第四拍 ⑥ 挖出并修掉的四个坑（都是「量出来才现形」）

**(a) `.td-mm-item{background:transparent}` 把 DS 选中态底抹掉了**
`.td-mm-item` 的 (0,1,0) 与 DS `.giencoder-menu-item-selected{background:--color-primary-light-1}` **特异性打平**，
而本块写在文档后面 ⇒ 后者被压掉，选中项只剩蓝字 + 左缘条、缺浅蓝底。
修法：改 `.td-mm-item:not(.giencoder-menu-item-selected){background:transparent}`（(0,2,0)、且与选中态不相交）。
`.td-ctx-item` 同步。复测选中态底 = `rgb(245,248,255)` ✓。

**(b) ★★ 四枚下拉被页面级通配适配层翻到锚点上方、顶出视口**
`html[data-r93-page='conversation'] .giencoder-select-popup { top:auto!important; bottom:calc(100% + 4px)!important }`
（r93 ④ 给「贴底 composer 的下拉向上弹」写的）**连右栏新挂的 DS 弹层一起扫到** ⇒ `rect.y = -170`（打开后 -183），
整排菜单看不见 —— 而 `hidden` 摘掉、`popup-open` 加上、`visibility:visible`、`transform:none`、`scale:1` **全对，就是位置错**。
同处还有 r75 的 `.giencoder-select-popup{display:block!important}` 让 `[hidden]` 的 `display:none` 也压不过。
修法：在 `panel.css` 加**更高特异性**（多一层 `.td-browse` ⇒ (0,3,1)）的同名适配把右栏弹层翻回向下
（`top:42px!important; bottom:auto!important; transform-origin:top`）。复测 `w=200, x=856, y=91` ✓。

**(c) ★★ `!important` 连行内样式也压得过 ⇒ 右键菜单坐标改用自定义属性**
同一条 r93 适配层连 `top:auto!important` 都下得去手，**行内 `style.top/left` 也压不过**。
修法：坐标写进 `--td-ctx-x` / `--td-ctx-y` 两个**自定义属性**，再由
`html[data-r93-page='conversation'] .td-browse .td-ctxmenu { top:var(--td-ctx-y)!important; left:var(--td-ctx-x)!important }` 落位。
复测 `pos [980,324]` = 造的 `clientX/clientY` ✓。

**(d) 探针的「过渡中取值」假失败（第三次踩）**
开菜单后**同一次 eval** 里量到 `opacity:0` / `width:192`（过渡起始值），误读成「DS 动画没跑起来」。
修法：打开与量测拆成**两次 eval**（中间 `wait 600`）⇒ `opacity 1 / scale 1 / transform none / pad 4px / border 1px / w 200` 全部到位。

### 第四拍 ⑦ 门禁（复跑）

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` ⇒ **10/10**（conversation `script=9 style=16`） |
| 设计回归 | `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增 |
| 改动面 | `git status` 只有 `M pages/conversation.html`；`base.html` **+0 字符（472150）** |
| 代数 | `r107-conv-css` / `r107-conv-js` 各 **1**；`r106-*` / `r102-*` / `r101-*` / `r93-conv-*` 全 **0** |
| 新增件计数 | `td-ctxmenu` **8** · `td-selbar` **4** · `activate('summary')` **1** · `giencoder-menu-item` **48** · `giencoder-select-popup` **20** · `giencoder-menu-group-title` **4** |

**产物**：`pages/conversation.html` **894916 → 920259 字符**（第四拍 **+25343**；相对 HEAD **+121028**）。
工作区字节（CRLF）**1011192**；UTF-8 字节（LF 归一）**1004420**；LF `sha 5e4ee0c68d70`。
**资产**：`part107/{_head.html 5363 · _mods.html 36137 · browse.html 71892 · panel.css 33651 · panel.js 47097}`。
**裁片**：`raw/d1-summary.png`（默认摘要 + 卡片式）· `d2-modmenu.png`（`+` 菜单 DS + 摘要选中态）·
`d3-ctxmenu.png`（标签右键）· `d4-selbar.png`（划词浮条）· `d5-ctx-src.png`（来源右键）·
`d6-ctx-file.png`（审查文件头右键，含红字危险项）· `d7-ctx-el.png`（浏览器元素右键）。
**探针**：`ev/p107d1~d9.js` · `ev/shots107d.sh` · `ev/shots107e.sh` · `ev/d107g/h/i.log`。

---

## 十、第五拍（邵先生 2026-10-01 11:3x 返工 · 两条）

> 原话：**① 目前新右栏的所有下拉菜单都少了 hover 效果，需补充；
> ② `td-rv-menu giencoder-select-popup giencoder-menu td-rv-opts giencoder-popup-open`
> 这个菜单还没有应用设计系统的组件，需改造。**
>
> 体位：r107 **仍未提交** ⇒ 按硬规则「未提交期一律就地返工」**就地改 `apply107.py`**、不另起代数；
> `GENS` / 注入块 id / `NAV_TAG` 一字不动 ⇒ 工作区照旧只有 `M pages/conversation.html` + `?? mg-work/r107/`。
> 源头改序（双层产物，只能下→上）：`part107/{_head.html, _mods.html, panel.css, panel.js}`
> → `ev/splice107.py` → `ev/make107.py` → `apply107.py`。

### 第五拍 ① hover 全无 —— 真 bug，根因是**同特异性 + 文档序**

| 项 | 内容 |
|---|---|
| 症状 | 四枚下拉 + 右键菜单**一项都没有 hover 反馈**。真鼠标悬停后 `el.matches(':hover') === true`，但 `getComputedStyle(background)` 仍是 `rgba(0, 0, 0, 0)` |
| 根因 | 第四拍为避免「`<button>` 的 UA 灰底 `buttonface` 露出来」，写了基态 `.td-mm-item:not(.giencoder-menu-item-selected){background:transparent}` —— 特异性 (0,2,0)，与 DS 的 `.giencoder-menu-item:hover{background:--color-fill-1}` (0,2,0) **打平**，而本块在文档里**排在 DS 之后** ⇒ 把 hover 底（和选中底）**一起压掉** |
| 修法 | 换族后把**基态与 `:hover` 写在同一块、基态在前**（同为 (0,3,0) 语境），顺序自洽；且不再依赖「DS 的 `:hover` 能不能活下来」 |
| 实测 | `+` 菜单第 2 项：`hover:true` / `bg:rgb(242,242,242)`（= `--color-fill-2`）；其余 4 项仍 `rgba(0,0,0,0)` ✓ |
| 裁片 | `raw/e4-mod-hover.png`（`+` 菜单 hover 高亮）· `raw/e5-ctx-hover.png`（右键菜单 hover 高亮） |

### 第五拍 ② 换组件族：`giencoder-menu` → **DS Dropdown**

**调查过程（结论与字面直觉相反，三步都做了取证）**：

1. **先核字面**：页面里 `td-rv-opts` **只有 1 处**（`pages/conversation.html` 642713），
   其 class 串**完全等于**邵先生给的那串，DS 类名（`giencoder-select-popup` / `giencoder-menu` /
   `giencoder-menu-item` / `giencoder-menu-group-title` / `giencoder-menu-icon`）**一个不缺**
   ⇒ 说明问题不在「有没有挂 DS 类」，而在**挂错族**。
2. **枚举 DS 的菜单家族**（`giencoder-design-system/components/`，68 个契约 json）：
   - `menu.json` —— `mapsFrom: sidenav/topnav`，summary 是「**导航菜单**：纵向/横向/弹出模式…」⇒ 不是下拉；
   - `select.json` —— 「**选择器**：单选/多选/可搜索…」，其弹层类正是 `.giencoder-select-popup` ⇒ 我拿它当了「弹层」用；
   - `dropdown.json` —— 「**下拉菜单**：点击/悬停/**右键**触发的弹出菜单，用于收纳次级操作」，
     `variants.contextMenu` = 右键展开、`anatomy.菜单项` = 「可含**图标 / 快捷键** / 禁用态」、
     `states.selected` = 「文字 `--color-primary-6` **或勾选图标**」、`interaction.hover` = 背景 `--color-fill-2`
     ⇒ **这才是本类交互的正主**。
   - `divider.json` 存在，但**菜单族没有 divider 子部件**（`menu` / `select` 都没有）。
3. **找本仓既有范例**（PLAYBOOK 规则 4：动手前先 grep 组件类名）：
   - **本页 r93 ⑦ 的行右键菜单 `.r93-ctx`** 就是 `.giencoder-dropdown-popup` +
     `.giencoder-dropdown-item` + `.giencoder-dropdown-divider` —— **同一页**、**同一套 DS Dropdown 取值**；
   - `pages/task-detail.html` 的 `.td-ctx` 是另一份（hover 用 `--color-fill-1`，注释写明「以视觉稿为准」）。
     ⇒ 取**本页 r93 的口径**（`--color-fill-2`，与 DS 契约一致）保持**同页自洽**。
   - 页面里 `.giencoder-dropdown-popup` 只内联了**骨架**（`transform-origin:top` / `min-width:168px` /
     `padding:6px` + 一条 `animation: giencoder-popup-in`），`-item` / `-divider` 的编译样式**不存在**
     ⇒ 按 r93 的既定做法「契约类 + 双类提权适配层 + 按需自补」。

**改动清单**：

| 件 | 前 | 后 |
|---|---|---|
| 容器（4 枚 + 右键菜单） | `giencoder-select-popup giencoder-menu` | **`giencoder-dropdown-popup`**（双类提权：`.td-mod-menu.giencoder-dropdown-popup` 等） |
| 条目 | `td-mm-item giencoder-menu-item` | **`td-mm-item giencoder-dropdown-item`** |
| 选中项 | `… giencoder-menu-item-selected is-checked` | **`… is-checked`**（撤掉 Menu 族类） |
| 图标位 | `td-mm-ico giencoder-menu-icon` | **`td-mm-ico`**（收回自绘：Dropdown 无 icon 子部件） |
| 分隔线 | `<span class="td-mm-line">` | **`<span class="td-mm-line giencoder-dropdown-divider">`**（DS 子部件） |
| 分组标题 | `td-mm-cap giencoder-menu-group-title` | **保留**（Dropdown 无此件，借 Menu 的 DS 类；适配层把左内距 16 → 8 与条目对齐） |
| 选中态视觉 | 主色字 + `--color-primary-light-1` 底 + 左缘 3px 条 | **主色字 + 勾选图标 ✓**（DS Dropdown **没有** `-selected` 类，不虚构；契约给的两种表达取全）⇒ 两枚 radio 项补上 `.td-mm-mark` |
| 面板/条目几何 | 自绘一套（36 高 / hover fill-1 / max-height 280 出滚动条） | DS 契约 + 本页 r93 实测：面板 `pad 6 / gap 2 / radius 8 / bg-popup / border-2 1px / shadow3-down`；条目 `pad 5px 8px / radius 4 / lh calc(22px × --ui-fs-ratio) / gap 8`；分隔线 `1px + --color-border-1` |

**换族**顺带解决两件事（都在注释里留了痕）：

- DS 骨架那条 `animation: giencoder-popup-in` **播完会把 `opacity` 打回 0**（菜单「闪一下就不见」）
  ⇒ 适配层显式 `animation: none`，开合一律走契约状态类 `.giencoder-popup-open`（r93 同款处置）；
- `.giencoder-select-popup` 上有一条 **r75 的 `display: block !important`** 通配（给浮窗过渡留起点）
  ⇒ 它把上一版菜单的 `[hidden]` 兜底压死了；换族后不再扫到本菜单 ⇒ **`[hidden]` 恢复可用**
  （实测关菜单后 `afterCloseHidden:true` / `afterClosePopOpen:false`）。

### 第五拍 验证读数（agent-browser 真机）

| 对象 | 读数 |
|---|---|
| `+` 菜单 | `cls=td-mod-menu giencoder-dropdown-popup giencoder-popup-open` · `disp:flex` · `pad:6px` · `gap:2px` · `rad:8px` · `bg:rgb(255,255,255)` · `bw:1px` · `sh:rgba(0,0,0,.1) 0 8px 20px` · **`anim:none`** · `w:168` · `h:214` · `x:856 y:91` · `ovfY:visible` |
| 条目（5 项） | `pad:5px 8px` · `rad:4px` · `lh:22px` · `fs:14px` · `gap:8px` · `bd:0px` · **`h:32`**；**hover 项 `bg:rgb(242,242,242)`，其余透明** |
| 分组标题 | `pad:8px 16px 4px 8px`（左已压到 8 与条目对齐）· `h:30` |
| 开合 | `afterCloseHidden:true` · `afterClosePopOpen:false` |
| `.td-rv-opts` | `w:172` · `h:385`（10 项**不再被 280 截断、无滚动条**）· `ovfY:visible` · 3 条 `giencoder-dropdown-divider`（`h:1` / `bg:rgb(242,242,242)`） |
| 选中项 | `cls=td-mm-item giencoder-dropdown-item is-checked` · `bg:rgba(0,0,0,0)`（DS Dropdown 无选中底）· **`✓` 的 `opacity:1`** |
| `.td-rv-scope-menu` | `w:172` · `h:146` · `x:800 y:91` · 3 项 |
| `.td-commit-menu` | `w:168` · `h:80` · 2 项 |
| `.td-ctxmenu`（右键） | `pos:fixed` · `x:980 y:320`（= 造的 `clientX/clientY`）· `w:186.52` · `h:144` · 3 项 · `head.h:28` · 首项「复制链接」· `ctxClosed:true` |
| **全页残留** | `giencoder-select-popup` **0** · `giencoder-menu-item` **0** · `giencoder-menu-icon` **0** · 反面：`dropdown-popup` **5** · `dropdown-item` **23** · `dropdown-divider` **3** |
| 裁片 | `raw/e4-mod-hover.png` · `raw/e5-ctx-hover.png` · `raw/e6-opts-new.png` |

### 第五拍 门禁

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` ⇒ **10/10**（conversation `script=9 style=16`） |
| 设计回归 | `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增 |
| 改动面 | `git status` 只有 `M pages/conversation.html`（`+2107 / −3` 行）；`base.html` **472150 字符逐字节不变**，另 8 页同 |
| 代数 | `r107-conv-css` / `r107-conv-js` 各 **1**；`r106-*` / `r107-nav-js` 全 **0**（nav 块在 base.html） |
| 残留断言 | 三个迁移脚本自带：旧族类名在**剥掉 CSS 注释后**必须为 0（注释里会提旧类名做说明，不能按裸字面数） |

**产物**：`pages/conversation.html` **920259 → 921730 字符**（第五拍 **+1471**；相对 HEAD **+122499**）。
**资产**：`part107/{_head.html 5270 · _mods.html 35876 · browse.html 71538 · panel.css 35315 · panel.js 47259}`。
**探针**：`ev/p107e1.js`（几何 + 级联诊断）· `ev/p107e2.js`（换族后综合几何/态/残留）·
`ev/fix107e1.py`（`_mods.html` 迁移）· `ev/fix107e2.py`（`panel.css` 两节重写）·
`ev/verify107e.sh` + `ev/e107a/b/c.log` · `ev/shots107f.sh`。

## 十一、第六拍（邵先生 2026-10-01 11:4x 返工 · 三条）

> 原话：**① 对话框 `relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors`
> 底部的那行小字不能被框选是什么问题？② 去掉 `.r93-pre` 的字体族，使用全局默认的即可；
> ③ 当右栏展开后，对话内容容器宽度不够时，`giencoder-select` 技能选择浮窗的宽度也要自适应，
> 这个规则也包括 `r93-alert` 这个容器。**
>
> 体位：r107 仍未提交 ⇒ 就地返工；`GENS` / 注入块 id / `NAV_TAG` 一字不动。
> 三条**全部落在本页适配层**（`part107/panel.css` 第 10~12 节 + `panel.js` 的 `statsBoot`），
> 源件与历代遗产块**一字未动** —— 与 r106 ② （改 `.td-browse-bar` 高度走适配层、源件不动）同一体位
> ⇒ `apply107.py` 仍是「apply106 + 11 处替换」的干净产物。

### 第六拍 ① 底部统计小字框选不到 —— 它是 **CSS 生成内容**，不是 DOM

| 项 | 内容 |
|---|---|
| 宿主 | 邵先生点名的那串 class 是**输入卡**；小字在它**下面一行**，宿主是 React 渲染的 `div.mt-8`（`flex flex-col items-center gap-2`） |
| 根因 | 该行是 r97 ④ 用**纯 CSS `::after`** 生成的：`… > div.mt-8::after { content: '2 轮 · 27 步 · …'; … }`。**生成内容不在 DOM 里** ⇒ 浏览器的选区无法落进去（`content` 挂出来的字既不在 `textContent` 里，也不在 `Range` 里） |
| 判据 | ① `caretRangeFromPoint` 打进该行 → 返回的 `startContainer` 是 `DIV` 且 `offset 0`（没有可落的文本节点）、`Selection.toString()` **长度 0**；② 同一宿主 `Range.selectNodeContents` 只给 131 字符（= 卡内文案），**不含那 111 字的统计行** |
| 对照 | ★ **隔离测试**（`ev/p107f4.js` 临时建两块 DOM，同位置同手法拖选）：`#zzA::after{content:"PSEUDO-SELECT-ME"}` ⇒ `picked:""`；`#zzB` 真文本 ⇒ `picked:"REAL-SELECT-ME"`。**同一次运行、同一套手法**，排除「探针写错了」 |
| 修法 | 关掉旧伪元素（同选择器 + 文档序在后的 `content: none`）→ 由 `panel.js` 注入真节点 `.r107-stats`，版式由 panel.css 逐项复刻（12px / 行高 16×ratio / `--r93-meta` / nowrap） |
| ⚠ React 兜底 | 宿主是 React 的地盘，两个坑：① 重渲染会把不认识的节点**摘掉**；② 重挂时 React 把输入卡插到**末尾**，我们要**再挪回末尾**（否则统计行跑到输入卡上面）。⇒ `MutationObserver`（`document.body` / `childList+subtree`）回调里只做「判存 + 不在末尾就 `appendChild`」，自己造成的 mutation 再进一次回调时判存即返回 ⇒ **天然收敛**，不打架 |
| 实测（1440 关/开、1280 开、1100 开四档） | `statsFound:true` · `isLast:true` · 宿主 `gap:8px` · `{fs:12px, lh:16px, color:rgb(169,169,169), ws:nowrap}` **与旧伪元素逐项相同** · 宿主 `::after` 的 `content` 已是 `none` · **框选 `caretNode:"#text"`、`selLen` 103/103/90/62（>0，改前恒 0）** |
| 位置复核 | `stats` rect `[420, 867, 860, 16]`（1440 关）— 卡底 859 + 宿主 gap 8 = 867，与伪元素版**同一行** |

### 第六拍 ② `.r93-pre` 去掉字体族

| 项 | 内容 |
|---|---|
| 改前 | `.r93-pre { margin: 0; white-space: pre-wrap; word-break: break-all; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }` |
| 改法 | 只覆写 `font-family: var(--font-family)`（= 站点默认那一档，`--font-family` 定义在页面 @332458）；盒模型 / 字号 / 行高 / 换行策略**一字不动**，且**不写 `inherit`**——语义直白、不赌祖先链上没人另设字体 |
| 实测 | `.r93-pre` 计算字体 **=== `body` 计算字体**（`preSameAsBody: true`）；全页 `.r93-pre` 只剩 **1 种**字体族；`font-size 14px` / `line-height 16px` 与改前一致 |

### 第六拍 ③ 内容列变窄时的两条自适应

判据**不是视口分辨率**，而是**对话内容列的可用宽**（右栏开合、左导航收拢都会改它）⇒ 两条都写成
`min(原值, 容器宽)`，天然跟着容器走（口径同 ④b 的 `.r93-bub`）。

**改前实测（右栏展开，`ev/f107w{1440,1280,1100,1024}.log`）**：

| 视口 | 列宽 | 技能浮窗（写死 760） | `.r93-alert`（写死定高 44） |
|---|---|---|---|
| 1440 | 714 | 左右各溢 **23px**（顶到滚动口裁剪边） | `42/42` ✓ |
| 1280 | 554 | 左右各溢 **81px** ⇒ **左侧技能名字头被裁** | `42/43` 起溢 |
| 1100 | 374 | 严重越界 | `42/65` ⇒ 文字**溢出圆角盒**压到相邻行 |
| 1024 | 315 | 严重越界 | `42/87` |

**改法**：
- 技能浮窗（React **行内** `style` 写死 `width:760`）⇒ `width: min(760px, 100%) !important`。
  `!important` 是必需的：**行内样式优先级最高**，同特异性/更高特异性都不够。
  包含块是输入卡（`position: relative`）⇒ `100%` = 输入卡内宽，浮窗恒居中、不越界。
- `.r93-alert` ⇒ `height: auto; min-height: 44px; padding: 8px 16px`。
  `8px` 竖内距与单行态**完全等价**（内容 22+16 = 38 < 44 ⇒ 仍被 `min-height` 顶到 44，
  `align-items:center` 让单行照样居中）⇒ **单行宽度不变化**，只有折行时才真正长高。

**改后实测**：

| 视口 | 技能浮窗 | 相对滚动口溢出 | `.r93-alert` |
|---|---|---|---|
| 1440 | `w 712`（= 输入卡 714 − 2 边框） | **−23 / −23**（在内侧） | `h 44` · `42/42` ✓ 不变 |
| 1280 | `w 552` | −23 / −23 | 第一条 **`h 62`** · `60/60` · `descInside:true` |
| 1100 | `w 372` | −23 / −23 | **`h 106`** · `104/104` · 第二条 `h 84` · `82/82` |

### 第六拍 门禁 / 产物

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍「已是目标态（无改动）」 |
| 语法 | `check-syntax.py pages/*.html` ⇒ **10/10**（conversation `script=9 style=16`） |
| 设计回归 | `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增 |
| `converge()` 安全 | `fs.converge()` 会把 `<style id="r107-conv-css">` **整块 stash 跳过**（`RE_OWN_STYLE`）⇒ 新增的 `min/heights` 不会被 unscale/scale 派生吃掉 |
| 改动面 | `git status` 只有 `M pages/conversation.html`（`+2202 / −3` 行）；`base.html` **472150 字符逐字节不变**，另 8 页同 |
| 增量归属 | 页面 **+4046** = `panel.css +2723` + `panel.js +1324`（差 1 字节 = 注入时 `.strip()` 去掉的尾换行） |

**产物**：`pages/conversation.html` **921730 → 925776 字符**（第六拍 **+4046**；相对 HEAD **+126545**）。
工作区字节（CRLF）**1019153**；UTF-8（LF 归一）**1012253**；LF `sha1 6655f13a1afd`。
**资产**：`part107/{_head.html 5270 · _mods.html 35876 · browse.html 71538 · panel.css 38038 · panel.js 48583}`。
**探针**：`ev/p107f1~f7.js` · `ev/p107g1.js` · `ev/probe107f.sh` · `ev/verify107g.sh` ·
`ev/f107a~g.log` / `f107w*.log` / `g1-*.log`。**出图**：`raw/f1-composer.png`（改前底排）·
`raw/f3-alert1100.png`（改前 alert 溢出）· `raw/f4-skill1280.png`（改前浮窗被裁）·
`raw/g1-stats.png`（改后统计行可框选）· `raw/g3-skill1280.png` · `raw/g5-alert1100.png`。


## 十二、第七拍（邵先生 2026-10-01 12:1x 返工 · 七条）

> 七条里六条落在右栏样式层（`part107/panel.css`），一条是文案替换（`part107/_mods.html` + `apply107.py`）。
> 仍是 r107 **未提交期的就地返工** ⇒ `GENS` / 注入块 id / `NAV_TAG` 一字不动，
> 改序照旧：`part107/*` → `ev/patch107h*.py` → `ev/splice107.py` → `ev/make107.py` → `apply107.py`。

### 第七拍 ① 竞品名 → GienCoder

**改动面** = 右栏里**渲染成文字**的 8 处 + 两处悬停 `title`：

| 位置 | 改前 | 改后 |
|---|---|---|
| `.td-diff-path`（审查 · 文件头） | `docs/codex-sidepanel-research.md` | `docs/giencoder-sidepanel-research.md` |
| `.td-dr-t` ×3（统一视图 / 并排视图 / 折叠行） | `# Codex 右栏调研` | `# GienCoder 右栏调研` |
| `.td-sum-p`（摘要 · 描述段） | `…升级成 Codex 那套标签式 Side Panel` | `…升级成 GienCoder 那套…` |
| `.td-sum-src b` ×2（来源标题） | `The complete guide to Codex` | `The complete guide to GienCoder` |
| `.td-sum-src b`（来源标题） | `Codex changelog` | `GienCoder changelog` |

★ **判据**：`createTreeWalker(SHOW_TEXT)` 走一遍 `.td-browse` 子树，正则 `/codex|chat\s?gpt/i` 命中数
**8 → 0**（1440 / 1280 / 1100 / 1024 四档一致）；属性扫描（**排除 `href`**）**2 → 0**。

**有意保留 3 处**：`td-sum-src` 的三条外链 `href`（`flaviocopes.com/codex/` ·
`developers.openai.com/codex/changelog` · `worldprogramming.org/posts/the-complete-guide-to-codex-ghdafz`）——
它们是**真实可打开的地址**，替换域名段直接 404；且**不渲染成页面文字**（只在状态栏出现）。

**另清一处（真·全局）**：`pages/avatar.html` 历史会话列表里的示例标题
`'Codex自定义大模型方法'` → `'GienCoder自定义大模型方法'`（`git diff --numstat` = `+1 / −1`，只这一处）。
做法照 `apply106.py` 里 `2b)`（GienX → GienCoder 改 task-detail.html）的先例，在 `apply107.py` 新增
**`2d)` 正向 + 逆操作**，`make107.py` 的 EDITS 由 11 处增至 **13 处**（E12 / E13）。
⚠ 锚点用**带引号的整串**（`'Codex自定义大模型方法'`），不碰该文件里的同名注释；幂等。

**剩下的 7 处**（CSS 5 · JS 2）是本代前六拍写下的**设计来源注释**（如「复刻对象 = Codex 右侧 Side Panel」），
不渲染、且是后续维护者判断「照谁做的」的唯一线索 ⇒ **保留**。
★ **本轮自己新增的注释已改成「竞品名」中性表述**（第 13 节头部），避免「新增文档里又引入被清理的词」。

### 第七拍 ② 去掉下拉菜单的标题行

真身两类：

- **静态 HTML**：`.td-mm-cap`（`+` 菜单的「在侧栏打开」、审查范围菜单的「对比范围」）
- **JS 现场生成**：`.td-ctx-head`（右键菜单顶部的「目标名」行，`ctxBuild()` 里建）

修法 = **一段 CSS 同时关掉两类**：

```css
.td-browse .td-mm-cap,
.td-browse .td-ctx-head { display: none; }
```

为什么用 `display:none` 而不是删节点：① 两类来源一处管（JS 生成的那类没法用 HTML 删）；
② 菜单是 `flex-direction: column`，塌掉的行不参与布局 ⇒ 与真删节点视觉等价。
**实测**：`capDisp: "none"`、`getBoundingClientRect()` 归零；
右键菜单 `heads:1`（节点仍生成）而 `headDisp: "none"`（不占位）。

### 第七拍 ③ 选中项常显底色

**改前实测**：4 个 `.is-checked` 项 `background-color: rgba(0,0,0,0)` —— 只有主色文字 + 右侧 ✓。
**改后**：`rgb(245, 248, 255)`。

取色依据 = **DS Menu 的 `.giencoder-menu-item-selected`**（`background: var(--color-primary-light-1)`）；
**不补**那枚 3px 左缘条 —— 第五拍已认定它属于 Menu 族的表达，不是 Dropdown 的（不虚构组件没有的部件）。
规则写在 `:hover` 规则**之后** ⇒ 悬停选中项时底色不翻成 hover 灰（邵先生要的「常显」）。

### 第七拍 ④ 去掉快捷键提示

`.td-mm-key` 实测 **10 处**：⇧⌘G / ⌃\` / ⌘T / ⌘P / ⌘I / ⌥⌘C / ⌥⌘P / ⌘1 / ⌘2 / ⌘R；
右键菜单里另有一类 `.td-ctx-key`（JS 生成）。同 ② 用一段 CSS 关掉。
**实测**：`keyDisp: "none"`；菜单宽度随之收窄（右侧那列不再占位），菜单高度也矮了一行（标题行）。

### 第七拍 ⑤ 提交卡「目标分支」输入框拉通

**根因**：它挂 DS 的 `.giencoder-input-wrapper`，编译样式是
`display: inline-flex; width: auto; min-width: 120px` ⇒ 宽度只吃内容自然宽。

**实测（改前）**：卡片内容宽 **308**，它只有 **207**（差 **101**）；
同一张卡里的 `.td-commit-h` / `.td-commit-lb` / `.td-commit-msg` / `.td-commit-f` **都是 308** —— 只有它短一截。

**修法**：`.giencoder-input-wrapper.td-commit-in { display: flex }` —— 写**双类**（(0,2,0)）而不是单类，
不依赖「panel.css 在文档序最后」这条约定，内部 `prefix + input` 的排布一字不动。

**实测（改后）**：`308 / 308`、`gap: 0`，四档分辨率一致（卡片 `max-width: 340` + `padding: 16` ⇒ 308 恒定）。

### 第七拍 ⑥ 右栏字体统一

**分两处做**（因为来源不同）：

1. `panel.css` 自己那 **8 条**写死的等宽族**就地改**成 `var(--font-family)`：
   `.td-diff-path` / `.td-diff-stat` / `.td-dr` / `.td-dsc-c` / `.td-diff-more` / `.td-commit-num` /
   `.td-term` / `.td-url-pill input`。
2. 「文件」模块代码区那条**挂在本代不修订的移植件上** —— `.td-browse-pre` 的
   `font-family: ui-monospace, …` 在 **r102 代已交付的 `mg-work/r102/part105/browse.css`** 里
   （跨代沿用，不回改已交付的代）⇒ 在 panel.css 末尾用**多一级类数**覆盖：
   `.td-browse .td-browse-pre { font-family: var(--font-family) }`；
   它那 `.td-code` / `-no` / `-tx` / `-k` / `-s` 子树（实测 **153 个节点**）全靠继承。
   ★ 这条是**改完第一遍量出来才补的**：首轮只改了 panel.css 里的 8 条，
      量到「还剩 153 个节点落等宽」⇒ 再往下查才定位到移植件。

**判据**：`.td-browse *`（1137 → 1149 个元素）里 `getComputedStyle(el).fontFamily !== bodyFont` 的
**计数 153 → 0**；8 个抽样点（终端 / diff 行 / diff 路径 / 提交卡分支名 / URL 槽 / 文件树代码区…）全部 `OK`。

### 第七拍 ⑦ 全屏按钮随右栏展开 / 收起

**判据位置（★ 「先量后写」的典型）**：右栏的开关类是 `.av-browse-on`。
实测它加在 **shell 的 flex 行**上（`class="flex min-h-0 flex-1 pb-2 pl-3 pr-2 av-browse-on"`），
而页头那枚按钮在 `main` 里 ⇒ 它是该类元素的**后代** ⇒ **纯 CSS 可判，不需要 JS 联动**。

```css
.av-browse-on .r93-baract[data-r93-fullscreen] { display: none; }
```

只针对「全屏」那一枚（`data-r93-fullscreen`）；旁边那枚开关侧栏的**不动**（`.r93-baracts` 里两枚共 2 个子元素）。
**实测**：右栏关 `display: flex`（`rect [1359,57,28,28]`）／右栏开 `display: none`（rect 归零）——
页头右侧由两枚变一枚。

### 第七拍 门禁 / 产物

| 项 | 读数 |
|---|---|
| 幂等 | `apply107.py` 两遍 ⇒ 第二遍「已是目标态」；`patch107h.py` / `patch107h2.py` 复跑均 0 变化 |
| JS/CSS 语法 | `mg-work/check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`） |
| 设计校验 | `verify-design.py ./pages` 与上轮 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增** |
| 改动面 | `git status` = `M pages/conversation.html`（`+2244 / −3`）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/` |
| 其它页 | `base.html` **472150 字符 / LF sha1 `23f6fbedfe76` 逐字节不变**；另 8 页字符数全同 |
| 字体残留 | `panel.css` 里 `ui-monospace` 只剩 **1 处**（第 11 节的说明注释，非声明） |
| 注入块 id | `r107-conv-css` / `r107-conv-js` 各 1；`r106-nav-js` / `r107-nav-js` / `r102-` 均 **0** |

**产物**：`pages/conversation.html` **925776 → 927464 字符**（第七拍 **+1688**；相对 HEAD **+128233**）。
工作区字节（CRLF）**1022207**；UTF-8（LF 归一）**1015265**；LF `sha1 79aa4533761b`。
**资产**：`part107/{_head.html 5270 · _mods.html 35916 · browse.html 71578 · panel.css 39686 · panel.js 48583}`。
**探针**：`ev/p107h1.js`（七条现状）· `ev/p107h2.js`（提交卡量宽）· `ev/p107h3.js`（七条验证）·
`ev/probe107h{,2,3}.sh` · `ev/h107-*.log`。
**出图**：改前 `raw/h2-{add-menu,opts-menu,commit}.png`；改后 `raw/h3-{add-menu,opts-menu,commit,ctxmenu}.png`。
**备份**：`ev/bak7/`（本轮动手前的 `panel.css` / `panel.js` / `_mods.html` / `make107.py` / `apply107.py`）。


---

## 十三、第八拍（邵先生 2026-10-01 12:3x 返工 · 六条）

六条全部落在 `part107/panel.css`（新增**第 14 节** + 第 3 / 6 / 10 节就地改）+ `part107/panel.js`（删一项菜单）；
`_mods.html` / `browse.html` **一字未动** ⇒ 不必重跑 `splice107.py` / `make107.py`。

### 第八拍 ① 全局「宽度不够 ⇒ 文字省略号」（★ 本轮主体）

**落地口径 = 三类分治**（写死进第 14 节的注释，免得下轮再逐条讨论）：

| 类 | 处置 | 例子 |
|---|---|---|
| 单行文本容器（名称 / 路径 / 域名 / 标题 / 计数） | **省略号** | `.td-browse-tree-title` / `.td-diff-btn` / `.td-commit-btn` / `.td-note-time` / `.td-sum-tag` / `.td-rv-commit` … |
| 代码与终端 | **不截断**（保持 `pre` + 折行） | `.td-dr-t` / `.td-dsc-c` / `.td-code-*` / `.td-term-*` |
| 多行正文 | **不截断**（折行） | `.td-sum-p` / `.td-note-b` / `.td-sum-plan li` / `.td-page-h1` |

**三件套缺一不可**：`min-width: 0`（flex 子项的收缩下限默认是 `min-content`，不解除就永远把兄弟顶出去）
+ `overflow: hidden` + `text-overflow: ellipsis` + `white-space: nowrap`（不换行才谈得上省略）。

**白名单 17 类**（`querySelectorAll(sel).length` vs 「三件套齐」的元素数 —— 三档实测 **EL = n，零例外**）：

| 选择器 | n | 选择器 | n |
|---|---|---|---|
| `.td-browse-tree-title` | 1 | `.td-sum-tag` | 1 |
| `.td-diff-more` | 2 | `.td-sum-srct i` | 3 |
| `.td-diff-btn` | 10 | `.td-sum-artt i` | 2 |
| `.td-commit-btn` | 2 | `.td-elnote-t` | 1 |
| `.td-commit-t` | 1 | `.td-url-annot` | 1 |
| `.td-commit-lb` | 1 | `.td-page-cta` | 1 |
| `.td-note-who` | 2 | `.td-page-foot` | 1 |
| `.td-note-time` | 2 | `.td-rv-commit` / `.td-rv-pr` | 1 / 1 |

**改前已覆盖的六类未被弄坏**：`td-tab-name` / `td-mm-name` / `td-diff-path` / `td-rv-meta` /
`td-sum-hint` / `td-browse-crumb-path`。

★ **两条补充规则**（容器自带 `display:flex / inline-flex` 时，裸文本会变成**匿名 flex 项**，
容器上的 `text-overflow` 对它**无效** ⇒ 文字落在子 `<span>` 里的要单独点）：
`.td-rv-commit` / `.td-rv-pr` / `.td-commit-row` / `.td-commit-ck` 的 `> span`；
行内评论头 `td-note-who` 先让位（`flex: 1 1 auto`）、`td-note-time` 保原宽（`flex: none`）。

**验证（三档真机）**：1440 / 右栏开 · 1024 / 右栏开 · 右栏压到 **240px**（改 `--av-browse-w`）。
窄栏实测被裁元素**全部**呈 `ellipsis/nowrap`（`i3-panel230-review.png` 里 `p...` / `m...` / `do...` / `.work...`
均出省略号），且多行评论 / 代码**正常折行、未截断**。

### 第八拍 ② 去掉「折叠此文件」

`panel.js` 的 `ctxForFile()` 里**整项删除** `{ label: isOpen ? '折叠此文件' : '展开此文件', … }`；
顺手删掉失去引用的 `var isOpen = art.classList.contains('is-open');`（全文 `isOpen` 剩 **0** 次）。
右键文件菜单 = **6 项**：暂存此文件 / 撤销此文件的改动 / 复制文件路径 / 复制 git apply 命令 /
在文件树中定位 / **展开全部文件**（探针 `hasFoldOne: false`）。
★ 头部职责注释同步：`③ 审查：文件折叠（点头部 = 单个 / 菜单 = 全部⇄展开全部）…`。

### 第八拍 ③ `.td-sum-h` = 15px

`.td-sum-h { font-size: calc(15px * var(--ui-fs-ratio)); }` —— **不写裸 `15px`**：
本代 `converge()` 把「体里含 `var(--font-size-*)`」当作重派生判据，而 15px **没有 title token**
⇒ 用 `calc(Npx * var(--ui-fs-ratio))` 形态（**自动豁免压平**、且仍吃 `--ui-fs` 杠杆）。
实测 4 个 `h4.td-sum-h` = `{('15px','500')}`，行高随之 `22.5px`（`.td-sum-sec` 自然长高），三档一致。

### 第八拍 ④ `.td-diff-path` 展开后中粗 500

```css
.td-diff.is-open .td-diff-path { font-weight: 500; }
```

展开 `font-weight: 500` / 折叠 `400` —— 4 张 diff 卡同屏对照（`i3-review-panel.png` 可见粗细差）。

### 第八拍 ⑤ `.td-diff-path` 与 `.td-diff-rows` 内一律 13px

`path` 容器 = `var(--font-size-body-2)`（13）；`rows` 容器同样 13，且 `.td-dr` / `.td-dsc-c` / `.td-diff-more`
**三处各自写死的字号**逐条同值覆盖（只改容器无效）。
★ **只换 token 档位**（仍旧写成 `var(--font-size-*)`）⇒ `converge()` 的「含 token 才重派生行高」判据不受影响：
`.td-dr` 行高 **20px 未变**、`.td-diff-h` 高 **38 未变**（派生链完好）。

### 第八拍 ⑥ `.r107-stats` 文字居中（★ 两处死胡同，值得记）

**死胡同 1**：第一版写 `width: fit-content; max-width: 100%; margin: 0 auto` ⇒ 被页面级两条
`!important` 规则**压死**（`main > … > div.mt-8 > div`：r95 ② 的 `width:50%!important; min-width:860px!important`
与 r106 ④ 的 `width:min(…)!important; min-width:0!important`）⇒ 盒宽**恒等于输入卡**（实测 860 / 714 / 315 三档全等），
`width / min-width / max-width` **一条都改不动** ⇒ `fit-content` 是**死代码**。
诊断路径：先以为是 `min-width:auto` ⇒ 用 `min-width:0` / `width:100%` 做**反证**，三种状态盒宽**都不变**
⇒ 才顺藤查到那两条页面级 `!important`。

**死胡同 2**：真节点不像当年的 `::after` 那样自动 shrink-wrap ⇒ 满宽盒里文字默认靠左；
而宿主的 `items-center` 对这个**满宽子项**不生效（实测输入卡自己就是齐左的）⇒ `margin: auto` 会比输入卡**偏 32px**。

⇒ **正解 = `text-align: center`**（它没有任何 `!important` 竞争者）。
判据 = **文字盒中心 − 输入卡中心 = 0**（用 `Range.selectNodeContents` 取**文字真实盒**，与输入卡几何比）。
1440（右栏开）：盒 714 / 文字 630 / 左内距 42 ⇒ **中心差 0**。

★ **① 与 ⑥ 在本元素上可以共存**：Chromium 在「居中 + 溢出」时对齐行为**退化为 `start`**
（文字盒仍自盒左缘起算），省略号**照常落在行尾** —— 实测 1024 截图尾部为「首 token 平…」。
（★ 第一版注释把这条写反了，看截图后**整块更正**。）

### 第八拍 门禁 / 产物

| 项 | 读数 |
|---|---|
| 幂等 | `patch107i.py` 末次 **`应用 0 项 / 跳过 8 项`**；`apply107.py` 第二遍「已是目标态」 |
| JS/CSS 语法 | `mg-work/check-syntax.py pages/*.html` **10/10 通过**（conversation `script=9 style=16`） |
| 设计校验 | `verify-design.py ./pages` 与上轮 `vd-r107h.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增** |
| 压平自查 | `ev/scan-flatten.py` 改前改后均 **2 条**（`.td-mod-bar` / `.td-url`，与本拍无关）⇒ 无新增风险 |
| 改动面 | `git status` = `M pages/conversation.html`（`+2299 / −3`）+ `M pages/avatar.html`（`+1 / −1`，第七拍遗留）+ `M .workbuddy/memory/*` + `?? mg-work/r107/` |
| 其它页 | `base.html` **472150 字符 / LF sha1 `23f6fbedfe76` 逐字节不变**；另 8 页 sha1 全同 |
| 注入块 id | `r107-conv-css` / `r107-conv-js` 各 1；`r106-nav-js` / `r107-nav-js` / `r102-` 全 **0** |

**产物**：`pages/conversation.html` **927464 → 930384 字符**（第八拍 **+2920**；相对 HEAD **+131153**）。
工作区字节（CRLF）**1026880**；UTF-8（LF 归一）**1019883**；LF `sha1 c8b5e944e2de`。
**资产**：`part107/panel.css` **40517 → 42788** 字符（CRLF 832 → 889 行）· `panel.js` **48583 → 48401** 字符（LF 1127 行）；
`_head.html` / `_mods.html` / `browse.html` 未动。
**探针**：`ev/p107i1~i5.js` + `ev/probe107i{,2,3,4,5}.sh` + `ev/shots107i.sh`；
日志 `i107-*.log` / `i107-v-*.log` / `i107-s-*.log` / `vd-r107i{,2}.txt`；出图 `raw/i1-*` · `raw/i2-*` · `raw/i3-*`。
**备份**：`ev/bak8/`（动手前的 `panel.css` / `panel.js`）。

## 十四、第九拍

邵先生 2026-10-01 13:1x 两条（**r107 未提交期就地返工，不另起代数**）：

> 在新右栏"全屏"后：
> 1、原全屏按钮的图标没有变为"取消全屏"的图标；
> 2、"拖动调整文件预览栏宽度"的功能不正常，按下鼠标不能正常左右拖动，似乎一下就复位了。

### ① 全屏后按钮图标不翻（真 bug）

**根因**：按钮的内联 SVG 是 `browse.html` 里**写死**的「四角朝外」字形，
`panel.js` 切换时只翻了 `aria-pressed` / `title` / `aria-label`（实测这三项都对），
**`<path d>` 一个字节没动** ⇒ 字形永远是「最大化」。

**修法**（`part107/panel.js`）：抽 `setMax(on, silent)` + 新增 `setMaxIcon(on)`；
MAX 那套**从 DOM 读出来缓存**（不另抄一份免得漂移），MIN 那套硬编码四条
（Lucide `minimize`：`M8 3v3a2 2 0 0 1-2 2H3` / `M21 8h-3a2 2 0 0 1-2-2V3` /
`M3 16h3a2 2 0 0 1 2 2v3` / `M16 21v-3a2 2 0 0 1 2-2h3`），只切 `d` 属性、**不重建节点**
（不碰 React，hover / focus / 键盘可达性一字不变）。

**判据**：全屏后 4 条 path 的 `d` = MIN 那套 ✓；拖拽退出后回 MAX ✓；再全屏又 MIN ✓；
收起侧栏后回 MAX ✓。★ **目视复核**（`raw/j3-bar-1440-max.png` vs `j3-bar-1440-min.png`）：
一个四角朝外、一个四角朝内，方向相反。

### ② 全屏后拖分栏条「一按就复位」（真 bug，两个因）

**因 (a)：拖拽起点取的是「内部缓存」，不是实况。**
`ctrl-conv.js` 的 `bindSplit()` 里 `startPanel = panelW`；而 `panelW` 只在
「恢复记忆 / 拖动 / 双击复位 / 键盘」时更新 —— r107 的「最大化」是**绕过控制器直接写
`--av-browse-w`** ⇒ 缓存停在 641，实际已是 1040。实测（1440 / 右栏开 / 全屏 1040）：

| 动作 | 改前 `--av-browse-w` | 应为 |
|---|---|---|
| pointerdown | 1040 | 1040 |
| pointermove(-120) | **761**（= 641 + 120） | 1160 → 钳回 1040 |

⇒ 一按下拖动，右栏从 1040 猛缩到 761（≈ 记忆宽）—— 正是报障的「一下就复位」。

**因 (b)：`pointermove` / `pointerup` 挂在元素上，只靠 `setPointerCapture` 兜底。**
全屏后分栏条紧贴窗口左缘，往左拖时指针很快离开元素；一旦捕获没生效（元素被 React 重挂 /
`pointerId` 失配），拖动就**中途断掉**。

**修法**：
* (a) 起点改读**实际渲染宽** —— 先落 `.is-col-dragging`（= `transition: none`）再取
  `getBoundingClientRect()`（拿到的是**终值**而非过渡中间值），并把缓存同步回来；
* (b) `pointermove` / `pointerup` / `pointercancel` / `blur` **一律挂 `window`**（站内其它拖拽同口径）；
* 另加两条**退出路径**：**全屏态下按下分栏条 = 放弃全屏**（`setMax(false, true)` —— 只清状态、
  **不动宽**，宽度交给控制器从实际宽起算）；**侧栏收起时也退出全屏**。

**判据**（1440 / 清 localStorage / 全屏 1040 / 合成 PointerEvent）：

| 动作 | 结果 |
|---|---|
| 全屏 | `--av-browse-w` 1040 ｜ `data-td-maxw` 1040 ｜ `aria-pressed` true ｜ 图标 MIN |
| pointerdown | `maxw` → **(none)**（静默退全屏）、宽度仍 **1040** |
| move(+80) **派发到 `document.body`** | **1040 → 960** ✓（起点 = 实际宽 ✓；事件确已挂 `window` ✓） |
| pointerup | 960 保持；按钮回 `aria-pressed=false` / 图标 MAX |
| 收起侧栏 | `maxw` **(none)** / `aria-pressed` false / 图标 MAX ✓ |

1024 档同流程：全屏 624 → move(+80) ⇒ **561**（= `MIN_PANEL`，钳位正确）。
**回归**：文件树分栏条（`[data-td-split="tree"]`）先把右栏拉到 900 再拖 ⇒ 240 → **280** ✓
（同一函数的两处绑定都验过）。

### 体位 / 覆盖件说明（本拍唯一的结构性决定）

`part105/*` 是**跨代资产**（源页 `avatar.html` 的移植源，历代刻意不回头动它）。
本拍要改的 `bindSplit()` 正在 `part105/ctrl-conv.js` 里 ⇒ 按
`_read_part()` 的 `PART_DIRS = (part107, part105)` **双目录回退**语义，在 `part107/` 放一份
**逐字副本 + 一处修正**（`part107/ctrl-conv.js`）—— **part105 原文与 `avatar.html` 零影响**。
⚠ 代价 = 副本会漂移，已在副本头部写明来源与差异点。

★ **别用 MutationObserver 盯「后插节点」的父级**：那条 flex 行与分栏条都是 ctrl-conv 在
`place()` 里后插的，本文件跑得更早 ⇒ 初次观察挂在**旧父级**上、**永不触发**
（本拍第一版就是这么坏的：收起后 `data-td-maxw` 残留 784、按钮仍是「还原」态）。
正解 = 搭 ctrl-conv 既有的 `setOpen()` **必定 dispatch 一次 resize** 这个事件流。

### ⑨ 本拍门禁 / 产物

幂等 ✓（`应用 0 项 / 跳过 3 项`；`apply107.py` 第二遍「已是目标态」）｜`check-syntax.py pages/*.html` **10/10**｜
`verify-design.py ./pages` 与 `vd-r107i2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜
`scan-flatten.py` `panel.css` 仍 **2 条**（本拍**零 CSS 改动**）｜
改动面 = `M pages/conversation.html`（`+2373 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍文案）
+ `?? mg-work/r107/`（含新建 `part107/ctrl-conv.js`）。
产物 **930384 → 934109 字符（+3725；相对 HEAD +134878）**。
★ **体位**：本拍**未动** `_mods.html` / `browse.html` ⇒ 不必重跑 `splice107.py` / `make107.py`，
改序只剩 `part107/*` → `apply107.py`（part 文件是**运行时读**的，改完直接重跑即落页面）。

## 十五、第十拍（邵先生 2026-10-01 13:2x 返工 · 一条）

> 原文：**「`td-rv-menu giencoder-dropdown-popup td-rv-opts giencoder-popup-open`
> 菜单的位置不对，应该显示在触发按钮的下方」**

### 第十拍 ① 三枚 `.td-rv-menu` 从「钉面板 `top: 42px`」改为「按触发器现场摆位」

**症状**：点「显示选项」（`.td-rv-opts`）时，菜单跑到**触发按钮上方**。

**量出来的实况**（1440 / 右栏开 / 审查模块；`dy = 菜单 top − 触发器 bottom`）：

| 菜单 | 触发器 | 所在容器 | 触发器 bottom | 菜单 top | dy | 判定 |
|---|---|---|---|---|---|---|
| `.td-mod-menu` | `.td-browse-add` | 标签栏 | 84.5 | 91.0 | **+6.5** | OK |
| `.td-rv-scope-menu` | `.td-rv-scope` | **工具条** | 126.0 | 91.0 | **−35.0** | 错 |
| `.td-rv-opts` | `.td-browse-ico[data-td-rv-opts]` | **工具条** | 125.0 | 91.0 | **−34.0** | 错 |
| `.td-commit-menu` | `.td-rv-commit` | **工具条** | 127.0 | 91.0 | **−36.0** | 错 |

**根因**：四枚下拉共用一条基类规则 `{ position: absolute; top: 42px }`（相对 `.td-browse`，
42px = 标签栏 44px 下方）。但 `.td-mod-menu` 的触发器在**标签栏**里，另三枚的触发器在
**审查模块的工具条**（`.td-mod-bar`，绝对 93~134）里 ⇒ 同一条 `top` 对后者就变成「按钮上方 35px」。
**一条规则服务两种锚点高度 ⇒ 必然错一半。**

**修法**（JS 现场摆位；`.td-mod-menu` 一字不动）：

```js
var RV_GAP = 6, RV_PAD = 4;
function placeRv(menu, trigger) {
  if (!trigger || !menu.classList.contains('td-rv-menu')) return;
  var host = menu.offsetParent;                  /* = .td-browse（position: relative） */
  if (!host) return;
  var hr = host.getBoundingClientRect();
  var ox = hr.left + host.clientLeft, oy = hr.top + host.clientTop;   /* 包含块原点 = padding box */
  var tr = trigger.getBoundingClientRect();
  var top = tr.bottom - oy + RV_GAP;
  var left = tr.left - ox;
  var maxLeft = host.clientWidth - menu.offsetWidth - RV_PAD;
  if (left > maxLeft) left = maxLeft;            /* 右侧放不下 ⇒ 向左收，贴住面板右内边 */
  if (left < RV_PAD) left = RV_PAD;
  menu.style.top = Math.round(top) + 'px';
  menu.style.left = Math.round(left) + 'px';
  menu.style.right = 'auto';                     /* 不清 right，会与 left 一起把盒子拉宽 */
}
```

调用点 = `toggleMenu()` 的**打开分支**，且必须在**摘掉 `[hidden]` 之后**（否则量到 0×0）：

```js
menu.removeAttribute('hidden');
menu.classList.add(POP_OPEN);
if (trigger) trigger.setAttribute('aria-expanded', 'true');
placeRv(menu, trigger);          /* ← 新增 */
```

CSS 侧只做两件事：把共用规则**拆成两条**，并给 `.td-rv-menu` 一个**静态兜底** `top: 83px`
（JS 未生效时的近似值；真位置一律由行内样式接管）。

**为什么否决了纯 CSS**（三条路都试过）：
1. 静态 `top: calc(44px + 40px * var(--ui-fs-ratio) + 6px)` —— 工具条高度确实是
   `min-height: calc(40px * var(--ui-fs-ratio))`，但标签栏高度来自**跨代资产** `browse.css`
   （写死 `height: 40px`、**实测 44**）⇒ 两个魔法数**来源不同**，且字号一缩放就脱节。
2. 「包含块换成 `.td-mod-bar` + `top: 100%`」—— 祖先 `.td-mod { overflow: hidden }` 会裁掉菜单
   （这正是当年改用 `.td-browse` 当参照的原因）。
3. 水平也做不到：三枚触发器的 x 各不相同，「各自对齐各自触发器」纯 CSS 表达不了。

**判据**（1440 / 清缓存 / 三枚全开）：

| 菜单 | dy | dxLeft | coversH | 行内值 |
|---|---|---|---|---|
| `.td-rv-scope-menu` | **+6.0** | **+0.0** | true | top 83 / left 12 |
| `.td-rv-opts` | **+6.0** | **−0.1** | true | top 82 / left 710 |
| `.td-commit-menu` | **+6.0** | −14.1 | true | top 84 / left 726 |
| `.td-mod-menu`（**回归**） | +6.5 | −118.0 | true | 仍是 CSS 的 42 / 64 ⇒ **未受影响** |

★ `.td-commit-menu` 的 `dxLeft = −14.1` 是 **clamp 生效**（菜单宽 168 > 按钮 84 ⇒ 右缘贴住面板右内边 4px），
**不是错位**。
★ **行内确实接管了**：`opts` 实测行内 `top: 82px` ≠ CSS 兜底 `83px`。

**窄栏降级**（`--av-browse-w: 315px`）：三枚均 `insideMod = true`（不被 `.td-mod{overflow:hidden}` 裁）、
`inPanel L/R = true`；opts 被 clamp 到 `left = 137`（= `313 − 172 − 4`）⇒ 贴住右内边。

**行为回归**（真机 / 真键盘 `press Escape` / 真鼠标）：

| 步骤 | 结果 |
|---|---|
| 打开 `.td-rv-opts` | `top 82 / left 710` ✓ |
| `press Escape` | 关闭 ✓ |
| **再次打开** | 位置**完全一致**（82 / 710）⇒ 内联重算幂等 ✓ |
| 点面板空白 | 关闭 ✓ |
| 打开 `.td-rv-scope-menu` → 点工具条 | 关闭 ✓ |
| 右键 `.td-diff-h` | `.td-ctxmenu` 落在指针处（`top 300 / left 900`）✓，Esc 关 ✓ |

### 第十拍 门禁 / 产物

幂等 ✓（`应用 0 项 / 跳过 3 项`；`apply107.py` 第二遍「已是目标态」）｜`check-syntax.py pages/*.html` **10/10**｜
`verify-design.py ./pages` 与 `vd-r107j.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜
`scan-flatten.py panel.css` 仍 **2 条**（本拍**不动字号**）｜
改动面 = `M pages/conversation.html`（`+2419 / −8` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍遗留）
+ `?? mg-work/r107/`。
产物 **934109 → 936625 字符（+2516；相对 HEAD +137394）**；UTF-8（LF 归一）**1029334** / 工作区 **1036446** /
LF `sha1 bc830fa56c0c`。
资产 `panel.css 43657`（CRLF）· `panel.js 52203`（LF）。探针 `ev/p107k_pos.js`（几何对照）+ `ev/p107k_narrow.js`
（越界判据）+ `probe107k{,1,2,3}.sh` + `shots107k.sh`；出图 `raw/k-*.png`。备份 `ev/bak10/`。
★ **体位**：本拍仍**未动** `_mods.html` / `browse.html` ⇒ 不必重跑 `splice107.py` / `make107.py`；
改序只剩 `part107/panel.{css,js}` → `ev/patch107k.py` → `apply107.py`（part 文件是**运行时读**的）。

## 十六、第十一拍（邵先生 2026-10-01 13:4x · 四条）

> 原文：
> 1、**「`td-selbar` 的图标和文字颜色默认应该是正文黑色」**
> 2、**「新右栏浏览器的输入框 `td-url-pill` 少了输入中电激活态效果」**
> 3、**「『调用 5 个工具』的这种数字动效实在是太慢，还以为没有数字呢」**
> 4、**「再调查一下 codex 官方原版有无缺少的功能，能落地的都补充」**

### 第十一拍 ① `.td-selbar` 图标与文字默认正文黑

**根因**：两枚按钮的类串是 `giencoder-btn giencoder-btn-text giencoder-btn-size-small`，
DS 的 `.giencoder-btn-text` 基类把文字色定成 `--color-primary-6` ⇒ 实测 `color = rgb(55, 112, 247)`。

**修法**（`panel.css` 第 15 节）：`.td-selbar .giencoder-btn { color: var(--color-text-1); }`
—— 特异性 (0,2,0) 且文档序在 DS 之后 ⇒ 必胜；SVG 走 `stroke="currentColor"`，跟着一起变、不必单独点。

| 量点 | 改前 | 改后 |
|---|---|---|
| 两枚按钮 `color` | `rgb(55, 112, 247)` | **`rgb(31, 31, 31)`**（= `--color-text-1`）|
| SVG `stroke` / `color` | 同上 | **同上（全为 `rgb(31,31,31)`）** |

### 第十一拍 ② `.td-url-pill` 补「输入中激活态」

**根因**：pill 只有 `background: --color-fill-2`，而 `input:focus { outline: none }`
⇒ 聚焦后**零视觉变化**（实测 shadow 恒 `none`、底色恒 `rgb(242,242,242)`）。

**修法**（第 16 节）—— 照 DS `.giencoder-input-wrapper:focus-within` 的口径，
但**用 `inset` 描边代替 `border`**（`border` 会把 26px 的胶囊撑高）：

```css
.td-url-pill { transition: background-color 120ms ease, box-shadow 120ms ease; }
.td-url-pill:focus-within {
  background: var(--color-bg-2);
  box-shadow: inset 0 0 0 1px var(--color-primary-6), 0 0 0 2px var(--color-primary-light-2);
}
.td-url-pill:focus-within > svg { color: var(--color-text-2); }
```

★ **取证踩坑**：第一次在 `focus()` 之后**同步**读 `getComputedStyle`，拿到的是**过渡起点**
（`rgba(0,0,0,0) 0px 0px 0px 0px inset`）⇒ 差点误判成「样式没生效」。
改成 `focus → 等 400ms → 读数 → blur → 等 400ms → 读数` 才拿到真值。

| 状态 | 底色 | `box-shadow` | `:focus-within` | 锁形图标 | pill 高 |
|---|---|---|---|---|---|
| 默认 | `rgb(242,242,242)` | `none` | false | `rgb(134,134,134)` | 26 |
| **聚焦** | **`rgb(255,255,255)`** | **`rgb(55,112,247) 0 0 0 1px inset, rgb(218,228,254) 0 0 0 2px`** | **true** | `rgb(78,78,78)` | **26（未变）**|
| 失焦 | `rgb(242,242,242)` | `none` | false | `rgb(134,134,134)` | 26 |

### 第十一拍 ③ 「调用 5 个工具」数字动效提速

**根因（两层）**：
1. 数字的 `animation-delay: calc(1.5s + var(--r93-ni)*55ms)` + `fill: both`
   ⇒ 延迟期停在 `from`（`opacity: 0`）⇒ **那 1.5 秒里数字位是空的**（`.r93-num` 是 `inline-block`，空位一直占着）。
2. 那 1.5s 是**为等骨架屏退场**：`.r93-sk` 是 `position:absolute; inset:0` + **不透明** `--color-bg-2` 底
   ⇒ **早于它退场的任何动效都白做**。

**改前真机时间线**（1440 / `performance.now()`）：骨架屏 **2012ms** 开始淡出 → **2326ms** 从 DOM 移除
→ 数字 **2493ms** 才首次可见（**整整 2.5 秒** —— 难怪「以为没有数字」）。

**修法 = 两边一起动**：
- `apply107.py` 的 `wire()`：骨架屏 `1100` → **`380`**（保留 `320`：CSS 那条 `transition: opacity .3s`
  走完正好 300ms，再早移除会跳一下）；
- `panel.css` 第 17 节：`animation-duration: 0.46s → 0.30s`、`animation-delay: 1.5s → calc(0.44s + ni*26ms)`
  —— **只覆写这两条长属性**，不动 `animation-name` / `fill-mode`。

**改后实测**：`tSkGone == tNumVisible`（空窗 **167ms → 0**）、
`numAnim = { delay: "0.44s", dur: "0.3s", fill: "both", name: "r93-num-in", text: "5" }`、
`numCount = 13`、`skStillInDom = false`、整体约 **1.66s**。

> ⚠ 探针 `tSkOut = null` / `late = 1` 是**起跑偏晚**的探针 artifact（`wait 4200` 在装轮询器之后才执行，
> 轮询器错过了早段），**不是产品问题** —— 判据取 `tSkGone` 与 `tNumVisible`。

### 第十一拍 ④ 对照 Codex 官方原版补缺（落地三件）

**调研结论**（官方 openai.com「Codex:全能型助手」+ 第三方教程汇总）：五入口 文件 / 侧边聊天 /
浏览器 / 审查 / 终端 + **摘要面板**（计划·来源·产物·摘要）；审查支持「本轮改动 ⇄ 整体分支改动」筛选、
行内评论、暂存/撤销、界面内 Commit/Push/PR、查看 PR 与评论、文件预览；浏览器可开本地或公网页、
**在渲染页面上直接标注**、**一键截图到剪贴板**、一次只开一页；终端与 Codex 共享工作目录、
**多标签终端**；**产物查看器**（PDF / 表格 / 文档 / 演示文稿）；另有 SSH 远程连接（alpha，**不在侧栏**）、
多窗口、系统托盘。

**对照我们右栏**（一~十拍已落地）：五模块 + 摘要 + 行内评论 + 暂存·撤销 + 统一⇄并排 +
自动换行 / 隐藏空白 / 词级差异 / 折叠未改动 + 对比范围三档 + 提交·推送·PR + 浏览器标注 + 终端
—— **已相当齐全**。**真正还缺且能落地**的只有三件：

> ⚠ 官方 SSH / 多窗口 / 系统托盘：**静态演示页落不了地 ⇒ 不做**；
> 「文件」模块不能编辑：**官方亦然 ⇒ 不动**。

#### ④-a 终端多标签（官方「多标签终端」）

- `_mods.html`：`.td-mod-term` 里补 `.td-term-tabs`（`role="tablist"`：`zsh` / `npm run dev` 两枚静态 +
  一枚 `+`），并把原 `.td-term` 正文**逐字**搬进 `[data-td-term-pane="t1"]`，另新增 `t2`（`git status -sb` 会话）。
- `panel.js`：把原来「一个 `term` 变量 + 闭包 `echo`」拆成 **`bindTerm(el)` 按块绑定**
  （`echo` 收进各自闭包；同一份 `CANNED` 表 + 同一套 `keydown` 分支 ⇒ 行为与改前逐字一致）；
  新增 `termPanes()` / `activeTerm()` / `showTerm(id, focus)` —— 标签只切 `hidden`、各块内容互不影响；
  `newTermTab()` 现场新建（新标签 = 空提示符）；右键菜单那条「新建终端标签」从「只弹 toast」
  **改成真新建**，并把**当前标签名**放进菜单标题。
- `panel.css` 第 18-① 节：标签条 `min-height 34`、标签 `h 22 / r 6`、激活态 `--color-fill-2` + 图标转主色；
  `+` 是同尺寸方形按钮。

**实测**（1440）：`tabsBar=true / tabsBarH=34`；切 `t2` → `visiblePanes=["t2"]`、
`activeName="npm run dev"`、`activeElement="td-term"`；点 `+` → `tabCount=3`、新标签「终端 3」激活、
`paneCount=3`；**t1 输出行数仍是 4、t2 是 3 —— 各块独立、原终端零回归**。

#### ④-b 浏览器「截图到剪贴板」（官方「一键截图到剪贴板」）

- `_mods.html`：地址栏「标注」与「缩放」之间补一枚 `[data-td-brw-act="shot"]`（相机图标）。
- `panel.js`：`BRW_TEXT` 加 `shot`；点击时先 `shotFlash()` 再 `say()`；`ctxForBrw()` 也补一条
  「截图到剪贴板」（与按钮走同一个入口）。
- `panel.css` 第 18-② 节：`.td-mod.td-brw { position: relative }` + `.td-brw.is-shot::after` 快门白闪
  **260ms**（⚠ `verify-design.py` 的 `CRAFT-ANIM` 规则会数 > 300ms 的动画 ⇒ **必须 ≤300**）。

★ **为什么闪整个模块、不闪 `.td-view`**：`.td-view` 自己是 `overflow:auto` 的滚动容器，
绝对定位子元素会**跟着内容滚走** ⇒ 滚动之后快门就闪不见了。

**实测**：按钮存在（`aria-label` / `title` 均为「截图到剪贴板」）；点击瞬间 `flashed=true`、
`animationName="td-shot-flash"`、`animationDuration="0.26s"`、toast = 「已复制截图到剪贴板（视觉演示）」；
400ms 后 `flashed=false`（自动回收）；★ **地址栏布局零扰动**：`.td-url` 高仍 **40**、`.td-url-pill` 高仍 **26**。

#### ④-c 产物预览层（官方「产物查看器」）

- `_mods.html`：`.td-mod.td-sum` 内补 `.td-sum-prev`（覆盖整块摘要；头部 = 图标 + 文件名 + 元信息 + 关闭；
  正文 = **文档骨架** `.td-pv-md`（h1 + 段落 + 标题 + 5 根占位条）/ **表格骨架** `.td-pv-sheet`
  （6 行 × 4 列，含表头）；页脚 = 「在系统打开」「关闭」）。
- `panel.js`：`prevShow(btn)` 从产物行取文件名与元信息，**按扩展名**（`.xlsx/.xls/.csv/.tsv`）选骨架，
  两套骨架靠 `[data-td-prev-kind]` 互斥；`prevHide()` 关闭；
  **Esc 裁决把预览层算作一层** —— 否则开着预览按 Esc 会把**整条侧栏**关掉（那是 `ctrl-conv.js` 在处理）。
- `panel.css` 第 18-③ 节：`.td-sum-prev { position: absolute; inset: 0; z-index: 6 }`；
  ⚠ 两套骨架**必须显式写 `[hidden] { display: none }`**（`.td-pv-md` 自己声明了 `display:flex`，
  会压过 UA 的 `[hidden]`）。

**实测**（1440）：点第 1 枚「预览」→ 预览层 `hidden=false`、名 `右栏复刻方案.md`、
元信息 `Markdown · 12 KB · 只读预览`、`mdHidden=false / xlsxHidden=true`、
**`prevBox == paneBox == [898, 798]`（完整覆盖）**、图标 SVG 已带过来；
点「关闭」→ `hidden=true`；再开 → **`press Escape` → 预览层关、`paneOpen=true`（侧栏没被误关）**；
点第 2 枚「预览」→ 名 `sidepanel-metrics.xlsx`、`mdHidden=true / xlsxHidden=false`（骨架正确切换）。

### 第十一拍 门禁 / 产物

幂等 ✓（`patch107l2.py` 第二遍「应用 0 项 / 跳过 3 项」；`apply107.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
`verify-design.py ./pages` 与 `vd-r107k.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）
⇒ **零新增**（三件新增物**一处渐变都没引**）｜
`scan-flatten.py panel.css` 仍 **2 条**（新增规则一律带 `var(--font-size-*)`）｜
改动面 = `M pages/conversation.html`（`+2806 / −12` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍遗留）
+ `?? mg-work/r107/`。
产物 **936625 → 958568 字符**（第十一拍合计 **+21943** = ①②③ 的 +3776 + ④ 的 +18167）；
UTF-8（LF 归一）**1055517 字节** ｜ 工作区字节（CRLF）**1063012** ｜ LF `sha1 5ce6b87f5150`；
`base.html` **472150 逐字节不变**。
资产 `panel.css 66757`（CRLF / 1090 行）· `panel.js 67591`（LF / 1335 行）· `browse.html 80284`（LF）·
`_mods.html 44246`（LF）。
探针 `ev/p107m.js` + `ev/probe107m.sh` → `ev/m-raw.log`；补丁 `ev/patch107l1.py`（①②③）+ `ev/patch107l2.py`（④）。
★ **体位**：本拍**首次动了 `_mods.html`** ⇒ 改序必须 `part107/_mods.html` → `ev/splice107.py`（重组
`browse.html`）→ `mg-work/r107/apply107.py`；⚠ **`browse.html` 是 splice 的产物、不是手改对象**
（手改会在下次 splice 时被冲掉）。
