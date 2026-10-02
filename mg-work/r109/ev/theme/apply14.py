# -*- coding: utf-8 -*-
u"""apply14.py —— **生成物**（由 make14.py 产生，请改 make14.py 的 EDITS 表）。

r109 第十五拍四条：恢复批注模块 / `.r93-todocard` 去缩进 / 任务产物卡可点 / 独立页签。
详见 make14.py 顶部 docstring。"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, u'..', u'..', u'..', u'..'))
PAGE = os.path.join(ROOT, u'pages', u'conversation.html')
PART = os.path.join(ROOT, u'mg-work', u'r109', u'part109')


def _read(path):
    with io.open(path, u'rb') as f:
        return f.read().decode(u'utf-8').replace(u'\r\n', u'\n')


def _part(name):
    return _read(os.path.join(PART, name))



def extract_new_note_js():
    u"""从权威源 `panel.js` 里抽出**新版批注 JS 整段**（不含头尾锚点）。"""
    src = _part(u'panel.js')
    a = src.find(u'var brw = pane.querySelector(\'.td-brw\');')
    b = src.find(u'var BRW_TEXT = {', a)
    if a < 0 or b < 0:
        raise SystemExit(u'[FATAL] panel.js 里找不到新版批注 JS 段的起止')
    return src[a:b]


def extract_new_note_css():
    u"""从权威源 `panel.css` 里抽出**新版批注 CSS 整段**（`.td-elnote {` → 「/* r109-l1 */」后）。"""
    src = _part(u'panel.css')
    a = src.find(u'.td-elnote {')
    # 新版段的终点 = 那段注释里第一条分隔线，或 `.td-elnote-ok[disabled]` 之后
    b = src.find(u'.td-elnote-ok[disabled]', a)
    if a < 0 or b < 0:
        raise SystemExit(u'[FATAL] panel.css 里找不到新版批注 CSS 段的起止')
    e = src.find(u'\n', b)
    e = src.find(u'\n', e + 1)          # 吃掉 `…pointer-events: none; }` 那一行 + 其后的 `/* r109-l1 */`
    return src[a:e]


def make_js_edit():
    u"""生成 `note-js` 这一条 EDIT 的 old / new。

    **old（页面旧版）**：从 `var brw = pane.querySelector('.td-brw');` 起，
    到 `var BRW_TEXT = {` 前 —— 与权威源同一对锚点，只是内容不同。
    **new（权威源新版）**：`extract_new_note_js()`。

    ⚠ 幂等：若页面已是新版，old 段 == new 段 ⇒ 判据 `new in t` 命中 ⇒ `[skip]`。
    """
    t = _read(PAGE)
    a = t.find(u'var brw = pane.querySelector(\'.td-brw\');')
    b = t.find(u'var BRW_TEXT = {', a)
    if a < 0 or b < 0:
        raise SystemExit(u'[FATAL] pages/conversation.html 里找不到旧版批注 JS 段的起止')
    old = t[a:b]
    new = extract_new_note_js()
    return old, new


def make_css_edit():
    u"""生成 `note-css` 这一条 EDIT 的 old / new。

    ⚠ 旧版段末锚点 = `.td-elnote-f button.is-primary`（旧版独有）。
    若页面已是新版 ⇒ 该锚点不存在 ⇒ 回退成「取当前页面上 `.td-elnote {` 那一段」当 old，
    这样幂等判据 (`new in t and count(old)==count(new)`) 会立刻命中 `new in t` 而 `[skip]`。
    """
    t = _read(PAGE)
    a = t.find(u'.td-elnote {')
    b = t.find(u'.td-elnote-f button.is-primary', a)
    if a < 0:
        raise SystemExit(u'[FATAL] pages/conversation.html 里找不到 .td-elnote { ')
    if b < 0:
        # 已是新版：把「现有的那一段」当 old 交回去，交由幂等判据 skip
        c = t.find(u'.td-elnote-ok[disabled]', a)
        e = t.find(u'\n', c)
        e = t.find(u'\n', e + 1)
        return t[a:e], extract_new_note_css()
    e = t.find(u'\n', b)
    e = t.find(u'\n', e + 1)
    old = t[a:e]
    new = extract_new_note_css()
    return old, new


def make_prev_edit():
    u"""生成 `prev-show` 这一条 EDIT 的 old / new（本轮 ③④ 的主改动）。

    old = 页面里 `var prevPane = pane.querySelector(…)` 起、到 `var artBtns = …` 前的整段
          （含 `prevShow` + 附件卡 IIFE）。
    new = `_new-prev.js`（本目录下的手写新实现，逐字读入）。
    """
    t = _read(PAGE)
    a = t.find(u'  var prevPane = pane.querySelector')
    b = t.find(u'  var artBtns = pane.querySelector', a)
    if a < 0 or b < 0:
        raise SystemExit(u'[FATAL] 页面里找不到 prevShow / attShow 段的起止')
    old = t[a:b]
    new = _read(os.path.join(HERE, u'_new-prev.js'))
    return old, new


EDITS = []


def _load_dynamic_edits():
    js_old, js_new = make_js_edit()
    css_old, css_new = make_css_edit()
    pv_old, pv_new = make_prev_edit()
    del EDITS[:]
    EDITS.extend([
        (u'note-css',       css_old,  css_new,  1),
        (u'note-js',        js_old,   js_new,   1),
        (u'note-bar',       BAR_OLD,  BAR_NEW,  1),
        (u'blank-css',      BLANK_CSS_OLD, BLANK_CSS_NEW, 1),
        (u'blank-html',     BLANK_HTML_OLD, BLANK_HTML_NEW, 1),
        (u'todocard-flush', TODOCARD_OLD, TODOCARD_NEW, 1),
        (u'tab-open',       OPENTAB_OLD, OPENTAB_NEW, 1),
        (u'tab-act',        ACT_OLD, ACT_NEW, 1),
        (u'tab-fileattr',   TABFILE_OLD, TABFILE_NEW, 1),
        (u'tab-bind',       BINDTAB_OLD, BINDTAB_NEW, 1),
        (u'tab-activate',   TABACT_OLD, TABACT_NEW, 1),
        (u'prev-show',      pv_old, pv_new, 1),
    ])

BAR_OLD = '.td-annot-bar {\n  position: sticky; bottom: 0; z-index: 2;\n'
BAR_NEW = '/* ★ r109-l1 ②（邵先生：「`td-annot-bar` 这个容器要显示到上面去，不要显示在下面，\n   不容易被注意到」）：`bottom: 0` → `top: 0`。\n   ⚠ 只改这一行**不够** —— `position: sticky` 的 `top` 只在元素位于「滚动容器里首个\n     可滚动子件」之前才追得上；它原来是 `.td-view` 的**末位子件**（贴在末尾时 sticky\n     的 `top` 永远追不上滚动）。DOM 侧已同步把它挪成 `.td-view` 的**首位子件**，\n     两处一起才生效。 */\n.td-annot-bar {\n  position: sticky; top: 0; z-index: 2;\n'
BLANK_CSS_OLD = '.td-page-blank {\n  height: 26px; margin: -12px -12px 12px;\n  background: var(--color-fill-2);\n}\n'
BLANK_CSS_NEW = '/* r109-l1 · ① td-page-blank 已删 */\n/* ★ r109-l1 ①（邵先生：「右栏浏览器模式下，`td-page-blank` 这个容器要删除」）：\n   这里原有那条 26px 高的演示用灰带 —— `.td-page` 的负外边距 `-12px -12px 12px`\n   就是专门为它通栏写的。DOM 侧与规则一起删，不留死规则。 */\n'
BLANK_HTML_OLD = '        <div class="td-page">\n          <div class="td-page-blank">&nbsp;</div>\n          <div class="td-page-body">\n'
BLANK_HTML_NEW = '        <div class="td-page">\n          <!-- ★ r109-l1 ①（邵先生：「td-page-blank 这个容器要删除」）：\n               这里原有 `<div class="td-page-blank">&nbsp;</div>` —— 一条 26px 的演示用灰带。\n               整块连同 panel.css 里那条规则一起删掉，不留死规则。 -->\n          <div class="td-page-body">\n'
TODOCARD_OLD = '.r93-todocard {\n  position: relative; width: calc(100% - 18px); margin-left: 18px; box-sizing: border-box;\n'
TODOCARD_NEW = '.r93-todocard {\n  /* ★ r109 第十五拍 ②（邵先生：「这个容器 `r93-todocard` 也要去掉缩进」）：\n     本条原为 `width: calc(100% - 18px); margin-left: 18px`（左缩进 18px）。\n     `.r93-card` 已在第十三拍归零，本拍把最后一个带缩进的卡片家族一起归零，\n     两个卡片家族口径至此完全一致。几何其余各项（height 220 / padding / radius /\n     border / flex 列 / overflow）一字未动。 */\n  position: relative; box-sizing: border-box;\n'
OPENTAB_OLD = '  function openTab(mod, opts) {\n    var ex = tabsEl.querySelector(\'[data-td-tab][data-td-mod="\' + mod + \'"]\');\n'
OPENTAB_NEW = '  /* ★ r109 第十五拍 ④（邵先生：「不同的文件在右栏浏览时，要分别打开**独立的页签**，\n     不要都在一个页签里浏览」）：`opts.file` = **本枚页签专属的文件名**。\n     · 给了 `file` ⇒ 页签 id 由 `(mod, file)` 二元组决定 ⇒ 一个文件一枚页签；\n     · 没给 ⇒ 退回原来的「一个 mod 一枚页签」（文件 / 审查 / 终端 / 浏览器 / 摘要\n       这五个模块仍各只有一枚，`+` 菜单与快捷键那两条路径都走这一支）。\n     ⚠ `data-td-mod` 恒为 `mod`（= preview）—— `activate()` 靠它找面板，而预览\n       面板只有一块（`[data-td-pane="preview"]`），多枚文件页签**共用**它，靠\n       下面的 `showFile()` 把内容换成被点那一枚文件自己的。 */\n  function openTab(mod, opts) {\n    var file = opts && opts.file ? String(opts.file) : \'\';\n    var ex = file\n      ? tabsEl.querySelector(\'[data-td-tab][data-td-mod="\' + mod + \'"][data-td-file="\' + file + \'"]\')\n      : tabsEl.querySelector(\'[data-td-tab][data-td-mod="\' + mod + \'"]:not([data-td-file])\');\n'
ACT_OLD = "  function activate(mod) {\n    var list = tabs(), i, on, found = false;\n    for (i = 0; i < list.length; i++) {\n      on = list[i].getAttribute('data-td-mod') === mod;\n"
ACT_NEW = "  /* ★ r109 第十五拍 ④：`file` 第二参 —— 同一个 `mod` 下可能挂着**多枚文件页签**\n     （见 `openTab`）。给了 `file` 就只激活 `data-td-file` 相符的那一枚，其余同一\n     `mod` 的页签一并退激活；不给则维持原口径（该 `mod` 下所有页签都算）。 */\n  function activate(mod, file) {\n    var f = file ? String(file) : '';\n    var list = tabs(), i, on, found = false;\n    for (i = 0; i < list.length; i++) {\n      on = list[i].getAttribute('data-td-mod') === mod;\n      if (on && f) on = (list[i].getAttribute('data-td-file') || '') === f;\n"
TABFILE_OLD = "    t.setAttribute('data-td-mod', mod);\n    t.setAttribute('tabindex', '0');\n"
TABFILE_NEW = "    t.setAttribute('data-td-mod', mod);\n    /* ★ r109 第十五拍 ④：本枚页签专属文件名的落点（见 `openTab` 顶部注释）。\n       ⚠ 只给 `file` 时落 —— 五个模块页签没有 `data-td-file`，与「一种 mod 一枚」\n         的原口径共存（`openTab` 的查询串用 `:not([data-td-file])` 区分）。 */\n    if (file) t.setAttribute('data-td-file', file);\n    t.setAttribute('tabindex', '0');\n"
BINDTAB_OLD = "    tab.addEventListener('click', function (e) {\n      if (e.target && e.target.closest && e.target.closest('[data-td-tab-x]')) return;\n      activate(tab.getAttribute('data-td-mod'));\n    });\n    tab.addEventListener('keydown', function (e) {\n      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(tab.getAttribute('data-td-mod')); }\n    });\n"
BINDTAB_NEW = "    tab.addEventListener('click', function (e) {\n      if (e.target && e.target.closest && e.target.closest('[data-td-tab-x]')) return;\n      /* ★ r109 第十五拍 ④：带上自己的文件名 —— 同一个 `mod`（preview）下可能挂着\n         多枚文件页签，不传文件名会把它们**一起**点亮。 */\n      tabActivate(tab);\n    });\n    tab.addEventListener('keydown', function (e) {\n      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tabActivate(tab); }\n    });\n"
TABACT_OLD = '  function bindTab(tab) {\n'
TABACT_NEW = "  /* ★ r109 第十五拍 ④：从一枚页签取 (mod, file) 后激活它。\n     集中成一处 —— `bindTab` 的 click / keydown 都调它，口径只有一份。 */\n  function tabActivate(tab) {\n    activate(tab.getAttribute('data-td-mod'), tab.getAttribute('data-td-file') || '');\n  }\n  function bindTab(tab) {\n"


# ======================================================================
# 运行
# ======================================================================
def run():
    _load_dynamic_edits()
    t = _read(PAGE)
    total = 0
    for name, old, new, want in EDITS:
        if (new in t) and (t.count(old) == new.count(old)):
            print(u'  [skip] %-16s 已是目标态' % name)
            continue
        if (old not in t) and (old not in new):
            print(u'  [skip] %-16s 已是目标态' % name)
            continue
        c = t.count(old)
        if c != want:
            print(u'  [FAIL] %-16s 命中 %d 处（期望 %d）' % (name, c, want))
            sys.exit(1)
        t = t.replace(old, new)
        total += c
        print(u'  [ok]   %-16s 替换 %d 处' % (name, c))
    out = t.replace(u'\n', u'\r\n')
    data = out.encode(u'utf-8')
    with io.open(PAGE, 'wb') as f:
        f.write(data)
    print(u'  total = %d 处，写回 %d bytes' % (total, len(data)))


if __name__ == u'__main__':
    run()
