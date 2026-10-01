# -*- coding: utf-8 -*-
u"""r108 第十三拍收尾：把「六条（①②③④⑤ + ★ 复刻 ZCode 右上角任务信息面板）」同步进记忆文档。

★ 代数体位：第十二拍**未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 本拍是**就地返工**，
  **不另起 r109**、也**不另开一组记忆段** —— 全部并入 r108 既有段落（节标题从「十二拍」升为「十二 + 十三拍」）。

范围（同步的是「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md      —— 首行 + 顶部块（新拍插在第十二拍块之前、老块降级为「上一拍」）
                                          + 顺手修掉首部重复行 + 第一节 + conversation 表行 + mg-work/r108 表行
                                          + 二·h 节标题与节末追加 + 第七节现状
  2) .workbuddy/memory/PAGES.md        —— P3.11i 标题「共十二拍」→「共十三拍」+ ⑬ 要点 + 结构图补 .zd-host
                                          + 固定事实表增 5 行 + 必看清单增 20/21/22
  3) .workbuddy/memory/PLAYBOOK.md     —— 追加 P3.49（第十三拍 · 四条新教训）
  4) .workbuddy/memory/MEMORY.md       —— r108 段标题升为「十二 / 十三拍」+ 段末追加第十三拍要点
  5) 两份当日日志 2026-10-01.md（仓库内 + 工作区）—— 追加 r108 第十三拍段

★ 幂等设计（照 doc108n.py）：**mark 一律 = new**（`new` 天然只可能「改后才存在」）。
  步骤 = 3 元组 `(old, new, sub)`；`old=None` 表示尾部追加。
★ 与 doc108n.py 的差异：本脚本**不用 `%` 格式化**（正文里有大量 `86%` / `100%`），改用 `@WHEN@` 占位符替换。
用法： python ev/doc108o.py            # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
      python ev/doc108o.py --check    # 只校验锚点命中数（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 5 份文件各自保留原行尾（rd/wr 处理）。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 20:2x'

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def patch(p, steps, label):
    """steps = [(old, new, sub[, neg])]；old=None ⇒ 尾部追加。

    ★ neg=False（默认）：判据 = `new in t`（new 天然只可能「改后才存在」）⇒ 命中即「已应用」。
    ★★ neg=True（**「变短」的替换专用**）：当 new 是 old 的**子串**时（本站 = 删掉一行重复文案），
       `new in t` 在**改前就已为真** ⇒ 通用判据必然误判「已应用」；此路必须**反着判** = `old not in t` 才算已应用。
    """
    t, nl = rd(p)
    n0 = len(t)
    for step in steps:
        old, new, sub = step[0], step[1], step[2]
        neg = step[3] if len(step) > 3 else False
        new = new.replace(u'@WHEN@', WHEN).replace(u'@BLOCK@', R108O_BLOCK).replace(u'@2H@', R108O_2H)
        mark = new                       # ★ mark == new（唯一来源，不手抄）
        if CHECK:
            if old is not None and t.count(old) != 1:
                BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, t.count(old)))
            continue
        if neg:
            if old is not None and old not in t:   # ★ 反判据：老文本已消失 ⇒ 已应用
                SKIPPED.append(label + u' · ' + sub)
                continue
        elif mark and mark in t:
            SKIPPED.append(label + u' · ' + sub)
            continue
        if old is None:                  # 尾部追加
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
    print(u'   %-46s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


# ============================================================ 公共文案
R108O_BLOCK = u"""> ⚠️ **最新一拍 = r108 第十三拍（六条 · ★★ 就地返工、未另起代数）** —— 第十二拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> ① **`.td-sum-sec` hover 边框加深一级 → 已做**：`.td-sum-sec:hover { border-color: var(--color-border-2) }`；
>   基态 `rgb(242,242,242)`（border-1）→ hover **`rgb(229,229,229)`**（border-2 = **正好深一档**）；实测 `secHover:true`、rect 不动。
> ② **`.td-sum-h` 标题前的图标全去掉 → 已做**：4 处 `<svg>` 整段删净（`expect=4`）+ 清掉 `.td-sum-h svg` 死规则；
>   实测 `sumHSvg:0` / 文字 `["摘要","计划","来源","产物"]`。
> ③ **`.td-diff-toggle` 图标改正文色 + 13px → 已做**：`.td-diff-cv { width:13px; height:13px; color: var(--color-text-1) }`
>   （原 `--color-text-3` → 正文色）；实测可见几何 `rect [813,156,13,13]` / `color rgb(31,31,31)`；**第十二拍的卡片化没被带坏**（首卡 `[800,142,623,299]` / 8px / `rgb(229,229,229)`）。
> ④ **`.td-sum-art` 整卡可点预览 → 已做**：`data-td-art` 从内部「预览」按钮**上移到卡片本体**（2 处）+ `cursor:pointer`；
>   实测点「图标区」（而非按钮）即开预览层（`pvName:"右栏复刻方案.md"`）；按钮入口保留（`artBtnHasData:false` / `artCursor:"pointer"`）。
> ⑤ **任务详情页 `.giencoder-badge-status-text` 字号 → 13px → 已做**（★ **另一页 / 另一条血脉**）：
>   ★★ 关键发现 —— 文字节点**自己不声明字号**（继承），真源在父级 `.giencoder-badge-status{font-size:var(--font-size-body-3)}`（14px）
>   ⇒ 给**本页**补 `.giencoder-badge-status-text { font-size: var(--font-size-body-2) }`（13px）即可、
>   **无需特异性竞争、不动 DS 源**。落点 = `<style id="r108-td-css">`（插在 `</style>` 与 `<script id="r81-ws-js">` 之间）。
> ⑥ **★★★ 复刻 ZCode 右上角任务信息面板 → 已做**（本拍最大件）：上游 = **`zai-org/ZCode`**（Apache-2.0，2026-09-24 开源，7272 stars，default `main`），
>   权威依据 = `packages/ui/src/v4/ConversationStatusPanel.tsx`（2085 行）+ `conversationStatusPanelModel.ts`（385 行）
>   + `i18n/locales/zh-CN.ts`（6497 行；文案逐字取 `chat.statusPanel.*` / `chat.summaryPanel.*`）。
>   面板 = `.zd-host#av-zd-status`（`pointer-events:none`）+ `.zd-card`（`pointer-events:auto`）：四分区
>   `git`「Git 工具」/ `goal`「目标」/ `plan`「计划」/ `todo`「进程」；trailing `+566 −228` / `2 分 18 秒` / `3/5`；
>   行 = `更改 +566 −228` / `分支 main` / `提交 / 推送` / `右栏复刻方案.md`；目标两条迭代 `3/3` `3/4`；待办 5 条（3 done / 1 doing / 1 todo）；
>   折叠 = 分区头 `classList.toggle('is-closed')`（**不写内联 display**）；面板 ⇄ 胶囊 = `hidden` 属性互斥（胶囊文案「进程 3/5」）。
>   实测：`hostInMain:true` / **`cardRect [455,105,320,512]`** / `hostPE:"none"` / `panelRightGap:16` / `panelTopGap:57`；
>   折叠 ⇒ 卡高 **512 → 503**；收胶囊 ⇒ `miniRect [672,105,103,32]`；摊回 ⇒ **保留折叠态**。
> ★★★ **`.zd-host` 的 top 必须是 44px（不是 0）** —— `<main>` 顶部有 `.r93-bar`（`position:absolute; height:44px; z-index:10`，r106 的**固定档**），
>   右上角「全屏 / 打开侧栏」两枚按钮就在里面；面板从 `top:0` 起排会**把它盖住**
>   （实测 `elementFromPoint` 命中的是**面板自己的 `.zd-acts`**）⇒ 改 `top:44px` + `padding-top:12px`；
>   复测两枚按钮均 **`hitSelf:true`**、`zdTop:93`。
> ★ 暗色档 / **`--ui-fs=18` 杠杆** / 窄档 620 三组回归全绿（头部 36→46、分区头 28→36、卡 `[320,512]` 没被压平）。
> ★ **门禁四件套（在 top 修正之后复跑）全绿**：幂等 ✓（`patch108l2.py` 第二遍「**应用 0 / 跳过 8**」、`patch108td.py`「跳过」、`apply108.py`「已是目标态」）｜
>   `check-syntax.py pages/*.html` **10/10**｜`verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）｜
>   `scan-flatten.py part108/panel.css` 仍 **2 条**（`.td-mod-bar` / `.td-url`）。
> **产物**：`conversation.html` 978614 → **995133 字符（+16519）**（`git diff` **+582 / −11 行**）；`task-detail.html` 767428 → **767836（+408）**（**+7 / −0 行**）；
>   `base.html` **472150 逐字节不变**。
> 逐条实测见 `mg-work/r108/acceptance.md`（**十三节**；八 ~ 十二 = 第十三拍）；机制级教训见 PLAYBOOK **P3.49**；本页固定事实见 PAGES **P3.11i**。"""

R108O_2H = u"""
---

### 第十三拍（r108 第二层补丁 · 六条 · @WHEN@ 邵先生 · \U0001F6AB 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **八 ~ 十二节**；机制级教训见 PLAYBOOK **P3.49**。

**需求（逐字）**：
> 「1、当卡片"td-sum-sec"hover 时，边框的颜色会变成深一级的颜色；2、把"td-sum-h"这种标题前面的图标都去掉；
> 3、"td-diff-toggle"的图标颜色浅了，需使用正文颜色，并且将图标的字号调整为 13px；4、产物卡片"td-sum-art"要整体可点击预览；
> 5、任务详情页的"giencoder-badge-status-text"的字号改成 13px；6、完成上述任务后，请你调研智谱 AI 的 zcode 这个产品，
> 我需要将其对话界面右上角的那个实时任务信息卡片的内容（Git tools、Goal、Progress 等）**完全的复刻**到 `conversation.html` 页面的右上角的同样位置；」

**① 体位（就地返工，未另起代数）**：第十二拍 **未提交**（判据 `git status` 里 `conversation.html` 仍是 ` M`）
⇒ 按硬规则「**未交付 ⇒ 就地返工**」，本拍 = 第十二拍的**第二层补丁**，叠加在 `r108/` 内，**不新建 r109**。
改序仍是下→上：`part108/_mods.html` → `ev/splice108.py` → `apply108.py`。
★ 第 ⑤ 条落在 **`pages/task-detail.html`** —— **另一页、另一条血脉**（r42→…→r92 建成后只被 r101/r102/r106 改过文案），
既不参与 `splice108` 也不参与 `apply108` ⇒ 单独脚本 **`ev/patch108td.py`** 直接对页面落盘。

**② 新增/改动的文件**

| 文件 | 改动 |
|---|---|
| `ev/patch108l2.py`（**新建** 555 行） | 第 ①②③④⑥ 条，7 步 `drop_re` / `edit_all` / `tail` / `del_once` / `edit`；`mark = new` 幂等 |
| `ev/patch108td.py`（**新建** 85 行） | 第 ⑤ 条；锚点 `</style><script id="r81-ws-js">`；支持 `--revert` |
| `part108/_mods.html`（51798 → **59186** 字符） | 4 枚标题图标删净 / 2 处 `data-td-art` 上移到卡 / `PANEL_HTML`（7722 字符）追加在 `</aside>` 之前 |
| `part108/panel.css`（→ **65976** 字符 / 1387 行） | 第 280 / 1203 / 1206 行小改 + 末尾**第 19 节** + 幂等标记 `/* r108-l2 */` |
| `part108/panel.js`（→ **64682** 字符 / 1488 行） | 末尾追加面板控制器 IIFE（折展 / 胶囊 / 搬进 `main`）+ 4 枚 SVG 与文案 |
| `ev/p108n.js` + `probe108n.sh` / `probe108n2.sh` | 多相位探针（`fix` / `hover0` / `hover1` / `art` / `zd0` / `zd1` / `zd2`）+ 边界回归（遮挡 / 暗色 / 杠杆 / 窄档） |
| `ev/shots108n.sh` / `shots108n2.sh` + `raw/n-1440-*.png`（12 张） | 目视取证 |

**③ 逐条落点**

* **①** `.td-sum-sec:hover { border-color: var(--color-border-2) }`（同特异性 + 本块文档序在后 ⇒ 不用 `!important`）。
  基态 `border: 1px solid var(--color-border-1)`（`rgb(242,242,242)`）；hover **`rgb(229,229,229)`** = 深一档。
* **②** 正则 `<h4 class="td-sum-h">)<svg\b[^>]*>.*?</svg>` 替换成 `\1`（`expect=4`）；并 `del_once` 掉 `.td-sum-h svg` 死规则。
  ⚠ **删除类改动没有「改完才出现」的 `mark` ⇒ 幂等判据改用「模式不再命中」**。
* **③** `.td-diff-cv { flex:none; width:13px; height:13px; color: var(--color-text-1); transition: transform 160ms }`。
  该规则体内**不含** `line-height/height/min-height` ⇒ **不触发 `apply88b.converge()` 的压平路径**（`scan-flatten` 仍 2 条）。
* **④** `data-td-art="1"` 上移到 `.td-sum-art` 本体（2 处）+ `.td-sum-art[data-td-art] { cursor: pointer }`；内部按钮卸掉 `data`。
* **⑤** 只用一条页面级覆盖（详见「关键发现」）。
* **⑥** `PANEL_HTML` + `panel.css` 第 19 节 + `panel.js` 末段 IIFE（`place()` 搬进 `<main>`，失败则 `MutationObserver` + 4s 兜底）。

**④ ★★★ 上游体位（ZCode）**：容器 `pointer-events-none absolute top-0 right-4 z-20 pt-4`；卡片
`pointer-events-auto relative overflow-hidden rounded-2xl border shadow-md`；`panel` 档 = `w-80 max-h-[min(64dvh,32rem)]`；
`mini` 档 = `inline-flex max-h-8.5`；分区头 `h-8 min-w-0 shrink-0 items-center gap-1.5 px-2 pr-8`，
标题按钮里的 chevron **默认 `opacity-0`、hover/focus 才显形**（展开 ChevronDown / 收起 ChevronRight）。
分区 kind = `environment | goal | sessionPlans | plan | terminal | workflow | agent`；
文案逐字 = `Git 工具` / `更改` / `分支` / `提交 / 推送` / `目标` / `计划` / `进程` / `状态` / `收起为胶囊` / `展开状态`。

**⑤ 途中排掉四处坑**

1. ★★ **面板遮挡了 main 顶部工具条**（探针第一次 [B]/[C] 全废）：`.zd-host` 原本 `top:0`，与 `.r93-bar` 右上角两枚按钮重叠，
   `elementFromPoint(1410,71)` 命中的是**面板自己的 `<span class="zd-acts">`** ⇒ 探针的 `click` 点到了面板、右栏始终没开、
   `.td-sum-sec` 停在 `x=1445`（视口外）⇒ hover / 点击**静默失效**。修 = `top: 44px` + `padding-top: 12px`。
2. ★★ **`splice108.py` 的守卫被自己的注释绊倒**（第十二拍「注释绊倒判据」的**同型复现**）：
   `PANEL_HTML` 的说明注释里写了 `` `<aside class="td-browse">` 内只是为了… `` ⇒ `out.count('<aside')` 变成 **2** ⇒ 守卫 `!= 1` 报错。
   修：注释改成「右栏容器 `aside.td-browse` 内只是为了」（**不出现 `<aside` 这两个 token**）。
3. ★★ **`patch108td.py` 首版生成双 `</style>`**：锚点 `'</style><script id="r81-ws-js">'` 被**整体**替换 ⇒
   变的只是 `</style>` → `BLOCK`，插入点前面本来就有的 `</style>` 与新块自己的 `</style>` 撞成 `</style></style>`
   （DOM 解析时该 CSS 会被当 HTML 文本，**真 bug**）。修 = `REPLACEMENT = '</style>' + '{{BLOCK}}' + '<script id="r81-ws-js">'`，
   替换时只代换 `{{BLOCK}}`；复测 `</style></style>` **0** 次。
4. **截图框错了目标**：④ 的预览层 `rect x = 792` 起 —— 打开右栏后 `main` 只到 `x = 791`
   ⇒ `screenshot "main"` **正好把预览层切在画面外**（拍照成功但内容缺失，比报错更隐蔽）。修：改截 `.td-sum-prev` / `.td-browse`。

**⑥ 门禁与产物**（门禁在 `top` 修正**之后**复跑过一遍）
幂等 ✓（`patch108l2.py` 第二遍「应用 0 / 跳过 8」；`patch108td.py`「跳过（已应用）」；`apply108.py`「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`、task-detail `script=12 style=13`）｜
`verify-design.py ./pages` 与 `mg-work/r107/ev/vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`，21882 字节）｜
`scan-flatten.py part108/panel.css` ⇒ **2 条**（`.td-mod-bar` / `.td-url`）｜`pages/gaps.log` 已 `git checkout --` 清理。
`conversation.html` **978614 → 995133 字符（+16519）**（`git diff` **+582 / −11 行**）；
`task-detail.html` **767428 → 767836 字符（+408）**（**+7 / −0 行**）；`base.html` **472150 逐字节不变**；
代数核对：`r108-conv-css` / `r108-conv-js` 各 1，`r107/r106/r102-conv-*` **全 0**，base 的 nav 块仍是 `r106-nav-js`。

**⑦ 交接**：\U0001F6AB **仍未 commit / 未 push**（等邵先生显式发话；届时 `git reset -q -- mg-work/r107/ev/bak*`；`raw/` 照旧入库）。
★ r108 仍是**未交付的工作代** ⇒ 若还要改**会话详情页 / 右栏 / 任务详情页**，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。"""


# ============================================================ 1. HANDOFF.md
HOF = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')

HOF_STEPS = [
    # H1 首行「最后更新」+ 顶部块：新拍插在第十二拍块之前、老块降级为「上一拍」（两行合并成一步，锚点唯一）
    (u'> 最后更新：2026-10-01 19:4x（**r107 已推送 `e9c9498`** + **r108「diff 卡片化 + 文件树抽屉」已落地（第十二拍）** '
     u'→ 门禁四查全绿 + 真机实测（卡间距 [8,8,8] / 抽屉 panelBox [1135,49,296,842] / 两棵树零干扰）→ **\U0001F6AB 未提交**）\n'
     u'> \u26A0\uFE0F **最新一拍 = r108「diff 卡片化 + 文件树抽屉」**（第十二拍；**r107 已交付 `e9c9498` ⇒ 本代是新一代**，',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条（★ 复刻 ZCode 右上角任务信息面板）」** '
     u'→ 门禁四查全绿 + 真机实测（面板 cardRect [455,105,320,512] / 五组边界回归全绿）→ **\U0001F6AB 未提交**）\n'
     u'@BLOCK@\n'
     u'> \u26A0\uFE0F **上一拍 = r108 第十二拍「diff 卡片化 + 文件树抽屉」**（**同为 r108 未提交期**；r107 已交付 `e9c9498` ⇒ r108 是新一代，',
     u'H1 首行 + 顶部块换成第十三拍'),

    # H2 顺手修掉首部「每轮覆盖重写」重复行（历史遗留）
    # ★★ 注意第 4 个元素 `True` = **反判据**：new（一行）是 old（两行）的子串 ⇒ 常规 `mark = new` 在改前就已命中。
    (u'> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**\n'
     u'> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**',
     u'> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**',
     u'H2 修首部重复行', True),

    # H3 第一节标题 + 工作区现状
    (u'★★ **r108（diff 卡片化 + 文件树抽屉）＝本代新产物，\U0001F6AB 未提交**（2026-10-01 19:4x，第十二拍）。工作区：\n'
     u'**` M pages/conversation.html`（978614 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— '
     u'**base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'★★ **r108（第十二拍 + 第十三拍六条）＝本代新产物，\U0001F6AB 未提交**（@WHEN@，第十三拍）。工作区：\n'
     u'**` M pages/conversation.html`（995133 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— '
     u'**base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。\n'
     u'\u26A0 ★★ **本代动了第二页**：第 ⑤ 条（任务详情页徽章字号）走**独立血脉** `ev/patch108td.py`，'
     u'既不参与 `splice108` 也不参与 `apply108`。',
     u'H3 第一节标题 + 工作区现状'),

    # H4 conversation 表行的 r108 态
    (u'★ **r108 态（\U0001F6AB 未提交）**：958568 → **978614 字符**（第十二拍 +20046）；'
     u'LF bytes 1078406 / 工作区 bytes 1086146 / 7741 行 / LF `sha1_lf 7a1be6be9b76`；'
     u'注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 十二拍见 `mg-work/r108/acceptance.md`（**七节**） |',
     u'★ **r108 态（\U0001F6AB 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）**；'
     u'LF bytes 1096235 / 工作区 bytes 1105158 / **8066 行**；'
     u'注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；'
     u'r108 **十二 + 十三拍**见 `mg-work/r108/acceptance.md`（**十三节**，八 ~ 十二 = 第十三拍） |\n'
     u'| `pages/task-detail.html` | ★ **r108 第十三拍动了本页**（独立血脉 `ev/patch108td.py`）：'
     u'767428 → **767836 字符（+408）**；`git diff --numstat` = **+7 / −0 行**；'
     u'只加了一个 `<style id="r108-td-css">`（`.giencoder-badge-status-text { font-size: var(--font-size-body-2) }`，13px），'
     u'插入点 = `</style>` 与 `<script id="r81-ws-js">` 之间；`check-syntax` `script=12 style=13` |',
     u'H4 conversation 表行补 r108 十三拍'),

    # H5 mg-work/r108 表行：补第十三拍资产
    (u'`part108/`**（只覆盖改过的三件：`_mods.html` 52848 · `panel.css` 1090 → 1196 行 · `panel.js` 1335 → 1412 行；'
     u'`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）/ '
     u'`ev/`（`make108.py` · `splice108.py` · `patch108l1.py` · `p108m.js` + `probe108m{,2,3,4,5,6}.sh` · `shots108m.sh` · '
     u'`scan-flatten.py` · `vd-r108a/b.txt` · `m-raw.log` / `m2-raw.log`）/ '
     u'`raw/`（`m-1440-{diff,diff-pane,diff-split,tree,tree-panel,tree-fold,rvbar}.png`）|',
     u'`part108/`**（只覆盖改过的三件：`_mods.html` 51798 → **59186** 字符 · `panel.css` → **65976** 字符 / 1387 行 · '
     u'`panel.js` → **64682** 字符 / 1488 行；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）/ '
     u'`ev/`（**第十二拍**：`make108.py` · `splice108.py` · `patch108l1.py` · `p108m.js` + `probe108m{,2,3,4,5,6}.sh` · `shots108m.sh` · '
     u'`scan-flatten.py` · `vd-r108a/b.txt` · `m-raw.log` / `m2-raw.log`；'
     u'**第十三拍**：`patch108l2.py`（555 行）· **`patch108td.py`**（85 行，任务详情页）· `p108n.js` + `probe108n.sh` / `probe108n2.sh` · '
     u'`shots108n.sh` / `shots108n2.sh` · `vd-r108l2b.txt` · `n-raw.log` / `n2-raw.log`）/ '
     u'`raw/`（`m-1440-{diff,diff-pane,diff-split,tree,tree-panel,tree-fold,rvbar}.png` + '
     u'`n-1440-{zd,zd-card,zd-fold,zd-mini,zd-dark,bar,sum,sum-hover,art-preview,art-pane,diff,diff-toggle,revbar}.png`）|',
     u'H5 mg-work/r108 表行补十三拍资产'),

    # H6 二·h 节标题升为「十二 + 十三拍」
    (u'## 二·h ★★ r108（最新一拍 · 会话详情页「diff 卡片化 + 文件树抽屉」· 2026-10-01 19:4x 起，共**十二拍**）'
     u'—— **新一代（r107 已交付 `e9c9498`），\U0001F6AB 未提交**',
     u'## 二·h ★★ r108（最新一拍 · 会话详情页「diff 卡片化 + 文件树抽屉」+ 六条精修「含 ★ 复刻 ZCode 右上角任务信息面板」'
     u'· 2026-10-01 19:4x 起，共**十二拍 + 十三拍补丁**）—— **（r107 已交付 `e9c9498`），\U0001F6AB 未提交**',
     u'H6 二·h 节标题升为十二 + 十三拍'),

    # H7 二·h 节末追加第十三拍（锚点 = 第十二拍的 ⑦ 交接段）
    (u'**⑦ 交接**：\U0001F6AB **未 commit / 未 push**（等邵先生显式发话）。提交时注意 '
     u'`git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`（返工期的临时三源快照、不入库）。',
     u'**⑦ 交接**：\U0001F6AB **未 commit / 未 push**（等邵先生显式发话）。提交时注意 '
     u'`git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`（返工期的临时三源快照、不入库）。\n'
     u'@2H@',
     u'H7 二·h 节末追加第十三拍'),

    # H8 第七节现状
    (u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` 十二拍 \U0001F6AB 未提交**'
     u'（工作区 ` M pages/conversation.html`）。',
     u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` **十二 + 十三拍** \U0001F6AB 未提交**'
     u'（工作区 ` M pages/conversation.html` + ` M pages/task-detail.html`）。',
     u'H8 第七节现状'),

    # H9 第七节封板说明里补「第十三拍仍在未提交期」
    (u'   ★ **r108 尚在未提交期 ⇒ 可就地返工**：若还要改**会话详情页 / 右栏**，**直接改 `mg-work/r108/`**\n'
     u'   （改序 = `part108/_mods.html` → `ev/splice108.py` → `apply108.py`；\u26A0 `apply108.py` 由 `ev/make108.py` 生成、**禁手改**）。',
     u'   ★ **r108 尚在未提交期 ⇒ 可就地返工**（**第十三拍即按此体位就地叠加，未另起 r109**）：'
     u'若还要改**会话详情页 / 右栏**，**直接改 `mg-work/r108/`**\n'
     u'   （改序 = `part108/_mods.html` → `ev/splice108.py` → `apply108.py`；\u26A0 `apply108.py` 由 `ev/make108.py` 生成、**禁手改**）。\n'
     u'   \u26A0 ★★ **若改的是 `pages/task-detail.html`（另一条血脉）** ⇒ 走 **`ev/patch108td.py`**（锚点式、支持 `--revert`），'
     u'**不要**把它塞进 `apply108.py`。',
     u'H9 第七节补 task-detail 通道'),
]

# ============================================================ 2. PAGES.md
PAG = os.path.join(REPO, '.workbuddy', 'memory', 'PAGES.md')

PAG_STEPS = [
    # P1 标题：共十二拍 → 共十三拍
    (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十二拍**）',
     u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十三拍**）',
     u'P1 标题'),

    # P2 追加 ⑬ 要点
    (u'> （详见 `mg-work/r107/acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五** / **十六**节；'
     u'r108 = `mg-work/r108/acceptance.md` 七节）。',
     u'> **⑬（r108 第十三拍 · 六条精修 + ★ 复刻 ZCode 右上角任务信息面板）**：'
     u'`td-sum-sec` hover 边框深一档 / `td-sum-h` 标题图标移除 / `td-diff-toggle` 图标正文色 13px / '
     u'`td-sum-art` 整卡可点预览 / `task-detail` 徽章字号 13px / '
     u'**右上角 `.zd-host` 任务信息面板（四分区 Git 工具 · 目标 · 计划 · 进程 + 折叠 + 胶囊）**。\n'
     u'> （详见 `mg-work/r107/acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五** / **十六**节；'
     u'r108 = `mg-work/r108/acceptance.md` **十三节**，八 ~ 十二 = 第十三拍）。',
     u'P2 追加 ⑬ 要点'),

    # P3 结构图补 .zd-host
    (u'      └ div.td-tree[data-td-tree]   ← ★ r108：文件树抽屉（`z-index:35`；`.td-tree-panel` `min(296px,86%)` + '
     u'`.td-tree-files` 内 10 行 `.td-tf*`，类名与「文件」模块的 `.td-bf*` **刻意分离**）\n```',
     u'      ├ div.td-tree[data-td-tree]   ← ★ r108 ②：文件树抽屉（`z-index:35`；`.td-tree-panel` `min(296px,86%)` + '
     u'`.td-tree-files` 内 10 行 `.td-tf*`，类名与「文件」模块的 `.td-bf*` **刻意分离**）\n'
     u'      └ div.zd-host#av-zd-status    ← ★★ r108 ⑥：右上角任务信息面板（复刻 ZCode；`position:absolute` **top:44px** + '
     u'`right:16px`；`z-index:20`；**`pointer-events:none`**，只有内层 `.zd-card` 是 `auto`；'
     u'由 `panel.js` 的 `place()` 搬进 `<main>`）\n```',
     u'P3 结构图补 .zd-host'),

    # P4 固定事实表增 5 行（插在「抽屉树独立类名」行之后）
    (u'     u\'`filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10 |\',',
     u'     u\'`filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10 |\',',
     u'P4 占位（本步不改）'),
]

PAG_STEPS = [s for s in PAG_STEPS if not s[2].startswith(u'P4 占位')]

PAG_MORE = [
    # P4 固定事实表增行（锚点 = P5 最后一行「抽屉树独立类名」）
    (u'`filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10 |',
     u'`filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10 |\n'
     u'| **摘要卡 hover 边框** | ★ **r108 第十三拍 ①**：`.td-sum-sec:hover { border-color: var(--color-border-2) }` —— '
     u'基态 `var(--color-border-1)` = `rgb(242,242,242)`（gray-2）、hover **`rgb(229,229,229)`**（gray-3）= **深一档**。'
     u'同特异性 + 本块文档序在后 ⇒ 不用 `!important`。实测 `secHover:true`、rect 不动 |\n'
     u'| **摘要标题无图标** | ★ **r108 第十三拍 ②**：`.td-sum-h` 内 4 枚 `<svg>` 整段删净 + 清掉 `.td-sum-h svg` 死规则 ⇒ '
     u'实测 `sumHCount:4` / **`sumHSvg:0`** / 文字 `["摘要","计划","来源","产物"]`。'
     u'⚠ **删除类改动没有 `mark`** ⇒ 幂等判据改「模式不再命中」（`drop_re` 的 `expect` 第二遍 0）|\n'
     u'| **diff 折叠图标色 / 尺寸** | ★ **r108 第十三拍 ③**：`.td-diff-cv { flex:none; width:13px; height:13px; '
     u'color: var(--color-text-1); transition: transform 160ms }`（原 `--color-text-3`）—— 图标 svg 的 `width/height` 属性虽是 16，'
     u'但 **`.td-diff-cv` 自身没框 ⇒ 必须补 `width/height` 才是真「13px」**。实测 `rect [813,156,13,13]` / `rgb(31,31,31)`；'
     u'该规则体不含 `line-height/height/min-height` ⇒ 不触发 `converge()` 压平 |\n'
     u'| **产物卡整卡可点** | ★ **r108 第十三拍 ④**：`data-td-art="1"` 从内部「预览」按钮**上移到 `.td-sum-art` 本体**（2 处）+ '
     u'`.td-sum-art[data-td-art] { cursor: pointer }`；内部按钮卸掉 `data`（**视觉与键盘入口保留**）。'
     u'实测点「图标区」（`.td-sum-arti`）即开预览层（`pvName:"右栏复刻方案.md"`）|\n'
     u'| **★★ 右上角任务信息面板** | ★★★ **r108 第十三拍 ⑥（本拍最大件）**：`.zd-host#av-zd-status`（**`position:absolute` '
     u'**top:44px**（**不是 0**）+ `right:16px`、`z-index:20`、`padding-top:12px`、`pointer-events:none`、`max-width: calc(100% - 32px)`）'
     u' + `.zd-card`（`pointer-events:auto`）= **四分区** `git`「Git 工具」/ `goal`「目标」/ `plan`「计划」/ `todo`「进程」。'
     u'★ **`top` 必须避开 `<main>` 顶部的 `.r93-bar`**（`position:absolute; height:44px; z-index:10`，r106 的**固定档**、'
     u'**不随 `--ui-fs` 变**）—— 从 `top:0` 起排会**盖住右上角「全屏 / 打开侧栏」两枚按钮**。'
     u'折叠 = 分区头 `classList.toggle(\'is-closed\')`（**不写内联 display**）；面板 ⇄ 胶囊 = `hidden` 属性互斥。'
     u'实测 `hostInMain:true` / **`cardRect [455,105,320,512]`** / `panelRightGap:16` / `panelTopGap:57` / '
     u'`zdTop:93`（= 48 + 44 + 1）/ 折叠后卡高 **512 → 503** / 胶囊 `[672,105,103,32]` / 两枚工具条按钮 `hitSelf:true` |\n'
     u'| **任务详情页徽章字号** | ★ **r108 第十三拍 ⑤**（**另一页 / 独立血脉**）：`.giencoder-badge-status-text` 的**文字节点自己不声明字号**'
     u'（继承），真源在父级 `.giencoder-badge-status{font-size:var(--font-size-body-3)}`（14px）⇒ 只补一条**本页**规则 '
     u'`.giencoder-badge-status-text { font-size: var(--font-size-body-2) }`（13px）即可、**无需特异性竞争、不动 DS 源**。'
     u'落点 = `<style id="r108-td-css">`（插在 `</style>` 与 `<script id="r81-ws-js">` 之间）；'
     u'⚠ 替换时要保留锚点自身两个 token，否则生成 `</style></style>`（该 CSS 会被当 HTML 文本、**真 bug**）。'
     u'入口 = `ev/patch108td.py`（**不进 `apply108.py`**）|',
     u'P4 固定事实表增 6 行'),

    # P5 必看清单增 20/21/22
    (u'19. ★★ **带派生高度的新规则必须补 `var(--font-size-*)`** —— `.td-tree-h` 有 `height:calc(40px*ratio)` 但体里无 token '
     u'⇒ 被 `apply88b.converge()` 压平、`scan-flatten` 多报 1 条 ⇒ 补 `font-size: var(--font-size-body-3)` 回基线 2 条。',
     u'19. ★★ **带派生高度的新规则必须补 `var(--font-size-*)`** —— `.td-tree-h` 有 `height:calc(40px*ratio)` 但体里无 token '
     u'⇒ 被 `apply88b.converge()` 压平、`scan-flatten` 多报 1 条 ⇒ 补 `font-size: var(--font-size-body-3)` 回基线 2 条。\n'
     u'20. ★★★ **新浮层必须避开「固定高工具条」，且先做 `elementFromPoint` 自检**（r108 十三拍）：`.zd-host` 从 `top:0` 起排会盖住 '
     u'`<main>` 顶部 `.r93-bar`（`height:44px`、**不随 `--ui-fs` 变**）里的两枚按钮 ⇒ 探针的 `click` 点到浮层自己、'
     u'真正的触发器**静默没被点到**（症状 = 下游元素停在视口外、hover/点击全失效）。改 `top:44px` 后 `hitSelf:true`。\n'
     u'21. ★★ **「预览层被截在画面外」= 拍照成功的假失败** —— ④ 的预览层 `rect x=792` 起，而打开右栏后 `main` 只到 `x=791` '
     u'⇒ `screenshot "main"` **正好切掉它**（比报错更隐蔽）⇒ 截图目标要选**覆盖层自身**或它的父容器。\n'
     u'22. ★★ **回填式补丁的锚点要「保留锚点自身的 token」** —— `patch108td.py` 首版把锚点 '
     u'`\'</style><script id="r81-ws-js">\'` **整体**替换 ⇒ 生成 `</style></style>`（CSS 被当 HTML 文本）。'
     u'正解 = `REPLACEMENT = \'</style>\' + \'{{BLOCK}}\' + \'<script id="r81-ws-js">\'`，只代换 `{{BLOCK}}`。',
     u'P5 必看清单增 20/21/22'),
]

PAG_STEPS = PAG_STEPS + PAG_MORE

# ============================================================ 3. PLAYBOOK.md
PBK = os.path.join(REPO, '.workbuddy', 'memory', 'PLAYBOOK.md')

PBK_TAIL = u"""
## P3.49 ★★ r108 第十三拍（六条 · @WHEN@ 邵先生）—— ★ 四条新教训

**① ★★★ 新浮层必须避开「固定高工具条」——否则它会挡住自己的触发器（探针先做 `elementFromPoint` 自检）**
* 症状：探针点「打开侧栏」按钮**没有任何反应**，下游的 `.td-sum-sec` 停在 `x=1445`（视口外）⇒ hover / click **静默失效**，
  看起来像「hover 不生效 / 预览打不开」。
* 根因：右上角任务面板 `.zd-host` 原本 `top:0`，与 `<main>` 顶部 `.r93-bar`
  （`position:absolute; height:44px; z-index:10`，r106 定的**固定档**、**不随 `--ui-fs` 变**）右上角那两枚
  「全屏 / 打开侧栏」按钮**重叠** ⇒ `elementFromPoint(1410,71)` 命中的是**面板自己的 `<span class="zd-acts">`**。
* ★ 配方：① 新浮层排布时**先量既有固定高工具条的高度**（本站 44px）再起排（`top:44px` + `padding-top:12px`）；
  ② 探针**先验 `elementFromPoint(中心) === 自己`**（`hitSelf`）再下结论；③ 容器 `pointer-events:none` + 只有卡片 `auto`，
  这样容器占位不会吃点击。
* ⚠ 与硬规则 25（探针假失败）同族，但这是**产品真问题**、不是探针问题 —— 判据 = 真鼠标点下去**目标状态完全没变**。

**② ★★★ 「注释里出现被断言的裸 token」会绊倒自己的守卫（第二次踩，同型复现）**
* 症状：`splice108.py` 报 `!! <aside> 计数异常`，而 `<aside>` 明明只有一个。
* 根因：新写的 `PANEL_HTML` 说明注释里为了讲清体位，写了 `` `<aside class="td-browse">` 内只是为了… `` ⇒
  `out.count('<aside')` 变成 **2**（**注释也算**）。
* ★ 配方：守卫用**带引号的属性形式**（`class="td-browse-files"`）或**在注释里改写 token**（本站改成「右栏容器 `aside.td-browse` 内…」）；
  **永远别在注释里裸写被 `count()` 断言的子串**。⚠ 与 r108 第十二拍的 `td-browse-files` 同型。

**③ ★★ 回填式补丁的锚点要「保留锚点自身的 token」——否则生成双 `</style>`**
* 症状：`task-detail.html` 里出现 `</style></style>` —— DOM 解析时那段 CSS 会被当 **HTML 文本**渲染（真 bug，但不报错）。
* 根因：锚点 `'</style><script id="r81-ws-js">'` 被**整体**替换成 `BLOCK + '</style><script …>'` ⇒
  变的只是 `</style>` → `BLOCK`，于是插入点**前面本来就有的** `</style>` 与新块自己的 `</style>` 撞在一起。
* ★ 配方：`REPLACEMENT = '</style>' + '{{BLOCK}}' + '<script id="r81-ws-js">'`，替换时**只代换 `{{BLOCK}}`**，
  两个 token 各出现各一次。判据 = `s.count('</style></style>') == 0`。

**④ ★★ 「预览层被截在画面外」= 拍照成功的假失败**
* 症状：④ 的取证截图**拍成功了、但画面里没有预览层**（比报错更隐蔽）。
* 根因：预览层 `rect x = 792` 起，而**打开右栏后** `main` 只到 `x = 791`（`main` 宽从 1078 缩到 779）⇒
  `screenshot "main"` **正好把它切在画面外**。
* ★ 配方：截图目标选**覆盖层自身**（`.td-sum-prev`）或它的父容器；量测时**先确认视口/容器宽度**（布局一变，`x` 就变）。

★ **体位**：第十二拍**未提交** ⇒ **就地返工**（**不另起 r109**），本拍 = 第十二拍的第二层补丁（`patch108l2.py` + `patch108td.py`）。
★ ★ **第 ⑤ 条走独立血脉**：`pages/task-detail.html` 既不参与 `splice108` 也不参与 `apply108` ⇒ 单独脚本 `ev/patch108td.py`。
★ ★ **删除类改动没有 `mark`** ⇒ 幂等判据改「**模式不再命中**」。
★ ⑥ = 复刻 `zai-org/ZCode`（Apache-2.0）`packages/ui/src/v4/ConversationStatusPanel.tsx`（2085 行）的右上角状态面板；
  文案逐字取 `i18n/locales/zh-CN.ts` 的 `chat.statusPanel.*` / `chat.summaryPanel.*`。
★ 门禁四件套（**在 `top` 修正之后复跑**）全绿；产物 `conversation.html` → **995133 字符**（+16519，`+582 / −11` 行）、
  `task-detail.html` → **767836 字符**（+408，`+7 / −0` 行）、`base.html` **逐字节不变**。
"""

PBK_STEPS = [
    (None, PBK_TAIL, u'PB1 追加 P3.49'),
]

# ============================================================ 4. 仓库 MEMORY.md
MEM = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')

MEM_STEPS = [
    # M1 r108 段标题升为「十二 / 十三拍」
    (u'> **r108（2026-10-01 19:4x · 会话详情页「diff 卡片化 + 文件树抽屉」· **第十二拍**）—— \U0001F6AB 未提交**'
     u'（新一代，承接 r107 `e9c9498`）：',
     u'> **r108（2026-10-01 19:4x 起 · 会话详情页「diff 卡片化 + 文件树抽屉」+ 六条精修「含 ★ 复刻 ZCode 右上角任务信息面板」'
     u'· **第十二拍 + 第十三拍补丁**）—— \U0001F6AB 未提交**（r107 已交付 `e9c9498`）：',
     u'M1 r108 段标题升为十二 / 十三拍'),

    # M2 段末追加第十三拍
    (u'> \U0001F6AB 未 commit / 未 push；提交时 `git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`。',
     u'> \U0001F6AB 未 commit / 未 push；提交时 `git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`。\n'
     u'>\n'
     u'> **★ r108 第十三拍（@WHEN@ · 六条 · ★★ 就地返工、未另起代数）—— \U0001F6AB 仍未提交**：'
     u'第十二拍**未提交** ⇒ 按硬规则「**未交付 ⇒ 就地返工**」，本拍 = 第十二拍的**第二层补丁**（叠加在 `r108/` 内）。\n'
     u'> ★ 新增脚本：`ev/patch108l2.py`（555 行，第 ①②③④⑥ 条）· `ev/patch108td.py`（85 行，第 ⑤ 条）；'
     u'探针 `ev/p108n.js` + `probe108n{,2}.sh`；截图 `ev/shots108n{,2}.sh` + `raw/n-1440-*.png`（12 张）。\n'
     u'> **六条** = ① `.td-sum-sec:hover { border-color: var(--color-border-2) }`（基态 border-1 `rgb(242,242,242)` → '
     u'hover **`rgb(229,229,229)`** = 深一档）；② `.td-sum-h` 内 4 枚标题 `<svg>` 删净 + 清 `.td-sum-h svg` 死规则'
     u'（实测 `sumHSvg:0`）；③ `.td-diff-cv { width:13px; height:13px; color: var(--color-text-1) }`（原 `text-3`；'
     u'实测 `rect [813,156,13,13]` / `rgb(31,31,31)`）；④ `data-td-art` 从内部「预览」按钮**上移到卡片本体**（2 处）+ `cursor:pointer`'
     u'（点图标区即开预览层、按钮入口保留）；⑤ **任务详情页** `.giencoder-badge-status-text` → 13px'
     u'（★ 真源在父级 `.giencoder-badge-status` 的 14px，文字节点自己不声明字号 ⇒ **补本页一条规则即可、不动 DS 源**；'
     u'落点 `<style id="r108-td-css">`）；⑥ **★★★ 复刻 ZCode 右上角任务信息面板**。\n'
     u'> ★★★ **⑥ 最关键的坑 —— `.zd-host` 的 `top` 必须是 44px（不是 0）**：`<main>` 顶部有 `.r93-bar`'
     u'（`position:absolute; height:44px; z-index:10`，r106 的**固定档**、不随 `--ui-fs` 变），'
     u'右上角「全屏 / 打开侧栏」两枚按钮就在里面 ⇒ 面板从 `top:0` 起排会**把它盖住**'
     u'（实测 `elementFromPoint` 命中的是面板自己的 `.zd-acts`，导致探针的 click 点到面板、右栏没开、下游 hover/click 全失效）。'
     u'改 `top:44px` + `padding-top:12px` 后两枚按钮 `hitSelf:true`、`zdTop:93`。\n'
     u'> ★ ⑥ 落地：`.zd-host#av-zd-status`（`pointer-events:none`）+ `.zd-card`（`auto`）= 四分区 '
     u'`git`「Git 工具」/ `goal`「目标」/ `plan`「计划」/ `todo`「进程」，trailing `+566 −228` / `2 分 18 秒` / `3/5`；'
     u'折叠 = `classList.toggle(\'is-closed\')`（不写内联 display）；面板 ⇄ 胶囊 = `hidden` 互斥。'
     u'实测 `cardRect [455,105,320,512]` / `panelRightGap:16` / `panelTopGap:57` / 折叠后卡高 **512 → 503** / '
     u'胶囊 `[672,105,103,32]`。上游 = `zai-org/ZCode`（Apache-2.0）`ConversationStatusPanel.tsx`（2085 行）+ '
     u'`i18n/locales/zh-CN.ts`（`chat.statusPanel.*`）。\n'
     u'> \U0001F527 另三坑 = ① `splice108.py` 守卫被**自己注释里的裸 `<aside>` token** 绊倒（第二次同型 ⇒ 注释改成「右栏容器 `aside.td-browse`」）；'
     u'② `patch108td.py` 首版生成 `</style></style>`（锚点被整体替换 ⇒ 改为只代换 `{{BLOCK}}`）；'
     u'③ ④ 的预览层 `x=792` 起、打开右栏后 `main` 只到 791 ⇒ 截 `main` **正好切掉预览层**（改截 `.td-sum-prev`）。\n'
     u'> **门禁四件套（在 `top` 修正之后复跑）全绿**：幂等 ✓（`patch108l2.py` 第二遍「应用 0 / 跳过 8」；'
     u'`patch108td.py`「跳过」；`apply108.py`「已是目标态」）｜`check-syntax` **10/10**｜'
     u'`verify-design` 与 `vd-r107l2.txt` **逐字节同**（md5 `3dbf654337559509110899e48bef1b1c`）｜`scan-flatten` 仍 **2 条**。\n'
     u'> **产物**：`conversation.html` 978614 → **995133 字符**（+16519；`git diff` **+582 / −11 行**）；'
     u'`task-detail.html` 767428 → **767836 字符**（+408；**+7 / −0 行**）；`base.html` **472150 逐字节不变**。\n'
     u'> ★★ **新增定论见 PLAYBOOK P3.49**（四条：固定高工具条遮挡 / 注释绊倒守卫 / 锚点 token 回填 / 截图切掉覆盖层）；'
     u'逐条实测见 **`mg-work/r108/acceptance.md` 八 ~ 十二节**（共十三节）。',
     u'M2 段末追加第十三拍'),
]

# ============================================================ 5. 两份当日日志
LOG_REPO = os.path.join(REPO, '.workbuddy', 'memory', '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')

LOG_NOTE = u"""
### r108 · 第十三拍（@WHEN@ 邵先生 · \U0001F6AB 仍未提交）

**需求**（逐字）：「1、当卡片"td-sum-sec"hover 时，边框的颜色会变成深一级的颜色；2、把"td-sum-h"这种标题前面的图标都去掉；
3、"td-diff-toggle"的图标颜色浅了，需使用正文颜色，并且将图标的字号调整为 13px；4、产物卡片"td-sum-art"要整体可点击预览；
5、任务详情页的"giencoder-badge-status-text"的字号改成 13px；6、完成上述任务后，请你调研智谱 AI 的 zcode 这个产品，
我需要将其对话界面右上角的那个实时任务信息卡片的内容（Git tools、Goal、Progress 等）完全的复刻到 `conversation.html` 页面的右上角的同样位置；」

**体位**：第十二拍**未提交**（判据 `git status` 里 `conversation.html` 仍是 ` M`）⇒ 按硬规则「**未交付 ⇒ 就地返工**」，
本拍 = 第十二拍的**第二层补丁**（`ev/patch108l2.py` + `ev/patch108td.py`），**不另起 r109**。
★ 第 ⑤ 条落在 **`pages/task-detail.html`** —— 另一页、另一条血脉（不参与 `splice108` / `apply108`），单独脚本落盘。

* **①** `.td-sum-sec:hover { border-color: var(--color-border-2) }`；基态 `rgb(242,242,242)`（border-1）→ hover
  **`rgb(229,229,229)`**（border-2）= **深一档**。实测 `secHover:true`、rect 不动。
* **②** `.td-sum-h` 内 4 枚 `<svg>` 用正则 `<h4 class="td-sum-h">)<svg\b[^>]*>.*?</svg>` → `\1` 删净（`expect=4`）+ 清掉
  `.td-sum-h svg` 死规则。实测 `sumHCount:4` / **`sumHSvg:0`** / 文字 `["摘要","计划","来源","产物"]`。
  ⚠ **删除类改动没有 `mark`** ⇒ 幂等判据改「**模式不再命中**」。
* **③** `.td-diff-cv { flex:none; width:13px; height:13px; color: var(--color-text-1); transition: transform 160ms }`
  （原 `--color-text-3` → **正文色**）；图标 svg 的 `width/height` 属性虽是 16，但 `.td-diff-cv` 自身没框 ⇒ 补尺寸才是真 13px。
  实测 `rect [813,156,13,13]` / `rgb(31,31,31)`；`cardCount:4`、首卡 `[800,142,623,299]`/8px/`rgb(229,229,229)`（卡片化没被带坏）。
* **④** `data-td-art="1"` 从内部「预览」按钮**上移到 `.td-sum-art` 本体**（2 处）+ `.td-sum-art[data-td-art] { cursor:pointer }`；
  内部按钮卸掉 `data`。实测点「图标区」即开预览层（`pvName:"右栏复刻方案.md"` / `pvRect [792,93,639,798]`）、按钮入口保留。
* **⑤** `.giencoder-badge-status-text` → 13px：★ **文字节点自己不声明字号**（继承），真源在父级
  `.giencoder-badge-status{font-size:var(--font-size-body-3)}`（14px）⇒ 给**本页**补一条 `…-text { font-size: var(--font-size-body-2) }`，
  **无需特异性竞争、不动 DS 源**。落点 `<style id="r108-td-css">`（插在 `</style>` 与 `<script id="r81-ws-js">` 之间）。
  实测 `task-detail.html` 767428 → **767836 字符（+408）**；`</style></style>` **0** 次。
* **⑥ ★★★ 复刻 ZCode 右上角任务信息面板**：上游 = **`zai-org/ZCode`**（Apache-2.0，2026-09-24 开源，7272 stars，`main`）；
  权威依据 = `packages/ui/src/v4/ConversationStatusPanel.tsx`（2085 行）+ `conversationStatusPanelModel.ts`（385 行）
  + `i18n/locales/zh-CN.ts`（6497 行；文案逐字取 `chat.statusPanel.*` / `chat.summaryPanel.*`）。
  落地 = `.zd-host#av-zd-status`（`pointer-events:none`；`top:44px` + `right:16px` + `padding-top:12px` + `z-index:20`）
  + `.zd-card`（`auto`）= 四分区 `git`「Git 工具」/ `goal`「目标」/ `plan`「计划」/ `todo`「进程」；
  trailing `+566 −228` / `2 分 18 秒` / `3/5`；行 `更改 +566 −228` / `分支 main` / `提交 / 推送` / `右栏复刻方案.md`；
  目标两条迭代 `3/3` `3/4`；待办 5 条（3 done / 1 doing / 1 todo）；
  折叠 = 分区头 `classList.toggle('is-closed')`（**不写内联 display**）；面板 ⇄ 胶囊 = `hidden` 互斥（胶囊「进程 3/5」）。
  实测 `hostInMain:true` / **`cardRect [455,105,320,512]`** / `hostPE:"none"` / `panelRightGap:16` / `panelTopGap:57` /
  折叠后卡高 **512 → 503** / 胶囊 `miniRect [672,105,103,32]` / 摊回**保留折叠态**。
  ★★★ **`.zd-host` 的 `top` 必须是 44px**：`<main>` 顶部有 `.r93-bar`（`height:44px; z-index:10`，r106 的**固定档**、不随 `--ui-fs` 变），
  右上角「全屏 / 打开侧栏」两枚按钮就在里面 ⇒ 从 `top:0` 起排会**盖住它们**（实测 `elementFromPoint` 命中的是面板自己的 `.zd-acts`，
  于是探针 click 点到面板、右栏没开、下游 hover/click **静默失效**）；改 `top:44px` 后两枚按钮 `hitSelf:true`、`zdTop:93`。
* **边界回归（`probe108n2.sh` → `n2-raw.log`，五组全绿）**：`[A]` 遮挡回归 `hitSelf:true`；
  `[B]` diff 图标 `rect [813,156,13,13]` / `rgb(31,31,31)`；`[C]` 暗色档 卡 `rgb(35,35,36)` / 边 `rgb(78,78,78)` / 名 `rgb(247,247,247)`；
  `[D]` `--ui-fs=18` ⇒ ratio `calc(18 / 14)`、头部 36→46、分区头 28→36、卡 `[320,512]`（**没被压平**）；
  `[E]` 窄档 620 ⇒ `cardR [29,105,6,512]`、`overflowRight:-16`（`max-width: calc(100% - 32px)` 生效）。
* \U0001F527 另三坑：① **`splice108.py` 守卫被自己的注释绊倒**（`PANEL_HTML` 注释里裸写了 `` `<aside class="td-browse">` `` ⇒
  `out.count('<aside')` 变 2）—— 第十二拍「注释绊倒判据」的**同型复现**，改注释为「右栏容器 `aside.td-browse`」；
  ② **`patch108td.py` 首版生成 `</style></style>`**（锚点被整体替换 ⇒ 改为 `REPLACEMENT` 只代换 `{{BLOCK}}`，保留两个 token）；
  ③ **截图框错目标**：预览层 `x=792` 起、打开右栏后 `main` 只到 791 ⇒ 截 `main` **正好切掉预览层**（改截 `.td-sum-prev` / `.td-browse`）。

**门禁四件套（在 `top` 修正之后复跑一遍）**：幂等 ✓（`patch108l2.py` 第二遍「**应用 0 / 跳过 8**」；`patch108td.py`「跳过（已应用）」；
`apply108.py`「已是目标态」）/ `check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`、task-detail `script=12 style=13`）/
`verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节同**（md5 `3dbf654337559509110899e48bef1b1c`，21882 字节）/
`scan-flatten.py part108/panel.css` 仍 **2 条**（`.td-mod-bar` / `.td-url`）/ `pages/gaps.log` 已 `git checkout --` 清理。
**产物**：`conversation.html` 978614 → **995133 字符（+16519）**（`git diff --numstat` = `582  11`）；
`task-detail.html` 767428 → **767836 字符（+408）**（`7  0`）；`base.html` **472150 逐字节不变**；
代数核对 `r108-conv-css` / `r108-conv-js` 各 1、`r107/r106/r102-conv-*` **全 0**、base nav 块仍 `r106-nav-js`。
**探针** `ev/p108n.js` + `probe108n.sh` / `probe108n2.sh` → `n-raw.log` / `n2-raw.log`；
**截图** `ev/shots108n.sh` / `shots108n2.sh` → `raw/n-1440-*.png`（12 张）；
**补丁** `ev/patch108l2.py`（7 步）+ `ev/patch108td.py`。\U0001F6AB 未 commit / 未 push。
"""

LOG_STEPS = [
    (None, LOG_NOTE, u'L1 日志追加第十三拍'),
]

# ============================================================ 执行
print(u'=== 1. HANDOFF.md ===')
patch(HOF, HOF_STEPS, u'HANDOFF')
print(u'=== 2. PAGES.md ===')
patch(PAG, PAG_STEPS, u'PAGES')
print(u'=== 3. PLAYBOOK.md ===')
patch(PBK, PBK_STEPS, u'PLAYBOOK')
print(u'=== 4. 仓库 MEMORY.md ===')
patch(MEM, MEM_STEPS, u'MEMORY')
print(u'=== 5. 日志（仓库）===')
patch(LOG_REPO, LOG_STEPS, u'log-repo')
print(u'=== 6. 日志（工作区）===')
patch(LOG_WS, LOG_STEPS, u'log-ws')

print(u'')
if CHECK:
    if BAD:
        print(u'!! 锚点异常 %d 处：' % len(BAD))
        for b in BAD:
            print(u'   ' + b)
        sys.exit(1)
    print(u'\u2705 锚点全部命中 1 次')
else:
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for a in APPLIED:
        print(u'   + ' + a)
    for s in SKIPPED:
        print(u'   = ' + s)
