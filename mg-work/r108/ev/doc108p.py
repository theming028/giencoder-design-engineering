# -*- coding: utf-8 -*-
u"""r108 第十四拍收尾：把「四条（zd-card 的 Git 三行接交互 / 删计划分区 / 目标按上游校准 / 折展与胶囊弹性动效）」
同步进记忆文档。

★ 代数体位：第十二 / 十三拍**未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 第十四拍同样是
  **就地返工**、**不另起 r109**、也**不另开一组记忆段** —— 全部并入 r108 既有段落
  （节标题由「十二 + 十三拍」升为「十二 + 十三 + 十四拍」）。

范围（同步「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行 + 顶部「最新一拍」块（整块换新、第十三拍降级为「上一拍」）
                                       + §一 状态段与 conversation 表行 + 二·h 标题 + mg-work/r108 表行
                                       + 二·h 段末追加「### 第十四拍」
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十三拍」→「共十四拍」+ 追加 ⑭ 要点行
  3) .workbuddy/memory/PLAYBOOK.md  —— 追加 P3.50（第十四拍 · 六条新教训）+ 附录「工作区 58 条速览」
                                       （★ 工作区 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 受 3000 字符限额，
                                        原 58 条铁律整表**迁到这里**存档，工作区那份只留索引 + 红线速览）
  4) .workbuddy/memory/MEMORY.md    —— r108 段追加第十四拍要点
  5) 两份 2026-10-01.md（仓库内 + 工作区）—— 追加第十四拍段

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换另给显式 mark。
★ 用法： python ev/doc108p.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc108p.py --check    # 只校验锚点命中数（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 6 份文件各自保留原行尾（rd/wr 处理）。
⚠ 正文里有 `86%` / `100%` 这类百分号 ⇒ **不用 `%` 格式化**，改用 `@WHEN@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 20:5x'

MEMDIR = os.path.join(REPO, '.workbuddy', 'memory')
HOF = os.path.join(MEMDIR, 'HANDOFF.md')
PAG = os.path.join(MEMDIR, 'PAGES.md')
PBK = os.path.join(MEMDIR, 'PLAYBOOK.md')
MEM = os.path.join(MEMDIR, 'MEMORY.md')
LOG_REPO = os.path.join(MEMDIR, '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def patch(p, steps, label):
    """steps = [(old, new, sub[, neg])]；old=None ⇒ 尾部追加。"""
    t, nl = rd(p)
    n0 = len(t)
    for step in steps:
        old, new, sub = step[0], step[1], step[2]
        neg = step[3] if len(step) > 3 else False
        new = new.replace(u'@WHEN@', WHEN)
        mark = new                       # ★ mark == new（唯一来源，不手抄）
        if CHECK:
            if old is not None and t.count(old) != 1:
                BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, t.count(old)))
            continue
        if neg:
            if old is not None and old not in t:
                SKIPPED.append(label + u' · ' + sub)
                continue
        elif mark and mark in t:
            SKIPPED.append(label + u' · ' + sub)
            continue
        if old is None:
            APPLIED.append(label + u' · ' + sub)
            t = t + new
            continue
        c = t.count(old)
        if c != 1:
            sys.exit(u'!! %s · %s：锚点命中 %d 次（应 1）\n   old=%r' % (label, sub, c, old[:200]))
        APPLIED.append(label + u' · ' + sub)
        t = t.replace(old, new, 1)
    if CHECK:
        print(u'   [check] %s' % os.path.relpath(p, WS))
        return
    if len(t) != n0:
        wr(p, t, nl)
    print(u'   %-44s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


def span(p, first_pre, last_pre, new, label, sub):
    """把「以 <first_pre> 起、以 <last_pre> 含」的**连续若干行**整段换掉。

    顶部的「最新一拍」块每轮都要整块换新 ⇒ 首尾各给一个行首前缀即可定位，
    比把 27 行老文本抄成正则稳（老文本会随每轮改动漂移）。
    mark = `new` 的首行。
    """
    t, nl = rd(p)
    mark = new.split(u'\n')[0]
    if mark and mark in t:
        SKIPPED.append(label + u' · ' + sub)
        print(u'   跳过  %s（已应用，文件未变）' % (label + u' · ' + sub))
        return
    lines = t.split(u'\n')
    i = j = -1
    for k, ln in enumerate(lines):
        if i < 0 and ln.startswith(first_pre):
            i = k
            continue
        if i >= 0 and ln.startswith(last_pre):
            j = k
            break
    if i < 0 or j < 0:
        sys.exit(u'!! %s：范围定位失败（i=%d j=%d）' % (label, i, j))
    if CHECK:
        print(u'   [check] %s → 行 %d..%d（%d 行）将被替换' % (label, i + 1, j + 1, j - i + 1))
        return
    lines[i:j + 1] = new.split(u'\n')
    t2 = u'\n'.join(lines)
    wr(p, t2, nl)
    APPLIED.append(label + u' · ' + sub)
    print(u'   %-44s %d -> %d（替换第 %d..%d 行）'
          % (os.path.relpath(p, WS), len(t), len(t2), i + 1, j + 1))


# ==================================================================== 公共文案
HOF_TOP = u"""> ⚠️ **最新一拍 = r108 第十四拍（四条 · ★★ 就地返工、未另起代数）** —— 第十二 / 十三拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> 本拍全部围绕 **`.zd-card`（ZCode 右上角任务信息面板）**，上游依据 = `zai-org/ZCode` 的 `ConversationStatusPanel.tsx` / `GitActionMenu.tsx` / `GitBranchSwitcher.tsx` / `collapsible.tsx`（已入库 `mg-work/r108/up/`）。
> ① **Git 三行接上交互 → 已做**：「更改」**复用右栏既有链路**（`[data-td-open-mod="review"]`.click() ⇒ `openTab('review')` ⇒ `ensureOpen()`），
>   实测 `browseOn false→true` / `tabs ["summary ✓"]→["summary","review ✓"]` / `reviewRect [792,93,639,798]`；
>   「分支」= `.zd-menu-branch`（5 项 + divider + 「创建并检出新分支...」），实测 `dy:6` / `inView:true` / 选中项蓝字 + ✓；
>   选完 ⇒ 行值 `main → feature/right-panel` + 轻提示「已切换到 feature/right-panel（视觉演示）」；
>   「提交或推送」= `.zd-menu-commit`（文案逐字取上游 `git.actionMenu.*`），与分支菜单**互斥**；点「提交并推送」⇒ 轻提示。
>   ★ **关闭三路径齐全**：外点（document）/ **Esc（window 捕获段，且只有真关掉了才 `preventDefault`）**/ 选完自动收起；
>     Esc 复测 ⇒ **`browseOn:false` + `zcardHidden:false`**（既没顺带关侧栏、也没关面板）。
> ② **删「计划」分区 → 已做**：`secs:3` / `secKinds ["git","goal","todo"]` / `planGone:true` / `secTitles ["Git 工具","目标","进程"]`。
> ③ **「目标」按上游逐项校准 → 已做**：未完成项图标换 **lucide `goal` 原路径**（3 条子路径，不再是自绘旗子）；
>   迭代行 `padding 8px`（上游 `px-2 py-2`）+ `radius 8px`（`rounded-lg`）+ `gap 8px`；标题 `line-height 16px`（`leading-4`）/ 13px；
>   trailing `·`；暂停钮 24×24（`size-6`）+ 内部 14×14（`size-3.5`）= lucide `pause`；分区头 32px（`h-8`）；
>   头部「收起为胶囊」= lucide `minimize-2`（不再是 chevron-up）。★ 面板里单挂体量类 **`.zd-ico`**（24 / 14），
>   **不动 `.td-browse-ico`**（那是右栏工具条的 28 / 16）。
>   ★★ **顺手补修一处边界缺陷**：`.zd-it-no`（绿圈序号）原 `width:16px; height:16px`，而本规则含 `var(--font-size-*)`
>   ⇒ `apply88b` 的 `scale_block` **只派生 `height`** ⇒ `--ui-fs` ≠ 14 时**变椭圆**（18 档实测 16 × 20.57）⇒ 两边都写
>   `calc(16px * var(--ui-fs-ratio))`（复测 **20.5625 × 20.5625**，`itNoRound:true`）。
> ④ **折展 + 面板⇄胶囊的弹性微动效 → 已做**：折展机制换成上游同款 **`grid-template-rows: 1fr ⇄ 0fr` + 内层透明度/位移/缩放**
>   （33 帧采样：`0 → 5.45 → 18.75 → … → 96`；`bodyDisplay` 恒 `grid`，**不再 `display:none` 硬切**；
>   `translate` 越过终点后回坐、`scale` 峰值 1.00195 = **spring 过冲**）；
>   面板⇄胶囊 = 出场「快速淡出 + 微缩上浮」（21 帧，约 180ms 处切件）+ 入场 `zd-panel-in` 回弹（`scale` 峰值 **1.0058** / `translate` 峰值 **+0.58px**）。
>   ⚠ **时长一律 ≤300ms**（`verify-design.py` 的 CRAFT-ANIM 上限）—— 「弹性」来自 `--transition-timing-function-spring`（`y1=1.56`）的过冲，不是靠拉长时长。
> ⑤ **边界与回归全绿**（`ev/probe108p2.sh`）：面板**不遮挡** `.r93-bar` 两枚按钮（`hitSelf:true`）/ 暗色档 **§19.x 零硬编码 hex** /
>   `--ui-fs=18` 杠杆逐档对（分区头 41.14 / 头部 46.28 / 标题行高 20.57）/ 窄档 620 `overflowRight:-17` /
>   **右栏四枚 `.td-rv-menu` 一族与扩员前逐字一致**（真鼠标 hover 底色仍 `rgb(242,242,242)`）。
> ★ **补丁 = `ev/patch108l3.py`**（772 行 / **27 项**，三层幂等 `0/27`，4/4 跨层标记兜底断言「全部存活 ✓」）。
> ★★ **本拍六条坑**见 PLAYBOOK **P3.50**（跨层 mark 契约 / `drop_re` 缺 `(?s)` / 多步共用 mark / CRAFT-ANIM 300ms 上限 / 探针三类假失败 / **主题类结论先取色**）。

> ▸ **上一拍 = r108 第十三拍（六条 · 就地返工，🚫 未提交）**：① `.td-sum-sec:hover` 边框深一档 / ② `.td-sum-h` 标题图标删净 /
> ③ `.td-diff-toggle` 图标正文色 13px / ④ `.td-sum-art` 整卡可点预览 / ⑤ **`task-detail.html`** 徽章 13px（独立血脉 `ev/patch108td.py`）/
> ⑥ **复刻 ZCode 右上角任务信息面板 `.zd-host#av-zd-status`**。要点与本拍同源，逐条见下方「### 第十三拍」。
> ▸ **再上一拍 = r108 第十二拍**：`.td-diff` 卡片化 + 「文件树」抽屉（独立类名 `td-tf*`）。"""

HOF_14 = u"""
### 第十四拍（r108 第三层补丁 · 四条 · @WHEN@ 邵先生 · 🚫 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **十三 ~ 十八节**；机制级教训见 PLAYBOOK **P3.50**。

**需求（逐字）**：

> 1、『zd-card』里的git工具的三个item（更改、分支、提交/推送）点击都无响应，需继续实现交互功能；
> 2、『zd-card』里的『计划』模块不需要，可以去掉；
> 3、『zd-card』里的『目标』的页面UI细节还原不到位，比如图标、间距等元素；
> 4、『zd-card』的折叠和展开都需要点弹性微动效。

**① 体位**：第十二 / 十三拍**未提交** ⇒ 按「未交付 ⇒ 就地返工」⇒ 本拍 = **第三层补丁** `ev/patch108l3.py`（**不另起 r109**）。
三层各带独立 `mark`：l1（6 步）/ l2（8 步）/ l3（**27 项**）；改序仍是下→上
`part108/{_mods.html,panel.css,panel.js}` → `ev/splice108.py` → `apply108.py`。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_mods.html`（59186 → **62859** 字符） | 删「计划」分区；三行接交互；图标全换 lucide 原路径；`.zd-cv` 14px；尾部追加 `.zd-menu-branch` / `.zd-menu-commit` / `.zd-toast`（★ 挂在 `.zd-mini` 之后、**`.zd-host` 内、`.zd-card` 外** —— 卡片 `overflow:hidden` 会裁掉 DS 弹层） |
| `part108/panel.css`（65976 → **70729** 字符 / 1488 行） | 就地改 6 处（分区头 28→32 / 折叠箭头 12→14 + spring / 删 `.zd-sec.is-closed .zd-sec-b{display:none}` / 迭代行内距圆角 hover / 标题行高 20→16 / **圆序号宽高同比**）+ 末尾 `19.1`/`19.2`/`19.3` 三小节 + **G1~G8 八处选择器组各加一行 `.zd-menu`**（收进第 1 节的 DS Dropdown 适配层） |
| `part108/panel.js`（64682 → **71160** 字符） | 末尾 IIFE 从「立刻 `hidden` 硬切」换成「Git 三行 + 两枚下拉（`closeZdMenus`/`toggleZdMenu`/`placeZdMenu`）+ `zdSwap` 弹性场次」 |
| `ev/p108p.js` | 主链多相位探针（16 相位；`foldStart`/`miniOutStart`/`miniInStart` **在同一 eval 内装 rAF 采样器再触发点击**） |
| `ev/probe108p2.sh` + `ev/p108p2.js` | **新建**：边界与回归探针（`bar`/`dark`/`fs`/`narrow`/`rv0`/`rvs`/`rvsh`/`rvc`/`rvo`/`rvall`/`final`） |
| `ev/shots108p.sh` + `raw/p-1440-*.png`（16 张） | **新建**：目视取证（含暗色 / `--ui-fs=18` / 窄档 620 三档） |
| `ev/pix.py` | **新建**：截图取色核验（防「目视误判明暗」） |
| `up/ConversationStatusPanel.tsx` + `up/conversationStatusPanelModel.ts` | **新建**：上游源码入库（权威依据） |

**③ 真机实测（1440）**

* 静态：`secs:3` / `planGone:true` / `menuCount:2`；`rows ["更改+566 −228","分支feature/right-panel","提交或推送"]`；
  目标两项 = 绿圈 `noRect [1112,335,16,16]` + lucide goal `icoPaths` 3 条 / `icoRect [1112,383,16,16]`；
  `it.pad "8px/8px/8px/8px"` / `radius 8px` / `titleLH 16px` / `titleFS 13px`；
  暂停钮 `[1364,299,24,24]` + svg 14×14；分区头 `32px` / `pad "0px 8px"` / `gap 6px`；折叠箭头 `14px` / `opacity 0`。
* 分支菜单：`rect [1223,252,192,225]` / `dy:6` / `inView:true` / `minW 168px` / `pad 6px` / 条目 `"5px 8px"` + `radius 4px`；
  选 `feature/right-panel` ⇒ `branchText` 更新 + `rowAria:"false"` + 轻提示。
* 提交菜单：`rect [1247,284,168,80]` / `dy:6` / 分支菜单 `hidden:true`（互斥）。
* Esc：两菜单 `hidden:true`，`browseOn:false` / `zcardHidden:false`。
* 折展：`foldStart/foldRead` 33 帧；`gridTemplateRows 0→…→96`；`translate` 过零点回坐；`scale 0.98→…→1.00195→1`；`bodyDisplay:"grid"`。
* 胶囊：出场 21 帧（`scale→0.934` / `translate→-6.58px` / 约 180ms 切件）；入场 39 帧（`maxScale 1.0058` / 回摆 `[1095,105,320,512]` / `settledScale:"none"`）。
* 边界：`[A]` 两枚顶栏按钮 `hitSelf:true`、`overlap:false`、`hexLeak:[]`；`[B]` 暗色 `card rgb(35,35,36)` / `menu rgb(95,95,96)` / **`hexLeak:[]`**；
  `[C]` `ratio "calc(18 / 14)"` / `secH 41.1406` / `headH 46.2812` / `itTitleLH 20.5714` / **`itNoRound:true`**；
  `[D]` 620 档 `overflowRight:-17` / `inView:true`；`[E]` 四枚 `.td-rv-menu` **逐字未变** + hover 底色 `rgb(242,242,242)` + `openCount:1`。

**④ 排掉的六处坑**（详见 PLAYBOOK **P3.50**）

1. ★★ **各层 `mark` 是「后一层必须替前一层保住」的契约** —— l3 的 `CSS_TAIL` 把 l2 的 `/* r108-l2 */` 覆盖掉 ⇒ 复跑 l2 判「第 19 节还没写过」而**把整节 CSS 又追加一份**（`19. 任务信息面板` 与 `.zd-card {` 各 2 处）⇒ 改成 `CSS_TAIL + '/* r108-l2 */\n'` **原样接回** + 收尾加跨层标记兜底断言。
2. **`drop_re` 的 `.*?` 缺 `(?s)`** ⇒ 「删『计划』分区」永远 0 命中、被静态判成「已应用」而**静默跳过** ⇒ 加 `(?s)` + 反判据（删完计数 = 3）。
3. **八处 `GROUP_EDITS` 共用同一个 mark** ⇒ 第一处落地后其余七处全被判「已应用」而**静默漏改** ⇒ 每处自带独立锚点行。
4. **`verify-design.py` 的 CRAFT-ANIM 上限 = 300ms** ⇒ 初稿 340/360ms 让 md5 从基线变 `bd9f423b…` ⇒ 全部压到 ≤300ms。
5. ★ **探针自身三类假失败**：`ev()` 裁 `tail -1` 把有用信息裁掉 / `S(el).color` 不判空（分支菜单无 `.td-mm-key`）/ rAF 末帧 `scale` 为 `none` ⇒ `lastScale` 误报 0。
6. ★★ **「暗色截图看起来是浅底」是假象** —— 取色实测 `rgb(35,35,36)` ⇒ 新增 `ev/pix.py`；**主题类结论先取色再下判断**。

**⑤ 产物与门禁**：`conversation.html` 995133 → **1009968 字符（+14835）**（对 `HEAD` 累计 +51400）；
LF bytes **1115013** / 工作区 bytes **1123344** / **8332 行** / LF `sha1_lf 73c9ccd93c3d`；
`git diff --numstat` = `855  19  pages/conversation.html`；`task-detail.html` **767836（本拍未动，仍 `7  0`）**；`base.html` **逐字节不变**。
代数核对：`r108-conv-css` / `r108-conv-js` 各 **1**，`r107/r106/r102-conv-*` **全 0**。
幂等 ✓（l1 全跳过 / l2 `0/8` / l3 **`0/27`** + 4/4 断言「全部存活 ✓」；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）｜
`scan-flatten.py part108/panel.css` **2 条**（`.td-mod-bar` / `.td-url` 基线）｜ `pages/gaps.log` 已 `git checkout --` 清理。

**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`
还要 **`git reset -q -- mg-work/r108/ev/bak1[34]/ mg-work/r108/ev/bak14b-panel.css`**；`mg-work/r108/raw/` 与 `mg-work/r108/up/` 照旧入库。
★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。
★ ★★ **l3 之后若再叠一层**：新层的 `CSS_TAIL` 必须把 `/* r108-l3 */` **也原样接回**（否则 l3 复跑整块重挂）。
"""

# ==================================================================== HANDOFF
HOF_STEPS = [
    (u'> 最后更新：2026-10-01 20:2x（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条（★ 复刻 ZCode 右上角任务信息面板）」** → 门禁四查全绿 + 真机实测（面板 cardRect [455,105,320,512] / 五组边界回归全绿）→ **🚫 未提交**）',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条（zd-card：Git 三行交互 / 删计划 / 目标按上游校准 / 折展与胶囊弹性动效）」** → 门禁四查全绿 + 真机实测（主链八组 + 边界五组全绿）→ **🚫 未提交**）',
     u'首行时间戳 → 第十四拍'),

    # §一 状态段
    (u'★★ **r108（第十二拍 + 第十三拍六条）＝本代新产物，🚫 未提交**（2026-10-01 20:2x，第十三拍）。工作区：\n**` M pages/conversation.html`（995133 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'★★ **r108（第十二 + 十三 + 十四拍）＝本代新产物，🚫 未提交**（@WHEN@，第十四拍）。工作区：\n**` M pages/conversation.html`（1009968 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'§一 状态段 → 第十四拍'),

    # conversation 表行
    (u'★ **r108 态（🚫 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）**；LF bytes 1096235 / 工作区 bytes 1105158 / **8066 行**；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 **十二 + 十三拍**见 `mg-work/r108/acceptance.md`（**十三节**，八 ~ 十二 = 第十三拍）',
     u'★ **r108 态（🚫 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）→ 1009968（第十四拍 +14835）**；LF bytes **1115013** / 工作区 bytes **1123344** / **8332 行** / LF `sha1_lf 73c9ccd93c3d`；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 **十二 + 十三 + 十四拍**见 `mg-work/r108/acceptance.md`（**十八节**，八 ~ 十二 = 第十三拍、十三 ~ 十八 = 第十四拍）',
     u'conversation 表行 → 第十四拍'),

    # mg-work/r108 表行
    (u'| `mg-work/r108/` | **🚫 未提交（第十二拍）**：`apply108.py`（**由 `ev/make108.py` 从 apply107 做 7 处精确替换生成**；GENS 六代、nav 沿用 `r106-nav-js`）/ `acceptance.md`（**七节**）/ **`part108/`**（只覆盖改过的三件：`_mods.html` 51798 → **59186** 字符 · `panel.css` → **65976** 字符 / 1387 行 · `panel.js` → **64682** 字符 / 1488 行；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）/ `ev/`',
     u'| `mg-work/r108/` | **🚫 未提交（第十二 + 十三 + 十四拍）**：`apply108.py`（**由 `ev/make108.py` 从 apply107 做 7 处精确替换生成**；GENS 六代、nav 沿用 `r106-nav-js`）/ `acceptance.md`（**十八节**）/ **`part108/`**（只覆盖改过的三件：`_mods.html` 51798 → 59186 → **62859** 字符 · `panel.css` → **70729** 字符 / 1488 行 · `panel.js` → **71160** 字符；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）/ **`up/`**（上游 `ConversationStatusPanel.tsx` + `conversationStatusPanelModel.ts`）/ `ev/`',
     u'mg-work/r108 表行 → 第十四拍'),

    (u'> 完整版见 `mg-work/r108/acceptance.md`（**七节**）；机制级教训见 PLAYBOOK **P3.48**；本页固定事实见 PAGES **P3.11i**。',
     u'> 完整版见 `mg-work/r108/acceptance.md`（**十八节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.50**；本页固定事实见 PAGES **P3.11i**。',
     u'二·h 引言行 → 第十四拍'),
]

PAG_STEPS = [
    (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十三拍**）',
     u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三 / 十四拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十四拍**）',
     u'P3.11i 标题 → 共十四拍'),

    (u'> **⑨ 全屏按钮图标随态切换（四角朝外 ⇄ 朝内，切 `<path d>`、不重建节点）/ 全屏态拖拽起点改读「实际渲染宽」（先停过渡再取几何）/ 拖拽事件改挂 `window` / 全屏态按下分栏条＝放弃全屏 / 收起侧栏也退全屏**',
     u'> **⑨ 全屏按钮图标随态切换（四角朝外 ⇄ 朝内，切 `<path d>`、不重建节点）/ 全屏态拖拽起点改读「实际渲染宽」（先停过渡再取几何）/ 拖拽事件改挂 `window` / 全屏态按下分栏条＝放弃全屏 / 收起侧栏也退全屏** ·\n'
     u'> **⑩ r108 第十二拍** `.td-diff` 独立成小卡片（描边 + 8px 圆角 + `gap:8px`）+「文件树」抽屉（`.td-tree` · `z-index:35` · 296px · **独立类名 `td-tf*`** · Esc 算一层）·\n'
     u'> **⑪ r108 第十三拍**（六条）：`.td-sum-sec:hover` 边框深一档 / `.td-sum-h` 标题图标删净 / `.td-diff-toggle` 图标正文色 13px / `.td-sum-art` 整卡可点预览 / **`task-detail.html`** 徽章 13px / **复刻 ZCode 右上角任务信息面板** ·\n'
     u'> **⑫ r108 第十四拍（四条 · 全部围绕 `.zd-card`）**：\n'
     u'> 　① **Git 三行接交互** —— 「更改」复用右栏链路（`[data-td-open-mod="review"]` ⇒ `openTab(\'review\')` ⇒ `ensureOpen()`）；\n'
     u'> 　　「分支」= `.zd-menu-branch`（`data-zd-br` 4 条 + divider + `data-zd-br-new`）→ 行值 `.zd-row-v[data-zd-branch]` 更新 + `.zd-toast` 轻提示；\n'
     u'> 　　「提交或推送」= `.zd-menu-commit`（`data-zd-commit` 2 条，文案取上游 `git.actionMenu.*`）；两枚**互斥**；\n'
     u'> 　　摆位 = 触发行下缘 + `ZD_GAP(6)`、右对齐卡片右缘（**`offsetWidth`** 而非 rect —— rect 会把入场 `scale(0.96)` 乘进去）；\n'
     u'> 　　关闭三路径 = 外点（document）+ **Esc（`window` 捕获段，只有真关掉了才 `preventDefault`）** + 选完自动收起；\n'
     u'> 　② **「计划」分区删净**（`secKinds ["git","goal","todo"]`，`list-checks` 图标由「进程」与胶囊复用）；\n'
     u'> 　③ **「目标」按上游校准** —— 图标 = lucide `goal`（未完成）/ 绿圈序号（已完成）/ `pause`（暂停钮）/ `minimize-2`（收起为胶囊）；\n'
     u'> 　　几何 = 迭代行 `padding 8px` + `radius 8px` + `gap 8px`、标题 `line-height 16px`（`leading-4`）、分区头 `32px`（`h-8`）、\n'
     u'> 　　`.zd-ico` = 24 / 14（**不动 `.td-browse-ico` 的 28 / 16**）、`.zd-cv` 14px、trailing `·` 分隔符；\n'
     u'> 　　★ **圆序号宽高同比**（本规则含字号 token ⇒ `scale_block` 只派生 `height` ⇒ 非默认字号下会成椭圆）；\n'
     u'> ④ **弹性微动效** —— 折展 = `grid-template-rows: 1fr ⇄ 0fr` + 内层 `opacity/translate/scale`（上游 `CollapsibleContent` 同款，**替掉 `display:none`**）；\n'
     u'> 　　面板 ⇄ 胶囊 = 出场「淡出 + 微缩上浮」+ 入场 `@keyframes zd-panel-in` 回弹；缓动 = `--transition-timing-function-spring`（`y1=1.56` ⇒ 过冲）；\n'
     u'> 　　⚠ **时长一律 ≤300ms**（`verify-design.py` CRAFT-ANIM 上限）—— 弹性靠过冲、不是靠拉长时长。',
     u'P3.11i 追加 ⑩⑪⑫ 三拍要点'),
]

PBK_APPEND = u"""

---

## P3.50 ★★ r108 第十四拍（四条 · @WHEN@ 邵先生）—— ★ 六条新教训

> 主题：`zd-card`（ZCode 右上角任务信息面板）的 ① Git 三行接交互 ② 删「计划」分区 ③ 「目标」按上游校准 ④ 折展与面板⇄胶囊弹性动效。
> 补丁 = `mg-work/r108/ev/patch108l3.py`（772 行 / 27 项）；完整实测见 `mg-work/r108/acceptance.md` 十三 ~ 十八节。

**① ★★★ 各层 `mark` 是「后一层必须替前一层保住」的契约（P3.39 / 硬规则 49 的姊妹条）**
* 症状：l3 的 `CSS_TAIL` 把 l2 的幂等标记 `/* r108-l2 */` **覆盖掉** ⇒ 紧接着复跑 `patch108l2.py` 时判「第 19 节还没写过」⇒
  **把整节 CSS 又追加了一份**（`panel.css` 涨到 78431 字符，`19. 任务信息面板` 与 `.zd-card {` 各出现 **2** 次）。
* ★ 配方：新一层的尾部插入一律写成 `CSS_TAIL + '<上一层的标记>\\n'`（**原样接回**），本层标记用新的；
  **收尾加一条跨层兜底断言**：N 个标记必须全部存活 + 目标小节不得重复出现，任一不满足即 `sys.exit`。
* ⚠ 症状的诡异之处：**l3 自己跑两遍是幂等的**（`0/27`），只有「回头复跑上一层」才会暴露 ⇒ 门禁里必须**三层都复跑一遍**。

**② ★★ `drop_re` 的 `.*?` 必须带 `(?s)`，且删除类改动要补「反判据」**
* 症状：「删『计划』分区」的正则里 `.*?` **不跨行** ⇒ 命中数恒 0 ⇒ 被静态判成「已应用」而**静默跳过**（脚本不报错）。
* ★ 配方：`(?s)` 打开 dotall；**并且**补一条「删完 `data-zd-sec="plan"` 不再命中 **且** `data-zd-sec=` 计数 = 3」的反判据，
  写盘前 `sys.exit`。⚠ 与 P3.39「删除类改动没有 mark ⇒ 判据改『模式不再命中』」配套 —— **「不再命中」本身也可能是「从来没命中」**。

**③ ★★ 多处替换共用同一 `mark` = 静默漏改**
* 症状：八处 `GROUP_EDITS`（给同一组选择器各加一行 `.zd-menu`）的 mark 都写成 `.zd-menu.giencoder-dropdown-popup {`
  ⇒ 第一处一落地，后七处**全被判「已应用」而跳过**（脚本照样报「跳过 N 项」，看不出漏）。
* ★ 配方：**每处自带独立的完整锚点行**作 mark（本站改成 4 元组 `(old, new, label, mark)`）；批量同构改动尤其要数一遍「应用数 == 预期处数」。

**④ ★★ `verify-design.py` 的 CRAFT-ANIM 上限 = 300ms**
* 症状：初稿写 `transition: grid-template-rows 340ms` + `animation: zd-panel-in 360ms` ⇒ 门禁 md5 从基线 `3dbf6543…`
  变成 `bd9f423b…`、汇总 76 → 78 条（**没有报错，只是清单变长**）。
* ★ 配方：所有动效时长 ≤ **300ms**；要「弹性」就换缓动曲线 —— 本站 DS 的 `--transition-timing-function-spring`
  是 `cubic-bezier(.34, 1.56, .64, 1)`，**`y1 = 1.56 ⇒ 天然过冲**（实测 `scale` 峰值 1.0058 / `translate` 峰值 +0.58px）。
  ⚠ 量弹性必须**在同一 `eval` 内装 rAF 采样器再触发**（点击与读数跨帧就只剩首末两帧）。

**⑤ ★ 探针自身的三类假失败（P3.25 补第 ⑥ 类）**
* ⓐ **包装函数里裁 `tail -1`** ⇒ 探针自身抛错时输出是「Error 行 + 栈行」两行，裁掉首行只剩
  `at <anonymous>:215:3`（栈指向 IIFE 收尾行，**完全无法定位**）⇒ 包装函数一律**全量输出**。
* ⓑ **`S(el).color` 不判空** —— 分支菜单没有 `.td-mm-key` ⇒ TypeError ⇒ 同 ⓐ 一起伪装成「探针坏了」。⇒ 加 `C()/BG()` 安全取值。
* ⓒ **`scale` 的 computed 值在无变换时是 `none`**（`parseFloat → NaN`）⇒ rAF 末帧落在入场类被摘掉之后就**误报 `lastScale 0`**
  ⇒ 过滤 NaN 并另报一个 `settledScale`（静止态 `"none"`），把「峰值过冲」与「终态」彻底分开。

**⑥ ★★★ 「主题类结论先取色、再下判断」**
* 症状：暗色档截图（`p-1440-dark.png` / `n-1440-zd-dark.png`）在预览器里**看着是浅灰底** ⇒ 差点误判「暗色没生效」。
* ★ 实测：`PIL` 取色 = **`rgb(35, 35, 36)` `#232324`（lum 35.3）** —— 主题一直是生效的，**是肉眼/预览器骗人**。
* ★ 配方：新增 `mg-work/r108/ev/pix.py`（<png> [x,y] …，输出 rgb / hex / lum / 深底浅底）；
  **任何「暗色 / 对比度 / 底色」结论都必须先取色**。⚠ 与 P3.25（探针假失败）同族，但这次骗人的是**眼睛**、不是工具。

---

## 附：工作区速览 58 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）

> ⚠ 工作区那份 `MEMORY.md` 受 **3000 字符**限额（超了会被截断注入 ⇒ 等于没写）⇒ 原 58 条整表**迁到本附录存档**，
> 工作区只保留「Windows 速记 + 红线速览 + 最近拍」。本附录 = 那 58 条的**压缩原文**（细节仍在各 P3.x 与 skill 里）。

1. 改页面走 `mg-work/rNN/applyNN.py`（净底 → 注入 ⇒ 重跑自愈）；跑两遍验幂等；断言只用「标签级精确增减」；**新增注释里不得出现被断言的 token**；回滚 `git checkout -- <页>`。
2. **未提交期返工 ⇒ 就地改原补丁**（判据 `git status` 仍 ` M`）；**已交付才新建 `rNN+1`**。★★★ 跨代沿用的宿主标记**不换名**；**改了的块必须换名**。
3. **改前先用 DOM 核实现状**（同名同构模块多页各一份）⇒ 不凭字面推断。
4. 组件复用走 `components/{slug}.json` 契约类 + 适配层（`rq-/kb-/td-/av-`）；**按钮一律挂 DS Button、禁自绘**；圆角 **large 8 / small 4**；DS 基类自带 1px 透明描边 ⇒ 凑整数宽内距减 1；变化态只写 `min-height`。
5. **禁硬编码 hex**；非 token 色进页面 `:root` 适配层并注明出处，**且在 `[giencoder-theme='dark']` 补回**；白底一律 `var(--color-bg-2)`。
6. 弹层开合唯一开关 **`.giencoder-popup-open`**；禁内联 `display`；幂等块 END **必须包住 `<script>`**。★★ 一个关闭器管多个浮窗时**搜索根取最近共同祖先**。
7. ★★ **DS 组件样式有「三份源」** ⇒ 改 DS = 3 源 + 9 页 + 契约，改完全仓 grep 零残留。
8. ★★ **幂等脚本别把自己注入的块一起 `unscale`**（永久损毁而「跑两遍 sha 不变」照样通过）⇒ `converge()` + 逐条断言注入内容。
9. ★★★ 全站字号杠杆 = **`--ui-fs`**（不是 `html{font-size}`）。凡声明 `line-height`/`height`/`min-height: calc(Npx * var(--ui-fs-ratio))` 的规则，**`font-size` 必须写 token**；无 token 档用**两段式**；自查 `ev/scan-flatten.py`，**判据看 `--ui-fs=18`**。
10. ★★ **「可选子部件」一律判空**（含探针侧）—— 否则 TypeError 冒泡 ⇒ **整页白屏但页签/导航正常**。
11. ★★ 拖拽的 `pointermove`/`pointerup` **挂 `window`** + `blur` 兜底；第一帧读**实际几何**；拖动中只改视觉、**松手才落盘**。
12. ★★ 给 DS 组件加子元素 = 一次几何再协商（先读容器 `display/gap/padding/box-sizing`）；内描边用 **`outline` 不用 `border`**。
13. ★ 小尺寸图标按渲染尺寸建 **1:1 网格**（`viewBox="0 0 N N"`，坐标取 x.5）；同一字形不同渲染尺寸各备一份。
14. ★★ 给 React 渲染的元素加新色 ⇒ 后置 CSS 两盲区（**尾风任意类**是构建期产物、**内联 `style` 优先级最高**）⇒ 只能「挂自定义类」或「改 React 源」。
15. ★★★ 设计稿导出图**「状态变体是叠放的」**；**导出 PNG 的绝对 y 不可当设计坐标**（容器 top 之差可信任）。★ **弹层尺寸要在过渡结束后量**。
16. ★★★ 导出图标可能带 `transform="matrix(...)"` ⇒ 先 `getBBox()` 交叉验证；判图标坏源用**隔离测试页**。
17. ★★ 字号机制层 `body .cls` 会反噬任意值工具类 ⇒ size 类行高加 `:not([class*="leading-"])`；给 `leading-[Npx]` 补**同特异性**规则、写在 text-\* 之后。
18. ★★ 新开一页 = **由源页净底重建** + 全页 `ROUTE` 各 +1 条；复用外壳真组件 = **纯 CSS 改视觉顺序**。
19. ★★★ **用户只给「一个数」⇒ 反查那个数，别按他给的类名字面改**（数字比类名可信）：量他点名的类**证伪** → 全页扫该值 ±30px → 全仓 grep 字面值 → 写**溢出判据**。⚠ 改动在他点名的分辨率下不可见时必须明说。
20. ★★ 新加模块容器：① 类名不得与内部件**重名**（重名 ⇒ `querySelector` 取到外层、`tabIndex=-1`、**不报错**）；② 绝对定位子件前**先确认容器 `position`**。
21. ★ 验「按键 → 页面响应」只用 `agent-browser press`（真按键）；`keyboard type`/`focus` 不触发 `keydown`；先量 `activeElement`。
22. ★★ 「组装件 + 生成器」双层产物只能**下→上**改；**禁手改 `applyNN.py`**。⚠ `--revert` 是**整代回滚** ⇒ 只退本代用 `git checkout -- <页>`；别重跑上一代。
23. ★ Esc 分层：挂 **`window` 捕获段**；「这一下该关哪一层」必须自己写在处理器里，且**只有真关掉了才 `preventDefault`**。
24. ★★ 互斥态的两条 `display` 规则**特异性必须错开**（同特异性只靠文档序 ⇒ 后写者永久胜出、「点了没反应且不报错」）；验证用四象限实测。
25. ★★ **探针自身的假失败**：① 选择器层级错；② 先点后读必须同一次 `eval`；③ 点在 `display:none` 上静默失败；④ 过渡中取值；⑤ 截图框错目标；⑥ `scale` 静止时是 `none`（见 P3.50 ⑤）。
26. ★★★ 往老页面新挂「本来带全局适配层的 DS 类」⇒ **先查页面级通配规则**；⚠ 最坑的是**除位置外一切属性都「看起来对」** ⇒ **必须量 `getBoundingClientRect()`**。
27. ★★★ 有 `!important` 定位规则的页面上，JS 定位浮层一律走**「自定义属性 + 规则」**；★ 自定义属性**不是声明、不被 `!important` 压制** = 天然穿透通道。
28. ★★★ 给 DS 组件写「兜底声明」= **基态与 `:hover` 写在同一块、基态在前**；★ 判据 = 真鼠标 hover 后读 `backgroundColor`。
29. ★★★ **「挂错组件族」比「没挂组件」难发现**：① 读 `components/*.json` 的 `summary/variants/states/mapsFrom`，**别被类名骗**；② 「DS 有没有某组件」**查页面内联 bundle**；③ 取「与本页同页」的口径。
30. ★★ 换组件族 = 一次连锁再协商：① 页面级通配自行失效；② DS 弹层 **entry 动画**播完 `opacity` 打回 0 ⇒ 显式 `animation:none`；③ 选中态重新协商。
31. ★ 迁移脚本的「零残留」自检要**剥掉 CSS 注释再查**。
32. ★★★ 「这段文字框选不到」先查它是不是 **`::after` 的 `content`** ⇒ 隔离对照一比即定（对照物别用 `<textarea>`）。修法 = `content:none` + 注入真节点（React 宿主配 `MutationObserver`）。
33. ★★ 行内 `style` 写死的尺寸只有 `!important` 压得住；「定高 → 自适应」时竖内距要「单行态完全等价」。
34. ★★ 「全局去掉某词」先分类：① 渲染成文字必改；② 外链 `href` 不改；③ 设计来源注释保留。
35. ★★ 先判**节点从哪来**（静态 HTML vs JS 现场生成）⇒ 一段 CSS 把两类一起 `display:none`；能纯 CSS 就别写 JS。
36. ★★ 「统一某属性」要分清**本代样式 vs 跨代移植件**；判据覆盖整棵子树。
37. ★★ 「全局出省略号」分三类：单行截断（四件缺一不可）/ 代码终端折行 / 多行正文不截。⚠ flex 里裸文本是**匿名 flex 项**。
38. ★★★ 元素「居中」改不动 ⇒ 先查**谁在管这个 `width`**（多半是页面级 `!important`，正解常是 `text-align:center`）。
39. ★★ 幂等补丁的 mark 必须是「只有改后才存在」的串。★★ **「变短」的替换天然不满足 ⇒ 必须用反判据**。
40. ★★ 写进注释的「实测结论」必须来自**截图/取值**。
41. ★★ 改跨代移植件 ⇒ 本代放**同名覆盖件**（`PART_DIRS` 顺序回退，头部写明来源与差异点）。
42. ★★ 别用 `MutationObserver` 观察**后插节点**的父级；「独占态」**退出路径要列全**、退出用 silent 变体。
43. ★★ 浮层的锚点是**触发器的实际几何**。三规矩：摘 `[hidden]` 后再量 / 量尺寸用 `offsetWidth` / 写行内 `left` 必须同时 `right:'auto'`。
44. ★★ 别用静态 `top: calc(...)` 代替现场摆位；clamp 到容器内边 = 天然窄栏降级。
45. ★★ 动效延迟若在「等某个遮罩退场」⇒ 提速必须**两边一起改**；量 `transition` 必须等过渡走完。
46. ★★ 覆盖层别放进滚动容器；给自带 `display` 的类加 `[hidden]` **必须显式写规则**。
47. ★ DS `-text` 按钮默认主色（要正文黑得显式 `color: var(--color-text-1)`）；DS 输入框激活态用 `inset` 描边。★ 「有入口但只弹 toast、没有视觉」= **真缺口**。
48. ★★ 交付 = **两次提交 + 两次 push**；⚠ `git add -A` 后要 `git reset -- <rNN>/ev/bak*/`；`raw/*.png` 已被 `.gitignore` 屏蔽。
49. ★★★ 同步文档时**「mark 一律 = new」是硬规则**；★ 新一层必须**替上一层保住 `/* rNN-lN */` 标记**（见 P3.50 ①）。
50. ★★★ 给既有控制器**加同构控件 ⇒ 一律换独立类名**；判据 = 操作新件后老模块「选中项/行数/折叠数」**一字未变**（先数 `.cls` 匹配数 > 1 = 撞车）。
51. ★★ **覆盖层会挡住它自己的触发器**；⚠ 别写 `q() || fn().click()` 短路表达式。
52. ★★★ **新浮层必须避开「固定高工具条」，探针先做 `elementFromPoint` 自检**；容器 `pointer-events:none` + 只有卡片 `auto`。
53. ★★ **回填式补丁的锚点要「保留锚点自身的 token」**（整体替换 `'</style><script …>'` 会生成 `</style></style>`）；判据 `count('</style></style>') == 0`。
54. ★★ **注释里出现被 `count()` 断言的裸 token 会绊倒自己的守卫** ⇒ 守卫用带引号的属性形式或在注释里改写 token。
55. ★★ **覆盖层的截图目标别选「它所属的布局容器」**（会被切在画面外）⇒ 选覆盖层自身或父容器。
56. ★★★ **各层 `mark` 是「后一层必须替前一层保住」的契约**（= 49 姊妹条）；跨层兜底断言「N 个标记全存活 + 目标节不得重复」。
57. ★★ **多处替换共用同一 `mark` = 静默漏改**；★ `drop_re` 的 `.*?` **必须带 `(?s)`**（否则跨行锚点永远 0 命中而静默跳过）+ 补反判据。
58. ★★★ **「主题类结论」先取色再下判断**（`ev/pix.py`）；⚠ 动效时长一律 **≤300ms**（CRAFT-ANIM 上限），「弹性」靠缓动曲线过冲（spring `y1=1.56`）而非拉长时长。
"""

MEM_STEPS = [
    (u'> ★★ **新增定论见 PLAYBOOK P3.49**（四条：固定高工具条遮挡 / 注释绊倒守卫 / 锚点 token 回填 / 截图切掉覆盖层）；逐条实测见 **`mg-work/r108/acceptance.md` 八 ~ 十二节**（共十三节）。',
     u'> ★★ **新增定论见 PLAYBOOK P3.49**（四条：固定高工具条遮挡 / 注释绊倒守卫 / 锚点 token 回填 / 截图切掉覆盖层）；逐条实测见 **`mg-work/r108/acceptance.md` 八 ~ 十二节**（共十三节）。\n'
     u'>\n'
     u'> **★ r108 第十四拍（@WHEN@ · 四条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二 / 十三拍**未提交** ⇒ 同上规则，本拍 = **第三层补丁** `ev/patch108l3.py`（772 行 / **27 项**），全部围绕 **`.zd-card`**。\n'
     u'> **四条** = ① **Git 三行接交互**（「更改」复用右栏链路 `[data-td-open-mod="review"]` ⇒ `openTab(\'review\')`；「分支」= `.zd-menu-branch` 5 项 + 行值 `.zd-row-v[data-zd-branch]` 更新 + `.zd-toast` 轻提示；「提交或推送」= `.zd-menu-commit` 2 项，两枚互斥；摆位 = 触发行下缘 + 6px、右对齐卡片右缘、**用 `offsetWidth`**；关闭三路径 = 外点 + **Esc（`window` 捕获段）** + 选完收起）；\n'
     u'> ② **删「计划」分区**（`secKinds ["git","goal","todo"]`）；③ **「目标」按上游校准**（lucide `goal` / 绿圈序号 / `pause`(24+14) / `minimize-2` / `padding 8px` + `radius 8px` + `leading-4` + `h-8 32px` + trailing `·`；★ **圆序号宽高同比** —— 本规则含字号 token ⇒ `scale_block` 只派生 `height` ⇒ 非默认字号下会成椭圆）；\n'
     u'> ④ **弹性微动效**（折展 = `grid-template-rows: 1fr ⇄ 0fr` + 内层 `opacity/translate/scale`，**替掉 `display:none`**；面板 ⇄ 胶囊 = 出场微缩上浮 + 入场 `zd-panel-in` 回弹；缓动 = `--transition-timing-function-spring`，**时长一律 ≤300ms**）。\n'
     u'> **六条坑** = **P3.50**（① 各层 `mark` 是「后一层替前一层保住」的契约 ② `drop_re` 的 `.*?` 必须 `(?s)` + 反判据 ③ 多处共用同一 mark = 静默漏改 ④ CRAFT-ANIM 300ms 上限 ⑤ 探针三类假失败 ⑥ **主题类结论先取色**）。\n'
     u'> **产物**：`conversation.html` → **1009968 字符**（+14835；对 `HEAD` 累计 +51400；`855 / 19` 行）、`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**。\n'
     u'> ⚠ **工作区 `MEMORY.md` 受 3000 字符限额** ⇒ 原 58 条铁律整表已迁入 PLAYBOOK 附录「工作区速览 58 条」。',
     u'MEMORY r108 段 → 第十四拍'),
]

LOG = u"""

---

## r108 · 第十四拍（四条 · 就地返工 · @WHEN@ 邵先生）—— 🚫 未提交

**需求（逐字）**：1、『zd-card』里的git工具的三个item（更改、分支、提交/推送）点击都无响应，需继续实现交互功能；
2、『zd-card』里的『计划』模块不需要，可以去掉；3、『zd-card』里的『目标』的页面UI细节还原不到位，比如图标、间距等元素；
4、『zd-card』的折叠和展开都需要点弹性微动效。

**体位**：第十二 / 十三拍未提交 ⇒ 就地返工 ⇒ 本拍 = **第三层补丁** `ev/patch108l3.py`（772 行 / **27 项**）。
改序仍是 `part108/{_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`。
上游依据：`zai-org/ZCode` 的 `ConversationStatusPanel.tsx` / `GitActionMenu.tsx` / `GitBranchSwitcher.tsx` / `collapsible.tsx`
（前两份已入库 `mg-work/r108/up/`），图标取 `lucide-static@1.49.0` 原路径。

**落地**：① Git 三行 —— 「更改」复用右栏链路（`browseOn false→true` / `tabs ["summary","review ✓"]` / `reviewRect [792,93,639,798]`）；
「分支」`.zd-menu-branch`（`dy:6` / `inView:true` / `minW 168` / 条目 `"5px 8px"` + `radius 4px`；选完 ⇒ 行值更新 + 轻提示）；
「提交或推送」`.zd-menu-commit`（两项，与分支菜单互斥）；**Esc 关层不误关侧栏/面板**（`browseOn:false` / `zcardHidden:false`）。
② 删「计划」⇒ `secs:3` / `planGone:true`。③ 「目标」⇒ lucide `goal`（3 条子路径）/ 绿圈序号 / `pause` 24+14 / `minimize-2` /
`pad "8px/8px/8px/8px"` + `radius 8px` + `titleLH 16px` + 分区头 `32px` + trailing `·`。
④ 折展 = `grid-template-rows` 1fr ⇄ 0fr（33 帧采样 `0→5.45→…→96`，`bodyDisplay` 恒 `grid`；`translate`/`scale` 过冲）；
面板 ⇄ 胶囊 = 出场 21 帧（`scale→0.934`）+ 入场 39 帧（`maxScale 1.0058`）；**全部 ≤300ms**。

**排掉的六处坑**（PLAYBOOK **P3.50**）：① 跨层 `mark` 契约（l3 覆盖 l2 标记 ⇒ l2 复跑整节重挂）；
② `drop_re` 缺 `(?s)`（跨行锚点永远 0 命中而静默跳过）；③ 八处 `GROUP_EDITS` 共用 mark ⇒ 静默漏改；
④ `verify-design.py` CRAFT-ANIM **300ms 上限**；⑤ 探针三类假失败（`tail -1` / `S(el)` 不判空 / `scale=none` 误报 0）；
⑥ **「暗色截图看着浅底」是假象** —— 取色实测 `rgb(35,35,36)` ⇒ 新增 `ev/pix.py`。

**探针**：`ev/p108p.js` + `probe108p.sh` → `p-raw.log`（13520 字节，八组全绿）；
`ev/p108p2.js` + `probe108p2.sh` → `p2-raw.log`（8777 字节，五组全绿：顶栏不被遮挡 / 暗色零 hex / `--ui-fs=18` / 窄档 620 / 右栏四枚下拉回归）。
**截图** `ev/shots108p.sh` → `raw/p-1440-*.png`（16 张，含暗色 / `--ui-fs=18` / 窄档三档）。

**门禁**：三层幂等（l1 全跳过 / l2 `0/8` / l3 **`0/27`** + 4/4 跨层断言「全部存活 ✓」）/ `apply108.py` 第二遍「已是目标态」/
`check-syntax.py pages/*.html` **10/10** / `verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）/
`scan-flatten.py part108/panel.css` **2 条**（基线）/ `pages/gaps.log` 已 `git checkout --` 清理。
**产物**：`conversation.html` 995133 → **1009968 字符（+14835）**（`git diff --numstat` = `855  19`）；对 `HEAD` 累计 **+51400**；
LF bytes **1115013** / 工作区 bytes **1123344** / **8332 行** / LF `sha1_lf 73c9ccd93c3d`；
`task-detail.html` **767836（本拍未动）**；`base.html` **逐字节不变**；代数核对 `r108-conv-css` / `r108-conv-js` 各 1、`r107/r106/r102-conv-*` 全 0。
**验收** `mg-work/r108/acceptance.md` **十三 ~ 十八节**；**记忆同步** `ev/doc108p.py`（本文件）。🚫 未 commit / 未 push。
"""


def main():
    print(u'=== 1/6 HANDOFF.md ===')
    span(HOF, u'> ⚠️ **最新一拍 = r108 第十三拍', u'>   复测两枚按钮均',
         HOF_TOP, u'HANDOFF', u'顶部「最新一拍」块整块换新（第十三拍降级为「上一拍」）')
    patch(HOF, HOF_STEPS, u'HANDOFF')
    # 二·h 段末追加「### 第十四拍」（anchor = 段末那两行交接语）
    patch(HOF, [(
        u'**⑦ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话；届时 `git reset -q -- mg-work/r107/ev/bak*`；`raw/` 照旧入库）。\n'
        u'★ r108 仍是**未交付的工作代** ⇒ 若还要改**会话详情页 / 右栏 / 任务详情页**，**继续在 `mg-work/r108/` 就地返工**；\n'
        u'**不要**新建 r109、**不要**回头改 `apply107.py`。\n',
        u'**⑦ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话；届时 `git reset -q -- mg-work/r107/ev/bak*`；`raw/` 照旧入库）。\n'
        u'★ r108 仍是**未交付的工作代** ⇒ 若还要改**会话详情页 / 右栏 / 任务详情页**，**继续在 `mg-work/r108/` 就地返工**；\n'
        u'**不要**新建 r109、**不要**回头改 `apply107.py`。\n' + HOF_14,
        u'二·h 段末追加「### 第十四拍」')], u'HANDOFF')

    print(u'=== 2/6 PAGES.md ===')
    patch(PAG, PAG_STEPS, u'PAGES')

    print(u'=== 3/6 PLAYBOOK.md ===')
    patch(PBK, [(None, PBK_APPEND, u'追加 P3.50 + 附录「工作区速览 58 条」')], u'PLAYBOOK')

    print(u'=== 4/6 MEMORY.md ===')
    patch(MEM, MEM_STEPS, u'MEMORY')

    print(u'=== 5/6 log-repo ===')
    patch(LOG_REPO, [(None, LOG, u'追加第十四拍段')], u'log-repo')

    print(u'=== 6/6 log-ws ===')
    patch(LOG_WS, [(None, LOG, u'追加第十四拍段')], u'log-ws')

    print()
    if CHECK:
        print(u'--check 完成：锚点异常 %d 处' % len(BAD))
        for b in BAD:
            print(u'   !! ' + b)
        return 1 if BAD else 0
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print(u'   跳过  %s' % s)
    return 0


if __name__ == '__main__':
    sys.exit(main())
