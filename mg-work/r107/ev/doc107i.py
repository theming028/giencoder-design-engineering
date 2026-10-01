# -*- coding: utf-8 -*-
"""r107 第八拍 · 记忆同步（幂等：跑两遍验）。

覆盖：
  1. mg-work/r107/acceptance.md                  -> 追加「十三、第八拍」
  2. mg-work/r107/apply107.py                    -> docstring 补第八拍段
  3. .workbuddy/memory/HANDOFF.md                -> 头行 / 二·g 段（七拍->八拍）/ 追加 ⑧ 小节
  4. .workbuddy/memory/PAGES.md                  -> P3.11i（共七拍->共八拍 + 逐拍要点 + 4 行固定事实）
  5. .workbuddy/memory/PLAYBOOK.md               -> 追加 P3.44
  6. .workbuddy/memory/MEMORY.md                 -> 索引 + r107 段
  7. E:/GienCoder/.workbuddy/memory/MEMORY.md    -> 硬规则 38~41
  8. 两份当日日志                                 -> 追加第八拍条目

用法： python mg-work/r107/ev/doc107i.py
"""
import io
import sys

HANDOFF = u'.workbuddy/memory/HANDOFF.md'
PAGES = u'.workbuddy/memory/PAGES.md'
PLAYBOOK = u'.workbuddy/memory/PLAYBOOK.md'
REPO_MEM = u'.workbuddy/memory/MEMORY.md'
WS_MEM = u'E:/GienCoder/.workbuddy/memory/MEMORY.md'
ACC = u'mg-work/r107/acceptance.md'
APPLY = u'mg-work/r107/apply107.py'
LOG_REPO = u'.workbuddy/memory/2026-10-01.md'
LOG_WS = u'E:/GienCoder/.workbuddy/memory/2026-10-01.md'

APPLIED = []
SKIPPED = []


def rd(p):
    return io.open(p, 'rb').read().decode('utf-8')


def wr(p, t):
    io.open(p, 'wb').write(t.encode('utf-8'))


def patch(p, steps, label):
    t = rd(p)
    n0 = len(t)
    for mark, old, new, sub in steps:
        if mark and mark in t:
            SKIPPED.append(label + u' \u00b7 ' + sub + u'\uff08\u5df2\u5b58\u5728\uff09')
            continue
        if not mark and old not in t:
            # \u81ea\u52a8\u5e42\u7b49\u5224\u636e\uff1a\u65e7\u4e32\u4e0d\u5728\u4e86\u3001\u4e14\u76ee\u6807\u6001\u5df2\u5728 \u21d2 \u5df2\u5e94\u7528
            if new in t:
                SKIPPED.append(label + u' \u00b7 ' + sub + u'\uff08\u5df2\u5e94\u7528\uff09')
                continue
            sys.exit(u'!! %s \u00b7 %s\uff1a\u65e7\u4e32\u4e0e\u65b0\u4e32\u90fd\u4e0d\u5b58\u5728' % (label, sub))
        c = t.count(old)
        if c != 1:
            sys.exit(u'!! %s \u00b7 %s\uff1a\u951a\u70b9\u547d\u4e2d %d \u6b21\uff08\u5e94 1\uff09' % (label, sub, c))
        t = t.replace(old, new, 1)
        APPLIED.append(label + u' \u00b7 ' + sub)
    if len(t) != n0:
        wr(p, t)
    print(u'   %-46s %d -> %d' % (p, n0, len(t)))


def append_once(p, mark, block, label):
    t = rd(p)
    if mark in t:
        SKIPPED.append(label + u'\uff08\u5df2\u5b58\u5728\uff09')
        print(u'   %-46s %d (\u65e0\u53d8\u5316)' % (p, len(t)))
        return
    wr(p, t.rstrip('\n') + block)
    APPLIED.append(label)
    print(u'   %-46s %d -> %d' % (p, len(t), len(rd(p))))


# ================================================================ 1. acceptance.md
ACC_BLOCK = u'''


---

## 十三、第八拍（邵先生 2026-10-01 12:3x 返工 · 六条）

六条全部落在 `part107/panel.css`（新增**第 14 节** + 第 3 / 6 / 10 节就地改）+ `part107/panel.js`（删一项菜单）；
`_mods.html` / `browse.html` **一字未动** ⇒ 不必重跑 `splice107.py` / `make107.py`。

### 第八拍 ① 全局「宽度不够 ⇒ 文字省略号」（★ 本轮主体）

**落地口径 = 三类分治**（写死进第 14 节的注释，免得下轮再逐条讨论）：

| 类 | 处置 | 例子 |
|---|---|---|
| 单行文本容器（名称 / 路径 / 域名 / 标题 / 计数） | **省略号** | `.td-browse-tree-title` / `.td-diff-btn` / `.td-commit-btn` / `.td-note-time` / `.td-sum-tag` / `.td-rv-commit` … |
| 代码与终端 | **不截断**（保持 `pre` + 折行） | `.td-dr-t` / `.td-dsc-c` / `.td-code-*` / `.td-term-*` |
| 多行正文 | **不截断**（折行） | `.td-sum-p` / `.td-note-b` / `.td-sum-plan li` / `.td-page-h1` |

**三件套缺一不可**：`min-width: 0`（flex 子项的收缩下限默认是 `min-content`，不解除就永远把兄弟顶出去）
+ `overflow: hidden` + `text-overflow: ellipsis` + `white-space: nowrap`（不换行才谈得上省略）。

**白名单 17 类**（`querySelectorAll(sel).length` vs 「三件套齐」的元素数 —— 三档实测 **EL = n，零例外**）：

| 选择器 | n | 选择器 | n |
|---|---|---|---|
| `.td-browse-tree-title` | 1 | `.td-sum-tag` | 1 |
| `.td-diff-more` | 2 | `.td-sum-srct i` | 3 |
| `.td-diff-btn` | 10 | `.td-sum-artt i` | 2 |
| `.td-commit-btn` | 2 | `.td-elnote-t` | 1 |
| `.td-commit-t` | 1 | `.td-url-annot` | 1 |
| `.td-commit-lb` | 1 | `.td-page-cta` | 1 |
| `.td-note-who` | 2 | `.td-page-foot` | 1 |
| `.td-note-time` | 2 | `.td-rv-commit` / `.td-rv-pr` | 1 / 1 |

**改前已覆盖的六类未被弄坏**：`td-tab-name` / `td-mm-name` / `td-diff-path` / `td-rv-meta` /
`td-sum-hint` / `td-browse-crumb-path`。

★ **两条补充规则**（容器自带 `display:flex / inline-flex` 时，裸文本会变成**匿名 flex 项**，
容器上的 `text-overflow` 对它**无效** ⇒ 文字落在子 `<span>` 里的要单独点）：
`.td-rv-commit` / `.td-rv-pr` / `.td-commit-row` / `.td-commit-ck` 的 `> span`；
行内评论头 `td-note-who` 先让位（`flex: 1 1 auto`）、`td-note-time` 保原宽（`flex: none`）。

**验证（三档真机）**：1440 / 右栏开 · 1024 / 右栏开 · 右栏压到 **240px**（改 `--av-browse-w`）。
窄栏实测被裁元素**全部**呈 `ellipsis/nowrap`（`i3-panel230-review.png` 里 `p...` / `m...` / `do...` / `.work...`
均出省略号），且多行评论 / 代码**正常折行、未截断**。

### 第八拍 ② 去掉「折叠此文件」

`panel.js` 的 `ctxForFile()` 里**整项删除** `{ label: isOpen ? '折叠此文件' : '展开此文件', … }`；
顺手删掉失去引用的 `var isOpen = art.classList.contains('is-open');`（全文 `isOpen` 剩 **0** 次）。
右键文件菜单 = **6 项**：暂存此文件 / 撤销此文件的改动 / 复制文件路径 / 复制 git apply 命令 /
在文件树中定位 / **展开全部文件**（探针 `hasFoldOne: false`）。
★ 头部职责注释同步：`③ 审查：文件折叠（点头部 = 单个 / 菜单 = 全部⇄展开全部）…`。

### 第八拍 ③ `.td-sum-h` = 15px

`.td-sum-h { font-size: calc(15px * var(--ui-fs-ratio)); }` —— **不写裸 `15px`**：
本代 `converge()` 把「体里含 `var(--font-size-*)`」当作重派生判据，而 15px **没有 title token**
⇒ 用 `calc(Npx * var(--ui-fs-ratio))` 形态（**自动豁免压平**、且仍吃 `--ui-fs` 杠杆）。
实测 4 个 `h4.td-sum-h` = `{('15px','500')}`，行高随之 `22.5px`（`.td-sum-sec` 自然长高），三档一致。

### 第八拍 ④ `.td-diff-path` 展开后中粗 500

```css
.td-diff.is-open .td-diff-path { font-weight: 500; }
```

展开 `font-weight: 500` / 折叠 `400` —— 4 张 diff 卡同屏对照（`i3-review-panel.png` 可见粗细差）。

### 第八拍 ⑤ `.td-diff-path` 与 `.td-diff-rows` 内一律 13px

`path` 容器 = `var(--font-size-body-2)`（13）；`rows` 容器同样 13，且 `.td-dr` / `.td-dsc-c` / `.td-diff-more`
**三处各自写死的字号**逐条同值覆盖（只改容器无效）。
★ **只换 token 档位**（仍旧写成 `var(--font-size-*)`）⇒ `converge()` 的「含 token 才重派生行高」判据不受影响：
`.td-dr` 行高 **20px 未变**、`.td-diff-h` 高 **38 未变**（派生链完好）。

### 第八拍 ⑥ `.r107-stats` 文字居中（★ 两处死胡同，值得记）

**死胡同 1**：第一版写 `width: fit-content; max-width: 100%; margin: 0 auto` ⇒ 被页面级两条
`!important` 规则**压死**（`main > … > div.mt-8 > div`：r95 ② 的 `width:50%!important; min-width:860px!important`
与 r106 ④ 的 `width:min(…)!important; min-width:0!important`）⇒ 盒宽**恒等于输入卡**（实测 860 / 714 / 315 三档全等），
`width / min-width / max-width` **一条都改不动** ⇒ `fit-content` 是**死代码**。
诊断路径：先以为是 `min-width:auto` ⇒ 用 `min-width:0` / `width:100%` 做**反证**，三种状态盒宽**都不变**
⇒ 才顺藤查到那两条页面级 `!important`。

**死胡同 2**：真节点不像当年的 `::after` 那样自动 shrink-wrap ⇒ 满宽盒里文字默认靠左；
而宿主的 `items-center` 对这个**满宽子项**不生效（实测输入卡自己就是齐左的）⇒ `margin: auto` 会比输入卡**偏 32px**。

⇒ **正解 = `text-align: center`**（它没有任何 `!important` 竞争者）。
判据 = **文字盒中心 − 输入卡中心 = 0**（用 `Range.selectNodeContents` 取**文字真实盒**，与输入卡几何比）。
1440（右栏开）：盒 714 / 文字 630 / 左内距 42 ⇒ **中心差 0**。

★ **① 与 ⑥ 在本元素上可以共存**：Chromium 在「居中 + 溢出」时对齐行为**退化为 `start`**
（文字盒仍自盒左缘起算），省略号**照常落在行尾** —— 实测 1024 截图尾部为「首 token 平…」。
（★ 第一版注释把这条写反了，看截图后**整块更正**。）

### 第八拍 门禁 / 产物

| 项 | 读数 |
|---|---|
| 幂等 | `patch107i.py` 末次 **`应用 0 项 / 跳过 8 项`**；`apply107.py` 第二遍「已是目标态」 |
| JS/CSS 语法 | `mg-work/check-syntax.py pages/*.html` **10/10 通过**（conversation `script=9 style=16`） |
| 设计校验 | `verify-design.py ./pages` 与上轮 `vd-r107h.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）⇒ **零新增** |
| 压平自查 | `ev/scan-flatten.py` 改前改后均 **2 条**（`.td-mod-bar` / `.td-url`，与本拍无关）⇒ 无新增风险 |
| 改动面 | `git status` = `M pages/conversation.html`（`+2299 / −3`）+ `M pages/avatar.html`（`+1 / −1`，第七拍遗留）+ `M .workbuddy/memory/*` + `?? mg-work/r107/` |
| 其它页 | `base.html` **472150 字符 / LF sha1 `23f6fbedfe76` 逐字节不变**；另 8 页 sha1 全同 |
| 注入块 id | `r107-conv-css` / `r107-conv-js` 各 1；`r106-nav-js` / `r107-nav-js` / `r102-` 全 **0** |

**产物**：`pages/conversation.html` **927464 → 930384 字符**（第八拍 **+2920**；相对 HEAD **+131153**）。
工作区字节（CRLF）**1026880**；UTF-8（LF 归一）**1019883**；LF `sha1 c8b5e944e2de`。
**资产**：`part107/panel.css` **40517 → 42788** 字符（CRLF 832 → 889 行）· `panel.js` **48583 → 48401** 字符（LF 1127 行）；
`_head.html` / `_mods.html` / `browse.html` 未动。
**探针**：`ev/p107i1~i5.js` + `ev/probe107i{,2,3,4,5}.sh` + `ev/shots107i.sh`；
日志 `i107-*.log` / `i107-v-*.log` / `i107-s-*.log` / `vd-r107i{,2}.txt`；出图 `raw/i1-*` · `raw/i2-*` · `raw/i3-*`。
**备份**：`ev/bak8/`（动手前的 `panel.css` / `panel.js`）。
'''

# ================================================================ 2. apply107.py
APPLY_BLOCK = u'''\u2605 **第八拍（2026-10-01 12:3x 邵先生六条）** —— 仍是 r107 未提交期的**就地返工**，
  `GENS` / 注入块 id / `NAV_TAG` 依旧一字不动（工作区仍是 `M conversation.html` + `?? mg-work/r107/`）；
  六条全部落在 `part107/panel.css`（新增第 14 节 + 第 3 / 6 / 10 节就地改）+ `part107/panel.js`（删一项菜单）；
  `_mods.html` / `browse.html` **一字未动** ⇒ 不必重跑 `splice107.py` / `make107.py`：
    ① **全局「宽度不够 ⇒ 省略号」** —— 新增第 14 节，17 类单行文本容器挂三件套
       （`min-width:0` + `overflow:hidden` + `text-overflow:ellipsis` + `white-space:nowrap`）。
       \u2605 **三类分治**：单行文本 ⇒ 截断；**代码 / 终端**（`.td-dr-t` / `.td-dsc-c` / `.td-code-*` / `.td-term-*`）
       与**多行正文**（`.td-sum-p` / `.td-note-b` / `.td-sum-plan li` / `.td-page-h1`）⇒ 保持折行、**明确不截断**。
       \u26a0 容器自带 `display:flex / inline-flex` 时裸文本会变**匿名 flex 项**、容器上的 `text-overflow` 对它无效
         ⇒ 文字落在子 `<span>` 里的那几处要单独点。
    ② **去掉「折叠此文件」** —— `panel.js` 的 `ctxForFile()` 整项删除，并清掉失去引用的 `var isOpen`。
       右键文件菜单 = 6 项（尾为「展开全部文件」）。
    ③ **`.td-sum-h` = 15px** —— 写 `calc(15px * var(--ui-fs-ratio))`（15px **无 title token**；该形态自动豁免
       `converge()` 的压平，且仍吃 `--ui-fs` 杠杆）。行高随之 22.5、`.td-sum-sec` 自然长高。
    ④ **`.td-diff-path` 展开后中粗 500** —— `.td-diff.is-open .td-diff-path { font-weight: 500 }`。
    ⑤ **`.td-diff-path` / `.td-diff-rows` 内一律 13px** —— 只换 token 档位（`--font-size-body-2`），
       且子规则 `.td-dr` / `.td-dsc-c` / `.td-diff-more` 自己写死了字号 ⇒ **逐条同值覆盖**（改容器无效）。
       `.td-dr` 行高 20 / `.td-diff-h` 高 38 **未变**（converge 派生链完好）。
    ⑥ **`.r107-stats` 文字居中** —— \u2605 两处死胡同：`width:fit-content; margin:0 auto` 被页面级两条
       `!important` 盒宽规则压死（盒宽恒等于输入卡 860/714/315，`width/min-width/max-width` 全改不动）；
       真节点又不像 `::after` 自动 shrink-wrap ⇒ 满宽盒里 `margin:auto` 会比输入卡**偏 32px**
       ⇒ 正解 = **`text-align: center`**（无 `!important` 竞争者）。判据 = 文字盒中心 − 输入卡中心 = 0。
       \u2605 ① 与 ⑥ 可共存：Chromium 居中 + 溢出时对齐退化为 `start`，省略号照常落行尾（实测 1024）。

'''

# ================================================================ 3. HANDOFF.md
HANDOFF_G8 = u'''**\u2467 第八拍（邵先生 2026-10-01 12:3x 返工 · 六条）** —— 六条全落 `part107/panel.css` + `panel.js`，
`_mods.html` / `browse.html` 一字未动（不必重跑 splice / make）：
1. **全局「宽度不够 ⇒ 省略号」**（新增第 14 节，17 类单行文本容器挂三件套）；\u2605 **三类分治** ——
   单行文本 ⇒ 截断；**代码 / 终端**与**多行正文** ⇒ 保持折行、**明确不截断**（截断即丢信息）。
   \u26a0 flex / inline-flex 容器里的裸文本是**匿名 flex 项** ⇒ 容器上的 `text-overflow` 无效，文字在子 `<span>` 的要单独点。
2. **去掉「折叠此文件」**（`ctxForFile()` 整项删；右键文件菜单 = 6 项，尾为「展开全部文件」）。
3. **`.td-sum-h` = 15px**（写 `calc(15px * var(--ui-fs-ratio))`，15px 无 title token；行高随 22.5）。
4. **`.td-diff-path` 展开后中粗 500**。
5. **`.td-diff-path` / `.td-diff-rows` 内一律 13px**（只换 token 档位；子规则逐条同值覆盖；
   `.td-dr` 行高 20 / `.td-diff-h` 38 未变 ⇒ converge 派生链完好）。
6. **`.r107-stats` 文字居中** ⇒ \u2605 **两处死胡同**：`fit-content + margin:auto` 被页面级两条 `!important`
   盒宽规则压死（盒宽恒等于输入卡 860/714/315）；真节点不像 `::after` 自动 shrink-wrap ⇒ `margin:auto` 偏 **32px**
   ⇒ 正解 = **`text-align: center`**。\u2605 ① 与 ⑥ 可共存（居中 + 溢出时 Chromium 退化为 `start`、省略号照落行尾）。

**第八拍门禁**：幂等 ✓（`应用 0 / 跳过 8`）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107h.txt`
**逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜`scan-flatten` 改前改后均 2 条（无新增压平）。
产物 **927464 → 930384 字符（+2920；相对 HEAD +131153）**；工作区字节 1026880 / UTF-8（LF 归一）1019883 / LF `sha1 c8b5e944e2de`。
资产 `panel.css 42788`（CRLF 889 行）· `panel.js 48401`（LF 1127 行）。探针 `ev/p107i1~i5.js` + `probe107i{,2,3,4,5}.sh`；
出图 `raw/i{1,2,3}-*.png`。动手前备份 `ev/bak8/`。

'''

# ================================================================ 4. PAGES.md
PAGES_QS_NEW = u'''> **八拍要点**：① 三段式骨架 + 五模块 \u00b7 ② 浮窗关不掉 / 侧聊对齐 \u00b7 ③ 删侧聊 / 并排折叠 / 折叠全部 / 补 Codex 遗漏 \u00b7
> ④ 摘要升默认 + 卡片式 / 补划词浮条 / 补右键菜单 / tab 14px / 下拉 DS 化 \u00b7
> ⑤ 下拉 hover 补齐 + 下拉改挂 DS Dropdown（从「导航菜单 Menu」族改正过来）\u00b7
> **⑥ 底部统计行「框选不到」实为 CSS 生成内容 \u2192 换真 DOM / `.r93-pre` 去字体族 / 内容列变窄时技能浮窗与 `.r93-alert` 自适应** \u00b7
> **⑦ 右栏里的竞品名全换 GienCoder / 去掉下拉菜单的标题行与快捷键提示 / 选中项补底色 / 提交卡输入框拉通 / 右栏字体统一 / 全屏按钮联动** \u00b7
> **⑧ 全局宽度不足出省略号（三类分治）/ 去掉「折叠此文件」/ `.td-sum-h` 15px / `.td-diff-path` 展开中粗 / `.td-diff-path` 与 `.td-diff-rows` 内 13px / `.r107-stats` 居中**
> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三**节）。'''

PAGES_QS_OLD = u'''> 六拍照次：① 三段式骨架 + 五模块 \u00b7 ② 浮窗关不掉 / 侧聊对齐 \u00b7 ③ 删侧聊 / 并排折叠 / 折叠全部 / 补 Codex 遗漏 \u00b7
> ④ 摘要升默认 + 卡片式 / 补划词浮条 / 补右键菜单 / tab 14px / 下拉 DS 化 \u00b7
> ⑤ 下拉 hover 补齐 + 下拉改挂 DS Dropdown（从「导航菜单 Menu」族改正过来）\u00b7
> **⑥ 底部统计行「框选不到」实为 CSS 生成内容 \u2192 换真 DOM / `.r93-pre` 去字体族 / 内容列变窄时技能浮窗与 `.r93-alert` 自适应** \u00b7
> **⑦ 右栏里的竞品名全换 GienCoder / 去掉下拉菜单的标题行与快捷键提示 / 选中项补底色 / 提交卡输入框拉通 / 右栏字体统一 / 全屏按钮随右栏联动**
> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二节）。'''

PAGES_ROWS = u'''| **全局省略号口径** | \u2605 **第八拍 ①**：**三类分治** —— 单行文本容器 \u21d2 三件套截断（`min-width:0` + `overflow:hidden` + `text-overflow:ellipsis` + `white-space:nowrap`）；**代码 / 终端**与**多行正文** \u21d2 保持折行、**不截断**。白名单 17 类见 `panel.css` 第 14 节 |
| **`.td-sum-h` 字号** | \u2605 **第八拍 ③**：`calc(15px * var(--ui-fs-ratio))` —— 15px **无 title token**，故**不写裸 px**（裸 px 会被 `converge()` 压平、且不吃 `--ui-fs` 杠杆） |
| **`.td-diff-path` / `.td-diff-rows`** | \u2605 **第八拍 ④⑤**：path 13px；`is-open` 时 path `font-weight:500`；rows 容器 13 且 `.td-dr` / `.td-dsc-c` / `.td-diff-more` **逐条覆盖**（只改容器无效） |
| **`.r107-stats` 居中** | \u2605 **第八拍 ⑥**：`text-align: center` —— \u26a0 `width/min-width/max-width` **全被页面级两条 `!important` 钉死**（盒宽恒等于输入卡 860/714/315），`fit-content + margin:auto` 那一版是**死代码** |
'''

# ================================================================ 5. PLAYBOOK.md
PB_BLOCK = u'''
---

## P3.44 \u2605\u2605 r107 第八拍（六条 \u00b7 2026-10-01 12:3x 邵先生返工）

> 六条 = ① 全局「宽度不够 \u21d2 省略号」 ② 去掉「折叠此文件」 ③ `.td-sum-h` 15px
> ④ `.td-diff-path` 展开中粗 500 ⑤ `.td-diff-path` / `.td-diff-rows` 内 13px ⑥ `.r107-stats` 文字居中。
> 逐条实测见 `mg-work/r107/acceptance.md` 第十三节；本节只提炼**机制级**教训。

#### ① \u2605\u2605 「全局宽度不够出省略号」先分**三类**，别一把梭

邵先生原话是「**全局所有的**对象元素或容器」—— **照字面全挂 `text-overflow` 是错的**：

| 类 | 处置 | 理由 |
|---|---|---|
| 单行文本容器（名称 / 路径 / 域名 / 标题 / 计数） | **截断出省略号** | 本来就是「一眼看个大概」的信息 |
| 代码与终端（`.td-dr-t` / `.td-dsc-c` / `.td-code-*` / `.td-term-*`） | **保持折行、不截断** | 截断代码 = 丢信息；它们本就是「窄了换行」的语义 |
| 多行正文（`.td-sum-p` / `.td-note-b` / `.td-sum-plan li` / `.td-page-h1`） | **保持折行、不截断** | 截断段落 = 丢内容 |

**三件套缺一不可**：`min-width: 0`（flex 子项的收缩下限默认是 `min-content`，不解除就永远把兄弟顶出去）
+ `overflow: hidden` + `text-overflow: ellipsis` + `white-space: nowrap`（不换行才谈得上省略）。

\u2605 **容器自带 `display:flex / inline-flex` 时，裸文本会变成「匿名 flex 项」**
\u21d2 容器上的 `text-overflow` 对它**无效** \u21d2 文字落在子 `<span>` 里的那几处要**单独点**
（本拍：`.td-rv-commit` / `.td-rv-pr` / `.td-commit-row` / `.td-commit-ck` 的 `> span`）。
\u2605 同一行里的两个元素要**排优先级**：谁让位（`flex: 1 1 auto`）、谁保原宽（`flex: none`）——
本拍是「评论人让位、时间保宽」（时间只有几个字，被截断就读不懂了）。

#### ② \u2605\u2605\u2605 「居中」遇上**页面级 `!important` 钉死的盒宽**：先查「谁在管这个 width」

本拍要把 `.r107-stats`（输入卡下方那行统计小字）居中。**第一版是死代码**：

```css
/* 错误写法：width / min-width / max-width 全被别处 !important 钉住 */
.r107-stats { width: fit-content; max-width: 100%; margin: 0 auto; }
```

**根因**：它的盒宽由**页面级两条 `!important`** 决定（都挂在 `main > … > div.mt-8 > div` 上，
r95 ② 与 r106 ④ 两个版本）\u21d2 盒宽**恒等于输入卡**（实测 860 / 714 / 315 三档全等），
三条 width 属性**一条都改不动**。

**诊断路径（可照抄）**：
1. 先怀疑「`min-width: auto` 撑住了」\u21d2 注入 `min-width: 0` / `width: 100%` 做**反证**；
2. 三种状态盒宽**都不变** \u21d2 说明**有更高优先级的东西在管它**（不是你改的那几条）；
3. 翻页面级规则 \u21d2 找到那两条 `!important` \u21d2 定性。

**正解**：`text-align: center`（**它没有任何 `!important` 竞争者**）。
\u2605 **真节点 \u2260 伪元素**：当年的 `::after` 是 shrink-wrap 的（盒随文走），换成的真节点在**满宽盒**里
默认靠左；而宿主的 `items-center` 对这个满宽子项**不生效**（实测输入卡自己就是齐左的）
\u21d2 靠 `margin: auto` 会比输入卡**偏 32px**。

**判据**：`Range.selectNodeContents(el)` 取**文字真实盒**（不是盒子盒）与输入卡几何比
\u21d2 **文字盒中心 \u2212 输入卡中心 = 0**。

#### ③ \u2605\u2605 「居中」与「溢出省略」可以共存 —— 别凭「常识」写进注释

同一条规则里既要居中又要省略。**第一版注释想当然写成「Chromium 居中 + 溢出时两端对称裁切、
不落省略号 \u21d2 省略号让位于居中」—— 是错的**。

实测（1024 / 右栏开）：Chromium 在「居中 + 溢出」时对齐行为**退化为 `start`**（文字盒仍自盒左缘起算）
\u21d2 **省略号照常落在行尾**（截图尾部为「首 token 平…」）\u21d2 **① 与 ⑥ 可以共存**（注释已整块更正）。

\u2605 教训：**写进代码注释里的实测结论必须来自截图 / 取值，不能来自「应该是这样」** ——
否则下一个人会照着你写反的注释做出错误的取舍。

#### ④ \u2605 15px 档没有 title token \u21d2 用 `calc(Npx * var(--ui-fs-ratio))`

本代 `converge()`（`mg-work/r88/apply88b-fontsize.py`）的判据是「**体里含 `var(--font-size-*)`**
才重派生 `line-height / height / min-height`」\u21d2 裸 `font-size: 15px` 既**被压平**、又**不吃 `--ui-fs` 杠杆**。
DS 字号 token 实测只有 12 / 13 / 14 / 16（**无 15**）\u21d2 **15px 档一律写 `calc(15px * var(--ui-fs-ratio))`**
（该形态自动豁免压平，且仍随杠杆走）。判据：`h4.td-sum-h` 实测 `15px`、行高随之 `22.5px`。

#### ⑤ \u2605 「同值覆盖」要**逐条**，改容器无效

`.td-diff-rows` 容器改字号**不影响子树** —— 里面 `.td-dr`(12) / `.td-dsc-c`(12) / `.td-diff-more`(12)
**三处各自写死了字号** \u21d2 只改容器，容器自己变了、文字一点没动。
\u2605 同值覆盖时**只换 token 档位**（仍旧写 `var(--font-size-*)`）\u21d2 `converge()` 的重派生判据不受影响，
行高 / 块高派生链**完好**（实测 `.td-dr` 行高 20 / `.td-diff-h` 高 38 未变）。

#### ⑥ \u2605\u2605 幂等补丁的 `mark` 必须是「**只有改后才存在**」的串

本拍 `panel.js` 要删 `ctxForFile()` 里「折叠此文件」那一项。`mark` 一开始选了

```python
mark = "'\u5c55\u5f00\u5168\u90e8\u6587\u4ef6' : '\u6298\u53e0\u5168\u90e8\u6587\u4ef6', ico: toExpand ? 'plus' : 'close'"
```

—— **这段在改前就已存在** \u21d2 第一遍就被误判成「已应用」而**静默跳过删除**，
而同批的另一处（删 `var isOpen`）**已经执行** \u21d2 `isOpen` 变成未定义变量（**页面不报错、只是后续判断恒假**）。

**修法**：`mark` 改成**只有删掉中间那项才成立的邻接关系**：

```python
mark = "'-',\\n      { label: toExpand ? '\u5c55\u5f00\u5168\u90e8\u6587\u4ef6'"
```

\u2605 通法：幂等 `mark` 的语义是「**目标态特征**」，不是「这段代码长什么样」。
删中间项 \u21d2 用「**删完后才相邻**的两端」当 mark；改值 \u21d2 用「**改完后才出现的**新值」当 mark。

#### ⑦ \u2605\u2605 同一选择器改多稿 \u21d2 用「**按选择器整块替换**」，别逐版字符串匹配

`.r107-stats` 那条规则改了三稿（`fit-content` \u2192 `text-align` \u2192 更正注释），
`patch` 脚本对三个历史版本各写一份常量 \u21d2 全部匹配失败（`new 0 / mid 0 / old 0`）。
**修法** = 换成一个通用函数：按**选择器**定位、找首个 `\\n}\\n` 作块尾、整块替换：

```python
def replace_block(t, sel, new_block, label):
    i = t.find(sel)
    if i < 0:
        return t
    j = t.find('\\n}\\n', i)
    cur = t[i:j + 3]
    if cur == new_block:          # 已是目标态 -> 幂等
        return t
    return t[:i] + new_block + t[j + 3:]
```

\u21d2 **对历史版本彻底解耦**（不管中间改过几稿，只要「选择器定位到的那块」不等于目标文本就重写）。

#### ⑧ 本拍门禁 / 产物

幂等 \u2713（`应用 0 项 / 跳过 8 项`；`apply107.py` 第二遍「已是目标态」）｜`check-syntax` **10/10**｜
`verify-design` 与 `vd-r107h.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）\u21d2 零新增｜
`scan-flatten` 改前改后均 **2 条**（无新增压平风险）｜改动面 = `M pages/conversation.html`（`+2299 / \u22123`）
+ `M pages/avatar.html`（`+1 / \u22121`）+ `?? mg-work/r107/`。
产物 **927464 \u2192 930384 字符（+2920；相对 HEAD +131153）**。
\u2605 **体位**：本拍**未动** `_mods.html` / `browse.html` \u21d2 不必重跑 `splice107.py` / `make107.py`，
改序只剩 `part107/*` \u2192 `apply107.py`（part 文件是**运行时读**的，改完直接重跑即落页面）。
'''

# ================================================================ 6. repo MEMORY.md
MEM_R107_G8 = u'''> **第八拍（六条）** = \u2466 **全局「宽度不够 \u21d2 省略号」**（新增第 14 节，17 类单行文本容器挂三件套；\u2605 **三类分治** ——
> 单行文本 \u21d2 截断；**代码 / 终端**与**多行正文** \u21d2 保持折行、**明确不截断**；\u26a0 flex / inline-flex 容器里的裸文本是
> **匿名 flex 项** \u21d2 容器上的 `text-overflow` 无效，文字在子 `<span>` 的要单独点）\uff5c
> \u2467 **去掉「折叠此文件」**（`ctxForFile()` 整项删，右键文件菜单 = 6 项）\uff5c
> \u2468 **`.td-sum-h` = 15px**（写 `calc(15px * var(--ui-fs-ratio))`，15px 无 title token）\uff5c
> \u2469 **`.td-diff-path` 展开后中粗 500**\uff5c
> \u246a **`.td-diff-path` / `.td-diff-rows` 内一律 13px**（只换 token 档位；子规则逐条同值覆盖；`.td-dr` 行高 20 / `.td-diff-h` 38 未变）\uff5c
> \u246b **`.r107-stats` 文字居中**（\u2605 两处死胡同：`fit-content + margin:auto` 被页面级两条 `!important` 盒宽规则压死；
> 真节点不像 `::after` 自动 shrink-wrap \u21d2 `margin:auto` 偏 **32px** \u21d2 正解 = **`text-align: center`**；
> \u2605 ① 与 ⑥ **可共存**（居中 + 溢出时 Chromium 退化为 `start`、省略号照落行尾））。
> **产物**：`conversation.html` **799231 \u2192 \u2026 \u2192 927464 \u2192 930384 Unicode 字符**（八拍合计 **+131153**）；
> UTF-8 字节（LF 归一）**1019883** \uff5c 工作区字节（CRLF）**1026880** \uff5c LF `sha1 c8b5e944e2de`；`base.html` **472150 逐字节不变**。
> **八查**：幂等 \u2713（每拍连跑两遍）\uff5c`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）\uff5c
> `verify-design.py ./pages` 与 `vd-r107c.txt` **逐字节相同**（21882 字节 / md5 `3dbf654337559509110899e48bef1b1c`）\u21d2 **零新增**\uff5c
> `scan-flatten.py` 改前改后均 **2 条**（无新增压平）\uff5c代数残留 **0**\uff5c
> `git status` = `M pages/conversation.html`（`+2299 / \u22123` 行）+ `M pages/avatar.html`（`+1 / \u22121`）+ `?? mg-work/r107/`。
> \u2605\u2605 **新增定论见 PLAYBOOK P3.39 ~ P3.44**；各拍要点见 **PAGES P3.11i（共八拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十三节）**。
'''

MEM_IDX_INLINE = (
    u'\uff5c**P3.44=r107 \u7b2c\u516b\u62cd\uff08\u516d\u6761\uff09** \u2605\u2605\u2605 '
    u'**\u300c\u5168\u5c40\u90fd\u8981\u51fa\u7701\u7565\u53f7\u300d\u8fd9\u7c7b\u300c\u5168\u5c40\u300d\u9700\u6c42\u5148\u7ed9\u5bf9\u8c61**\u5206\u4e09\u7c7b**'
    u'\uff08\u5355\u884c\u6587\u672c\u21d2\u622a\u65ad / **\u4ee3\u7801\u00b7\u7ec8\u7aef**\u4e0e**\u591a\u884c\u6b63\u6587**\u21d2\u4fdd\u6301\u6298\u884c\u3001**\u4e0d\u622a\u65ad**\uff1b'
    u'\u2605 **\u5bb9\u5668\u81ea\u5e26 `display:flex / inline-flex` \u65f6\u88f8\u6587\u672c\u662f\u300c\u533f\u540d flex \u9879\u300d** \u21d2 \u5bb9\u5668\u4e0a\u7684 `text-overflow` \u5bf9\u5b83\u65e0\u6548\uff09'
    u' / \u2605\u2605\u2605 **\u300c\u5c45\u4e2d\u300d\u6539\u4e0d\u52a8 \u21d2 \u5148\u67e5\u300c\u8c01\u5728\u7ba1\u8fd9\u4e2a `width`\u300d**'
    u'\uff08`.r107-stats` \u7684 `fit-content + margin:auto` \u88ab\u9875\u9762\u7ea7\u4e24\u6761 `!important` \u76d2\u5bbd\u89c4\u5219**\u538b\u6b7b**\uff1b'
    u'\u7b2c\u4e00\u6b65\u7528\u6ce8\u5165 `min-width:0` / `width:100%` **\u53cd\u8bc1**\u770b\u76d2\u5bbd\u52a8\u4e0d\u52a8\uff1b'
    u'\u6b63\u89e3 = `text-align:center`\uff1b\u2605 **\u771f\u8282\u70b9 \u2260 \u4f2a\u5143\u7d20**\uff1a`::after` \u662f shrink-wrap\u3001\u771f\u8282\u70b9\u5728\u6ee1\u5bbd\u76d2\u91cc\u9ed8\u8ba4\u9760\u5de6\uff0c'
    u'`margin:auto` \u4f1a\u504f 32px\uff1b**\u5224\u636e = `Range.selectNodeContents` \u53d6\u300c\u6587\u5b57\u771f\u5b9e\u76d2\u300d\u7684\u4e2d\u5fc3**\uff09'
    u' / \u2605\u2605 **\u5e42\u7b49\u8865\u4e01\u7684\u300c\u5df2\u5e94\u7528\u300d\u5224\u636e\uff08mark\uff09\u5fc5\u987b\u662f\u300c\u53ea\u6709\u6539\u540e\u624d\u5b58\u5728\u300d\u7684\u4e32**'
    u'\uff08\u5220\u5217\u8868\u4e2d\u95f4\u4e00\u9879\u65f6 mark \u9009\u4e86\u6539\u524d\u5c31\u6709\u7684\u90bb\u63a5\u884c \u21d2 **\u9759\u9ed8\u8df3\u8fc7**\uff1b'
    u'**\u540c\u4e00\u9009\u62e9\u5668\u6539\u591a\u7a3f\u522b\u9010\u7248\u5b57\u7b26\u4e32\u5339\u914d** \u21d2 \u7528\u300c\u6309\u9009\u62e9\u5668\u5b9a\u4f4d + \u627e\u9996\u4e2a `\\n}\\n` \u4f5c\u5757\u5c3e + \u6574\u5757\u66ff\u6362\u300d\uff09'
    u' / \u2605\u2605 **\u5199\u8fdb\u4ee3\u7801\u6ce8\u91ca\u91cc\u7684\u5b9e\u6d4b\u7ed3\u8bba\u5fc5\u987b\u6765\u81ea\u622a\u56fe\u53d6\u503c\uff0c\u4e0d\u80fd\u51ed\u300c\u5e94\u8be5\u662f\u8fd9\u6837\u300d**'
    u'\uff08\u66fe\u628a\u300c\u5c45\u4e2d + \u6ea2\u51fa\u4e0d\u843d\u7701\u7565\u53f7\u300d\u5199\u53cd\uff1b\u5b9e\u6d4b\u662f\u5bf9\u9f50**\u9000\u5316\u4e3a `start`**\u3001\u7701\u7565\u53f7\u7167\u843d\u884c\u5c3e\uff09'
    u' / **15px \u65e0 token \u6863\u4f4d \u21d2 \u5199 `calc(15px * var(--ui-fs-ratio))`**\uff08\u88f8 px \u4f1a\u88ab `converge()` \u538b\u5e73\uff09'
    u' / **\u6539\u5b57\u53f7\u6539\u5bb9\u5668\u65e0\u6548**\uff08\u5b50\u89c4\u5219\u5404\u81ea\u5199\u6b7b\u4e86\u5b57\u53f7 \u21d2 \u9010\u6761\u540c\u503c\u8986\u76d6\uff0c\u4e14\u53ea\u6362 token \u6863\u4f4d\u4ee5\u4fdd\u4f4f\u884c\u9ad8\u6d3e\u751f\u94fe\uff09'
)

# ================================================================ 7. 工作区 MEMORY.md
WS_BLOCK = u'''38. \u2605\u2605 **「全局都要出省略号」这类"全局"需求，先给对象**分三类**再动手**（r107 第八拍）：
    ① 单行文本容器（名称 / 路径 / 域名 / 标题 / 计数）\u21d2 **截断**（`min-width:0` + `overflow:hidden` +
    `text-overflow:ellipsis` + `white-space:nowrap`，**四件缺一不可**）；② **代码 / 终端** \u21d2 保持折行、**不截断**
    （截断代码 = 丢信息，且它们本就是「窄了换行」的语义）；③ **多行正文** \u21d2 保持折行、**不截断**（截断段落 = 丢内容）。
    \u26a0\u2605 **容器自带 `display:flex / inline-flex` 时裸文本是「匿名 flex 项」** \u21d2 容器上的 `text-overflow` 对它**无效**
    \u21d2 文字落在子 `<span>` 里的要**单独点**；同一行两个元素还要排优先级（谁 `flex:1 1 auto` 让位、谁 `flex:none` 保宽）。
39. \u2605\u2605\u2605 **元素"居中"改不动 \u21d2 先查「谁在管这个 `width`」，多半是页面级 `!important`**（r107 第八拍）：
    `.r107-stats` 第一版 `width: fit-content; max-width: 100%; margin: 0 auto` 是**死代码** —— 它的盒宽被页面级两条
    `!important`（同一选择器 `main > … > div.mt-8 > div` 的两个历史版本）**钉死**，盒宽恒等于输入卡（860 / 714 / 315 三档全等）。
    **诊断路径**：先怀疑 `min-width:auto` \u21d2 注入 `min-width:0` / `width:100%` 做**反证** \u21d2 三种状态盒宽**都不变**
    \u21d2 才去翻页面级规则。**正解 = `text-align: center`**（它没有 `!important` 竞争者）。
    \u2605 **真节点 \u2260 伪元素**：`::after` 是 shrink-wrap 的，真节点在**满宽盒**里默认靠左，而宿主 `items-center`
    对满宽子项**不生效** \u21d2 `margin:auto` 会比对齐基准**偏 32px**。**判据 = 用 `Range.selectNodeContents` 取「文字真实盒」
    的中心**（不是盒子盒）与基准元素几何比，差 0 才算过。
40. \u2605\u2605 **幂等补丁的"已应用"判据（mark）必须是「只有改后才存在」的串**（r107 第八拍踩过**静默跳过**）：
    删列表中间一项时，mark 若选了**改前就已存在**的邻接行 \u21d2 第一遍就判"已应用"、**整条删除被跳过**，
    而同批另一处（删失去引用的变量）**已经执行** \u21d2 变量变未定义（**页面不报错、只是后续判断恒假**，极难发现）。
    通法：**删中间项** \u21d2 mark = 「**删完后才相邻**的两端」；**改值** \u21d2 mark = 「**改完后才出现的**新值」。
    \u2605 同族：**同一选择器改多稿时，别逐版写字符串常量匹配**（第三稿就会 `old 0 / mid 0 / new 0` 全不中）
    \u21d2 用「**按选择器定位 + 找首个 ``\\n}\\n`` 作块尾 + 整块替换**」的通用函数，与历史版本彻底解耦。
41. \u2605\u2605 **写进代码注释里的"实测结论"必须来自截图 / 取值，不能来自"应该是这样"**（r107 第八拍把结论写反过一次）：
    我原以为「Chromium 居中 + 溢出时两端对称裁切、不落省略号」\u21d2 看截图才发现**对齐退化为 `start`、省略号照落行尾**。
    \u21d2 注释写反 \u21d2 下一个人会照着做错取舍。\u2605 同族：**15px 这类"没有 token 档位"的字号，写
    `calc(15px * var(--ui-fs-ratio))`**（裸 px 会被 `converge()` 压平、且不吃 `--ui-fs` 杠杆）；
    \u2605 改字号**改容器无效**（子规则各自写死了字号）\u21d2 **逐条同值覆盖，且只换 token 档位**（保住行高派生链）。

'''

# ================================================================ 8. 日志
LOG_BLOCK = u'''
### 第八拍（邵先生 2026-10-01 12:3x · 六条返工）

1. **全局「宽度不够 ⇒ 省略号」** ⇒ `panel.css` 新增**第 14 节**（白名单 17 类单行文本容器挂三件套：
   `min-width:0` + `overflow:hidden` + `text-overflow:ellipsis` + `white-space:nowrap`）。
   \u2605 **三类分治**：单行文本 ⇒ 截断；**代码 / 终端**（`.td-dr-t` / `.td-dsc-c` / `.td-code-*` / `.td-term-*`）
   与**多行正文**（`.td-sum-p` / `.td-note-b` / `.td-sum-plan li` / `.td-page-h1`）⇒ 保持折行、**明确不截断**。
   \u26a0 flex / inline-flex 容器里的裸文本是**匿名 flex 项** ⇒ 容器上的 `text-overflow` 无效，
   文字在子 `<span>` 里的那几处（`.td-rv-commit` / `.td-rv-pr` / `.td-commit-row` / `.td-commit-ck`）要单独点。
   三档实测 EL = n（1/2/10/2/1/1/2/2/1/3/2/1/1/1/1/1/1），**零例外**；改前已覆盖的六类未被弄坏。
2. **去掉「折叠此文件」** ⇒ `panel.js` 的 `ctxForFile()` 整项删除 + 清掉失去引用的 `var isOpen`
   （全文 `isOpen` 剩 0 次）；右键文件菜单 = 6 项（尾为「展开全部文件」），探针 `hasFoldOne:false`。
3. **`.td-sum-h` = 15px** ⇒ 写 `calc(15px * var(--ui-fs-ratio))`（15px **无 title token**；该形态自动豁免
   `converge()` 的压平、且仍吃 `--ui-fs` 杠杆）。实测 4 个 `h4.td-sum-h` = `{('15px','500')}`，行高 22.5。
4. **`.td-diff-path` 展开后中粗 500** ⇒ `.td-diff.is-open .td-diff-path { font-weight: 500 }`（折叠仍 400）。
5. **`.td-diff-path` / `.td-diff-rows` 内一律 13px** ⇒ 只换 token 档位（`--font-size-body-2`）；
   子规则 `.td-dr` / `.td-dsc-c` / `.td-diff-more` 自己写死了字号 ⇒ **逐条同值覆盖**。
   `.td-dr` 行高 20 / `.td-diff-h` 高 38 **未变**（converge 派生链完好）。
6. **`.r107-stats` 文字居中** ⇒ \u2605 **两处死胡同**：`width: fit-content; margin: 0 auto` 被页面级两条
   `!important` 盒宽规则**压死**（盒宽恒等于输入卡 860 / 714 / 315）；真节点不像 `::after` 自动 shrink-wrap
   ⇒ `margin:auto` 比输入卡**偏 32px** ⇒ 正解 = **`text-align: center`**（无 `!important` 竞争者）。
   判据 = 文字盒中心 − 输入卡中心 = 0（1440 右栏开：盒 714 / 文字 630 / 左内距 42）。
   \u2605 ① 与 ⑥ **可共存**：Chromium 居中 + 溢出时对齐退化为 `start`、省略号照落行尾（1024 实测）。

**产物**：`pages/conversation.html` **927464 → 930384 字符**（第八拍 **+2920**；相对 HEAD **+131153**）；
工作区字节（CRLF）**1026880** / UTF-8（LF 归一）**1019883** / LF `sha1 c8b5e944e2de`。
**改动面**：`M pages/conversation.html`（`+2299 / −3`）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`；
`base.html` **472150 逐字节不变**。
**门禁**：幂等 ✓（`patch107i.py` 末次 `应用 0 项 / 跳过 8 项`；`apply107.py` 第二遍「已是目标态」）/
`check-syntax.py pages/*.html` **10/10** / `verify-design.py ./pages` 与 `vd-r107h.txt` **逐字节相同**
（md5 `3dbf654337559509110899e48bef1b1c`）/ `scan-flatten.py` 改前改后均 2 条。
**体位**：仍是 r107 **未提交期的就地返工**（`GENS` / 注入块 id / `NAV_TAG` 一字不动）；
改序 `part107/*` → `ev/patch107i.py` → `apply107.py`（**未动** `_mods.html` / `browse.html` ⇒ 不重跑 splice / make）。
**资产**：`part107/panel.css 42788`（CRLF 889 行）· `panel.js 48401`（LF 1127 行）。
**探针**：`ev/p107i1~i5.js` + `probe107i{,2,3,4,5}.sh` + `shots107i.sh`；出图 `raw/i{1,2,3}-*.png`。**备份**：`ev/bak8/`。
'''


def main():
    # ---- 1
    append_once(ACC, u'## \u5341\u4e09\u3001\u7b2c\u516b\u62cd', ACC_BLOCK, u'acceptance.md \u00b7 \u5341\u4e09\u8282\uff08\u7b2c\u516b\u62cd\uff09')

    # ---- 2
    patch(APPLY, [
        (u'**\u7b2c\u516b\u62cd\uff082026-10-01 12:3x',
         u'\n\n\u4f53\u4f4d\u4e0e\u5386\u4ee3\u4e00\u81f4\uff1a\u672c\u811a\u672c = **\u51c0\u5e95',
         u'\n\n' + APPLY_BLOCK + u'\u4f53\u4f4d\u4e0e\u5386\u4ee3\u4e00\u81f4\uff1a\u672c\u811a\u672c = **\u51c0\u5e95',
         u'docstring \u7b2c\u516b\u62cd\u6bb5'),
    ], u'apply107.py')

    # ---- 3
    patch(HANDOFF, [
        (u'\u516b\u62cd\u7d2f\u79ef\uff09** \u2192 \u56db\u67e5\u5168\u7eff + \u4e94\u6a21\u5757\u5b9e\u6d4b + \u591a\u8f6e\u771f bug',
         u'\u4e03\u62cd\u7d2f\u79ef\uff09** \u2192 \u56db\u67e5\u5168\u7eff + \u4e94\u6a21\u5757\u5b9e\u6d4b + \u5341\u56db\u5904\u771f bug',
         u'\u516b\u62cd\u7d2f\u79ef\uff09** \u2192 \u56db\u67e5\u5168\u7eff + \u4e94\u6a21\u5757\u5b9e\u6d4b + \u591a\u8f6e\u771f bug',
         u'\u5934\u884c\uff08\u4e03\u62cd\u2192\u516b\u62cd + \u56db\u67e5\u2192\u591a\u8f6e\uff09'),
        (None, u'\u6700\u540e\u66f4\u65b0\uff1a2026-10-01 11:4x',
         u'\u6700\u540e\u66f4\u65b0\uff1a2026-10-01 13:0x', u'\u5934\u884c\u65f6\u95f4'),
        (None, u'2026-10-01 09:3x \u8d77\uff0c\u5171**\u4e03\u62cd**',
         u'2026-10-01 09:3x \u8d77\uff0c\u5171**\u516b\u62cd**', u'\u4e8c\u00b7g \u6807\u9898'),
        (None, u'\uff08**\u5341\u4e8c\u8282**\uff0c\u542b\u7b2c\u4e8c ~ \u4e03\u62cd\u8fd4\u5de5\uff09\uff1b\u673a\u5236\u7ea7\u6559\u8bad\u89c1 PLAYBOOK **P3.39 ~ P3.43**\uff1b',
         u'\uff08**\u5341\u4e09\u8282**\uff0c\u542b\u7b2c\u4e8c ~ \u516b\u62cd\u8fd4\u5de5\uff09\uff1b\u673a\u5236\u7ea7\u6559\u8bad\u89c1 PLAYBOOK **P3.39 ~ P3.44**\uff1b',
         u'\u4e8c\u00b7g \u5f15\u8a00'),
        (u'\u2467 \u7b2c\u516b\u62cd\uff08\u90b5\u5148\u751f 2026-10-01 12:3x',
         u'\n---\n\n## \u4e09\u3001r88 ~ r92 \u505a\u4e86\u4ec0\u4e48\uff08\u524d\u60c5\u63d0\u8981\uff09',
         u'\n' + HANDOFF_G8 + u'---\n\n## \u4e09\u3001r88 ~ r92 \u505a\u4e86\u4ec0\u4e48\uff08\u524d\u60c5\u63d0\u8981\uff09',
         u'\u8ffd\u52a0 \u2467 \u5c0f\u8282'),
    ], u'HANDOFF.md')

    # ---- 4
    patch(PAGES, [
        (None, u'2026-10-01 \u00b7 **\u5171\u4e03\u62cd**', u'2026-10-01 \u00b7 **\u5171\u516b\u62cd**', u'P3.11i \u6807\u9898'),
        (None, PAGES_QS_OLD, PAGES_QS_NEW, u'\u9010\u62cd\u8981\u70b9'),
        (u'**`.r107-stats` \u5c45\u4e2d**',
         u'\n\n**\u26a0 \u6539\u8fd9\u4e00\u5757\u4e4b\u524d\u5fc5\u770b**\n',
         u'\n' + PAGES_ROWS + u'\n**\u26a0 \u6539\u8fd9\u4e00\u5757\u4e4b\u524d\u5fc5\u770b**\n',
         u'\u56fa\u5b9a\u4e8b\u5b9e\u8868 +4 \u884c'),
    ], u'PAGES.md')

    # ---- 5
    append_once(PLAYBOOK, u'## P3.44 ', PB_BLOCK, u'PLAYBOOK.md \u00b7 P3.44')

    # ---- 6
    patch(REPO_MEM, [
        (u'\uff5c**P3.44=r107',
         u'\uff5c skill\uff08\u7528\u6237\u7ea7\uff09\uff1adesign-to-code-modular',
         MEM_IDX_INLINE + u'\uff5c skill\uff08\u7528\u6237\u7ea7\uff09\uff1adesign-to-code-modular',
         u'\u7d22\u5f15 \u00b7 \u8ffd\u52a0 P3.44'),
        (None, u'\uff08r107 \u00b7 \u5171\u4e03\u62cd\uff1a', u'\uff08r107 \u00b7 \u5171\u516b\u62cd\uff1a', u'\u7d22\u5f15 \u00b7 P3.11i \u5171\u4e03\u62cd\u2192\u516b\u62cd'),
        (None, u'\u53f3\u680f\u5b57\u4f53\u7edf\u4e00 + \u5168\u5c4f\u6309\u94ae\u968f\u53f3\u680f\u8054\u52a8**\uff09**\uff09\uff5c `YYYY-MM-DD.md` \u539f\u59cb\u65e5\u5fd7',
         u'\u53f3\u680f\u5b57\u4f53\u7edf\u4e00 + \u5168\u5c4f\u6309\u94ae\u968f\u53f3\u680f\u8054\u52a8** / **\u5168\u5c40\u5bbd\u5ea6\u4e0d\u8db3\u51fa\u7701\u7565\u53f7\uff08\u4e09\u7c7b\u5206\u6cbb\uff09+ \u53bb\u6389\u300c\u6298\u53e0\u6b64\u6587\u4ef6\u300d+ `.td-sum-h` 15px + diff path \u5c55\u5f00\u4e2d\u7c97 + diff path/rows \u5185 13px + \u7edf\u8ba1\u884c\u5c45\u4e2d**\uff09**\uff09\uff5c `YYYY-MM-DD.md` \u539f\u59cb\u65e5\u5fd7',
         u'\u7d22\u5f15 \u00b7 P3.11i \u62cd\u6b21\u63cf\u8ff0\u8865 ⑧'),
        (None, u'> **r107\uff082026-10-01 09:3x ~ 12:1x \u00b7 \u4f1a\u8bdd\u8be6\u60c5\u9875\u300c\u4fa7\u680f\u6a21\u5757\u6807\u7b7e\u5316\u300d= \u590d\u523b Codex \u53f3\u680f \u00b7 \u4e03\u62cd\uff09',
         u'> **r107\uff082026-10-01 09:3x ~ 12:4x \u00b7 \u4f1a\u8bdd\u8be6\u60c5\u9875\u300c\u4fa7\u680f\u6a21\u5757\u6807\u7b7e\u5316\u300d= \u590d\u523b Codex \u53f3\u680f \u00b7 \u516b\u62cd\uff09',
         u'r107 \u6bb5 \u00b7 \u6807\u9898\uff08\u4e03\u62cd\u2192\u516b\u62cd\uff09'),
        (None, u'\u2605 \u672c\u4ee3**\u4e03\u62cd**\uff08\u540c\u4e00\u4ee3\u3001`apply107.py` \u5c31\u5730\u8fd4\u5de5\u4e03\u6b21\u3001**\u59cb\u7ec8\u672a\u63d0\u4ea4**\uff09',
         u'\u2605 \u672c\u4ee3**\u516b\u62cd**\uff08\u540c\u4e00\u4ee3\u3001`apply107.py` \u5c31\u5730\u8fd4\u5de5\u516b\u6b21\u3001**\u59cb\u7ec8\u672a\u63d0\u4ea4**\uff09',
         u'r107 \u6bb5 \u00b7 \u4e03\u62cd\u2192\u516b\u62cd'),
        (None, u'\u2192 925776 \u2192 927464 Unicode \u5b57\u7b26**\uff08\u4e03\u62cd\u5408\u8ba1 **+128233**\uff09\uff1b',
         u'\u2192 925776 \u2192 927464 \u2192 930384 Unicode \u5b57\u7b26**\uff08\u516b\u62cd\u5408\u8ba1 **+131153**\uff09\uff1b',
         u'r107 \u6bb5 \u00b7 \u4ea7\u7269\u5b57\u7b26\u6570'),
        (None, u'> UTF-8 \u5b57\u8282\uff08LF \u5f52\u4e00\uff09**1015265** \uff5c \u5de5\u4f5c\u533a\u5b57\u8282\uff08CRLF\uff09**1022207** \uff5c LF `sha1 79aa4533761b`\uff1b',
         u'> UTF-8 \u5b57\u8282\uff08LF \u5f52\u4e00\uff09**1019883** \uff5c \u5de5\u4f5c\u533a\u5b57\u8282\uff08CRLF\uff09**1026880** \uff5c LF `sha1 c8b5e944e2de`\uff1b',
         u'r107 \u6bb5 \u00b7 \u4e09\u79cd\u53e3\u5f84'),
        (None, u'> **\u4e03\u67e5**\uff1a\u5e42\u7b49 \u2713\uff08**\u6bcf\u62cd\u8fde\u8dd1\u4e24\u904d**\uff09',
         u'> **\u516b\u67e5**\uff1a\u5e42\u7b49 \u2713\uff08**\u6bcf\u62cd\u8fde\u8dd1\u4e24\u904d**\uff09',
         u'r107 \u6bb5 \u00b7 \u4e03\u67e5\u2192\u516b\u67e5'),
        (None, u'\uff08`+2244 / \u22123` \u884c\uff09+ `M pages/avatar.html`\uff08`+1 / \u22121`\uff0c\u7b2c\u4e03\u62cd\u6587\u6848\uff09+ `?? mg-work/r107/`\u3002',
         u'\uff08`+2299 / \u22123` \u884c\uff09+ `M pages/avatar.html`\uff08`+1 / \u22121`\uff0c\u7b2c\u4e03\u62cd\u6587\u6848\uff09+ `?? mg-work/r107/`\u3002',
         u'r107 \u6bb5 \u00b7 \u6539\u52a8\u9762'),
        (None, u'\u2605\u2605 **\u65b0\u589e\u5b9a\u8bba\u89c1 PLAYBOOK P3.39 ~ P3.43**\uff1b\u5404\u62cd\u8981\u70b9\u89c1 **PAGES P3.11i\uff08\u5171\u4e03\u62cd\uff09**\uff1b\u9010\u6761\u5b9e\u6d4b\u89c1 **`mg-work/r107/acceptance.md`\uff08\u5341\u4e8c\u8282\uff09**\u3002',
         u'\u2605\u2605 **\u65b0\u589e\u5b9a\u8bba\u89c1 PLAYBOOK P3.39 ~ P3.44**\uff1b\u5404\u62cd\u8981\u70b9\u89c1 **PAGES P3.11i\uff08\u5171\u516b\u62cd\uff09**\uff1b\u9010\u6761\u5b9e\u6d4b\u89c1 **`mg-work/r107/acceptance.md`\uff08\u5341\u4e09\u8282\uff09**\u3002',
         u'r107 \u6bb5 \u00b7 \u5f15\u7528\u884c'),
        (u'> **\u7b2c\u516b\u62cd\uff08\u516d\u6761\uff09**',
         u'> \u26a0 **\u672c\u4ee3\u4e0d\u8981\u91cd\u8dd1 `apply106.py`**',
         MEM_R107_G8 + u'> \u26a0 **\u672c\u4ee3\u4e0d\u8981\u91cd\u8dd1 `apply106.py`**',
         u'r107 \u6bb5 \u00b7 \u8ffd\u52a0\u7b2c\u516b\u62cd\u5757'),
    ], u'MEMORY.md')

    # ---- 7
    patch(WS_MEM, [
        (u'38. \u2605\u2605 **\u300c\u5168\u5c40\u90fd\u8981\u51fa\u7701\u7565\u53f7\u300d',
         u'\n## \u4e8c\u3001Windows \u73af\u5883\u901f\u8bb0',
         u'\n' + WS_BLOCK.rstrip('\n') + u'\n## \u4e8c\u3001Windows \u73af\u5883\u901f\u8bb0',
         u'\u786c\u89c4\u5219 38~41'),
    ], u'WS_MEMORY.md')

    # ---- 8
    append_once(LOG_REPO, u'### \u7b2c\u516b\u62cd\uff08\u90b5\u5148\u751f 2026-10-01 12:3x', LOG_BLOCK, u'\u4ed3\u5e93\u65e5\u5fd7 \u00b7 \u7b2c\u516b\u62cd')
    append_once(LOG_WS, u'### \u7b2c\u516b\u62cd\uff08\u90b5\u5148\u751f 2026-10-01 12:3x', LOG_BLOCK, u'\u5de5\u4f5c\u533a\u65e5\u5fd7 \u00b7 \u7b2c\u516b\u62cd')

    print(u'\n-- \u5e94\u7528 %d \u9879 / \u8df3\u8fc7 %d \u9879 --' % (len(APPLIED), len(SKIPPED)))
    for s in APPLIED:
        print(u'   + ' + s)
    for s in SKIPPED:
        print(u'   = ' + s)


if __name__ == '__main__':
    main()
