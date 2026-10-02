# -*- coding: utf-8 -*-
u"""make14.py —— 生成第 16 层增量补丁 apply14.py（r109 第十五拍四条）。

邵先生原话（第十五拍）：
  1) 按照你倾向的路径恢复；（= 恢复右栏浏览器「批注模块」新版三拍 l1/l2/l3）
  2) 这个容器 `r93-todocard` 也要去掉缩进。
  3) 「任务产物」里的卡片文件也要支持点击后展开右栏浏览；
  4) 不同的文件在右栏浏览时，要分别打开独立的页签，不要都在一个页签里浏览。

★ 本层为什么是「增量层」而不是重跑整链：
  页面在 21:09→21:26 之间发生过一次**整页重建**，把注入的 `panel.js` 换回了旧版
  （r109-l1 之前的那份），于是 l1/l2/l3 三拍的批注改造在页面上**整体消失**。
  而权威源 `part109/panel.js` / `panel.css` 里的新版批注**一字未丢**。
  ⇒ 正确做法 = 从权威源**逐段提取**新版，精确替换页面里的旧段（见下方四条 EDIT）。

★ 四条 EDIT 的位置与形态：
  · `note-js`   —— JS：页面里 `var elnote = null;` 起、到 `var BRW_TEXT = {` 前的一段
                  （旧版整段）→ 换成权威源 `panel.js` 的同位置新版整段。
  · `note-css`  —— CSS：页面里 `.td-elnote {` 起、到「元素评论气泡」段末（`.td-elnote-f button.is-primary` 之后）→
                  换成权威源 `panel.css` 的 `.td-elnote { … }` 新版整段。
  · `note-bar`  —— CSS：`.td-annot-bar` 的 `position: sticky; bottom: 0;` → `top: 0;`（r109-l1 ②）。
  · `blank-css` —— CSS：`.td-page-blank { … }` 整条规则 → 留痕注释（r109-l1 ①）。
  · `blank-html`—— HTML：`<div class="td-page-blank">&nbsp;</div>` → 留痕注释。
  · `todocard-flush` —— CSS：`.r93-todocard` 的 `width: calc(100% - 18px); margin-left: 18px;` → 归零（本轮 ②）。
  · `prev-pertab`（本轮 ③④）—— JS：`prevShow` / `attShow` 从「复用同一枚 preview 页签」
                  改为「每个文件一枚独立页签」，并把 `.td-sum-art`（任务产物卡）也接到同一条链路。

★ 幂等判据（红线）：`(new in t) and (t.count(old) == new.count(old))` + 兜底
  `(old not in t) and (old not in new)`。纯追加型 EDIT 两个残式都会误判，唯一正确就是这条。

★ 链序：本层排在最后（第 16 层），文件名 `apply14.py`（`apply12.py` 之后、
  若将来有第 17 层再往后排）。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, u'..', u'..', u'..', u'..'))
PAGE = os.path.join(ROOT, u'pages', u'conversation.html')
PART = os.path.join(ROOT, u'mg-work', u'r109', u'part109')


def _read(path):
    with io.open(path, 'rb') as f:
        return f.read().decode('utf-8').replace('\r\n', '\n')


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


# ======================================================================
# 下列各条是**字面量 EDIT**（不依赖抽取），逐条给 old / new。
# ======================================================================

# ① `.td-annot-bar` 底部 → 顶部 sticky（r109-l1 ②）
BAR_OLD = (
    u'.td-annot-bar {\n'
    u'  position: sticky; bottom: 0; z-index: 2;\n'
)
BAR_NEW = (
    u'/* ★ r109-l1 ②（邵先生：「`td-annot-bar` 这个容器要显示到上面去，不要显示在下面，\n'
    u'   不容易被注意到」）：`bottom: 0` → `top: 0`。\n'
    u'   ⚠ 只改这一行**不够** —— `position: sticky` 的 `top` 只在元素位于「滚动容器里首个\n'
    u'     可滚动子件」之前才追得上；它原来是 `.td-view` 的**末位子件**（贴在末尾时 sticky\n'
    u'     的 `top` 永远追不上滚动）。DOM 侧已同步把它挪成 `.td-view` 的**首位子件**，\n'
    u'     两处一起才生效。 */\n'
    u'.td-annot-bar {\n'
    u'  position: sticky; top: 0; z-index: 2;\n'
)

# ② `.td-page-blank` 规则删除（r109-l1 ①）
BLANK_CSS_OLD = (
    u'.td-page-blank {\n'
    u'  height: 26px; margin: -12px -12px 12px;\n'
    u'  background: var(--color-fill-2);\n'
    u'}\n'
)
BLANK_CSS_NEW = (
    u'/* r109-l1 · ① td-page-blank 已删 */\n'
    u'/* ★ r109-l1 ①（邵先生：「右栏浏览器模式下，`td-page-blank` 这个容器要删除」）：\n'
    u'   这里原有那条 26px 高的演示用灰带 —— `.td-page` 的负外边距 `-12px -12px 12px`\n'
    u'   就是专门为它通栏写的。DOM 侧与规则一起删，不留死规则。 */\n'
)

# ③ `.td-page-blank` DOM 删除（r109-l1 ①）
BLANK_HTML_OLD = (
    u'        <div class="td-page">\n'
    u'          <div class="td-page-blank">&nbsp;</div>\n'
    u'          <div class="td-page-body">\n'
)
BLANK_HTML_NEW = (
    u'        <div class="td-page">\n'
    u'          <!-- ★ r109-l1 ①（邵先生：「td-page-blank 这个容器要删除」）：\n'
    u'               这里原有 `<div class="td-page-blank">&nbsp;</div>` —— 一条 26px 的演示用灰带。\n'
    u'               整块连同 panel.css 里那条规则一起删掉，不留死规则。 -->\n'
    u'          <div class="td-page-body">\n'
)

# ④ `.r93-todocard` 去缩进（本轮 ②）
TODOCARD_OLD = (
    u'.r93-todocard {\n'
    u'  position: relative; width: calc(100% - 18px); margin-left: 18px; box-sizing: border-box;\n'
)
TODOCARD_NEW = (
    u'.r93-todocard {\n'
    u'  /* ★ r109 第十五拍 ②（邵先生：「这个容器 `r93-todocard` 也要去掉缩进」）：\n'
    u'     本条原为 `width: calc(100% - 18px); margin-left: 18px`（左缩进 18px）。\n'
    u'     `.r93-card` 已在第十三拍归零，本拍把最后一个带缩进的卡片家族一起归零，\n'
    u'     两个卡片家族口径至此完全一致。几何其余各项（height 220 / padding / radius /\n'
    u'     border / flex 列 / overflow）一字未动。 */\n'
    u'  position: relative; box-sizing: border-box;\n'
)

# ======================================================================
# ⑤ 本轮 ③④：任务产物卡可点 + 每个文件一枚独立页签
# ======================================================================
# 现状（本轮改前）：`prevShow()` / `attShow()` 都是
#   `openTab('preview', { name, ico })` —— `openTab` 命中同名 `mod="preview"` 就 `activate()`
#   那**同一枚**页签，只把页签名 / 图标 / 正文换掉。
# 邵先生第 ④ 条要的是「不同的文件……分别打开独立的页签，不要都在一个页签里浏览」
# ⇒ 把「一个 mod 一枚页签」改成「**一个文件一枚页签**」：
#   · 页签 id 用 `data-td-file`（文件名）区分；`data-td-mod` 一律是 `'preview'`
#     （`activate()` 靠它找面板 —— 面板只有一块，多枚页签共用同一个 `[data-td-pane="preview"]`）；
#   · `activate(mod, file)` 第二参带文件名时，只让 `data-td-file` 相符的那一枚页签 `is-active`；
#   · 点页签切回某个文件时，`showFile()` 用该文件自己的元信息重填标题行 + 骨架。
# 第 ③ 条：`.td-sum-art`（任务产物卡）—— 原来只有卡里那枚 `.td-diff-btn`「预览」按钮挂了
#   `[data-td-art]` 委托。本拍把委托扩到**整张卡**（卡上已有 `data-td-art="1"`）⇒ 点卡
#   任意处都能开右栏浏览。

# ① `openTab` —— 加 `opts.file` 支持 + 独立页签
OPENTAB_OLD = (
    u'  function openTab(mod, opts) {\n'
    u'    var ex = tabsEl.querySelector(\'[data-td-tab][data-td-mod="\' + mod + \'"]\');\n'
)
OPENTAB_NEW = (
    u'  /* ★ r109 第十五拍 ④（邵先生：「不同的文件在右栏浏览时，要分别打开**独立的页签**，\n'
    u'     不要都在一个页签里浏览」）：`opts.file` = **本枚页签专属的文件名**。\n'
    u'     · 给了 `file` ⇒ 页签 id 由 `(mod, file)` 二元组决定 ⇒ 一个文件一枚页签；\n'
    u'     · 没给 ⇒ 退回原来的「一个 mod 一枚页签」（文件 / 审查 / 终端 / 浏览器 / 摘要\n'
    u'       这五个模块仍各只有一枚，`+` 菜单与快捷键那两条路径都走这一支）。\n'
    u'     ⚠ `data-td-mod` 恒为 `mod`（= preview）—— `activate()` 靠它找面板，而预览\n'
    u'       面板只有一块（`[data-td-pane="preview"]`），多枚文件页签**共用**它，靠\n'
    u'       下面的 `showFile()` 把内容换成被点那一枚文件自己的。 */\n'
    u'  function openTab(mod, opts) {\n'
    u'    var file = opts && opts.file ? String(opts.file) : \'\';\n'
    u'    var ex = file\n'
    u'      ? tabsEl.querySelector(\'[data-td-tab][data-td-mod="\' + mod + \'"][data-td-file="\' + file + \'"]\')\n'
    u'      : tabsEl.querySelector(\'[data-td-tab][data-td-mod="\' + mod + \'"]:not([data-td-file])\');\n'
)

# ② `activate` —— 支持按文件名精确激活
ACT_OLD = (
    u'  function activate(mod) {\n'
    u'    var list = tabs(), i, on, found = false;\n'
    u'    for (i = 0; i < list.length; i++) {\n'
    u'      on = list[i].getAttribute(\'data-td-mod\') === mod;\n'
)
ACT_NEW = (
    u'  /* ★ r109 第十五拍 ④：`file` 第二参 —— 同一个 `mod` 下可能挂着**多枚文件页签**\n'
    u'     （见 `openTab`）。给了 `file` 就只激活 `data-td-file` 相符的那一枚，其余同一\n'
    u'     `mod` 的页签一并退激活；不给则维持原口径（该 `mod` 下所有页签都算）。 */\n'
    u'  function activate(mod, file) {\n'
    u'    var f = file ? String(file) : \'\';\n'
    u'    var list = tabs(), i, on, found = false;\n'
    u'    for (i = 0; i < list.length; i++) {\n'
    u'      on = list[i].getAttribute(\'data-td-mod\') === mod;\n'
    u'      if (on && f) on = (list[i].getAttribute(\'data-td-file\') || \'\') === f;\n'
)

# ③ 新建页签时把 `data-td-file` 落到 DOM 上（只有 `opts.file` 给了才落）
TABFILE_OLD = (
    u'    t.setAttribute(\'data-td-mod\', mod);\n'
    u'    t.setAttribute(\'tabindex\', \'0\');\n'
)
TABFILE_NEW = (
    u'    t.setAttribute(\'data-td-mod\', mod);\n'
    u'    /* ★ r109 第十五拍 ④：本枚页签专属文件名的落点（见 `openTab` 顶部注释）。\n'
    u'       ⚠ 只给 `file` 时落 —— 五个模块页签没有 `data-td-file`，与「一种 mod 一枚」\n'
    u'         的原口径共存（`openTab` 的查询串用 `:not([data-td-file])` 区分）。 */\n'
    u'    if (file) t.setAttribute(\'data-td-file\', file);\n'
    u'    t.setAttribute(\'tabindex\', \'0\');\n'
)

# ④ 页签自己的 `click` / 键盘激活要带上文件名（否则点回某枚文件页签，
#    `activate(mod)` 会把同 mod 的几枚**一起**点亮）
BINDTAB_OLD = (
    u'    tab.addEventListener(\'click\', function (e) {\n'
    u'      if (e.target && e.target.closest && e.target.closest(\'[data-td-tab-x]\')) return;\n'
    u'      activate(tab.getAttribute(\'data-td-mod\'));\n'
    u'    });\n'
    u'    tab.addEventListener(\'keydown\', function (e) {\n'
    u'      if (e.key === \'Enter\' || e.key === \' \') { e.preventDefault(); activate(tab.getAttribute(\'data-td-mod\')); }\n'
    u'    });\n'
)
BINDTAB_NEW = (
    u'    tab.addEventListener(\'click\', function (e) {\n'
    u'      if (e.target && e.target.closest && e.target.closest(\'[data-td-tab-x]\')) return;\n'
    u'      /* ★ r109 第十五拍 ④：带上自己的文件名 —— 同一个 `mod`（preview）下可能挂着\n'
    u'         多枚文件页签，不传文件名会把它们**一起**点亮。 */\n'
    u'      tabActivate(tab);\n'
    u'    });\n'
    u'    tab.addEventListener(\'keydown\', function (e) {\n'
    u'      if (e.key === \'Enter\' || e.key === \' \') { e.preventDefault(); tabActivate(tab); }\n'
    u'    });\n'
)

# ⑤ 按页签自己携带的 (mod, file) 激活
TABACT_OLD = (
    u'  function bindTab(tab) {\n'
)
TABACT_NEW = (
    u'  /* ★ r109 第十五拍 ④：从一枚页签取 (mod, file) 后激活它。\n'
    u'     集中成一处 —— `bindTab` 的 click / keydown 都调它，口径只有一份。 */\n'
    u'  function tabActivate(tab) {\n'
    u'    activate(tab.getAttribute(\'data-td-mod\'), tab.getAttribute(\'data-td-file\') || \'\');\n'
    u'  }\n'
    u'  function bindTab(tab) {\n'
)

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
    EDITS.extend([
        (u'note-css',     css_old,        css_new,        1),
        (u'note-js',      js_old,         js_new,         1),
        (u'note-bar',     BAR_OLD,        BAR_NEW,        1),
        (u'blank-css',    BLANK_CSS_OLD,  BLANK_CSS_NEW,  1),
        (u'blank-html',   BLANK_HTML_OLD, BLANK_HTML_NEW, 1),
        (u'todocard-flush', TODOCARD_OLD, TODOCARD_NEW,   1),
        (u'tab-open',     OPENTAB_OLD,    OPENTAB_NEW,    1),
        (u'tab-act',      ACT_OLD,        ACT_NEW,        1),
        (u'tab-fileattr', TABFILE_OLD,    TABFILE_NEW,    1),
        (u'tab-bind',     BINDTAB_OLD,    BINDTAB_NEW,    1),
        (u'tab-activate', TABACT_OLD,     TABACT_NEW,     1),
        (u'prev-show',    pv_old,         pv_new,         1),
    ])


FOOTER = u'''

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
    out = t.replace(u'\\n', u'\\r\\n')
    data = out.encode(u'utf-8')
    with io.open(PAGE, 'wb') as f:
        f.write(data)
    print(u'  total = %d 处，写回 %d bytes' % (total, len(data)))


if __name__ == u'__main__':
    run()
'''


def render():
    parts = [
        u'# -*- coding: utf-8 -*-',
        u'u"""apply14.py —— **生成物**（由 make14.py 产生，请改 make14.py 的 EDITS 表）。',
        u'',
        u'r109 第十五拍四条：恢复批注模块 / `.r93-todocard` 去缩进 / 任务产物卡可点 / 独立页签。',
        u'详见 make14.py 顶部 docstring。"""',
        u'import io',
        u'import os',
        u'import sys',
        u'',
        u'HERE = os.path.dirname(os.path.abspath(__file__))',
        u'ROOT = os.path.abspath(os.path.join(HERE, u\'..\', u\'..\', u\'..\', u\'..\'))',
        u'PAGE = os.path.join(ROOT, u\'pages\', u\'conversation.html\')',
        u'PART = os.path.join(ROOT, u\'mg-work\', u\'r109\', u\'part109\')',
        u'',
        u'',
        u'def _read(path):',
        u'    with io.open(path, u\'rb\') as f:',
        u'        return f.read().decode(u\'utf-8\').replace(u\'\\r\\n\', u\'\\n\')',
        u'',
        u'',
        u'def _part(name):',
        u'    return _read(os.path.join(PART, name))',
        u'',
    ]
    # 函数体逐字搬
    for fn in (extract_new_note_js, extract_new_note_css, make_js_edit, make_css_edit,
               make_prev_edit):
        parts.append(u'')
        parts.append(u'')
        src = _fn_source(fn)
        parts.append(src)
    parts.append(u'')
    parts.append(u'')
    parts.append(u'EDITS = []')
    parts.append(u'')
    parts.append(u'')
    body = _load_dynamic_source()
    parts.append(body)
    txt = u'\n'.join(parts) + u'\n' + FOOTER
    return txt


def _fn_source(fn):
    import inspect
    src = inspect.getsource(fn)
    return src.replace(u'\r\n', u'\n').rstrip(u'\n')


def _load_dynamic_source():
    src = u'''def _load_dynamic_edits():
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
    ])'''
    out = [src, u'']
    for name, val in ((u'BAR_OLD', BAR_OLD), (u'BAR_NEW', BAR_NEW),
                      (u'BLANK_CSS_OLD', BLANK_CSS_OLD), (u'BLANK_CSS_NEW', BLANK_CSS_NEW),
                      (u'BLANK_HTML_OLD', BLANK_HTML_OLD), (u'BLANK_HTML_NEW', BLANK_HTML_NEW),
                      (u'TODOCARD_OLD', TODOCARD_OLD), (u'TODOCARD_NEW', TODOCARD_NEW),
                      (u'OPENTAB_OLD', OPENTAB_OLD), (u'OPENTAB_NEW', OPENTAB_NEW),
                      (u'ACT_OLD', ACT_OLD), (u'ACT_NEW', ACT_NEW),
                      (u'TABFILE_OLD', TABFILE_OLD), (u'TABFILE_NEW', TABFILE_NEW),
                      (u'BINDTAB_OLD', BINDTAB_OLD), (u'BINDTAB_NEW', BINDTAB_NEW),
                      (u'TABACT_OLD', TABACT_OLD), (u'TABACT_NEW', TABACT_NEW)):
        out.append(u'%s = %r' % (name, val))
    return u'\n'.join(out)


if __name__ == u'__main__':
    out = render()
    dst = os.path.join(HERE, u'apply14.py')
    with io.open(dst, 'w', encoding='utf-8', newline=u'') as f:
        f.write(out)
    print(u'wrote %s  (%d chars)' % (dst, len(out)))
