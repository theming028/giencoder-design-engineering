# -*- coding: utf-8 -*-
u"""r108 第十七拍收尾：把「四条（`+` 菜单定位跟随 / 浏览器工具条瘦身 / 文件树抽屉让开标题栏 / diff 加长）」
同步进记忆文档。

★ 代数体位：第十二 ~ 十六拍**均未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 第十七拍同样是
  **就地返工**、**不另起 r109**、**不另开一组记忆段** —— 全部并入 r108 既有段落
  （节标题由「十二 + 十三 + 十四 + 十五 + 十六拍」升为「十二 + … + 十七拍」）。

范围（同步「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行 + 顶部「最新一拍」块整块换新（第十六拍降级为「上一拍」、
                                      第十五 / 十四拍顺次降级）+ §一 状态段 + conversation 表行 + 二·h 段
                                      + §二·h 标题/引言行 + 段末追加「### 第十七拍」
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十六拍」→「共十七拍」+ 在 ⑭ 段前插入 ⑮ 要点段
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录前插入 **P3.53**（八条新教训）+ 标题「69 条」→「77 条」
                                      + 附录追加 70~77 八条
  4) .workbuddy/memory/MEMORY.md    —— r108 段追加第十七拍要点
  5) 两份 2026-10-01.md（仓库内 + 工作区）—— 追加第十七拍段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 维持 ≤3000 的前提下更新「最近拍」

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换另给显式 mark。
★ 「mark 歧义」硬断言（P3.51 ①）：mark 与 old **同时**存在 ⇒ 只可能是 mark 不唯一 ⇒ `sys.exit`；
  豁免位判据 = `old in new`（「把锚点原样保留在 new 里」的写入本来就要求锚点留下当下层契约）。
★ 用法： python ev/doc108s.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc108s.py --check    # 只校验锚点命中数（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 7 份文件各自保留原行尾（rd/wr 处理）。
⚠ 正文里有 `100%` / `60%` 这类百分号 ⇒ **不用 `%` 格式化**，改用 `@WHEN@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 22:2x'

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


def patch(p, steps, label):
    """steps = [(old, new, sub)]；old=None ⇒ 尾部追加。"""
    t, nl = rd(p)
    n0 = len(t)
    for step in steps:
        old, new, sub = step[0], step[1], step[2]
        new = new.replace(u'@WHEN@', WHEN)
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
HOF_TOP = u"""> ⚠️ **最新一拍 = r108 第十七拍（四条 · ★★ 就地返工、未另起代数）** —— 第十二 / 十三 / 十四 / 十五 / 十六拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> 本拍 = **右栏 `+` 菜单定位修复 + 浏览器工具条瘦身 + 文件树抽屉让开标题栏 + diff 演示内容加长**，**未动任何其他模块**（`task-detail.html` / `base.html` 一字未动）。
> ① **`+` 下拉菜单的位置没跟着触发器走 → 已修**。根因**不在** `placeRv` 的算式里 —— 它上面那句
>   `if (!menu.classList.contains('td-rv-menu')) return;` 把 `.td-mod-menu` **显式放行**了（注释还写着「保持它原来的 CSS 落位不动」），
>   于是它一直吃基类 CSS 写死的 `left: 64px`（相对 `.td-browse-bar`），而 `+` 的 x **随页签数量浮动**。
>   1440 实测（修复前）：3 枚页签时 `+` 左缘 **1074**、菜单左缘 **856** ⇒ **dx = −218px**。
>   修法 = `PLACE_ABS = ['td-mod-menu', 'td-rv-menu']` 白名单（**不用排除法**：`.td-ctxmenu` 走 `fixed` 跟指针、
>   `.zd-menu` 在 `.zd-host` 里另一个包含块，都不能吃这套算法）。
>   修复后 **dx 恒 0**：1 枚页签 `1505 / 1505`；4 枚 `1160 / 1160`（inline `left:368px`）；`--ui-fs=18` `1196 / 1196`。
>   垂直恰好仍是 42px（bar 44、按钮 28 居中 ⇒ 按钮下缘在栏内 36px，+6 = 42）⇒ `top` 兜底值不动。
> ② **浏览器「截图到剪贴板 / 缩放 / 发送页面到对话」三枚图标按钮去掉 → 已做**：三枚 `data-td-brw-act="shot|zoom|send"` 整块移除（`more` 保留）；
>   配套死代码一并清 —— `panel.js` 的 `BRW_TEXT` 三条 + `shotFlash()` + 调用点、`panel.css` 的 18-② 快门
>   （`.td-brw.is-shot::after` + `@keyframes td-shot-flash`）与**只为快门存在**的 `.td-mod.td-brw{position:relative}`。
>   实测 `brwActs = ["more"]`、`shotEls = 0`；CSS **剥注释后** `is-shot` / `td-shot-flash` 各 0 处。
>   ★ 右键菜单那条「截图到剪贴板」（`ctxForBrw`）**不是**工具条图标按钮 ⇒ 按「不得改动不必涉及的模块」保留，
>     但切断它借工具条按钮的力（原 `sb.click()`，虽 `if (sb)` 有守卫不报错、但会「点了没反应」）⇒ 改成直接给轻提示。
> ③ **审查模式的文件树蒙层要留出标题栏 → 已做**：`.td-tree` 由 `inset: 0` 改 `top: 44px; left/right/bottom: 0`
>   （它是 `.td-browse`（`position: relative`）的**直接子级** ⇒ `inset: 0` 正好把标题栏一起盖住；实测修复前 `tree.top = bar.top = 49`）。
>   44 = `.td-browse-bar` 实测高（跨代资产 browse.css 写死 40、实测 44；`--ui-fs` = 14 / 18 两档量出来都是 44 ⇒ **不随字号杠杆变**）。
>   实测 `treeRect.top − barRect.bottom = 0`、`scrimTopVsBarBottom = 0`、`treeTop: "44px"` —— scrim 与 panel **一起**下移。
> ④ **diff 里的代码要更多更长 → 已做**：两张展开卡片的统一视图 +17 / +12 行、并排视图 +11 / +6 行（真实 HTML / CSS 文本）。
>   实测行数：卡片 1 统一 **11→28**、并排 **6→17**；卡片 2 统一 **4→16**、并排 **3→9**；`.td-rv-body`
>   `scrollHeight == clientHeight == 757` ⇒ **正好填满、不溢出**（演示时一屏看全，不用滚）。
> ★ **边界与回归全绿**（`ev/probe108t.sh` + `probe108t2.sh`）：三场景（1 / 4 枚页签、`--ui-fs=18`）dx 恒 0；
>   抽屉两种几何（含 scrim）都贴标题栏下缘；工具条只剩「更多」；diff 四组行数 + 空态两卡片未受影响。
> ★ **补丁 = `ev/patch108l6.py`**（**15 步**；六层幂等 `l1 全跳过 / 0-8 / 0-27 / 0-8 / 0-10 / 0-15`，跨层标记兜底断言「全部存活 ✓」）。
> ★★ **本拍八条坑**见 PLAYBOOK **P3.53**（`mark` 选在「改前就存在的串」上 ⇒ 直接 `sys.exit` / `old` 被 `new` 原样保留 ⇒ 要 `strict=False` / 自检别用「裸属性名计数」/ 「位置不对」先分清「没跑到算法」还是「没进算法」/ 删组件要清「借它力」的引用 / `.td-tree` 包含块是整条侧栏 / **探针可见性盲区：量到了 ≠ 看得见** / `verify-design` 重写 `gaps.log`）。"""

# ==================================================================== HANDOFF 第十七拍段
HOF_17 = u"""
### 第十七拍（r108 第六层补丁 · 四条 · @WHEN@ 邵先生 · 🚫 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **三十 ~ 三十四节**；机制级教训见 PLAYBOOK **P3.53**。

**需求（逐字）**：

> 1、下拉菜单"td-mod-menu giencoder-dropdown-popup giencoder-popup-open"的位置没有跟着触发器"td-browse-add"走，导致位置偏移；
> 2、浏览器的"截图到剪贴板、缩放、发送页面到对话"这三个图标按钮不需要，请去掉；
> 3、新右栏的审查模式下，文件数的蒙层"td-tree is-open"要把标题栏"td-browse-bar"留出来，不要覆盖；
> 4、为了便于演示和观察，我需要"td-diff-rows"里的代码多一些，代码内容长一些。

**① 体位**：第十二 ~ 十六拍**未提交** ⇒ 按「未交付 ⇒ 就地返工」⇒ 本拍 = **第六层补丁** `ev/patch108l6.py`
（**15 步**，**不另起 r109**）。六层各带独立 `mark`；改序仍是下→上：
`part108/{_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`（**无需** `make108.py`）。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_mods.html`（62454 → **70783** 字符） | 删浏览器工具条三枚 `data-td-brw-act="shot\\|zoom\\|send"`（留一条 `<!-- r108-l6 ② -->` 留痕注释）；两张展开卡片补 46 行 diff（统一 +17 / +12、并排 +11 / +6，真实 HTML / CSS 文本） |
| `part108/panel.css`（74888 → **75956** 字符 / 1573 行） | 第 1 节注释改「`.td-mod-menu` 也纳入 `placeRv`」+ `.td-mod-menu{left}` 降级为兜底；删 18-② 快门整块（`is-shot::after` + `@keyframes td-shot-flash` + 只为它存在的 `.td-mod.td-brw{position:relative}`）+ 18 节头注释同步；`.td-tree` 改 `top: 44px`；插入 `/* r108-l6 */`（**把 `/* r108-l5 */` 原样接回**） |
| `part108/panel.js`（72477 → **72690** 字符） | `placeRv` 加 `PLACE_ABS = ['td-mod-menu','td-rv-menu']` 白名单（删掉旧的单族守卫 `!menu.classList.contains('td-rv-menu')`）+ 注释同步；`BRW_TEXT` 只留 `more`、删 `shotFlash()` 与 `if (kind === 'shot')` 调用；右键菜单那条「截图到剪贴板」改为直接 `say(...)`（切断 `sb.click()` 死引用） |
| `part108/browse.html` | 102564 → **106445**（`splice108.py` 重建；**是产物、不是手改对象**） |
| `ev/patch108l6.py` | **新建**（15 步；含「mark 歧义」硬断言 + 跨层兜底断言） |
| `ev/p108t.js` / `probe108t.sh` / `probe108t2.sh` | **新建**（六相位探针 / 全链执行 / 菜单目视复测） |
| `ev/bak17/` | **新建**（回滚基线：`_mods.html` / `panel.css` / `panel.js` / `browse.html`；提交前 `git reset`） |

**③ 真机实测（1440×900 / `--ui-fs=14`）**：① 侧栏就位后 **dx 恒 0**（1 枚页签 `add[1505] / menu[1505]`；
4 枚 `1160 / 1160`，inline `left:368px`；`--ui-fs=18` `1196 / 1196`，inline `left:404px`），`dy = 7` 恒定；
主证据截图 `raw/t-menu-4tabs-browse.png`（菜单左缘精确对齐 `+`），修复前复现证据 `raw/s-menu-before.png`；
② `brwActs = ["more"]`、`shotEls = 0`，截图 `raw/t-url-after.png` 只剩 后退 / 前进 / 刷新 / 地址栏 / 标注 / 更多；
③ `treeRect.top − barRect.bottom = 0`、`scrimTopVsBarBottom = 0`、`treeTop: "44px"`，
截图 `raw/t-tree-open.png` 标题栏（摘要 / 终端 / 浏览器 / 审查 / `+`）完整露出；
④ 行数 28 / 17 / 16 / 9，`.td-rv-body` `scrollHeight == clientHeight == 757`，截图 `raw/t-rv-rows.png`。

**④ 排掉的八处坑**（详见 PLAYBOOK **P3.53**）

1. ★★★ **`mark` 选在「改前就存在的串」上** ⇒ `edit()` 抛「mark 歧义」并 `sys.exit`。本轮真踩：`BRW_TEXT` 里 `more: '…'` 那条**改前就在**（本来就是最后一条）⇒ 不能当 mark。正解 = 取**「改完才形成的相邻关系」**（`var BRW_TEXT = {` **紧跟** `more:`）。
2. ★★ **`old` 会被 `new` 原样保留 ⇒ 复跑时 `old` 仍命中**（`.td-mod-menu { left: 64px; right: auto; }` 只在它**上方补了一段注释**）⇒ 必须显式 `strict=False`（与 l5「插在锚点前 + 接回锚点」同类）。
3. ★★ **自检判据别用「裸属性名计数」**：`panel.js` 里 `data-td-brw-act` 保留 **2** 处才对（`querySelectorAll` + `getAttribute`）⇒ 判据改成「**带 kind 的**引用为 0」。**先想清楚这个计数该等于几**。
4. ★★★ **「位置不对」先分清「没跑到算法」还是「压根没进算法」**：`+` 菜单漂移的根因不在算式里，而在那句**显式放行**的守卫 ⇒ 排查浮层位置的第一问是「这个元素进算法了吗」。
5. ★★ **删掉一个组件要连带清「借它力」的引用**：右键菜单那条 `sb.click()`（有 `if (sb)` 守卫 ⇒ 不报错、**点了没反应**，更难发现）⇒ 判据 = 全页 grep 被删元素的**所有**引用点（DOM / 类名 / 属性选择器 / 事件）。
6. ★★ **`.td-tree` 的包含块是 `.td-browse`（整条侧栏）而不是某个模块** ⇒ 改它的 `inset` 会**同时**把 scrim 与 panel 下移；判据要用**相对量**（`treeRect.top − barRect.bottom === 0`）。
7. ★★ **探针的「可见性」盲区**：侧栏初始 `translateX` 把整条 `.td-browse` 推到视口右外（实测 `browse.left = 1432`、`+` 在 `1505` > 视口宽 1440）⇒ 这时量 dx 仍是 0（两边同处栏外、一起偏移）**但截图是空的**。要看菜单必须走「先点一枚页签 ⇒ 侧栏滑入」那条路径（`probe108t2.sh` 的 `openTabs` 步）。**量到了 ≠ 看得见**。
8. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（行号随任何改动漂移）⇒ 收尾 `git checkout -- pages/gaps.log`。（第二次踩 ⇒ 已进 PLAYBOOK P3.53。）

**⑤ 产物与门禁**：`conversation.html` 1015095 → **1024705 字符（+9610）**（对 `HEAD` 累计 **`1146 142`** 行）；
工作区 bytes **1143754** / **8500 行** / LF `sha1_lf cc2105413d08`；
`task-detail.html` **767836（本拍未动，仍 `7 0`）**；`base.html` **472150 逐字节不变**。
代数核对：`r108-conv-css` / `r108-conv-js` / `r108-l5` 各 **1**、`r108-l6` **10**（含注释）；
`is-shot` / `td-shot-flash` **各 1 且都在注释里**（代码 0 处）。
幂等 ✓（l1 全跳过 / l2 `0/8` / l3 `0/27` / l4 `0/8` / l5 `0/10` / **l6 `0/15`** + 6/6 断言「全部存活 ✓」；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` 与基线 **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）｜
`scan-flatten.py part108/panel.css` **2 条**（`.td-mod-bar` / `.td-url` 基线）｜ `pages/gaps.log` 已 `git checkout --` 清理。

**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`
还要 **`git reset -q -- mg-work/r108/ev/bak1[3-7]*`**；`mg-work/r108/part108/` 与 `raw/`、`up/` 照旧入库。
★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。
★ **别忘 `git checkout -- pages/gaps.log`**（本轮它同样被重写）。
★ ★★ **l6 之后若再叠一层（`patch108l7.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l6 */` **也原样接回**（否则 l6 复跑整块重挂）。
"""

HOF_STEPS = [
    # 首行时间戳
    (u'> 最后更新：2026-10-01 21:5x（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条（产物预览改挂页签 + `.zd-host` 折展动效 + 毛玻璃）」** → 门禁四查全绿 + 真机实测（主链八组 + 边界三组全绿）→ **🚫 未提交**）',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条」+「第十七拍 四条（`+` 菜单定位跟随 / 浏览器工具条瘦身 / 文件树抽屉让开标题栏 / diff 加长）」** → 门禁四查全绿 + 真机实测（菜单三场景对齐 + 抽屉几何 + 行数表全绿）→ **🚫 未提交**）',
     u'首行时间戳 → 第十七拍'),

    # 降级链条
    (u'> ▸ **上一拍 = r108 第十五拍（六条 · 就地返工，🚫 未提交）**：① `.zd-sec-t` 正文黑 / 500 / 14px · ② `.zd-ico` 补 hover · ③ 「目标」只留 1 条 · ④ 已完成删除线 + 进行中转 loading · ⑤ 骨架屏期隐藏 `.zd-card` · ⑥ `.zd-sec-x` 仅折叠态显示。',
     u'> ▸ **上一拍 = r108 第十六拍（三条 · 就地返工，🚫 未提交）**：① 产物预览改挂「预览」页签（旧 `.td-sum-prev` 浮层整体拆除）· ② `.zd-host` 折展动效改「收进 / 摊开右上角」· ③ `.zd-host` 四件改毛玻璃。要点见 PLAYBOOK **P3.52**。',
     u'降级链条 · 第十六拍'),
    (u'> ▸ **再上一拍 = r108 第十四拍（四条 · 就地返工，🚫 未提交）**：① Git 三行接交互 / ② 删「计划」分区 / ③ 「目标」按上游校准 / ④ 折展与面板 ⇄ 胶囊弹性动效。',
     u'> ▸ **再上一拍 = r108 第十五拍（六条 · 就地返工，🚫 未提交）**：① `.zd-sec-t` 正文黑 / 500 / 14px · ② `.zd-ico` 补 hover · ③ 「目标」只留 1 条 · ④ 已完成删除线 + 进行中转 loading · ⑤ 骨架屏期隐藏 `.zd-card` · ⑥ `.zd-sec-x` 仅折叠态显示。',
     u'降级链条 · 第十五拍'),
    (u'> 要点与本拍同源，逐条见下方「### 第十五拍」。（其下数行 = 再上一拍（第十四拍）与更早（第十三 / 十二拍），本轮已顺次降级标签。）',
     u'> 要点与本拍同源，逐条见下方「### 第十七拍」。（其下数行 = 更早各拍，本轮已顺次降级标签。）',
     u'降级链条 · 要点行'),

    # §一 状态段
    (u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六拍）＝本代新产物，🚫 未提交**（2026-10-01 21:5x，第十六拍）。工作区：\n**` M pages/conversation.html`（1015095 字符）',
     u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七拍）＝本代新产物，🚫 未提交**（@WHEN@，第十七拍）。工作区：\n**` M pages/conversation.html`（1024705 字符）',
     u'§一 状态段 → 第十七拍'),

    # conversation 表行
    (u'→ 1012144（第十五拍 +2176）→ 1015095（第十六拍 +2951）**；LF bytes **1124149** / 工作区 bytes **1132584** / **8436 行** / LF `sha1_lf da1acf6a091c`；',
     u'→ 1012144（第十五拍 +2176）→ 1015095（第十六拍 +2951）→ 1024705（第十七拍 +9610）**；工作区 bytes **1143754** / **8500 行** / LF `sha1_lf cc2105413d08`；',
     u'conversation 表行 → 第十七拍'),

    # mg-work/r108 表行
    (u'| `mg-work/r108/` | **🚫 未提交（第十二 + 十三 + 十四 + 十五 + 十六拍）**：',
     u'| `mg-work/r108/` | **🚫 未提交（第十二 ~ 十七拍）**：',
     u'表行 · 代数标签'),
    (u'`acceptance.md`（**二十九节**）/ **`part108/`**',
     u'`acceptance.md`（**三十四节**）/ **`part108/`**',
     u'表行 · acceptance 节数'),
    (u'`_mods.html` 51798 → 59186 → 62859 → 62701 → **62454** 字符 · `panel.css` → 70729 → 73063 → **74888** 字符 / 1569 行 · `panel.js` → 71160 → **72477** 字符 / 1670 行；',
     u'`_mods.html` 51798 → … → 62454 → **70783** 字符 · `panel.css` → … → 74888 → **75956** 字符 / 1573 行 · `panel.js` → 71160 → 72477 → **72690** 字符；',
     u'表行 · part108 体积'),
    (u'· `q-raw.log`；**第十六拍**：`patch108l5.py`（10 步）· `p108r.js` · `probe108r.sh` / `probe108r2.sh` · `on.js` · `bak16/` · `r-raw.log` / `r2-raw.log` / `r3-raw.log` / `r4-raw.log` / `r5-raw.log`）/ `raw/`',
     u'· `q-raw.log`；**第十六拍**：`patch108l5.py`（10 步）· `p108r.js` · `probe108r.sh` / `probe108r2.sh` · `on.js` · `bak16/`；**第十七拍**：`patch108l6.py`（15 步）· `p108t.js` · `probe108t.sh` / `probe108t2.sh` · `bak17/` · `s-raw.log` / `t-raw.log`）/ `raw/`',
     u'表行 · ev 清单补本拍'),
    (u'`r-1440-{pv-md,pv-xlsx,dark}.png` / `r2-{tabs-after-pvB,bars-fs14-terminal,bars-fs18-preview}.png` / `r-card-over-{red,page}.png',
     u'`r-1440-{pv-md,pv-xlsx,dark}.png` / `r2-{tabs-after-pvB,bars-fs14-terminal,bars-fs18-preview}.png` / `r-card-over-{red,page}.png` / `s-menu-{before,after}.png` / `t-{menu-4tabs-browse,menu-full,url-after,tree-open,rv-rows}.png',
     u'表行 · raw/ 补本拍截图'),

    # §二·h 标题 + 引言行
    (u'2026-10-01 19:4x 起，共**十二 ~ 十六拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'2026-10-01 19:4x 起，共**十二 ~ 十七拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'二·h 标题 → 共十二 ~ 十七拍'),
    (u'> 完整版见 `mg-work/r108/acceptance.md`（**二十九节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.52**；本页固定事实见 PAGES **P3.11i**。',
     u'> 完整版见 `mg-work/r108/acceptance.md`（**三十四节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.53**；本页固定事实见 PAGES **P3.11i**。',
     u'二·h 引言行 → 第十七拍'),
]

# 「### 第十七拍」插在第十六拍段的「⑥ 交接」整块之后（该块末行是 l6 那句）
HOF_17_ANCHOR = (u'★ ★★ **l5 之后若再叠一层（`patch108l6.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l5 */` **也原样接回**（否则 l5 复跑整块重挂）。\n')

# ==================================================================== PAGES
PAG_15 = u"""> **⑮ r108 第十七拍（四条 · `+` 菜单定位跟随 / 浏览器工具条瘦身 / 文件树抽屉让开标题栏 / diff 加长）**：
> 　① **`+` 菜单位置跟随触发器** —— 根因是 `placeRv()` 里那句 `!menu.classList.contains('td-rv-menu')` 把
> 　　`.td-mod-menu` **显式放行**（注释还写着「保持它原来的 CSS 落位不动」）⇒ 它一直吃基类写死的 `left: 64px`；
> 　　修法 = `PLACE_ABS = ['td-mod-menu','td-rv-menu']` 白名单 ⇒ 实测 **dx 恒 0**（1 枚页签 `1505/1505`、
> 　　4 枚 `1160/1160`、`--ui-fs=18` `1196/1196`）；修复前 3 枚页签实测 **dx = −218px**；
> 　② **浏览器工具条瘦身** —— 删「截图到剪贴板 / 缩放 / 发送页面到对话」三枚（`brwActs = ["more"]`、`shotEls = 0`），
> 　　配套清掉 `BRW_TEXT` 三条 + `shotFlash()` + `panel.css` 18-② 快门（`.is-shot::after` + `@keyframes td-shot-flash`）
> 　　与只为它存在的 `.td-mod.td-brw{position:relative}`；右键菜单那条改为直接 `say(...)`（切断 `sb.click()` 死引用）；
> 　③ **文件树抽屉让开标题栏** —— `.td-tree` 由 `inset: 0` 改 `top: 44px`（44 = `.td-browse-bar` 实测高，
> 　　`--ui-fs` 14/18 两档都是 44 ⇒ 不随字号杠杆变）⇒ 实测 `treeRect.top − barRect.bottom = 0`（scrim 与 panel 一起下移）；
> 　④ **diff 演示内容加长** —— 统一视图 +17 / +12 行、并排 +11 / +6 行 ⇒ 实测行数 卡片 1 **11→28** / **6→17**、
> 　　卡片 2 **4→16** / **3→9**，`.td-rv-body` `scrollHeight == clientHeight == 757`（**正好填满、不溢出**）。"""

PAG_14_HEAD = u'> **⑭ r108 第十六拍（三条 · 产物预览改挂页签 + `.zd-host` 折展动效 & 毛玻璃）**：'

# ==================================================================== PLAYBOOK P3.53
PBK_P353 = u"""## P3.53 ★★ r108 第十七拍（四条 · @WHEN@ 邵先生）—— ★★ 八条新教训

**① ★★★ `mark` 的语义是「只有改完才存在的串」——别选在「改前就在」的那一行上**

* 本轮真踩：`BRW_TEXT` 的三条（`send` / `shot` / `zoom`）要删掉、只留 `more`，于是把 mark 写成
  `more: '更多浏览器选项（视觉演示）'` —— 它**改前就在**（本来就是最后一条）⇒ `edit()` 的
  「mark 歧义」硬断言直接 `sys.exit`（这是它该做的事，别把断言删掉来「过」）。
* ★ 正解 = 取**「改完才形成的**相邻**关系」**：`var BRW_TEXT = {` **紧跟** `more:` 只在删掉三条之后才成立。
* ⚠ 同类：删元素、删分支这类**纯删除**改动的 mark，永远要落在「删除后新形成的相邻串」上
  （本轮删三枚按钮用的是「标注按钮收尾 + 更多按钮开头」这个**改前被三行隔开、改后才相邻**的组合）。

**② ★★ `old` 会被 `new` 原样保留时，必须显式 `strict=False`**

* 本轮：给 `.td-mod-menu { left: 64px; right: auto; }` **上方补一段注释** ⇒ `new` 里原样带着 `old`
  ⇒ 复跑时 `old` 仍在文件里、与 `mark` 同时命中 ⇒ 硬断言误判为「mark 不唯一」。
* ★ 豁免判据 = `old in new`（「把锚点原样留在 new 里」的写入**本来就要求**锚点留下当下一层的定位点）。
  与 l5「插在锚点前 + 把锚点接回」是同一类。

**③ ★★ 自检判据别用「裸属性名计数」——先想清楚这个数**该**等于几**

* 本轮判据写「`panel.js` 里 `data-td-brw-act` 应恰好 1 处」，实测 2 处、看着像失败，
  其实两处都对（`querySelectorAll('[data-td-brw-act]')` + `getAttribute('data-td-brw-act')`）。
* ★ 改成「**带 kind 的**引用为 0」（`data-td-brw-act="`）才表达真实意图。
* ⚠ 与「判据要剥注释」同族：**先写出「这个计数为什么该等于 N」**，再写断言。

**④ ★★★ 「位置不对」先分清「没跑到算法」还是「压根没进算法」**

* `+` 菜单漂移看着像「`placeRv` 算错了」，实际是它上面那句 `if (!menu.classList.contains('td-rv-menu')) return;`
  —— **显式放行**，菜单从来没进过这套算法；注释甚至写着「保持它原来的 CSS 落位不动」。
* ★ 排查浮层位置的第一问 = **「这个元素进算法了吗」**（看守卫 / 白名单 / 选择器命中），第二问才是「算式对不对」。

**⑤ ★★ 删掉一个组件，要连带清「借它力」的引用**

* 工具条三枚图标按钮删掉后，右键菜单那条「截图到剪贴板」还在 `sb.click()` 借它的力 ——
  因为有 `if (sb)` 守卫，**不报错**、只是「点了没反应」，比报错更难发现。
* ★ 判据 = 全页 grep 被删元素的**所有**引用点：DOM 标签 / 类名 / `data-*` 选择器 / 事件绑定 /
  「另一个功能的入口」（这条最容易漏）。
* ⚠ 但**别越界**：右键菜单那条**不是**「工具条图标按钮」⇒ 保留它，只切断死引用。

**⑥ ★★ `.td-tree` 的包含块是 `.td-browse`（整条侧栏），不是某个模块**

* 它是 `.td-browse`（`position: relative`）的**直接子级** ⇒ `inset: 0` 会把标题栏一起盖住
  （实测修复前 `tree.top = bar.top = 49`）。
* ★ 改 `inset` 会**同时**把 scrim 与 panel 下移 ⇒ 判据要用**相对量**：
  `treeRect.top − barRect.bottom === 0`（本层两个量都取到 0）。
* ★ 那个 `44` 是实测值（跨代资产 browse.css 写死 40、实测 44），`--ui-fs` = 14 / 18 两档都是 44
  ⇒ **不随字号杠杆变** ⇒ 写裸 px；若写成 `calc(44px * var(--ui-fs-ratio))` 反而会被
  `apply88b.converge()` 的 unscale 压平（硬规则 9 的镜像坑）。

**⑦ ★★ 探针的「可见性」盲区：量到了 ≠ 看得见**

* 侧栏初始 `translateX` 把整条 `.td-browse` 推到**视口右外**（实测 `browse.left = 1432`、`+` 在 `1505`
  > 视口宽 1440）⇒ 这时量「菜单 vs 按钮」的 dx 仍然是 **0**（两者同处栏外、一起偏移），
  **但截图是空的**。
* ★ 要看外观必须走「**先点一枚页签 ⇒ 侧栏滑入**」那条路径（`probe108t2.sh` 的 `openTabs` 步）。
* ★ 结论：**「dx = 0」是几何证据，「截图能看到」是可见性证据，两者互不替代**（与 P3.52 ⑥
  「半透明与模糊各一条证据」同源）。

**⑧ ★ `verify-design.py` 每次都会重写 `pages/gaps.log`**（第二次踩）

* 行号随任何改动漂移 ⇒ 收尾固定 **`git checkout -- pages/gaps.log`**。
* ⚠ 这条已在附录第 69 条写过一次；本轮又踩 ⇒ 与「收尾两跑都会污染工作区」合并成一条肌肉记忆。

"""

MEASURE = u"""
**★ 判据速查（本轮实测值）**：菜单左缘 − `+` 左缘 **dx = 0**（三场景）/ `dy = 7`；
`treeRect.top − barRect.bottom = 0` / `treeTop = 44px`；`brwActs = ["more"]` / `shotEls = 0`；
diff 行数 卡片1 统一 **11→28**、并排 **6→17**；卡片2 统一 **4→16**、并排 **3→9**；
`.td-rv-body` `scrollHeight == clientHeight == 757`（正好填满）。

---
"""

# ==================================================================== MEMORY（仓库）
MEM_17 = u"""
### 第十七拍（r108 第六层补丁 · 四条 · @WHEN@ · 🚫 未提交）

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
"""

LOG_17 = u"""
### 第十七拍（r108 第六层补丁 · 四条 · @WHEN@ 邵先生 · 🚫 未提交）

**需求**：① `td-mod-menu` 位置没跟着触发器 `td-browse-add` 走；② 浏览器「截图到剪贴板 / 缩放 / 发送页面到对话」三枚图标按钮去掉；
③ 审查模式文件树蒙层 `td-tree is-open` 要让开标题栏 `td-browse-bar`；④ `td-diff-rows` 代码要更多更长。

**体位**：第十二 ~ 十六拍未提交 ⇒ 就地返工 ⇒ 本拍 = **第六层补丁** `ev/patch108l6.py`（15 步，不另起 r109）。

**四条落地（真机实测 / 1440×900 / `--ui-fs=14`）**：
① `placeRv` 加 `PLACE_ABS` 白名单 ⇒ 菜单左缘 **dx 恒 0**（1 枚 `add[1505]/menu[1505]`、4 枚 `1160/1160` inline `left:368px`、
`--ui-fs=18` `1196/1196`），`dy = 7` 恒定；修复前 3 枚页签 **dx = −218px**（`add 1074` / `menu 856`）；
② `brwActs = ["more"]`、`shotEls = 0`；清掉 `BRW_TEXT` 三条 + `shotFlash()` + `panel.css` 18-② 快门 + 只为快门存在的
`.td-mod.td-brw{position:relative}`；右键菜单那条改直接 `say(...)`（切断 `sb.click()`）；
③ `.td-tree` `inset:0` → `top:44px`（44 = `.td-browse-bar` 实测高；字号两档都是 44）⇒ `treeRect.top − barRect.bottom = 0`、
`scrimTopVsBarBottom = 0`、`treeTop: "44px"`；
④ 统一视图 +17 / +12 行、并排 +11 / +6 行 ⇒ 卡片 1 **11→28** / **6→17**、卡片 2 **4→16** / **3→9**；
`.td-rv-body` `scrollHeight == clientHeight == 757`（正好填满、不溢出）。

**八条坑**（→ PLAYBOOK **P3.53**）：① `mark` 别选在「改前就在」的那行（`BRW_TEXT` 的 `more:` 真踩 ⇒ 硬断言 `sys.exit`）——
要取「改完才形成的**相邻**关系」；② `old` 被 `new` 原样保留（只在上方补注释）⇒ 显式 `strict=False`；
③ 自检别用「裸属性名计数」（`data-td-brw-act` 该有 2 处）⇒ 用「带 kind 的引用为 0」；
④ **「位置不对」先分清「没跑到算法」还是「压根没进算法」** —— 根因是 `placeRv` 里那句**显式放行** `td-mod-menu` 的守卫；
⑤ 删组件要清「借它力」的引用（右键菜单 `sb.click()` 有守卫 ⇒ 不报错、只是「点了没反应」，更难发现）；
⑥ `.td-tree` 的包含块是 `.td-browse`（整条侧栏）⇒ 改 `inset` 会**同时**移动 scrim 与 panel，判据用**相对量**；
⑦ **探针可见性盲区：量到了 ≠ 看得见**（侧栏 `translateX` 在视口外时 dx 仍 0、截图却是空的 ⇒ 要走「先点页签让侧栏滑入」那条路径）；
⑧ `verify-design.py` 每次重写 `pages/gaps.log`（第二次踩）。

**产物 / 门禁**：`part108/_mods.html` 62454 → **70783** · `panel.css` 74888 → **75956** · `panel.js` 72477 → **72690** ·
`browse.html` 102564 → **106445**（splice 产物）；
`conversation.html` **1015095 → 1024705 字符（+9610）**（对 `HEAD` 累计 **`1146 142`** 行）；
工作区 bytes **1143754** / **8500 行** / LF `sha1_lf cc2105413d08`；
`task-detail.html` **767836（本拍未动，仍 `7  0`）**；`base.html` **逐字节不变**。
六层幂等（l1 全跳过 / l2 0-8 / l3 0-27 / l4 0-8 / l5 0-10 / **l6 0-15** + 6/6 断言「全部存活 ✓」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` 与基线**逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）｜
`scan-flatten.py part108/panel.css` **2 条**（基线）｜ `pages/gaps.log` 已 `git checkout --` 清理。
**验收** `mg-work/r108/acceptance.md` **三十四节**（三十 ~ 三十四 = 第十七拍）；**记忆同步** `ev/doc108s.py`（本文件）。
🚫 未 commit / 未 push。
"""

# ==================================================================== 工作区 MEMORY
WSM_STEPS = [
    (u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.52** + 附录「工作区速览 69 条」·',
     u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.53** + 附录「工作区速览 77 条」·',
     u'头部版本号 → P3.53 / 77 条'),
    (u'## 二、红线索引（完整 69 条见仓库 PLAYBOOK 附录）',
     u'## 二、红线索引（完整 77 条见仓库 PLAYBOOK 附录）',
     u'红线索引标题 → 77 条'),
    (u'- **r108 十二 ~ 十六拍**（🚫 未提交 · **同一代就地返工**）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 六条（含复刻 ZCode 右上角 `.zd-card`）；十四 = `.zd-card` 四条；十五 = 六条（视觉精修 + 骨架屏门控）；**十六 = 三条** —— 产物预览改挂 **「预览」页签**（旧 `.td-sum-prev` 浮层整体拆除）· 折展改**右上角锚点**（`transform-origin:100% 0` + `zd-panel-in` 过冲）· `.zd-host` 四件改**毛玻璃**（`backdrop-filter: blur(18px) saturate(1.6)`）。',
     u'- **r108 十二 ~ 十七拍**（🚫 未提交 · **同一代就地返工**）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 六条（含复刻 ZCode 右上角 `.zd-card`）；十四 = `.zd-card` 四条；十五 = 六条（视觉精修 + 骨架屏门控）；十六 = 三条（预览改挂页签 / 折展改右上角锚点 / `.zd-host` 毛玻璃）；**十七 = 四条** —— `+` 菜单纳入 `placeRv` 现场摆位（原吃写死的 `left:64px`，3 页签时 **dx = −218px**）· 删浏览器工具条三枚按钮（连带快门死代码）· `.td-tree` 改 `top:44px` 让开标题栏 · diff 补 46 行。',
     u'最近拍 · 第十七拍'),
    (u'- 补丁链 `ev/patch108{l1,l2,l3,l4,l5}.py`；产物 `conversation.html` **1015095 字符**（`1047 / 107` 行）、`task-detail.html` **767836（未动）**、`base.html` 逐字节不变；`acceptance.md` **二十九节**。',
     u'- 补丁链 `ev/patch108{l1~l6}.py`；产物 `conversation.html` **1024705 字符**（`1146 / 142` 行）、`task-detail.html` **767836（未动）**、`base.html` 逐字节不变；`acceptance.md` **三十四节**。',
     u'补丁链 / 产物 → 第十七拍'),
]


def main():
    print(u'=== 1/7 HANDOFF.md ===')
    span(HOF, u'> ⚠️ **最新一拍 = r108 第十六拍', u'> ★★ **本拍六条坑**见 PLAYBOOK **P3.52**',
         HOF_TOP, u'HANDOFF', u'顶部「最新一拍」块整块换新（第十六拍降级为「上一拍」）')
    patch(HOF, HOF_STEPS, u'HANDOFF')
    patch(HOF, [(HOF_17_ANCHOR, HOF_17_ANCHOR + HOF_17, u'二·h 段末追加「### 第十七拍」')], u'HANDOFF')

    print(u'=== 2/7 PAGES.md ===')
    patch(PAG, [
        (u'（r107 十一拍 + **r108 十二 / 十三 / 十四 / 十五 / 十六拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十六拍**）',
         u'（r107 十一拍 + **r108 十二 ~ 十七拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十七拍**）',
         u'P3.11i 标题 → 共十七拍'),
        # ★ ⑮ 段插在 ⑭ 段**之前**（新段在上）—— 锚点 = ⑭ 段的首行，原样接回
        (PAG_14_HEAD, PAG_15 + u'\n' + PAG_14_HEAD + u'\n', u'P3.11i 在 ⑭ 前插入 ⑮ 第十七拍要点'),
    ], u'PAGES')

    print(u'=== 3/7 PLAYBOOK.md ===')
    patch(PBK, [
        # 一步同时完成「在其前插入 P3.53 + 判据速查」+「标题 69 → 77 条」
        (u'## 附：工作区速览 69 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         PBK_P353 + MEASURE + u'## 附：工作区速览 77 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         u'附录前插入 P3.53 + 标题 → 77 条'),
        (u'（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**，工作区实测 **2982 字符**），',
         u'（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**、**第十七拍加到 77 条**，工作区实测 **2989 字符**），',
         u'附录引言 → 77 条'),
        (u'69. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（行号随任何改动漂移）⇒ 收尾一律 **`git checkout -- pages/gaps.log`**，别把它当成「我改错了」。',
         u'69. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（行号随任何改动漂移）⇒ 收尾一律 **`git checkout -- pages/gaps.log`**，别把它当成「我改错了」。\n'
         u'70. ★★★ **`mark` 的语义是「只有改完才存在的串」** —— 纯删除类改动的 mark 必须落在「删除后**新形成的相邻串**」上；本轮把 mark 写成 `more: …`（改前就在的最后一条）⇒ 硬断言直接 `sys.exit`。\n'
         u'71. ★★ **`old` 被 `new` 原样保留（只在上方补注释）时，必须显式 `strict=False`** —— 否则复跑时 `old` 仍在、与 mark 同时命中 ⇒ 被误判「mark 不唯一」。\n'
         u'72. ★★ **自检判据别用「裸属性名计数」** —— 先写清「这个数为什么该等于 N」（`data-td-brw-act` 该有 **2** 处：`querySelectorAll` + `getAttribute`）。\n'
         u'73. ★★★ **「位置不对」先分清「没跑到算法」还是「压根没进算法」** —— 根因常常是一句**显式放行**的守卫（本页 `placeRv` 里 `!classList.contains(\'td-rv-menu\')`），而不是算式。\n'
         u'74. ★★ **删组件要清「借它力」的引用** —— 有 `if (el)` 守卫时**不报错**、只是「点了没反应」，比报错更难发现；判据 = 全页 grep 所有引用点（含「另一个功能的入口」）。\n'
         u'75. ★★ **浮层的包含块要先确认** —— `.td-tree` 的包含块是整条侧栏（`.td-browse`）⇒ 改 `inset` 会**同时**移动 scrim 与 panel；判据用**相对量**（`子件top − 兄弟bottom === 0`）。\n'
         u'76. ★★ **探针的「可见性」盲区：量到了 ≠ 看得见** —— 元素在视口外时几何量（dx=0）照样「正确」，但截图是空的；**几何证据与可见性证据互不替代**。\n'
         u'77. ★ **收尾两跑都会污染工作区** —— `check-syntax` / `verify-design` 各自重写产物；`verify-design` 还会重写 **`pages/gaps.log`**（行号漂移）⇒ 一律 `git checkout --`。',
         u'附录追加 70~77 八条'),
    ], u'PLAYBOOK')

    print(u'=== 4/7 MEMORY.md（仓库） ===')
    patch(MEM, [(None, MEM_17, u'追加第十七拍段')], u'MEMORY')

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
    patch(LOG_REPO, [(None, LOG_17, u'追加第十七拍段')], u'log-repo')

    print(u'=== 7/7 log-ws ===')
    patch(LOG_WS, [(None, LOG_17, u'追加第十七拍段')], u'log-ws')

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
