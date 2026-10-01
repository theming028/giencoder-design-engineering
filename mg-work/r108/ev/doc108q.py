# -*- coding: utf-8 -*-
u"""r108 第十五拍收尾：把「六条（`.zd-card` 视觉精修 + 骨架屏门控）」同步进记忆文档。

★ 代数体位：第十二 / 十三 / 十四拍**均未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 第十五拍同样是
  **就地返工**、**不另起 r109**、**不另开一组记忆段** —— 全部并入 r108 既有段落
  （节标题由「十二 + 十三 + 十四拍」升为「十二 + 十三 + 十四 + 十五拍」）。

范围（同步「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行 + 顶部「最新一拍」块整块换新（第十四拍降级为「上一拍」、
                                      第十三 / 十二拍顺次降级）+ §一 状态段 + conversation 表行
                                      + mg-work/r108 表行（四小步）+ 二·h 引言行 + 二·h 段末追加「### 第十五拍」
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十四拍」→「共十五拍」+ 追加 ⑬ 要点行
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录「工作区速览 58 条」→「63 条」+ 新增 59~63 五条 + 在其前插入 P3.51
  4) .workbuddy/memory/MEMORY.md    —— r108 段追加第十五拍要点（并把 L301 的附录条数改成 63）
  5) 两份 2026-10-01.md（仓库内 + 工作区）—— 追加第十五拍段

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换另给显式 mark。
★★ 本轮新增「**mark 歧义**」硬断言（P3.51 ① 的由来）：mark 与 old **同时**存在 ⇒ 只可能是 mark 不唯一
   ⇒ `sys.exit`。⚠ 判据是 `old in new` —— 凡是「把锚点原样保留在 new 里」的写入（尾部追加 / 插在锚点前
   并把锚点接回）豁免，因为那类步骤**本来就要求锚点留下当下层契约**。
★ 用法： python ev/doc108q.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc108q.py --check    # 只校验锚点命中数（不写）
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

WHEN = u'2026-10-01 21:1x'

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
    """把「以 <first_pre> 起、以 <last_pre> 含」的**连续若干行**整段换掉。

    顶部的「最新一拍」块每轮都要整块换新 ⇒ 首尾各给一个行首前缀即可定位，
    比把 30 行老文本抄成正则稳（老文本会随每轮改动漂移）。
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
HOF_TOP = u"""> ⚠️ **最新一拍 = r108 第十五拍（六条 · ★★ 就地返工、未另起代数）** —— 第十二 / 十三 / 十四拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> 本拍是 **`.zd-card`（ZCode 右上角任务信息面板）的视觉精修 + 骨架屏门控**，**未动任何其他模块**（`part108/panel.js` 一字未改）。
> ① **`.zd-sec-t` 标题文字 = 正文黑 + 中粗 500 + 14px → 已做**：去掉 `font-size/color: inherit`，显式 `font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1)`；
>   三个分区标题（Git 工具 / 目标 / 进程）实测**全部** `fs 14px` / `fw 500` / `color rgb(31,31,31)`；顺带删掉已成**死规则**的 `.zd-sec-t:hover { color: text-1 }`。
> ② **`.zd-card` 内操作图标补 hover → 已做**：`.zd-ico` 由「只有宽高」改成照本页既有口径 **`.td-browse-ico` 的完整契约**
>   （`inline-flex` / `24×24` / `padding:0` / `border:0` / `border-radius:4px` / 透明底 / `color:var(--color-text-2)`）+ 同块内 `:hover { background: var(--color-fill-1); color: var(--color-text-1) }`（硬规则 28：**基态在前**）；
>   真鼠标 hover「收起为胶囊」实测 `bg rgba(0,0,0,0) → **rgb(247,247,247)**`（= `--color-fill-1`）、`color rgb(78,78,78) → **rgb(31,31,31)**`（= `--color-text-1`），两枚 `.zd-ico` 都拿到了这套规则。
>   ★ 伴生变化（记录在案）：`.zd-ico` 原本**没有任何 `color` 声明** ⇒ 头部那枚继承 `text-1`、分区头那枚继承 `text-3`，两枚深浅不一致；改后**基态统一 `text-2`**、hover 统一 `text-1`。
> ③ **「目标」只留 1 条 → 已做**：`_mods.html` 删掉带圆序号那条（`drop_re` 连前导换行一起删、不留空行）⇒ `.zd-it` **1** 行 / `.zd-it-no` **0** / `.zd-it-i` **1**，保留「落地审查、终端、浏览器、摘要四个面板 · 3/4」。
> ④ **已完成进程加删除线 / 进行中 loading 转起来 → 已做**：`is-done`（3 条）`text-decoration: line-through` + `color rgb(134,134,134)`；
>   `is-doing::before` 压到 `opacity:.28`、`::after` 画一段 `primary-6` 实心弧 + `@keyframes zd-todo-spin`；
>   实测 `animationName **zd-todo-spin**` / `duration **0.82s**` / `iterationCount **infinite**` / `radius 50%` / `borderTopColor **rgb(55,112,247)**`；
>   **两次采样（间隔 320ms）的 `transform` 矩阵不同**（atan2 角度 81° → 12°）⇒ 确实在转。
>   ★ **`text-decoration` 不传播到绝对定位伪元素** ⇒ 删除线只划文字，绿圈与对勾不受影响（截图复核过）。
> ⑤ **骨架屏期不显示 `.zd-card` → 已做**：一条**纯 CSS 门控** `html:has(.r93-sk) .zd-host { display: none }`（骨架屏一从 DOM 移除即自动失效、零 JS）；
>   `CSS.supports('selector(html:has(.r93-sk))')` = **true**；注入假 `.r93-sk` ⇒ `display **none**`（cardRect 全 0）→ 移除 ⇒ 回到 `flex`；
>   ★ **真实加载期时序**（`open` 后立刻装 rAF 采样器）：`[[0,"none",true],[144,"flex",false]]`。
> ⑥ **`.zd-sec-x` 只在折叠态显示 → 已做**：基态 `display:none` + `.zd-sec.is-closed .zd-sec-x { display: flex }`（两者特异性 **(0,1,0) vs (0,3,0)** ⇒ 不涉硬规则 24 的「打平」）；
>   实测默认（全展开）三个分区 trailing **全 `none`**；折叠「目标」后该分区 `flex`（可见「2 分 18 秒 · ⏸」）且 `bodyRows 0px`；再展开回 `none`。
> ★ **边界与回归全绿**（`ev/probe108q.sh`）：暗色（card `rgb(35,35,36)` / 标题 `rgb(247,247,247)` / done `rgb(169,169,169)` / 弧 `rgb(84,151,255)` / **`hexLeak: []`**）/
>   `--ui-fs=18`（标题 `18px` + `fw 500`、分区头 `41.14px`、图标盒仍 `24px`、卡片 `[1095,105,320,512]`）/ 窄档 620（`overflowRight -17` / `inView true`）。
> ★ **补丁 = `ev/patch108l4.py`**（**8 项**；四层幂等 `l1 全跳过 / 0-8 / 0-27 / 0-8`，4/4 跨层标记兜底断言「全部存活 ✓」）。
> ★★ **本拍五条坑**见 PLAYBOOK **P3.51**（`mark` 撞车 ⇒ 静默跳过 / 持续旋转时长写进自定义属性 / `:has()` 纯 CSS 门控 + 探针要 `try/catch` / `text-decoration` 不传播伪元素 / 自检判据别用太短片段）。

> ▸ **上一拍 = r108 第十四拍（四条 · 就地返工，🚫 未提交）**：① Git 三行接交互 / ② 删「计划」分区 / ③ 「目标」按上游校准 / ④ 折展与面板 ⇄ 胶囊弹性动效。
> 要点与本拍同源，逐条见下方「### 第十四拍」。（其下数行 = 再上一拍（第十三拍）与更早（第十二拍），本轮已顺次降级标签。）"""

HOF_15 = u"""
### 第十五拍（r108 第四层补丁 · 六条 · @WHEN@ 邵先生 · 🚫 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **十九 ~ 二十四节**；机制级教训见 PLAYBOOK **P3.51**。

**需求（逐字）**：

> 1、"`.zd-sec-t`"的标题文字都使用正文黑色，且中粗500，字号14px；
> 2、"zd-card"容器里的操作图标都少了hover效果，需补充；
> 3、"目标"模块里面保留一个目标即可；
> 4、已完成的"进程"灰色标题加上删除线，进行中的进程要loading转起来；
> 5、conversation.html 页面在显示骨架屏时不应该显示"zd-card"；
> 6、"zd-sec-h"里的"zd-sec-x"只有在折叠状态时才显示，展开时不显示。

**① 体位**：第十二 / 十三 / 十四拍**未提交** ⇒ 按「未交付 ⇒ 就地返工」⇒ 本拍 = **第四层补丁** `ev/patch108l4.py`
（**8 项**，**不另起 r109**）。四层各带独立 `mark`；改序仍是下→上：
`part108/{_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`（**无需** `make108.py`）。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_mods.html`（62859 → **62701** 字符 / 441 行） | 删「目标」区圆序号那一行（`drop_re` 连前导换行一起删）⇒ `.zd-it` 2 行 → **1 行** |
| `part108/panel.css`（70729 → **73063** 字符 / 1531 行） | 6 处就地改：① `.zd-sec-t` 字号/字重/色 + 删死规则 · ② `.zd-ico` 换 `.td-browse-ico` 那套 + `:hover` · ④ `is-done` 删除线 + `is-doing::after` 旋转环 + `@keyframes zd-todo-spin` · ⑥ `.zd-sec-x` 基态 `none` + `.is-closed` 下 `flex`；另插 ⑤ 的 `html:has(.r93-sk)` 门控；末尾加 `/* r108-l4 */` 并把 `/* r108-l3 */` **原样接回** |
| `part108/panel.js` | **71160 字符，一字未动** |
| `part108/browse.html` | 98521 → **98363**（`splice108.py` 重建；**是产物、不是手改对象**） |
| `ev/patch108l4.py` | **新建**（8 项；含「`mark` 歧义」硬断言 + `strict=False` 豁免位） |
| `ev/p108q.js` / `p108q2.js` / `probe108q.sh` | **新建**（六条真机探针 / 加载期 rAF 时序采样器 / 执行链） |
| `ev/bak15-panel.css` / `bak15-mods.html` | **新建**（首跑翻车后的回滚基线；提交前 `git reset`） |

**③ 真机实测（1440）**：① 三个 `.zd-sec-t` **全** `fs 14px` / `fw 500` / `rgb(31,31,31)`（`lh 21px` 未声明、由行盒给出）；
② 真鼠标 hover ⇒ `bg rgb(247,247,247)` + `color rgb(31,31,31)`（`icoN:2`）；③ `.zd-it` 1 / `.zd-it-no` 0；
④ `deco: line-through` + 旋转 **0.82s / infinite**（角度 81° → 12°）；⑤ `display none ⇄ flex` + 真实加载期 `[[0,"none",true],[144,"flex",false]]`；
⑥ 默认三档 trailing 全 `none` → 折叠「目标」`flex` → 再展开 `none`。

**④ 排掉的五处坑**（详见 PLAYBOOK **P3.51**）

1. ★★ **`mark` 撞车 ⇒ 整条改动被静默跳过**：① 的 mark 初稿取改后的声明串，与上文 `.td-sum-prev-t b` 那条**逐字相同** ⇒ 首跑判「已应用」、**① 根本没写进去**，末行照样打印「应用 N 项」。⇒ 给 `edit()` 加**「`old` 与 `mark` 同时存在即报错」**的硬断言 + 类外豁免位（初跑当场被逮到，回滚 `bak15-*` 重来）。
2. ★★ **`verify-design.py` 的 CRAFT-ANIM 是「按行扫 `animation|transition … <数字>ms`」** ⇒ ④ 直接写 `animation: zd-todo-spin 820ms` 会新增 1 条 warning、门禁 md5 就不再等于基线 ⇒ 时长写进**自定义属性** `--zd-spin-dur: 820ms`，解释性注释也拆成「不含 `ms` 数字」的行。
3. **自检判据自己写错两处**：`'.zd-sec-x {'` 会被同层新加的 `.zd-sec.is-closed .zd-sec-x {` 一起命中；`zd-todo-spin` 天然出现 2 次（`animation-name` + `@keyframes`）⇒ 判据一律取**「块首那几行」的更大片段**。
4. **探针里 `querySelector('html:has(.r93-sk)')` 在不支持 `:has()` 的环境抛 `SyntaxError`** ⇒ 整条探针挂死、看起来像「产品坏了」⇒ 必须 `try/catch` 并标 `unsupported:<ErrName>`。
5. **`agent-browser` 没有 `move` 命令** ⇒ 想取消 hover 只能 hover 一个**中性兄弟元素**（本轮用 `.zd-name`）。

**⑤ 产物与门禁**：`conversation.html` 1009968 → **1012144 字符（+2176）**（对 `HEAD` 累计 `896 19` 行）；
LF bytes **1118375** / 工作区 bytes **1126747** / **8373 行** / LF `sha1_lf 12b000018f86`；
`task-detail.html` **767836（本拍未动，仍 `7 0`）**；`base.html` **472150 逐字节不变**。
代数核对：`r108-conv-css` / `r108-conv-js` 各 **1**，`r107-conv-*` / `r106-nav-js` **全 0**。
幂等 ✓（l1 全跳过 / l2 `0/8` / l3 `0/27` / l4 **`0/8`** + 4/4 断言「全部存活 ✓」；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）｜
`scan-flatten.py part108/panel.css` **2 条**（`.td-mod-bar` / `.td-url` 基线）｜ `pages/gaps.log` 已 `git checkout --` 清理。

**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`
还要 **`git reset -q -- mg-work/r108/ev/bak1[345]*`**；`mg-work/r108/part108/` 与 `raw/`、`up/` 照旧入库。
★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。
★ ★★ **l4 之后若再叠一层（`patch108l5.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l4 */` **也原样接回**（否则 l4 复跑整块重挂）。
"""

# ==================================================================== HANDOFF
HOF_STEPS = [
    (u'> 最后更新：2026-10-01 20:5x（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条（zd-card：Git 三行交互 / 删计划 / 目标按上游校准 / 折展与胶囊弹性动效）」** → 门禁四查全绿 + 真机实测（主链八组 + 边界五组全绿）→ **🚫 未提交**）',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条（zd-card 视觉精修 + 骨架屏门控）」** → 门禁四查全绿 + 真机实测（主链六组 + 边界三组全绿）→ **🚫 未提交**）',
     u'首行时间戳 → 第十五拍'),

    # §一 状态段
    (u'★★ **r108（第十二 + 十三 + 十四拍）＝本代新产物，🚫 未提交**（2026-10-01 20:5x，第十四拍）。工作区：\n**` M pages/conversation.html`（1009968 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'★★ **r108（第十二 + 十三 + 十四 + 十五拍）＝本代新产物，🚫 未提交**（@WHEN@，第十五拍）。工作区：\n**` M pages/conversation.html`（1012144 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'§一 状态段 → 第十五拍'),

    # conversation 表行
    (u'★ **r108 态（🚫 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）→ 1009968（第十四拍 +14835）**；LF bytes **1115013** / 工作区 bytes **1123344** / **8332 行** / LF `sha1_lf 73c9ccd93c3d`；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 **十二 + 十三 + 十四拍**见 `mg-work/r108/acceptance.md`（**十八节**，八 ~ 十二 = 第十三拍、十三 ~ 十八 = 第十四拍）',
     u'★ **r108 态（🚫 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）→ 1009968（第十四拍 +14835）→ 1012144（第十五拍 +2176）**；LF bytes **1118375** / 工作区 bytes **1126747** / **8373 行** / LF `sha1_lf 12b000018f86`；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 **十二 ~ 十五拍**见 `mg-work/r108/acceptance.md`（**二十四节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍）',
     u'conversation 表行 → 第十五拍'),

    # mg-work/r108 表行（拆四小步，避开超长单行）
    (u'| `mg-work/r108/` | **🚫 未提交（第十二 + 十三 + 十四拍）**：',
     u'| `mg-work/r108/` | **🚫 未提交（第十二 + 十三 + 十四 + 十五拍）**：',
     u'表行 · 代数标签'),
    (u'`acceptance.md`（**十八节**）/ **`part108/`**',
     u'`acceptance.md`（**二十四节**）/ **`part108/`**',
     u'表行 · acceptance 节数'),
    (u'`_mods.html` 51798 → 59186 → **62859** 字符 · `panel.css` → **70729** 字符 / 1488 行 · `panel.js` → **71160** 字符；',
     u'`_mods.html` 51798 → 59186 → 62859 → **62701** 字符 · `panel.css` → 70729 → **73063** 字符 / 1531 行 · `panel.js` → **71160** 字符（第十五拍未动）；',
     u'表行 · part108 体积'),
    (u'`vd-r108l2b.txt` · `n-raw.log` / `n2-raw.log`）/ `raw/`',
     u'`vd-r108l2b.txt` · `n-raw.log` / `n2-raw.log`；**第十四拍**：`patch108l3.py`（772 行 / 27 项）· `p108p.js` / `p108p2.js` · `probe108p2.sh` · `shots108p.sh` · `pix.py` · `p-raw.log` / `p2-raw.log`；**第十五拍**：`patch108l4.py`（8 项）· `p108q.js` / `p108q2.js` · `probe108q.sh` · `bak15-panel.css` / `bak15-mods.html` · `q-raw.log`）/ `raw/`',
     u'表行 · ev 清单补三拍'),

    # 二·h 引言行
    (u'> 完整版见 `mg-work/r108/acceptance.md`（**十八节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.50**；本页固定事实见 PAGES **P3.11i**。',
     u'> 完整版见 `mg-work/r108/acceptance.md`（**二十四节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.51**；本页固定事实见 PAGES **P3.11i**。',
     u'二·h 引言行 → 第十五拍'),

    # 顶部块下方三行标签顺次降级
    (u'> ▸ **上一拍 = r108 第十三拍（六条 · 就地返工，🚫 未提交）**：',
     u'> ▸ **再上一拍 = r108 第十三拍（六条 · 就地返工，🚫 未提交）**：',
     u'顶部下方 · 第十三拍降级'),
    (u'> ▸ **再上一拍 = r108 第十二拍**：',
     u'> ▸ **更早 = r108 第十二拍**：',
     u'顶部下方 · 第十二拍降级'),
]

HOF_15_ANCHOR = (u'**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`\n'
                 u'还要 **`git reset -q -- mg-work/r108/ev/bak1[34]/ mg-work/r108/ev/bak14b-panel.css`**；`mg-work/r108/raw/` 与 `mg-work/r108/up/` 照旧入库。\n'
                 u'★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；\n'
                 u'**不要**新建 r109、**不要**回头改 `apply107.py`。\n'
                 u'★ ★★ **l3 之后若再叠一层**：新层的 `CSS_TAIL` 必须把 `/* r108-l3 */` **也原样接回**（否则 l3 复跑整块重挂）。\n')

PAG_STEPS = [
    (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三 / 十四拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十四拍**）',
     u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三 / 十四 / 十五拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十五拍**）',
     u'P3.11i 标题 → 共十五拍'),

    (u'> \u3000\u3000⚠ **时长一律 ≤300ms**（`verify-design.py` CRAFT-ANIM 上限）—— 弹性靠过冲、不是靠拉长时长。',
     u'> \u3000\u3000⚠ **时长一律 ≤300ms**（`verify-design.py` CRAFT-ANIM 上限）—— 弹性靠过冲、不是靠拉长时长。\n'
     u'> **⑬ r108 第十五拍（六条 · 全部围绕 `.zd-card` 的视觉与门控）**：\n'
     u'> \u3000① **`.zd-sec-t` = 正文黑 + 中粗 500 + 14px** —— 去 `inherit`，显式 `font-size: var(--font-size-body-3)` + `font-weight: 500` + `color: var(--color-text-1)`；\n'
     u'> \u3000\u3000顺带删掉已成**死规则**的 `.zd-sec-t:hover { color: text-1 }`；\n'
     u'> \u3000② **`.zd-ico` 补 hover** —— 照本页既有 `.td-browse-ico` 的**完整契约**（`inline-flex` / `24×24` / `padding:0` / `border:0` / `radius 4` / 透明底 / `text-2`）\n'
     u'> \u3000\u3000+ 同块内 `:hover { background: var(--color-fill-1); color: var(--color-text-1) }`（**基态在前**，硬规则 28）；⚠ 伴生：`.zd-ico` 原本无 `color` ⇒ 两枚深浅不一致，改后**统一 `text-2`**；\n'
     u'> \u3000③ **「目标」只留 1 条** —— 删带圆序号那行（`drop_re` 连前导换行一起删）⇒ `.zd-it` **1** / `.zd-it-no` **0**；\n'
     u'> \u3000④ **已完成进程加删除线 + 进行中转 loading** —— `is-done { text-decoration: line-through }`（★ **不传播到绝对定位伪元素** ⇒ 只划文字、绿圈与对勾不受影响）；\n'
     u'> \u3000\u3000`is-doing::before` 压到 `opacity:.28`、`::after` 画 `primary-6` 实心弧 + `@keyframes zd-todo-spin`；★ 时长走**自定义属性** `--zd-spin-dur: 820ms`（避开 CRAFT-ANIM 按行扫）；\n'
     u'> \u3000⑤ **骨架屏期隐藏面板** —— 纯 CSS 门控 **`html:has(.r93-sk) .zd-host { display: none }`**（骨架屏一从 DOM 移除即自动失效、零 JS）；\n'
     u'> \u3000⑥ **`.zd-sec-x` 只在折叠态显示** —— 基态 `display:none` + `.zd-sec.is-closed .zd-sec-x { display: flex }`（**(0,1,0) vs (0,3,0)**，不打平）；',
     u'P3.11i 追加 ⑬ 第十五拍要点'),
]

PBK_P351 = u"""## P3.51 ★★ r108 第十五拍（六条 · @WHEN@ 邵先生）—— ★ 五条新教训

> 主题：`zd-card` 的 ① `.zd-sec-t` 正文黑/500/14px ② `.zd-ico` 补 hover ③ 「目标」只留 1 条
> ④ 已完成加删除线 + 进行中转 loading ⑤ 骨架屏期隐藏面板 ⑥ `.zd-sec-x` 只在折叠态显示。
> 补丁 = `mg-work/r108/ev/patch108l4.py`（8 项）；完整实测见 `mg-work/r108/acceptance.md` 二十 ~ 二十四节。

**① ★★★ `mark` 撞车 ⇒ 整条改动被「静默跳过」（P3.39 / P3.50 ③ 的升级版）**
* 症状：① 的 `mark` 初稿取的是**改后的声明串** `font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);`
  —— 它与上文 `.td-sum-prev-t b` 那条声明**逐字相同** ⇒ 首跑判「已应用」、**整条①根本没写进去**，
  而末行照样打印「应用 N 项 / 跳过 0 项」（**看不出漏**）。
* ★ 配方：给 `edit()` 加**「`mark` 歧义」硬断言** —— `old` 与 `mark` **同时**存在于同一份文件里就 `sys.exit`
  （mark 的语义就是「只有改完才出现」）。
* ⚠ **但必须留豁免位**：凡是「**把锚点原样保留在 `new` 里**」的写入（尾部追加 / 插在锚点前并把锚点接回）
  天然让两者共存 —— 那类步骤**本来就要求锚点留下当下层契约** ⇒ 判据写成 `keep_anchor = old in new`，
  为真则跳过歧义断言。★ 判据别写成 `new.startswith(old)`（只覆盖尾部追加，漏掉「插在锚点前」那类）。

**② ★★ 「持续旋转 / 不确定进度」类动效的时长写进自定义属性**
* 症状：`verify-design.py` 的 CRAFT-ANIM 判据是**按行**扫 `(?:animation|transition)[^;}]*?(\\d+)ms`、`>300ms` 报 warning。
  ④ 的 loading 若直接写 `animation: zd-todo-spin 820ms …` ⇒ **新增 1 条 warning** ⇒ 门禁 md5 不再等于 r107 基线。
* ★ 配方：时长写进**自定义属性** `--zd-spin-dur: 820ms`，规则里写 `animation: zd-todo-spin var(--zd-spin-dur) …`；
  **解释性注释也拆成「不含 `ms` 数字」的行**（否则注释把自己扫进去）。
* ★ 该判据针对的是**交互动效**（转场/悬停）；**持续旋转的不确定进度指示器**不在其适用范围 ⇒ 属性化是正当规避、不是作弊。

**③ ★★ 「某元素在 DOM 里 ⇒ 隐藏另一处」的纯 CSS 门控只有 `:has()` 能做**
* 落地：`html:has(.r93-sk) .zd-host { display: none }` —— 骨架屏一从 DOM 移除即**自动失效**，零 JS、零时序竞争。
* ⚠ **探针侧**：`document.querySelector('html:has(.r93-sk)')` 在不支持 `:has()` 的环境会抛 `SyntaxError`
  ⇒ **整条探针挂死**、看起来像「产品坏了」⇒ 必须 `try/catch` 并把结果标成 `unsupported:<ErrName>`。
* ★ 支持性自检：`CSS.supports('selector(html:has(.r93-sk))')`。

**④ ★★ `text-decoration` 不传播到绝对定位伪元素**
* 落地：`.zd-todo li.is-done { text-decoration: line-through }` 只划**文字**，自绘的绿圈 / 对勾（`::before` / `::after`）
  完全不受影响 ⇒ 删除线与自定义标记**可以共存**，不必再套一层 `<span>`。
* ★ 反例意识：若哪天发现「删除线连圈一起划了」，先怀疑那个标记**不是绝对定位伪元素**（可能是真元素）。

**⑤ ★★ 自检判据别用太短的片段**
* 症状：`.zd-sec-x {` 会被**同一层新加的** `.zd-sec.is-closed .zd-sec-x {` 一起命中（`count` 变 2 ⇒ 误判错误）；
  `zd-todo-spin` 天然出现 **2** 次（`animation-name` + `@keyframes`）。
* ★ 配方：判据取**「块首那几行」的更大片段**（`.zd-sec-x {\\n  flex: 1 1 auto` / `@keyframes zd-todo-spin {`）。

---

"""

PBK_APP_HEAD = (u'## 附：工作区速览 58 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
                u'## 附：工作区速览 63 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
                u'附录标题 → 63 条')

PBK_APP_INTRO = (u'> ⚠ 工作区那份 `MEMORY.md` 受 **3000 字符**限额（超了会被截断注入 ⇒ 等于没写）⇒ 原 58 条整表**迁到本附录存档**，',
                 u'> ⚠ 工作区那份 `MEMORY.md` 受 **3000 字符**限额（超了会被截断注入 ⇒ 等于没写）⇒ 原 58 条整表**迁到本附录存档**（第十五拍已按 **63 条**重整，工作区实测 **2982 字符**），',
                 u'附录引言 → 63 条')

PBK_APP_59_63 = (58,
                 u'58. ★★★ **「主题类结论」先取色再下判断**（`ev/pix.py`）；⚠ 动效时长一律 **≤300ms**（CRAFT-ANIM 上限），「弹性」靠缓动曲线过冲（spring `y1=1.56`）而非拉长时长。',
                 u'59. ★★★ **`mark` 撞车 ⇒ 整条改动被「静默跳过」**（角标串与上文某条声明**逐字相同**）⇒ 加「`old` 与 `mark` 同时存在即报错」的硬断言；★ 豁免位判据写 **`keep_anchor = old in new`**（别写 `new.startswith(old)`，会漏「插在锚点前」那类）。\n'
                 u'60. ★★ **「持续旋转 / 不确定进度」类动效的时长写进自定义属性**（`--zd-spin-dur: 820ms`）⇒ 避开 CRAFT-ANIM 的**按行**扫（注释也拆成不含 `ms` 数字的行）；该判据只管**交互动效**。\n'
                 u'61. ★★ 「某元素在 DOM 里 ⇒ 隐藏另一处」的**纯 CSS 门控只有 `:has()`**（`html:has(.r93-sk) .zd-host { display:none }`，自动失效、零 JS）；⚠ 探针里 `querySelector(\'html:has(...)\')` 必须 `try/catch`（否则 `SyntaxError` 把整条探针挂死）。\n'
                 u'62. ★★ **`text-decoration` 不传播到绝对定位伪元素** ⇒ 删除线与自绘标记（绿圈 / 对勾）**可以共存**、只划文字。\n'
                 u'63. ★★ **自检判据别用太短的片段** —— `\'.zd-sec-x {\'` 会被同层新加的 `.zd-sec.is-closed .zd-sec-x {` 一起命中、`\'zd-todo-spin\'` 天然出现 2 次（`animation-name` + `@keyframes`）⇒ 取**「块首那几行」的更大片段**。',
                 u'附录追加 59~63 五条')

MEM_STEPS = [
    (u'> ⚠ **工作区 `MEMORY.md` 受 3000 字符限额** ⇒ 原 58 条铁律整表已迁入 PLAYBOOK 附录「工作区速览 58 条」。',
     u'> ⚠ **工作区 `MEMORY.md` 受 3000 字符限额** ⇒ 原 58 条铁律整表已迁入 PLAYBOOK 附录「工作区速览 63 条」（第十五拍重整为「Windows 速记 + 红线索引 + 最近拍」，实测 **2982 字符**）。\n'
     u'>\n'
     u'> **★ r108 第十五拍（@WHEN@ · 六条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二 / 十三 / 十四拍**未提交** ⇒ 同上规则，本拍 = **第四层补丁** `ev/patch108l4.py`（**8 项**），全部围绕 **`.zd-card`** 的视觉精修 + 骨架屏门控。\n'
     u'> **六条** = ① **`.zd-sec-t` = 正文黑 + 中粗 500 + 14px**（去 `inherit`、显式 `font-size: var(--font-size-body-3)` + `font-weight: 500` + `color: var(--color-text-1)`；顺带删掉死规则 `.zd-sec-t:hover`）；\n'
     u'> ② **`.zd-ico` 补 hover**（照本页既有 `.td-browse-ico` 的**完整契约**：`inline-flex` / `24×24` / `padding:0` / `border:0` / `radius 4` / 透明底 / `text-2` + 同块内 `:hover { background: var(--color-fill-1); color: var(--color-text-1) }`，**基态在前**）；\n'
     u'> ③ **「目标」只留 1 条**（`drop_re` 删圆序号那行 ⇒ `.zd-it` 1 / `.zd-it-no` 0）；\n'
     u'> ④ **已完成进程加删除线 + 进行中转 loading**（`text-decoration: line-through` **不传播到绝对定位伪元素** ⇒ 只划文字；`::after` 实心弧 + `@keyframes zd-todo-spin`，★ 时长走 `--zd-spin-dur` **自定义属性**避开 CRAFT-ANIM 按行扫）；\n'
     u'> ⑤ **骨架屏期隐藏面板**（纯 CSS 门控 **`html:has(.r93-sk) .zd-host { display: none }`**，骨架屏一移除即自动失效）；\n'
     u'> ⑥ **`.zd-sec-x` 只在折叠态显示**（基态 `none` + `.zd-sec.is-closed .zd-sec-x { display: flex }`；**(0,1,0) vs (0,3,0)**，不打平）。\n'
     u'> **五条坑** = **P3.51**（① `mark` 撞车 ⇒ **静默跳过**（加硬断言 + `keep_anchor` 豁免位）② 持续旋转时长写进自定义属性 ③ `:has()` 纯 CSS 门控 + 探针要 `try/catch` ④ `text-decoration` 不传播伪元素 ⑤ 自检判据别用太短片段）。\n'
     u'> **产物**：`conversation.html` → **1012144 字符**（+2176；对 `HEAD` 累计 `896 / 19` 行）、`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**。',
     u'MEMORY r108 段 → 第十五拍'),
]

LOG = u"""

---

## r108 · 第十五拍（六条 · 就地返工 · @WHEN@ 邵先生）—— 🚫 未提交

**需求（逐字）**：1、"`.zd-sec-t`"的标题文字都使用正文黑色，且中粗500，字号14px；2、"zd-card"容器里的操作图标都少了hover效果，需补充；
3、"目标"模块里面保留一个目标即可；4、已完成的"进程"灰色标题加上删除线，进行中的进程要loading转起来；
5、conversation.html 页面在显示骨架屏时不应该显示"zd-card"；6、"zd-sec-h"里的"zd-sec-x"只有在折叠状态时才显示，展开时不显示。

**体位**：第十二 / 十三 / 十四拍未提交 ⇒ 就地返工 ⇒ 本拍 = **第四层补丁** `ev/patch108l4.py`（**8 项**）。
改序仍是 `part108/{_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`（**无需** `make108.py`）。
★ **未动任何其他模块**：`part108/panel.js` 一字未动；`task-detail.html` / `base.html` 未动。

**落地**：① 三个 `.zd-sec-t` **全** `fs 14px` / `fw 500` / `color rgb(31,31,31)`（`lh 21px` 由行盒给出）；
② 真鼠标 hover「收起为胶囊」⇒ `bg rgba(0,0,0,0) → rgb(247,247,247)`（`--color-fill-1`）、`color rgb(78,78,78) → rgb(31,31,31)`（`--color-text-1`），`icoN:2`；
③ `.zd-it` **1** / `.zd-it-no` **0** / 文案「落地审查、终端、浏览器、摘要四个面板 · 3/4」；
④ `is-done`（3 条）`deco: line-through` + `rgb(134,134,134)`；`is-doing::after` `zd-todo-spin` / `0.82s` / **infinite** / 弧 `rgb(55,112,247)`，
**两次采样（320ms 间隔）矩阵不同**（81° → 12°）⇒ 确实在转；
⑤ `html:has(.r93-sk) .zd-host { display:none }`：支持性 `true`；注入假 `.r93-sk` ⇒ `none`（cardRect 全 0）→ 移除 ⇒ `flex`；
★ **真实加载期 rAF 时间线** `[[0,"none",true],[144,"flex",false]]`；
⑥ 默认（全展开）三档 trailing **全 `none`** ⇒ 折叠「目标」`flex`（可见「2 分 18 秒 · ⏸」）且 `bodyRows 0px` ⇒ 再展开回 `none`。

**排掉的五处坑**（PLAYBOOK **P3.51**）：① `mark` 撞车（① 的 mark 与 `.td-sum-prev-t b` 那条逐字相同 ⇒ **整条①被静默跳过**，
加「`old` 与 `mark` 共存即报错」硬断言 + `keep_anchor = old in new` 豁免位；首跑当场被逮到、回滚 `bak15-*` 重来）；
② CRAFT-ANIM 按行扫 ⇒ 旋转时长写进 `--zd-spin-dur` 自定义属性、注释也拆成不含 `ms` 数字的行；
③ 自检判据太短（`.zd-sec-x {` 被同层新规则一起命中 / `zd-todo-spin` 天然 2 次）；④ 探针 `:has()` 要 `try/catch`；⑤ `agent-browser` 没有 `move`（取消 hover 只能 hover 中性兄弟元素 `.zd-name`）。

**探针**：`ev/p108q.js` + `probe108q.sh` → `q-raw.log`（8495 字节，六组全绿）；`ev/p108q2.js` = ⑤ 的真实加载期 rAF 时序采样器。
**截图** `ev/raw/q-1440-{todo,goal,collapsed,ico,sk}.png`（目视：删除线只划文字、绿圈与对勾不受影响；「目标」只剩 1 条；折叠态显示 trailing）。

**门禁**：四层幂等（l1 全跳过 / l2 `0/8` / l3 `0/27` / l4 **`0/8`** + 4/4 跨层断言「全部存活 ✓」）/ `apply108.py` 第二遍「已是目标态」/
`check-syntax.py pages/*.html` **10/10** / `verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）/
`scan-flatten.py part108/panel.css` **2 条**（基线）/ `pages/gaps.log` 已 `git checkout --` 清理。
**产物**：`conversation.html` 1009968 → **1012144 字符（+2176）**（`git diff --numstat` = `896  19`）；对 `HEAD` 累计 **+53576**；
LF bytes **1118375** / 工作区 bytes **1126747** / **8373 行** / LF `sha1_lf 12b000018f86`；
`task-detail.html` **767836（本拍未动，仍 `7  0`）**；`base.html` **逐字节不变**；代数核对 `r108-conv-css` / `r108-conv-js` 各 1、`r107/r106-conv-*` 全 0。
**验收** `mg-work/r108/acceptance.md` **二十四节**（二十 ~ 二十四 = 第十五拍）；**记忆同步** `ev/doc108q.py`（本文件）。🚫 未 commit / 未 push。
"""


def main():
    print(u'=== 1/6 HANDOFF.md ===')
    span(HOF, u'> ⚠️ **最新一拍 = r108 第十四拍', u'> ★★ **本拍六条坑**见 PLAYBOOK **P3.50**',
         HOF_TOP, u'HANDOFF', u'顶部「最新一拍」块整块换新（第十四拍降级为「上一拍」）')
    patch(HOF, HOF_STEPS, u'HANDOFF')
    # 二·h 段末追加「### 第十五拍」（anchor = 段末那一整块交接语）
    patch(HOF, [(HOF_15_ANCHOR, HOF_15_ANCHOR + HOF_15, u'二·h 段末追加「### 第十五拍」')], u'HANDOFF')

    print(u'=== 2/6 PAGES.md ===')
    patch(PAG, PAG_STEPS, u'PAGES')

    print(u'=== 3/6 PLAYBOOK.md ===')
    patch(PBK, [
        (PBK_APP_INTRO[0], PBK_APP_INTRO[1], PBK_APP_INTRO[2]),
        (PBK_APP_59_63[1], PBK_APP_59_63[2], PBK_APP_59_63[3]),
        # ★ 一步同时完成「在其前插入 P3.51」+「标题 58 → 63 条」——自包含、check 模式才有意义
        (PBK_APP_HEAD[0], PBK_P351 + PBK_APP_HEAD[1], u'附录前插入 P3.51 + 标题 → 63 条'),
    ], u'PLAYBOOK')

    print(u'=== 4/6 MEMORY.md ===')
    patch(MEM, MEM_STEPS, u'MEMORY')

    print(u'=== 5/6 log-repo ===')
    patch(LOG_REPO, [(None, LOG, u'追加第十五拍段')], u'log-repo')

    print(u'=== 6/6 log-ws ===')
    patch(LOG_WS, [(None, LOG, u'追加第十五拍段')], u'log-ws')

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
