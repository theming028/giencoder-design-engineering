# -*- coding: utf-8 -*-
u"""r108 第十六拍收尾：把「三条（产物预览改挂页签 + `.zd-host` 折展动效 + 毛玻璃）」同步进记忆文档。

★ 代数体位：第十二 / 十三 / 十四 / 十五拍**均未提交**（`git status` 里 `conversation.html` 仍 ` M`）⇒ 第十六拍同样是
  **就地返工**、**不另起 r109**、**不另开一组记忆段** —— 全部并入 r108 既有段落
  （节标题由「十二 + 十三 + 十四 + 十五拍」升为「十二 + 十三 + 十四 + 十五 + 十六拍」）。

范围（同步「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行 + 顶部「最新一拍」块整块换新（第十五拍降级为「上一拍」、
                                      第十四 / 十三 / 十二拍顺次降级）+ §一 状态段 + conversation 表行
                                      + mg-work/r108 表行（四小步）+ §二·h 标题/引言行 + 段末追加「### 第十六拍」
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十五拍」→「共十六拍」+ 追加 ⑭ 要点行
  3) .workbuddy/memory/PLAYBOOK.md  —— ★ 修回被 `doc108q.py` 误当作锚点替换掉的**第 58 条** + 新增 64~69 六条
                                      + 附录标题「63 条」→「69 条」+ 在其前插入 P3.52
  4) .workbuddy/memory/MEMORY.md    —— r108 段追加第十六拍要点（并把两处「共十二拍」/「63 条」改对）
  5) 两份 2026-10-01.md（仓库内 + 工作区）—— 追加第十六拍段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 维持 ≤3000 的前提下更新「最近拍」

★★ 本轮的「顺手修」：`doc108q.py` 的「附录追加 59~63」那一步把 `old` 写成了**第 58 条整行**（本意是「追加在 58 之后」），
   于是 58 被整条顶掉、标题却已改成「63 条」⇒ 附录实为 **62 条且缺 58**。本轮把它**补回**并把标题改到 69。

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换另给显式 mark。
★ 「mark 歧义」硬断言（P3.51 ①）：mark 与 old **同时**存在 ⇒ 只可能是 mark 不唯一 ⇒ `sys.exit`。
  ⚠ 豁免位判据 = `old in new`（「把锚点原样保留在 new 里」的写入本来就要求锚点留下当下层契约）。
★ 用法： python ev/doc108r.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc108r.py --check    # 只校验锚点命中数（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 7 份文件各自保留原行尾（rd/wr 处理）。
⚠ 正文里有 `100%` / `78%` 这类百分号 ⇒ **不用 `%` 格式化**，改用 `@WHEN@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 21:5x'

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
    """把「以 <first_pre> 起、以 <last_pre> 含」的**连续若干行**整段换掉。

    顶部的「最新一拍」块每轮都要整块换新 ⇒ 首尾各给一个行首前缀即可定位，
    比把 40 行老文本抄成正则稳（老文本会随每轮改动漂移）。
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


# ==================================================================== HANDOFF 顶部块
HOF_TOP = u"""> ⚠️ **最新一拍 = r108 第十六拍（三条 · ★★ 就地返工、未另起代数）** —— 第十二 / 十三 / 十四 / 十五拍仍未提交（判据 `git status` 里 `conversation.html` 仍是 ` M`）：
> 本拍 = **产物预览改挂侧栏页签 + 右上角任务面板（`.zd-host`）的折展动效与毛玻璃**，**未动任何其他模块**（`task-detail.html` / `base.html` 一字未动）。
> ① **产物卡片点击后的预览方式改挂「预览」页签 → 已做**：旧浮层 `.td-sum-prev`（`position:absolute; inset:0` 盖住 `.td-mod.td-sum`）**整体拆掉**
>   —— DOM 一块 + CSS 全套 + `.td-mod.td-sum { position: relative }` + **Esc 裁决链里占的那一层**；
>   新载体 = `#av-browse-pane-preview[data-td-pane="preview"]`（与「审查 / 终端 / 浏览器 / 摘要」同级），点产物即 `openTab('preview', { name, ico })`。
>   实测：点第 1 个产物 ⇒ 页签 `[摘要, 预览]`、`name='右栏复刻方案.md'`、`ico=true`、`aria-controls=av-browse-pane-preview`、`md=flex / xlsx=none`、**barH 40**；
>   点第 2 个 ⇒ **页签仍 1 枚**（复用）但 `name` 换成 `sidepanel-metrics.xlsx`、图标换表格字形、`md=none / xlsx=flex`；页签 `×` ⇒ 页签消失、`preview` 回 `hidden`、`summary` 回 40px。
>   ★ 设计取舍（一句话可翻转）：同一枚「预览」页签**复用**承载多个产物（VS Code 的 preview tab 同口径）；要「一产物一页签」只需去掉复用分支的 name/ico 同步、并把 `mod` 改成 `preview:<文件名>`。
>   ★ 连带清掉 `zd-sum-prev` **0** 处残留；代数核对 `r108-l5` 1。
> ② **`.zd-host` 折展动效换成「收进右上角 / 从右上角展开」→ 已做**：`transform-origin: 100% 0`（= 面板右上角，正是那枚「收起为胶囊」按钮所在的角）；
>   出场 `opacity 160ms` + `scale/translate 170ms`，入场 `@keyframes zd-panel-in` 260ms（spring 缓动）。
>   **同一次 eval 内「点 + rAF 采样」**（`recN=50/50`）实测：收 ⇒ `scale 1→0.62`、`translate 0px→12px -12px`、`opacity 1→0` 单调，t=186ms 到目标、t=203ms 卡片 `hidden`；
>   展 ⇒ t=186ms 首帧即 `scale 0.62 / translate 12px -12px / animationName=zd-panel-in`，**过冲**到 `scale 1.03715 / translate -1.173px` 再回 `1 / 0px`（t=453ms）。
>   `getComputedStyle` 量到 `transform-origin` = **`320px 0px`**（卡宽 320 ⇒ 就是「100% 0」）；胶囊 = `103.094px 0px`。
> ③ **`.zd-host` 整个容器改模糊背景（毛玻璃）→ 已做**：`.zd-host` 是**定位壳**（无底色 / `pointer-events:none`）⇒ 视觉表面 = 里面四件
>   （卡片 `.zd-card` / 胶囊 `.zd-mini` / 两枚下拉 `.zd-menu` / 轻提示 `.zd-toast`），**四件一起换**：底色 `color-mix` 就地取透（不新增 hex）+ `backdrop-filter: blur(18px) saturate(160%)`；
>   另给不支持 `backdrop-filter` 的引擎留 `@supports not (...)` 不透明兜底。
>   ★★ **取证必须落到像素**（只写 `backdrop-filter` 而底色仍不透明 token ⇒ **完全看不出效果**，而 computed 照样报 `blur(...)`）：
>   在卡片正下方临时铺 320×180 **纯红**，`ev/pix.py` 取色 ⇒ 卡片像素 `rgb(255, 199, 199)` = `0.78×白 + 0.22×红`（与解析解逐位吻合），
>   沿 y **平滑衰减** `199`(y40) → `211`(y170) → `237`(y190，**已越出红块下沿却仍带红** = 模糊外溢) → `254`(y470)；正常页面底同点位 `rgb(246, 248, 253)`。
>   ⇒ **半透明（底色被染）与模糊（边缘外溢、无锐利分界）各得一条互不替代的证据**。
> ★ **界面口径对齐（顺带）**：预览模块内两件控件各收到 26px（`.td-pv .td-sum-arti` / `.td-prev-btn`），
>   好让预览工具条 **40px = 摘要 40px**（`.td-mod-bar` 高度是**内容驱动**的：内容盒上限 = `min-height` − 上下 padding − border-bottom = 40 − 6 − 6 − 1 = 27px）。
> ★ **边界与回归全绿**（`ev/probe108r.sh` / `probe108r2.sh`）：暗色（卡片 `color(srgb 0.137255 0.137255 0.141176 / 0.78)` = #232324 的 78%）/
>   `--ui-fs=18`（摘要 41 / 审查 49 / 预览 46 —— 同页工具条**本来就不齐**，预览 40 已是最对齐的一种取法）/ 五模块工具条对照表。
> ★ **补丁 = `ev/patch108l5.py`**（**10 步**；五层幂等 `l1 全跳过 / 0-8 / 0-27 / 0-8 / 0-10`，5/5 跨层标记兜底断言「全部存活 ✓」）。
> ★★ **本拍六条坑**见 PLAYBOOK **P3.52**（删变量不删引用 ⇒ 按键抛 `ReferenceError` / `openTab` 复用分支不更新页签名 / `.td-mod-bar` 内容驱动高度 / 同页工具条本就不齐 / `backdrop-filter` 必须落像素 / `verify-design` 重写 `gaps.log`）。
> ▸ **上一拍 = r108 第十五拍（六条 · 就地返工，🚫 未提交）**：① `.zd-sec-t` 正文黑 / 500 / 14px · ② `.zd-ico` 补 hover · ③ 「目标」只留 1 条 · ④ 已完成删除线 + 进行中转 loading · ⑤ 骨架屏期隐藏 `.zd-card` · ⑥ `.zd-sec-x` 仅折叠态显示。"""

# ==================================================================== HANDOFF 第十六拍段
HOF_16 = u"""
### 第十六拍（r108 第五层补丁 · 三条 · @WHEN@ 邵先生 · 🚫 仍未提交）

> 完整版见 `mg-work/r108/acceptance.md` **二十五 ~ 二十九节**；机制级教训见 PLAYBOOK **P3.52**。

**需求（逐字）**：

> 1、改变一下产物"td-sum-art"卡片点击后的预览方式，在"td-browse-bar"作为一个新页签显示；
> 2、"zd-host"的展开折叠动效换一种，最好是那种折叠时收进右上角，展开式从右上角向左下角方向展开；
> 3、尝试把"zd-host"整个容器设计为模糊背景效果。

**① 体位**：第十二 / 十三 / 十四 / 十五拍**未提交** ⇒ 按「未交付 ⇒ 就地返工」⇒ 本拍 = **第五层补丁** `ev/patch108l5.py`
（**10 步**，**不另起 r109**）。五层各带独立 `mark`；改序仍是下→上：
`part108/{_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`（**无需** `make108.py`）。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_mods.html`（62701 → **62454** 字符 / 441 行） | 删旧浮层块（原 268~305 行）；摘要 `</section>` 之后新增 `#av-browse-pane-preview[data-td-pane="preview"]`（工具条 = 图标砖 + 名称 + 元信息 + 「在系统打开」；正文 = `md` / `xlsx` 两套骨架） |
| `part108/panel.css`（73063 → **74888** 字符 / 1569 行） | 18-③ 段重写为**页签版**（删 `.td-sum-prev*` 全套 + `.td-prev-btn.is-primary*`，新增 `.td-pv-name` / `.td-pv-hint` / `.td-pv-body`）；`.td-pv .td-sum-arti` 与 `.td-prev-btn` 收到 26px；④ 段重写为**右上角锚点**（`transform-origin:100% 0` + `scale .62` + `translate 12px -12px` + `@keyframes zd-panel-in`）；文件尾新增 **19.5 毛玻璃**段；末尾加 `/* r108-l5 */` 并把 `/* r108-l4 */` **原样接回** |
| `part108/panel.js`（71160 → **72477** 字符 / 1670 行） | `openTab` 支持 `opts.ico`；**复用分支加 `if (opts)` 守卫**同步 name / ico / `aria-label`；`prevShow` 改为「先填内容 → `openTab('preview', {name, ico})`」；Esc 裁决链**删掉预览那一层**（并删掉悬空的 `prevEl` / `prevOpen` / `prevHide` 引用） |
| `part108/browse.html` | 98363 → **98116**（`splice108.py` 重建；**是产物、不是手改对象**） |
| `ev/patch108l5.py` | **新建**（10 步；含「mark 歧义」硬断言 + 跨层兜底断言） |
| `ev/p108r.js` / `probe108r.sh` / `probe108r2.sh` + `on.js` | **新建**（相位探针 / 全链执行 / 复测 + 五模块工具条对照表） |
| `ev/bak16/` | **新建**（回滚基线：`_mods.html` / `panel.css` / `panel.js` / `browse.html`；提交前 `git reset`） |

**③ 真机实测（1440×900 / `--ui-fs=14`）**：① 点产物 ⇒ 页签 `[摘要, 预览]`、`barH 40`、`md=flex xlsx=none`；
连点两个 ⇒ 页签**仍 1 枚**但名字/图标换成 xlsx（截图 `r2-tabs-after-pvB.png`）；页签 `×` ⇒ `preview` 回 `hidden`、`summary` 回 40px；
旧浮层残留自检 `residue = {overlay:false, overlaySel:false, paneCount:1, sumPos:'static', prevElGlobal:'undefined'}`、`zd-sum-prev` **0**；
② `transform-origin` **`320px 0px`**；收（t=186ms 到目标 / t=203ms `hidden`）与展（首帧 `scale .62` ⇒ **过冲 `1.03715`** ⇒ 回 1，t=453ms）见上文；
③ computed 四件 `color(srgb 1 1 1 / 0.78)`（下拉 `0.82`）+ `backdrop-filter: blur(18px) saturate(1.6)`；
`CSS.supports('backdrop-filter','blur(2px)')` = **true**；像素取证见 ③ 与 `ev/pix.py`。

**④ 排掉的六处坑**（详见 PLAYBOOK **P3.52**）

1. ★★★ **删一个变量只删「定义」、不删「引用」⇒ 按一次键抛 `ReferenceError`**：`prevEl` / `prevHide` 定义在摘要模块段、却被**下面**的 Esc 裁决链引用，而它在一个 `window` **捕获段**的 keydown 里 ⇒ 整条处理器抛错、并带坏「关整条侧栏」。修：新增两步删掉引用；判据要**剥注释再搜** + **保留 `\\b` 词界**（`prevOpenBtn` 会命中 `prevOpen`，为此白跑一轮）。
2. ★★ **`openTab` 的「已存在 ⇒ activate」分支不更新页签名 / 图标**：连点两个产物 ⇒ 页签写着第一个文件名、正文已是第二个（截图肉眼可见）。修：复用分支加 `if (opts) { 同步 name / ico / aria-label }`，★ **必须带 `opts` 守卫**（`+` 菜单 / 右键菜单不传 `opts`，不守卫会误改「文件 / 审查 / 终端」页签名）。
3. ★★ **`.td-mod-bar` 高度是「内容驱动」而非 40px**：`min-height: calc(40px * ratio)` 被 `apply88b.converge()` 压平成裸 `40px` ⇒ 真实高 = `6 + max(内容高) + 6 + 1`，28px 的图标砖/按钮都顶成 **41px**。通用判据：**内容盒上限 = `min-height` − 上下 padding − border-bottom**。
4. ★★ **同一页里工具条本来就不齐**：`--ui-fs=14` 摘要 **40** / 审查 **41**；`--ui-fs=18` 摘要 **41** / 审查 **49** / 预览 **46**。⇒ 「预览 40 = 摘要 40」已是本页最对齐的取法（两者互切时工具条不跳）。
5. ★ **只写 `backdrop-filter`、底色仍是不透明 token ⇒ 完全看不出效果**，而 computed 照样报 `blur(...)`（本层第一版差点这么收货）⇒ 必须落像素（见 ③）。
6. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（行号随任何改动漂移，本轮凭空多 `64 / 44` 行 diff）⇒ **收尾一律 `git checkout -- pages/gaps.log`**。

**⑤ 产物与门禁**：`conversation.html` 1012144 → **1015095 字符（+2951）**（对 `HEAD` 累计 **`1047 107`** 行）；
LF bytes **1124149** / 工作区 bytes **1132584** / **8436 行** / LF `sha1_lf da1acf6a091c`；
`task-detail.html` **767836（本拍未动，仍 `7 0`）**；`base.html` **472150 逐字节不变**。
代数核对：`r108-conv-css` / `r108-conv-js` / `r108-l5` 各 **1**，`r107-conv-*` / `zd-sum-prev` **全 0**。
幂等 ✓（l1 全跳过 / l2 `0/8` / l3 `0/27` / l4 `0/8` / **l5 `0/10`** + 5/5 断言「全部存活 ✓」；`apply108.py` 第二遍「已是目标态」）｜
`check-syntax.py pages/*.html` **10/10** ｜ `verify-design.py ./pages` 与基线 **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）｜
`scan-flatten.py part108/panel.css` **2 条**（`.td-mod-bar` / `.td-url` 基线）｜ `pages/gaps.log` 已 `git checkout --` 清理。

**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`
还要 **`git reset -q -- mg-work/r108/ev/bak1[3-6]*`**；`mg-work/r108/part108/` 与 `raw/`、`up/` 照旧入库。
★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；
**不要**新建 r109、**不要**回头改 `apply107.py`。
★ **别忘 `git checkout -- pages/gaps.log`**（本轮它就凭空多了 64 / 44 行）。
★ ★★ **l5 之后若再叠一层（`patch108l6.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l5 */` **也原样接回**（否则 l5 复跑整块重挂）。
"""

HOF_STEPS = [
    # 首行时间戳
    (u'> 最后更新：2026-10-01 21:1x（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条（zd-card 视觉精修 + 骨架屏门控）」** → 门禁四查全绿 + 真机实测（主链六组 + 边界三组全绿）→ **🚫 未提交**）',
     u'> 最后更新：@WHEN@（**r107 已推送 `e9c9498`** + **r108 已落地「第十二拍 diff 卡片化 + 文件树抽屉」+「第十三拍 六条」+「第十四拍 四条」+「第十五拍 六条」+「第十六拍 三条（产物预览改挂页签 + `.zd-host` 折展动效 + 毛玻璃）」** → 门禁四查全绿 + 真机实测（主链八组 + 边界三组全绿）→ **🚫 未提交**）',
     u'首行时间戳 → 第十六拍'),

    # 降级链条（第十五拍新占「上一拍」位；其下三轮顺次降级）
    (u'> 要点与本拍同源，逐条见下方「### 第十四拍」。（其下数行 = 再上一拍（第十三拍）与更早（第十二拍），本轮已顺次降级标签。）',
     u'> 要点与本拍同源，逐条见下方「### 第十五拍」。（其下数行 = 再上一拍（第十四拍）与更早（第十三 / 十二拍），本轮已顺次降级标签。）',
     u'降级链条 · 要点行'),
    (u'> ▸ **上一拍 = r108 第十四拍（四条 · 就地返工，🚫 未提交）**：',
     u'> ▸ **再上一拍 = r108 第十四拍（四条 · 就地返工，🚫 未提交）**：',
     u'降级链条 · 第十四拍'),
    (u'> ▸ **再上一拍 = r108 第十三拍（六条 · 就地返工，🚫 未提交）**：',
     u'> ▸ **更早 = r108 第十三拍（六条 · 就地返工，🚫 未提交）**：',
     u'降级链条 · 第十三拍'),
    (u'> ▸ **更早 = r108 第十二拍**：',
     u'> ▸ **最早 = r108 第十二拍**：',
     u'降级链条 · 第十二拍'),

    # §一 状态段
    (u'★★ **r108（第十二 + 十三 + 十四 + 十五拍）＝本代新产物，🚫 未提交**（2026-10-01 21:1x，第十五拍）。工作区：\n**` M pages/conversation.html`（1012144 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六拍）＝本代新产物，🚫 未提交**（@WHEN@，第十六拍）。工作区：\n**` M pages/conversation.html`（1015095 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'§一 状态段 → 第十六拍'),

    # conversation 表行
    (u'★ **r108 态（🚫 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）→ 1009968（第十四拍 +14835）→ 1012144（第十五拍 +2176）**；LF bytes **1118375** / 工作区 bytes **1126747** / **8373 行** / LF `sha1_lf 12b000018f86`；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 **十二 ~ 十五拍**见 `mg-work/r108/acceptance.md`（**二十四节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍）',
     u'★ **r108 态（🚫 未提交）**：958568 → **978614（第十二拍 +20046）→ 995133（第十三拍 +16519）→ 1009968（第十四拍 +14835）→ 1012144（第十五拍 +2176）→ 1015095（第十六拍 +2951）**；LF bytes **1124149** / 工作区 bytes **1132584** / **8436 行** / LF `sha1_lf da1acf6a091c`；注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**；另加一档 `r108-l5`）；r108 **十二 ~ 十六拍**见 `mg-work/r108/acceptance.md`（**二十九节**，八 ~ 十二 = 第十三拍、十三 ~ 十九 = 第十四拍、二十 ~ 二十四 = 第十五拍、二十五 ~ 二十九 = 第十六拍）',
     u'conversation 表行 → 第十六拍'),

    # mg-work/r108 表行（拆四小步，避开超长单行）
    (u'| `mg-work/r108/` | **🚫 未提交（第十二 + 十三 + 十四 + 十五拍）**：',
     u'| `mg-work/r108/` | **🚫 未提交（第十二 + 十三 + 十四 + 十五 + 十六拍）**：',
     u'表行 · 代数标签'),
    (u'`acceptance.md`（**二十四节**）/ **`part108/`**',
     u'`acceptance.md`（**二十九节**）/ **`part108/`**',
     u'表行 · acceptance 节数'),
    (u'`_mods.html` 51798 → 59186 → 62859 → **62701** 字符 · `panel.css` → 70729 → **73063** 字符 / 1531 行 · `panel.js` → **71160** 字符（第十五拍未动）；',
     u'`_mods.html` 51798 → 59186 → 62859 → 62701 → **62454** 字符 · `panel.css` → 70729 → 73063 → **74888** 字符 / 1569 行 · `panel.js` → 71160 → **72477** 字符 / 1670 行；',
     u'表行 · part108 体积'),
    (u'· `q-raw.log`）/ `raw/`',
     u'· `q-raw.log`；**第十六拍**：`patch108l5.py`（10 步）· `p108r.js` · `probe108r.sh` / `probe108r2.sh` · `on.js` · `bak16/` · `r-raw.log` / `r2-raw.log` / `r3-raw.log` / `r4-raw.log` / `r5-raw.log`）/ `raw/`',
     u'表行 · ev 清单补本拍'),
    (u'`n-1440-{zd,zd-card,zd-fold,zd-mini,zd-dark,bar,sum,sum-hover,art-preview,art-pane,diff,diff-toggle,revbar}.png`）|',
     u'`n-1440-{zd,zd-card,zd-fold,zd-mini,zd-dark,bar,sum,sum-hover,art-preview,art-pane,diff,diff-toggle,revbar}.png` + `r-1440-{pv-md,pv-xlsx,dark}.png` / `r2-{tabs-after-pvB,bars-fs14-terminal,bars-fs18-preview}.png` / `r-card-over-{red,page}.png`）|',
     u'表行 · raw/ 补本拍截图'),

    # §二·h 标题 + 引言行
    (u'## 二·h ★★ r108（最新一拍 · 会话详情页「diff 卡片化 + 文件树抽屉」+ 六条精修「含 ★ 复刻 ZCode 右上角任务信息面板」· 2026-10-01 19:4x 起，共**十二拍 + 十三拍补丁**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'## 二·h ★★ r108（最新一拍 · 会话详情页「diff 卡片化 + 文件树抽屉」+ 六条精修「含 ★ 复刻 ZCode 右上角任务信息面板」· 2026-10-01 19:4x 起，共**十二 ~ 十六拍**）—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'二·h 标题 → 共十二 ~ 十六拍'),
    (u'> 完整版见 `mg-work/r108/acceptance.md`（**二十四节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.51**；本页固定事实见 PAGES **P3.11i**。',
     u'> 完整版见 `mg-work/r108/acceptance.md`（**二十九节**）；机制级教训见 PLAYBOOK **P3.48 ~ P3.52**；本页固定事实见 PAGES **P3.11i**。',
     u'二·h 引言行 → 第十六拍'),
]

HOF_16_ANCHOR = (u'**⑥ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`\n'
                 u'还要 **`git reset -q -- mg-work/r108/ev/bak1[345]*`**；`mg-work/r108/part108/` 与 `raw/`、`up/` 照旧入库。\n'
                 u'★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；\n'
                 u'**不要**新建 r109、**不要**回头改 `apply107.py`。\n'
                 u'★ ★★ **l4 之后若再叠一层（`patch108l5.py`）**：新层的 `CSS_TAIL` 必须把 `/* r108-l4 */` **也原样接回**（否则 l4 复跑整块重挂）。\n')

# ==================================================================== PAGES
PAG_14 = u"""> **⑭ r108 第十六拍（三条 · 产物预览改挂页签 + `.zd-host` 折展动效 & 毛玻璃）**：
> 　① **产物预览改挂「预览」页签** —— 旧浮层 `.td-sum-prev`（`position:absolute; inset:0` 盖住 `.td-mod.td-sum`）**整体拆掉**
> 　　（DOM 一块 + CSS 全套 + `.td-mod.td-sum{position:relative}` + **Esc 裁决链里占的那一层**）；
> 　　新载体 `#av-browse-pane-preview[data-td-pane="preview"]`（与审查 / 终端 / 浏览器 / 摘要同级），点产物 `openTab('preview', {name, ico})`；
> 　　★ 同一枚页签**复用**承载多个产物（连点两个只改名 + 换图标，不开第二枚）；`zd-sum-prev` 残留 **0**；
> 　② **折展动效「收进右上角 / 从右上角展开」** —— `transform-origin: 100% 0`（实测 computed `320px 0px`）；
> 　　收 ⇒ `scale 1→0.62` + `translate 0px→12px -12px` + `opacity→0`（186ms 到目标 / 203ms `hidden`）；
> 　　展 ⇒ `@keyframes zd-panel-in` 260ms，首帧 `scale .62 / translate 12px -12px`，**过冲** `scale 1.03715` 再回 `1 / 0px`（453ms）；
> 　③ **`.zd-host` 改毛玻璃** —— 视觉四件（`.zd-card` / `.zd-mini` / `.zd-menu`×2 / `.zd-toast`）底色 `color-mix` 就地取透 + `backdrop-filter: blur(18px) saturate(160%)`，另留 `@supports not` 不透明兜底；
> 　　★★ 取证必须**落像素**（只写 `backdrop-filter` 而底色不透明 = 看不出效果、computed 却照样报 `blur`）：临时铺 320×180 纯红 ⇒ 卡面 `rgb(255,199,199)`（= `0.78×白 + 0.22×红`），沿 y 平滑衰减并**外溢**到红块下沿之外（`237`@y190 → `254`@y470）；
> 　★ 顺带：预览工具条两件控件各收 26px ⇒ 预览 **40px = 摘要 40px**（`.td-mod-bar` 高度**内容驱动**，内容盒上限 = 40 − 6 − 6 − 1 = 27px；同页工具条**本来就不齐**：fs14 摘要 40 / 审查 41，fs18 41 / 49 / 46）；"""

PAG_STEPS = [
    (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三 / 十四 / 十五拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十五拍**）',
     u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 / 十三 / 十四 / 十五 / 十六拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十六拍**）',
     u'P3.11i 标题 → 共十六拍'),
]

PAG_ANCHOR = (u'> \u3000⑥ **`.zd-sec-x` 只在折叠态显示** —— 基态 `display:none` + `.zd-sec.is-closed .zd-sec-x { display: flex }`（**(0,1,0) vs (0,3,0)**，不打平）；\n')

# ==================================================================== PLAYBOOK P3.52
PBK_P352 = u"""## P3.52 ★★ r108 第十六拍（三条 · @WHEN@ 邵先生）—— ★★ 六条新教训

> 主题：① 产物 `td-sum-art` 卡片点击后的预览改挂 `td-browse-bar` **新页签** ② `zd-host` 折展动效改成
> 「收进右上角 / 从右上角展开」 ③ `zd-host` 整容器改**毛玻璃**。
> 补丁 = `mg-work/r108/ev/patch108l5.py`（10 步）；完整实测见 `mg-work/r108/acceptance.md` 二十五 ~ 二十九节。

**① ★★★ 删一个变量只删「定义」、不删「引用」⇒ 按一次键就抛 `ReferenceError`**
* 症状：`prevEl` / `prevHide` 定义在**摘要模块**那一段，却被**下面**的 Esc 裁决链引用
  （`var prevOpen = prevEl && !prevEl.hasAttribute('hidden')` + `if (prevOpen) prevHide();`）。
  浮层一删这个标识符就悬空 —— 而它在一个 `window` **捕获段**的 keydown 里 ⇒ **按一次 Esc 整条处理器抛错**，
  顺带把「关整条侧栏」也带坏（还会伪装成「另一个功能坏了」）。
* ★ 配方：**删组件时全仓 grep 该变量名（含引用点）**，判据要**剥掉注释再搜**
  （本层注释里为留痕主动写了 `prevEl` / `prevOpen` ⇒ 裸串搜索必误报）；
  同时**别把 `\\b` 词界丢掉**（`prevOpenBtn` 会把 `prevOpen` 命中，本层为此白跑一轮）。
* ★ 判据形态：`len(re.findall(r'\\bprevEl\\b', nocmt)) == 0`（先 `re.sub(r'/\\*.*?\\*/', '', s, flags=re.S)`）。

**② ★★ `openTab` 的「已存在 ⇒ activate」分支**不会**更新页签名 / 图标**
* 症状：连点两个产物 ⇒ **页签写着 `右栏复刻方案.md`、正文已经是 `sidepanel-metrics.xlsx` 的表格**
  （截图肉眼可见）；判据 = 探针里 `tabs[].name` 与 `prev.name` 对不上。
* ★ 配方：复用分支加 `if (opts) { 同步 name / ico / aria-label }`。
  ⚠ **必须带 `opts` 守卫** —— `+` 模块菜单与右键菜单那几处**不传 `opts`**，
  不守卫就会顺手改掉「文件 / 审查 / 终端」的页签名（自检加 `jcode.count('if (opts) {') == 1`）。
* ★ 同族提醒：「新增可选参数」要同时检查**所有调用点**是否都该传（本层只给 `prevShow` 传 `ico`）。

**③ ★★ `.td-mod-bar` 的高度不是 40px，而是「内容驱动」**
* 根因：`min-height: calc(40px * var(--ui-fs-ratio))` 被 `apply88b.converge()` **压平成裸 `40px`**
  （=`scan-flatten.py` 那 2 条基线之一）⇒ 真实高 = `6 + max(内容高) + 6 + 1(border)`。
  28px 的图标砖 / 按钮都把它顶成 **41px**。
* ★ 通用判据：**内容盒上限 = `min-height` − 上下 padding − border-bottom**（本页 = 40 − 6 − 6 − 1 = 27px）。
  要在 40px 工具条里放图标砖 ⇒ 收到 **26px**（28 必溢出 1px）。
* ⚠ 收尺寸必须**带模块作用域**（`.td-pv .td-sum-arti`），别改到别的模块的同类砖。

**④ ★★ 同一页里工具条本来就不齐，别默认「基线是齐的」**
* 实测 `--ui-fs=14`：摘要 **40** / 审查 **41**；`--ui-fs=18`：摘要 **41** / 审查 **49** / 预览 **46**。
  根因同 ③（谁内容高谁高）。
* ★ 因此「对齐」要选**有语义的那一对**（预览页签由摘要点出来 ⇒ 两者互切时工具条不跳 = 40 = 40），
  而不是「全页同高」（做不到，也不该为了它去改别的模块）。
* ★ 汇报口径：fs18 下与摘要差 5px 属**既有结构**（审查差 8px），**不是本层引入的** ⇒ 要主动说明，免得被当成回归。

**⑤ ★ `backdrop-filter` 的取证陷阱：只写 `backdrop-filter`、底色仍是不透明 token = 完全看不出效果**
* 而 computed 照样报 `blur(18px) saturate(1.6)` ⇒ 「量一下 computed 有 `backdrop-filter` 就以为成了」是**假绿**。
* ★ 配方（必须**落到像素**）：在目标正下方临时插一个 `position:fixed` 的纯色块（本轮 320×180 **纯红**），
  再 `ev/pix.py <png> x,y` 取色 —— 本轮卡面 `rgb(255,199,199)` = `0.78×白 + 0.22×红`（与解析解逐位吻合）；
  沿 y 取样还能证明**模糊**：`199`(y40) → `211`(y170) → `237`(y190，**已越出红块下沿却仍带红** = 外溢) → `254`(y470)。
* ★ **半透明（底色被染）与模糊（边缘外溢、无锐利分界）是两条互不替代的证据**，缺一不可。
* ★ 兜底：给不支持 `backdrop-filter` 的引擎留 `@supports not (...)` 不透明分支（`CSS.supports` 先自检）。

**⑥ ★ `verify-design.py` 每次都会重写 `pages/gaps.log`**
* 内容是 `file:line — 描述`，**行号会随任何改动漂移** ⇒ 本轮凭空多出 `64 / 44` 行 diff，
  容易误判成「我改了不该改的」。
* ★ 收尾固定动作：**`git checkout -- pages/gaps.log`**（与 `check-syntax` / `verify-design` 的污染一起清）。

---

"""

# ==================================================================== PLAYBOOK 附录
PBK_58_BACK = u"""58. ★★★ **「主题类结论」先取色再下判断**（`ev/pix.py`）；⚠ 动效时长一律 **≤300ms**（CRAFT-ANIM 上限），「弹性」靠缓动曲线过冲（spring `y1=1.56`）而非拉长时长。
59. ★★★ **`mark` 撞车 ⇒ 整条改动被「静默跳过」**（角标串与上文某条声明**逐字相同**）⇒ 加「`old` 与 `mark` 同时存在即报错」的硬断言；★ 豁免位判据写 **`keep_anchor = old in new`**（别写 `new.startswith(old)`，会漏「插在锚点前」那类）。"""

PBK_64_69 = u"""
64. ★★★ **删一个变量只删「定义」、不删「引用」⇒ 按一次键抛 `ReferenceError`** —— 处理器里（尤其 `window` **捕获段**）的悬空标识符会把**整条处理器**带坏、并伪装成「另一个功能坏了」；配方 = 全仓 grep 变量名（含引用点）+ 判据**剥注释** + 别丢 `\\b` 词界（`prevOpenBtn` 会命中 `prevOpen`）。
65. ★★ **`openTab`（复用型开页签）的「已存在 ⇒ activate」分支不会更新页签名/图标** ⇒ 复用分支同步 name / ico / `aria-label`；⚠ **必须带 `opts` 守卫**（不传 `opts` 的调用点会被误改）。
66. ★★ **`.td-mod-bar` 高度是「内容驱动」不是 40px**（`min-height` 被压平 ⇒ 真高 = `6 + max(内容高) + 6 + 1`）；通用判据 **内容盒上限 = `min-height` − 上下 padding − border-bottom**（本页 27px，放图标砖要收到 26px，且带模块作用域）。
67. ★★ **同一页里工具条本来就不齐，别默认「基线是齐的」**（fs14 摘要 40 / 审查 41；fs18 41 / 49 / 46）⇒ 对齐要选**有语义的那一对**，并把「非本层引入的差」在汇报里主动说明。
68. ★ **`backdrop-filter` 取证陷阱**：只写 `backdrop-filter`、底色仍不透明 token = **完全看不出效果**（computed 却照样报 `blur`）⇒ 必须**落像素**（底下铺纯色块 + 逐点取色）；★ 半透明（被染）与模糊（外溢）是**两条互不替代**的证据。
69. ★ **`verify-design.py` 每次都会重写 `pages/gaps.log`**（行号随任何改动漂移）⇒ 收尾一律 **`git checkout -- pages/gaps.log`**，别把它当成「我改错了」。
"""

PBK_APP_HEAD = u'## 附：工作区速览 63 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）'
PBK_APP_HEAD_NEW = u'## 附：工作区速览 69 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）'

PBK_APP_INTRO_OLD = u'> ⚠ 工作区那份 `MEMORY.md` 受 **3000 字符**限额（超了会被截断注入 ⇒ 等于没写）⇒ 原 58 条整表**迁到本附录存档**（第十五拍已按 **63 条**重整，工作区实测 **2982 字符**），'
PBK_APP_INTRO_NEW = u'> ⚠ 工作区那份 `MEMORY.md` 受 **3000 字符**限额（超了会被截断注入 ⇒ 等于没写）⇒ 原 58 条整表**迁到本附录存档**（第十五拍按 **63 条**重整、**第十六拍补回被误当作锚点顶掉的第 58 条并加到 69 条**，工作区实测 **2982 字符**），'

PBK_59_OLD = u'59. ★★★ **`mark` 撞车 ⇒ 整条改动被「静默跳过」**（角标串与上文某条声明**逐字相同**）⇒ 加「`old` 与 `mark` 同时存在即报错」的硬断言；★ 豁免位判据写 **`keep_anchor = old in new`**（别写 `new.startswith(old)`，会漏「插在锚点前」那类）。'

PBK_63_OLD = u"63. ★★ **自检判据别用太短的片段** —— `'.zd-sec-x {'` 会被同层新加的 `.zd-sec.is-closed .zd-sec-x {` 一起命中、`'zd-todo-spin'` 天然出现 2 次（`animation-name` + `@keyframes`）⇒ 取**「块首那几行」的更大片段**。"

# ==================================================================== MEMORY（仓库）
MEM_16 = u"""
> **★ r108 第十六拍（@WHEN@ · 三条 · ★★ 就地返工、未另起代数）—— 🚫 仍未提交**：第十二 / 十三 / 十四 / 十五拍**未提交** ⇒ 同上规则，本拍 = **第五层补丁** `ev/patch108l5.py`（**10 步**）：① 产物预览改挂侧栏**「预览」页签** ② `.zd-host` 折展动效改「收进右上角 / 从右上角展开」 ③ `.zd-host` 整容器改**毛玻璃**。
> **三条** = ① **产物 `td-sum-art` 卡片点击后的预览改挂 `td-browse-bar` 新页签** —— 旧浮层 `.td-sum-prev`（`position:absolute; inset:0`）**整体拆掉**（DOM + CSS + `.td-mod.td-sum{position:relative}` + **Esc 裁决链那一层**；残留 `zd-sum-prev` **0**），
> 新载体 `#av-browse-pane-preview[data-td-pane="preview"]`、点产物 `openTab('preview', {name, ico})`；★ 同一枚页签**复用**承载多产物（连点两个只改名换图标）+ 复用分支加 `if (opts)` 守卫；
> ② **`.zd-host` 折展动效** —— `transform-origin: 100% 0`（computed **`320px 0px`**）；收 ⇒ `scale 1→0.62` + `translate 0px→12px -12px` + `opacity→0`（186ms 到目标 / 203ms `hidden`）；展 ⇒ `@keyframes zd-panel-in` 260ms，**过冲** `scale 1.03715` 再回 1（453ms）；
> ③ **`.zd-host` 改毛玻璃** —— 视觉四件（`.zd-card` / `.zd-mini` / `.zd-menu`×2 / `.zd-toast`）底色 `color-mix` 取透 + `backdrop-filter: blur(18px) saturate(160%)` + `@supports not` 不透明兜底；
> ★★ **取证必须落像素**（只写 `backdrop-filter` 而底色不透明 = 看不出效果）：铺 320×180 纯红 ⇒ 卡面 `rgb(255,199,199)`（`0.78×白 + 0.22×红`），沿 y 衰减 `199`→`237`(y190，已越出红块下沿= **模糊外溢**) →`254`。
> **六条坑** = **P3.52**（① **删变量没删引用 ⇒ 按键抛 `ReferenceError`**（判据剥注释 + 保 `\\b` 词界）② `openTab` 复用分支不更新页签名（加 `opts` 守卫）③ `.td-mod-bar` **内容驱动高度**（内容盒上限 = `min-height` − 上下 padding − border-bottom = 27px）④ 同页工具条**本就不齐**（fs14 40/41、fs18 41/49/46）⑤ `backdrop-filter` **必须落像素** ⑥ `verify-design` 重写 `pages/gaps.log` ⇒ 收尾 `git checkout --`）。
> **产物**：`conversation.html` → **1015095 字符**（+2951；对 `HEAD` 累计 **`1047 / 107`** 行；LF `sha1_lf da1acf6a091c` / 8436 行）、`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **二十九节**。
> ⚠ **PLAYBOOK 附录修错**：`doc108q.py` 的「追加 59~63」把 `old` 写成**第 58 条整行** ⇒ 58 被整条顶掉（附录实为 62 条、标题却写 63）⇒ 第十六拍**已补回 58 并加到 69 条**。
"""

MEM_STEPS = [
    (u'> ⚠ **工作区 `MEMORY.md` 受 3000 字符限额** ⇒ 原 58 条铁律整表已迁入 PLAYBOOK 附录「工作区速览 63 条」（第十五拍重整为「Windows 速记 + 红线索引 + 最近拍」，实测 **2982 字符**）。',
     u'> ⚠ **工作区 `MEMORY.md` 受 3000 字符限额** ⇒ 原 58 条铁律整表已迁入 PLAYBOOK 附录「工作区速览 69 条」（第十五拍重整为「Windows 速记 + 红线索引 + 最近拍」、**第十六拍补回被误顶掉的第 58 条并加到 69 条**，实测 **2982 字符**）。',
     u'MEMORY → 附录 69 条'),
    (u'> ★★ **新增定论见 PLAYBOOK P3.48**；各拍要点见 **PAGES P3.11i（共十二拍）**；逐条实测见 **`mg-work/r108/acceptance.md`（七节）**。',
     u'> ★★ **新增定论见 PLAYBOOK P3.48**；各拍要点见 **PAGES P3.11i（共十六拍）**；逐条实测见 **`mg-work/r108/acceptance.md`（二十九节）**。',
     u'MEMORY → 拍数/节数对齐'),
]

# ==================================================================== 工作区 MEMORY.md
WSM_STEPS = [
    (u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.51** + 附录「工作区速览 63 条」·',
     u'> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.52** + 附录「工作区速览 69 条」·',
     u'WS-MEM → P3.52 / 69 条'),

    (u'## 二、红线索引（完整 63 条见仓库 PLAYBOOK 附录）',
     u'## 二、红线索引（完整 69 条见仓库 PLAYBOOK 附录）',
     u'WS-MEM → 红线索引 69 条'),

    (u'- **r108 十二 ~ 十五拍**（🚫 未提交 · **同一代就地返工**）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 六条（含复刻 ZCode 右上角 `.zd-card`）；十四 = `.zd-card` 四条（Git 三行交互 / 删计划 / 目标按上游校准 / 弹性动效）；**十五 = 六条** —— `.zd-sec-t` 正文黑 + 500 + 14px · `.zd-ico` 补 hover · 「目标」只留 1 条 · 已完成进程加删除线 & 进行中 loading 旋转 · **骨架屏期隐藏 `.zd-card`（`html:has(.r93-sk)`）** · `.zd-sec-x` 只在折叠态显示。',
     u'- **r108 十二 ~ 十六拍**（🚫 未提交 · **同一代就地返工**）：十二 = `.td-diff` 卡片化 + 文件树抽屉；十三 = 六条（含复刻 ZCode 右上角 `.zd-card`）；十四 = `.zd-card` 四条；十五 = 六条（视觉精修 + 骨架屏门控）；**十六 = 三条** —— 产物预览改挂 **「预览」页签**（旧 `.td-sum-prev` 浮层整体拆除）· 折展改**右上角锚点**（`transform-origin:100% 0` + `zd-panel-in` 过冲）· `.zd-host` 四件改**毛玻璃**（`backdrop-filter: blur(18px) saturate(1.6)`）。',
     u'WS-MEM → 最近拍 r108 十六拍'),

    (u'- 补丁链 `ev/patch108{l1,l2,l3,l4}.py`；产物 `conversation.html` **1012144 字符**（`896 / 19` 行）、`task-detail.html` **767836（未动）**、`base.html` 逐字节不变；`acceptance.md` **二十四节**。',
     u'- 补丁链 `ev/patch108{l1,l2,l3,l4,l5}.py`；产物 `conversation.html` **1015095 字符**（`1047 / 107` 行）、`task-detail.html` **767836（未动）**、`base.html` 逐字节不变；`acceptance.md` **二十九节**。',
     u'WS-MEM → 补丁链/产物'),
]

# ==================================================================== 日志
LOG = u"""

---

## r108 · 第十六拍（三条 · 就地返工 · @WHEN@ 邵先生）—— 🚫 未提交

**需求（逐字）**：1、改变一下产物"td-sum-art"卡片点击后的预览方式，在"td-browse-bar"作为一个新页签显示；
2、"zd-host"的展开折叠动效换一种，最好是那种折叠时收进右上角，展开式从右上角向左下角方向展开；3、尝试把"zd-host"整个容器设计为模糊背景效果。

**体位**：第十二 / 十三 / 十四 / 十五拍未提交 ⇒ 就地返工 ⇒ 本拍 = **第五层补丁** `ev/patch108l5.py`（**10 步**）。
改序仍是 `part108/{_mods.html,panel.css,panel.js}`（前两件走 `ev/splice108.py`）→ `apply108.py`（**无需** `make108.py`）。
★ **未动任何其他模块**：`task-detail.html` / `base.html` 一字未动。

**落地**：① 旧浮层 `.td-sum-prev` 整体拆掉（DOM + CSS + `.td-mod.td-sum{position:relative}` + **Esc 裁决链那一层**），
新载体 `#av-browse-pane-preview[data-td-pane="preview"]` ⇒ 点产物 `openTab('preview', {name, ico})`；
实测点第 1 个 ⇒ 页签 `[摘要, 预览]` / `name='右栏复刻方案.md'` / `ico=true` / `md=flex xlsx=none` / **barH 40**，
点第 2 个 ⇒ **页签仍 1 枚**但改名换图标（`sidepanel-metrics.xlsx` / 表格字形 / `md=none xlsx=flex`），页签 `×` ⇒ `preview` 回 `hidden`、`summary` 回 40px；
残留自检 `residue = {overlay:false, paneCount:1, sumPos:'static', prevElGlobal:'undefined'}`、`zd-sum-prev` **0**。
② `transform-origin` **`320px 0px`**（卡宽 320 = 100% 0）；同一次 eval「点 + rAF 采样」（`recN=50/50`）：
收 ⇒ `scale 1→0.62` + `translate 0px→12px -12px` + `opacity 1→0`（186ms 到目标 / 203ms `hidden`）；
展 ⇒ `@keyframes zd-panel-in` 260ms，首帧 `scale .62 / translate 12px -12px` ⇒ **过冲 `1.03715`** ⇒ 回 `1 / 0px`（453ms）。
③ 四件 computed = `color(srgb 1 1 1 / 0.78)`（下拉 `0.82`）+ `backdrop-filter: blur(18px) saturate(1.6)`，暗色卡 `color(srgb 0.137255 0.137255 0.141176 / 0.78)`；
`CSS.supports('backdrop-filter','blur(2px)')` = **true**；**像素取证**：铺 320×180 纯红 ⇒ 卡面 `rgb(255,199,199)`（= `0.78×白 + 0.22×红`），
沿 y 衰减 `199`(y40) → `211`(y170) → `237`(y190，**已越出红块下沿仍带红 = 模糊外溢**) → `254`(y470)；正常页面底同点位 `rgb(246,248,253)`。
★ 顺带对齐：预览模块两件控件各收 26px ⇒ 预览工具条 **40 = 摘要 40**。

**排掉的六处坑**（PLAYBOOK **P3.52**）：① ★★★ **删变量只删定义不删引用 ⇒ 按一次 Esc 抛 `ReferenceError`**
（`prevEl` / `prevOpen` 悬空且处在 `window` 捕获段 ⇒ 整条处理器抛错、并带坏「关整条侧栏」；判据要**剥注释** + **保 `\b` 词界**，`prevOpenBtn` 会命中 `prevOpen`）；
② ★★ **`openTab` 复用分支不更新页签名/图标**（连点两个产物 ⇒ 页签写第一个、正文是第二个；修 = 加 `if (opts)` 守卫）；
③ ★★ **`.td-mod-bar` 是内容驱动高度**（`min-height` 被压平 ⇒ 真高 = `6 + max(内容高) + 6 + 1`；内容盒上限 27px，28px 砖必溢出 1px）；
④ ★★ **同页工具条本就不齐**（fs14 摘要 40 / 审查 41；fs18 41 / 49 / 46）；
⑤ ★ **只写 `backdrop-filter` 而底色不透明 = 看不出效果**（computed 却报 `blur`）⇒ 必须落像素；
⑥ ★ **`verify-design.py` 会重写 `pages/gaps.log`** ⇒ 收尾 `git checkout --`。
★ 另有两处探针自身假失败：首帧量到「侧栏滑入中」的坐标（⇒ 新增 60ms 等待的 `slot` 相位）、`on()` 对**没有页签**的模块点不到（⇒ 改走 `[data-td-open-mod]` 建页签）。

**探针**：`ev/p108r.js`（相位探针）+ `probe108r.sh`（全链）+ `probe108r2.sh` / `on.js`（复测 + 五模块工具条对照表）；
日志 `ev/r-raw.log` / `r2-raw.log` / `r3-raw.log` / `r4-raw.log` / `r5-raw.log`（最终 14890 字节）。
**截图** `raw/r-1440-pv-md.png` / `r-1440-pv-xlsx.png` / `r2-tabs-after-pvB.png` / `r-card-over-red.png` / `r-card-over-page.png` / `r-1440-dark.png` / `r2-bars-fs14-terminal.png` / `r2-bars-fs18-preview.png`。

**门禁**：五层幂等（l1 全跳过 / l2 `0/8` / l3 `0/27` / l4 `0/8` / **l5 `0/10`** + 5/5 跨层断言「全部存活 ✓」）/ `apply108.py` 第二遍「已是目标态」/
`check-syntax.py pages/*.html` **10/10** / `verify-design.py ./pages` 与基线**逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c` / 21882 字节）/
`scan-flatten.py part108/panel.css` **2 条**（基线）/ `pages/gaps.log` 已 `git checkout --` 清理。
**产物**：`conversation.html` 1012144 → **1015095 字符（+2951）**（`git diff --numstat` = `1047  107`）；
LF bytes **1124149** / 工作区 bytes **1132584** / **8436 行** / LF `sha1_lf da1acf6a091c`；
`task-detail.html` **767836（本拍未动，仍 `7  0`）**；`base.html` **逐字节不变**；代数核对 `r108-conv-css` / `r108-conv-js` / `r108-l5` 各 1、`r107-conv-*` / `zd-sum-prev` 全 0。
**验收** `mg-work/r108/acceptance.md` **二十九节**（二十五 ~ 二十九 = 第十六拍）；**记忆同步** `ev/doc108r.py`（本文件）。
★ **顺手修掉上一轮的错**：`doc108q.py` 把 PLAYBOOK 附录第 **58** 条当成锚点整条替换掉（实为 62 条、标题却写 63）⇒ 本轮**补回 58 并加到 69 条**。
🚫 未 commit / 未 push。
"""


def main():
    print(u'=== 1/7 HANDOFF.md ===')
    span(HOF, u'> ⚠️ **最新一拍 = r108 第十五拍', u'> ★★ **本拍五条坑**见 PLAYBOOK **P3.51**',
         HOF_TOP, u'HANDOFF', u'顶部「最新一拍」块整块换新（第十五拍降级为「上一拍」）')
    patch(HOF, HOF_STEPS, u'HANDOFF')
    # 二·h 段末追加「### 第十六拍」（anchor = 第十五拍那一段末的「⑥ 交接」整块）
    patch(HOF, [(HOF_16_ANCHOR, HOF_16_ANCHOR + HOF_16, u'二·h 段末追加「### 第十六拍」')], u'HANDOFF')

    print(u'=== 2/7 PAGES.md ===')
    patch(PAG, PAG_STEPS, u'PAGES')
    patch(PAG, [(PAG_ANCHOR, PAG_ANCHOR + PAG_14, u'P3.11i 追加 ⑭ 第十六拍要点')], u'PAGES')

    print(u'=== 3/7 PLAYBOOK.md ===')
    patch(PBK, [
        (PBK_APP_INTRO_OLD, PBK_APP_INTRO_NEW, u'附录引言 → 69 条 + 说明补回 58'),
        # ★ 补回被上一轮误顶掉的第 58 条（插在 59 条之前；59 原样接回 ⇒ keep_anchor=True）
        (PBK_59_OLD, PBK_58_BACK, u'补回被误顶掉的第 58 条'),
        (PBK_63_OLD, PBK_63_OLD + PBK_64_69, u'附录追加 64~69 六条'),
        # ★ 一步同时完成「在其前插入 P3.52」+「标题 63 → 69 条」——自包含、check 模式才有意义
        (PBK_APP_HEAD, PBK_P352 + PBK_APP_HEAD_NEW, u'附录前插入 P3.52 + 标题 → 69 条'),
    ], u'PLAYBOOK')

    print(u'=== 4/7 MEMORY.md（仓库） ===')
    patch(MEM, MEM_STEPS, u'MEMORY')
    patch(MEM, [(None, MEM_16, u'追加第十六拍段')], u'MEMORY')

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
    patch(LOG_REPO, [(None, LOG, u'追加第十六拍段')], u'log-repo')

    print(u'=== 7/7 log-ws ===')
    patch(LOG_WS, [(None, LOG, u'追加第十六拍段')], u'log-ws')

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
