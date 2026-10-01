# -*- coding: utf-8 -*-
"""r108 第十七拍（第六层补丁）—— 邵先生四条：

  ① **修 `+` 菜单的定位漂移**。标签栏里那枚 `+`（`[data-td-add]`）弹出的
     `.td-mod-menu` 一直吃的是基类 CSS 里写死的 `left: 64px`（相对 `.td-browse-bar`），
     而 `+` 的 x **随页签数量浮动** ⇒ 页签一多就脱钩。1440 实测：3 枚页签时
     `+` 左缘 **1074**、菜单左缘 **856** ⇒ **dx = −218px**。
     ⇒ 把 `.td-mod-menu` 也纳入 `panel.js` 的 `placeRv()`（原本它被那句
       `!menu.classList.contains('td-rv-menu')` 显式放行）。

  ② **删掉浏览器工具条的三枚图标按钮**（截图到剪贴板 / 缩放 / 发送页面到对话）。
     · `_mods.html` 里三枚 `data-td-brw-act="shot|zoom|send"` 整块移除（`more` 保留）。
     · 配套死代码一并清：`panel.js` 的 `BRW_TEXT` 三条 + `shotFlash()` 及其调用；
       `panel.css` 的 18-② 快门（`.td-brw.is-shot::after` + `@keyframes td-shot-flash`）
       与只为快门存在的 `.td-mod.td-brw { position: relative }`。
     · ⚠ 右键菜单里那条「截图到剪贴板」（`ctxForBrw`）**不是**工具条图标按钮 ⇒ 按
       「不得改动不必涉及的模块」保留，但它原来靠 `sb.click()` 借工具条的力 ⇒ 改成直接
       给轻提示，免留一个指向已删元素的死引用。

  ③ **文件树抽屉的蒙层要让开标题栏**。`.td-tree` 原为 `inset: 0` ⇒ 铺满整条 `.td-browse`
     （1440 实测：`tree.top = bar.top = 49`，标题栏被半透明遮罩盖住）。邵先生要求
     「把标题栏 `td-browse-bar` 留出来」⇒ 改成从标题栏下方起（`top: 44px`）。

  ④ **把 diff 里的代码加多、加长**（便于演示观察）。给两张展开着的卡片
     （`pages/conversation.html` / `mg-work/r107/part107/panel.css`）的统一视图与并排视图
     各补一批真实行 —— 统一视图补 17 + 12 行，并排视图补 11 + 6 行。

改序（只能下→上，硬规则 22）：
    1. `mg-work/r108/part108/_mods.html`   ② 删三枚按钮 + ④ 补 diff 行
    2. `mg-work/r108/part108/panel.css`    ① 注释 + ② 删快门 + ③ 抽屉让位 + l6 标记
    3. `mg-work/r108/part108/panel.js`     ① `placeRv` 白名单 + ② 删 `shotFlash`/`BRW_TEXT`
    4. `python mg-work/r108/ev/splice108.py`  → 重建 `part108/browse.html`（_mods.html 变了）
    5. `python mg-work/r108/apply108.py`      → 落 `pages/conversation.html`

★ 为什么另起一层（l6）而不是就地改 l1~l5：r108 未提交 ⇒ **不另起代数**，但在代内分层。
  ★★ 各层的 `mark` 是「**后一层必须替前一层保住**」的契约：本层把 `/* r108-l6 */` 插在
     `/* r108-l5 */` **之前**、并把 l5 标记**原样接回**；l1~l5 的标记本层一个不碰
     （收尾有跨层兜底断言）。

幂等判据：每处都带 `mark`（**只有改完之后才存在的串**）；两处删除类改动（三枚按钮 / 快门
          整块）把 `mark` 落在「删除后新形成的**连续**串」上 —— 三枚按钮那处用
          「标注按钮收尾 + 更多按钮开头」这个**改前被三行隔开、改后才相邻**的组合。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
MODS = os.path.join(P108, '_mods.html')
PCS = os.path.join(P108, 'panel.css')
PJS = os.path.join(P108, 'panel.js')

APPLIED = []
SKIPPED = []
# ★ 打开「mark 歧义」硬断言（本层只有末尾那条「插在锚点前 + 接回锚点」是合法例外）
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
        # ★★ 「mark 歧义」硬断言：`mark` 的语义是**只有改完才存在**。
        if strict and old in t:
            sys.exit('!! %s：mark 歧义 —— `old` 与 `mark` 同时存在 ⇒ mark 不是「改完才出现」的串\n'
                     '   mark=%r\n   old=%r' % (label, mark, old[:160]))
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:220]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


# ================================================================================
# ④ 的构件：两张卡片的补行
#   · 统一视图 = `.td-dr`（`<i class="td-dr-no">旧</i><i class="td-dr-nn">新</i>`）
#   · 并排视图 = `.td-dsc`（左右各一个 `.td-dsc-c` 单元格；行号沿用现有口径写在 `td-dr-no`）
#   ⚠ 内容里的 `<` `>` 一律写成 `&lt;` `&gt;`（与既有行同口径，否则会被浏览器当标签解析）
# ================================================================================
def dr_add(nn, text):
    return ('            <div class="td-dr is-add"><i class="td-dr-no"></i>'
            '<i class="td-dr-nn">%s</i><span class="td-dr-t">+%s</span></div>' % (nn, text))


def dsc_add(nn, text):
    return ('            <div class="td-dsc is-add"><span class="td-dsc-c"></span>'
            '<span class="td-dsc-c"><i class="td-dr-no">%s</i>'
            '<span class="td-dr-t">+%s</span></span></div>' % (nn, text))


# ---- 卡片 1（pages/conversation.html）：统一视图 +17 行 -------------------------
C1_ROWS = [
    (92,  '       &lt;div class="td-browse-tab is-active" data-td-mod="review" role="tab" aria-selected="false"&gt;'),
    (93,  '         &lt;span class="td-tab-ico"&gt;&lt;svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"&gt;…&lt;/svg&gt;&lt;/span&gt;'),
    (94,  '         &lt;span class="td-tab-name"&gt;审查&lt;/span&gt;'),
    (95,  '         &lt;button class="td-tab-x" type="button" aria-label="关闭审查"&gt;&lt;svg viewBox="0 0 24 24" aria-hidden="true"&gt;…&lt;/svg&gt;&lt;/button&gt;'),
    (96,  '       &lt;/div&gt;'),
    (97,  '       &lt;div class="td-browse-tab" data-td-mod="terminal" role="tab" aria-selected="false"&gt;'),
    (98,  '         &lt;span class="td-tab-ico"&gt;&lt;svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"&gt;…&lt;/svg&gt;&lt;/span&gt;'),
    (99,  '         &lt;span class="td-tab-name"&gt;终端&lt;/span&gt;'),
    (100, '       &lt;/div&gt;'),
    (101, '       &lt;div class="td-browse-tab" data-td-mod="browser" role="tab" aria-selected="false"&gt;'),
    (102, '         &lt;span class="td-tab-name"&gt;浏览器&lt;/span&gt;'),
    (103, '       &lt;/div&gt;'),
    (104, '     &lt;/div&gt;'),
    (105, '     &lt;div class="td-browse-acts"&gt;'),
    (106, '       &lt;button class="td-browse-ico" type="button" aria-label="最大化" data-td-max="1"&gt;…&lt;/button&gt;'),
    (107, '       &lt;button class="td-browse-ico" type="button" aria-label="收起侧栏" data-td-close="1"&gt;…&lt;/button&gt;'),
    (108, '     &lt;/div&gt;'),
]

# ---- 卡片 1：并排视图 +11 行 ---------------------------------------------------
C1_SPLIT = [
    (92,  '       &lt;div class="td-browse-tab is-active" data-td-mod="review" role="tab"&gt;'),
    (93,  '         &lt;span class="td-tab-name"&gt;审查&lt;/span&gt;'),
    (94,  '       &lt;/div&gt;'),
    (95,  '       &lt;div class="td-browse-tab" data-td-mod="terminal" role="tab"&gt;'),
    (96,  '         &lt;span class="td-tab-name"&gt;终端&lt;/span&gt;'),
    (97,  '       &lt;/div&gt;'),
    (98,  '       &lt;div class="td-browse-tab" data-td-mod="browser" role="tab"&gt;'),
    (99,  '         &lt;span class="td-tab-name"&gt;浏览器&lt;/span&gt;'),
    (100, '       &lt;/div&gt;'),
    (101, '     &lt;/div&gt;'),
    (102, '     &lt;div class="td-browse-acts"&gt;'),
]

# ---- 卡片 2（mg-work/r107/part107/panel.css）：统一视图 +12 行 ----------------
#   ⚠ CSS 文本不进 HTML 转义（它是纯文本节点，`{ } ;` 原样显示才是 diff 的样子）
C2_ROWS = [
    (4,  '.td-browse-bar { padding: 0 8px; gap: 4px; position: relative; }'),
    (5,  '.td-browse-tab { height: 28px; border-radius: 6px; padding: 0 4px 0 8px; }'),
    (6,  '.td-browse-tab:hover { background: var(--color-fill-1); color: var(--color-text-1); }'),
    (7,  '.td-browse-tab.is-active { background: var(--color-fill-2); color: var(--color-text-1); }'),
    (8,  '.td-tab-x { display: inline-flex; width: 18px; height: 18px; opacity: 0; }'),
    (9,  '.td-browse-tab:hover .td-tab-x { opacity: 1; }'),
    (10, '.td-mod { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }'),
    (11, '.td-mod-bar { flex: none; min-height: 40px; padding: 6px 12px; border-bottom: 1px solid var(--color-border-1); }'),
    (12, '.td-mod-bar-acts { margin-left: auto; display: flex; align-items: center; gap: 4px; }'),
    (13, '.td-mod-body { flex: 1 1 auto; min-height: 0; overflow: auto; }'),
    (14, '.td-rv-body { display: flex; flex-direction: column; gap: 8px; padding: 8px; }'),
    (15, '.zd-host { position: absolute; top: 44px; right: 16px; display: flex; justify-content: flex-end; }'),
]

# ---- 卡片 2：并排视图 +6 行 ---------------------------------------------------
C2_SPLIT = [
    (4,  '.td-browse-bar { padding: 0 8px; gap: 4px; }'),
    (5,  '.td-browse-tab { height: 28px; border-radius: 6px; }'),
    (6,  '.td-browse-tab:hover { background: var(--color-fill-1); }'),
    (7,  '.td-mod { display: flex; flex-direction: column; overflow: hidden; }'),
    (8,  '.td-mod-bar { min-height: 40px; padding: 6px 12px; }'),
    (9,  '.td-rv-body { display: flex; flex-direction: column; gap: 8px; }'),
]


def main():
    # ---------------------------------------------------------------- ② _mods.html
    print('=== 1/3  _mods.html ===')
    # ★ 删除类改动的 mark：三枚按钮删掉后，「标注按钮的收尾」与「更多按钮的开头」才相邻。
    BTN_OLD = (
        '        <button class="td-url-annot" type="button" aria-pressed="false" data-td-annot="1">'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M20 15a2 2 0 0 1-2 2H8l-4 3V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2Z"/>'
        '<path d="M9 9h6"/><path d="M9 13h4"/></svg><span>标注</span></button>\n'
        '        <button class="td-browse-ico" type="button" aria-label="截图到剪贴板" title="截图到剪贴板" '
        'data-td-brw-act="shot"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M3 8.5h3.2l1.6-2.3h8.4l1.6 2.3H21a1 1 0 0 1 1 1v8.5a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1'
        'V9.5a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13.5" r="3.2"/></svg></button>\n'
        '        <button class="td-browse-ico" type="button" aria-label="缩放" title="缩放" '
        'data-td-brw-act="zoom"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/><path d="M11 8v6"/>'
        '<path d="M8 11h6"/></svg></button>\n'
        '        <button class="td-browse-ico" type="button" aria-label="发送页面到对话" title="发送页面到对话" '
        'data-td-brw-act="send"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M4 19h16"/></svg></button>\n'
        '        <button class="td-browse-ico" type="button" aria-label="更多"'
    )
    BTN_NEW = (
        '        <button class="td-url-annot" type="button" aria-pressed="false" data-td-annot="1">'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M20 15a2 2 0 0 1-2 2H8l-4 3V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2Z"/>'
        '<path d="M9 9h6"/><path d="M9 13h4"/></svg><span>标注</span></button>\n'
        '        <!-- ★ r108-l6 ②：这里原有三枚图标按钮（截图到剪贴板 / 缩放 / 发送页面到对话），\n'
        '             按邵先生「不需要，请去掉」整块移除；配套的 JS（`BRW_TEXT` 三条 + `shotFlash()`）\n'
        '             与 CSS（18-② 快门）已一并清掉。右端的「更多」保留。 -->\n'
        '        <button class="td-browse-ico" type="button" aria-label="更多"'
    )
    edit(MODS, BTN_OLD, BTN_NEW, '② 删三枚图标按钮（shot / zoom / send）',
         'r108-l6 ②：这里原有三枚图标按钮')

    # ---- ④-a 卡片 1 · 统一视图 ------------------------------------------------
    A_OLD = (
        '            <div class="td-dr is-add"><i class="td-dr-no"></i><i class="td-dr-nn">91</i>'
        '<span class="td-dr-t">+     &lt;/div&gt;</span></div>\n'
        '            <button class="td-diff-more" type="button" data-td-more="1">⋯ 折叠 46 行未改动</button>'
    )
    A_NEW = (
        '            <div class="td-dr is-add"><i class="td-dr-no"></i><i class="td-dr-nn">91</i>'
        '<span class="td-dr-t">+     &lt;/div&gt;</span></div>\n'
        + '\n'.join(dr_add(nn, tx) for nn, tx in C1_ROWS) + '\n'
        '            <button class="td-diff-more" type="button" data-td-more="1">⋯ 折叠 46 行未改动</button>'
    )
    edit(MODS, A_OLD, A_NEW, '④-a 卡片 1 统一视图 +%d 行' % len(C1_ROWS),
         '&lt;span class="td-tab-name"&gt;浏览器&lt;/span&gt;')

    # ---- ④-b 卡片 1 · 并排视图 ------------------------------------------------
    B_OLD = (
        '            <div class="td-dsc is-add"><span class="td-dsc-c"></span><span class="td-dsc-c">'
        '<i class="td-dr-no">90</i><span class="td-dr-t">+       &lt;div class="td-browse-tab'
        '<mark class="td-dr-wd"> is-active</mark>"&gt;…&lt;/div&gt;</span></span></div>\n'
        '            <button class="td-diff-more" type="button" data-td-more="1">⋯ 折叠 46 行未改动</button>'
    )
    B_NEW = (
        '            <div class="td-dsc is-add"><span class="td-dsc-c"></span><span class="td-dsc-c">'
        '<i class="td-dr-no">90</i><span class="td-dr-t">+       &lt;div class="td-browse-tab'
        '<mark class="td-dr-wd"> is-active</mark>"&gt;…&lt;/div&gt;</span></span></div>\n'
        + '\n'.join(dsc_add(nn, tx) for nn, tx in C1_SPLIT) + '\n'
        '            <button class="td-diff-more" type="button" data-td-more="1">⋯ 折叠 46 行未改动</button>'
    )
    edit(MODS, B_OLD, B_NEW, '④-b 卡片 1 并排视图 +%d 行' % len(C1_SPLIT),
         '&lt;span class="td-tab-name"&gt;浏览器&lt;/span&gt;</span></span></div>')

    # ---- ④-c 卡片 2 · 统一视图 ------------------------------------------------
    C_OLD = (
        '            <div class="td-dr is-add"><i class="td-dr-no"></i><i class="td-dr-nn">3</i>'
        '<span class="td-dr-t">+.td-mod[hidden] { display: none; }</span></div>\n'
        '          </div>'
    )
    C_NEW = (
        '            <div class="td-dr is-add"><i class="td-dr-no"></i><i class="td-dr-nn">3</i>'
        '<span class="td-dr-t">+.td-mod[hidden] { display: none; }</span></div>\n'
        + '\n'.join(dr_add(nn, tx) for nn, tx in C2_ROWS) + '\n'
        '          </div>'
    )
    edit(MODS, C_OLD, C_NEW, '④-c 卡片 2 统一视图 +%d 行' % len(C2_ROWS),
         '.td-rv-body { display: flex; flex-direction: column; gap: 8px; padding: 8px; }')

    # ---- ④-d 卡片 2 · 并排视图 ------------------------------------------------
    D_OLD = (
        '            <div class="td-dsc is-add"><span class="td-dsc-c"></span><span class="td-dsc-c">'
        '<i class="td-dr-no">2</i><span class="td-dr-t">+.td-browse-tabs { '
        '<mark class="td-dr-wd">min-width: 0;</mark> }</span></span></div>\n'
        '          </div>'
    )
    D_NEW = (
        '            <div class="td-dsc is-add"><span class="td-dsc-c"></span><span class="td-dsc-c">'
        '<i class="td-dr-no">2</i><span class="td-dr-t">+.td-browse-tabs { '
        '<mark class="td-dr-wd">min-width: 0;</mark> }</span></span></div>\n'
        + '\n'.join(dsc_add(nn, tx) for nn, tx in C2_SPLIT) + '\n'
        '          </div>'
    )
    edit(MODS, D_OLD, D_NEW, '④-d 卡片 2 并排视图 +%d 行' % len(C2_SPLIT),
         '.td-mod { display: flex; flex-direction: column; overflow: hidden; }')

    # ---------------------------------------------------------------- ①③② panel.css
    print('=== 2/3  panel.css ===')
    # ① 注释：`.td-mod-menu` 不再「不动」
    C1_OLD = ('   `.td-mod-menu` 的触发器（`+`）就在标签栏里 ⇒ `top: 42px`（= 标签栏 44px 下方）'
              '天然是「按钮下方」，不动。\n')
    C1_NEW = ('   ★★ r108-l6 ①（邵先生报「位置没跟着触发器走」）：`.td-mod-menu` 的触发器\n'
              '   （`+` = `[data-td-add]`）**确实在标签栏里**，但它的**水平位置随页签数量浮动**，\n'
              '   而基类把它钉死在 `left: 64px`（= 只有 1 枚页签时的近似值）⇒ 页签一多就脱钩。\n'
              '   1440 实测：3 枚页签时 `+` 左缘 **1074**、菜单左缘 **856** ⇒ **dx = −218px**。\n'
              '   ⇒ 本类也交给 `panel.js` 的 `placeRv()` 现场摆位（与下面三枚同一套算法）；\n'
              '      垂直恰好仍是 42px（bar 高 44、按钮 28 居中 ⇒ 按钮下缘在栏内 36px，+6 = 42），\n'
              '      故 `top` 的**兜底值**不动。\n')
    edit(PCS, C1_OLD, C1_NEW, '① 注释：菜单纳入 placeRv',
         'r108-l6 ①（邵先生报「位置没跟着触发器走」）')

    C2_OLD = '.td-mod-menu { left: 64px; right: auto; }\n'
    C2_NEW = ('/* `left` 只是 JS 未生效时的兜底（默认字号下「只有 1 枚页签」的近似值）——\n'
              '   真位置由 `panel.js` 的 `placeRv()` 按 `+` 的实际几何现场写入行内样式（r108-l6 ①）。 */\n'
              '.td-mod-menu { left: 64px; right: auto; }\n')
    # ⚠ 这条 old 会被 new **原样保留**（只是在上方补一段注释）⇒ 复跑时 old 仍命中，
    #   属「合法例外」，显式 strict=False。
    edit(PCS, C2_OLD, C2_NEW, '① `.td-mod-menu` 的 left 降级为兜底',
         '`left` 只是 JS 未生效时的兜底', strict=False)

    # ② 删 18-② 快门
    S_OLD = (
        '/* 18-② 浏览器「截图」快门 —— 闪整个模块（`.td-view` 是滚动容器，覆盖层会跟着内容滚走） */\n'
        '.td-mod.td-brw { position: relative; }\n'
        '.td-brw.is-shot::after {\n'
        "  content: ''; position: absolute; inset: 0; z-index: 5;\n"
        '  background: var(--color-bg-2); opacity: 0;\n'
        '  pointer-events: none;\n'
        '  animation: td-shot-flash 260ms ease;\n'
        '}\n'
        '@keyframes td-shot-flash { 0% { opacity: .9; } 100% { opacity: 0; } }\n'
    )
    S_NEW = (
        '/* 18-② 原「浏览器截图快门」已删（r108-l6 ②）——\n'
        '   邵先生「截图到剪贴板 / 缩放 / 发送页面到对话这三枚图标按钮不需要」⇒ 工具条那三枚\n'
        '   连同快门白闪（`.td-brw.is-shot::after` + `@keyframes td-shot-flash`）一并移除。\n'
        '   ⚠ 原先只为快门写的 `.td-mod.td-brw { position: relative }` 也一并删掉：模块内唯一的\n'
        '     绝对定位子件 `.td-elnote` 是 `view.appendChild()` 挂进 `.td-view` 的，而 `.td-view`\n'
        '     自己有 `position: relative`（第 498 行）⇒ 这条没有消费者了。\n'
        '   ⚠ 想复刻：`git show <第十七拍交付前>:mg-work/r108/part108/panel.css` 取回本段即可。 */\n'
    )
    edit(PCS, S_OLD, S_NEW, '② 删 18-② 快门白闪', '18-② 原「浏览器截图快门」已删（r108-l6 ②）')

    # 18 节头注释里那条「②」标注过时
    H_OLD = '      ② 一键截图到剪贴板（官方）—— 补地址栏那枚相机按钮 + 快门白闪\n'
    H_NEW = ('      ② 一键截图到剪贴板（官方）—— 曾落地为「地址栏相机按钮 + 快门白闪」；'
             '**第十七拍已移除**（见 18-②）\n')
    edit(PCS, H_OLD, H_NEW, '② 18 节头注释同步', '**第十七拍已移除**（见 18-②）')

    # ③ 抽屉让开标题栏
    T_OLD = '.td-tree { position: absolute; inset: 0; z-index: 35; }\n'
    T_NEW = (
        '/* ★ r108-l6 ③：`inset: 0` → 从**标题栏下方**起（邵先生「文件树的蒙层要把标题栏留出来」）。\n'
        '   44 = `.td-browse-bar` 的实测高：它来自跨代资产 browse.css 的写死值 40（实测 44），\n'
        '   且 `--ui-fs` = 14 / 18 两档量出来都是 44 ⇒ **不随字号杠杆变** ⇒ 用裸 px 而非\n'
        '   `calc(44px * var(--ui-fs-ratio))`（那条会被 apply88b.converge 的 unscale 压平成裸 44px，\n'
        '   反而绕一圈）。\n'
        '   ⚠ `.td-tree` 是 `.td-browse`（position: relative）的**直接子级** ⇒ 它的「0」就是侧栏\n'
        '     padding box 顶，正是标题栏顶上（1440 实测：`tree.top = bar.top = 49`）⇒ 原样压住标题栏。\n'
        '   ⚠ 不写 `inset: 44px 0 0 0` 简写：`inset` 的「值顺序」在四值时是 上/右/下/左，可读性差，\n'
        '     本工程一贯写四向长手（与 `.td-tree-panel` 同口径）。 */\n'
        '.td-tree { position: absolute; top: 44px; left: 0; right: 0; bottom: 0; z-index: 35; }\n'
    )
    edit(PCS, T_OLD, T_NEW, '③ 抽屉从标题栏下方起', 'top: 44px; left: 0; right: 0; bottom: 0; z-index: 35;')

    # l6 标记（插在 l5 之前，并把 l5 原样接回）
    edit(PCS, '/* r108-l5 */\n', '/* r108-l6 */\n/* r108-l5 */\n',
         'l6 标记（接回 l5）', '/* r108-l6 */', strict=False)

    # ---------------------------------------------------------------- ①② panel.js
    print('=== 3/3  panel.js ===')
    J1_OLD = (
        '     ⚠ `.td-mod-menu` 走同一条 `toggleMenu`，但它不带 `.td-rv-menu` ⇒ 这里直接放行，\n'
        '       保持它原来的 CSS 落位（`top: 42px; left: 64px`）不动。 */\n'
    )
    J1_NEW = (
        '     ★★ r108-l6 ①：`.td-mod-menu` 原先走同一条 `toggleMenu` 却被这里「直接放行」，吃的是\n'
        '       基类 CSS 里写死的 `left: 64px` ⇒ 它的触发器 `+` 一随页签数量右移，两者就脱钩\n'
        '       （1440 三枚页签实测 dx = −218px）。⇒ 白名单改成 `PLACE_ABS`，两类都按几何现场摆位。\n'
        '       ⚠ 别用「排除法」：`.td-ctxmenu`（`position: fixed` 跟指针）与 `.zd-menu`（在\n'
        '         `.zd-host` 里、另一个包含块）都不能吃这套算法，必须显式列白名单。 */\n'
    )
    edit(PJS, J1_OLD, J1_NEW, '① 注释：白名单说明', 'r108-l6 ①：`.td-mod-menu` 原先走同一条')

    J2_OLD = (
        '  var RV_GAP = 6, RV_PAD = 4;\n'
        '  function placeRv(menu, trigger) {\n'
        '    if (!trigger || !menu.classList.contains(\'td-rv-menu\')) return;\n'
    )
    J2_NEW = (
        '  var RV_GAP = 6, RV_PAD = 4;\n'
        '  /* ★ r108-l6 ①：可现场摆位的两族 —— `.td-mod-menu`（标签栏 `+`）/ `.td-rv-menu`（审查工具条）。 */\n'
        '  var PLACE_ABS = [\'td-mod-menu\', \'td-rv-menu\'];\n'
        '  function placeRv(menu, trigger) {\n'
        '    if (!trigger) return;\n'
        '    var placeable = false;\n'
        '    for (var pa = 0; pa < PLACE_ABS.length; pa++) {\n'
        '      if (menu.classList.contains(PLACE_ABS[pa])) { placeable = true; break; }\n'
        '    }\n'
        '    if (!placeable) return;\n'
    )
    edit(PJS, J2_OLD, J2_NEW, '① placeRv 白名单',
         "var PLACE_ABS = ['td-mod-menu', 'td-rv-menu'];")

    J3_OLD = (
        '    var BRW_TEXT = {\n'
        "      send: '已把当前页面发到对话（视觉演示）',\n"
        "      shot: '已复制截图到剪贴板（视觉演示）',\n"
        "      zoom: '缩放：100%（视觉演示）',\n"
        "      more: '更多浏览器选项（视觉演示）'\n"
        '    };\n'
        '    /* ★ 第十一拍 ④（r107-l2）：官方「一键截图到剪贴板」= 快门白闪。\n'
        '       ⚠ 闪的是**整个浏览器模块**（`.td-brw`）而不是 `.td-view`：`.td-view` 自己是\n'
        '         `overflow:auto` 的滚动容器，绝对定位子元素会跟着内容滚走 ⇒ 滚动后就闪不见了。 */\n'
        '    function shotFlash() {\n'
        '      brw.classList.remove(\'is-shot\');\n'
        '      void brw.offsetWidth;                       /* 强制回流：同一个 class 的动画能重播 */\n'
        '      brw.classList.add(\'is-shot\');\n'
        '      setTimeout(function () { brw.classList.remove(\'is-shot\'); }, 300);\n'
        '    }\n'
        '    var brwActs = pane.querySelectorAll(\'[data-td-brw-act]\');\n'
        '    for (var ba = 0; ba < brwActs.length; ba++) {\n'
        '      (function (b) {\n'
        '        b.addEventListener(\'click\', function () {\n'
        '          var kind = b.getAttribute(\'data-td-brw-act\');\n'
        '          if (kind === \'shot\') shotFlash();\n'
        '          say(BRW_TEXT[kind] || \'已执行\');\n'
        '        });\n'
        '      })(brwActs[ba]);\n'
        '    }\n'
    )
    J3_NEW = (
        '    var BRW_TEXT = {\n'
        "      more: '更多浏览器选项（视觉演示）'\n"
        '    };\n'
        '    /* ★ r108-l6 ②：这里原有 `send` / `shot` / `zoom` 三条 —— 对应的三枚工具条图标按钮\n'
        '       已按邵先生「不需要，请去掉」整块移除 ⇒ 它们、以及为 `shot` 服务的 `shotFlash()`\n'
        '       快门（连同 CSS 18-②）一并删掉，不留死代码。右端的「更多」保留。\n'
        '       ⚠ 右键菜单里那条「截图到剪贴板」（`ctxForBrw`）是**另一处**功能，不是「工具条图标\n'
        '         按钮」⇒ 按「不得改动不必涉及的模块」保留；但它原来靠 `sb.click()` 借工具条按钮的\n'
        '         力 ⇒ 那里改成直接给轻提示（免留指向已删元素的死引用）。 */\n'
        '    var brwActs = pane.querySelectorAll(\'[data-td-brw-act]\');\n'
        '    for (var ba = 0; ba < brwActs.length; ba++) {\n'
        '      (function (b) {\n'
        '        b.addEventListener(\'click\', function () {\n'
        '          say(BRW_TEXT[b.getAttribute(\'data-td-brw-act\')] || \'已执行\');\n'
        '        });\n'
        '      })(brwActs[ba]);\n'
        '    }\n'
    )
    # ⚠ mark 不能取 `more: '…'` 那行 —— 它改前就在（send/shot/zoom/more 里 more 是最后一条）。
    #   必须取「BRW_TEXT 后**直接**跟 more」这个改后才形成的相邻关系。
    edit(PJS, J3_OLD, J3_NEW, '② 删 BRW_TEXT 三条 + shotFlash',
         "var BRW_TEXT = {\n      more: '更多浏览器选项（视觉演示）'")

    J4_OLD = (
        "    items.push({ label: '截图到剪贴板', key: '⇧⌘S', ico: 'pin', act: function () {\n"
        "      var sb = pane.querySelector('[data-td-brw-act=\"shot\"]');\n"
        '      if (sb) sb.click();\n'
        '    } });\n'
    )
    J4_NEW = (
        "    items.push({ label: '截图到剪贴板', key: '⇧⌘S', ico: 'pin', act: function () {\n"
        '      /* r108-l6 ②：工具条那枚相机按钮已删 ⇒ 不再借它的力（原 `sb.click()` 会指向空元素）。 */\n'
        "      say('已复制截图到剪贴板（视觉演示）');\n"
        '    } });\n'
    )
    edit(PJS, J4_OLD, J4_NEW, '② 右键菜单那条切断死引用',
         '/* r108-l6 ②：工具条那枚相机按钮已删')

    # ---------------------------------------------------------------- 跨层兜底
    print()
    print('=== 4/4  跨层标记兜底断言 ===')
    marks = [
        (MODS, 'id="av-zd-status"', 'l2 · 面板静态 DOM'),
        (PCS, '/* r108-l2 */', 'l2 · 第 19 节'),
        (PCS, '/* r108-l3 */', 'l3 · 第 19.1~19.3 节'),
        (PCS, '/* r108-l4 */', 'l4 · 第十五拍'),
        (PCS, '/* r108-l5 */', 'l5 · 第十六拍'),
        (PCS, '/* r108-l6 */', 'l6 · 第十七拍'),
        (MODS, 'class="zd-menu giencoder-dropdown-popup zd-menu-branch"', 'l3 · 两枚下拉'),
        (MODS, 'data-zd-git="commit"', 'l3 · Git 三行'),
        (MODS, 'class="zd-cv"', 'l2 · 折叠箭头'),
        (PCS, '.zd-sec.is-closed .zd-sec-x { display: flex; }', 'l4 · ⑥ trailing 仅折叠可见'),
        (PCS, '@keyframes zd-todo-spin {', 'l4 · ④ loading 弧'),
        (MODS, 'id="av-browse-pane-preview"', 'l5 · 预览页签面板'),
        (MODS, 'data-td-art="1"', '① 产物行仍在（两行 = 两个产物）'),
    ]
    bad = []
    for p, mk, label in marks:
        if mk not in rd(p)[0]:
            bad.append('%s：%s（在 %s 里找不到）' % (label, mk, os.path.basename(p)))

    m = rd(MODS)[0]
    j = rd(PJS)[0]
    c = rd(PCS)[0]
    # ② 的归零判据：三个 kind 全页 0 处、工具条只剩 more
    if m.count('data-td-brw-act="shot"') or m.count('data-td-brw-act="zoom"') or m.count('data-td-brw-act="send"'):
        bad.append('_mods.html：三枚被删按钮仍有残留')
    if m.count('data-td-brw-act="more"') != 1:
        bad.append('_mods.html：data-td-brw-act="more" 应恰好 1 处（实 %d）' % m.count('data-td-brw-act="more"'))
    # ⚠ 判据必须先剥注释（本层注释里为留痕主动写了 `shotFlash` / `is-shot` 这些旧标识符）
    jcode = re.sub(r'/\*.*?\*/', '', j, flags=re.S)
    jcode = re.sub(r'(?m)^\s*//.*$', '', jcode)
    for pat in (r'\bshotFlash\b', r"'shot'", r"'zoom'", r"'send'"):
        if re.search(pat, jcode):
            bad.append('panel.js：%s 引用残留（代码里，不是注释）' % pat)
    # ⚠ 判据看的是**带 kind 的**引用（`="shot"` 这种）；裸属性名保留 2 处是对的
    #   （`querySelectorAll('[data-td-brw-act]')` + `getAttribute('data-td-brw-act')`）。
    if jcode.count('data-td-brw-act="') != 0:
        bad.append('panel.js：仍有带 kind 的 data-td-brw-act 引用（应 0，实 %d）'
                   % jcode.count('data-td-brw-act="'))
    ccode = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    for pat in (r'\bis-shot\b', r'td-shot-flash'):
        if re.search(pat, ccode):
            bad.append('panel.css：%s 残留（代码里，不是注释）' % pat)
    # ① 的判据
    if jcode.count("var PLACE_ABS = ['td-mod-menu', 'td-rv-menu'];") != 1:
        bad.append('panel.js：PLACE_ABS 声明应恰好 1 处')
    if jcode.count("!menu.classList.contains('td-rv-menu')") != 0:
        bad.append('panel.js：旧的 td-rv-menu 单族守卫仍在')
    # ③ 的判据
    if '.td-tree { position: absolute; top: 44px;' not in c:
        bad.append('panel.css：.td-tree 未改成 top: 44px')
    if re.search(r'\.td-tree \{ position: absolute; inset: 0', c):
        bad.append('panel.css：.td-tree 仍是 inset: 0')
    # ④ 的判据：两张卡片都变长了
    if m.count('<div class="td-dr is-add">') < 4 + len(C1_ROWS):
        bad.append('_mods.html：卡片 1 统一视图新增行数不足（实 %d）' % m.count('<div class="td-dr is-add">'))
    for probe in ('.td-mod-body { flex: 1 1 auto; min-height: 0; overflow: auto; }',
                  'payload-marker-not-used'):
        if probe.startswith('payload'):
            continue
        if probe not in m:
            bad.append('_mods.html：卡片 2 新增行缺失（%s）' % probe[:40])
    if bad:
        sys.exit('!! 跨层标记自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')

    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


if __name__ == '__main__':
    main()
