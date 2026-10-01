# -*- coding: utf-8 -*-
"""r108 第十八拍（第七层补丁）—— 邵先生四条：

  ① **`td-mod-bar` 右端的「在系统打开」拆成两枚按钮**：`另存为` + `打开所在文件夹`。
     原一枚语义过载（既可能指另存、也可能指定位文件）⇒ 拆开并列。仍是纯静态演示（各给轻提示）。

  ② **去掉 `td-browse-bar` 栏的「最大化侧栏」按钮**。按钮移出后，`panel.js` 里整段
     「最大化 / 还原」变成**不可达代码**（`data-td-maxw` 全仓只有本文件读，无第二个消费者）
     ⇒ 整段删除（`freeW` / `maxPanelW` / `applyMaxW` / `storedPanelW` / `setMaxIcon` /
     `setMax` + 按钮 click + 分栏条 pointerdown + resize 两条监听），并清掉只为它声明的
     `DEF_PANEL / MIN_PANEL / MAIN_MIN / STORE_KEY`。

  ③ **修 `td-mod-body td-rv-body is-worddiff` 「不能滚动」**。实测（1440×900）：
     `.td-rv-body` 是 flex 纵列，卡片 `.td-diff` **没写 `flex`** ⇒ 吃默认 `flex: 0 1 auto`
     ⇒ 装不下时先**压扁卡片**（卡 1 实占 369px、内容实需 637px），而 `.td-diff{overflow:hidden}`
     又把压扁后的内容**裁掉** ⇒ ① `scrollHeight` 恒等于 `clientHeight`、容器**永远不滚**；
     ② 超出部分**永久看不见**。⇒ 卡片 `flex: none`，让内容正常溢出、容器的 `overflow:auto` 生效。

  ④ **把 `.td-mod-menu` 里的「摘要」放到第一项**（原顺序：审查 / 终端 / 浏览器 / 文件 / 摘要）。

★ 体位与硬规则：
  · r108 **仍未提交**（判据 `git status` 里 `conversation.html` 仍是 ` M`）⇒ **就地返工、不另起代数**，
    本拍作为 r108 的**第七层补丁**（l1~l6 之后）。
  · 硬规则 22「双层产物只能下→上改」⇒ 改序：
      1. `mg-work/r108/part108/_head.html`   ② 删最大化按钮 + ④ 摘要挪首位
         （★ `_head.html` 原是 **r107 的资产**，按「要改跨代资产 ⇒ 放本代同名覆盖件」规矩，
           先 `cp` 成 `part108/_head.html` 再改；`part107/_head.html` 一字不动）
      2. `mg-work/r108/part108/_mods.html`   ① 拆两枚按钮
      3. `mg-work/r108/part108/panel.css`    ③ 卡片不收缩 + l7 标记（接回 l6）
      4. `mg-work/r108/part108/panel.js`     ① 两枚处理器 + ② 删最大化整段 + 头注释
      5. `python mg-work/r108/ev/splice108.py`  → 重建 `part108/browse.html`
      6. `python mg-work/r108/apply108.py`      → 落 `pages/conversation.html`

★ 各层的 `mark` 是「后一层必须替前一层保住」的契约：本层把 `/* r108-l7 */` 插在
  `/* r108-l6 */` **之前**并把 l6 原样接回；l1~l6 的标记本层一个不碰（收尾有跨层兜底断言）。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
HEAD = os.path.join(P108, '_head.html')
MODS = os.path.join(P108, '_mods.html')
PCS = os.path.join(P108, 'panel.css')
PJS = os.path.join(P108, 'panel.js')

APPLIED = []
SKIPPED = []
STRICT = True


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark, strict=None):
    t, nl = rd(p)
    strict = STRICT if strict is None else strict
    if mark and mark in t:
        if strict and old in t:
            sys.exit('!! %s：mark 歧义 —— `old` 与 `mark` 同时存在 ⇒ mark 不是「改完才出现」的串\n'
                     '   mark=%r\n   old=%r' % (label, mark, old[:200]))
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:240]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


def erase_between(p, a, b, new, label, mark):
    """整段删除：[a 的开头 .. b 的开头) 换成 `new`。
    ⚠ 纯删除类改动的 mark 必须落在「删除后新出现的串」上 ⇒ 这里干脆让 `new` 自己带一条
      留痕注释（`mark` 取该注释里的唯一片段），天然满足「只有改完才存在」。"""
    t, nl = rd(p)
    if mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if t.count(a) != 1:
        sys.exit('!! %s：起点锚点命中 %d 次（应 1 次）\n   a=%r' % (label, t.count(a), a[:160]))
    if t.count(b) != 1:
        sys.exit('!! %s：终点锚点命中 %d 次（应 1 次）\n   b=%r' % (label, t.count(b), b[:160]))
    i0, i1 = t.index(a), t.index(b)
    if i0 >= i1:
        sys.exit('!! %s：起点在终点之后' % label)
    old = t[i0:i1]
    wr(p, t[:i0] + new + t[i1:], nl)
    APPLIED.append(label)
    print('   应用  %s（删 %d 字符 → 换 %d 字符）' % (label, len(old), len(new)))


# ================================================================================
# ② + ④  `_head.html`
# ================================================================================
def do_head():
    print('=== 1/4  _head.html（② 删最大化按钮 · ④ 摘要挪首位）===')
    t = rd(HEAD)[0]

    # ---- ④ 摘要挪到第一项 ------------------------------------------------------
    # ★★ 必须**一次性整块重排**（`old` = 原顺序的 5 行、`new` = 重排后的 5 行）。
    #    第一版写成「先摘掉那一行、再插到标题后」两步 —— 单跑没问题，**复跑直接 `mark` 歧义**：
    #    终态里 mark（标题紧跟摘要）与第 (a) 步的 `old`（摘要那一行）**同时存在** ⇒ 硬断言拦下。
    #    ⇒ 教训：拆成多步时，**中间态才成立的 mark 在终态必须消失**；做不到就别拆。
    ITEM_RX = re.compile(r'(?m)^      <button class="td-mm-item giencoder-dropdown-item" '
                         r'type="button" role="menuitem" data-td-open-mod="[a-z]+">.*$')
    items = ITEM_RX.findall(t)
    if len(items) != 5:
        sys.exit('!! ④ 菜单项应 5 项（实 %d）' % len(items))
    order = [re.search(r'data-td-open-mod="([a-z]+)"', x).group(1) for x in items]
    TITLE = '      <div class="td-mm-cap giencoder-menu-group-title">在侧栏打开</div>'
    # mark = 改后才成立的相邻关系：分组标题行**紧跟**摘要按钮
    ADJ = ('在侧栏打开</div>\n      <button class="td-mm-item giencoder-dropdown-item" '
           'type="button" role="menuitem" data-td-open-mod="summary">')
    if order == ['summary', 'review', 'terminal', 'browser', 'files']:
        SKIPPED.append('④「摘要」挪到第一项')
        print('   跳过  ④「摘要」挪到第一项（已应用）')
    else:
        if order != ['review', 'terminal', 'browser', 'files', 'summary']:
            sys.exit('!! ④ 菜单项顺序意外：%r' % (order,))
        by_mod = dict(zip(order, items))
        new_order = [by_mod[k] for k in ('summary', 'review', 'terminal', 'browser', 'files')]
        edit(HEAD, '\n'.join(items), '\n'.join(new_order),
             '④「摘要」挪到第一项（整块重排）', ADJ)

    # ---- ② 删「最大化侧栏」按钮 ------------------------------------------------
    MAXBTN_RX = (r'(?m)^      <button class="td-browse-ico" type="button" aria-label="最大化侧栏" '
                 r'title="最大化侧栏" aria-pressed="false" data-td-max="1">.*$\n')
    t2 = rd(HEAD)[0]
    mm = re.search(MAXBTN_RX, t2)
    if not mm:
        # 幂等：按钮已不在 ⇒ 只校验「删除后应形成的相邻关系」确实成立
        if ('<div class="td-browse-acts">\n'
            '      <button class="td-browse-ico" type="button" aria-label="收起侧栏"') in t2:
            SKIPPED.append('② 删「最大化侧栏」按钮')
            print('   跳过  ② 删「最大化侧栏」按钮（已应用）')
        else:
            sys.exit('!! ② 既找不到「最大化侧栏」按钮，也没有形成「收起侧栏紧跟标题栏动作组」的相邻关系')
    else:
        BTN_LINE = mm.group(0)
        # mark = 删除后新形成的相邻关系：`<div class="td-browse-acts">` 紧跟「收起侧栏」按钮
        edit(HEAD, BTN_LINE, '', '② 删「最大化侧栏」按钮',
             '<div class="td-browse-acts">\n'
             '      <button class="td-browse-ico" type="button" aria-label="收起侧栏"')


# ================================================================================
# ①  `_mods.html`：一枚 → 两枚
# ================================================================================
def do_mods():
    print('=== 2/4  _mods.html（① 拆两枚按钮）===')
    OLD = ('          <button class="td-prev-btn" type="button" data-td-prev-open="1">在系统打开</button>\n')
    NEW = (
        '          <!-- ★ r108-l7 ①（邵先生：把「在系统打开」拆成两个按钮）：\n'
        '               原一枚「在系统打开」语义过载 —— 分不清是「另存一份」还是「在文件管理器里\n'
        '               定位」。按邵先生给的命名拆成两枚并列按钮；仍是**静态演示**（各给一句轻提示），\n'
        '               不引入任何真实文件系统调用。 -->\n'
        '          <button class="td-prev-btn" type="button" data-td-prev-save="1">另存为</button>\n'
        '          <button class="td-prev-btn" type="button" data-td-prev-reveal="1">打开所在文件夹</button>\n'
    )
    edit(MODS, OLD, NEW, '①「在系统打开」拆成「另存为 / 打开所在文件夹」',
         'data-td-prev-save="1"')


# ================================================================================
# ③  `panel.css`：卡片不再被压扁 + l7 标记
# ================================================================================
def do_css():
    print('=== 3/4  panel.css（③ 卡片不收缩 + l7 标记）===')
    OLD = (
        '.td-rv-body {\n'
        '  display: flex; flex-direction: column; gap: 8px;\n'
        '  padding: 8px;\n'
        '}\n'
    )
    NEW = (
        '.td-rv-body {\n'
        '  display: flex; flex-direction: column; gap: 8px;\n'
        '  padding: 8px;\n'
        '}\n'
        '/* ★ r108-l7 ③（邵先生：「`td-mod-body td-rv-body is-worddiff` 容器不能滚动页面，需修复」）：\n'
        '   `.td-rv-body` 是 **flex 纵列**，而卡片 `.td-diff` **没写 `flex`** ⇒ 吃默认的\n'
        '   `flex: 0 1 auto`（可收缩）⇒ 装不下时浏览器**先压扁卡片**而不是让它溢出。\n'
        '   1440×900 实测（四张卡片全展开）：卡 1 实占 **369px**、内容实需 **637px**；\n'
        '   卡 2 实占 262 / 需 451 —— 而 `.td-diff { overflow: hidden }` 又把压扁后多出来的\n'
        '   部分**裁掉** ⇒ 两个后果：\n'
        '     ① `scrollHeight` 恒等于 `clientHeight`（369→637 全被吃掉）⇒ 容器**永远不滚**；\n'
        '     ② 被裁掉的那部分（合计约 489px）**永久看不见**，也没法滚出来。\n'
        '   ⇒ 让卡片不再收缩（`flex: none` = `0 0 auto`）：内容照原样溢出，\n'
        '     `.td-mod-body` 那条既有的 `overflow: auto` 才真正生效，滚动**留在容器内**。\n'
        '   ⚠ 整个祖先链本就是「定高 + overflow:hidden」（`.td-mod` / `.td-browse` / 外壳\n'
        '     `.h-dvh.overflow-hidden`）⇒ 修完**不会**把整页顶高（实测 `docOverflow = 0`）。\n'
        '   ⚠ 只命中审查模块的**直接子件**，不动其它 `.td-mod-body`（摘要 / 终端 / 浏览器 / 预览）。 */\n'
        '.td-rv-body > .td-diff { flex: none; }\n'
    )
    # ⚠★ mark 必须**逐字等于**注释里真实存在的那一段 —— 第一版写成 `/* r108-l7 ③`，
    #   而实际注释是 `/* ★ r108-l7 ③`（中间有个「★ 」）⇒ 判据永不命中 ⇒ **补丁被重复应用**
    #   （panel.css 里多出整整一份 799 字符的重复块，而当时的「存在性」断言照样通过）。
    #   ⇒ 教训②：「存在性」断言抓不到重复；同一条判据要写成 **count == 1**。
    #   ⚠ strict=False：本步的 `new` = `old`（原 `.td-rv-body{...}` 块）**原样接回** + 追加新规则
    #     ⇒ 复跑时 `old` 必然仍在，与 mark 同时命中会被误判「mark 不唯一」
    #     （与 l5 的「插在锚点前 + 把锚点接回」、l6 的 `.td-mod-menu{left}` 同一类豁免）。
    edit(PCS, OLD, NEW, '③ 卡片 flex: none（容器恢复可滚）', '/* ★ r108-l7 ③', strict=False)

    # l7 标记：插在 l6 之前，并把 l6 原样接回
    edit(PCS, '/* r108-l6 */\n', '/* r108-l7 */\n/* r108-l6 */\n',
         'l7 标记（接回 l6）', '/* r108-l7 */', strict=False)


# ================================================================================
# ① + ②  `panel.js`
# ================================================================================
def do_js():
    print('=== 4/4  panel.js（① 两枚处理器 · ② 删最大化整段）===')

    # ---- ① 「在系统打开」→ 两枚 -------------------------------------------------
    J1_OLD = (
        "  /* 面板工具条上的「在系统打开」—— 关闭改由页签自己的 `×`（`closeTab` 那段现有逻辑） */\n"
        "  if (prevPane) {\n"
        "    var prevOpenBtn = prevPane.querySelector('[data-td-prev-open]');\n"
        "    if (prevOpenBtn) prevOpenBtn.addEventListener('click', function () { say('已在系统应用中打开（视觉演示）'); });\n"
        "  }\n"
    )
    J1_NEW = (
        "  /* 面板工具条上的两枚动作 —— 关闭改由页签自己的 `×`（`closeTab` 那段现有逻辑）。\n"
        "     ★ r108-l7 ①（邵先生：把「在系统打开」拆成两个按钮）：原一枚语义过载 —— 分不清是\n"
        "       「另存一份」还是「在文件管理器里定位」⇒ 拆成「另存为」与「打开所在文件夹」两枚。\n"
        "       ⚠ 仍是**纯静态演示**（各给一句轻提示），不引入任何真实文件系统调用。 */\n"
        "  if (prevPane) {\n"
        "    var prevSaveBtn = prevPane.querySelector('[data-td-prev-save]');\n"
        "    if (prevSaveBtn) prevSaveBtn.addEventListener('click', function () { say('已另存为到本地（视觉演示）'); });\n"
        "    var prevRevealBtn = prevPane.querySelector('[data-td-prev-reveal]');\n"
        "    if (prevRevealBtn) prevRevealBtn.addEventListener('click', function () { say('已在文件管理器中定位该文件（视觉演示）'); });\n"
        "  }\n"
    )
    edit(PJS, J1_OLD, J1_NEW, '① 拆成「另存为 / 打开所在文件夹」两枚处理器',
         "var prevSaveBtn = prevPane.querySelector('[data-td-prev-save]');")

    # ---- ② 删「最大化 / 还原」整段 ---------------------------------------------
    MAX_HDR = '  /* ==================== 最大化 / 还原 ==================== */\n'
    RV_HDR = '  /* ==================== 审查模块 ==================== */\n'
    NEW = (
        '  /* ★ r108-l7 ②：这里原有「最大化 / 还原」**整段** —— `freeW()` / `maxPanelW()` /\n'
        '     `applyMaxW()` / `storedPanelW()` / `setMaxIcon()` / `setMax()`，加上按钮的 click\n'
        '     监听、分栏条上的 `pointerdown` 捕获监听、以及 `resize` 两条监听。\n'
        '     邵先生「把 `td-browse-bar` 栏的「最大化侧栏」按钮去掉」—— 按钮是**唯一入口** ⇒\n'
        '     整段立刻变成不可达代码（`setMax` 首行那句 `if (!maxBtn) return;` 之后再也走不到）。\n'
        '     ★ 判据支撑：`data-td-maxw` 全仓**只有本文件**读（已 grep 过 `pages/`、各 `part` 目录、\n'
        '       以及全部 css / js / py），删掉不会有第二个消费者落单。\n'
        '     ⚠ 宽度记忆（`--av-browse-w` + key `giencoder:r105-browse:v1`）的**拖拽与持久化**\n'
        '       一直归宿主 `ctrl-conv.js`，本段删掉不影响它。 */\n'
        '\n'
    )
    erase_between(PJS, MAX_HDR, RV_HDR, NEW, '② 删「最大化 / 还原」整段', '★ r108-l7 ②：这里原有')

    # ---- ② 头注释同步 -----------------------------------------------------------
    edit(PJS,
         '     ② 侧栏「最大化 / 还原」（复用宿主 --av-browse-w，自算 maxPanelW）\n',
         '     ② （★ r108-l7 ②：原「侧栏最大化 / 还原」已按邵先生要求整段删除，见下方留痕注释）\n',
         '② 头注释同步', '★ r108-l7 ②：原「侧栏最大化 / 还原」')

    # ---- ② 清掉只为它声明的宽度常量 --------------------------------------------
    edit(PJS,
         "  var STORE_KEY = 'giencoder:r105-browse:v1';   /* 与 ctrl-conv.js 同一个 key（宽度记忆） */\n"
         '  var DEF_PANEL = 641, MIN_PANEL = 561, MAIN_MIN = 380;\n',
         '  /* ⚠ 右栏宽度（`--av-browse-w`）与其记忆 key `giencoder:r105-browse:v1` 的**拖拽 / 持久化**\n'
         '     一直归宿主 `ctrl-conv.js`（它自算上下限）。\n'
         '     ★ r108-l7 ②：原先这里还声明 `DEF_PANEL / MIN_PANEL / MAIN_MIN / STORE_KEY` 供\n'
         '       「最大化 / 还原」自算宽度；该功能整段删除后它们已无消费者，一并清掉。 */\n',
         '② 清掉只为最大化声明的宽度常量', '★ r108-l7 ②：原先这里还声明')


# ================================================================================
# 跨层兜底断言
# ================================================================================
def verify():
    print()
    print('=== 跨层兜底断言 ===')
    h = rd(HEAD)[0]
    m = rd(MODS)[0]
    c = rd(PCS)[0]
    j = rd(PJS)[0]
    jcode = re.sub(r'/\*.*?\*/', '', j, flags=re.S)
    jcode = re.sub(r'(?m)^\s*//.*$', '', jcode)
    ccode = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    mcode = re.sub(r'<!--.*?-->', '', m, flags=re.S)
    bad = []

    # ① 判据
    if mcode.count('data-td-prev-open') != 0:
        bad.append('_mods.html：「在系统打开」那枚按钮仍有残留')
    for k in ('data-td-prev-save="1"', 'data-td-prev-reveal="1"'):
        if mcode.count(k) != 1:
            bad.append('_mods.html：%s 应恰好 1 处（实 %d）' % (k, mcode.count(k)))
    if mcode.count('class="td-prev-btn"') != 2:
        bad.append('_mods.html：.td-prev-btn 应恰好 2 枚（实 %d）' % mcode.count('class="td-prev-btn"'))
    if jcode.count('data-td-prev-open') != 0:
        bad.append('panel.js：data-td-prev-open 引用残留')
    for k in ('data-td-prev-save', 'data-td-prev-reveal'):
        if jcode.count(k) != 1:
            bad.append('panel.js：%s 应恰好 1 处（实 %d）' % (k, jcode.count(k)))

    # ② 判据
    if h.count('data-td-max') != 0:
        bad.append('_head.html：「最大化侧栏」按钮仍有残留')
    if h.count('aria-label="收起侧栏"') != 1:
        bad.append('_head.html：「收起侧栏」按钮应恰好 1 枚')
    for pat in (r'\bmaxBtn\b', r'\bsetMax\b', r'\bsetMaxIcon\b', r'\bapplyMaxW\b',
                r'\bmaxPanelW\b', r'\bfreeW\b', r'\bstoredPanelW\b', r'\bmaxPaths\b',
                r'\bICON_MIN\b', r'\bICON_MAX\b', r'\bMIN_PANEL\b', r'\bMAIN_MIN\b',
                r'\bDEF_PANEL\b', r'\bSTORE_KEY\b', r'data-td-max'):
        if re.search(pat, jcode):
            bad.append('panel.js：%s 残留（代码里，不是注释）' % pat)

    # ③ 判据（⚠ 写成 count == 1：只查「存在」抓不到「重复应用」——见上面那条 ★ 教训）
    if ccode.count('.td-rv-body > .td-diff { flex: none; }') != 1:
        bad.append('panel.css：`.td-rv-body > .td-diff { flex: none; }` 应恰好 1 处（实 %d）'
                   % ccode.count('.td-rv-body > .td-diff { flex: none; }'))
    if c.count('/* ★ r108-l7 ③') != 1:
        bad.append('panel.css：③ 的留痕注释应恰好 1 处（实 %d）' % c.count('/* ★ r108-l7 ③'))
    if c.count('/* r108-l7 */') != 1:
        bad.append('panel.css：`/* r108-l7 */` 标记应恰好 1 处（实 %d）' % c.count('/* r108-l7 */'))
    if j.count("var prevSaveBtn = prevPane.querySelector('[data-td-prev-save]');") != 1:
        bad.append('panel.js：① 的两枚处理器各应恰好 1 处')
    if j.count('★ r108-l7 ②：这里原有') != 1:
        bad.append('panel.js：② 的留痕注释应恰好 1 处')
    # ④ 判据
    order = re.findall(r'data-td-open-mod="([a-z]+)"', h)
    if order != ['summary', 'review', 'terminal', 'browser', 'files']:
        bad.append('_head.html：菜单项顺序应为 summary/review/terminal/browser/files（实 %r）' % (order,))
    if h.count('data-td-open-mod=') != 5:
        bad.append('_head.html：菜单项应恰好 5 项（实 %d）' % h.count('data-td-open-mod='))

    # 跨层标记存活
    marks = [
        (PCS, '/* r108-l2 */', 'l2'), (PCS, '/* r108-l3 */', 'l3'), (PCS, '/* r108-l4 */', 'l4'),
        (PCS, '/* r108-l5 */', 'l5'), (PCS, '/* r108-l6 */', 'l6'), (PCS, '/* r108-l7 */', 'l7'),
        (MODS, 'id="av-zd-status"', 'l2 · 面板静态 DOM'),
        (MODS, 'class="zd-menu giencoder-dropdown-popup zd-menu-branch"', 'l3 · 两枚下拉'),
        (MODS, 'data-zd-git="commit"', 'l3 · Git 三行'),
        (MODS, 'class="zd-cv"', 'l2 · 折叠箭头'),
        (PCS, '.zd-sec.is-closed .zd-sec-x { display: flex; }', 'l4 · trailing 仅折叠可见'),
        (PCS, '@keyframes zd-todo-spin {', 'l4 · loading 弧'),
        (MODS, 'id="av-browse-pane-preview"', 'l5 · 预览页签面板'),
        (MODS, 'data-td-art="1"', '① 产物行仍在'),
        (MODS, 'data-td-brw-act="more"', 'l6 · 浏览器只剩「更多」'),
        (PCS, '.td-tree { position: absolute; top: 44px;', 'l6 · 抽屉让开标题栏'),
        (PJS, "var PLACE_ABS = ['td-mod-menu', 'td-rv-menu'];", 'l6 · 定位白名单'),
        (PJS, "'已复制截图到剪贴板（视觉演示）'", 'l6 · 右键菜单那条'),
    ]
    for p, mk, label in marks:
        if mk not in rd(p)[0]:
            bad.append('%s：%s（在 %s 里找不到）' % (label, mk, os.path.basename(p)))

    # ★★★ 注释括号配平（本拍真踩）：第一版在注释正文里写了 `part*/` —— 那个 `*/`
    #     **提前闭合了块注释**，后面的注释正文被当成 JS 代码 ⇒ `check-syntax` 直接 FAIL
    #     （报在注释行上，看起来「不可能出错」）。与硬规则 6「CSS 注释禁嵌 `/* */`」同族。
    #     ⇒ 判据：`/*` 与 `*/` 计数必须相等（多出的那一个 `*/` 就是提前闭合的元凶）。
    for p, label in ((PJS, 'panel.js'), (PCS, 'panel.css')):
        s = rd(p)[0]
        if s.count('/*') != s.count('*/'):
            bad.append('%s：注释括号不配平（`/*` %d 个 / `*/` %d 个）—— 多半是注释正文里'
                       '出现了 `*/`' % (label, s.count('/*'), s.count('*/')))

    if bad:
        sys.exit('!! 跨层自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')
    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


def main():
    do_head()
    do_mods()
    do_css()
    do_js()
    verify()


if __name__ == '__main__':
    main()
