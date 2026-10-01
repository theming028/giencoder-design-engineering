# -*- coding: utf-8 -*-
u"""r108 第十九拍收尾：把「两条（右栏全栏划词弹浮动工具条 / `+`/下拉菜单入场补上 0.2s spring）」
同步进记忆文档。

★ 代数体位：第十二 ~ 十八拍**均未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 第十九拍同样是
  **就地返工**、**不另起 r109**、**不另开一组记忆段** —— 全部并入 r108 既有段落
  （节标题由「十二 + … + 十八拍」升为「十二 + … + 十九拍」）。

范围（同步「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行 + 顶部「最新一拍」块整块换新（第十八拍降级为「上一拍」）
                                      + §一 状态段 + conversation 表行 + mg-work 表行
                                      + §二·h 标题/引言行 + 段末追加「### 第十九拍」
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十八拍」→「共十九拍」+ 在 ⑯ 段前插入 ⑰ 要点段
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录前插入 **P3.55**（六条新教训）+ 标题「86 条」→「92 条」
                                      + 附录追加 87~92 六条
  4) .workbuddy/memory/MEMORY.md    —— r108 段追加第十九拍要点
  5) 两份 2026-10-01.md（仓库内 + 工作区）—— 追加第十九拍段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 维持 ≤3000 的前提下更新「最近拍」

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换（span）另用 `new` 首行当 mark。
★ 「mark 歧义」硬断言：mark 与 old **同时**存在 ⇒ 只可能是 mark 不唯一 ⇒ `sys.exit`；
  豁免位判据 = `old in new`（「把锚点原样保留在 new 里」的写入本来就要求锚点留下当下层契约）。
★ ⚠ 降级链条两句的**前缀不同**（`**上一拍 =` vs `**再上一拍 =`）⇒ 「上句的 old」不会成为「下句的 new」的子串
  ⇒ 复跑时不会误判「mark 歧义」（照抄 doc108t 体位）。
★ ⚠ 工作区 MEMORY.md 上一拍已到 **2998 / 3000 字符** ⇒ 本拍必须**净零增长**：新增两条红线 +
  十九拍要点，靠**压缩「十二~十七拍」枚举**与**修一条已过期的旧红线**腾出空间（脚本会硬断言 ≤3000）。
★ 用法： python ev/doc108u.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc108u.py --check    # 只校验锚点命中数 + 工作区字符预算（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 7 份文件各自保留原行尾（rd/wr 处理）。
⚠ 正文里有 `100%` 这类百分号 ⇒ **不用 `%` 格式化**，改用 `@WHEN@` / `@WSMCHARS@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 22:5x'

MEMDIR = os.path.join(REPO, '.workbuddy', 'memory')
HOF = os.path.join(MEMDIR, 'HANDOFF.md')
PAG = os.path.join(MEMDIR, 'PAGES.md')
PBK = os.path.join(MEMDIR, 'PLAYBOOK.md')
MEM = os.path.join(MEMDIR, 'MEMORY.md')
LOG_REPO = os.path.join(MEMDIR, '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')
WSMEM = os.path.join(WS, '.workbuddy', 'memory', 'MEMORY.md')

WSMEM_BUDGET = 3000          # ★ 工作区 MEMORY.md 限额（超了会被截断注入 ⇒ 等于没写）

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def subst(s):
    return s.replace(u'@WHEN@', WHEN).replace(u'@WSMCHARS@', u'%d' % WSM_CHARS)


def patch(p, steps, label):
    """steps = [(old, new, sub)]；old=None ⇒ 尾部追加。"""
    t, nl = rd(p)
    n0 = len(t)
    for step in steps:
        old, new, sub = step[0], step[1], step[2]
        new = subst(new)
        mark = new                       # ★ mark == new（唯一来源，不手抄）
        keep_anchor = old is not None and old in new
        if CHECK:
            if old is not None and t.count(old) != 1:
                BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, t.count(old)))
            continue
        if mark and mark in t:
            if (not keep_anchor) and old is not None and old in t:
                sys.exit(u'!! %s · %s：mark 歧义 —— `mark` 与 `old` 同时存在（mark 不唯一）\n'
                         u'   mark=%r' % (label, sub, mark[:160]))
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
    """把「以 <first_pre> 起、以 <last_pre> 含」的**连续若干行**整段换掉。mark = `new` 的首行。"""
    t, nl = rd(p)
    new = subst(new)
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


# ==================================================================== HANDOFF 顶部块
HOF_TOP = u"""> ⚠️ **最新一拍 = r108 第十九拍（两条 · ★★ 就地返工、未另起代数）** —— 第十二 / 十三 / 十四 / 十五 / 十六 / 十七 / 十八拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> 本拍 = **右栏全栏划词都弹浮动工具条 + `+` / 四枚下拉的入场补上「从未跑过的 0.2s spring」**，**未动任何其他模块**（`task-detail.html` / `base.html` 一字未动）。
> ① **整个右栏划词都弹浮条 → 已做**。放行根由 `.r93-scroll` 扩到 `.closest('.r93-scroll, .td-browse')`
>   （两者是**并列的 flex 兄弟**、互不包含：1440 实测 `.r93-scroll` [13,49,778,604] / `.td-browse` [791,48,641,844] ⇒ 不误判；
>   主对话口原有能力一字未动）。真机 CDP **真鼠标**拖选：审查 diff 代码 / 摘要散文小字 / 文件代码区 JSON
>   —— 改前 `selbarExists = false`（**浮条根本不弹**）→ 改后 `true`，浮条框 `[886,139,200,38]` / `[835,59,200,38]` / `[1120,113,200,38]`、
>   **在选区上方 8px**、`elementFromPoint` 命中浮条自身（`selbarOnTop = true`）；点「复制」⇒ 浮条收起 + 选区清空。
> ② **菜单入场不再硬切 → 已修**。根因 = `toggleMenu()` 把「摘 `[hidden]`（`display:none`）」与「挂开态类」挤在**同一 tick**
>   ⇒ 浏览器拿不到「改前样式」⇒ `opacity / translate / scale` 过渡**被静默跳过**（契约里 0.2s spring 入场**从未运行过**）。
>   修法 = 开态拆四步：`menu.removeAttribute('hidden')` → **`void menu.offsetWidth`（强制重排）** → `placeRv()`（位置先行 ⇒ 零位移）→ `menu.classList.add(POP_OPEN)`。
>   实测改前第 4 帧 `anims=-`、`op=1 / tr=0px / sc=1`（**一帧到终态**）；改后第 4 帧 `anims=opacity|scale|translate`、`op=0 / tr=0px 4px / sc=0.96`，
>   逐帧 `op` 0 → .188273 → .425908 → … → 1（约 12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039** 再回落、`off=(368,42)` **逐帧不变 = 零位移**。
>   四枚下拉（`+` / 对比范围 / 提交·推送 / 显示选项）**同一条代码路径一起生效**，位置口径仍 = 触发器下缘 +6px（`+` 取整 7px）。
> ★ **回归全绿**（改了 `toggleMenu` 时序 ⇒ 依赖它的旧路径全量重跑）：Esc 分层（侧栏**未被连坐**关掉）/ `+` 选「终端」/ 右键菜单 / 收侧栏 / 切页签 / `closeAll`。
> ★ **补丁 = `ev/patch108l8.py`**（**4 步**；八层幂等 `l1 全跳过 / l2 0-8 / l3 0-27 / l4 0-8 / l5 0-10 / l6 0-15 / l7 0-9 / l8 0-4`）。
> ★★ **本拍六条坑**见 PLAYBOOK **P3.55**（★★★ **「摘 `[hidden]`（`display:none`）+ 挂开态类」挤在同一 tick ⇒ CSS 过渡被静默跳过**（无报错、`getComputedStyle` 直接给终态 ⇒ 声明的入场动画可能是**死代码**；判据 = 逐帧 `getAnimations()` + **打开那一帧**读 computed；修法 = 中间**插一次强制重排**）/ 断言必须限定**函数体内**（全文计数会把另一处 `.zd-menu` 同形代码误报）/ 注释**不能插在被逐字断言的代码序列中间** / `old` 被 `new` 原样保留 ⇒ `strict=False`（**第四次**）/ **判据要跟着事实走**（探针选择器先核 DOM：正文是 `.td-browse-body` 而非 `.td-mod-body`）/ **「改前对照页」不能沿用上一轮 `bakNN/`**（混合态）⇒ 本代另立整代快照）。"""

# ==================================================================== HANDOFF 第十九拍段
HOF_19 = u"""
### 第十九拍（r108 第八层补丁 · 两条 · @WHEN@ 邵先生 · 🚫 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **四十 ~ 四十四节**；机制级教训见 PLAYBOOK **P3.55**。

**需求（逐字）**：

> 1、整个右栏"td-browse"所以的文本（含代码）被鼠标框选后，都要在上方显示浮动工具条（添加到对话、复制）；
> 2、菜单"td-mod-menu giencoder-dropdown-popup giencoder-popup-open"出现的瞬间会有闪烁或跳动或位移现象，不够自然；

**① 体位**：第十二 ~ 十八拍**未提交** ⇒ 按「未交付 ⇒ 就地返工」⇒ 本拍 = **第八层补丁** `ev/patch108l8.py`
（**4 步**，**不另起 r109**）。★ **本层只改 `panel.js` 一件**（不改 CSS / 不改 HTML）
⇒ **不必重跑 `ev/splice108.py`**，直接 `python mg-work/r108/apply108.py` 落盘即可（`part108/browse.html` 里没有 panel.js 的内容）。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/panel.js`（69623 → **72191** 字符 / 1595 → **1639** 行） | ① 划词浮条放行根 `.r93-scroll` → `.closest('.r93-scroll, .td-browse')` + 段落头注释同步 + 文件头第 ⑦ 条；② `toggleMenu()` 开态由「同一 tick 两步」拆**四步**（`removeAttribute('hidden')` → **`void menu.offsetWidth`** → `placeRv()` → `classList.add(POP_OPEN)`） |
| `part108/{panel.css,_head.html,_mods.html,browse.html}` | **一字未动**（md5 与 `ev/bak19/` 逐个相同）⇒ 无需重跑 `splice108.py` |
| `pages/conversation.html`（产物） | 1022257 → **1024825 字符**（+2568）/ **8487 行**；对 `HEAD` 累计 **`1234 / 242`** 行；工作区 bytes **1145785** / `sha1_lf` **`2c1ed815740e`** |
| `pages/base.html` / `pages/task-detail.html` | **逐字节不变** / **未动**（仍存量 `7 0`） |
| `ev/patch108l8.py` | **新建**（4 步 + 跨层断言 / 函数体限定计数 / 注释括号配平） |
| `ev/{r108v-recon.js,r108v2.js,r108v3.js,p108w.js,p108x.js}` · `probe108v{,2,3}.sh` · `probe108w.sh` · `probe108x.sh` · `shots108v.sh` | **新建**（② 逐帧采样 / A-B 对照 + ① 真鼠标拖选 + 回归重测 / 出图） |
| `ev/bak19/` | **新建**（pre-l8 **整代快照**：四件 part + `conversation-pre-l8.html`） |

**③ 真机实测（1440×900 / `--ui-fs=14`）**

① 划词浮条（CDP 真鼠标 `move/down/move×3/up`，**不是**合成事件）：审查 diff 代码 `'   <aside class="td-browse" …'` /
摘要小字 `'4 轮 · 12 次工具调用 · 2 分 '` / 文件代码区 `'"snake-game'` —— 改前 `selbarExists = false`（不弹）
→ 改后 `true`，浮条框 `[886,139,200,38]` / `[835,59,200,38]` / `[1120,113,200,38]`、**在选区上方 8px**、
`elementFromPoint` 命中浮条自身（`selbarOnTop = true`）；点「复制」⇒ 浮条收起（`selbarHidden = true`）+ 选区清空。
截图 `raw/w-before-selbar.png`（有蓝色选区、**无浮条**）→ `raw/w-after-selbar.png`（选区上方出现「添加到对话 / 复制」）。
★ 页签名 `.td-browse-tab` 与文件树行名 `.td-bf` 本来就带 `user-select: none`（它们是「控件」不是「内容」）⇒ 那两处仍拖不出选区，属**既有口径、本拍不动**。

② 菜单入场（rAF 逐帧采样，关态采 4 帧 → 第 5 帧点开 → 再采 30 帧）：
改前第 4 帧 `anims=-`、`op=1 / tr=0px / sc=1`（**一帧到终态**、此后 `getAnimations()` 恒空）；
改后第 4 帧 `anims=opacity|scale|translate`、`op=0 / tr=0px 4px / sc=0.96`，逐帧 `op` 0 → .188273 → .425908 → … → 1
（约 12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039** 再回落；`off=(368,42)` **逐帧不变 = 零位移**。
A/B 对照（`ev/r108v3.js`，两例只差那一行强制重排）：A 旧写法 `getAnimations() = []` 首帧即终态 vs B 两步写法 `opacity/scale/translate:running`。
四枚下拉一起生效（同一条代码路径）：「点开即读」实测 `.td-mod-menu` / `.td-rv-scope-menu` / `.td-commit-menu` / `.td-rv-opts`
均 `anims=opacity|scale|translate`、`op0=0`（`sc0=0.96`）；位置口径 `modDy=7` / `optsDy=6` / `scopeDy=6` / `commitDy=6`（与 l6 / 第十拍一致）。

**④ 回归重测**：Esc 前 `openMenus=["td-rv-menu"]` + `sidebarOn=true`；Esc 后 `openMenus=[]` + **`sidebarOn=true`**（侧栏未被连坐）✓；
`+` 选「终端」⇒ `activeTab=terminal` / `allMenusClosed=true` ✓；右键菜单仍可开（`box [841,194,168,193]`、走另一个函数 `ctxShow()`）✓；
收侧栏 `sidebarOn=false` ✓；页签切换 / 四枚下拉能开能关 ✓；`closeAll` 后开着的有 **0** 枚 ✓。

**⑤ 排掉的六处坑**（详见 PLAYBOOK **P3.55**）：① ★★★ **「摘 `[hidden]` + 挂开态类」同一 tick ⇒ 过渡被静默跳过**（无报错、computed 直接给终态 ⇒ 声明的入场动画可能是死代码；判据 = 逐帧 `getAnimations()` + 开帧 computed；修法 = 中间 `void el.offsetWidth`）；② ★★ 断言必须限定**函数体内**（全文计数被 `.zd-menu` 同形代码误报）；③ ★★ 注释**不能插在被逐字断言的序列中间**；④ ★★ `old` 被 `new` 原样保留 ⇒ `strict=False`（**第四次**）；⑤ ★★ 判据要跟着事实走（探针选择器先核 DOM：正文是 `.td-browse-body` 而非 `.td-mod-body`）；⑥ ★★ **「改前对照页」不能沿用上一轮 `bakNN/`**（混合态）⇒ 本代另立 `ev/bak19/`。

**⑥ 产物与门禁**：`conversation.html` 1022257 → **1024825 字符（+2568）**（对 `HEAD` 累计 **`1234 242`** 行）；
工作区 bytes **1145785** / **8487 行** / LF `sha1_lf 2c1ed815740e`；
`task-detail.html` **767836 字符（未动，仍 `7 0`）**；`base.html` **逐字节不变**。
代数核对：`★ r108-l8 ①（邵先生：` **1**、`★★ r108-l8 ②（邵先生：` **1**、`void menu.offsetWidth;` **1**、
`.closest('.r93-scroll, .td-browse')` **1**、**`.closest('.r93-scroll')` 0**、`r108-l7` **7**、`r108-l6` **10**、`data-td-prev-save` **2**。
八层幂等（l1 全跳过 / l2 0-8 / l3 0-27 / l4 0-8 / l5 0-10 / l6 0-15 / l7 0-9 / **l8 0-4**；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` **76 个问题（66 warning / 10 info / 0 critical）** ｜
注释配平 `panel.js` `/*` **96** / `*/` **96** ｜ `gaps.log` pre vs post l8 **逐字节相同**（md5 `81fb5522ffd1f97524c21819df7770fc`）。

**⑦ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`
与 `mg-work/r108/ev/bak1[3-8]*`，还要 **`git reset -q -- mg-work/r108/ev/bak19`**；
`mg-work/r108/part108/` 与 `raw/`、`up/` 照旧入库。
★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。★ **别忘 `git checkout -- pages/gaps.log`**（本轮它同样被重写）。
★ **关的那一侧本拍有意不动**（摘 `POP_OPEN` + 置 `[hidden]` ⇒ 立即 `display:none`，无退场动画）；
理由 = `[hidden]` 是 Esc 分层 / 连点重开这些路径的**唯一状态位**，加退场延迟会与它们抢时序。
★ 遗留（**有意保留、未动**）：另有两处**同型入口缺陷** —— 右键菜单 `ctxShow()` 与 `.zd-menu` 的 `placeZdMenu()`
同样是「摘 `[hidden]` + 挂类」抢在同一 tick ⇒ 它们的入场也仍是硬切（各 1 行强制重排即可对齐）。
★ ★★ **l8 之后若再叠一层（`patch108l9.py`）**：本层**未动 CSS** ⇒ `CSS_TAIL` 仍须把 `/* r108-l7 */` 原样接回；
且须保住 `panel.js` 里两处 l8 留痕注释与那**四步连续序列**（收尾有跨层兜底断言）。
"""

HOF_STEPS = [
    # 首行时间戳
    (u'> 最后更新：2026-10-01 22:4x（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条」+「第十七拍 四条」+「第十八拍 四条（预览工具条拆「另存为 / 打开所在文件夹」/ 去「最大化侧栏」/ 右栏 diff 滚动修复 / `+` 菜单「摘要」置首）」** → 门禁四查全绿 + 真机实测（工具条几何 + 逐卡可滚 + 菜单序全绿）→ **🚫 未提交**）',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条」+「第十七拍 四条」+「第十八拍 四条」+「第十九拍 两条（右栏全栏划词弹浮条 / `+` 菜单入场补上 0.2s spring）」** → 门禁四查全绿 + 真机实测（右栏三处划词出条 + 逐帧 spring 曲线 + 回归全绿）→ **🚫 未提交**）',
     u'首行时间戳 → 第十九拍'),

    # 降级链条
    (u'> ▸ **上一拍 = r108 第十七拍（四条 · 就地返工，🚫 未提交）**：① `+` 菜单纳入 `placeRv` 现场摆位（原吃写死的 `left:64px`，3 页签时 dx = −218px）· ② 删浏览器工具条三枚按钮（连带快门死代码）· ③ `.td-tree` 改 `top:44px` 让开标题栏 · ④ diff 补 46 行。要点见 PLAYBOOK **P3.53**。',
     u'> ▸ **上一拍 = r108 第十八拍（四条 · 就地返工，🚫 未提交）**：① 预览工具条「在系统打开」拆「另存为 / 打开所在文件夹」· ② 去掉「最大化侧栏」（连带整段 JS，−4039 字符）· ③ `.td-rv-body > .td-diff { flex: none; }`（原 flex 子件被压扁 + 裁掉 ⇒ 容器永不滚）· ④ `+` 菜单「摘要」置首。要点见 PLAYBOOK **P3.54**。',
     u'降级链条 · 第十八拍'),
    (u'> ▸ **再上一拍 = r108 第十六拍（三条 · 就地返工，🚫 未提交）**：① 产物预览改挂「预览」页签（旧 `.td-sum-prev` 浮层整体拆除）· ② `.zd-host` 折展动效改「收进 / 摊开右上角」· ③ `.zd-host` 四件改毛玻璃。要点见 PLAYBOOK **P3.52**。',
     u'> ▸ **再上一拍 = r108 第十七拍（四条 · 就地返工，🚫 未提交）**：① `+` 菜单纳入 `placeRv` 现场摆位（原吃写死的 `left:64px`，3 页签时 dx = −218px）· ② 删浏览器工具条三枚按钮（连带快门死代码）· ③ `.td-tree` 改 `top:44px` 让开标题栏 · ④ diff 补 46 行。要点见 PLAYBOOK **P3.53**。',
     u'降级链条 · 第十七拍'),
    (u'> 要点与本拍同源，逐条见下方「### 第十八拍」。（其下数行 = 更早各拍，本轮已顺次降级标签。）',
     u'> 要点与本拍同源，逐条见下方「### 第十九拍」。（其下数行 = 更早各拍，本轮已顺次降级标签。）',
     u'降级链条 · 要点行'),

    # §一 状态段
    (u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七 + 十八拍）＝本代新产物，🚫 未提交**（2026-10-01 22:4x，第十八拍）。工作区：\n**` M pages/conversation.html`（1022257 字符）',
     u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七 + 十八 + 十九拍）＝本代新产物，🚫 未提交**（@WHEN@，第十九拍）。工作区：\n**` M pages/conversation.html`（1024825 字符）',
     u'§一 状态段 → 第十九拍'),

    # conversation 表行
    (u'→ 1022257（第十八拍 −2448）**；工作区 bytes **1141453** / **8442 行** / LF `sha1_lf f3e0bcc1a8e2`；',
     u'→ 1022257（第十八拍 −2448）→ 1024825（第十九拍 +2568）**；工作区 bytes **1145785** / **8487 行** / LF `sha1_lf 2c1ed815740e`；',
     u'conversation 表行 → 第十九拍'),
    (u'r108 **十二 ~ 十八拍**见 `mg-work/r108/acceptance.md`（**三十九节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍、二十五 ~ 二十九 = 第十六拍、三十 ~ 三十四 = 第十七拍、三十五 ~ 三十九 = 第十八拍） |',
     u'r108 **十二 ~ 十九拍**见 `mg-work/r108/acceptance.md`（**四十四节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍、二十五 ~ 二十九 = 第十六拍、三十 ~ 三十四 = 第十七拍、三十五 ~ 三十九 = 第十八拍、**四十 ~ 四十四 = 第十九拍**） |',
     u'conversation 表行 · acceptance 节数'),

    # mg-work/r108 表行
    (u'| `mg-work/r108/` | **🚫 未提交（第十二 ~ 十八拍）**：',
     u'| `mg-work/r108/` | **🚫 未提交（第十二 ~ 十九拍）**：',
     u'表行 · 代数标签'),
    (u'`acceptance.md`（**三十九节**）/ **`part108/`**（本代**四件**：`_head.html` **4918 字节**（第十八拍**新建**，由 part107 拷贝后打 ②④）· `_mods.html` 51798 → … → 62454 → 70783 → **71067** 字符 · `panel.css` → … → 74888 → 75956 → **76769** 字符 / 1599 行 · `panel.js` → 71160 → 72477 → 72690 → **69623** 字符；`ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）',
     u'`acceptance.md`（**四十四节**）/ **`part108/`**（本代**四件**：`_head.html` **4918 字节**（第十八拍**新建**，由 part107 拷贝后打 ②④）· `_mods.html` 51798 → … → 62454 → 70783 → **71067** 字符 · `panel.css` → … → 74888 → 75956 → **76769** 字符 / 1599 行 · `panel.js` → 71160 → 72477 → 72690 → 69623 → **72191** 字符 / 1639 行（第十九拍）；`ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）',
     u'表行 · part108 体积'),
    (u'**第十八拍**：`patch108l7.py`（9 步）· `p108u.js` / `p108u2.js` · `probe108u.sh` / `probe108u2.sh` / `probe108u3.sh` · `shots108u.sh` · `bak18/` · `bak18pre/` · `chk18{,b,c}.py` · `u-raw.log` / `u-after-raw.log`）',
     u'**第十八拍**：`patch108l7.py`（9 步）· `p108u.js` / `p108u2.js` · `probe108u.sh` / `probe108u2.sh` / `probe108u3.sh` · `shots108u.sh` · `bak18/` · `bak18pre/` · `chk18{,b,c}.py` · `u-raw.log` / `u-after-raw.log`；**第十九拍**：`patch108l8.py`（4 步）· `r108v-recon.js` / `r108v2.js` / `r108v3.js` / `p108w.js` / `p108x.js` · `probe108v.sh` / `probe108v2.sh` / `probe108v3.sh` / `probe108w.sh` / `probe108x.sh` / `shots108v.sh` · `bak19/` · `{v,v2-before,v2-after,v3,w-before,w-after,x-after}-raw.log`）',
     u'表行 · ev 清单补本拍'),
    (u'`t-{menu-4tabs-browse,menu-full,url-after,tree-open,rv-rows}.png` / `u-{before,after}-{menu,bar,pvbar,rv-top,rv-scrolled}.png`）|',
     u'`t-{menu-4tabs-browse,menu-full,url-after,tree-open,rv-rows}.png` / `u-{before,after}-{menu,bar,pvbar,rv-top,rv-scrolled}.png` / `w-{before,after}-selbar.png` / `w-after-files-selbar.png` / `v-after-menu.png` / `x-after-{after-esc,ctx}.png`）|',
     u'表行 · raw/ 补本拍截图'),

    # §二·h 标题 + 引言行
    (u'2026-10-01 19:4x 起，共**十二 ~ 十八拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'2026-10-01 19:4x 起，共**十二 ~ 十九拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'二·h 标题 → 共十二 ~ 十九拍'),
    (u'> 完整版见 `mg-work/r108/acceptance.md`（**三十九节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.54**；本页固定事实见 PAGES **P3.11i**。',
     u'> 完整版见 `mg-work/r108/acceptance.md`（**四十四节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.55**；本页固定事实见 PAGES **P3.11i**。',
     u'二·h 引言行 → 第十九拍'),
]

# 「### 第十九拍」插在第十八拍段的「⑥ 交接」整块之后（该块末行是 l8 那句）
HOF_19_ANCHOR = (u'★ ★★ **l7 之后若再叠一层（`patch108l8.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l7 */` **也原样接回**（否则 l7 复跑整块重挂）。\n')

# ==================================================================== PAGES
PAG_17 = u"""> **⑰ r108 第十九拍（两条 · 右栏全栏划词弹浮条 / 菜单入场补上 0.2s spring）**：
> 　① **整个右栏划词都弹浮动工具条** —— 根因 = 放行判据写死主对话口 `if (!e.target.closest('.r93-scroll')) { selHide(); return; }`
> 　　⇒ 右栏里划词浮条**根本不弹**；改法 = 放行根扩为 **`.closest('.r93-scroll, .td-browse')`**
> 　　（两者是**并列 flex 兄弟**、互不包含：1440 实测 `.r93-scroll` [13,49,778,604] / `.td-browse` [791,48,641,844]）；
> 　　真机 CDP **真鼠标**拖选：审查 diff 代码 / 摘要散文小字 / 文件代码区 JSON —— 改前 `selbarExists = false` → 改后 `true`，
> 　　浮条框 `[886,139,200,38]` / `[835,59,200,38]` / `[1120,113,200,38]`、**在选区上方 8px**、`elementFromPoint` 命中浮条自身。
> 　② **`+` 菜单入场不再硬切** —— 根因 = `toggleMenu()` 把「摘 `[hidden]`（`display:none`）」与「挂开态类」挤在**同一 tick**
> 　　⇒ 浏览器拿不到「改前样式」⇒ `opacity / translate / scale` 过渡**被静默跳过**（契约里 0.2s spring 入场**从未运行过**）；
> 　　修法 = 开态拆四步 `removeAttribute('hidden')` → **`void menu.offsetWidth`（强制重排）** → `placeRv()` → `classList.add(POP_OPEN)`；
> 　　实测改前第 4 帧 `anims=-` / `op=1`（一帧到终态）；改后第 4 帧 `anims=opacity|scale|translate` / `op=0 / tr=0px 4px / sc=0.96`，
> 　　逐帧 `op` 0 → .188 → .426 → … → 1（≈12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039** 再回落、`off=(368,42)` **逐帧不变 = 零位移**；
> 　　四枚下拉（`+` / 对比范围 / 提交·推送 / 显示选项）同一条代码路径一起生效，位置口径仍 = 触发器下缘 +6px（`+` 取整 7px）。"""

PAG_16_HEAD = u'> **⑯ r108 第十八拍（四条 · 预览工具条拆两枚 / 去「最大化侧栏」/ 右栏 diff 滚动修复 / `+` 菜单「摘要」置首）**：'

# ==================================================================== PLAYBOOK P3.55
PBK_P355 = u"""## P3.55 ★★ r108 第十九拍（两条 · @WHEN@ 邵先生）—— ★★ 六条新教训

**① ★★★ 「摘 `[hidden]`（`display:none`）+ 挂开态类」挤在同一 tick ⇒ CSS 过渡被静默跳过**

* 本拍真踩（邵先生：「菜单出现的瞬间会有闪烁或跳动或位移现象，不够自然」）：`toggleMenu()` 里
  `menu.removeAttribute('hidden'); menu.classList.add(POP_OPEN);` 落在**同一次样式变更** ⇒
  `display:none` 时浏览器**没有「改前样式」可比** ⇒ 那一次变更里的 `opacity / translate / scale` 过渡**不会跑**，
  且**不报任何错**（`getComputedStyle` 直接给终态，看着"一切正常"）⇒ **契约里声明的入场动画完全可能是死代码**。
* ★ 判据 = ① **逐帧** `getAnimations()`（**空 = 没跑**）；② **打开那一帧**读 computed（拿到终态 = 没跑）。
  ⚠ 不能只看「有没有过渡声明」，也不能「点开后等一会儿再读」（那只会拿到终态 ⇒ 假阴性）。
* ★ 修法 = 在两次变更**中间插一次强制重排**：
  `menu.removeAttribute('hidden'); void menu.offsetWidth; menu.classList.add(POP_OPEN);`
* ★ 期望语义：改后第 4 帧 `anims=opacity|scale|translate`、`op=0 / tr=0px 4px / sc=0.96`，
  逐帧 `op` 0 → .188273 → … → 1（≈12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039** 再回落、`off` **逐帧不变**。

**② ★★ 断言必须限定在「函数体内」—— 全文计数会被「另一处同形代码」误报**

* `menu.setAttribute('hidden', '')` + `menu.classList.remove(POP_OPEN)` 这个形状在 `panel.js` 里出现 **2 次**
  （另一处是 `.zd-menu` 的 `placeZdMenu()`，**本拍有意保留**）⇒ 全文计数会把「有意保留的另一处」
  误报成「结构被改动」。**同型**：`menu.removeAttribute('hidden')` + `menu.classList.add(POP_OPEN)` 也是 2 处。
* ★ 正解 = 先切出函数体（`j.index('function toggleMenu(menu, trigger) {')` .. `j.index('\\n  }\\n', t0)`）再计数；
  并补一条**正向**断言（**全文 `count == 1`**）保证「另一处没被误删」。

**③ ★★ 注释不能插在「被逐字断言的代码序列」中间**

* 第一版把 ② 的长注释放在 `menu.removeAttribute('hidden');` 与 `void menu.offsetWidth;` **之间**
  ⇒ 「四步连续序列」的断言必然落空（**补丁本身是对的**，断的是探针）。
* ★ 要么把注释整体挪到序列**之前**，要么把断言改成「四步分四条各查一次」。

**④ ★★ `old` 被 `new` 原样保留 ⇒ 必须显式 `strict=False`**（**第四次踩**：l5 / l6 / l7 / l8）

* 文件头那条「⑥ …」原样接回、后面追加第 ⑦ 条 ⇒ `old in new` ⇒ 复跑时 `old` 与 `mark` 同时命中
  ⇒ 被误判「mark 歧义」⇒ 直接 `sys.exit`。★ 豁免判据 = `old in new`。

**⑤ ★★ 判据要跟着事实走 —— 探针选择器先核 DOM 再写**

* 文件模块正文**不叫** `.td-mod-body`，而是从 r105 逐字剪出来的 `.td-browse-body`
  （左「文件树」+ 右「代码区」`.td-browse-code` / `.td-browse-pre` / `.td-code-tx`）
  ⇒ 选择器写错只得到 `pick: null`，看着像「拖不出选区」的**假失败**。

**⑥ ★★ 「改前对照页」不能沿用上一轮 `bakNN/` —— 那是混合态**

* 上一轮（l7）的快照是 **pre-l7**；本拍是 l8 ⇒ 拿它当「改前」会得到 `browse.html` 是 pre-l7、
  `panel.js` 是 l7 改到一半的**混合态**。
* ★ 正解 = **本拍另立整代快照 `ev/bak19/`**（四件 part + `conversation-pre-l8.html`）。
  ★ 同族（P3.54 ⑦「改前态是一组文件的联合状态」）第二次踩 ⇒ **对照页必须与当前代同代、且整代齐上**。

"""

MEASURE = u"""
**★ 判据速查（本轮实测值）**：划词浮条框 `[886,139,200,38]` / `[835,59,200,38]` / `[1120,113,200,38]`（**在选区上方 8px**、`selbarOnTop = true`）；
改前第 4 帧 `anims=-` / `op=1` → 改后第 4 帧 `anims=opacity|scale|translate` / `op=0 / tr=0px 4px / sc=0.96`；
逐帧 `op` 0 → .188273 → .425908 → … → 1（≈12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039**、`off=(368,42)` **逐帧不变**；
四枚下拉 `anims` 均 `opacity|scale|translate`、`op0=0`（`sc0=0.96`）；位置口径 `modDy=7` / `optsDy=6` / `scopeDy=6` / `commitDy=6`。

---
"""

# ==================================================================== MEMORY（仓库）
MEM_19 = u"""
### 第十九拍（r108 第八层补丁 · 两条 · @WHEN@ · 🚫 未提交）

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
"""

LOG_19 = u"""
### 第十九拍（r108 第八层补丁 · 两条 · @WHEN@ 邵先生 · 🚫 未提交）

**需求**：① 整个右栏 `td-browse` 所有文本（含代码）被鼠标框选后都要在上方显示浮动工具条（添加到对话 / 复制）；
② 菜单 `td-mod-menu giencoder-dropdown-popup giencoder-popup-open` 出现瞬间有闪烁 / 跳动 / 位移，不够自然。

**体位**：第十二 ~ 十八拍未提交 ⇒ 就地返工 ⇒ 本拍 = **第八层补丁** `ev/patch108l8.py`（4 步，不另起 r109）。
★ **本层只改 `panel.js` 一件**（不动 CSS / 不动 HTML）⇒ **不必重跑 `ev/splice108.py`**，直接 `apply108.py` 落盘。

**两条落地（真机实测 / 1440×900 / `--ui-fs=14`）**：
① 放行根 `.r93-scroll` → **`.closest('.r93-scroll, .td-browse')`** ⇒ CDP **真鼠标**拖选：审查 diff 代码 / 摘要小字 / 文件代码区
改前 `selbarExists = false` → 改后 `true`，浮条框 `[886,139,200,38]` / `[835,59,200,38]` / `[1120,113,200,38]`、**在选区上方 8px**、
`elementFromPoint` 命中浮条自身；点「复制」⇒ 浮条收起 + 选区清空。截图 `raw/w-before-selbar.png` → `raw/w-after-selbar.png`。
② `toggleMenu()` 开态拆四步（`removeAttribute('hidden')` → **`void menu.offsetWidth`** → `placeRv()` → `classList.add(POP_OPEN)`）⇒
改前第 4 帧 `anims=-` / `op=1`（一帧到终态）；改后第 4 帧 `anims=opacity|scale|translate` / `op=0 / tr=0px 4px / sc=0.96`，
逐帧 `op` 0 → .188273 → .425908 → … → 1（≈12 帧 ≈ 0.2s）、`scale` 过冲 **1.0039** 再回落、`off=(368,42)` **逐帧不变 = 零位移**；
A/B 对照（`ev/r108v3.js`）：A 旧写法 `getAnimations()=[]` 首帧即终态 vs B 两步写法 `opacity/scale/translate:running`；
四枚下拉（`+` / 对比范围 / 提交·推送 / 显示选项）一起生效，「点开即读」均 `anims=opacity|scale|translate` / `op0=0`（`sc0=0.96`），
位置口径 `modDy=7` / `optsDy=6` / `scopeDy=6` / `commitDy=6`（与 l6 一致）。
**回归**：Esc 分层（`openMenus=[]` + **`sidebarOn=true`** 未被连坐）✓ / `+` 选「终端」`activeTab=terminal` ✓ / 右键菜单 `[841,194,168,193]` ✓ / 收侧栏 ✓ / 切页签 ✓ / `closeAll` 后 0 枚 ✓。

**六条坑**（→ PLAYBOOK **P3.55**）：① ★★★ **「摘 `[hidden]` + 挂开态类」挤在同一 tick ⇒ CSS 过渡被静默跳过**（无报错、computed 直接给终态 ⇒ 声明的入场动画可能是**死代码**；
判据 = **逐帧** `getAnimations()` + **打开那一帧**读 computed；修法 = 中间插 `void el.offsetWidth` 强制重排）；
② 断言必须限定**函数体内**（`panel.js` 里另一处 `.zd-menu` 的 `placeZdMenu()` 同形、有意保留 ⇒ 全文计数误报；正解 = 切函数体再数 + 补「全文 count == 1」正向断言）；
③ 注释**不能插在被逐字断言的代码序列中间**（否则四步连续序列断言必落空，补丁是对的、断的是探针）；
④ `old` 被 `new` 原样保留 ⇒ 显式 `strict=False`（**第四次**，l5/l6/l7/l8）；
⑤ **判据要跟着事实走** —— 探针选择器先核 DOM（文件模块正文是 `.td-browse-body` / `.td-browse-code`，**不叫** `.td-mod-body`；写错只得到 `pick: null` 假失败）；
⑥ **「改前对照页」不能沿用上一轮 `bakNN/`**（那是上一代的快照 ⇒ 混合态）⇒ 本代另立整代快照 `ev/bak19/`（四件 part + `conversation-pre-l8.html`）。

**产物 / 门禁**：`part108/panel.js` 69623 → **72191 字符 / 1639 行**（本拍唯一改动的源件；`panel.css` / `_head.html` / `_mods.html` / `browse.html` **一字未动** ⇒ 无需重跑 splice）；
`conversation.html` **1022257 → 1024825 字符（+2568）**（对 `HEAD` 累计 **`1234 242`** 行）；工作区 bytes **1145785** / **8487 行** / LF `sha1_lf 2c1ed815740e`；
`task-detail.html` **767836 字符（本拍未动，仍 `7 0`）**；`base.html` **逐字节不变**。
代数核对：`★ r108-l8 ①（邵先生：` **1**、`★★ r108-l8 ②（邵先生：` **1**、`void menu.offsetWidth;` **1**、`.closest('.r93-scroll, .td-browse')` **1**、**`.closest('.r93-scroll')` 0**（有意清零）、`r108-l7` **7**、`r108-l6` **10**、`data-td-prev-save` **2**。
八层幂等（l1 全跳过 / l2 0-8 / l3 0-27 / l4 0-8 / l5 0-10 / l6 0-15 / l7 0-9 / **l8 0-4**；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` **76 个问题（66 warning / 10 info / 0 critical）** ｜
注释配平（panel.js `/*` 96 / `*/` 96）｜ `gaps.log` pre vs post l8 **逐字节相同**（md5 `81fb5522ffd1f97524c21819df7770fc`）｜ `pages/gaps.log` 已 `git checkout --` 清理。
**验收** `mg-work/r108/acceptance.md` **四十四节**（四十 ~ 四十四 = 第十九拍）；**记忆同步** `ev/doc108u.py`（本文件）。
🚫 未 commit / 未 push。
"""

# ==================================================================== 工作区 MEMORY
# ★★ 上一拍已到 2998 / 3000 ⇒ 本拍加内容必须**同步压缩**（下面 3~8 步是「腾空间」的修剪，
#    都是把细节让给仓库 PLAYBOOK / 日报的**降冗余**，不是丢信息）。
WSM_STEPS = [
    (u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.54** + 附录「工作区速览 86 条」·',
     u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.55** + 附录「工作区速览 92 条」·',
     u'头部版本号 → P3.55 / 92 条'),
    (u'## 二、红线索引（完整 86 条见仓库 PLAYBOOK 附录）',
     u'## 二、红线索引（完整 92 条见仓库 PLAYBOOK 附录）',
     u'红线索引标题 → 92 条'),
    # ---- 腾空间 ①：agent-browser 细节让给 PLAYBOOK P3.21；★ 顺手修**已过期**的红线（现在有真鼠标命令）
    (u'- ⚠ `agent-browser` 不在 PATH：CLI `…/node/workspace/node_modules/agent-browser/bin/agent-browser.js`；`screenshot [选择器] [路径]`（**省略选择器 = 整屏**）、截图前 `set viewport 1440 900`；**没有 `move` 命令**（取消 hover 只能 hover 中性兄弟元素）；`eval` 输出是 **JSON 套 JSON**，**别裁 `tail -1`**。',
     u'- ⚠ `agent-browser` **不在 PATH** ⇒ 走绝对路径（细节见 PLAYBOOK P3.21）；**真鼠标 = `mouse move/down/up`**（合成 `PointerEvent` ≠ 真事件）；`screenshot [选择器] [路径]`（省略 = 整屏，先 `set viewport 1440 900`）；`eval` 是 **JSON 套 JSON**，**别裁 `tail -1`**。',
     u'腾空间 ① · agent-browser 行瘦身 + 修真鼠标'),
    # ---- 腾空间 ②：md5 明细已在仓库日报里（2026-10-01.md 多处）
    (u'- 🚨 `core.autocrlf=true` ⇒ blob 存 LF、工作区落 CRLF ⇒ **`wc -c`（字节）与 `git diff --numstat`（行）两套口径禁混用**；★ 工程说的「字符」= `decode(\'utf-8\')` 后 `\\r\\n→\\n` 的 `len()`。',
     u'- 🚨 `core.autocrlf=true` ⇒ blob 存 LF、工作区落 CRLF ⇒ **`wc -c` 与 `git diff --numstat` 两套口径禁混用**；★ 工程「字符」= `decode(\'utf-8\')` 后 `\\r\\n→\\n` 的 `len()`。',
     u'腾空间 ② · autocrlf 行瘦身'),
    (u'- 禁整文件 Read `pages/*.html`（单行 bundle ⇒ 用 Python 打印片段）；⚠ 本机 `grep` 查中文**返回空** ⇒ 中文用 Python；超长链式 bash 报 `decisionRecord missing…` ⇒ 拆条。',
     u'- 禁整文件 Read `pages/*.html`（单行 bundle ⇒ 用 Python 打片段）；⚠ 本机 `grep` 查中文**返回空** ⇒ 用 Python；超长链式 bash 报 `decisionRecord missing…` ⇒ 拆条。',
     u'腾空间 ③ · 读写行瘦身'),
    (u'- 收尾两跑：`check-syntax.py pages/*.html`（**10/10**）+ `verify-design.py ./pages`（**必须传目录**）与上轮逐条 diff；两者都污染工作区 ⇒ `git checkout --`。基线 md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节；渐变 ≤3 处；**动效 ≤300ms（CRAFT-ANIM）**。',
     u'- 收尾两跑：`check-syntax.py pages/*.html`（**10/10**）+ `verify-design.py ./pages`（**必须传目录**）与上轮逐条 diff；两者都污染工作区 ⇒ `git checkout --`。渐变 ≤3 处；**动效 ≤300ms（CRAFT-ANIM）**。',
     u'腾空间 ④ · 收尾两跑（基线 md5 已在日报存档）'),
    # ---- 本拍新增红线（合并成一条，省字）
    (u'- 可选子部件**一律判空**（含探针侧）；探针假失败七类（时序 / 过渡中取值 / `display:none` / 截图框错 / `scale:none` / 选择器层级错 / 探针自身 bug）。',
     u'- ★★★ **「摘 `[hidden]` + 挂开态类」同一 tick ⇒ 过渡被静默跳过**（无报错、computed 给终态 ⇒ 入场动画可能是**死代码**）⇒ 判据 = **逐帧 `getAnimations()`**；修法 = 中间插 `void el.offsetWidth`。\n'
     u'- 可选子部件**一律判空**（含探针侧）；探针假失败八类（时序 / 过渡中取值 / `display:none` / 截图框错 / `scale:none` / 选择器层级错 / 探针自身 bug / **沿用上轮 `bakNN/`（混合态）**）。',
     u'新增过渡红线 + 探针假失败 → 八类'),
    (u'- **r108 十二 ~ 十八拍**（🚫 未提交 · 就地返工）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 复刻 ZCode `.zd-card` 六条；十四 = `.zd-card` 四条；十五 = 视觉精修六条；十六 = 预览改挂页签 / 折展右上角 / 毛玻璃；十七 = `+` 菜单纳入 `placeRv` · 删浏览器工具条三枚 · `.td-tree` 让开标题栏 · diff 补 46 行；**十八 = 四条** —— 预览「在系统打开」拆**另存为 / 打开所在文件夹** · 删「最大化侧栏」（含 JS）· **`.td-rv-body>.td-diff{flex:none}`**（原 flex 子件被压扁+裁掉⇒永不滚）· `+` 菜单**摘要置首**。',
     u'- **r108 十二 ~ 十九拍**（🚫 未提交 · 就地返工，逐拍见 `HANDOFF.md` §二·h）：**十九 = 划词浮条放行根 `\'.r93-scroll\'` → `\'.r93-scroll, .td-browse\'`**（右栏划词终于弹条）· **`toggleMenu` 开态拆四步（`void menu.offsetWidth` 强制重排）**（原同 tick「摘 `[hidden]` + 挂类」⇒ 0.2s spring **从未跑过**）。',
     u'最近拍 · 第十九拍'),
    (u'- 补丁链 `ev/patch108{l1~l7}.py`；产物 `conversation.html` **1022257 字符**（`1186 / 239` 行）、`task-detail.html` 未动、`base.html` 不变；`acceptance.md` **三十九节**。',
     u'- 补丁链 `ev/patch108{l1~l8}.py`；产物 `conversation.html` **1024825 字符**（`1234 / 242` 行）、`task-detail.html` 未动、`base.html` 不变；`acceptance.md` **四十四节**。',
     u'补丁链 / 产物 → 第十九拍'),
]


def main():
    global WSM_CHARS
    # ---- 先预算工作区 MEMORY 改后的字符数（供 PLAYBOOK 引言引用）----
    _t, _nl = rd(WSMEM)
    for _old, _new, _sub in WSM_STEPS:
        _t = _t.replace(_old, _new, 1)
    WSM_CHARS = len(_t)
    print(u'=== 预算：工作区 MEMORY.md 改后 %d 字符（限额 %d，余量 %d）==='
          % (WSM_CHARS, WSMEM_BUDGET, WSMEM_BUDGET - WSM_CHARS))
    if WSM_CHARS > WSMEM_BUDGET:
        sys.exit(u'!! 工作区 MEMORY.md 将超出限额：%d > %d（先精简再落盘）' % (WSM_CHARS, WSMEM_BUDGET))

    print(u'=== 1/7 HANDOFF.md ===')
    span(HOF, u'> ⚠️ **最新一拍 = r108 第十八拍', u'> ★★ **本拍九条坑**见 PLAYBOOK **P3.54**',
         HOF_TOP, u'HANDOFF', u'顶部「最新一拍」块整块换新（第十八拍降级为「上一拍」）')
    patch(HOF, HOF_STEPS, u'HANDOFF')
    patch(HOF, [(HOF_19_ANCHOR, HOF_19_ANCHOR + HOF_19, u'二·h 段末追加「### 第十九拍」')], u'HANDOFF')

    print(u'=== 2/7 PAGES.md ===')
    patch(PAG, [
        (u'（r107 十一拍 + **r108 十二 ~ 十八拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十八拍**）',
         u'（r107 十一拍 + **r108 十二 ~ 十九拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十九拍**）',
         u'P3.11i 标题 → 共十九拍'),
        # ★ ⑰ 段插在 ⑯ 段**之前**（新段在上）—— 锚点 = ⑯ 段的首行，原样接回
        (PAG_16_HEAD, PAG_17 + u'\n' + PAG_16_HEAD, u'P3.11i 在 ⑯ 前插入 ⑰ 第十九拍要点'),
    ], u'PAGES')

    print(u'=== 3/7 PLAYBOOK.md ===')
    patch(PBK, [
        # ★ 顺手修 P3.21 里**已过期**的一条：agent-browser 现在有真鼠标命令（本轮 ① 就靠它取证）
        (u'  （否则 `Cannot read properties of null`）。\n',
         u'  （否则 `Cannot read properties of null`）；**真鼠标 = `mouse move/down/up`**（合成 `PointerEvent` ≠ 真事件，判据看 `isTrusted`）；`screenshot [选择器] [路径]` 省略选择器 = 整屏。\n',
         u'P3.21 补真鼠标命令（修过期条目）'),
        # 一步同时完成「在其前插入 P3.55 + 判据速查」+「标题 86 → 92 条」
        (u'## 附：工作区速览 86 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         PBK_P355 + MEASURE + u'## 附：工作区速览 92 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         u'附录前插入 P3.55 + 标题 → 92 条'),
        (u'（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**、**第十七拍加到 77 条**、**第十八拍加到 86 条**，工作区实测 **2998 字符**），',
         u'（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**、**第十七拍加到 77 条**、**第十八拍加到 86 条**、**第十九拍加到 92 条**，工作区实测 **@WSMCHARS@ 字符**），',
         u'附录引言 → 92 条'),
        (u'86. ★★ **探针自身也会假失败** —— 别先怀疑产品：`p108u2.js` 把「插入点」误写进 `stub()` 函数体、又对已展开项无脑 toggle（净开数恒 0）⇒ 假失败。',
         u'86. ★★ **探针自身也会假失败** —— 别先怀疑产品：`p108u2.js` 把「插入点」误写进 `stub()` 函数体、又对已展开项无脑 toggle（净开数恒 0）⇒ 假失败。\n'
         u'87. ★★★ **「摘 `[hidden]`（`display:none`）+ 挂开态类」挤在同一 tick ⇒ CSS 过渡被静默跳过** —— 无报错、`getComputedStyle` 直接给终态 ⇒ **契约里声明的入场动画可能是死代码**；判据 = ① **逐帧** `getAnimations()`（空 = 没跑）② **打开那一帧**读 computed（终态 = 没跑）；修法 = 中间插 **`void el.offsetWidth`** 强制重排。\n'
         u'88. ★★ **断言必须限定「函数体内」** —— 全文计数会被「另一处同形代码」误报（`panel.js` 里 `.zd-menu` 的 `placeZdMenu()` 与 `toggleMenu()` 同形、**有意保留**）⇒ 切出函数体再数 + 补「**全文 count == 1**」正向断言（保证另一处没被误删）。\n'
         u'89. ★★ **注释不能插在「被逐字断言的代码序列」中间** —— 会把连续序列断言打断（**补丁是对的、断的是探针**）⇒ 注释整体挪到序列**之前**，或把断言改成「逐条各查一次」。\n'
         u'90. ★★ **`old` 被 `new` 原样保留 ⇒ 必须显式 `strict=False`** —— **第四次踩**（l5 / l6 / l7 / l8）；豁免判据 = **`old in new`**。\n'
         u'91. ★★ **判据要跟着事实走 —— 探针选择器先核 DOM 再写** —— 文件模块正文是 `.td-browse-body` / `.td-browse-code`（**不叫** `.td-mod-body`）⇒ 写错只得到 `pick: null`（假失败：看着像「拖不出选区」）。\n'
         u'92. ★★ **「改前对照页」不能沿用上一轮 `bakNN/`** —— 那是**上一代的快照**（拿 l7 的 bak 当「改前」⇒ `browse.html` 是 pre-l7、`panel.js` 是 l7 改到一半的**混合态**）⇒ **本代另立 `ev/bak19/`**（四件 part + `conversation-pre-l8.html`）。',
         u'附录追加 87~92 六条'),
    ], u'PLAYBOOK')

    print(u'=== 4/7 MEMORY.md（仓库） ===')
    patch(MEM, [(None, MEM_19, u'追加第十九拍段')], u'MEMORY')

    print(u'=== 5/7 MEMORY.md（工作区，限额 %d 字符） ===' % WSMEM_BUDGET)
    t0, _nl0 = rd(WSMEM)
    n0 = len(t0)
    patch(WSMEM, WSM_STEPS, u'WS-MEMORY')
    if not CHECK:
        t1, _nl1 = rd(WSMEM)
        print(u'   工作区 MEMORY.md = %d 字符（限额 %d，余量 %d）' % (len(t1), WSMEM_BUDGET, WSMEM_BUDGET - len(t1)))
        if len(t1) > WSMEM_BUDGET:
            sys.exit(u'!! 工作区 MEMORY.md 超出限额：%d > %d（先精简再落盘）' % (len(t1), WSMEM_BUDGET))
    print(u'   (改动前 %d 字符)' % n0)

    print(u'=== 6/7 log-repo ===')
    patch(LOG_REPO, [(None, LOG_19, u'追加第十九拍段')], u'log-repo')

    print(u'=== 7/7 log-ws ===')
    patch(LOG_WS, [(None, LOG_19, u'追加第十九拍段')], u'log-ws')

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


WSM_CHARS = 0

if __name__ == '__main__':
    sys.exit(main())
