# -*- coding: utf-8 -*-
u"""r108 第十二拍收尾：把「diff 卡片化 + 文件树抽屉」同步进 5 份记忆文档。

范围（本代 🚫 未提交，故同步的是「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md      —— 首行 + 顶部「最新一拍」块 + 第一节 + 二·h 新节 + 六/七/八节
  2) .workbuddy/memory/PAGES.md        —— P3.11i 标题「共十一拍」→「共十二拍」+ ⑫ 要点 + 结构图 + 固定事实表
  3) .workbuddy/memory/PLAYBOOK.md     —— 追加 P3.48（第十二拍 · 三条新教训）
  4) .workbuddy/memory/MEMORY.md       —— r107 段标「已封板」+ 追加 r108 段
  5) 两份当日日志 2026-10-01.md（仓库内 + 工作区）—— 追加 r108 段

★ 幂等设计（照 doc107m.py）：**mark 一律 = new**（`new` 天然只可能「改后才存在」）。
  步骤 = 3 元组 `(old, new, sub)`；`old=None` 表示尾部追加。
用法： python ev/doc108n.py            # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
      python ev/doc108n.py --check    # 只校验锚点命中数（不写）
⚠ 本文件由 Write 落盘（UTF-8 LF）；被改的 5 份文件各自保留原行尾（rd/wr 处理）。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-01 19:4x'

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def patch(p, steps, label):
    """steps = [(old, new, sub)]；old=None ⇒ 尾部追加；mark 自动取 new。"""
    t, nl = rd(p)
    n0 = len(t)
    for old, new, sub in steps:
        mark = new                       # ★ mark == new（唯一来源，不手抄）
        if CHECK:
            if old is not None and t.count(old) != 1:
                BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, t.count(old)))
            continue
        if mark and mark in t:
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
R108_BLOCK = u"""> ⚠️ **最新一拍 = r108「diff 卡片化 + 文件树抽屉」**（第十二拍；**r107 已交付 `e9c9498` ⇒ 本代是新一代**，
> **新建 `mg-work/r108/apply108.py`**（由 `ev/make108.py` 从 apply107 做 **7 处精确替换**生成），
> `GENS` 摘除表扩到**六代**（r93/r101/r102/r106/r107/r108），注入块 id = `r108-conv-css` / `r108-conv-js`；
> ★★★ **nav 块继续沿用 `r106-nav-js` 不换名**（`NAV_TAG='r106'`）⇒ **base + 8 外壳页逐字节不变、只改 `conversation.html` 一页**）：
> ① **`.td-diff` 独立成一张张小卡片 → 已做**：`.td-rv-body` 改 `flex` 纵列 + `gap:8px` + `padding:8px`；
>   `.td-diff` = `1px --color-border-2` 描边 + `8px` 圆角 + `--color-bg-2` 底 + `overflow:hidden`
>   （让 `.td-diff-h:hover` 的底色被圆角裁住）；头 / 体之间补 `border-top: 1px --color-border-1`。
>   实测四张卡 `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`、卡间距 **`[8,8,8]`**。
> ② **「在文件树中定位」右侧新增「文件树」按钮 ⇒ 右侧弹文件树抽屉 → 已做**：
>   按钮 `data-td-rv-act="tree"`（folder-tree SVG，24 网格 / stroke 2 / 渲染 16px），插在「定位」**右紧邻**；
>   抽屉 `.td-tree[data-td-tree]`（`position:absolute; inset:0; z-index:35`；**下拉 30 < 抽屉 35 < 提交模态 40**）
>   = 遮罩 + 右侧 `min(296px, 86%)` 面板 + 头部（`.td-tree-h` 40px）+ 搜索 + `.td-tree-files`（10 行）。
>   开合 = `hidden` 属性 + `.is-open` 类（**先 `removeAttribute('hidden')` → `void offsetWidth` 强制 reflow → 再 `add('is-open')`**；
>   关 = 摘 `is-open` → **240ms 后**挂 `hidden`）。实测 `panelBox=[1135,49,296,842]`（右缘 1431 = 右栏右缘）；
>   **三条关闭路径全通**（遮罩 / Esc / 头部 ✕），**Esc 只关抽屉、不关侧栏**（裁决链：模态 → 抽屉 → 菜单）。
> ★★★ **本拍最关键的技术决定 —— 抽屉树用「独立类名 `td-tf*`」**：`ctrl-conv.js` 的
>   `pane = slot.querySelector('.td-browse')` 是**整个 aside**、`pane.querySelector('.td-browse-files')` **只绑第一棵**
>   ⇒ 若复用 `td-bf*` 会两边互相打架、抽屉里的行点了没反应。零干扰已实测：
>   抽屉里点 `Controls.tsx` ⇒ 抽屉 `active` 变，而「文件」模块那棵树 `filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**。
> 🔧 **途中排掉三处坑（两个真问题 + 一处探针假失败）**：
>   ① **「文件树」按钮会弹一个多余的「已执行」toast** —— `panel.js` 那条 `[data-td-rv-act]` 通用循环把它也吃了
>     ⇒ 在 `closeMenus(null)` 之后加 `if (kind === 'tree') return;`（**保留 closeMenus**、只跳过 toast）。
>   ② **`.td-tree-h` 被 `scan-flatten` 多报 1 条**（基线 2 → 3）—— 该规则有 `height: calc(40px*ratio)` 但体里没有
>     `var(--font-size-*)` ⇒ 会被 `apply88b.converge()` 压平 ⇒ 补 `font-size: var(--font-size-body-3)` 回到 2 条。
>   ③ **探针两处假失败（产品没问题）**：抽屉遮罩挡住工具条点击（想切并排视图要先关抽屉）+
>     短路表达式 `q() || fn().click()` 让「并排」根本没切过去。
> ★ **门禁四件套全绿**：幂等 ✓（`patch108l1.py` 第二遍「应用 0 / 跳过 6」；`apply108.py` 第二遍「已是目标态」）｜
>   `check-syntax.py pages/*.html` **10/10**｜`verify-design.py ./pages` 与 `vd-r107l2.txt` **逐字节相同**
>   （md5 `3dbf654337559509110899e48bef1b1c`，21882 字节 ⇒ 零新增、一处渐变都没引）｜
>   `scan-flatten.py part108/panel.css` 仍 **2 条**（`.td-mod-bar` / `.td-url`）。
> ★ 边界验证：并排视图 `isSplit=true` / 统一行 `display:none`；`--ui-fs=18` 杠杆 ⇒ 树行 **28 → 36**、头部 **40 → 51**；
>   窄档 620 ⇒ 面板仍 296（`min()` 的 `296px` 分支正确）。
> **产物**：`conversation.html` **958568 → 978614 字符（+20046）**，LF bytes **1078406** / 工作区 bytes **1086146** /
> **7741 行** / LF `sha1_lf 7a1be6be9b76`；`base.html` **472150 逐字节不变**；`git diff --numstat` = `248  3  pages/conversation.html`。
> 逐条实测见 `mg-work/r108/acceptance.md`（**七节**）；机制级教训见 PLAYBOOK **P3.48**；本页固定事实见 PAGES **P3.11i**。"""

R108_2H = u"""## 二·h ★★ r108（最新一拍 · 会话详情页「diff 卡片化 + 文件树抽屉」· 2026-10-01 19:4x 起，共**十二拍**）—— **新一代（r107 已交付 `e9c9498`），\U0001F6AB 未提交**

> 完整版见 `mg-work/r108/acceptance.md`（**七节**）；机制级教训见 PLAYBOOK **P3.48**；本页固定事实见 PAGES **P3.11i**。

**① 体位**：r107 **已交付 `e9c9498`** ⇒ **新建 `mg-work/r108/apply108.py`**（**不就地返工**），
由 **`ev/make108.py`** 从 `apply107.py` 做 **7 处精确替换**生成
（E1 标题 / E2 ×5 路径 / E2b ×2 段号 / E3 `GENS` 加第六代 / E4 `PART_DIRS` 加 `part108` / E5 注释目录名 / E6 docstring 加第十二拍块；
每处命中数断言，不符即 `sys.exit`）。`GENS` 扩成**六代**（r93/r101/r102/r106/r107/r108）。

**★★★ nav 块继续沿用 `r106-nav-js`（不换名）**：`GENS[-1] = ('r108','r108-conv-css','r108-conv-js','r106-nav-js')` + `NAV_TAG='r106'`
⇒ `base.html` 与 8 个外壳页**逐字节不变**，`git status` 只有 `conversation.html` 一个 ` M`。
⚠ **但 CSS / JS 两块都改了 ⇒ 必须换名 `r108-conv-css` / `r108-conv-js`**（否则「摘块」正则会连本代新内容一起摘掉）。

**② `PART_DIRS` 三级回落**：`(part108, part107, part105)` —— 本代只覆盖改过的三件
（`_mods.html` · `panel.css` · `panel.js`），`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 继续从 part107 / part105 取。

**③ 改动清单**

| 文件 | 改动 |
|---|---|
| `part108/_mods.html`（44246 → 52848 字节） | ① 工具条 `.td-mod-bar-acts` 里「在文件树中定位」**右紧邻**插 `data-td-rv-act="tree"` 按钮（folder-tree SVG）；② `</aside>` 前追加 `.td-tree[data-td-tree]` 抽屉（`.td-tree-scrim` / `.td-tree-panel` / `.td-tree-h` / `.td-browse-search` / `.td-tree-files` 10 行 `.td-tf*`） |
| `part108/panel.css`（1090 → 1196 行） | **新增第 18 节**（`/* r108-l1 */` 幂等标记）：18.1 diff 卡片化 · 18.2 文件树抽屉 · `.td-tf*` 行几何逐条对齐 `browse.css` 的 `.td-bf` |
| `part108/panel.js`（1335 → 1412 行） | 抽屉控制器（`treeRefresh()` / `treeShow()` / `treeHide()` + 点击委托 + document 点击收抽屉）；Esc 裁决链**加抽屉一层**（`if (treeOpen) { treeHide(); return; }` 插在 `modal` 之后、`menuOpen` 之前）；`[data-td-rv-act]` 通用循环加 `if (kind === 'tree') return;` |
| `ev/make108.py` · `ev/splice108.py` · `ev/patch108l1.py` | 生成器（7 处替换）/ 组装器（头部取 part107、新模块取 part108、Files 正文从 part105 剪出）/ 补丁（6 步，`mark = new` 幂等） |

**★★★ 独立类名隔离**：`ctrl-conv.js` 的 `pane = slot.querySelector('.td-browse')`（**整个 aside**）、
`rows = pane.querySelectorAll('.td-bf')`、`files = pane.querySelector('.td-browse-files')`（**只绑第一个**）
⇒ 抽屉树**必须用独立类名 `td-tf*`**，否则两边互相打架且抽屉里的行点了没反应。
★ 实测零干扰：抽屉里点 `Controls.tsx` ⇒ 抽屉 `drawerActive` 变，而「文件」模块那棵树 `filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**。
★ 抽屉树自身折叠：点 `games` ⇒ `visibleRows 10 → 3`，再点回 10。

**④ 真机实测（1440）**

* diff：四张卡 rect `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`，**卡间距 `[8,8,8]`**；
  卡描边 `1px solid rgb(229,229,229)` / 圆角 `8px` / 底 `rgb(255,255,255)` / `overflow:hidden`；
  头 / 体分隔线 `1px rgb(242,242,242)`；并排下折叠 ⇒ 卡高 **40**、`rowsDisplay:none`（**无残留分隔线**）。
* 按钮位置（`raw/m-1440-rvbar.png`）：工具条右端 = 复制 · **定位** · **文件树** · `⋯` · 提交⌄ · PR ⇒ **在「在文件树中定位」右紧邻** ✓。
* 抽屉：`hidden:true→false`、`is-open` 同步、`btnAria false→true`、**`panelBox=[1135,49,296,842]`**、`transform:none`、`scrim opacity 1`；
  与右栏 `paneBox=[791,48,641,844]` ⇒ 面板右缘 `1135+296 = 1431 = 791+641−1` = **紧贴右栏右缘** ✓。
* 关闭路径：点遮罩 ⇒ `hidden=true` + `paneOpen=true`（**侧栏没被误关**）；**Esc** ⇒ `hidden=true` / `paneOpen=true` / `paneHidden=false`（**只关抽屉**）；重开 ⇒ `panelBox` 不变（无残留污染）。
* 边界：`.td-tree-h` h=**40** fs=14px；`.td-tf` h=**28** fs=13px；并排 `isSplit=true` / 统一行 `display:none` / 并排行 `display:block` + `border-top:1px`；
  **`--ui-fs=18`** ⇒ 树行 **28 → 36**、头部 **40 → 51**、行字号 13 → 16.71px（**杠杆生效、没被压平**）；窄档 620 ⇒ 面板仍 296。

**⑤ 途中排掉三处坑**（详见 PLAYBOOK **P3.48**）

1. **「文件树」按钮弹多余「已执行」toast** —— `panel.js` 的 `[data-td-rv-act]` 通用循环（`say(ACT_TEXT[kind] || '已执行')`）把它也吃了 ⇒
   在 `closeMenus(null)` 之后加 `if (kind === 'tree') return;`（**保留 closeMenus**、只跳过 toast）。
   复测：点「文件树」⇒ `toastShown=false`；再点「在文件树中定位」⇒ `toastText="已在「文件」标签中定位该文件"` + `activeTab="文件"` ⇒ **老动作没被带坏** ✓。
2. **`.td-tree-h` 被 `scan-flatten` 多报 1 条（3 条 > 基线 2 条）** —— 该规则有 `height/min-height: calc(40px * var(--ui-fs-ratio))` 但体里
   **没有 `var(--font-size-*)`** ⇒ 会被 `apply88b.converge()` 压平成裸 40px ⇒ 补 `font-size: var(--font-size-body-3)`（`patch108l1.py` 的 `CSS_NEW` 同步）⇒ 回到 **2 条** ✓。
3. **探针两处假失败（产品代码没问题）** —— ① 抽屉开着时遮罩 `z-index:35` 挡住工具条点击 ⇒ 想点 `⋯` 切「并排视图」必须先关抽屉；
   ② 上一版探针写 `document.querySelector(...) || (fn)().click()` 这种**短路表达式** ⇒ 左侧 `querySelector` 命中（哪怕元素 hidden）就短路，
   「并排」根本没切过去。修：`probe108m6.sh` **先确认抽屉关闭**再点 ⇒ `isSplit=true` ✓。

**⑥ 产物与门禁**：`conversation.html` **958568 → 978614 字符**（+20046）；LF bytes **1078406** / 工作区 bytes **1086146** / **7741 行** / LF `sha1_lf 7a1be6be9b76`；
`base.html` **472150 逐字节不变**；`git diff --numstat` = `248  3  pages/conversation.html`。
幂等 ✓（`patch108l1.py` 第二遍「应用 0 / 跳过 6」；`apply108.py` 第二遍「已是目标态」）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜
`verify-design.py ./pages` 与 `mg-work/r107/ev/vd-r107l2.txt` **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`，21882 字节 ⇒ 零新增）｜
`scan-flatten.py part108/panel.css` ⇒ **2 条**（`.td-mod-bar` / `.td-url`）。

**⑦ 交接**：\U0001F6AB **未 commit / 未 push**（等邵先生显式发话）。提交时注意 `git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`（返工期的临时三源快照、不入库）。"""


# ============================================================ 1. HANDOFF.md
HOF = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')

HOF_STEPS = [
    # H1 首行「最后更新」+ 顶部「最新一拍」块上移（整段合并成一步，锚点唯一）
    (u'> 最后更新：2026-10-01 14:2x（**r106 已提交 `4d081ba`** + **r107 侧栏模块标签化已落地（十一拍累积）** '
     u'→ 四查全绿 + 五模块实测 + 多轮真 bug / 机制坑修复 → **已推送 `e9c9498`**（2026-10-01 14:2x 邵先生发话 commit and push））\n'
     u'> \u26A0\uFE0F **最新一拍 = r107「侧栏模块标签化」**',
     u'> 最后更新：%s（**r107 已推送 `e9c9498`** + **r108「diff 卡片化 + 文件树抽屉」已落地（第十二拍）** '
     u'→ 门禁四查全绿 + 真机实测（卡间距 [8,8,8] / 抽屉 panelBox [1135,49,296,842] / 两棵树零干扰）→ **\U0001F6AB 未提交**）\n'
     u'%s\n'
     u'> \u26A0\uFE0F **上一拍 = r107「侧栏模块标签化」（已推送 `e9c9498`）**' % (WHEN, R108_BLOCK),
     u'H1 首行 + 顶部块换成 r108'),

    # H2 第一节标题
    (u'★★ **r107（侧栏模块标签化）＝本代新产物，已推送 `e9c9498`**（2026-10-01 14:2x 邵先生发话 commit and push）。推送后工作区：',
     u'★★ **r108（diff 卡片化 + 文件树抽屉）＝本代新产物，\U0001F6AB 未提交**（%s，第十二拍）。工作区：' % WHEN,
     u'H2 第一节标题'),

    # H3 第一节工作区现状
    (u'**干净**（只剩 `?? mg-work/r107/ev/bak{7,8,9,10}/` 4 个返工备份目录，刻意留在库外）—— '
     u'**base.html 逐字节不变**（8 个外壳页里只有 avatar.html 因文案动 1 处，其余 7 页不动）。',
     u'**` M pages/conversation.html`（978614 字符）+ `?? mg-work/r108/` + `?? mg-work/r107/ev/bak{7,8,9,10}/`** —— '
     u'**base.html 逐字节不变**（8 个外壳页一字未动，nav 块沿用 `r106-nav-js`）。',
     u'H3 工作区现状'),

    # H4 不要重跑上一代
    (u'\u26A0 ★ **本代不要重跑 `apply106.py`**：它的 `GENS` 只有四代，会把「基线里仍残留 `r107-conv-css`」判成错误直接退出。\n'
     u'  退 r107 只需 `git checkout -- pages/conversation.html`（只改了这一页）。',
     u'\u26A0 ★ **本代不要重跑 `apply107.py`**：它的 `GENS` 只有五代，会把「基线里仍残留 `r108-conv-css`」判成错误直接退出。\n'
     u'  退 r108 只需 `git checkout -- pages/conversation.html`（只改了这一页）。',
     u'H4 不要重跑上一代'),

    # H5 顶部块里的「工作区」行（改成 r107 交付时的时点描述）
    (u'> 工作区：**干净**（仅剩 `?? mg-work/r107/ev/bak{7,8,9,10}/` 4 个返工备份目录，刻意留在库外）。已推送 `e9c9498`：`conversation.html` **958568 字符**。',
     u'> （r107 交付时）工作区：**干净**（仅剩 `?? mg-work/r107/ev/bak{7,8,9,10}/`）。已推送 `e9c9498`：`conversation.html` **958568 字符**。',
     u'H5 顶部块工作区行'),

    # H6 origin/main（顶部块内）
    (u'>   `origin/main` = **`e9c9498`**（本地 HEAD 已到 `e9c9498` = r107 代终态，**已推送**）。',
     u'>   `origin/main` = **`e9c9498`**（本地 HEAD 仍 `e9c9498`；**r108 十二拍已在工作区落地、\U0001F6AB 未提交**）。',
     u'H6 origin/main（顶部块）'),

    # H7 conversation.html 表行：补 r108 态
    (u'r107 十一拍见 `mg-work/r107/acceptance.md`（**十六节**） |',
     u'r107 十一拍见 `mg-work/r107/acceptance.md`（**十六节**）。★ **r108 态（\U0001F6AB 未提交）**：'
     u'958568 → **978614 字符**（第十二拍 +20046）；LF bytes 1078406 / 工作区 bytes 1086146 / 7741 行 / LF `sha1_lf 7a1be6be9b76`；'
     u'注入块 id `r108-conv-css` / `r108-conv-js`（**`r107-*` 及以前全 0**）；r108 十二拍见 `mg-work/r108/acceptance.md`（**七节**） |',
     u'H7 conversation 表行补 r108'),

    # H8 表格新增 mg-work/r108 行
    (u'| `docs/codex-refs/` + `docs/codex-sidepanel-research.md` |',
     u'| `mg-work/r108/` | **\U0001F6AB 未提交（第十二拍）**：`apply108.py`（**由 `ev/make108.py` 从 apply107 做 7 处精确替换生成**；GENS 六代、nav 沿用 `r106-nav-js`）/ `acceptance.md`（**七节**）/ **`part108/`**（只覆盖改过的三件：`_mods.html` 52848 · `panel.css` 1090 → 1196 行 · `panel.js` 1335 → 1412 行；`_head.html` / `ctrl-conv.js` / `browse.{css,js}` 三级回落取 part107 / part105）/ `ev/`（`make108.py` · `splice108.py` · `patch108l1.py` · `p108m.js` + `probe108m{,2,3,4,5,6}.sh` · `shots108m.sh` · `scan-flatten.py` · `vd-r108a/b.txt` · `m-raw.log` / `m2-raw.log`）/ `raw/`（`m-1440-{diff,diff-pane,diff-split,tree,tree-panel,tree-fold,rvbar}.png`）|\n'
     u'| `docs/codex-refs/` + `docs/codex-sidepanel-research.md` |',
     u'H8 表格增 r108 行'),

    # H9 origin/main 段（第 206 行）
    (u'`origin/main` @ **`e9c9498`**（**r106 六条 + Codex 右栏调研 + r107 十一拍已全部推送**，工作区**干净**；',
     u'`origin/main` @ **`e9c9498`**（**r106 六条 + Codex 右栏调研 + r107 十一拍已全部推送**；**r108 十二拍 \U0001F6AB 未提交**，工作区 ` M pages/conversation.html`；',
     u'H9 origin/main 段'),

    # H10 二·g 标题「最新一拍」→「上一拍」
    (u'## 二·g ★★ r107（最新一拍 · 会话详情页「侧栏模块标签化」＝复刻 Codex 右栏 · 2026-10-01 09:3x 起，共**十一拍**）',
     u'## 二·g ★★ r107（上一拍 · 会话详情页「侧栏模块标签化」＝复刻 Codex 右栏 · 2026-10-01 09:3x 起，共**十一拍**）',
     u'H10 二·g 标题降级'),

    # H11 新增 二·h 节（插在「## 三、」前）
    (u'---\n\n## 三、r88 ~ r92 做了什么（前情提要）',
     R108_2H + u'\n\n---\n\n## 三、r88 ~ r92 做了什么（前情提要）',
     u'H11 新增 二·h 节'),

    # H12 第七节：接手清单的补丁链
    (u'→ `mg-work/r102/apply102.py`\n   → **`mg-work/r107/apply107.py`**',
     u'→ `mg-work/r102/apply102.py`\n   → **`mg-work/r108/apply108.py`**',
     u'H12 接手清单补丁链'),

    # H13 第七节：多代同页说明
    (u'   \u26A0 ★★ **`apply102` / `apply106` / `apply107` 都作用于 `conversation.html`**：r102 与 r106 的块**已被 apply107 的 `GENS` 涵盖**，\n'
     u'     所以**只需跑 `apply107` 一条即可自愈到 r107 态**（历代块会被整块剥离再重注）。\n'
     u'     反过来**绝不要**跑到 r107 之后再跑 `apply106`（它只认四代 ⇒ 「基线残留 r107-conv-css」自检会直接退出）。',
     u'   \u26A0 ★★ **`apply102` / `apply106` / `apply107` / `apply108` 都作用于 `conversation.html`**：前几代的块**已被 apply108 的 `GENS` 涵盖**，\n'
     u'     所以**只需跑 `apply108` 一条即可自愈到 r108 态**（历代块会被整块剥离再重注）。\n'
     u'     反过来**绝不要**跑到 r108 之后再跑 `apply107`（它只认五代 ⇒ 「基线残留 r108-conv-css」自检会直接退出）。',
     u'H13 第七节多代说明'),

    # H14 第七节：组装件说明
    (u'   \u26A0 另：`part107/browse.html` 是**组装件** ⇒ 改 `_head.html` / `_mods.html` 后必须重跑 `ev/splice107.py` 再跑 `apply107.py`。',
     u'   \u26A0 另：`partNNN/browse.html` 是**组装件** ⇒ 改 `_head.html` / `_mods.html` 后必须重跑本代 `ev/spliceNNN.py` 再跑 `applyNNN.py`。\n'
     u'     本代 `part108/` 只覆盖改过的三件，其余从 `part107` / `part105` **三级回落**。',
     u'H14 第七节组装件说明'),

    # H15 第七节：现状时间戳 + r108 未提交
    (u'   ★ 现状（**2026-10-01 14:2x**）：`r86 ~ r100`（`d7e2151`）、**`r101`（`9f252e5`）**、\n'
     u'   **`r102~r105`（`87e2caa`）**、**`r106` 六条（`4d081ba`）**、**Codex 右栏调研（`f13b3bf`）**、\n'
     u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**。',
     u'   ★ 现状（**%s**）：`r86 ~ r100`（`d7e2151`）、**`r101`（`9f252e5`）**、\n'
     u'   **`r102~r105`（`87e2caa`）**、**`r106` 六条（`4d081ba`）**、**Codex 右栏调研（`f13b3bf`）**、\n'
     u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` 十二拍 \U0001F6AB 未提交**（工作区 ` M pages/conversation.html`）。' % WHEN,
     u'H15 第七节现状'),

    # H16 第七节：封板 → 就地返工
    (u'   ★ **r107 已交付 ⇒ 已封板**：若还要改**会话详情页 / 右栏**，**新建 `mg-work/r108/apply108.py`**\n'
     u'   （照抄 r107 的**五代** `GENS` 摘除表，扩成六代；并可继续沿用 `NAV_TAG=\'r106\'`，只要 nav 脚本仍未改）。\n'
     u'   **不要**再就地改 `apply107.py` —— 它已是交付态，改了会凭空产生与 `e9c9498` 的未提交差异。',
     u'   ★ **r108 尚在未提交期 ⇒ 可就地返工**：若还要改**会话详情页 / 右栏**，**直接改 `mg-work/r108/`**\n'
     u'   （改序 = `part108/_mods.html` → `ev/splice108.py` → `apply108.py`；⚠ `apply108.py` 由 `ev/make108.py` 生成、**禁手改**）。\n'
     u'   **不要**再把改动落回 `apply107.py` —— 它已是交付态（`e9c9498`）。\n'
     u'   ⚠ 若 r108 已交付后再改，则新建 `mg-work/r109/`（照抄六代 `GENS`、扩成七代；nav 脚本仍未改则可继续沿用 `NAV_TAG=\'r106\'`）。',
     u'H16 第七节封板→返工'),

    # H17 第八节：补 r108 回滚
    (u'# ★ r106 回滚（本代 · 首选：脚本自带 --revert）',
     u'# ★ r108 回滚（本代 · 只改了一页 ⇒ 一行即退（推荐））\n'
     u'git checkout -- pages/conversation.html\n'
     u'# ★ r106 回滚（首选：脚本自带 --revert）',
     u'H17 第八节回滚'),
]

# ============================================================ 2. PAGES.md
PAG = os.path.join(REPO, '.workbuddy', 'memory', 'PAGES.md')

PAG_STEPS = [
    # P1 标题：共十一拍 → 共十二拍
    (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 · 复刻 Codex 右栏 · 2026-10-01 · **共十一拍**）',
     u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二拍** · 复刻 Codex 右栏 · 2026-10-01 · **共十二拍**）',
     u'P1 标题'),

    # P2 补丁指针
    (u'> 补丁 = `mg-work/r107/apply107.py`；设计依据 = `docs/codex-sidepanel-research.md` + `docs/codex-refs/`。',
     u'> 补丁 = **`mg-work/r108/apply108.py`**（\U0001F6AB 未提交 · 第十二拍；前身 `mg-work/r107/apply107.py` 已推送 `e9c9498`）；'
     u'设计依据 = `docs/codex-sidepanel-research.md` + `docs/codex-refs/`。',
     u'P2 补丁指针'),

    # P3 追加 ⑫ 要点
    (u'> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五** / **十六**节）。',
     u'> **⑫（r108 第十二拍）`td-diff` 独立成小卡片（`1px` 描边 + `8px` 圆角 + `--color-bg-2` 底 + 容器 `gap:8px`）/ '
     u'「在文件树中定位」右侧新增「文件树」按钮 ⇒ 右侧弹**文件树抽屉**（`.td-tree` · `z-index:35` · 独立类名 `td-tf*` · Esc 算一层）**。\n'
     u'> （详见 `mg-work/r107/acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二 / **十三** / **十四** / **十五** / **十六**节；'
     u'r108 = `mg-work/r108/acceptance.md` 七节）。',
     u'P3 追加 ⑫ 要点'),

    # P4 结构图补 .td-tree
    (u'      └ section.td-mod.td-sum     [data-td-pane="summary"]  ← 摘要（任务侧栏：摘要 / 计划 / 来源 / 产物）\n```',
     u'      ├ section.td-mod.td-sum     [data-td-pane="summary"]  ← 摘要（任务侧栏：摘要 / 计划 / 来源 / 产物）\n'
     u'      └ div.td-tree[data-td-tree]   ← ★ r108：文件树抽屉（`z-index:35`；`.td-tree-panel` `min(296px,86%)` + '
     u'`.td-tree-files` 内 10 行 `.td-tf*`，类名与「文件」模块的 `.td-bf*` **刻意分离**）\n```',
     u'P4 结构图补 .td-tree'),

    # P5 固定事实表增三行（插在「地址栏激活态 / 浮条色」行之后）
    (u'| **地址栏激活态 / 浮条色** | ★ **第十一拍 ①②**：`.td-url-pill:focus-within`（底色转白 + `inset 0 0 0 1px` 主色 + '
     u'外 `0 0 0 2px` 浅主色环，`transition 120ms`）· `.td-selbar .giencoder-btn { color: var(--color-text-1) }`（DS `-btn-text` 默认主色蓝） |',
     u'| **地址栏激活态 / 浮条色** | ★ **第十一拍 ①②**：`.td-url-pill:focus-within`（底色转白 + `inset 0 0 0 1px` 主色 + '
     u'外 `0 0 0 2px` 浅主色环，`transition 120ms`）· `.td-selbar .giencoder-btn { color: var(--color-text-1) }`（DS `-btn-text` 默认主色蓝） |\n'
     u'| **diff 独立卡片** | ★★ **r108 ①**：`.td-rv-body { display:flex; flex-direction:column; gap:8px; padding:8px }` + '
     u'`.td-diff { border:1px solid var(--color-border-2); border-radius:8px; background:var(--color-bg-2); overflow:hidden }` + '
     u'`.td-diff-rows { border-top:1px solid var(--color-border-1) }`。`overflow:hidden` 让 `.td-diff-h:hover` 底色被圆角裁住；'
     u'`border-top` 不会双线（折叠态 `-rows` 本就 `display:none`，统一 / 并排两个 `-rows` 同刻只有一个可见）。'
     u'实测四张卡 `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`、**卡间距 `[8,8,8]`**；'
     u'描边 `1px rgb(229,229,229)` / 圆角 `8px` / 底 `rgb(255,255,255)`；并排折叠 ⇒ 卡高 **40**、`rowsDisplay:none` |\n'
     u'| **文件树抽屉** | ★★ **r108 ②**：按钮 `[data-td-rv-act="tree"]`（folder-tree SVG，24 网格 / stroke 2 / 渲染 16px，'
     u'插在「在文件树中定位」**右紧邻**）+ `.td-tree[data-td-tree]`（`position:absolute; inset:0; z-index:35`；'
     u'**右栏下拉 30 < 抽屉 35 < 提交模态 40**）。开合 = `hidden` 属性 + `.is-open` 类（`removeAttribute(\'hidden\')` → '
     u'`void offsetWidth` **强制 reflow** → `add(\'is-open\')`；关 = 摘 `is-open` → **240ms（过渡 220ms）后**挂 `hidden`）。'
     u'`min(296px, 86%)` 面板 ⇒ 实测 **`panelBox=[1135,49,296,842]`**（右缘 1431 = `paneBox` 791+641−1）；'
     u'**Esc 只关抽屉、不关侧栏**（裁决链：模态 → 抽屉 → 菜单）|\n'
     u'| **抽屉树独立类名** | ★★★ **r108 最关键的决定**：`ctrl-conv.js` 的 `pane = slot.querySelector(\'.td-browse\')` 是**整个 aside**、'
     u'`pane.querySelector(\'.td-browse-files\')` **只绑第一棵**（`querySelectorAll(\'.td-bf\')` 会扫到抽屉树）⇒ 抽屉树**必须用独立类名 `td-tf*`**'
     u'（行 `.td-tf` / 箭头 `.td-tf-arrow` / 图标 `.td-tf-ico` / 名称 `.td-tf-name`；`.td-tf.is-dir` 的 `padding-left` 与 `.td-bf.is-dir` 同口径），'
     u'否则两边互相打架、抽屉里的行点了没反应。实测：抽屉里点 `Controls.tsx` ⇒ 抽屉 `active` 变，而「文件」模块那棵树 '
     u'`filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10 |',
     u'P5 固定事实表增三行'),

    # P6 必看清单增 17/18
    (u'    改完必须**在窄档复量**：1440 全绿不代表 1280 / 1100 也全绿（第六拍两条都是窄档才暴露）。',
     u'    改完必须**在窄档复量**：1440 全绿不代表 1280 / 1100 也全绿（第六拍两条都是窄档才暴露）。\n'
     u'17. ★★★ **给右栏加「与既有控件同构」的新件 ⇒ 一律换独立类名**（r108）：`ctrl-conv.js` 的 `pane` 是**整个 `aside.td-browse`**、'
     u'`.td-browse-files` 用 `querySelector` **只绑第一棵** ⇒ 抽屉树用 `td-tf*` 才不打架'
     u'（判据 = 操作抽屉后老模块的 `active` / `rows` / `hidden` 计数**一字未变**）。\n'
     u'18. ★★ **覆盖层会挡住它自己的触发器** —— 抽屉 `z-index:35` 的遮罩铺满面板 ⇒ 探针里想点工具条上的 `⋯` **必须先关抽屉**'
     u'（否则点到遮罩、把抽屉关掉），否则会把「切并排视图失败」误判成 bug。\n'
     u'19. ★★ **带派生高度的新规则必须补 `var(--font-size-*)`** —— `.td-tree-h` 有 `height:calc(40px*ratio)` 但体里无 token '
     u'⇒ 被 `apply88b.converge()` 压平、`scan-flatten` 多报 1 条 ⇒ 补 `font-size: var(--font-size-body-3)` 回基线 2 条。',
     u'P6 必看清单增 17/18/19'),
]

# ============================================================ 3. PLAYBOOK.md
PBK = os.path.join(REPO, '.workbuddy', 'memory', 'PLAYBOOK.md')

PBK_TAIL = u"""
## P3.48 ★★ r108 第十二拍（两条 · %s 邵先生）—— ★ 三条新教训

**① ★★★ 给既有控制器「加一个同构控件」⇒ 一律换独立类名（否则两边互相打架）**
* 症状：新增的「文件树抽屉」若复用既有树的行类名，抽屉里的行**点了没反应**、且会让原模块的选中态乱跳。
* 根因：`ctrl-conv.js` 的控制器作用域 = `pane = slot.querySelector('.td-browse')`（**整个 `aside`**，不是某一棵树），
  而取子树用的是 `pane.querySelector('.td-browse-files')` —— `querySelector` **只返回第一个**（还有 `pane.querySelectorAll('.td-bf')` 会扫到抽屉树）。
* ★ 配方：新增同构件**换一套独立类名**（本拍 = 抽屉树 `td-tf*`，与「文件」模块的 `td-bf*` 完全分离）。
  **判据 = 在抽屉里操作之后，老模块的「选中项 / 行数 / 折叠数」计数一字未变**
  （本站 `filesActive` / `filesRows 28` / `filesHidden 9`）。
* ⚠ 同族：**先数一遍 `document.querySelectorAll('.cls').length`** —— `> 1` 就是撞车
  （r107 的 `td-term` 也是这个指纹：`querySelector('.td-term')` 取到外层 section）。

**② ★★ 覆盖层会挡住「它自己的触发器」——探针里必须先关掉再点**
* 症状：想点工具条上的 `⋯` 切「并排视图」，结果点到的是抽屉的**遮罩**（把抽屉关掉了），读数变成 `isSplit:false`
  ⇒ 误判「并排没生效」。
* 根因：抽屉 `z-index:35` 的 `.td-tree-scrim` 铺满整个面板 —— **开着抽屉时，面板里任何按钮都点不到**。
* ★ 正解：探针**先确认目标弹层已关闭**（`el.hidden === true`）再点它外面的按钮；
  ⚠ 顺便：别写 `querySelector(a) || (fn)().click()` 这种**短路表达式** —— 左侧命中（哪怕元素 `hidden`）就短路，动作根本没执行
  （本站「并排」两次都没切过去就是这个）。

**③ ★★ 给「派生高度的抽屉头」补 `font-size` token（否则被 `converge()` 压平、门禁多报一条）**
* `.td-tree-h` 声明了 `height/min-height: calc(40px * var(--ui-fs-ratio))`，但规则体里**没有 `var(--font-size-*)`**
  ⇒ `apply88b.converge()` 先 unscale 还原成裸 px、又因体里没 token 而不再重派生 ⇒ **声明被永久压平**。
* ★ 判据：`mg-work/rNN/ev/scan-flatten.py <css>` 的条数**多出 1**（本站基线 2 条 —— `.td-mod-bar` / `.td-url`）。
  修法 = 给该规则补任意一条 `var(--font-size-*)`（本拍补 `font-size: var(--font-size-body-3)`）。
* ⚠ 与硬规则 9 同源；**只在默认 `--ui-fs=14` 下量发现不了**（`calc(Npx × 1) = Npx`）⇒ 判据要看 `--ui-fs=18`。

★ **体位**：r107 **已交付** ⇒ 新建 `mg-work/r108/apply108.py`（`ev/make108.py` 从 apply107 做 **7 处精确替换**）；
`GENS` **六代**；★★★ **nav 块继续沿用 `r106-nav-js`（`NAV_TAG='r106'`）** ⇒ `base.html` + 8 页逐字节不变、`git status` 只一个 ` M`。
★ **CSS / JS 两块都改了 ⇒ 必须换名** `r108-conv-css` / `r108-conv-js`
（沿用同一代名会让「摘块」正则把本代新内容**一起摘掉**）。
★ `PART_DIRS` **三级回落**（`part108` → `part107` → `part105`）⇒ 本代只覆盖改过的三件。
★ 改序（下→上）：`part108/_mods.html` → `ev/splice108.py` → `apply108.py`；⚠ `browse.html` 是 splice 的产物、不是手改对象。
产物 `958568 → 978614` 字符（第十二拍 **+20046**）；`+248 / −3` 行；门禁四绿；
`scan-flatten` 仍 **2 条**；`verify-design` 与上轮**逐字节同**（md5 `3dbf654337559509110899e48bef1b1c`）。
""" % WHEN

PBK_STEPS = [
    (None, PBK_TAIL, u'PB1 追加 P3.48'),
]

# ============================================================ 4. 仓库 MEMORY.md
MEM = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')

MEM_STEPS = [
    # M1 r107 段标「已封板」
    (u'—— **已推送 `e9c9498`**（新一代，承接 r106 `4d081ba`；2026-10-01 14:2x 邵先生发话）**：',
     u'—— **已推送 `e9c9498`**（**已封板**；新一代，承接 r106 `4d081ba`；2026-10-01 14:2x 邵先生发话）**：',
     u'M1 r107 段标已封板'),

    # M2 追加 r108 段
    (None, u"""
> **r108（%s · 会话详情页「diff 卡片化 + 文件树抽屉」· **第十二拍**）—— \U0001F6AB 未提交**（新一代，承接 r107 `e9c9498`）：
> ★ **体位**：r107 **已交付** ⇒ **新建 `mg-work/r108/apply108.py`**（`ev/make108.py` 从 apply107 做 **7 处精确替换**）；
> `GENS` = **六代**（r93/r101/r102/r106/r107/r108）；`PART_DIRS` = `part108` → `part107` → `part105` **三级回落**
> （本代只覆盖 `_mods.html` / `panel.css` / `panel.js` 三件）。
> ★★★ **nav 块继续沿用 `r106-nav-js`（不换名）** ⇒ `base.html` + 8 外壳页**逐字节不变**，`git status` 只有 ` M pages/conversation.html`。
> ⚠ **但 CSS / JS 两块都改了 ⇒ 换名 `r108-conv-css` / `r108-conv-js`**（沿用同代名会把新内容一起摘掉）。
> **两条** = ① **`.td-diff` 独立成卡片**（`.td-rv-body` 改 flex 纵列 + `gap:8px` + `padding:8px`；
> `.td-diff` = 1px 描边 + 8px 圆角 + `--color-bg-2` 底 + `overflow:hidden`；头/体补 `border-top: 1px --color-border-1`）
> ⇒ 实测四张卡卡间距 **`[8,8,8]`**；
> ② **「在文件树中定位」右侧加「文件树」按钮 + 右侧文件树抽屉**（`data-td-rv-act="tree"` · `.td-tree` `z-index:35` ·
> 遮罩 + `min(296px,86%%)` 面板 + `.td-tree-files` 10 行 · 开合 = `hidden` + `.is-open`
> （`removeAttribute` → `void offsetWidth` → `add`）· 关 = 摘类后 **240ms** 挂 `hidden`）
> ⇒ 实测 `panelBox=[1135,49,296,842]`（右缘贴右栏右缘）、**Esc 只关抽屉不关侧栏**。
> ★★★ **本拍最关键的技术决定 —— 抽屉树用独立类名 `td-tf*`**：`ctrl-conv.js` 的 `pane` 是**整个 aside**、
> `.td-browse-files` 用 `querySelector` **只绑第一棵** ⇒ 复用 `td-bf*` 会打架（抽屉里的行点了没反应）；
> 零干扰已实测（抽屉点文件后「文件」模块 `filesActive` / `filesRows 28` / `filesHidden 9` 一字未变）。
> \U0001F527 三处坑 = ① 「文件树」按钮被 `[data-td-rv-act]` 通用循环弹多余 toast（加 `if (kind === 'tree') return`，**保留 closeMenus**）；
> ② `.td-tree-h` 被 `scan-flatten` 多报 1 条（派生高度规则缺 `var(--font-size-*)` ⇒ 被 `converge()` 压平 ⇒ 补 token 回 2 条）；
> ③ 探针两处假失败（遮罩挡住自己的触发器 / `||` 短路表达式让动作没执行）。
> **产物**：`958568 → 978614` 字符（第十二拍 +20046）；LF bytes 1078406 / 工作区 1086146 / 7741 行 / LF `sha1_lf 7a1be6be9b76`；
> `base.html` **472150 逐字节不变**；`git diff --numstat` = `248  3`。
> **门禁四绿**：幂等 ✓｜`check-syntax` 10/10｜`verify-design` 与 `vd-r107l2.txt` **逐字节同**
> （md5 `3dbf654337559509110899e48bef1b1c`）｜`scan-flatten` 仍 **2 条**。
> ★★ **新增定论见 PLAYBOOK P3.48**；各拍要点见 **PAGES P3.11i（共十二拍）**；逐条实测见 **`mg-work/r108/acceptance.md`（七节）**。
> ⚠ **本代不要重跑 `apply107.py`**（GENS 只有五代 ⇒ 「基线残留 `r108-conv-css`」自检直接退出）；
> 退 r108 = `git checkout -- pages/conversation.html`。
> \U0001F6AB 未 commit / 未 push；提交时 `git reset -q -- mg-work/r107/ev/bak{7,8,9,10}/`。
""" % WHEN, u'M2 追加 r108 段'),
]

# ============================================================ 5. 两份当日日志
LOG_REPO = os.path.join(REPO, '.workbuddy', 'memory', '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')

LOG_NOTE = u"""
### r108（第十二拍 · %s 邵先生 · \U0001F6AB 未提交）

**需求**（逐字）：「1、"td-diff"要独立成一个个的小卡片；2、需要在"在文件树中定位"按钮的右边再加一个"文件树"的图标按钮，
点击有会在右侧弹出一个文件数的抽屉；」（「文件数」按上下文判定为「文件树」。）

**体位**：r107 **已交付 `e9c9498`** ⇒ 按硬规则**新建 `mg-work/r108/apply108.py`**（不就地返工）。
`ev/make108.py` 从 `apply107.py` 做 **7 处精确替换**生成（3628 行 / 189273 字符）；`GENS` 扩成**六代**；
★★★ **nav 块继续沿用 `r106-nav-js`（`NAV_TAG='r106'`）** ⇒ **base + 8 外壳页逐字节不变**；
⚠ **CSS / JS 两块都改了 ⇒ 换名 `r108-conv-css` / `r108-conv-js`**。
`PART_DIRS` = `part108` → `part107` → `part105` 三级回落（只覆盖 `_mods.html` / `panel.css` / `panel.js`）。
改序（下→上）：`part108/_mods.html` → `ev/splice108.py` → `apply108.py`。

* **① `.td-diff` 独立成卡片**：`.td-rv-body { display:flex; flex-direction:column; gap:8px; padding:8px }`；
  `.td-diff { border:1px solid var(--color-border-2); border-radius:8px; background:var(--color-bg-2); overflow:hidden }`；
  `.td-diff-rows { border-top:1px solid var(--color-border-1) }`。`overflow:hidden` 是为了让 `.td-diff-h:hover` 底色被圆角裁住；
  `border-top` 不会双线（折叠态 `-rows` 本就 `display:none`，统一 / 并排两个 `-rows` 同刻只有一个可见）。
  实测：四张卡 `[800,142,623,299] / [800,449,623,213] / [800,670,623,40] / [800,718,623,40]`，**卡间距 `[8,8,8]`**；
  描边 `1px rgb(229,229,229)` / 圆角 `8px` / 底 `rgb(255,255,255)`；并排折叠 ⇒ 卡高 40、`rowsDisplay:none`。
* **② 文件树按钮 + 抽屉**：工具条 `.td-mod-bar-acts` 里「在文件树中定位」**右紧邻**插 `data-td-rv-act="tree"`
  （folder-tree SVG，24 网格 / stroke 2 / 渲染 16px）；`</aside>` 前追加 `.td-tree[data-td-tree]`
  （`position:absolute; inset:0; z-index:35`）= 遮罩 + 右侧 `min(296px,86%%)` 面板 + 头部 40px + 搜索 + `.td-tree-files`（10 行）。
  开合 = `hidden` 属性 + `.is-open` 类（`removeAttribute('hidden')` → **`void offsetWidth` 强制 reflow** → `add('is-open')`；
  关 = 摘 `is-open` → **240ms 后**挂 `hidden`）。z-index：**下拉 30 < 抽屉 35 < 提交模态 40**；Esc 裁决链同序（模态 → 抽屉 → 菜单）。
  实测：`panelBox=[1135,49,296,842]`（右缘 1431 = `paneBox` 791+641−1）、`transform:none`、`scrim opacity 1`；
  点遮罩 / Esc / 头部 ✕ 三条关闭路径全通，**Esc 只关抽屉不关侧栏**；重开 `panelBox` 不变。
* ★★★ **抽屉树用独立类名 `td-tf*`**：`ctrl-conv.js` 的 `pane = slot.querySelector('.td-browse')` 是**整个 aside**、
  `pane.querySelector('.td-browse-files')` **只绑第一棵** ⇒ 复用 `td-bf*` 会打架。零干扰实测：抽屉里点 `Controls.tsx`
  ⇒ 抽屉 `active` 变，而「文件」模块 `filesActive` / `filesRows 28` / `filesHidden 9` **一字未变**；抽屉树自身折叠 `games` ⇒ 行 10 → 3 → 10。
* \U0001F527 三处坑：① 「文件树」按钮被 `[data-td-rv-act]` 通用循环弹多余「已执行」toast ⇒ 在 `closeMenus(null)` 之后加 `if (kind === 'tree') return;`（**保留 closeMenus**）；
  ② `.td-tree-h` 有 `height:calc(40px*ratio)` 但体里没 `var(--font-size-*)` ⇒ 被 `converge()` 压平、`scan-flatten` 多报 1 条 ⇒ 补 `font-size: var(--font-size-body-3)` 回 2 条；
  ③ 探针两处假失败（产品没问题）：抽屉遮罩挡住工具条点击（改前先关抽屉）+ `q() || fn().click()` 短路表达式让「并排」没切过去。
* **边界**：`.td-tree-h` h=40 fs=14 · `.td-tf` h=28 fs=13 · 并排 `isSplit=true` / 统一行 `display:none` / 并排行 `display:block` + `border-top:1px` ·
  **`--ui-fs=18`** ⇒ 树行 28 → **36**、头部 40 → **51**、行字号 13 → 16.71px（杠杆生效）；窄档 620 ⇒ 面板仍 296。

**门禁**：幂等 ✓（`patch108l1.py` 第二遍「应用 0 / 跳过 6」；`apply108.py` 第二遍「已是目标态」）/ `check-syntax` **10/10** /
`verify-design` 与 `vd-r107l2.txt` **逐字节同**（md5 `3dbf654337559509110899e48bef1b1c`，21882 字节，零新增、一处渐变都没引）/
`scan-flatten part108/panel.css` 仍 **2 条**（`.td-mod-bar` / `.td-url`）。
**产物**：`conversation.html` 958568 → **978614** 字符（+20046；LF bytes 1078406 / 工作区 1086146 / 7741 行 / LF `sha1_lf 7a1be6be9b76`）；
`base.html` 472150 逐字节不变；`git diff --numstat` = `248  3  pages/conversation.html`。
**探针** `ev/p108m.js` + `ev/probe108m{,2,3,4,5,6}.sh` → `ev/m-raw.log` / `m2-raw.log`；**补丁** `ev/patch108l1.py`（6 步）。
\U0001F6AB 未 commit / 未 push。
""" % WHEN

LOG_STEPS = [
    (None, LOG_NOTE, u'L1 日志追加'),
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