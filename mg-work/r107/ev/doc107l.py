# -*- coding: utf-8 -*-
u"""r107 第十一拍记忆同步：acceptance / apply107 docstring / HANDOFF / PAGES / PLAYBOOK / 仓库 MEMORY /
工作区 MEMORY / 两份日志。

幂等：每步的 mark 都必须是「只有改后才存在」的串；跑两遍第二遍应全为「跳过」。
用法： python ev/doc107l.py            # 写
      python ev/doc107l.py --check    # 只校验锚点命中数（不写）
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def patch(p, steps, label):
    t, nl = rd(p)
    n0 = len(t)
    for mark, old, new, sub in steps:
        if CHECK:
            if old is not None and t.count(old) != 1:
                BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, t.count(old)))
            continue
        if mark and mark in t:
            SKIPPED.append(label + u' · ' + sub)
            continue
        if old is None:                       # None = 尾部追加
            APPLIED.append(label + u' · ' + sub)
            t = t + new
            continue
        c = t.count(old)
        if c != 1:
            sys.exit(u'!! %s · %s：锚点命中 %d 次（应 1）\n   old=%r' % (label, sub, c, old[:160]))
        APPLIED.append(label + u' · ' + sub)
        t = t.replace(old, new, 1)
    if CHECK:
        print(u'   [check] %s' % os.path.relpath(p, WS))
        return
    if len(t) != n0:
        wr(p, t, nl)
    print(u'   %-42s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


# ============================================================ 1. acceptance.md 第十六节
ACC = os.path.join(REPO, 'mg-work', 'r107', 'acceptance.md')
ACC_NEW = u"""
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
"""

# ============================================================ 2. apply107.py docstring
APPLY = os.path.join(REPO, 'mg-work', 'r107', 'apply107.py')
APPLY_ANCHOR = u"\n体位与历代一致：本脚本 = **净底（base.html 摘掉历代注入块）+ 重新注入本代块**，"
APPLY_NEW = u"""
★ **第十一拍（2026-10-01 13:4x 邵先生四条）** —— 仍是 r107 未提交期的**就地返工**，
  `GENS` / 注入块 id / `NAV_TAG` 依旧一字不动：
    ① **`.td-selbar` 图标与文字应为正文黑** —— 两枚按钮带 `giencoder-btn-text`，DS 该基类把文字色
       定成 `--color-primary-6` ⇒ 实测 `rgb(55,112,247)`。修法 = `.td-selbar .giencoder-btn
       { color: var(--color-text-1) }`（`panel.css` 第 15 节；SVG 走 `currentColor` 自动跟）。
    ② **`.td-url-pill` 补「输入中激活态」** —— 原来只有灰底 + `input:focus{outline:none}` ⇒ 聚焦零变化。
       照 DS `.giencoder-input-wrapper:focus-within` 的口径写「底色转白 + `inset` 1px 主色描边 +
       外 2px 浅主色环 + `transition 120ms`」（第 16 节）；★ **用 `inset` 不用 `border`** ——
       `border` 会把 26px 的胶囊撑高。
    ③ **「调用 N 个工具」数字动效太慢** —— 根因两层：数字 `delay: 1.5s` + `fill: both` ⇒ 延迟期停在
       `from`（`opacity:0`）、**窗口是空的**；而那 1.5s 是**算着骨架屏的生命周期**定的
       （`.r93-sk` 不透明 `inset:0`，早于它退场的动效全白做）。改前真机时间线（`performance.now()`）：
       骨架屏 **2012ms** 淡出 → **2326ms** 移除 → 数字 **2493ms** 首见。
       修法 = **两边一起动**：本文件 `wire()` 里骨架屏 `1100 → 380`（保留 `320`）+ `panel.css` 第 17 节
       数字 `duration .46 → .30` / `delay 1.5s → calc(0.44s + ni*26ms)`（只覆写这两条长属性）
       ⇒ 实测空窗 **167ms → 0**、`tSkGone == tNumVisible`。
    ④ **对照 Codex 官方原版补缺（落地三件）** —— 本拍**首次动了 `_mods.html`**：
       · **终端多标签**（官方「多标签终端」）：`.td-term-tabs` + N 块 `.td-term[data-td-term-pane]`，
         `panel.js` 里 `bindTerm(el)` **按块绑定**、`showTerm()` 只切 `hidden`、`+` 走 `newTermTab()` 真新建；
         ⚠ 全页 `.td-term` 单数选择器一律改走 `termPanes()`（`ctxForTerm()` 也改 `activeTerm()`）。
       · **浏览器截图**（官方「一键截图到剪贴板」）：地址栏补 `[data-td-brw-act="shot"]` +
         `.td-brw.is-shot::after` 快门白闪 **260ms**；⚠ 闪**整模块**、不闪 `.td-view`（后者 `overflow:auto`，
         绝对定位子元素**跟着内容滚走**）；⚠ 动画必须 **≤300ms**（`verify-design.py` 的 `CRAFT-ANIM` 会数）。
       · **产物预览层**（官方「产物查看器」）：`.td-sum-prev`（`inset:0` 覆盖摘要）+ `md`/`xlsx` 两套骨架；
         ⚠ 骨架自带 `display:flex` ⇒ **必须显式写 `[hidden]{display:none}`**；
         ⚠ **Esc 层级多了一层**（预览层 → 元素评论 → 菜单 → 模态），不接进来会「开着预览按 Esc
           把整条侧栏关掉」。
       （官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 ⇒ 静态演示页落不了地，**不做**。）
       ★ **改序**：`part107/_mods.html` → `ev/splice107.py` → 本脚本；⚠ `browse.html` 是 **splice 的产物**、
         不是手改对象。
"""

# ============================================================ 3. HANDOFF.md
HANDOFF = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')
HANDOFF_TAIL_ANCHOR = u"""   产物 **934109 → 936625 字符**（+2516），`+2419 / −8` 行。适配层**零字号改动**。
"""
HANDOFF_TAIL_NEW = HANDOFF_TAIL_ANCHOR + u"""
**⑪ 第十一拍（邵先生 2026-10-01 13:4x 返工 · 四条）**：
1. **`.td-selbar` 图标 / 文字应为正文黑** —— DS `.giencoder-btn-text` 基类给的是**主色蓝**
   （实测 `rgb(55,112,247)`）⇒ 加 `.td-selbar .giencoder-btn { color: var(--color-text-1) }`
   （SVG 走 `currentColor` 跟着变）。实测两枚按钮 `color` / SVG `stroke` 全变 **`rgb(31,31,31)`**。
2. **`.td-url-pill` 补「输入中激活态」** —— 原来 `input:focus{outline:none}` 且只有灰底 ⇒ **聚焦零变化**。
   照 DS `.giencoder-input-wrapper:focus-within` 写「底色转白 + `inset` 1px 主色 + 外 2px 浅主色环 +
   `transition 120ms`」；★ **用 `inset` 不用 `border`**（border 会把 26px 胶囊撑高）。
   ★ 取证坑：`focus()` 后**同步** `getComputedStyle` 读到的是**过渡起点** ⇒ 必须等 400ms 再读。
3. **数字动效太慢** —— 根因两层：`delay 1.5s + fill:both` ⇒ 延迟期窗口是空的；而 1.5s 是
   **为等骨架屏退场**（`.r93-sk` 不透明 `inset:0`）。改前真机时间线 **2012 淡出 → 2326 移除 → 2493 首见**。
   修法**两边一起动**：`apply107.py` 的 `wire()` 骨架屏 `1100→380`（保留 320）+
   CSS 数字 `duration .46→.30` / `delay 1.5s→calc(.44s + ni*26ms)` ⇒ 空窗 **167ms → 0**。整体 ~1.66s。
4. **对照 Codex 官方补缺，落地三件**：**终端多标签**（`.td-term-tabs` + `bindTerm()` 按块绑定 +
   `+` 真新建；右键那条也从「只弹 toast」改成真新建）· **浏览器截图**（相机按钮 + `.td-brw.is-shot::after`
   快门 **260ms**，闪**整模块**而非滚动容器 `.td-view`）· **产物预览层**（`.td-sum-prev` 覆盖摘要 +
   `md`/`xlsx` 两套骨架 + **Esc 算一层**）。官方 SSH / 多窗口 / 托盘不在静态页范围 ⇒ 不做。
   门禁：幂等 ✓ / `check-syntax` 10/10 / `verify-design` 与上轮**逐字节同** / `scan-flatten` 仍 2 条。
   产物 **936625 → 958568 字符**（+21943），`+2806 / −12` 行。★ 本拍**首次动了 `_mods.html`**
   ⇒ 改序 = `_mods.html → ev/splice107.py → apply107.py`（`browse.html` 是 splice 的产物）。
"""

# ============================================================ 4. PAGES.md
PAGES = os.path.join(REPO, '.workbuddy', 'memory', 'PAGES.md')
PAGES_L1 = u"""**⑪ 对照 Codex 官方补缺（三件）+ 划词浮条正文黑 + 地址栏激活态 + 数字动效提速** ——
> ① `.td-selbar` 两枚 DS 文字按钮 **默认正文黑**（`.td-selbar .giencoder-btn{color:var(--color-text-1)}`；
> DS 的 `-btn-text` 基类默认是**主色蓝** `rgb(55,112,247)`）·
> ② `.td-url-pill` 补 **`:focus-within` 激活态**（底色转白 + **`inset` 1px** 主色 + 外 **2px** 浅主色环 + `transition 120ms`；
> ★ **用 `inset` 不用 `border`**，否则 26px 胶囊被撑高）·
> ③ 数字动效提速（骨架屏 `1100→380` + `duration .46→.30` / `delay 1.5s→calc(.44s+ni*26ms)`，空窗 **167ms → 0**）·
> ④ **补三件官方能力**：**终端多标签**（`.td-term-tabs` + `bindTerm()` 按块绑定 + `+` 真新建）/
> **浏览器截图**（`[data-td-brw-act="shot"]` + `.td-brw.is-shot::after` 快门 **260ms**，闪**整模块**而非滚动容器 `.td-view`）/
> **产物预览层**（`.td-sum-prev` 覆盖摘要 + `md`/`xlsx` 两套骨架 + **Esc 算一层**）
> """
PAGES_ROWS = u"""| **终端标签条** | ★ **第十一拍 ④a**：`.td-term-tabs`（`role=tablist`）+ N 块 `.td-term[data-td-term-pane]`，切换**只切 `hidden`**。`panel.js` 里 `bindTerm(el)` **按块绑定**（`echo` 收进各自闭包）；另有 `termPanes()` / `activeTerm()` / `showTerm(id, focus)` / `newTermTab()`。⚠ 全页 `.td-term` 的**单数选择器**一律改走 `termPanes()`（`ctxForTerm()` 也改 `activeTerm()`，否则永远只操作第一块） |
| **浏览器截图** | ★ **第十一拍 ④b**：`[data-td-brw-act="shot"]`（相机图标，插在「标注」与「缩放」之间）+ `.td-mod.td-brw{position:relative}` + `.td-brw.is-shot::after` 快门白闪 **260ms**。⚠ 闪**整模块**、不闪 `.td-view`（后者 `overflow:auto`，绝对定位子元素**跟着内容滚走**）；⚠ 动画必须 **≤300ms**（`verify-design.py` 的 `CRAFT-ANIM` 会数 >300ms 的） |
| **产物预览层** | ★ **第十一拍 ④c**：`.td-sum-prev`（`position:absolute; inset:0; z-index:6`，包含块 = `.td-mod.td-sum`）+ 两套骨架 `[data-td-prev-kind="md"/"xlsx"]`（**按扩展名**切）。⚠ 骨架自带 `display:flex` ⇒ **必须显式写 `[hidden]{display:none}`**；⚠ **Esc 层级多了一层**（预览层 → 元素评论 → 菜单 → 模态） |
| **地址栏激活态 / 浮条色** | ★ **第十一拍 ①②**：`.td-url-pill:focus-within`（底色转白 + `inset 0 0 0 1px` 主色 + 外 `0 0 0 2px` 浅主色环，`transition 120ms`）· `.td-selbar .giencoder-btn { color: var(--color-text-1) }`（DS `-btn-text` 默认主色蓝） |
"""

# ============================================================ 5. PLAYBOOK.md
PLAYBOOK = os.path.join(REPO, '.workbuddy', 'memory', 'PLAYBOOK.md')
PLAYBOOK_NEW = u"""
## P3.47 ★★ r107 第十一拍（四条 · 2026-10-01 13:4x 邵先生）

**① 「动效的延迟若是等某个遮罩退场」⇒ 提速必须两边一起改**
* 症状：数字滑入动效「快 2.5 秒才出现」、观感像「根本没有数字」。
* 根因两层：(a) `animation-delay: calc(1.5s + ni*55ms)` **+** `fill: both` ⇒ 延迟期停在 `from`
  （`opacity: 0`），而 `.r93-num` 是 `inline-block`、**空位一直占着** ⇒ 那段时间窗口是**空的**；
  (b) 那个 1.5s 是**算着骨架屏的生命周期**定的（`.r93-sk` = `position:absolute; inset:0` + **不透明**
  `--color-bg-2` ⇒ **早于它退场的任何动效都白做**）。
* ★ **配方**：先用 `performance.now()` **量出真实时间线**（本站 = 遮罩淡出 2012 / 遮罩移除 2326 /
  内容首见 2493），再**同时**调「遮罩生命周期」与「动效 `delay/duration`」，判据用**空窗时长**
  （本站 167ms → **0**）。只调一边必然无效：只提前动效 ⇒ 被遮罩盖着；只提前遮罩 ⇒ 动效还在等。
* ⚠ 探针自身也会骗人：轮询器**装得太晚**会漏掉早段（本站 `tSkOut = null` / `late = 1`）⇒
  判据取**「遮罩移除时刻」与「内容首见时刻」**这对不受起跑影响的量。

**② 量 `transition` 属性必须等过渡走完**
* 症状：改完聚焦态样式，`focus()` 后**同步**读 `getComputedStyle` 得到 `none` / 起点值 ⇒ 误判「没生效」。
* ★ 正解：`focus → setTimeout(…, 400) → 读数 → blur → setTimeout(…) → 读数`，把结果存 `window.__X`
  再另一次 eval 取回（本站 `p107l_pill.js`）。**任何带 `transition` 的属性都适用。**

**③ 覆盖层别放进滚动容器；给自带 `display` 的类加 `[hidden]` 必须显式写规则**
* `.td-view` 是 `overflow:auto` ⇒ 绝对定位子元素会**跟着内容滚走**（滚过之后快门就闪不见了）
  ⇒ 覆盖层挂到**最近的、非滚动的**祖先（`.td-brw` + `position:relative`）。
* 另一半是同一个坑：**自带 `display` 的类会压过 UA 的 `[hidden]{display:none}`**
  （本站 `.td-pv-md{display:flex}`）⇒ 覆盖层 / 骨架一律补 `[hidden]{display:none}`。

**④ DS 的 `-text` 按钮默认是主色；DS 输入框的激活态有固定口径**
* `.giencoder-btn-text` 把 `color` 定成 `--color-primary-6` ⇒ 要「正文黑」得显式
  `color: var(--color-text-1)`（SVG 走 `currentColor`，自动跟）。
* DS 输入框激活态 = `.giencoder-input-wrapper:focus-within { border-color: primary-6;
  box-shadow: 0 0 0 2px primary-light-2 }`。**Pill / 定高形态改用 `inset` 描边**
  （`box-shadow: inset 0 0 0 1px primary-6, 0 0 0 2px primary-light-2`）——
  写 `border` 会把定高胶囊**撑高 2px**。

**⑤ 「点了只弹 toast」= 真缺口（对照官方补缺的判据）**
* 方法：拿**官方功能清单**逐条对照本地实现，凡「有入口但点了只有一句 toast、没有任何视觉」
  的就是缺口（本站 = 产物「预览」、右键「新建终端标签」）。补的时候**优先补视觉/结构**，
  不是补文案。★ 顺带一条：**给元素换视觉要挑对宿主** —— 想「闪整个面板」就挂面板，
  挂内部滚动容器会被滚走（见 ③）。

★ **体位**：本拍**首次动了 `_mods.html`** ⇒ 改序 = `part107/_mods.html` → `ev/splice107.py`
（重组 `browse.html`）→ `apply107.py`；⚠ **`browse.html` 是 splice 的产物、不是手改对象**
（手改会在下次 splice 时被冲掉）。`part105/*` 仍是跨代资产、零改动。
产物 `936625 → 958568` 字符（第十一拍 +21943）；`+2806 / −12` 行；门禁全绿；
`scan-flatten` 仍 **2 条**（新增规则一律带 `var(--font-size-*)`）；`verify-design` 与上轮**逐字节同**。
"""

# ============================================================ 6. 仓库 MEMORY.md
MEM = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')
MEM_L1 = u"""> **第十一拍（四条）** = ⑯ **划词浮条图标 / 文字应为正文黑**（DS `.giencoder-btn-text` 基类给的是**主色蓝**
> `rgb(55,112,247)` ⇒ 加 `.td-selbar .giencoder-btn{color:var(--color-text-1)}`；SVG 走 `currentColor` 自动跟）｜
> ⑰ **地址栏 `.td-url-pill` 补 `:focus-within` 激活态**（底色转白 + **`inset` 1px 主色** + 外 2px 浅主色环；
> ★ 用 `inset` 不用 `border`，否则 26px 胶囊被撑高；★ 取证坑：`focus()` 后**同步** `getComputedStyle`
> 读到的是**过渡起点**，必须等 400ms）｜
> ⑱ **数字动效提速**（根因两层：`delay 1.5s + fill:both` ⇒ 延迟期停在 `from`、**窗口是空的**；
> 而那 1.5s 是**为等骨架屏退场**。改前真机时间线 **2012 淡出 → 2326 移除 → 2493 首见**。
> 修法**两边一起动**：`apply107.py` 的 `wire()` 骨架屏 `1100→380` + CSS `duration .46→.30` /
> `delay 1.5s→calc(.44s + ni*26ms)` ⇒ 空窗 **167ms→0**）｜
> ⑲ **对照 Codex 官方补缺，落地三件**：**终端多标签**（`bindTerm()` 按块绑定 + 标签只切 `hidden` +
> `+` 真新建；⚠ 全页 `.td-term` 单数选择器一律改走 `termPanes()`）· **浏览器截图**（相机按钮 +
> `.td-brw.is-shot::after` 快门 **260ms**；★ 闪**整模块**而非滚动容器 `.td-view`；⚠ 动画 ≤300ms 因
> `verify-design` 的 `CRAFT-ANIM`）· **产物预览层**（`.td-sum-prev` 覆盖摘要 + `md`/`xlsx` 两套骨架 +
> **Esc 算一层**，否则开着预览按 Esc 会**关掉整条侧栏**）。
> （官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 ⇒ 静态演示页落不了地，**不做**。）
> ★ **体位**：本拍**首次动了 `_mods.html`** ⇒ 改序 = `_mods.html` → `ev/splice107.py`（重组 `browse.html`）
> → `apply107.py`；⚠ **`browse.html` 是 splice 的产物、不是手改对象**。
"""
MEM_PROD_OLD = (u"> **产物**：`conversation.html` **799231 → … → 934109 → 936625 Unicode 字符**（十拍合计 **+137394**）；\n"
                u"> UTF-8 字节（LF 归一）**1029334** ｜ 工作区字节（CRLF）**1036446** ｜ LF `sha1 bc830fa56c0c`；"
                u"`base.html` **472150 逐字节不变**。")
MEM_PROD_NEW = (MEM_L1 +
                u"> **产物**：`conversation.html` **799231 → … → 934109 → 936625 → 958568 Unicode 字符**"
                u"（十一拍合计 **+159337**）；\n"
                u"> UTF-8 字节（LF 归一）**1055517** ｜ 工作区字节（CRLF）**1063012** ｜ LF `sha1 5ce6b87f5150`；"
                u"`base.html` **472150 逐字节不变**。")

# ============================================================ 7. 工作区 MEMORY.md
WSMEM = os.path.join(WS, '.workbuddy', 'memory', 'MEMORY.md')
WSMEM_ANCHOR = u"## 二、Windows 环境速记"
WSMEM_NEW = u"""49. ★★ **动效的延迟若是「等某个遮罩退场」，提速必须两边一起改**（r107 第十一拍）：数字动效
    `delay: 1.5s + fill: both` 让延迟期停在 `from`（`opacity:0`）⇒ 那段时间**窗口是空的**；
    而 1.5s 本身是**算着骨架屏生命周期**定的（`.r93-sk` 不透明 `inset:0` ⇒ 早于它退场的动效全白做）。
    ★ 配方：先用 `performance.now()` **量真实时间线**（本站 = 淡出 2012 / 移除 2326 / 首见 2493），
    再**同时**调「遮罩生命周期」与「动效 delay/duration」，判据用**空窗时长**（167ms → **0**）。
    ⚠ 轮询器**装得太晚**会漏掉早段（`tSkOut=null / late=1`）⇒ 判据取「移除时刻 + 首见时刻」这对量。
50. ★★ **量 `transition` 属性必须等过渡走完**（r107 第十一拍）：`focus()` 后**同步**读
    `getComputedStyle` 拿到的是**起点值**（`rgba(0,0,0,0) 0px 0px 0px 0px inset`）⇒ 会误判「没生效」。
    ★ 正解 = `focus → setTimeout(…, 400) → 读数 → blur → setTimeout(…) → 读数`（存 `window.__X` 再取回）。
51. ★★ **覆盖层别放进滚动容器 + 自带 `display` 的类加 `[hidden]` 必须显式写规则**（r107 第十一拍）：
    `overflow:auto` 的容器里，绝对定位子元素会**跟着内容滚走**（`.td-view` 实测）⇒ 覆盖层挂**最近的
    非滚动祖先**；另一半是同一个坑 —— `.td-pv-md{display:flex}` 会**压过 UA 的 `[hidden]{display:none}`**。
52. ★ **DS 的 `-text` 按钮默认是主色；DS 输入框激活态有固定口径**（r107 第十一拍）：
    `.giencoder-btn-text` 把 `color` 定成 `--color-primary-6` ⇒ 要「正文黑」得显式
    `color: var(--color-text-1)`。DS 输入框激活态 = 底色转白 + `border-color: primary-6` +
    `box-shadow: 0 0 0 2px primary-light-2`；**Pill / 定高形态改用 `inset` 描边**（写 `border` 会撑高 2px）。
    ★ 顺带：「有入口但点了只弹 toast、没有任何视觉」= **真缺口**（对照官方功能清单就是判据）。

"""

# ============================================================ 8. 两份日志
LOG_REPO = os.path.join(REPO, '.workbuddy', 'memory', '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')
LOG_NEW = u"""
### 第十一拍（邵先生 2026-10-01 13:4x · 四条）

**① `.td-selbar` 图标与文字默认正文黑** —— 根因：两枚按钮带 DS 的 `giencoder-btn-text`，
该基类把 `color` 定成 `--color-primary-6`（实测 `rgb(55,112,247)`）。
修法 `.td-selbar .giencoder-btn { color: var(--color-text-1) }`（(0,2,0) + 文档序在后）；
实测两枚按钮 `color` / SVG `stroke` / SVG `color` **全变 `rgb(31,31,31)`**。

**② `.td-url-pill` 补「输入中激活态」** —— 原来只有灰底 + `input:focus{outline:none}` ⇒ 聚焦**零变化**。
照 DS `.giencoder-input-wrapper:focus-within` 写：底色转白 + `inset 0 0 0 1px` 主色 +
外 `0 0 0 2px` 浅主色环 + `transition 120ms`（★ **`inset` 代替 `border`**，否则 26px 胶囊被撑高）。
实测聚焦 `bg=rgb(255,255,255)`、`shadow=rgb(55,112,247) 0 0 0 1px inset, rgb(218,228,254) 0 0 0 2px`、
`:focus-within=true`、**pill 高恒 26**；失焦完全回退。
★ 踩坑：`focus()` 后**同步**读 `getComputedStyle` 拿到的是**过渡起点** ⇒ 改成「等 400ms 再读」。

**③ 「调用 5 个工具」数字动效提速** —— 根因两层：`delay: 1.5s` + `fill: both` ⇒ 延迟期停在 `from`
（`opacity:0`）而 `.r93-num` 是 `inline-block`、空位一直占着 ⇒ **窗口是空的**；那 1.5s 是
**为等骨架屏退场**（`.r93-sk` 不透明 `inset:0`）。改前真机时间线：**2012 淡出 → 2326 移除 → 2493 首见**。
修法 = **两边一起动**：`apply107.py` 的 `wire()` 骨架屏 `1100 → 380`（保留 `320`）+ `panel.css` 第 17 节
数字 `duration .46 → .30` / `delay 1.5s → calc(.44s + ni*26ms)`。
实测 `tSkGone == tNumVisible`（空窗 **167ms → 0**）、`numAnim={delay:"0.44s", dur:"0.3s", fill:"both"}`、
`skStillInDom=false`、整体 ~1.66s。

**④ 对照 Codex 官方补缺（落地三件）** —— 调研：官方 = 五入口 + 摘要面板 + 行内评论 + 暂存/撤销 +
界面内 Commit/Push/PR + **渲染页面上直接标注** + **一键截图到剪贴板** + **多标签终端** + **产物查看器**
（PDF/表格/文档/演示）+ SSH（alpha，不在侧栏）/ 多窗口 / 托盘。我们已相当齐全，**真缺且能落地**的只有三件：
* **④a 终端多标签**：`_mods.html` 补 `.td-term-tabs`（`zsh` / `npm run dev` / `+`），原 `.td-term` 正文
  **逐字**搬进 `t1`、新增 `t2`；`panel.js` 把「单 `term` 变量」拆成 **`bindTerm(el)` 按块绑定**
  （`echo` 进各自闭包，`CANNED` 表与 `keydown` 分支逐字未改），新增 `termPanes()/activeTerm()/showTerm()/newTermTab()`。
  实测：切 `t2` → `visiblePanes=["t2"]`、`activeName="npm run dev"`；点 `+` → `tabCount=3`、新标签「终端 3」激活；
  **t1 输出 4 行 / t2 3 行，零回归**。
* **④b 浏览器截图**：地址栏「标注」与「缩放」之间补 `[data-td-brw-act="shot"]`（相机）；
  `.td-mod.td-brw{position:relative}` + `.td-brw.is-shot::after` 快门白闪 **260ms**
  （★ 闪**整模块**不闪滚动容器 `.td-view`；★ 必须 ≤300ms，`verify-design` 的 `CRAFT-ANIM` 会数）。
  实测：`flashed=true` / `animationName="td-shot-flash"` / `0.26s` / toast 正确 / 400ms 后回收；
  ★ 布局零扰动（`.td-url` 高仍 40、pill 高仍 26）。
* **④c 产物预览层**：「预览」从「只弹 toast」变成 `panel.js` 的 `prevShow()` 打开 `.td-sum-prev`
  （覆盖整块摘要）+ `md`/`xlsx` 两套骨架 + 「在系统打开 / 关闭」；**Esc 裁决把预览层算一层**。
  实测：`prevBox == paneBox == [898,798]`（完整覆盖）、名/元信息正确、骨架按扩展名切换；
  `press Escape` → 预览层关、**`paneOpen=true`（侧栏没被误关）**。

**门禁**：幂等 ✓（`patch107l2.py` 第二遍「应用 0 / 跳过 3」；`apply107.py` 第二遍「已是目标态」）/
`check-syntax` **10/10** / `verify-design` 与 `vd-r107k.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`，
零新增、**一处渐变都没引**）/ `scan-flatten panel.css` 仍 **2 条**。
**产物**：`conversation.html` 936625 → **958568** 字符（第十一拍合计 **+21943**；UTF-8 LF 归一 1055517 字节 /
工作区 1063012 / LF `sha1 5ce6b87f5150`）；`base.html` 472150 逐字节不变；`+2806 / −12` 行。
**探针** `ev/p107m.js` + `ev/probe107m.sh` → `ev/m-raw.log`；**补丁** `ev/patch107l1.py`（①②③）+
`ev/patch107l2.py`（④）。★ **本拍首次动了 `_mods.html`** ⇒ 改序 = `_mods.html → ev/splice107.py → apply107.py`。
🚫 未 commit / 未 push。
"""


def main():
    # 1. acceptance.md：尾部追加第十六节
    patch(ACC, [(u'## 十六、第十一拍（邵先生 2026-10-01 13:4x · 四条）', None, ACC_NEW, u'追加第十六节')],
          'acceptance.md')
    # 2. apply107.py docstring
    patch(APPLY, [(u'第十一拍（2026-10-01 13:4x 邵先生四条）', APPLY_ANCHOR,
                   APPLY_NEW + APPLY_ANCHOR, u'docstring 第十一拍段')], 'apply107.py')
    # 3. HANDOFF
    patch(HANDOFF, [
        (u'（十一拍累积）', u'最后更新：2026-10-01 14:0x（**r106 已提交 `4d081ba`** + **r107 侧栏模块标签化已落地（十拍累积）**',
         u'最后更新：2026-10-01 14:1x（**r106 已提交 `4d081ba`** + **r107 侧栏模块标签化已落地（十一拍累积）**',
         u'头行 时间 + 十拍→十一拍累积'),
        (u'共**十一拍**）', u'共**十拍**）', u'共**十一拍**）', u'r107 段头 十拍→十一拍'),
        (u'（**十六节**，含第二 ~ 十一拍返工）', u'（**十五节**，含第二 ~ 十拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.46**；',
         u'（**十六节**，含第二 ~ 十一拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.47**；', u'节数 + P3.47'),
        (u'**⑪ 第十一拍（邵先生 2026-10-01 13:4x 返工 · 四条）**', HANDOFF_TAIL_ANCHOR, HANDOFF_TAIL_NEW,
         u'追加第十一拍段'),
    ], 'HANDOFF.md')
    # 4. PAGES
    patch(PAGES, [
        (u'· **共十一拍**）', u'· **共十拍**）', u'· **共十一拍**）', u'P3.11i 标题 十拍→十一拍'),
        (u'**十一拍要点**', u'> **十拍要点**：', u'> **十一拍要点**：', u'逐拍要点标题'),
        (u'**⑪ 对照 Codex 官方补缺（三件）+ 划词浮条正文黑', u'（详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五**节）。',
         u'> ' + PAGES_L1 + u'（详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五** / **十六**节）。',
         u'逐拍要点 +⑪'),
        (u'**终端标签条**', u'\n**⚠ 改这一块之前必看**\n',
         u'\n' + PAGES_ROWS + u'**⚠ 改这一块之前必看**\n', u'固定事实表 +4 行'),
        (u'| Esc 层级 | window 捕获段：**划词浮条** →', u'| Esc 层级 | window 捕获段：模态 → 菜单 → 元素评论 →（再交给 ctrl-conv）关侧栏 |',
         u'| Esc 层级 | window 捕获段：**划词浮条** → 模态 → 菜单 → 元素评论 → **产物预览层** →（再交给 ctrl-conv）关侧栏（★ 第十一拍 ④c 把预览层接进来，否则开着预览按 Esc 会**把整条侧栏关掉**）|',
         u'Esc 层级行更新'),
        (u'（终端正文，收键盘；★ 第十一拍', u'（终端正文，收键盘）',
         u'（终端正文，收键盘；★ 第十一拍 ④a 起**每块一份**，N 个）', u'tabindex 行更新'),
        (u'\n> **⑪ 对照 Codex 官方补缺（三件）', u'\n> > **⑪ 对照 Codex 官方补缺（三件）',
         u'\n> **⑪ 对照 Codex 官方补缺（三件）', u'修正重复引用符（> >  →  >）'),
        (u'.td-term-tabs（★ 第十一拍 ④a', u'      ├ section.td-mod.td-mod-term[data-td-pane="terminal"]\n',
         u'      ├ section.td-mod.td-mod-term[data-td-pane="terminal"]\n'
         u'      │   ├ .td-term-tabs（★ 第十一拍 ④a：zsh / npm run dev / ＋）\n'
         u'      │   └ .td-term[data-td-term-pane="t1|t2|…"] ×N\n', u'结构图 终端展开'),
    ], 'PAGES.md')
    # 5. PLAYBOOK
    patch(PLAYBOOK, [(u'## P3.47 ★★ r107 第十一拍', None, PLAYBOOK_NEW, u'追加 P3.47')], 'PLAYBOOK.md')
    # 6. 仓库 MEMORY.md
    patch(MEM, [
        (u'· 十一拍）——', u'· 十拍）—— 🚫 未提交', u'· 十一拍）—— 🚫 未提交', u'r107 段头 十拍→十一拍'),
        (u'本代**十一拍**', u'本代**十拍**（同一代、`apply107.py` 就地返工十次',
         u'本代**十一拍**（同一代、`apply107.py` 就地返工十一次', u'本代十拍→十一拍'),
        (u'第十一拍（四条）** = ⑯', MEM_PROD_OLD, MEM_PROD_NEW, u'追加第十一拍段 + 更新产物段'),
        (u'与 `vd-r107l.txt` **逐字节相同**', u'与 `vd-r107c.txt` **逐字节相同**',
         u'与 `vd-r107l.txt` **逐字节相同**', u'verify-design 基线文件名'),
        (u'第十一拍**新增 0 条**', u'仍 **2 条**（第十拍**不动字号**）', u'仍 **2 条**（第十一拍**新增 0 条**）',
         u'scan-flatten 描述'),
        (u'（`+2806 / −12` 行）', u'（`+2419 / −8` 行）', u'（`+2806 / −12` 行）', u'git status 行数'),
        (u'P3.39 ~ P3.47**；各拍要点见 **PAGES P3.11i（共十一拍）**',
         u'P3.39 ~ P3.46**；各拍要点见 **PAGES P3.11i（共十拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十五节）**。',
         u'P3.39 ~ P3.47**；各拍要点见 **PAGES P3.11i（共十一拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十六节）**。',
         u'定论指向 + P3.47/十一拍/十六节'),
        (u'｜官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 **不在静态页范围**（本轮已拍板不做）',
         u'｜折叠默认范围。', u'｜折叠默认范围｜官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 **不在静态页范围**（本轮已拍板不做）。',
         u'待拍板 + 官方三项说明'),
    ], 'MEMORY.md(仓库)')
    # 7. 工作区 MEMORY.md
    patch(WSMEM, [(u'49. ★★ **动效的延迟若是', WSMEM_ANCHOR, WSMEM_NEW + WSMEM_ANCHOR, u'硬规则 +49~52')],
          'MEMORY.md(工作区)')
    # 8. 两份日志
    patch(LOG_REPO, [(u'### 第十一拍（邵先生 2026-10-01 13:4x', None, LOG_NEW, u'追加第十一拍')], '日志(repo)')
    patch(LOG_WS, [(u'### 第十一拍（邵先生 2026-10-01 13:4x', None, LOG_NEW, u'追加第十一拍')], '日志(ws)')

    print()
    if BAD:
        print(u'!! 锚点异常 %d 处：' % len(BAD))
        for x in BAD:
            print(u'   ' + x)
        sys.exit(1)
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for x in APPLIED:
        print(u'  + ' + x)
    for x in SKIPPED:
        print(u'  = ' + x)


if __name__ == '__main__':
    main()
