# -*- coding: utf-8 -*-
u"""r108 第十八拍收尾：把「四条（预览工具条拆两枚 / 去「最大化侧栏」/ 右栏 diff 滚动修复 / `+` 菜单「摘要」置首）」
同步进记忆文档。

★ 代数体位：第十二 ~ 十七拍**均未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 第十八拍同样是
  **就地返工**、**不另起 r109**、**不另开一组记忆段** —— 全部并入 r108 既有段落
  （节标题由「十二 + … + 十七拍」升为「十二 + … + 十八拍」）。

范围（同步「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行 + 顶部「最新一拍」块整块换新（第十七拍降级为「上一拍」、
                                      第十六 / 十五拍顺次降级）+ §一 状态段 + conversation 表行 + mg-work 表行
                                      + §二·h 标题/引言行 + 段末追加「### 第十八拍」
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十七拍」→「共十八拍」+ 在 ⑮ 段前插入 ⑯ 要点段
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录前插入 **P3.54**（九条新教训）+ 标题「77 条」→「86 条」
                                      + 附录追加 78~86 九条
  4) .workbuddy/memory/MEMORY.md    —— r108 段追加第十八拍要点
  5) 两份 2026-10-01.md（仓库内 + 工作区）—— 追加第十八拍段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 维持 ≤3000 的前提下更新「最近拍」

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换（span）另用 `new` 首行当 mark。
★ 「mark 歧义」硬断言：mark 与 old **同时**存在 ⇒ 只可能是 mark 不唯一 ⇒ `sys.exit`；
  豁免位判据 = `old in new`（「把锚点原样保留在 new 里」的写入本来就要求锚点留下当下层契约）。
★ ⚠ 降级链条两句的**前缀不同**（`**上一拍 =` vs `**再上一拍 =`）⇒ 「上句的 old」不会成为「下句的 new」的子串
  ⇒ 复跑时不会误判「mark 歧义」（这是 doc108s 就验证过的体位，照抄）。
★ 用法： python ev/doc108t.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc108t.py --check    # 只校验锚点命中数（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 7 份文件各自保留原行尾（rd/wr 处理）。
⚠ 正文里有 `100%` / `60%` 这类百分号 ⇒ **不用 `%` 格式化**，改用 `@WHEN@` / `@WSMCHARS@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 22:4x'

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
HOF_TOP = u"""> ⚠️ **最新一拍 = r108 第十八拍（四条 · ★★ 就地返工、未另起代数）** —— 第十二 / 十三 / 十四 / 十五 / 十六 / 十七拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> 本拍 = **预览工具条「在系统打开」拆两枚 + 侧栏标题栏去「最大化」+ 右栏 diff 滚动修复 + `+` 菜单「摘要」置首**，**未动任何其他模块**（`task-detail.html` / `base.html` 一字未动）。
> ① **「在系统打开」拆成「另存为 / 打开所在文件夹」→ 已做**。`part108/_mods.html` 里那枚 `data-td-prev-open`
>   换成两枚 `data-td-prev-save` / `data-td-prev-reveal`（`panel.js` 各挂一条 `say(...)` 轻提示，旧分支一并删）。
>   实测 1440：`另存为` `[1223,100,69,26]` + `打开所在文件夹` `[1298,100,121,26]`，栏 `[792,93,639,40]`
>   ⇒ **右缘 1419 = 栏内容右缘、栏高仍 40**（修复前单枚 `在系统打开` `[1324,100,95,26]`）。
> ② **侧栏标题栏去掉「最大化侧栏」→ 已做**。按钮落在 `.td-browse-acts` 里（**不在** `.td-mod-bar`），
>   连同 `panel.js` 的整段「最大化 / 还原」逻辑（`maxBtn`/`setMax`/`setMaxIcon`/`applyMaxW`/`data-td-maxw` 读写
>   + `STORE_KEY`/`MIN_PANEL`/`DEF_PANEL`/`MAIN_MIN` 常量）一起清掉（−4039 字符）。
>   实测 `browseActs = ["收起侧栏"]`、`maxBtn = 0`；`data-td-maxw` 全仓只剩 `ctrl-conv.js` 自己 IIFE 里**同名但无关**的量。
> ③ **`td-rv-body` 滚不动 → 已修**。根因 = 它是 **flex 纵列**、子里 `.td-diff` 没写 `flex` ⇒ 默认 `flex: 0 1 auto`
>   **可收缩** ⇒ 装不下就被**压扁**（卡 1 实占 369 / 需 637），而 `.td-diff{overflow:hidden}` 把溢出**裁掉**
>   ⇒ ① `scrollHeight === clientHeight` 恒真（容器永远不滚）② 约 **489px** 内容永久看不见。
>   修法 = `.td-rv-body > .td-diff { flex: none; }`。实测 `bodySz = [757,1212]`、`cardFlex = "0 0 auto"`、
>   逐卡 `clientHeight == scrollHeight`、`scrollTop` 落到 **455**，且 **`pageScrollTopAfter = 0`**、`docOverflow = 0`（页面不再被顶）。
> ④ **`+` 菜单里「摘要」置首 → 已做**。菜单 5 项**整块重排**：`摘要 / 审查 / 终端 / 浏览器 / 文件`（实测 y 98/132/166/200/234 不变）。
> ★ **边界与回归全绿**（`ev/probe108u.sh` + `probe108u2.sh` / `probe108u3.sh`）：另存为 / 打开所在文件夹各命中 1 次、
>   `data-td-prev-open` 0 次；`.td-rv-body > .td-diff { flex: none; }` 恰 1 处；菜单顺序断言过。
> ★ **补丁 = `ev/patch108l7.py`**（**9 步**；七层幂等 `l1 全跳过 / l2 0-8 / l3 0-27 / l4 0-8 / l5 0-10 / l6 0-15 / l7 0-9`）。
> ★★ **本拍九条坑**见 PLAYBOOK **P3.54**（「存在性」断言抓不到「重复应用」⇒ 判据要 `count == 1` / 注释正文里写 `*/` 会提前闭合块注释 / 纯删除类 `mark` 要落「新形成的相邻串」· 能整块重排就别拆两步 / `old` 被 `new` 原样保留要 `strict=False`（第三次）/ 改了跨代资产下游生成器要跟着改来源 / 下游守卫别写裸属性名 / 重建「改前」对照页三件必须齐上 / **flex 纵列 + 可收缩子件 + 父级 `overflow:hidden` = 压扁 + 裁切 + 容器永不滚** / 探针自身也会假失败）。"""

# ==================================================================== HANDOFF 第十八拍段
HOF_18 = u"""
### 第十八拍（r108 第七层补丁 · 四条 · @WHEN@ 邵先生 · 🚫 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **三十五 ~ 三十九节**；机制级教训见 PLAYBOOK **P3.54**。

**需求（逐字）**：

> 1、"td-mod-bar"右侧的按钮"在系统打开"需要拆分为两个按钮，分别是：另存为、打开所在文件夹；
> 2、把"td-browse-bar"栏的"最大化侧栏"按钮去掉；
> 3、"td-mod-body td-rv-body is-worddiff"容器不能滚动页面，需修复；
> 4、把菜单"td-mod-menu giencoder-dropdown-popup giencoder-popup-open"里的"摘要"放在第一个

**① 体位**：第十二 ~ 十七拍**未提交** ⇒ 按「未交付 ⇒ 就地返工」⇒ 本拍 = **第七层补丁** `ev/patch108l7.py`
（**9 步**，**不另起 r109**）。七层各带独立 `mark`；改序仍是下→上：
`part108/{_head.html,_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`（**无需** `make108.py`）。
★ 本拍**新开一份本代覆盖件** `part108/_head.html`（由 `part107/_head.html` 逐字拷贝后打 ②④ 两处），
并**把 `ev/splice108.py` 的 head 来源从 P107 改成 P108**（不改则 ②④ 落不进产物）；`part107/_head.html` **一字未动**。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_head.html`（**新建** 5416 → 4918 字节 / 22 行） | 由 `part107/_head.html` 拷贝；② 删 `.td-browse-acts` 里那枚 `aria-label="最大化侧栏"` 按钮；④ `+` 菜单 5 项整块重排（摘要置首） |
| `part108/_mods.html`（70783 → **71067** 字符） | ① 预览工具条 `data-td-prev-open="1"` 那枚改两枚 `data-td-prev-save="1"` / `data-td-prev-reveal="1"` + 一条留痕注释 |
| `part108/panel.css`（75956 → **76769** 字符 / 1599 行） | ③ 追加 `.td-rv-body > .td-diff { flex: none; }` + 19 行注释；插入 `/* r108-l7 */`（**把 `/* r108-l6 */` 原样接回**） |
| `part108/panel.js`（72690 → **69623** 字符 / 1595 行） | ① `prevPane` 分支挂两条处理器、删旧 `prevOpenBtn` 分支；② 删整段「最大化 / 还原」逻辑（−4039 字符）+ 留痕注释 + 头注释同步 + 清 `STORE_KEY` / `DEF_PANEL` / `MIN_PANEL` / `MAIN_MIN` |
| `part108/browse.html` | 106445 → **106251**（`splice108.py` 重建；**是产物、不是手改对象**） |
| `ev/splice108.py` | head 来源 P107 → **P108** + 缺件硬失败 + 两条下游守卫（真按钮特征串 / 菜单顺序） |
| `ev/patch108l7.py` | **新建**（9 步；含「mark 歧义」硬断言 + `count == 1` 重复应用断言 + `/*`/`*/` 配平断言） |
| `ev/p108u.js` / `p108u2.js` · `probe108u{,2,3}.sh` · `shots108u.sh` | **新建**（十相位探针 / 压扁专项 / 三段执行 / 出图） |
| `ev/bak18/`（post-l7）+ `ev/bak18pre/`（pre-l7） | **新建**（回滚基线；提交前 `git reset`） |

**③ 真机实测（1440×900 / `--ui-fs=14`）**：① `另存为` `[1223,100,69,26]` + `打开所在文件夹` `[1298,100,121,26]`，
栏 `[792,93,639,40]`（右缘 1419 = 栏内容右缘、**栏高仍 40**）；修复前单枚 `在系统打开` `[1324,100,95,26]`；
主证据截图 `raw/u-after-pvbar.png` / 改前 `raw/u-before-pvbar.png`；
② `browseActs = ["收起侧栏"]`、`maxBtn = 0`，截图 `raw/u-before-bar.png`（`[⤢][×]`）→ `raw/u-after-bar.png`（只剩 `[×]`）；
③ 改前 `bodySz = [757,757]`（**`scrollHeight === clientHeight`**）、卡片 `[371,369,637]`（**实占 369 / 需 637**）；
改后 `bodySz = [757,1212]`、`cardFlex = "0 0 auto"`、`scrollTop = 455`、`pageScrollTopAfter = 0`、`docOverflow = 0`；
改前 `raw/u-before-rv-top.png` 与 `raw/u-before-rv-scrolled.png` **逐字节相同**（滚不动），改后两张**不同**；
④ 菜单序 `摘要 / 审查 / 终端 / 浏览器 / 文件`（y 98/132/166/200/234），截图 `raw/u-after-menu.png`。

**④ 排掉的九处坑**（详见 PLAYBOOK **P3.54**）

1. ★★★ **「存在性」断言抓不到「重复应用」**：③ 的 mark 少写一个「★ 」（`/* r108-l7 ③` vs 实际 `/* ★ r108-l7 ③`）⇒ mark **永不命中** ⇒ 补丁**被重复应用**（+799 字符重复块），而当时「存在 `flex: none`」的断言**照样通过**。判据一律写 **`count == 1`**。
2. ★★★ **注释正文里写 `*/` 会提前闭合块注释**：新注释里出现 `` `part*/` `` ⇒ `check-syntax` FAIL（9/10）。判据 = `/*` 与 `*/` 计数配平（本轮 panel.css `141/141`、panel.js `94/94`）。
3. ★★ **纯删除类改动的 mark 必须落「删除后新形成的相邻串」**；**能一次整块重排就别拆两步**（④ 第一版拆「先摘行、再插行」⇒ 终态里 mark 与第 (a) 步的 `old` 同时存在 ⇒ 硬断言 `sys.exit`）。
4. ★★ **`old` 被 `new` 原样保留 ⇒ 必须 `strict=False`**（③ 只在原 `.td-rv-body{…}` 块前追加、块本身逐字保留）—— **第三次踩**（l5 / l6 / l7）。
5. ★★★ **改了跨代资产 ⇒ 下游生成器要跟着改来源**：本拍要动 `_head.html` ⇒ 必须把 `splice108.py` 的 head 来源 P107 改成 P108，并加「缺本代覆盖件即 `sys.exit`」保护。
6. ★★ **下游守卫判据别写裸属性名**：`'data-td-max' in out` 被 `_mods.html` 的 demo diff **转义文本**命中误报 ⇒ 改取真按钮整段特征 `'<button class="td-browse-ico" type="button" aria-label="最大化侧栏"'`。
7. ★★ **重建「改前」页面做对照，三件必须齐上**：只换 `browse.html` 会得到「混合态」（1022451 ≠ 1024705）⇒ 必须 `bak18/browse.html` + `bak18pre/panel.css` + `bak18pre/panel.js` 一起 ⇒ 精确复现 1024705。
8. ★★★ **flex 纵列 + 可收缩子件 + 父级 `overflow:hidden` = 压扁 + 裁切 + 容器永不滚**：`scrollHeight === clientHeight` 会成为**恒真**，用「容器滚不滚」当判据永远看不出问题 ⇒ 判据要量**逐卡 `clientHeight` vs 内容所需高**。
9. ★★ **探针自身也会假失败** —— `p108u2.js` 把「插入点」误写进 `stub()` 函数体、又对已展开项无脑 toggle（净开数恒 0）⇒ 先复核探针再怀疑产品。

**⑤ 产物与门禁**：`conversation.html` 1024705 → **1022257 字符（−2448）**（对 `HEAD` 累计 **`1186 239`** 行）；
工作区 bytes **1141453** / **8442 行** / LF `sha1_lf f3e0bcc1a8e2`；
`task-detail.html` **831606 字节 / 767836 字符（本拍未动，仍 `7 0`）**；`base.html` **490294 字节 / 472150 字符 逐字节不变**。
代数核对：`r108-l7` **7**、`r108-l6` **10**、`data-td-prev-save` / `data-td-prev-reveal` 各 **2**、`data-td-prev-open` **0**、
`.td-rv-body > .td-diff { flex: none; }` **1**、`aria-label="最大化侧栏"` **0**（`data-td-max` **2 处均在 demo diff 转义文本里、有意保留**）。
幂等 ✓（l1 全跳过 / l2 `0/8` / l3 `0/27` / l4 `0/8` / l5 `0/10` / l6 `0/15` / **l7 `0/9`**；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` **76 个问题（66 warning / 10 info / 0 critical）** ｜
`scan-flatten.py part108/panel.css` **2 条**（`.td-mod-bar` / `.td-url` 基线）｜ `gaps.log` pre vs post l7 **逐字节相同**（md5 `81fb5522ffd1f97524c21819df7770fc`）。

**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`
还要 **`git reset -q -- mg-work/r108/ev/bak1[3-8]*`**；`mg-work/r108/part108/` 与 `raw/`、`up/` 照旧入库。
★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。
★ **别忘 `git checkout -- pages/gaps.log`**（本轮它同样被重写）。
★ ★★ **l7 之后若再叠一层（`patch108l8.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l7 */` **也原样接回**（否则 l7 复跑整块重挂）。
"""

HOF_STEPS = [
    # 首行时间戳
    (u'> 最后更新：2026-10-01 22:2x（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条」+「第十七拍 四条（`+` 菜单定位跟随 / 浏览器工具条瘦身 / 文件树抽屉让开标题栏 / diff 加长）」** → 门禁四查全绿 + 真机实测（菜单三场景对齐 + 抽屉几何 + 行数表全绿）→ **🚫 未提交**）',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条」+「第十七拍 四条」+「第十八拍 四条（预览工具条拆「另存为 / 打开所在文件夹」/ 去「最大化侧栏」/ 右栏 diff 滚动修复 / `+` 菜单「摘要」置首）」** → 门禁四查全绿 + 真机实测（工具条几何 + 逐卡可滚 + 菜单序全绿）→ **🚫 未提交**）',
     u'首行时间戳 → 第十八拍'),

    # 降级链条
    (u'> ▸ **上一拍 = r108 第十六拍（三条 · 就地返工，🚫 未提交）**：① 产物预览改挂「预览」页签（旧 `.td-sum-prev` 浮层整体拆除）· ② `.zd-host` 折展动效改「收进 / 摊开右上角」· ③ `.zd-host` 四件改毛玻璃。要点见 PLAYBOOK **P3.52**。',
     u'> ▸ **上一拍 = r108 第十七拍（四条 · 就地返工，🚫 未提交）**：① `+` 菜单纳入 `placeRv` 现场摆位（原吃写死的 `left:64px`，3 页签时 dx = −218px）· ② 删浏览器工具条三枚按钮（连带快门死代码）· ③ `.td-tree` 改 `top:44px` 让开标题栏 · ④ diff 补 46 行。要点见 PLAYBOOK **P3.53**。',
     u'降级链条 · 第十七拍'),
    (u'> ▸ **再上一拍 = r108 第十五拍（六条 · 就地返工，🚫 未提交）**：① `.zd-sec-t` 正文黑 / 500 / 14px · ② `.zd-ico` 补 hover · ③ 「目标」只留 1 条 · ④ 已完成删除线 + 进行中转 loading · ⑤ 骨架屏期隐藏 `.zd-card` · ⑥ `.zd-sec-x` 仅折叠态显示。',
     u'> ▸ **再上一拍 = r108 第十六拍（三条 · 就地返工，🚫 未提交）**：① 产物预览改挂「预览」页签（旧 `.td-sum-prev` 浮层整体拆除）· ② `.zd-host` 折展动效改「收进 / 摊开右上角」· ③ `.zd-host` 四件改毛玻璃。要点见 PLAYBOOK **P3.52**。',
     u'降级链条 · 第十六拍'),
    (u'> 要点与本拍同源，逐条见下方「### 第十七拍」。（其下数行 = 更早各拍，本轮已顺次降级标签。）',
     u'> 要点与本拍同源，逐条见下方「### 第十八拍」。（其下数行 = 更早各拍，本轮已顺次降级标签。）',
     u'降级链条 · 要点行'),

    # §一 状态段
    (u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七拍）＝本代新产物，🚫 未提交**（2026-10-01 22:2x，第十七拍）。工作区：\n**` M pages/conversation.html`（1024705 字符）',
     u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七 + 十八拍）＝本代新产物，🚫 未提交**（@WHEN@，第十八拍）。工作区：\n**` M pages/conversation.html`（1022257 字符）',
     u'§一 状态段 → 第十八拍'),

    # conversation 表行
    (u'→ 1024705（第十七拍 +9610）**；工作区 bytes **1143754** / **8500 行** / LF `sha1_lf cc2105413d08`；',
     u'→ 1024705（第十七拍 +9610）→ 1022257（第十八拍 −2448）**；工作区 bytes **1141453** / **8442 行** / LF `sha1_lf f3e0bcc1a8e2`；',
     u'conversation 表行 → 第十八拍'),
    (u'r108 **十二 ~ 十六拍**见 `mg-work/r108/acceptance.md`（**二十九节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍、二十五 ~ 二十九 = 第十六拍） |',
     u'r108 **十二 ~ 十八拍**见 `mg-work/r108/acceptance.md`（**三十九节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍、二十五 ~ 二十九 = 第十六拍、三十 ~ 三十四 = 第十七拍、三十五 ~ 三十九 = 第十八拍） |',
     u'conversation 表行 · acceptance 节数'),

    # mg-work/r108 表行
    (u'| `mg-work/r108/` | **🚫 未提交（第十二 ~ 十七拍）**：',
     u'| `mg-work/r108/` | **🚫 未提交（第十二 ~ 十八拍）**：',
     u'表行 · 代数标签'),
    (u'`acceptance.md`（**三十四节**）/ **`part108/`**（只覆盖改过的三件：`_mods.html` 51798 → … → 62454 → **70783** 字符 · `panel.css` → … → 74888 → **75956** 字符 / 1573 行 · `panel.js` → 71160 → 72477 → **72690** 字符；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）',
     u'`acceptance.md`（**三十九节**）/ **`part108/`**（本代**四件**：`_head.html` **4918 字节**（第十八拍**新建**，由 part107 拷贝后打 ②④）· `_mods.html` 51798 → … → 62454 → 70783 → **71067** 字符 · `panel.css` → … → 74888 → 75956 → **76769** 字符 / 1599 行 · `panel.js` → 71160 → 72477 → 72690 → **69623** 字符；`ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）',
     u'表行 · part108 体积'),
    (u'**第十七拍**：`patch108l6.py`（15 步）· `p108t.js` · `probe108t.sh` / `probe108t2.sh` · `bak17/` · `s-raw.log` / `t-raw.log`）',
     u'**第十七拍**：`patch108l6.py`（15 步）· `p108t.js` · `probe108t.sh` / `probe108t2.sh` · `bak17/` · `s-raw.log` / `t-raw.log`；**第十八拍**：`patch108l7.py`（9 步）· `p108u.js` / `p108u2.js` · `probe108u.sh` / `probe108u2.sh` / `probe108u3.sh` · `shots108u.sh` · `bak18/` · `bak18pre/` · `chk18{,b,c}.py` · `u-raw.log` / `u-after-raw.log`）',
     u'表行 · ev 清单补本拍'),
    (u'`t-{menu-4tabs-browse,menu-full,url-after,tree-open,rv-rows}.png`）|',
     u'`t-{menu-4tabs-browse,menu-full,url-after,tree-open,rv-rows}.png` / `u-{before,after}-{menu,bar,pvbar,rv-top,rv-scrolled}.png`）|',
     u'表行 · raw/ 补本拍截图'),

    # §二·h 标题 + 引言行
    (u'2026-10-01 19:4x 起，共**十二 ~ 十七拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'2026-10-01 19:4x 起，共**十二 ~ 十八拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'二·h 标题 → 共十二 ~ 十八拍'),
    (u'> 完整版见 `mg-work/r108/acceptance.md`（**三十四节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.53**；本页固定事实见 PAGES **P3.11i**。',
     u'> 完整版见 `mg-work/r108/acceptance.md`（**三十九节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.54**；本页固定事实见 PAGES **P3.11i**。',
     u'二·h 引言行 → 第十八拍'),
]

# 「### 第十八拍」插在第十七拍段的「⑥ 交接」整块之后（该块末行是 l7 那句）
HOF_18_ANCHOR = (u'★ ★★ **l6 之后若再叠一层（`patch108l7.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l6 */` **也原样接回**（否则 l6 复跑整块重挂）。\n')

# ==================================================================== PAGES
PAG_16 = u"""> **⑯ r108 第十八拍（四条 · 预览工具条拆两枚 / 去「最大化侧栏」/ 右栏 diff 滚动修复 / `+` 菜单「摘要」置首）**：
> 　① **「在系统打开」拆成两枚** —— `.td-prev-btn[data-td-prev-open]` → `[data-td-prev-save]`（另存为）+ `[data-td-prev-reveal]`（打开所在文件夹），
> 　　`panel.js` 各挂一条轻提示；实测 1440 `另存为` `[1223,100,69,26]` + `打开所在文件夹` `[1298,100,121,26]`，栏 `[792,93,639,40]`（**栏高仍 40**、右缘 1419 = 栏内容右缘）；
> 　② **去掉「最大化侧栏」** —— 按钮在 `.td-browse-acts`（**不在** `.td-mod-bar`），连同 `panel.js` 整段「最大化 / 还原」逻辑
> 　　（`maxBtn`/`setMax`/`setMaxIcon`/`applyMaxW`/`data-td-maxw` + `STORE_KEY`/`MIN_PANEL`/`DEF_PANEL`/`MAIN_MIN`）一起清；实测 `browseActs = ["收起侧栏"]`、`maxBtn = 0`；
> 　③ **`td-rv-body` 滚不动 → 已修** —— 根因是 **flex 纵列 + 子件默认 `flex: 0 1 auto`（可收缩）+ `.td-diff{overflow:hidden}`**
> 　　⇒ 卡片被**压扁**（卡 1 实占 369 / 需 637）、溢出被**裁掉**，`scrollHeight === clientHeight` 恒真（容器永不滚）、约 **489px** 内容永久看不见；
> 　　修法 = `.td-rv-body > .td-diff { flex: none; }`；实测改前 `bodySz = [757,757]` / 卡片 `[371,369,637]`；
> 　　改后 `bodySz = [757,1212]` / `cardFlex = "0 0 auto"` / `scrollTop = 455` / **`pageScrollTopAfter = 0`**、`docOverflow = 0`；
> 　④ **`+` 菜单「摘要」置首** —— 5 项**整块重排** ⇒ `摘要 / 审查 / 终端 / 浏览器 / 文件`（y 98/132/166/200/234 不变）。"""

PAG_15_HEAD = u'> **⑮ r108 第十七拍（四条 · `+` 菜单定位跟随 / 浏览器工具条瘦身 / 文件树抽屉让开标题栏 / diff 加长）**：'

# ==================================================================== PLAYBOOK P3.54
PBK_P354 = u"""## P3.54 ★★ r108 第十八拍（四条 · @WHEN@ 邵先生）—— ★★ 九条新教训

**① ★★★ 「存在性」断言抓不到「重复应用」——判据一律写 `count == 1`**

* 本拍真踩：③ 的 `mark` 少写一个「★ 」（写成 `/* r108-l7 ③`，实际注释是 `/* ★ r108-l7 ③`）
  ⇒ mark **永不命中** ⇒ `edit()` 每次都「新插一块」，补丁被**重复应用两次**（panel.css 多出 799 字符重复块）。
* ⚠ 最坑的是当时那条断言写的是「**存在** `.td-rv-body > .td-diff { flex: none; }`」——**照样通过**。
* ★ 结论：**凡「只该出现一次」的注入，判据就必须是 `count == 1`**；「存在性」只能证明「至少一次」。

**② ★★★ 注释正文里写 `*/` 会提前闭合块注释**

* 本拍真踩：新注释里出现 `` `part*/` `` —— 那个 `*/` **在块注释内提前闭合**，后面的注释正文被当成 JS 代码
  ⇒ `check-syntax` FAIL（9/10）。
* ★ 判据 = **`/*` 与 `*/` 计数配平**（本轮 panel.css `141/141`、panel.js `94/94`），
  收尾断言里固定写一条。⚠ 与「注释里别嵌注释」同族，但这次嵌的是**结束符**。

**③ ★★ 纯删除类改动的 `mark` 必须落「删除后新形成的相邻串」；★ 能一次整块重排就别拆两步**

* ④「摘要置首」第一版拆成「先摘掉那一行、再插到标题后」两步 ⇒ 终态里 mark（标题紧跟摘要）
  与第 (a) 步的 `old`（摘要那一行）**同时存在** ⇒ 硬断言 `sys.exit`。
* ★ 改成**一次性整块重排**（`old` = 原顺序 5 行、`new` = 重排后 5 行）后两遍皆稳。
* ★ 原则：**能一次整块重排就别拆两步**；非拆不可时，要保证**中间态的 mark 在终态消失**。

**④ ★★ `old` 被 `new` 原样保留 ⇒ 必须显式 `strict=False`**（**第三次踩**）

* ③ 只在原 `.td-rv-body{…}` 块**前面**追加一条新规则，块本身**逐字保留**在 `new` 里
  ⇒ 复跑时 `old` 仍命中、与 mark 同时存在 ⇒ 被误判「mark 不唯一」。
* ★ 豁免判据 = `old in new`。l5 / l6 / l7 三次同源 ⇒ **已固化成写 `edit()` 时的默认自问**。

**⑤ ★★★ 改了跨代资产 ⇒ 下游生成器必须跟着改来源**

* `.td-browse-acts` 那枚「最大化侧栏」按钮在 **`_head.html`** 里，而 `_head.html` 是**跨代资产**
  （`part108/` 本来只覆盖改过的三件，head 三级回落取 part107）⇒ 本拍必须**新开本代覆盖件**
  `part108/_head.html`，并**把 `splice108.py` 的 head 来源从 P107 改成 P108** —— 不改则 ②④ **落不进产物**。
* ★ 配套加「缺本代覆盖件即 `sys.exit`」硬失败保护。★ 同时确认 `part107/_head.html` **一字未动**。

**⑥ ★★ 下游守卫判据别写裸属性名**

* `splice108.py` 新加的守卫写成 `'data-td-max' in out` ⇒ 被 `_mods.html` 的 **demo diff 转义文本**
  （`&lt;button … data-td-max="1"&gt;`）命中 ⇒ **误报**。
* ★ 改取**真按钮整段特征**：`'<button class="td-browse-ico" type="button" aria-label="最大化侧栏"'`。
* ★ 同族（P3.53 ③「裸属性名计数」）第二次踩 ⇒ **判据要表达「意图」，不是「某个字面量出现过」**。

**⑦ ★★ 重建「改前」页面做对照，三件必须齐上**

* 本拍要证明「零 token 缺口回归」，需要重建 pre-l7 的 `conversation.html` 跑 `verify-design`。
  第一次只换 `browse.html`（而 `panel.css` / `panel.js` 还是 post-l7）⇒ 得到**混合态 1022451 ≠ 1024705**。
* ★ 正解 = `bak18/browse.html` + `bak18pre/panel.css` + `bak18pre/panel.js` **三件一起** ⇒ 精确复现 1024705，
  `gaps.log` 与基线**逐字节相同**（md5 `81fb5522ffd1f97524c21819df7770fc`）。
* ★ 原则：**「改前态」= 一组文件的联合状态，不是某一个文件**。

**⑧ ★★★ flex 纵列 + 可收缩子件 + 父级 `overflow:hidden` = 压扁 + 裁切 + 容器永不滚**

* `td-rv-body` 滚不动的根因：它是 `display:flex; flex-direction:column`，子件 `.td-diff` **没写 `flex`**
  ⇒ 默认 `flex: 0 1 auto`（**可收缩**）⇒ 装不下就被**压扁**（实测卡 1 实占 369px / 内容需 637px），
  而 `.td-diff{overflow:hidden}` 再把溢出**裁掉** ⇒ ① `scrollHeight === clientHeight` **恒真**（容器永远不滚）
  ② 约 **489px** 内容永久看不见。
* ★★ 因此**「容器滚不滚」这个判据永远看不出问题**（它恒为「不滚」）⇒ 判据要量
  **逐卡 `clientHeight` vs 内容所需高**（或逐个 `.td-diff` 的 `scrollHeight`）。
* ★ 修法 = `.td-rv-body > .td-diff { flex: none; }` ⇒ 改后 `bodySz = [757,1212]`、`cardFlex = "0 0 auto"`、
  逐卡 `clientHeight == scrollHeight`、`scrollTop` 落到 **455**。
* ⚠ 伴生：修好容器滚动后要**同时确认页面本身没被顶**（实测 `pageScrollTopAfter = 0`、`docOverflow = 0`）——
  否则「容器能滚了、整页也跟着滚」= 换了个毛病。

**⑨ ★★ 探针自身也会假失败 —— 别先怀疑产品**

* 本拍 `p108u2.js`（压扁假设专项）两处自身 bug：① 把「插入点」误写进 `stub()` **函数体**里；
  ② 对已展开项无脑 toggle（`净开数` 恒 0，看着像「展开失效」）。
* ★ 排查顺序：**先复核探针的每一处写入/点击是否落在预期元素上**，再怀疑产品。

"""

MEASURE = u"""
**★ 判据速查（本轮实测值）**：`另存为` `[1223,100,69,26]` / `打开所在文件夹` `[1298,100,121,26]`，栏高 **40**、右缘 1419；
`browseActs = ["收起侧栏"]` / `maxBtn = 0`；`.td-rv-body` 改前 `[757,757]` → 改后 `[757,1212]`，
`cardFlex = "0 0 auto"` / `scrollTop = 455` / `pageScrollTopAfter = 0` / `docOverflow = 0`；
菜单序 `摘要 / 审查 / 终端 / 浏览器 / 文件`。

---
"""

# ==================================================================== MEMORY（仓库）
MEM_18 = u"""
### 第十八拍（r108 第七层补丁 · 四条 · @WHEN@ · 🚫 未提交）

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
"""

LOG_18 = u"""
### 第十八拍（r108 第七层补丁 · 四条 · @WHEN@ 邵先生 · 🚫 未提交）

**需求**：① `td-mod-bar` 右侧「在系统打开」拆为「另存为 / 打开所在文件夹」；② 去掉 `td-browse-bar` 的「最大化侧栏」；
③ `td-mod-body td-rv-body is-worddiff` 容器滚不动，需修复；④ `td-mod-menu` 里「摘要」放到第一个。

**体位**：第十二 ~ 十七拍未提交 ⇒ 就地返工 ⇒ 本拍 = **第七层补丁** `ev/patch108l7.py`（9 步，不另起 r109）。
★ 新开本代覆盖件 `part108/_head.html`（由 part107 拷贝后打 ②④）+ `splice108.py` head 来源 P107 → **P108**（否则 ②④ 落不进产物）。

**四条落地（真机实测 / 1440×900 / `--ui-fs=14`）**：
① `data-td-prev-open` → `data-td-prev-save` + `data-td-prev-reveal` ⇒ `另存为` `[1223,100,69,26]` + `打开所在文件夹` `[1298,100,121,26]`，
栏 `[792,93,639,40]`（右缘 1419 = 栏内容右缘、**栏高仍 40**）；改前单枚 `在系统打开` `[1324,100,95,26]`；
② `browseActs = ["收起侧栏"]` / `maxBtn = 0`；整段最大化 JS 清空（−4039 字符）；
③ `.td-rv-body > .td-diff { flex: none; }` ⇒ 改前 `[757,757]` / 卡片 `[371,369,637]` → 改后 `[757,1212]` / `cardFlex "0 0 auto"` /
`scrollTop 455` / `pageScrollTopAfter 0` / `docOverflow 0`；
④ 菜单序 `摘要 / 审查 / 终端 / 浏览器 / 文件`（y 98/132/166/200/234 不变）。

**九条坑**（→ PLAYBOOK **P3.54**）：① 「存在性」断言抓不到「重复应用」⇒ 判据要 **`count == 1`**（mark 少写「★ 」⇒ 补丁重复应用两次 +799 字符，
而「存在 `flex:none`」断言照样过）；② 注释正文里写 `*/`（`` `part*/` ``）**提前闭合块注释** ⇒ `check-syntax` FAIL（panel.css 141/141、panel.js 94/94 配平）；
③ 纯删除类 mark 要落「删除后新形成的相邻串」·**能一次整块重排就别拆两步**；④ `old` 被 `new` 原样保留 ⇒ 显式 `strict=False`（第三次，l5/l6/l7）；
⑤ **改了跨代资产 ⇒ 下游生成器要跟着改来源**（`splice108.py` head P107→P108 + 缺件硬失败）；⑥ 下游守卫别写裸属性名（`data-td-max` 被 demo diff 转义文本误报 ⇒ 取真按钮整段特征）；
⑦ 重建「改前」对照页**三件必须齐上**（只换 browse.html = 混合态 1022451 ≠ 1024705）；⑧ **flex 纵列 + 可收缩子件 + 父级 `overflow:hidden` = 压扁 + 裁切 + 容器永不滚**
（`scrollHeight === clientHeight` 恒真 ⇒ 判据要量逐卡 `clientHeight` vs 内容所需高）；⑨ 探针自身也会假失败（`p108u2.js` 把插入点写进 `stub()` 函数体 / 无脑 toggle）。

**产物 / 门禁**：`part108/_head.html` **4918 字节**（新建）· `_mods.html` 70783 → **71067** · `panel.css` 75956 → **76769** · `panel.js` 72690 → **69623** ·
`browse.html` 106445 → **106251**（splice 产物）；
`conversation.html` **1024705 → 1022257 字符（−2448）**（对 `HEAD` 累计 **`1186 239`** 行）；工作区 bytes **1141453** / **8442 行** / LF `sha1_lf f3e0bcc1a8e2`；
`task-detail.html` **831606 字节 / 767836 字符（本拍未动，仍 `7 0`）**；`base.html` **490294 字节 逐字节不变**。
七层幂等（l1 全跳过 / l2 0-8 / l3 0-27 / l4 0-8 / l5 0-10 / l6 0-15 / **l7 0-9**）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` **76 个问题（66 warning / 10 info / 0 critical）** ｜
`scan-flatten.py part108/panel.css` **2 条**（基线）｜ `gaps.log` pre vs post l7 **逐字节相同**（md5 `81fb5522ffd1f97524c21819df7770fc`）｜ `pages/gaps.log` 已 `git checkout --` 清理。
**验收** `mg-work/r108/acceptance.md` **三十九节**（三十五 ~ 三十九 = 第十八拍）；**记忆同步** `ev/doc108t.py`（本文件）。
🚫 未 commit / 未 push。
"""

# ==================================================================== 工作区 MEMORY
WSM_STEPS = [
    (u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.53** + 附录「工作区速览 77 条」·',
     u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.54** + 附录「工作区速览 86 条」·',
     u'头部版本号 → P3.54 / 86 条'),
    (u'## 二、红线索引（完整 77 条见仓库 PLAYBOOK 附录）',
     u'## 二、红线索引（完整 86 条见仓库 PLAYBOOK 附录）',
     u'红线索引标题 → 86 条'),
    (u'- 可选子部件**一律判空**（含探针侧）；探针假失败六类（时序 / 过渡中取值 / `display:none` / 截图框错 / `scale=none` / 选择器层级错）。',
     u'- 可选子部件**一律判空**（含探针侧）；探针假失败七类（时序 / 过渡中取值 / `display:none` / 截图框错 / `scale:none` / 选择器层级错 / 探针自身 bug）。',
     u'探针假失败 → 七类'),
    (u'- **r108 十二 ~ 十七拍**（🚫 未提交 · **同一代就地返工**）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 六条（含复刻 ZCode 右上角 `.zd-card`）；十四 = `.zd-card` 四条；十五 = 六条（视觉精修 + 骨架屏门控）；十六 = 三条（预览改挂页签 / 折展改右上角锚点 / `.zd-host` 毛玻璃）；**十七 = 四条** —— `+` 菜单纳入 `placeRv` 现场摆位（原吃写死的 `left:64px`，3 页签时 **dx = −218px**）· 删浏览器工具条三枚按钮（连带快门死代码）· `.td-tree` 改 `top:44px` 让开标题栏 · diff 补 46 行。',
     u'- **r108 十二 ~ 十八拍**（🚫 未提交 · 就地返工）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 复刻 ZCode `.zd-card` 六条；十四 = `.zd-card` 四条；十五 = 视觉精修六条；十六 = 预览改挂页签 / 折展右上角 / 毛玻璃；十七 = `+` 菜单纳入 `placeRv` · 删浏览器工具条三枚 · `.td-tree` 让开标题栏 · diff 补 46 行；**十八 = 四条** —— 预览「在系统打开」拆**另存为 / 打开所在文件夹** · 删「最大化侧栏」（含 JS）· **`.td-rv-body>.td-diff{flex:none}`**（原 flex 子件被压扁+裁掉⇒永不滚）· `+` 菜单**摘要置首**。',
     u'最近拍 · 第十八拍'),
    (u'- 补丁链 `ev/patch108{l1~l6}.py`；产物 `conversation.html` **1024705 字符**（`1146 / 142` 行）、`task-detail.html` **767836（未动）**、`base.html` 逐字节不变；`acceptance.md` **三十四节**。',
     u'- 补丁链 `ev/patch108{l1~l7}.py`；产物 `conversation.html` **1022257 字符**（`1186 / 239` 行）、`task-detail.html` 未动、`base.html` 不变；`acceptance.md` **三十九节**。',
     u'补丁链 / 产物 → 第十八拍'),
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
    span(HOF, u'> ⚠️ **最新一拍 = r108 第十七拍', u'> ★★ **本拍八条坑**见 PLAYBOOK **P3.53**',
         HOF_TOP, u'HANDOFF', u'顶部「最新一拍」块整块换新（第十七拍降级为「上一拍」）')
    patch(HOF, HOF_STEPS, u'HANDOFF')
    patch(HOF, [(HOF_18_ANCHOR, HOF_18_ANCHOR + HOF_18, u'二·h 段末追加「### 第十八拍」')], u'HANDOFF')

    print(u'=== 2/7 PAGES.md ===')
    patch(PAG, [
        (u'（r107 十一拍 + **r108 十二 ~ 十七拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十七拍**）',
         u'（r107 十一拍 + **r108 十二 ~ 十八拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十八拍**）',
         u'P3.11i 标题 → 共十八拍'),
        # ★ ⑯ 段插在 ⑮ 段**之前**（新段在上）—— 锚点 = ⑮ 段的首行，原样接回
        (PAG_15_HEAD, PAG_16 + u'\n' + PAG_15_HEAD, u'P3.11i 在 ⑮ 前插入 ⑯ 第十八拍要点'),
    ], u'PAGES')

    print(u'=== 3/7 PLAYBOOK.md ===')
    patch(PBK, [
        # 一步同时完成「在其前插入 P3.54 + 判据速查」+「标题 77 → 86 条」
        (u'## 附：工作区速览 77 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         PBK_P354 + MEASURE + u'## 附：工作区速览 86 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         u'附录前插入 P3.54 + 标题 → 86 条'),
        (u'（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**、**第十七拍加到 77 条**，工作区实测 **2989 字符**），',
         u'（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**、**第十七拍加到 77 条**、**第十八拍加到 86 条**，工作区实测 **@WSMCHARS@ 字符**），',
         u'附录引言 → 86 条'),
        (u'77. ★ **收尾两跑都会污染工作区** —— `check-syntax` / `verify-design` 各自重写产物；`verify-design` 还会重写 **`pages/gaps.log`**（行号漂移）⇒ 一律 `git checkout --`。',
         u'77. ★ **收尾两跑都会污染工作区** —— `check-syntax` / `verify-design` 各自重写产物；`verify-design` 还会重写 **`pages/gaps.log`**（行号漂移）⇒ 一律 `git checkout --`。\n'
         u'78. ★★★ **「存在性」断言抓不到「重复应用」** —— 判据一律写 **`count == 1`**；本轮 ③ 的 `mark` 少写一个「★ 」⇒ mark **永不命中** ⇒ 补丁**被重复应用**（+799 字符重复块），而「存在 `flex: none`」的断言**照样通过**。\n'
         u'79. ★★★ **注释正文里写 `*/`（如 `part*/`）会提前闭合块注释** ⇒ 后面的注释正文被当成代码 ⇒ `check-syntax` FAIL；判据 = **`/*` 与 `*/` 计数配平**（本轮 panel.css `141/141`、panel.js `94/94`）。\n'
         u'80. ★★ **纯删除类改动的 `mark` 必须落「删除后新形成的相邻串」**；★ **能一次整块重排就别拆两步**（拆了要保证**中间态的 mark 在终态消失**，否则复跑触发「mark 歧义」硬断言 `sys.exit`）。\n'
         u'81. ★★ **`old` 被 `new` 原样保留 ⇒ 必须显式 `strict=False`** —— **第三次踩**（l5 / l6 / l7 同一类）；豁免判据 = `old in new`。\n'
         u'82. ★★★ **改了跨代资产 ⇒ 下游生成器要跟着改来源** —— 本拍要动 `_head.html` ⇒ `splice108.py` 的 head 来源必须 **P107 → P108**（否则改动落不进产物）+ 加「缺本代覆盖件即 `sys.exit`」保护。\n'
         u'83. ★★ **下游守卫判据别写裸属性名** —— `\'data-td-max\' in out` 被 `_mods.html` 的 demo diff **转义文本**（`&lt;button … data-td-max="1"&gt;`）命中误报 ⇒ 改取**真按钮整段特征**。\n'
         u'84. ★★ **重建「改前」页面做对照，三件必须齐上**（`browse.html` + `panel.css` + `panel.js`）—— 只换一件会得到「混合态」（实测 1022451 ≠ 1024705）；**「改前态」是一组文件的联合状态，不是某一个文件**。\n'
         u'85. ★★★ **flex 纵列 + 可收缩子件 + 父级 `overflow:hidden` = 压扁 + 裁切 + 容器永不滚** —— 子件未写 `flex` ⇒ 默认 `flex: 0 1 auto` 可收缩 ⇒ 被压扁（卡 1 实占 369 / 需 637），`overflow:hidden` 再把溢出裁掉 ⇒ `scrollHeight === clientHeight` **恒真**（用「容器滚不滚」当判据永远看不出问题）⇒ 判据要量**逐卡 `clientHeight` vs 内容所需高**；修法 `.td-rv-body > .td-diff { flex: none; }`。\n'
         u'86. ★★ **探针自身也会假失败** —— 别先怀疑产品：`p108u2.js` 把「插入点」误写进 `stub()` 函数体、又对已展开项无脑 toggle（净开数恒 0）⇒ 假失败。',
         u'附录追加 78~86 九条'),
    ], u'PLAYBOOK')

    print(u'=== 4/7 MEMORY.md（仓库） ===')
    patch(MEM, [(None, MEM_18, u'追加第十八拍段')], u'MEMORY')

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
    patch(LOG_REPO, [(None, LOG_18, u'追加第十八拍段')], u'log-repo')

    print(u'=== 7/7 log-ws ===')
    patch(LOG_WS, [(None, LOG_18, u'追加第十八拍段')], u'log-ws')

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
