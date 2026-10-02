# -*- coding: utf-8 -*-
u"""r109 第一拍收尾：把「会话详情页右栏 · 批注链路四件重做」同步进记忆文档。

范围（同步的是「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— 首行时间戳 + 顶部「最新一拍」块整块换新（r108 十九拍降级为「上一拍（已封板）」、
                                      十八/十七拍顺次降级、十二拍改「r108 起始拍」）+ §一 状态段 + conversation 表行
                                      + mg-work 表行（新增 r109）+ §二·h 头改「已封板」+ 新增 **§二·i r109** 节
                                      + §六 追加两条待拍板 + §七 接手清单（加 apply109）+ §八 回滚段加 r109
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题「共十九拍」→「共二十拍」+ 固定事实表新增 4 行（r109 四件）
                                      + 必看清单追加 23~26 四条
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录前插入 **P3.56**（八条新教训）+ 附录标题「92 条」→「98 条」
                                      + 附录追加 93~98 六条
  4) .workbuddy/memory/MEMORY.md    —— r108 段末标「已封板」+ 追加 r109 第一拍段
  5) 两份当日日志 **2026-10-02.md**（仓库内 + 工作区；当日新建）—— 追加 r109 段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 维持 ≤3000 的前提下更新「最近拍」

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）；范围替换另给显式 mark。
★ 「mark 歧义」硬断言：mark 与 old **同时**存在 ⇒ 只可能是 mark 不唯一 ⇒ `sys.exit`；
  豁免位判据 = `old in new`（「把锚点原样保留在 new 里」的写入本来就要求锚点留下当下层契约）。
★ 用法： python ev/doc109l1.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python ev/doc109l1.py --check    # 只校验锚点命中数 + 工作区字符预算（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的文件各自保留原行尾（rd/wr 处理）。
⚠ 正文里有 `100%` / `90%` 这类百分号 ⇒ **不用 `%` 格式化**，改用 `@WHEN@` 占位符替换。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-02 09:4x'

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
            BAD.append(u'%s：文件不存在（new=%r 待建）' % (label, steps[0][1][:60]))
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
    print(u'   %-48s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


# ============================================================ 公共文案

R109_TOP = u"""> 🚧 **最新一拍 = r109 第一拍（四条 · ★ 新一代 —— r108 已交付 `172e580` ⇒ 按硬规则新建 `mg-work/r109/`）** —— **🚫 未提交**（判据 `git status` 仍是 ` M pages/conversation.html`）：
> 本拍 = **右栏批注链路四件重做**（删灰带 / 标注条贴顶 / 批注钮转红 / `td-elnote` 按邵先生三稿逐像素重做），**未动任何其他模块**（`task-detail.html` / `base.html` 一字未动）。
> ① **删 `td-page-blank` → 已做**：DOM + `panel.css` 规则**双清零**（真机 `pageBlankCount: 0`）。
> ② **`td-annot-bar` 贴顶 → 已做**：★★ 只改 `bottom: 0 → top: 0` **不够** —— `position: sticky` 的 `top` 只在元素位于「滚动容器里首个可滚动子件」**之前**才追得上，
>   而它原是 `.td-view` 的**末位子件** ⇒ **DOM 侧同步把它挪成 `.td-view` 的首个子件**（`_mods.html`）才生效。
>   真机：`barIsFirstChild:true` / `position:"sticky"` / `top:"0px"` / `bottom:"auto"` / **`dTop:0`**（与 `.td-view` 顶沿齐平）/ `barCount:1`。
> ③ **`td-url-annot` 批注态转红 + 改文案 → 已做**：按「浅底红 + 红字」= `--color-danger-light-1`（red-1 **`#FFECE8`**）+ `--color-danger-6`（red-6 **`#F53F3F`**）；
>   文案由 `setAnnot(on)` 切 `标注 ⇄ 退出批注`（⚠ **只认 `.td-url-annot`** —— 标注条那枚「完成」也带 `data-td-annot`，不动它）。
>   真机：`uaLabelBefore:"标注" → uaLabelAfter:"退出批注"`；`uaBg rgba(0,0,0,0) → rgb(255,236,232)`、`uaColor rgb(245,63,63)`。
> ④ **`td-elnote` 按三稿逐像素重做 → 已做**（`file=193158744355579` / `page_id=1119:15374`，导出 PNG 均 **scale=2**，卡描边外沿在 PNG **(72, 28)**）：
>   稿1 `1409:18319` 初始态 356×48（pin 24×24 + 12 缝 + 卡 320×48）· 稿2 `1204:18467` 输入态 356×108（卡 = 输入区 296×44 + 12 + 底行 296×28）·
>   稿3 `1409:18332` 已批注锚点 24×24（与 pin 同形、实心主色 + 白数字 12/16/500）。
>   ★ **内距 12 = 1px 描边 + 11px padding**（稿2 的 `left:12 width:296` 从**描边外沿**起算 —— 只有 padding 11 对得上）；
>   ★ **卡高公式**（邵先生「按行数算，1 行=86」）= `12 + 22n + 12 + 28 + 12` ⇒ 空态 48 / 1 行 86 / 2 行 108；封顶 `calc(200px * var(--ui-fs-ratio))`、**由输入区自滚**（底行常驻）。
>   ★ **逐像素对照**（`ev/pix109.py`）：稿1 卡框 `(0,0,320,48)` **差 0**；稿2 卡框 `(0,0,320,12)` **差 0**、取消钮 / 添加钮 **差 0**；
>   两处「超 1px」都在**字形右沿的抗锯齿**（非布局差）。★ 唯一已知偏差：稿1 的「添加」右内距 **10px** vs 稿2 的 **12px** ⇒ 统一取 **12**（待邵先生定夺）。
>   ★ **Ctrl**（邵先生「按钮 + 提示都变」+「字不变，只高亮后半句」）：按钮 `添加 ⇄ 发送`（宽仍 48）、提示只亮后半句（`emColor rgb(169,169,169) → rgb(55,112,247)`、`hintColor` 不动）。
>   ★ **锚点** 落在被标注元素**右上角**（`anchorVsTarget {dRight:12, dTop:-12}`；稿子未给落点 ⇒ 取通行读法，待定夺）；提交后**留在批注模式**（不再 `setAnnot(false)`）。
>   ★★ **真机踩到并修掉的功能 bug**：`noteEdit()` 原「先 `noteGrow()` 再摘 `[hidden]`」⇒ 隐藏态 `scrollHeight === 0` ⇒ 回填文本被压成 0 高（卡停在 48 而非 108）⇒ **改成「先摘 `[hidden]` 再量」**，并加静态判据 `i_unhide < i_grow` 防回归。
>   ★ **字号杠杆**（`--ui-fs=18`）：`capped.card 313.16×257.14` = `calc(200px * 18/14)`（封顶**按比例**、不是写死 200）；`taScrollH 509 > taClientH 185` ⇒ `taCanScroll:true`、`cardOverflow "hidden"`、`footVisible 36`、**`docOverflowX 0`**。
> ★ **补丁 = `ev/patch109l1.py`**（**6 条编辑** + 跨层自检 + `--check`；`应用 0 / 跳过 6` 幂等）。
> ★★ **本拍八条坑**见 PLAYBOOK **P3.56**（★★★ **归零判据被自己的解释性注释绊倒** ⇒ 先剥三类注释 / **裸前缀**命中（`.td-elnote-f` 被 `.td-elnote-foot` 命中 ⇒ 词边界 `(?![-\\w])`）/ 命中**遗留死选择器**（顺手摘掉）/ 裸词「添加评论」被三处右键菜单项命中 ⇒ 查带上下文整串 / **跨代标记判据照实际清单抄** / **CSS 注释里写 hex 会被 `verify-design` 打成 TOKEN-GAP** / **`convert('RGB')` 把设计稿透明像素变纯黑** ⇒ 判据先限定卡片内区 / **设计稿 PNG 的卡片外沿是 (72,28) 而非行偏移**、元素截图是 **1×**）。
> **门禁**：`check-syntax` **10/10**；`verify-design` md5 `3dbf654337559509110899e48bef1b1c`（**与 r107 基线逐字节同 ⇒ 零新增、一处渐变都没引**）；`scan-flatten part109/panel.css` 仍 **2 条**；`patch109l1` / `apply109` 均「0 应用」幂等。
> **产物**：`conversation.html` 1024825 → **1036907 字符（+12082）**（**8733 行**；LF bytes **1154553** / 工作区 **1163285**；`git diff --numstat` **`300 55`**）；
> `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**（8 个外壳页零改动，nav 块沿用 `r106-nav-js`）。
> 逐条实测见 `mg-work/r109/acceptance.md`（**九节**）；机制级教训见 PLAYBOOK **P3.56**；本页固定事实见 PAGES **P3.11i**。
> 🚫 未 commit / 未 push。
"""

R109_SECTION = u"""## 二·i ★★ r109 第一拍（会话详情页右栏「批注链路四件重做」· 2026-10-02 08:5x 邵先生 · **共一拍**）—— **🚫 未提交**

> 完整版见 `mg-work/r109/acceptance.md`（**九节**）；机制级教训见 PLAYBOOK **P3.56**；本页固定事实见 PAGES **P3.11i**。

**① 体位**：r108 **已交付 `172e580`** ⇒ **新建 `mg-work/r109/apply109.py`**（**不就地返工**），
由 **`ev/make109.py`** 从 `apply108.py` 做精确替换生成。`GENS` 扩成**七代**（r93 / r101 / r102 / r106 / r107 / r108 / **r109**）。
**★★★ nav 块继续沿用 `r106-nav-js`**（`NAV_TAG='r106'`）⇒ `base.html` 与 8 个外壳页**逐字节不变**，`git status` 只有 `conversation.html` 一个 ` M`。
**`PART_DIRS` 四级回落**：`part109 → r108/part108 → r107/part107 → r102/part105`（本代只覆盖改过的三件：`_mods.html` / `panel.css` / `panel.js`）。

**② 改动清单**

| 文件 | 改动 |
|---|---|
| `part109/_head.html`（4792 字符） | **一字未动**（+0） |
| `part109/_mods.html`（71067 → 71501，+434） | ① 删 `<div class="td-page-blank">&nbsp;</div>`（留说明注释）；② `.td-annot-bar` 整块从 `.td-view` **末尾挪到首位**（在 `<div class="td-page">` 之前） |
| `part109/panel.css`（76769 → 83427，+6658） | ① 删 `.td-page-blank` 规则（不留死规则）；② `.td-annot-bar` `bottom:0 → top:0`；③ `.td-url-annot[aria-pressed='true']` 主色 → `--color-danger-light-1` / `--color-danger-6`；④ 旧「元素评论气泡」整块（9 条选择器）换成新一套（`.td-elnote-pin` / `.is-done` / `.td-anchor` / `-card` / `.has-text` / `-input` / `::placeholder` / `-foot` / `-hint` / `-acts` / `.td-elnote-ok[disabled]`）；④b 摘掉第 14 节选择器组里**遗留的死选择器** `.td-elnote-t` |
| `part109/panel.js`（72191 → 77185，+4994） | ③ `setAnnot()` 里只对 `.td-url-annot` 切文案；④ `elnote.innerHTML` 换 `pin + card` 两兄弟、新增 `noteList / noteCur / noteCtrlOn` + `noteFind / noteGrow / noteCtrl / noteEdit / noteDrop / noteCommit` + 事件（`document` 上的 Ctrl 键、`window.blur` 兜底、气泡内 `stopPropagation`） |
| `ev/make109.py` · `ev/splice109.py` · `ev/patch109l1.py` | 生成器 / 组装器（**四条守卫**：剥注释后归零 + 标注条在位 + `i_view < i_bar < i_page` + 「标注」未动）/ 补丁（6 条编辑 + 跨层自检 + `--check`） |

**③ 真机实测**（`ev/p109{a,b,c,d,e,z}.js` + `probe109{a,b,e,z}.sh`）

* ① `pageBlankCount: 0`；② `barIsFirstChild:true` / `bar.dTop:0` / `bar.top:"0px"` / `bottom:"auto"`；③ `uaLabel 标注→退出批注`、`uaBg rgb(255,236,232)` / `uaColor rgb(245,63,63)` / `uaBorder rgba(0,0,0,0)`。
* ④ 稿1：`note 356×48`、`card.box [840,430,320,48]`、`pin [804,442,24,24]`（`br "12px 12px 12px 0px"` / `bw 2px` / 白底 + 主色描边）、`ta.ph "输入你的注释"`、`ok {disabled:true, bg rgb(218,228,254), 48×28}`、`cancelDisplay "none"` / `hintDisplay "none"`。
* ④ 稿2：`card 320×108`、`ta 296×44 @dx12 dy12`（`lh 22px` / `inlineH "44px"`）、`foot 296×28 @dy68`、`cancel [204,…]` / `ok [260,…]`、`gapBtns 8`、**`rightInset 12`**、`hintMidY 14`。
* ④ Ctrl：`okTxt 添加→发送`、`emColor 169,169,169 → 55,112,247`、`hintColor` 不变、`okBox` 宽仍 48。
* ④ 稿3：`anchor 24×24`、`bg/color rgb(55,112,247)/rgb(255,255,255)`、`fs 12 / fw 500 / lh 16`、`br "12px 12px 12px 0px"`；`anchorVsTarget {dRight:12, dTop:-12}`；重开 `isDone:true / num "1" / dotContent "none" / cardH 108 / taInlineH "44px"`。
* ④ 字号杠杆（`--ui-fs=18`）：`capped.card 313.16×257.14` = `calc(200px * 18/14)`；`taScrollH 509 > taClientH 185` ⇒ `taCanScroll:true`；`cardOverflow "hidden"` / `footVisible 36` / **`docOverflowX 0`**。

**④ 产物与门禁**：`conversation.html` 1024825 → **1036907 字符（+12082）**；**8733 行**；LF bytes **1154553** / 工作区 bytes **1163285**；`git diff --numstat` **`300 55`**；
`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；注入块 id `r109-conv-css` / `r109-conv-js`（**`r108-*` 及以前全 0**；`base.html` 仍是 `r106-nav-js` 1 处）。
幂等（`patch109l1` 0 应用 / 6 跳过、md5 原地不变；`apply109` 「已是目标态」）｜`check-syntax` **10/10**｜
`verify-design` md5 `3dbf654337559509110899e48bef1b1c`（与 r107 基线逐字节同）｜`scan-flatten part109/panel.css` **2 条**（`.td-mod-bar` / `.td-url`）。

**⑤ 交接**：🚫 未 commit（等邵先生显式说「commit」）。**两处待邵先生定夺**：
(a) 稿1 的「添加」右内距 **10px** vs 稿2 的 **12px** —— 本层统一取 12，要不要给空态单开一条 −2px 补偿？
(b) 已批注锚点落点取「**右上角**」（稿子未给）—— 换左/右下只需改 `noteDrop()` 的两个 `−12`。
★ 遗留（**有意保留、未动**，与 r108 十九拍同一笔账）：右键菜单 `ctxShow()` 与 `.zd-menu` 的 `placeZdMenu()` 的入场仍是硬切（各 1 行强制重排即可对齐）。

---

"""

P356 = u"""## P3.56 ★★ r109 第一拍（会话详情页右栏「批注链路四件重做」· 2026-10-02 08:5x 邵先生）—— ★★ 八条新教训

**需求四条**：① 删 `td-page-blank` ② `td-annot-bar` 贴顶（「不要显示在下面，不容易被注意到」）③ `td-url-annot` 批注态转红 + 改文案「退出批注」 ④ `td-elnote` 按邵先生三张 MasterGo 稿**逐像素**重做。
**澄清五条**（逐字）：稿2 顶部那段话 = **「就是输入框的内容示例」** · 高度 **「输入的文字多了后才自动向下撑开，最高撑高到200px，溢出就内滚」** · Ctrl **「按钮 + 提示都变」** · 红 = **「浅底红 + 红字」** · 提示 **「字不变，只高亮后半句」** · 卡高 **「按行数算，1 行=86」**。

**① ★★★ `position: sticky` 的 `top` 只在元素位于「滚动容器里首个可滚动子件」之前才追得上**

改 `bottom: 0 → top: 0` **不够**：元素原本是 `.td-view` 的**末位子件**，它的静态位置本就在视口之下 ⇒ `top` 永远追不上。
**必须连 DOM 一起挪**（挪成 `.td-view` 的首个子件）。判据 = `barIsFirstChild && (bar.top − view.top === 0)`。
> 同族误判：**「改一条 CSS 就能改行为」** —— 先把「这个属性在什么 DOM 位置上才成立」问清楚，再动手。

**② ★★★ 「归零 / 不存在」判据必须先剥 HTML 注释**

`splice109.py` 里「产物里不得再出现 `class="td-page-blank"`」**当场假报失败** —— 绊倒它的是我自己那段说明注释
（注释正文逐字写了「这里原有 `<div class="td-page-blank">&nbsp;</div>`」）。
★ **归零判据必须剥三类注释**：HTML `<!-- -->`、CSS `/* */`、JS `^\\s*//`。
★ 这是「**判据不能写裸词**」的**第三种形态**：判据被自己的**解释性注释**命中 —— 注释里引用被删元素的名字是最自然的写法，也最容易把守卫绊倒。

**③ ★★ 判据不能写「裸前缀」**

`.td-elnote-f`（旧类）被新类名 **`.td-elnote-foot`** 的**前缀**命中 ⇒ 改用词边界 `\\.td-elnote-f(?![\\-\\w])`。
★ 同批还发现 `.td-elnote-t` 命中的是第 14 节选择器组里**遗留的死选择器** ⇒ **顺手把死选择器摘掉**（死选择器既是假报源、也是真技术债）。

**④ ★★ 裸词会被「三处无关文案」命中**

查旧结构残留时用「添加评论」是**裸词** —— JS 里本来就有三处无关的右键菜单项（「在此行添加评论」「已在该行添加评论」）。
⇒ 只查**带上下文的一整串**（`'<div class="td-elnote-t">评论元素'` / `'添加评论</button>'`）。

**⑤ ★ 跨代标记判据要照「实际清单」抄，别凭记忆**

原写 `/* r106-l1 */` / `/* r93-l1 */`（实际 r93 只在 `_mods.html` 的注释里）、JS 侧写 `r108-l6 ①`。
正解 = 先枚举出实际清单（本代：CSS `r107-l1/l2 + r108-l1…l7 + r109-l1`；JS `r107-l2 / r108-l6 / r108-l7 / r108-l8`）再逐条查。

**⑥ ★★★ CSS 注释也是 CSS 文本 —— 门禁会扫**

我在注释里逐字写 `#9ca3af` 解释「为什么不用它」，被 `verify-design.py` 打成 **TOKEN-GAP**（硬编码色值）。
⇒ 解释「为什么不用某色」时**不要写出那个 hex**，改写成人能读的指代（「尾风那档 gray-400」）。

**⑦ ★★ `convert('RGB')` 会把设计稿 PNG 的透明像素变纯黑**

`pix109.py` 第一版按颜色筛没限定区域 ⇒ 画布边缘的 `(0,0,0)` 全被吃进来，「占位墨迹」假报成 `(0,-14,338,70)`。
⇒ 一切按颜色筛的判据**先限定在卡片内区**。★ 同族（**P3.18 ②**）已记过一次，这是**第二次踩** —— 设计稿 PNG 是「透明底 + 投影」，这是它的固有属性。
★ 另一处：`Frame.find(t, tol, …)` 与 `findp(pred, …)` **签名不同**，混用会得到 `TypeError: 'function' object is not subscriptable`（`c[0]` 里 `c` 成了 lambda）。

**⑧ ★★ 设计稿 PNG 的定标要老老实实量；元素截图是 1×**

卡片**描边外沿**在 PNG 的 **(72, 28)** —— 上一轮把 (72,28) 里的 28 误记成「行偏移」⇒ 逻辑 `y = (imgY − 28)/2`。
元素截图 `screenshot "<sel>" "<path>"` 出的是 **1×**（356×48 就出 356×48），要 2× 得走 CDP。
★ 三组的**结构性判决全落在「外框」上**：稿1 卡框 `(0,0,320,48)`、稿2 卡框 `(0,0,320,12)`、稿2 两枚按钮 —— **逐项差 0**；
「超 1px」的两项都在**字形右沿的抗锯齿**（判据要承认这个噪声下限，别去修它）。

**★ 判据速查（本轮实测值）**：`pageBlankCount 0` · `barIsFirstChild true` / `bar.top "0px"` / `dTop 0` · `uaLabel 标注→退出批注` / `uaBg rgb(255,236,232)` / `uaColor rgb(245,63,63)`；
`card 320×48`（空态）/ `320×108`（输入态）/ `313.16×257.14`（fs18 压顶 = `calc(200px×18/14)`）；`ta 296×44 @dx12 dy12` / `foot 296×28 @dy68` / `gapBtns 8` / `rightInset 12` / `hintMidY 14`；
`ok {disabled:true, bg rgb(218,228,254)}`（稿1）/ `rgb(55,112,247)`（稿2）；Ctrl ⇒ `okTxt 发送` / `emColor rgb(55,112,247)` / `hintColor` 不变 / `okBox` 宽仍 48；
锚点 `24×24` / `br "12px 12px 12px 0px"` / `fs 12 / fw 500 / lh 16`、`anchorVsTarget {dRight:12, dTop:-12}`；重开 `cardH 108` / `taInlineH "44px"`；`docOverflowX 0`。

"""

LOG109 = u"""
## r109 第一拍 —— 会话详情页右栏「批注链路四件重做」（@WHEN@ · 🚫 未提交）

**需求四条 + 澄清五条**：见 PLAYBOOK **P3.56** 开头（逐字保留，别再转述）。

**产物**：`conversation.html` 1024825 → **1036907 字符（+12082）**、**8733 行**、LF bytes **1154553** / 工作区 **1163285**、`git diff --numstat` **`300 55`**；
`task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；注入块 id `r109-conv-css` / `r109-conv-js`（r108 及以前全 0）。

**改序**（硬规则「双层产物只能下→上改」）：`part109/{_head,_mods}.html` / `panel.css` / `panel.js`
→ `ev/splice109.py`（重建 `part109/browse.html` = 106685 字符）→ `mg-work/r109/apply109.py`。

**本轮排掉的坑（八条）**：见 PLAYBOOK **P3.56**。★ 最值钱的两条 =
① ★★★ **`position: sticky` 的 `top` 只在元素位于「滚动容器里首个可滚动子件」之前才追得上** —— 所以「标注条贴顶」必须**CSS + DOM 两处同改**；
② ★★★ **「归零」判据必须先剥三类注释** —— 它当场被我自己那段说明注释绊倒（这是「判据不能写裸词」的第三种形态）。

**收尾两跑**：`check-syntax.py pages/*.html` **10/10**；`verify-design.py ./pages` md5 **3dbf654337559509110899e48bef1b1c**（与 r107 基线逐字节同）；
`scan-flatten.py part109/panel.css` 仍 **2 条**。⚠ 两者都污染工作区 ⇒ `git checkout -- pages/gaps.log`（`git status` 只剩 ` M pages/conversation.html`）。

**待邵先生定夺两条**：(a) 稿1「添加」右内距 10px vs 稿2 12px（本层取了 12）；(b) 已批注锚点落点取「右上角」（稿子未给）。

🚫 未 commit / 未 push。
"""

WSM_STEPS_OLD = u"""- **r107 十一拍**「侧栏模块标签化」＝ **已推送 `e9c9498`**。
- **r108 十二 ~ 十九拍**（✅ 已交付 `172e580` · 就地返工，逐拍见 `HANDOFF.md` §二·h；**已交付 ⇒ 再改右栏须新建 r109**）：**十九 = 划词浮条放行根 `'.r93-scroll'` → `'.r93-scroll, .td-browse'`**（右栏划词终于弹条）· **`toggleMenu` 开态拆四步（`void menu.offsetWidth` 强制重排）**（原同 tick「摘 `[hidden]` + 挂类」⇒ 0.2s spring **从未跑过**）。
- 补丁链 `ev/patch108{l1~l8}.py`；产物 `conversation.html` **1024825 字符**（`1234 / 242` 行）、`task-detail.html` 未动、`base.html` 不变；`acceptance.md` **四十四节**。"""

WSM_STEPS_NEW = u"""- **r107**＝`e9c9498`；**r108 十二 ~ 十九拍**＝✅ `172e580`（**已封板 ⇒ 再改右栏须新建 r109**）。
- **r109 第一拍**（🚫 未提交 · 右栏「批注链路」四件）：删 `td-page-blank` · `td-annot-bar` **挪 `.td-view` 首子件** + `sticky top:0`（末位追不上）· `td-url-annot` 批注态转「浅红底红字」+ 文案「退出批注」· `td-elnote` 按三稿逐像素重做（内距 **12 = 1px 描边 + 11 padding**；高 `12+22n+12+28+12`、封顶 200 内滚；Ctrl ⇒ 按钮「发送」+ 只亮后半句）。补丁 `ev/patch109l1.py`；产物 **1036907 字符**；`acceptance.md` **九节**。
- 新红线：**归零判据先剥三类注释**；**`sticky top` 只在滚动容器首子件之前才追得上**；**隐藏元素量不出几何**。"""


def main():
    print(u'=== 1/6 HANDOFF.md ===')
    patch(HOF, [
        # 首行时间戳
        (u'> 最后更新：2026-10-01 23:1x（**★ r108 八拍已交付并推送',
         u'> 最后更新：@WHEN@（**★ r109 第一拍已落地 —— 🚫 未提交** —— **r108 八拍已交付并推送',
         u'首行时间戳 → r109'),

        # 顶部块：插 r109 + 降级 r108 十九拍
        (u'> ✅ **最新一拍 = r108 第十九拍（两条 · ★★ 就地返工、未另起代数）** —— **十二 ~ 十九拍已整代提交并推送 `172e580`**（判据 `git status` 已无 ` M pages/conversation.html`）：',
         R109_TOP + u'\n> ▸ **上一拍（★ r108 已封板）= r108 第十九拍（两条 · ★★ 就地返工）** —— **十二 ~ 十九拍已整代提交并推送 `172e580`**（判据 `git status` 已无 ` M pages/conversation.html`）：',
         u'顶部：插 r109 块 + 降级 r108'),

        (u'> ▸ **上一拍 = r108 第十八拍（四条 · 就地返工，✅ 已随 `172e580` 交付）**：',
         u'> ▸ **更早一拍 = r108 第十八拍（四条 · 就地返工，✅ 已随 `172e580` 交付）**：',
         u'降级：十八拍 → 更早一拍'),

        (u'> ▸ **再上一拍 = r108 第十七拍（四条 · 就地返工，✅ 已随 `172e580` 交付）**：',
         u'> ▸ **更早二拍 = r108 第十七拍（四条 · 就地返工，✅ 已随 `172e580` 交付）**：',
         u'降级：十七拍 → 更早二拍'),

        (u'> ⚠️ **上一拍 = r108 第十二拍「diff 卡片化 + 文件树抽屉」**（**同为 r108 一脉 · 已随 `172e580` 交付**',
         u'> ⚠️ **r108 起始拍 = r108 第十二拍「diff 卡片化 + 文件树抽屉」**（**已随 `172e580` 交付**',
         u'降级：十二拍 → r108 起始拍'),

        # §一 状态段
        (u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七 + 十八 + 十九拍）＝已交付 `172e580`（已推送 `origin/main`）**（2026-10-01 23:1x，第十九拍）。工作区：\n'
         u'**` M pages/conversation.html`（1024825 字符）+ ` M pages/task-detail.html`（767836 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— **base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
         u'★★ **r109（第一拍 · 四条「批注链路」）＝ 🚫 未提交**（2026-10-02 08:5x 起；等邵先生显式说 commit）。工作区：\n'
         u'**` M pages/conversation.html`（1036907 字符）+ `?? mg-work/r109/`** —— **`task-detail.html`（767836 字符）/ `base.html`（472150 字符）一字未动**（8 个外壳页零改动，nav 块沿用 `r106-nav-js`）。\n'
         u'★★ **r108（第十二 ~ 十九拍）已交付 `172e580`（已推送 `origin/main`）**（2026-10-01 23:1x）—— **已封板**：再改会话详情页 / 右栏 / 任务详情页须**新建 `mg-work/r109/`**；**不要**再回头改 `apply108.py` / `apply107.py`。',
         u'§一 状态段 → r109'),

        (u'⚠ ★★ **本代动了第二页**：第 ⑤ 条（任务详情页徽章字号）走**独立血脉**',
         u'⚠ ★★ **r108 动了第二页**：第 ⑤ 条（任务详情页徽章字号）走**独立血脉**',
         u'§一：本代 → r108'),

        (u'⚠ ★ **本代不要重跑 `apply107.py`**：它的 `GENS` 只有五代，会把「基线里仍残留 `r108-conv-css`」判成错误直接退出。\n'
         u'  退 r108 只需 `git checkout -- pages/conversation.html`（只改了这一页）。',
         u'\n'.join([
             u'⚠ ★ **r108 已封板 ⇒ 不要再跑 `apply108.py`**（会把「基线里残留 `r109-conv-*`」判成错误直接退出）。',
             u'  ★ **r109 是本代**：改序 = `part109/{_head,_mods}.html` / `panel.css` / `panel.js` → `ev/splice109.py` → `mg-work/r109/apply109.py`；',
             u'  回滚只需 `git checkout -- pages/conversation.html`（只改了这一页）。⚠ `browse.html` 是 `splice109.py` 的**产物**、`apply109.py` 由 `ev/make109.py` 生成 ⇒ **两者都禁手改**。',
         ]) + u'\n',
         u'§一：r109 体位 + 回滚'),

        # conversation 表行尾追加 r109 态
        (u'**四十 ~ 四十四 = 第十九拍**） |',
         u'**四十 ~ 四十四 = 第十九拍**）。★ **r109 态（🚫 未提交）**：1024825 → **1036907 字符（第一拍 +12082）**；**8733 行**；LF bytes **1154553** / 工作区 bytes **1163285**；`git diff --numstat` = **`300 55`**；注入块 id `r109-conv-css` / `r109-conv-js`（**`r108-*` 及以前全 0**）；r109 第一拍见 `mg-work/r109/acceptance.md`（**九节**） |',
         u'conversation 表行 → 追加 r109 态'),

        # mg-work 表行：新增 r109（插在 docs/codex-refs 行之前）
        (u'| `docs/codex-refs/` + `docs/codex-sidepanel-research.md` |',
         u'| `mg-work/r109/` | **🚫 未提交（第一拍 · 四条「批注链路」）**：`apply109.py`（**由 `ev/make109.py` 从 apply108 精确替换生成**；GENS 七代、nav 沿用 `r106-nav-js`；3647 行 / 190523 字符）/ `acceptance.md`（**九节**）/ **`part109/`**（**四件**：`_head.html` **4792（+0，一字未动）** · `_mods.html` 71067 → **71501** · `panel.css` 76769 → **83427** · `panel.js` 72191 → **77185**；`browse.html` = **106685**，`ev/splice109.py` 的产物）/ `ev/`（`make109.py` · `splice109.py` · **`patch109l1.py`（6 条编辑 + 跨层自检 + `--check`，39802 B）** · `p109{a,b,c,d,e,z}.js` + `probe109{a,b,e,z}.sh` · `pix109.py` + `pix109.log`（**逐像素对照**） · `vd-l1base.txt` / `vd-l1.txt` / `vd-l1now.txt` · `bak-l1/`（三件改前备份） · `tmp/vd0/`）/ `raw/`（设计稿 `design1-initial.png` 748×168 · `design2-typing.png` 748×288 · `anchor-18332.png` · 四张 MCP SVG / JSON · `_pin_zoom.png` + 真机 `{a-note-empty,a-brw-annotating,a-full-annotating,b-note-typing,b-brw-typing,c-note-ctrl,d-brw-anchored,d-note-reopen,e-note-18px}.png`）|',
         u'mg-work 表行：新增 r109'),

        # 二·h 头 → 已封板
        (u'## 二·h ★★ r108（最新一拍 ·',
         u'## 二·h ★★ r108（**已封板** ·',
         u'二·h 头 → 已封板'),

        # 新增 二·i
        (u'## 三、r88 ~ r92 做了什么（前情提要）',
         R109_SECTION + u'## 三、r88 ~ r92 做了什么（前情提要）',
         u'新增 §二·i r109 节'),

        # §六 追加待拍板两条（插在 `## 七、` 之前）
        (u'## 七、下一轮接手清单（按顺序）',
         u'### r109 新增（2 条，均需邵先生点头）\n\n'
         u'48. ★ **稿1 的「添加」右内距 10px vs 稿2 的 12px** —— 同一枚按钮在手放的两稿里差 2px。本层**统一取 12**（稿2 那侧是自动布局值）。\n'
         u'    若要严格照稿1：给空态单开一条 `.td-elnote-card:not(.has-text) .td-elnote-acts { margin-right: -2px }`（一行）。\n'
         u'49. ★ **已批注锚点（稿3）的落点取「被标注元素右上角」**（`left = right − 12` / `top = top − 12`，让 24×24 的锚点中心咬住那个角）——\n'
         u'    **稿子只给了锚点长相、没给落点** ⇒ 取通行读法（Figma 批注同款）。想换左/右下只需改 `noteDrop()` 的两个 `−12`。\n\n'
         u'---\n\n## 七、下一轮接手清单（按顺序）',
         u'§六：追加 r109 两条待拍板'),

        # §七 清单：加 apply109
        (u'   → **`mg-work/r108/apply108.py`**\n',
         u'   → **`mg-work/r108/apply108.py`**（**已封板，只供追溯**）\n'
         u'   → **`mg-work/r109/apply109.py`**（★ **本代**）\n',
         u'§七：接手链加 apply109'),

        (u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` 八拍（`172e580`）—— 亦已提交并推送**（工作区干净）。',
         u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` 八拍（`172e580`）—— 亦已提交并推送**（工作区干净）；\n'
         u'   **`r109` 第一拍 —— 🚫 未提交**（`git status` = ` M pages/conversation.html` + `?? mg-work/r109/`）。',
         u'§七：现状加 r109'),

        (u'   ★ **r108 已交付 ⇒ 封板**（**十二 ~ 十九拍全在同一代内就地叠加**）：再改**会话详情页 / 右栏**须**新建 `mg-work/r109/`**（照抄 `GENS` 六代、扩成七代）',
         u'   ★ **r108 已交付 ⇒ 封板**；**r109 已开代**（`GENS` **七代**、nav 仍沿用 `r106-nav-js`）：再改**会话详情页 / 右栏**在 **r109 内就地叠加**（`git status` 仍是 ` M`）',
         u'§七：r109 体位'),

        # §八 回滚：新增 r109 段
        (u'# ★ r108 回滚（本代 · 只改了一页 ⇒ 一行即退（推荐））',
         u'# ★ r109 回滚（本代 · 只改了一页 ⇒ 一行即退（推荐））\n'
         u'git checkout -- pages/conversation.html\n'
         u'# 还原 part 侧：git checkout -- mg-work/r109/part109/（或重跑 ev/patch109l1.py 前的 ev/bak-l1/）\n\n'
         u'# ★ r108 回滚（上一代 · 只改了一页 ⇒ 一行即退）',
         u'§八：新增 r109 回滚'),

        # 顺手把 §七 里几处「r108 口径」改成 r109（否则会误导下一轮）
        (u'     所以**只需跑 `apply108` 一条即可自愈到 r108 态**（历代块会被整块剥离再重注）。',
         u'     所以**只需跑最新一代那一条即可自愈到当前态**（现 = `apply109`；历代块会被整块剥离再重注）。',
         u'§七：自愈入口 → apply109'),

        (u'     反过来**绝不要**跑到 r108 之后再跑 `apply107`（它只认五代 ⇒ 「基线残留 r108-conv-css」自检会直接退出）。',
         u'     反过来**绝不要**跑到 r109 之后再跑 `apply108` / `apply107`（前者只认六代、后者只认五代 ⇒ 「基线残留 `r109-conv-*`」自检会直接退出）。',
         u'§七：退回入口 → apply108/107'),

        (u'   本代 `part108/` 只覆盖改过的三件，其余从 `part107` / `part105` **三级回落**。',
         u'   本代 `part109/` 只覆盖改过的三件（`_mods.html` / `panel.css` / `panel.js`），其余从 `part108` / `part107` / `part105` **四级回落**。',
         u'§七：part 回落 → 四级'),

        (u'   （改序 = `part108/_mods.html` → `ev/splice108.py` → `apply108.py`；⚠ `apply108.py` 由 `ev/make108.py` 生成、**禁手改**）。',
         u'   （改序 = `part109/{_head,_mods}.html` / `panel.css` / `panel.js` → `ev/splice109.py` → `apply109.py`；⚠ `apply109.py` 由 `ev/make109.py` 生成、**禁手改**）。',
         u'§七：改序 → r109'),

        (u'**不要**把它塞进 `apply108.py`。',
         u'**不要**把它塞进 `apply109.py`。',
         u'§七：task-detail 血脉 → apply109 口径'),

        (u'   ⚠ 若 r108 已交付后再改，则新建 `mg-work/r109/`（照抄六代 `GENS`、扩成七代；nav 脚本仍未改则可继续沿用 `NAV_TAG=\'r106\'`）。',
         u'   ★ **r109 就是这一代**（2026-10-02 已开）：`GENS` **七代**、nav 仍沿用 `NAV_TAG=\'r106\'`（nav 脚本仍未改）。',
         u'§七：r109 已开代'),
    ], u'HANDOFF')

    print(u'=== 2/6 PAGES.md ===')
    patch(PAG, [
        (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 ~ 十九拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十九拍**）',
         u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 ~ 十九拍** + **r109 第一拍「批注链路四件重做」** · 复刻 Codex 右栏 · 2026-10-01 / 10-02 · **共二十拍**）',
         u'P3.11i 标题 → 二十拍'),

        (u'**⚠ 改这一块之前必看**',
         u'\n'.join([
             u'| **`td-page-blank` 已删净** | ★ **r109 ①**：DOM（`_mods.html`）与 `panel.css` 规则**双清零** —— 不留死规则。⚠ 「归零」判据必须先剥三类注释（HTML / CSS / JS），否则会被说明注释绊倒（真踩）。 |',
             u'| **`td-annot-bar` 贴顶** | ★★ **r109 ②**：`position: sticky; top: 0`（原 `bottom: 0`）**＋ DOM 侧把它挪成 `.td-view` 的「首个子件」**（原来在末位 ⇒ `top` 永远追不上）。判据 = `barIsFirstChild && (bar.top − view.top === 0)`。 |',
             u'| **`td-url-annot` 批注态** | ★ **r109 ③**：`.td-url-annot[aria-pressed=\'true\'] { background: var(--color-danger-light-1); color: var(--color-danger-6) }`（「浅底红 + 红字」= red-1 `#FFECE8` / red-6 `#F53F3F`）；文案 `标注 ⇄ 退出批注` 由 `setAnnot(on)` 切，⚠ **只认 `.td-url-annot`**（标注条那枚「完成」也带 `data-td-annot`）。 |',
             u'| **`td-elnote` 三稿（pin / 卡 / 锚点）** | ★★★ **r109 ④（邵先生自己的设计，逐像素）**：pin 24×24 `border: 2px --color-primary-6` + `border-radius: 12px 12px 12px 0`（**左下角纯直角**）+ 中心 6px 圆点；`.is-done` / `.td-anchor` = 同形实心主色 + 白数字 12/16/500；卡 320 宽 / 1px `--color-border-2` / 8 圆角 / `--shadow2-down`、**内距 12 = 1px 描边 + 11px padding**；**卡高 `12 + 22n + 12 + 28 + 12`**（空 48 / 1 行 86 / 2 行 108）、封顶 `calc(200px * var(--ui-fs-ratio))`、**由输入区自滚**（`overflow-y:auto`，底行常驻）；空态无提示无取消（`:not(.has-text)` 关掉）；Ctrl ⇒ 按钮 `添加 ⇄ 发送`（宽不变）+ **只亮后半句**（`.is-ctrl .td-elnote-hint em`）；禁用的「添加」走 `--btn-bg: var(--color-primary-2)`（**不是** DS 的 `opacity:.4`）。⚠ 两枚按钮三处纠 DS 默认值（内距 11 / 字号 12 / `:not(:focus-visible)` 去 ring）。 |',
             u'| **`.td-elnote` 的 JS 时序（★ 硬约束）** | ★★★ **r109**：`noteEdit()` 必须 **先 `removeAttribute(\'hidden\')` 再 `noteGrow()`** —— 隐藏态 `ta.scrollHeight === 0` ⇒ 回填的长文本被压成 0 高（卡停在 48 而非 108）。判据 = 静态查 `i_unhide < i_grow`。**同一族的教训**：`display:none` 下量不出任何几何。 |',
             u'**⚠ 改这一块之前必看**',
         ]) + u'\n',
         u'P3.11i 固定事实表：新增 r109 四行'),

        (u'## P4 标准配方（r66 / r67 定稿）',
         u'\n'.join([
             u'23. ★★★ **「归零 / 不存在」判据必须先剥三类注释**（HTML `<!-- -->` / CSS `/* */` / JS `^\\s*//`）——',
             u'    注释里引用被删元素的名字是最自然的写法，也最容易把守卫绊倒（r109：`splice109.py` 的 `class="td-page-blank"` 检查被自己那段说明注释命中）。',
             u'24. ★★ **判据不能写「裸前缀」** —— `.td-elnote-f` 被新类名 `.td-elnote-foot` 命中 ⇒ 加词边界 `\\.td-elnote-f(?![\\-\\w])`；',
             u'    命中「遗留死选择器」时顺手把它摘掉（死选择器既是假报源、也是真技术债）。',
             u'25. ★★★ **`position: sticky` 的 `top` 只在元素位于「滚动容器里首个可滚动子件」之前才追得上** ——',
             u'    「把底部条挪到顶部」= **CSS `bottom→top` + DOM 挪首** 两处同改（只看 CSS 会以为改了一条属性。判据 = `bar.top − view.top === 0`）。',
             u'26. ★★ **改「`--ui-fs` 杠杆下要跟着变的尺寸」时**：`max-height: calc(200px * var(--ui-fs-ratio))` 会**按比例**放大（fs18 ⇒ 257.14）——',
             u'    这是 DS 既定体位、**不是**写死 200；内容溢出时让**内层输入区** `overflow-y:auto` 自滚，别让卡片滚（否则底行被顶走）。',
             u'',
             u'---',
             u'',
             u'## P4 标准配方（r66 / r67 定稿）',
         ]) + u'\n',
         u'必看清单：追加 23~26 四条'),
    ], u'PAGES')

    print(u'=== 3/6 PLAYBOOK.md ===')
    patch(PBK, [
        (u'## 附：工作区速览 92 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         P356 + u'## 附：工作区速览 98 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         u'附录前插 P3.56 + 标题 → 98 条'),

        (u'**第十八拍加到 86 条**、**第十九拍加到 92 条**，工作区实测 **2951 字符**），',
         u'**第十八拍加到 86 条**、**第十九拍加到 92 条**、**r109 第一拍加到 98 条**，工作区实测 **2944 字符**），',
         u'附录引言 → 98 条'),
    ], u'PLAYBOOK')

    patch(PBK, [(None, u"""
93. ★★★ **「归零 / 不存在」判据必须先剥三类注释**（HTML `<!-- -->` / CSS `/* */` / JS `^\\s*//`）—— 注释里引用被删元素的名字是最自然的写法，也最容易把守卫绊倒（r109 `splice109.py` 真踩）。
94. ★★ **判据不能写「裸前缀」** —— `.td-elnote-f` 被新类名 `.td-elnote-foot` 命中 ⇒ 加词边界 `\\.td-elnote-f(?![\\-\\w])`；命中「遗留死选择器」时顺手摘掉它。
95. ★★ **CSS 注释也是 CSS 文本，门禁会扫** —— 在注释里逐字写出 `#9ca3af` 解释「为什么不用它」，会被 `verify-design.py` 打成 TOKEN-GAP ⇒ 改写成人能读的指代（「尾风那档 gray-400」）。
96. ★★ **`convert('RGB')` 会把设计稿 PNG 的透明像素变纯黑** ⇒ 一切按颜色筛的判据**先限定在卡片内区**（第二次踩，见 P3.18②）。
97. ★★ **设计稿 PNG 定标要老实量** —— 卡片**描边外沿**在 (72, 28)、`scale=2`（别把 28 当成「行偏移」）；元素截图 `screenshot "<sel>"` 出的是 **1×**。
98. ★★★ **隐藏元素量不出几何** —— `display:none` 下 `scrollHeight === 0` ⇒ `noteEdit()` 先 `noteGrow()` 再摘 `[hidden]` 会把回填长文本压成 **0 高**（卡 48 而非 108）；修法 = **先摘 `[hidden]` 再量**，判据 = `i_unhide < i_grow`。
""", u'附录追加 93~98 六条')], u'PLAYBOOK')

    print(u'=== 4/6 MEMORY.md（仓库） ===')
    patch(MEM, [(u'> ✅ **已 commit `172e580` 并 push `origin/main`**（2026-10-01 23:1x）；工作区干净。',
                 u'> ✅ **已 commit `172e580` 并 push `origin/main`**（2026-10-01 23:1x）；工作区干净。\n'
                 u'> ★★ **r108 已封板** —— 再改会话详情页 / 右栏 / 任务详情页须**新建 `mg-work/r109/`**（不要回头改 `apply108.py` / `apply107.py`）。',
                 u'r108 段末 → 已封板')], u'MEMORY')

    patch(MEM, [(None, u"""
### 第一拍（r109 第一层补丁 · 四条 · 2026-10-02 08:5x · **🚫 未提交**）

> ★ 体位：r108 **已交付 `172e580`** ⇒ 本拍是**新一代 r109**（`GENS` **七代**、nav 仍沿用 `r106-nav-js` ⇒ 仍只改 `conversation.html` 一页）。
> 四条 = 右栏「**批注链路**」：① 删 `td-page-blank` ② `td-annot-bar` 贴顶 ③ `td-url-annot` 批注态转红 + 文案「退出批注」 ④ `td-elnote` 按邵先生三稿**逐像素**重做。
> **① 删 `td-page-blank`** —— DOM + `panel.css` 规则**双清零**（不留死规则）；真机 `pageBlankCount 0`。
> **② `td-annot-bar` 贴顶** —— ★★ **只改 `bottom:0 → top:0` 不够**：`position:sticky` 的 `top` 只在元素位于「滚动容器里首个可滚动子件」**之前**才追得上，而它原是 `.td-view` 的**末位子件** ⇒ **DOM 同步挪成首个子件**才生效；真机 `barIsFirstChild:true` / `bar.top:"0px"` / **`dTop:0`**。
> **③ 批注钮转红** —— 「浅底红 + 红字」= `--color-danger-light-1`（red-1 `#FFECE8`）+ `--color-danger-6`（red-6 `#F53F3F`）；文案由 `setAnnot(on)` 切 `标注 ⇄ 退出批注`（⚠ 只认 `.td-url-annot`）；真机 `uaBg rgb(255,236,232)` / `uaColor rgb(245,63,63)`。
> **④ `td-elnote` 三稿** —— 稿1 `1409:18319` 356×48 / 稿2 `1204:18467` 356×108 / 稿3 `1409:18332` 24×24（PNG 均 **scale=2**、卡描边外沿在 PNG **(72,28)**）。
>   ★ **内距 12 = 1px 描边 + 11px padding**；**卡高 `12 + 22n + 12 + 28 + 12`**（空 48 / 1 行 86 / 2 行 108）、封顶 `calc(200px * --ui-fs-ratio)`、**由输入区自滚**；
>   ★ Ctrl ⇒ 按钮 `添加 ⇄ 发送`（宽仍 48）+ **只亮后半句**（`emColor 169,169,169 → 55,112,247`、`hintColor` 不动）；锚点落**右上角**（`dRight 12 / dTop −12`）、提交后**留在批注模式**；
>   ★ **逐像素对照**：稿1 卡框 / 稿2 卡框 / 稿2 两枚按钮 **逐项差 0**；两处超 1px 均在**字形右沿抗锯齿**。★ 已知偏差：稿1「添加」右内距 10px vs 稿2 12px ⇒ 统一取 12（待定夺）。
>   ★★ **真机踩到并修掉的功能 bug**：`noteEdit()` 原「先 `noteGrow()` 再摘 `[hidden]`」⇒ 隐藏态 `scrollHeight === 0` ⇒ 回填文本被压成 0 高（卡 48 而非 108）⇒ 改成「**先摘 `[hidden]` 再量**」+ 静态判据 `i_unhide < i_grow`。
> **八条坑** = **P3.56**（① ★★★ **`sticky top` 只在滚动容器首子件之前才追得上** ② ★★★ **归零判据必须先剥三类注释**（被自己的说明注释绊倒）
> ③ ★★ **裸前缀**（`.td-elnote-f` 被 `.td-elnote-foot` 命中 ⇒ 词边界）④ 裸词「添加评论」被三处右键菜单项命中 ⇒ 查带上下文整串 ⑤ 跨代标记判据照**实际清单**抄
> ⑥ ★★★ **CSS 注释里写 hex 会被门禁打成 TOKEN-GAP** ⑦ ★★ **`convert('RGB')` 把设计稿透明像素变纯黑** ⇒ 先限定卡片内区 ⑧ 设计稿定标 (72,28)、元素截图 **1×**）。
> **产物**：`conversation.html` 1024825 → **1036907 字符（+12082）**（**8733 行**；LF bytes 1154553 / 工作区 1163285；`git diff --numstat` **`300 55`**）、
> `task-detail.html` **767836（未动）**、`base.html` **逐字节不变**；`acceptance.md` **九节**。
> 门禁：`check-syntax` **10/10**｜`verify-design` md5 `3dbf654337559509110899e48bef1b1c`（与 r107 基线同）｜`scan-flatten part109/panel.css` **2 条**｜`patch109l1` / `apply109` 幂等。
> 🚫 未 commit / 未 push。
""", u'追加 r109 第一拍段')], u'MEMORY')

    print(u'=== 5/6 当日日志 2026-10-02.md（仓库 + 工作区） ===')
    log_head = u'# 2026-10-02 工作日志 · GienCoder 设计工程（会话详情页右栏）\n'
    for p, tag in ((LOG_REPO, u'log-repo'), (LOG_WS, u'log-ws')):
        if not os.path.exists(p) and not CHECK:
            wr(p, log_head, u'\n')
        patch(p, [(None, LOG109, u'追加 r109 第一拍段')], tag)

    print(u'=== 6/6 MEMORY.md（工作区，限额 %d 字符） ===' % WSMEM_BUDGET)
    t0, _nl0 = rd(WSMEM)
    n0 = len(t0)
    patch(WSMEM, [
        (u'## 二、红线索引（完整 92 条见仓库 PLAYBOOK 附录）',
         u'## 二、红线索引（完整 98 条见仓库 PLAYBOOK 附录）',
         u'红线索引 → 98 条'),
        (WSM_STEPS_OLD, WSM_STEPS_NEW, u'最近拍 → r109'),
    ], u'WS-MEMORY')
    if not CHECK:
        t1, _nl1 = rd(WSMEM)
        print(u'   工作区 MEMORY.md = %d 字符（限额 %d，余量 %d）' % (len(t1), WSMEM_BUDGET, WSMEM_BUDGET - len(t1)))
        if len(t1) > WSMEM_BUDGET:
            sys.exit(u'!! 工作区 MEMORY.md 超出限额：%d > %d（先精简再落盘）' % (len(t1), WSMEM_BUDGET))
    print(u'   (改动前 %d 字符)' % n0)

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
