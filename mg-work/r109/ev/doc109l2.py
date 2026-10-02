# -*- coding: utf-8 -*-
u"""r109 第二拍收尾：把「五条 + 一条配套」同步进记忆文档。

范围（同步的是「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— L4 时间戳 + 顶部插入「最新一拍 = r109 第二拍」块（第一拍降级为「上一拍（同代）」
                                      + §二·i 标题改「共两拍」+ §二·i 追加「第二拍」节 + §六 加第 50 条
                                      + §七 状态行改「第一 / 二拍」+ §八 回滚段补 patch109l2
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题 + 固定事实表追加 5 行 + 必看清单追加 27~31 五条
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录前插入 **P3.57**（八条新教训）+ 附录标题「98 条」→「106 条」
                                      + 附录追加 99~106 八条
  4) .workbuddy/memory/MEMORY.md    —— 追加 r109 第二拍段
  5) 两份当日日志 **2026-10-02.md**（仓库内 + 工作区）—— 追加 r109 第二拍段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 在限额内更新「最近拍」

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换另给显式 mark。
★ 「mark 歧义」硬断言：mark 与 old **同时**存在 ⇒ 只可能 mark 不唯一 ⇒ `sys.exit`；
  豁免位判据 = `old in new`（「把锚点原样保留在 new 里」的写入本来就要求锚点留下当下层契约）。
★ 用法： python ev/doc109l2.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc109l2.py --check    # 只校验锚点命中数 + 工作区字符预算（不写）
⚠ 正文里有 `%` / `{` 这类字符 ⇒ **不用 `%` / `.format()`**，改用 `@WHEN@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-02 10:2x'

MEMDIR = os.path.join(REPO, '.workbuddy', 'memory')
HOF = os.path.join(MEMDIR, 'HANDOFF.md')
PAG = os.path.join(MEMDIR, 'PAGES.md')
PBK = os.path.join(MEMDIR, 'PLAYBOOK.md')
MEM = os.path.join(MEMDIR, 'MEMORY.md')
LOG_REPO = os.path.join(MEMDIR, '2026-10-02.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-02.md')
WSMEM = os.path.join(WS, '.workbuddy', 'memory', 'MEMORY.md')

WSMEM_BUDGET = 3000          # ★ 工作区 MEMORY.md 限额（超了会被截断注入 ⇒ 等于没写）

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def subst(s):
    return s.replace(u'@WHEN@', WHEN)


def patch(p, steps, label):
    """steps = [(old, new, sub)]；old=None ⇒ 尾部追加（文件不存在则新建）。"""
    if not os.path.exists(p):
        if CHECK:
            BAD.append(u'%s：文件不存在' % label)
            return
        wr(p, u'', u'\n')
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
                sys.exit(u'!! %s · %s：mark 与锚点同时存在 ⇒ mark 不唯一\n   mark=%r'
                         % (label, sub, mark[:200]))
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
    if len(t) != n0:
        wr(p, t, nl)
    print(u'   %-46s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


# ============================================================ 公共文案

R109_L2_TOP = u"""> 🚧 **最新一拍 = r109 第二拍（五条 + 一条配套 · ★★ 同代就地返工 —— 第一拍尚未提交 ⇒ 按硬规则就地改 `ev/patch109l2.py`）** —— **🚫 未提交**（判据 `git status` 仍是 ` M pages/conversation.html`）：
> 本拍 = **右栏四条精修 + 终端字号 + 图标重画 + 锚点从「只读标记」升级成「可交互对象」**，**未动任何其他模块**（`task-detail.html` / `base.html` 一字未动）。
> ① **右栏展开 ⇒ `zd-host` 自动折叠为胶囊 → 已做**：信号源 = 宿主状态类 **`.av-browse-on`**（打在 `div:has(> main)` = `#av-browse-slot.parentElement` 上、宿主 `setOpen()` **唯一**写入）；
>   **不 hook 开关的 `click`**（收起右栏有**三条**路径 + `ensureOpen()` 还会**合成** `b.click()` ⇒ 必漏）；**反向不摊回**（邵先生只说「展开**时**折叠」）；`childList` 观察器兜 React 重挂。
>   真机矩阵（`p109k.js`）：`a0 fresh on:false / card visible 320×484` → `a2 展开 on:true / card hidden / mini 103.09×32 visible` → `a3 手动摊回 card visible 455,105` → `a4 收起 on:false / card 仍 visible`。
> ② **终端模块字号全 13px → 已做**：`--font-size-body-1`(12) → `--font-size-body-2`(13)，**四条一起换**（`.td-term` / `-tabs` / `-tab` / `-tabadd`）；
>   ⚠ 标签条在 DOM 上是 `.td-term` 的**兄弟** ⇒ 追问后邵先生定「**整个终端模块都改**」。**盒模型一行未动** —— 真机 `termFs 13/13 · tabsFs 13 · tabFs 13/13 · tabaddFs 13`；
>   `lh 20` / `tabs minH 34` / `tab h 22` / `tabadd 22×22` / `caret 7×13` 全同；`term 639×764` 无内滚无横溢（`scrollH==clientH`）、标签文字 `clipped:false`。
> ③ **`r93-ib r93-bt`（重新生成）图标重画 → 已做**：★★ **落点 = `ev/make109.py` 的 `EDITS` 表 E8** —— `apply109.py` 是**生成物**（`make109.py` 从 `apply108.py` 逐字生成），直接改会被下次重跑**静默冲掉**。
>   新串 `M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5`（`stroke-width 1.3` / `round`）+ `M2.07 11.4 5.61 9.61 1.05 7.56Z`（`fill`）；真机 `d` 逐字命中、旧串 `M13.9 9.4` 全页 **0** 次。
>   ★ 拟合判据 = **坏格数**（a=1 / b=5 / c=7）**不是总 err**（c 的 2.192 < a 的 2.298 但是**过拟合**）；★「越界包络罚项」是**错的**（把正确的弧顶也罚了 ⇒ err 2.3 → 10.7）。
> ④ **已批注锚点 ⇒ 以编辑态显示详情 → 已做**：`noteOfAnchor()` 反查 + `noteEdit(el, at)`（`ref = at || el`，气泡按**锚点**定位）+ `noteDrop()` 换按钮语义（`role="button"` / `tabindex="0"` / `aria-label` / `title`）。
>   真机：气泡重开 / `taValue` 原文逐字回填 / `pin "1"` + `is-done` / `ok disabled:false` / **`气泡顶 = 锚点底 + 8`**；改文案再提交 ⇒ `anchorCount 1→1`、`left/top` 不动（**就地 update**）。
> ⑤ **锚点支持任意拖动 → 已做**：pointer + `window` 捕获段（`pointermove/up/cancel/blur`）+ **4px 阈值分流「拖 vs 点」** + `anchorPlace()` 夹进 `.td-view` 可视区；
>   CSS `cursor:grab` / `.is-dragging{cursor:grabbing}` / `touch-action:none` / `user-select:none`、**刻意无 `transition`**（拖影）、**不抬 `z-index`**（气泡 z=3 压着）。
>   真机（**真鼠标** `mouse move/down/up`）：`+40/+30` ⇒ 内联 `202→242 / 182→212` **精确**、松手 `elnoteHidden:true`（**没弹气泡**）；拖到视口 `1439,899` ⇒ 夹到 `605/734` == `expectMax`。
>   ★★ **配套修掉一条 ⑤ 引出的必现缺陷**：`.td-elnote` 是 `.td-view`（`overflow:auto`）的**子件** ⇒ 锚点贴底时 `top = 锚点底 + 8` 把气泡**整块**推出可视区
>   （实测 `bubbleBottomBelowView 116` / `visibleH −8` / **`fullyHidden true`**）⇒ 补「可视带夹取」且 **先摘 `[hidden]` 再量高**（`.td-elnote` 实测无 `transition` ⇒ 不引位移动画）；
>   修后 `0 / 108 / false`，而**常态仍是 `气泡顶 = 锚点底 + 8`**（`bubbleDTop 8`）⇒ l1 已验收观感**一字未变**（`conversation.html` **+1042 字符**就是这条）。
> ★ **补丁 = `ev/patch109l2.py`**（**12 条编辑** = css 4 / js 6 / l1 判据 1 / make109 1；`应用 1 → 复跑 0 / 12` 幂等）。
> ★★ **本拍八条坑**见 PLAYBOOK **P3.57**（★★★ `applyNNN.py` 是**生成物** / ★★ 追加式编辑走 `strict=False` / ★★★ 反解看**坏格数**不看总 err /
>   ★★★ 防过拟合靠**物理边界**不靠罚项 / ★★ 1× 真机与 SS=8 **不可逐格比** / ★★★ 观察**宿主状态类**别 hook 交互事件 / ★★★ 加可拖件必查祖先 `overflow` 裁不裁配套浮层 / ★★ 判「是 bug 还是探针 bug」先看事件序列完整否）。
> **门禁**：`check-syntax` **10/10**；`verify-design` 与 `vd-l1now.txt` / `vd-l2.txt` **双 0 diff**（零新增、一处渐变都没引）；`scan-flatten part109/panel.css` **仍 2 条**；
>   ★★ **自愈实证**：从 `ev/bak-l2/` 干净基线**全量重放**（应用 10 / 跳过 2）⇒ 产物与「就地修改后」的产物 **逐字节 0 差异**。
> **产物**：`conversation.html` 1036907 → **1045713 字符（+8806）**（**8918 行**；LF bytes **1167288**；md5 **`dc240794ab4ed6d262b02b739f68753f`**）；
>   `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**（md5 `044ca6c6d134534f9383685f597aede4`）。
> 逐条实测见 `mg-work/r109/acceptance.md`（**十一 ~ 十八节**）；机制级教训见 PLAYBOOK **P3.57**；本页固定事实见 PAGES **P3.11i**。
> 🚫 未 commit / 未 push。
"""

HOF_TOP_OLD = u"""> 🚧 **最新一拍 = r109 第一拍（四条 · ★ 新一代 —— r108 已交付 `172e580` ⇒ 按硬规则新建 `mg-work/r109/`）** —— **🚫 未提交**"""

HOF_TOP_NEW = R109_L2_TOP + u"""
> ▸ **上一拍（同代 · 第一拍）= r109 第一拍（四条 · ★ 新一代 —— r108 已交付 `172e580` ⇒ 按硬规则新建 `mg-work/r109/`）** —— **🚫 未提交**"""

SEC2I_L2 = u"""
### 第二拍（r109 第二层补丁 · 五条 + 一条配套 · 2026-10-02 09:xx 邵先生 · **就地返工 `ev/patch109l2.py`**）

> 需求逐字：① 「当右栏展开时，`zd-host` 容器会自动折叠为迷你按钮状态」；② 「`td-term` 容器内的字号都调整为 13px」；
> ③ 「`r93-ib r93-bt` 这个重新生产的图标异常，请修复」；④ 「添加已添加的批注的锚点 `td-anchor` 会以编辑态的形式显示批注详情」；
> ⑤ 「批注的锚点 `td-anchor` 需要支持任意拖动位置」。
> ★ 唯一追问（② 的范围）：标签条在 DOM 上是 `.td-term` 的**兄弟** ⇒ 邵先生答「**整个终端模块都改 13px**」。

**落地面**：`part109/panel.css` 83427 → **84764**；`part109/panel.js` 77185 → **84643**；
`part109/browse.html` **106685（0，四片同长）**；`ev/make109.py` 5139 → **7629**；`apply109.py` 190523 → **191131**（3658 行 / 8 处替换）；
`pages/conversation.html` 1036907 → **1045713**（+8806 / 8918 行 / md5 `dc240794ab4ed6d262b02b739f68753f`）。
**改序**：`ev/patch109l2.py` → `ev/splice109.py` → `ev/make109.py` → `apply109.py`。

**① 右栏展开 ⇒ zd 折胶囊**：盯 `.av-browse-on`（宿主 `ctrl-conv.js` 的 `setOpen()` 唯一写入、打在 `div:has(> main)` 上）；
`MutationObserver({attributes, attributeFilter:['class']})` + `childList` 兜 React 重挂；**反向不摊回**。
真机矩阵 a0/a1/a2/a3/a4 见上（`a2` = 自动折叠那一步：`on:true` / `card hidden` / `mini 103.09×32`）。
⚠ **取证顺序**：「初态」必须**独立一趟**取 —— 第一版把 ① 排在被 ② 的 `ensureOpen()` 打开右栏之后 ⇒ `toMini()` 早跑完、a0 失去鉴别力。

**② 终端字号 13px**：四条 token 换 `--font-size-body-2`；`--ui-fs:14` ⇒ `ratio 1` ⇒ 恰好 13px。
盒模型零改动、真机逐项读数见 PAGES P3.11i 那行。

**③ regen 图标**：落点 = `make109.py` 的 `EDITS` 表 E8；拟合 err **15.046 → 2.298**（6.5×）、坏格 **1 个**；
真机墨迹盒 `(1,5,12,10)` 与设计**一致**；1× 真机按**各自最深像素**归一后 err 1.620 / 5 个亚像素格。

**④ 锚点 ⇒ 编辑态详情**：`noteOfAnchor` 反查 + `noteEdit(el, at)` + `noteDrop` 按钮语义；真机 `气泡顶 − 锚点底 = 8`、`pin 1`、`ok 可用`、改文案就地 update。

**⑤ 锚点可任意拖 + 配套的「气泡可视带夹取」**：4px 阈值分流 / `anchorPlace` 夹 `.td-view` 可视区 / 无 transition；
★ 实测出来的必现缺陷（锚点贴底 ⇒ 气泡 `visibleH −8`、`fullyHidden true`）与修法（先摘 `[hidden]` 再量高 + `top = vBot − h`）见 `acceptance.md` §16.3。

**★ 探针 bug 一例**：合成 `a.click()` 不经过 `pointerdown` ⇒ `_tdMoved` 不复位 ⇒ 误报「重开失败」；真机路径本来是对的（改真鼠标 `move/down/up` 复核）。

**门禁**：`check-syntax` 10/10｜`verify-design` 双 0 diff｜`scan-flatten` 仍 2 条｜`patch109l2` 幂等（0/12）｜★ 自愈实证：从 `ev/bak-l2/` 全量重放 **0 差异**。
**取证资产**：`ev/p109{k,g,h,i,j,r}.js` + `ev/probe109l2.sh` + `raw/{f-zd-mini, g-regen-btn, d2-anchor-*, e2-anchor-*, cmp-regen-l2, l2-evidence}.png`。

"""

ITEM50 = u"""50. ★★ **`regen` 图标重画的正确落点是「生成器」** —— `mg-work/r109/apply109.py` 是 `ev/make109.py` 从 `apply108.py` **逐字生成**的
    （`EDITS` 表 = 全部差异）⇒ 图标 / 常量表 / 生成期替换类改动**只能**改 `make109.py` 的 `EDITS` 表；
    直接改 `apply109.py` 会在下一次重跑时**被静默冲掉**。★ 推论：**先问「谁生成的 apply」。**
51. ★★ **`td-anchor` 已经不再是「只读标记」** —— r109 第二拍把它升级成**可点开详情 / 可任意拖动**的对象
    （`role="button"` + `tabindex="0"` + `keydown` Enter/Space）。改这块时：`aria-hidden="true"` **不能**再挂（那会儿它确实只是标记）；
    拖动用 `pointer` + `window` **捕获段** + **4px 阈值**分流「拖 vs 点」，且 `_tdMoved` **必须在 `pointerdown` 处复位**（只在 `click` 里复位 ⇒ 松手落在锚点外时标记会卡住）。
52. ★★ **`.td-view` 是 `overflow:auto`，它的绝对定位子件会被裁** —— 任何「可以跑到边角」的浮层都要自己夹在
    `[scrollTop, scrollTop + clientHeight]` 里；⚠ 量高度**必须先把 `[hidden]` 摘掉**（隐藏态 `offsetHeight` 恒为 0 ⇒ 夹取失效）。

"""

# ---- PLAYBOOK P3.57 ----
PBK_P357 = u"""## P3.57 ★★ r109 第二拍（五条 + 一条配套 · 2026-10-02 09:xx 邵先生）—— ★★ 八条新教训

**★ 判据速查（本轮实测值）**：`termFs 13/13` / `tabsFs 13` / `tabFs 13/13` / `tabaddFs 13`；`lh 20` / `tabs minH 34` / `tab h 22` / `tabadd 22×22` / `caret 7×13`；`term 639×764`（`scrollH==clientH`）；
`regen`：`d` = 新串、旧串 `M13.9 9.4` **0** 次、墨迹盒 `(1,5,12,10)` 与设计一致；
`noteEdit` 重开：`elnoteHidden false` / `taValue` 原文 / `pin "1"` `is-done` / `ok disabled:false` / **`气泡顶 − 锚点底 = 8`**；
拖动：`+40/+30` ⇒ 内联 `202→242 / 182→212`、松手 `elnoteHidden:true`；越界拖 ⇒ `605/734` == `expectMax`；
夹取前 `bubbleBottomBelowView 116` / `visibleH −8` / `fullyVisible false` ⇒ 夹取后 `0 / 108 / true`；`docOverflowX 0`。

1. ★★★ **`applyNNN.py` 是生成物，不是手改对象** —— 它是 `ev/makeNNN.py` 从**上一代 apply 逐字生成**的（`EDITS` 表 = 全部差异，表以外一字不差）。
   ⇒ 「图标 / 常量表 / 生成期替换」类改动的**唯一落点 = `makeNNN.py` 的 `EDITS` 表**；直接改 applyNNN **会被下次重跑静默冲掉**。
   ★ 自检：改完 maker 重生成 apply，量「行数 / 字符数 / 替换处数」三件套。
2. ★★ **「追加式」编辑必须显式 `strict=False`** —— 当 `new` 原样包含 `old`（把锚点保留在 new 里当下层契约）时，
   STRICT 的「mark 与 `old` 同存 ⇒ mark 不唯一」判据**必然误报**（`old` 永远是 `new` 的子串）。
   幂等性仍由 mark 保证（重跑时 `count(old)` 还是 1，没有 mark 会**再追加一遍**）。
3. ★★★ **反解 / 拟合类判据看「坏格数」，不看总 err** —— 多起点能拿到总 err **2.192 < 2.298** 的「c 解」，
   但它有 **7 个格**与设计差 ≥0.33；a 解只有 **1 个**。**总 err 最小 ≠ 最贴设计**（c 是过拟合）。
   判据口径：先定阈值（本拍 |Δ| ≥ 0.33）、再数坏格、最后才看 err。
4. ★★★ **防过拟合靠「参数的物理边界」，不靠罚项** —— 给 `err()` 加「越界包络罚项」会把**正确的解**一起罚掉
   （设计真值在弧顶下方**本来就有洞**）⇒ err 从 2.3 抬到 **10.7**、解被推到「弧更扁」的另一侧。
   正解 = 收紧参数的物理边界（本拍 `BOX=(0.10,4.20,13.90,11.00)` 墨迹盒硬约束）。
5. ★★ **真机 1× 截图与「SS=N 数学模型」不可逐格比** —— 归一化必须按**各自最深像素**
   （本拍设计最深 134 / 真机最深 78 ⇒ 若都除以设计口径 121，真机每格被系统性放大 ~46% ⇒ 假失败 err 3.043 / 25 坏格 → 真值 1.620 / 5 格）。
   1× 真机只判两件事：**① 墨迹盒一致 ② 观感一致**；逐格精度回数学模型里判。
6. ★★★ **要「联动某个整体状态」⇒ 观察宿主自己就在用的状态类，别 hook 交互事件** ——
   「右栏展开」有**三条**退出路径（开关 / Esc / 面板自带的关闭钮）+ `ensureOpen()` 还会**合成** `b.click()` ⇒ hook click **必漏**；
   盯 `.av-browse-on`（打在 `div:has(> main)` 上、宿主唯一写入）才是**收敛点**。⚠ 宿主是 React ⇒ 元素会**重挂**，要配 `childList` 观察器重新认行。
7. ★★★ **加「可拖到任意位置」的件 ⇒ 必须一起查它的配套浮层会不会被祖先 `overflow` 裁掉** ——
   `.td-elnote` 是 `.td-view`（`overflow:auto`）的**子件** ⇒ 锚点贴底时 `top = 锚点底 + 8` 把气泡**整块**推出可视区（实测 `visibleH −8` / `fullyHidden true`）。
   修法 = 可视带夹取 + **先摘 `[hidden]` 再量高**（隐藏态 `offsetHeight` 恒 0）；⚠ 改完要**同时复量「常态」**（本拍 `气泡顶 − 锚点底` 仍 = 8 ⇒ l1 观感一字未变）。
8. ★★ **判「是 bug 还是探针 bug」先看事件序列完不完整** —— 合成 `el.click()` **不经过 `pointerdown`** ⇒
   「拖动后复位标记」那一步不会发生 ⇒ 误报「重开失败」。**真机路径本来就是对的**。⇒ 交互类判据**一律用真鼠标**（`mouse move/down/up`），
   合成事件只用于「点开语义」这类不含手势分流的场景。

**★ 门禁（本轮）**：`check-syntax` **10/10**；`verify-design` 与 `vd-l1now.txt` / `vd-l2.txt` **双 0 diff**；`scan-flatten part109/panel.css` **仍 2 条**；
`patch109l2` 幂等（第二次 **0 应用 / 12 跳过**）；★★ **自愈实证**：从 `ev/bak-l2/` **干净基线全量重放**（应用 10 / 跳过 2 / 全部存活 ✓）⇒ 产物与就地修改产物 **`diff` 0 差异**。

"""

# ---- PAGES ----
PAGES_ROWS = u"""| **右栏展开 ⇒ `zd-host` 折胶囊** | ★★ **r109 第二拍 ①**：盯宿主状态类 **`.av-browse-on`**（`div:has(> main)` = `#av-browse-slot.parentElement`，宿主 `setOpen()` 唯一写入）⇒ 变 `true` 即 `toMini()`；**反向不摊回**。⚠ 别 hook 开关 `click`（收起有三条路径 + `ensureOpen()` 合成 `b.click()`）；`childList` 观察器兜 React 重挂。真机：`a2 on:true card hidden / mini 103.09×32`。 |
| **终端模块字号 = 13px** | ★ **r109 第二拍 ②**：`.td-term` / `-tabs` / `-tab` / `-tabadd` 四条由 `--font-size-body-1`(12) 换 `--font-size-body-2`(13)；**盒模型零改动**（`lh 20` / `tabs 34` / `tab 22` / `tabadd 22×22` / `caret 7×13`）。⚠ 标签条是 `.td-term` 的**兄弟**（追问后定「整个终端模块都改」）。 |
| **`regen` 图标（`r93-ib r93-bt`）** | ★★ **r109 第二拍 ③**：★★ **落点 = `ev/make109.py` 的 `EDITS` 表 E8**（`apply109.py` 是生成物，直接改会被重跑冲掉）。新串 `M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5` + `M2.07 11.4 5.61 9.61 1.05 7.56Z`（`stroke-width 1.3` / `round`）。真机墨迹盒 `(1,5,12,10)` 与设计**一致**。 |
| **`.td-anchor` 的交互语义（★ 已不再是只读标记）** | ★★★ **r109 第二拍 ④⑤**：④ 点锚点 ⇒ **编辑态**详情（`noteOfAnchor` 反查 + `noteEdit(el, at)` 按**锚点**定位 + `noteDrop` 换 `role/tabindex/aria-label/title`）；⑤ **可任意拖动**（pointer + `window` 捕获段 + **4px 阈值**分流 + `anchorPlace()` 夹 `.td-view` 可视区；`cursor:grab`、**无 transition**）。判据：`气泡顶 − 锚点底 = 8`；拖 `+40/+30` ⇒ 内联精确 `+40/+30`。 |
| **`.td-elnote` 必须夹在 `.td-view` 可视带内** | ★★★ **r109 第二拍 ⑤ 配套**：锚点可拖到任意位置 ⇒ `.td-elnote`（`.td-view` 的**子件**、祖先 `overflow:auto`）在锚点贴底时会被**整块裁掉**（实测 `visibleH −8` / `fullyHidden true`）⇒ `noteEdit()` 加可视带夹取、并且**先摘 `[hidden]` 再量高**（隐藏态 `offsetHeight` 恒 0）。⚠ `.td-elnote` 无 `transition` ⇒ 把写 `top` 挪到摘 `[hidden]` 之后不引位移动画。 |
"""

PAGES_MUST = u"""
27. ★★★ **改「整体状态联动」别 hook 交互事件** —— 一个状态常有多条进出路径 + 脚本还会**合成** click ⇒ hook click 必漏；
    一律**观察宿主自己就在用的那个状态类**（r109：`.av-browse-on`），并配 `childList` 观察器兜 React 重挂。
28. ★★★ **加可拖 / 可移动的件 ⇒ 顺手查它的配套浮层会不会被祖先 `overflow` 裁掉**（r109：`.td-elnote` 是 `.td-view` 的子件 ⇒ 锚点贴底时气泡 `visibleH −8`）。
    修法与三条安全前提见 PLAYBOOK **P3.57⑦**。
29. ★★ **「生成器 + 应用器」两段式里，改动的落点要问「谁生成的 apply」** —— r109 的图标重画落点是 `ev/make109.py` 的 `EDITS` 表，
    不是 `apply109.py`（后者是生成物、会被重跑冲掉）。见 PLAYBOOK **P3.57①**。
30. ★★ **拟合 / 反解类判据先定阈值、再数「坏格数」，最后才看总 err** —— 总 err 更小的解可能是过拟合（r109：2.192 的解有 7 个坏格，2.298 的解只有 1 个）。
31. ★★ **真机 1× 截图与数学模型不可逐格比** —— 归一化按**各自最深像素**（r109：134 vs 78 ⇒ 混用会假失败），1× 真机只判「墨迹盒 + 观感」。
"""

# ---- MEMORY.md（仓库）----
MEM_L2 = u"""
### r109 第二拍（五条 + 一条配套 · 同日 09:xx 邵先生 · **就地返工 `ev/patch109l2.py`**）—— 🚫 未提交

> ① **右栏展开 ⇒ `zd-host` 自动折胶囊**：盯宿主状态类 **`.av-browse-on`**（`div:has(> main)`、宿主 `setOpen()` 唯一写入）⇒ `toMini()`；**反向不摊回**；
>   别 hook 开关 `click`（三条收起路径 + `ensureOpen()` 合成 `b.click()`）。真机 `a2 on:true / card hidden / mini 103.09×32 visible`。
> ② **终端模块全 13px**：四条 `.td-term*` 由 `--font-size-body-1`(12) 换 `--font-size-body-2`(13)；**盒模型零改动**（`lh 20` / `tabs 34` / `tab 22` / `tabadd 22×22`）。
>    ⚠ 标签条是 `.td-term` 的**兄弟** ⇒ 追问后邵先生定「整个终端模块都改」。
> ③ **`regen` 图标重画**：★★ 落点 = **`ev/make109.py` 的 `EDITS` 表 E8**（`apply109.py` 是生成物 ⇒ 直接改会被重跑静默冲掉）；
>    新串 `M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5` + `M2.07 11.4 5.61 9.61 1.05 7.56Z`；拟合 err **15.046 → 2.298**、坏格 **1**；真机墨迹盒 `(1,5,12,10)` 与设计一致。
> ④ **锚点 ⇒ 编辑态详情**：`noteOfAnchor` 反查 + `noteEdit(el, at)` + `noteDrop` 按钮语义（`role/tabindex/aria-label/title`）；真机 `气泡顶 − 锚点底 = 8`、`pin "1"`、改文案**就地 update**。
> ⑤ **锚点可任意拖**：pointer + `window` 捕获段 + **4px 阈值** + `anchorPlace()` 夹 `.td-view` 可视区；`cursor:grab`、**无 transition**、不抬 `z-index`。
>    ★★ **配套修掉 ⑤ 引出的必现缺陷**：锚点贴底 ⇒ `.td-elnote` 被 `.td-view`（`overflow:auto`）**整块裁掉**（`visibleH −8` / `fullyHidden true`）⇒ 补**可视带夹取** + **先摘 `[hidden]` 再量高**；修后 `0 / 108 / false`，常态仍 = `锚点底 + 8`。
> **八条坑** = **P3.57**（★★★ `applyNNN.py` 是生成物 / ★★ 追加式编辑走 `strict=False` / ★★★ 反解看**坏格数**不看总 err /
> ★★★ 防过拟合靠**物理边界**不靠罚项 / ★★ 1× 真机与 SS=N 不可逐格比 / ★★★ 观察**宿主状态类**别 hook 交互事件 /
> ★★★ 加可拖件必查祖先 `overflow` 裁不裁配套浮层 / ★★ 判「是 bug 还是探针 bug」先看事件序列完整否）。
> **产物**：`conversation.html` 1036907 → **1045713 字符（+8806）**（**8918 行**；LF bytes **1167288**；md5 **`dc240794ab4ed6d262b02b739f68753f`**）；
>   `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **十八节**。
> 门禁：`check-syntax` **10/10**｜`verify-design` 与 `vd-l1now.txt` / `vd-l2.txt` **双 0 diff**｜`scan-flatten part109/panel.css` **仍 2 条**｜`patch109l2` 幂等（0/12 跳过）。
> ★★ **自愈实证**：从 `ev/bak-l2/` 干净基线**全量重放**（应用 10 / 跳过 2）⇒ 产物与就地修改产物 **`diff` 0 差异**。
> 🚫 未 commit / 未 push。
"""

# ---- 当日日志 ----
LOG_L2_REPO = u"""
### r109 第二拍（五条 + 一条配套 · 09:xx 邵先生 · 就地返工 `ev/patch109l2.py`）—— 🚫 未提交

- 五条全部落地 + 真机取证：① 右栏展开 ⇒ `zd-host` 自动折胶囊（盯 `.av-browse-on`）② 终端模块字号全 **13px**（四条 token，盒模型零改动）
  ③ `regen` 图标重画（落点 = `ev/make109.py` 的 `EDITS` 表 E8；err **15.046 → 2.298**、坏格 1）④ 锚点 ⇒ **编辑态**详情（`noteOfAnchor` + `noteEdit(el, at)`）
  ⑤ 锚点**可任意拖**（pointer + 4px 阈值 + `anchorPlace` 夹可视区）。
- ★★ **配套修掉一条 ⑤ 引出的必现缺陷**：`.td-elnote` 是 `.td-view`（`overflow:auto`）的子件 ⇒ 锚点贴底时气泡被**整块裁掉**
  （实测 `visibleH −8` / `fullyHidden true`）⇒ 补「可视带夹取」+ **先摘 `[hidden]` 再量高**；修后 `0 / 108 / false`，常态仍 = `锚点底 + 8`。
- 门禁：`check-syntax` **10/10**｜`verify-design` 与 `vd-l1now.txt` / `vd-l2.txt` **双 0 diff**｜`scan-flatten part109/panel.css` **仍 2 条**｜`patch109l2` 幂等（第二次 **0 应用 / 12 跳过**）。
- ★★ **自愈实证**：从 `ev/bak-l2/` 干净基线**全量重放**（应用 10 / 跳过 2 / 全部存活 ✓）⇒ 产物与就地修改产物 **逐字节 0 差异**。
- 产物：`part109/panel.css` 84764 / `panel.js` 84643 / `browse.html` 106685（0）/ `ev/make109.py` 7629 / `apply109.py` 191131 / `conversation.html` **1045713**（8918 行 / md5 `dc240794ab4ed6d262b02b739f68753f`）。
- 八条机制级教训沉淀为 PLAYBOOK **P3.57**；固定事实进 PAGES **P3.11i**（+5 行 + 必看 27~31）；`acceptance.md` 续到 **十八节**。
- 记忆同步脚本 = `mg-work/r109/ev/doc109l2.py`。🚫 未 commit / 未 push。
"""

LOG_L2_WS = u"""
## r109 第二拍（09:xx · 就地返工 `ev/patch109l2.py`）—— 🚫 未提交

五条 + 一条配套全部落地并真机取证：① 右栏展开 ⇒ `zd-host` 自动折胶囊（盯宿主状态类 `.av-browse-on`，别 hook click）
② 终端模块字号全 13px（四条 token、盒模型零改动）③ `regen` 图标重画（★★ 落点 = `ev/make109.py` 的 `EDITS` 表 E8；err 15.046 → 2.298、坏格 1）
④ 锚点 ⇒ 编辑态详情（`noteOfAnchor` + `noteEdit(el, at)`）⑤ 锚点可任意拖（pointer + 4px 阈值 + 夹 `.td-view` 可视区）。
★★ 顺手修掉 ⑤ 引出的必现缺陷：`.td-elnote` 是 `.td-view`（`overflow:auto`）的子件 ⇒ 锚点贴底时气泡被整块裁掉（`visibleH −8` / `fullyHidden true`）
⇒ 补「可视带夹取」+ 先摘 `[hidden]` 再量高；修后 `0 / 108 / false`，常态仍 = `锚点底 + 8`。
门禁全绿（10/10 · verify-design 双 0 diff · scan-flatten 仍 2 条）；★★ 自愈实证：从 `ev/bak-l2/` 全量重放 ⇒ 0 差异。
产物 `conversation.html` **1045713**（+8806）。教训沉淀 PLAYBOOK **P3.57**；`acceptance.md` **十八节**。🚫 未 commit。
"""

# ---- 工作区 MEMORY.md ----
WSMEM_OLD = u"""## 三、最近拍

- **r107**＝`e9c9498`；**r108 十二 ~ 十九拍**＝✅ `172e580`（**已封板 ⇒ 再改右栏须新建 r109**）。
- **r109 第一拍**（🚫 未提交 · 右栏「批注链路」四件）：删 `td-page-blank` · `td-annot-bar` **挪 `.td-view` 首子件** + `sticky top:0`（末位追不上）· `td-url-annot` 批注态转「浅红底红字」+ 文案「退出批注」· `td-elnote` 按三稿逐像素重做（内距 **12 = 1px 描边 + 11 padding**；高 `12+22n+12+28+12`、封顶 200 内滚；Ctrl ⇒ 按钮「发送」+ 只亮后半句）。补丁 `ev/patch109l1.py`；产物 **1036907 字符**；`acceptance.md` **九节**。
- 新红线：**归零判据先剥三类注释**；**`sticky top` 只在滚动容器首子件之前才追得上**；**隐藏元素量不出几何**。
"""

WSMEM_NEW = u"""## 三、最近拍

- **r107**＝`e9c9498`；**r108 十二 ~ 十九拍**＝✅ `172e580`（已封板 ⇒ 再改右栏须新建 r109）。
- **r109 一 / 二拍**（🚫 未提交 · 右栏批注链路）：一拍＝删灰带 / 标注条贴顶 / 批注钮转红 / `td-elnote` 三稿逐像素。二拍＝右栏展开 ⇒ `zd-host` 折胶囊（盯 `.av-browse-on`）· 终端全 **13px** · `regen` 图标重画（落点 = **`make109.py` 的 `EDITS` 表**）· 锚点**点开 = 编辑态详情 / 可任意拖**（拖到底角 ⇒ 补气泡可视带夹取）。产物 **1045713 字符**；`acceptance.md` **十八节**。
- 新红线：**归零判据先剥三类注释**；**`sticky top` 只在滚动容器首子件之前才追得上**；**隐藏元素量不出几何**；**`applyNNN.py` 是生成物 ⇒ 图标类改动落 `makeNNN.py` 的 `EDITS` 表**；**反解判据看坏格数、不看总 err**；**加可拖件必查祖先 `overflow`**。
"""

# ★ 3000 字符限额的腾位压缩（「最近拍」块本身长了 296 ⇒ 必须从别处等量腾出）。
#   ⚠ 只删冗余字词、**不动任何一条判断口径**；判据 = 脚本末尾的限额硬断言。
WSMEM_TIGHTEN = [
    (u'（单行 bundle ⇒ 用 Python 打片段）', u'（用 Python 打片段）'),
    (u'走绝对路径（细节见 PLAYBOOK P3.21）；**真鼠标 = `mouse move/down/up`**（合成 `PointerEvent` ≠ 真事件）；'
     u'`screenshot [选择器] [路径]`（省略 = 整屏，先 `set viewport 1440 900`）',
     u'走绝对路径（P3.21）；**真鼠标 = `mouse move/down/up`**（合成事件 ≠ 真事件）；'
     u'`screenshot [选择器] [路径]`（先 `set viewport 1440 900`）'),
    (u'（**必须传目录**）与上轮逐条 diff', u'（**传目录**）与上轮 diff'),
    (u'**动效 ≤300ms（CRAFT-ANIM）**。', u'**动效 ≤300ms**。'),
    (u'/ `scale:none` / 选择器层级错 / 探针自身 bug / **沿用上轮 `bakNN/`（混合态）**）。',
     u'/ 选择器层级错 / 合成事件绕过手势 / 探针自身 bug / **沿用上轮 `bakNN/`**）。'),
    (u'里的中文与反引号会出事：含 `>` 的中文串被当**重定向目标**（凭空造 0 字节文件）',
     u'里中文与反引号会出事：含 `>` 的中文串被当**重定向目标**（造 0 字节文件）'),
    (u'- DS 兜底声明 = 基态与 `:hover` **同块、基态在前**；判据 = 真鼠标 hover 读底色。\n'
     u'- 换/挂组件族先读契约 `mapsFrom`（别被类名骗）；「DS 有没有」**查页面内联 bundle**。',
     u'- DS 兜底 = 基态与 `:hover` **同块、基态在前**（判据 = 真鼠标 hover 读底色）；'
     u'换/挂组件族先读契约 `mapsFrom`（别被类名骗）；「DS 有没有」**查页面内联 bundle**。'),
    (u'；修法 = 中间插 `void el.offsetWidth`。', u'；修法 = 插 `void el.offsetWidth`。'),
]

# ---- 工作区 MEMORY.md 的两处计数 ----
WSMEM_HDR_OLD = u"> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.55** + 附录「工作区速览 92 条」·"
WSMEM_HDR_NEW = u"> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.57** + 附录「工作区速览 106 条」·"
WSMEM_SEC_OLD = u"## 二、红线索引（完整 98 条见仓库 PLAYBOOK 附录）"
WSMEM_SEC_NEW = u"## 二、红线索引（完整 106 条见仓库 PLAYBOOK 附录）"


def do_handoff():
    print(u'== HANDOFF.md ==')
    patch(HOF, [
        (u'> 最后更新：2026-10-02 09:4x（**★ r109 第一拍已落地',
         u'> 最后更新：@WHEN@（**★ r109 第二拍已落地',
         u'L4 时间戳'),
        (HOF_TOP_OLD, HOF_TOP_NEW, u'顶部：插入第二拍块 + 第一拍降级'),
        (u'## 二·i ★★ r109 第一拍（会话详情页右栏「批注链路四件重做」· 2026-10-02 08:5x 邵先生 · **共一拍**）—— **🚫 未提交**',
         u'## 二·i ★★ r109（会话详情页右栏「批注链路四件重做」+ 第二拍「五条 + 一条配套」· 2026-10-02 08:5x 起 · **共两拍**）—— **🚫 未提交**',
         u'§二·i 标题'),
        (u'## 三、r88 ~ r92 做了什么（前情提要）',
         SEC2I_L2 + u'## 三、r88 ~ r92 做了什么（前情提要）',
         u'§二·i 追加第二拍'),
        (u'### r109 新增（2 条，均需邵先生点头）',
         u'### r109 新增（5 条，均需邵先生点头）',
         u'§六 标题计数'),
        (u'''    **稿子只给了锚点长相、没给落点** ⇒ 取通行读法（Figma 批注同款）。想换左/右下只需改 `noteDrop()` 的两个 `−12`。
''',
         u'''    **稿子只给了锚点长相、没给落点** ⇒ 取通行读法（Figma 批注同款）。想换左/右下只需改 `noteDrop()` 的两个 `−12`。
''' + ITEM50,
         u'§六 追加 50~52'),
        (u'   **`r109` 第一拍 —— 🚫 未提交**',
         u'   **`r109` 第一 / 二拍 —— 🚫 未提交**',
         u'§七 状态行'),
        (u'# 还原 part 侧：git checkout -- mg-work/r109/part109/（或重跑 ev/patch109l1.py 前的 ev/bak-l1/）',
         u'# 还原 part 侧：git checkout -- mg-work/r109/part109/（或重跑 ev/patch109l1.py 前的 ev/bak-l1/）\n'
         u'# ★ 第二拍（r109-l2）回滚：重跑 ev/patch109l2.py 前的 ev/bak-l2/{panel.css,panel.js}.before（连跑两遍验幂等）',
         u'§八 回滚段'),
    ], u'HANDOFF')


def do_pages():
    print(u'== PAGES.md ==')
    patch(PAG, [
        (u"""### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 ~ 十九拍** + **r109 第一拍「批注链路四件重做」** · 复刻 Codex 右栏 · 2026-10-01 / 10-02 · **共二十拍**）""",
         u"""### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 ~ 十九拍** + **r109 第一拍「批注链路四件重做」** + **r109 第二拍「五条 + 一条配套」** · 复刻 Codex 右栏 · 2026-10-01 / 10-02 · **共二十一拍**）""",
         u'P3.11i 标题'),
        (u"""**同一族的教训**：`display:none` 下量不出任何几何。 |
""",
         u"""**同一族的教训**：`display:none` 下量不出任何几何。 |
""" + PAGES_ROWS,
         u'固定事实表 +5 行'),
        (u"""26. ★★ **改「`--ui-fs` 杠杆下要跟着变的尺寸」时**""",
         PAGES_MUST + u"""
26. ★★ **改「`--ui-fs` 杠杆下要跟着变的尺寸」时**""",
         u'必看清单 27~31'),
    ], u'PAGES')


def do_playbook():
    print(u'== PLAYBOOK.md ==')
    patch(PBK, [
        (u'## 附：工作区速览 98 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         PBK_P357 + u'## 附：工作区速览 106 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         u'插入 P3.57 + 附录计数'),
        (None,
         u"""
99. ★★★ **`applyNNN.py` 是生成物** —— 它是 `ev/makeNNN.py` 从上一代 apply **逐字生成**的（`EDITS` 表 = 全部差异）⇒ 「图标 / 常量表 / 生成期替换」类改动的**唯一落点 = `makeNNN.py` 的 `EDITS` 表**；直接改 apply 会被下次重跑**静默冲掉**（r109 ③ 真踩）。
100. ★★ **「追加式」编辑必须显式 `strict=False`** —— `new` 原样包含 `old`（锚点留下当下层契约）时，STRICT 的「mark 与 `old` 同存 ⇒ mark 不唯一」判据**必然误报**；幂等性仍由 mark 保证。
101. ★★★ **反解 / 拟合类判据看「坏格数」，不看总 err** —— 多起点能拿到总 err **2.192 < 2.298** 却**坏格 7 vs 1** 的解 ⇒ **总 err 最小 ≠ 最贴设计**（那是过拟合）。
102. ★★★ **防过拟合靠「参数的物理边界」，不靠罚项** —— 给 err 加「越界包络罚项」会把**正确的解**一起罚掉（设计真值在弧顶下方本来就有洞）⇒ err 2.3 → **10.7**。
103. ★★ **真机 1× 截图与「SS=N 数学模型」不可逐格比** —— 归一化按**各自最深像素**（r109：134 vs 78 ⇒ 混用假失败）；1× 真机只判「**墨迹盒一致 + 观感一致**」，逐格精度回数学模型里判。
104. ★★★ **「联动整体状态」用「观察宿主状态类」，别 hook 交互事件** —— 一个状态常有多条进出路径 + 脚本还会**合成** click ⇒ hook click 必漏（r109 `ensureOpen()` 真按 `b.click()`）；且宿主是 React ⇒ 配 `childList` 观察器兜重挂。
105. ★★★ **加「可拖到任意位置」的件 ⇒ 必查它的配套浮层会不会被祖先 `overflow` 裁掉** —— `.td-elnote` 是 `.td-view`（`overflow:auto`）的子件 ⇒ 锚点贴底时气泡**整块**出界（`visibleH −8`）；修法 = 可视带夹取 + **先摘 `[hidden]` 再量高**，且**必须同时复量「常态」**（r109 常态仍是 `气泡顶 − 锚点底 = 8`）。
106. ★★ **判「是 bug 还是探针 bug」先看事件序列完不完整** —— 合成 `el.click()` **不经过 `pointerdown`** ⇒ 「拖动后复位标记」那步不发生 ⇒ 误报失败；交互类判据**一律用真鼠标**。
""",
         u'附录 +8 条'),
    ], u'PLAYBOOK')


def do_mem():
    print(u'== MEMORY.md（仓库）==')
    patch(MEM, [(None, MEM_L2, u'追加 r109 第二拍段')], u'MEMORY')


def do_logs():
    print(u'== 当日日志 ==')
    patch(LOG_REPO, [(None, LOG_L2_REPO, u'追加 r109 第二拍')], u'日志(仓库)')
    patch(LOG_WS, [(None, LOG_L2_WS, u'追加 r109 第二拍')], u'日志(工作区)')


def do_wsmem():
    print(u'== MEMORY.md（工作区 · 3000 限额）==')
    steps = [
        (WSMEM_HDR_OLD, WSMEM_HDR_NEW, u'头部计数'),
        (WSMEM_SEC_OLD, WSMEM_SEC_NEW, u'红线索引计数'),
        (WSMEM_OLD, WSMEM_NEW, u'最近拍'),
    ]
    for i, (o, n) in enumerate(WSMEM_TIGHTEN, start=1):
        steps.append((o, n, u'腾位压缩 %d' % i))
    patch(WSMEM, steps, u'工作区 MEMORY')
    if not CHECK:
        t, _ = rd(WSMEM)
        if len(t) > WSMEM_BUDGET:
            sys.exit(u'!! 工作区 MEMORY.md = %d 字符 > 限额 %d —— 必须再压' % (len(t), WSMEM_BUDGET))
        print(u'   工作区 MEMORY.md = %d / %d 字符 ✓' % (len(t), WSMEM_BUDGET))


def main():
    do_handoff()
    do_pages()
    do_playbook()
    do_mem()
    do_logs()
    do_wsmem()
    print()
    if CHECK:
        if BAD:
            print(u'!! 锚点校验失败 %d 条：' % len(BAD))
            for b in BAD:
                print(u'   - ' + b)
            sys.exit(1)
        print(u'锚点校验全部通过 ✓（本模式未写入）')
        return
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print(u'   跳过  ' + s)


if __name__ == '__main__':
    main()
