# -*- coding: utf-8 -*-
u"""apply12.py —— ★ 生成物，请勿手改；改动落 make12.py 的 EDITS 表。

r109 第十二拍（邵先生四条）：
  1) 标题栏 `.r93-bar` 背景色 = 白（走 `--color-bg-1`；变量 `--r93-glass` 保留给药丸）
  2) `.r93-att.r93-t14` 附件卡可点 ⇒ 开右栏「预览」页签浏览文件内容
  3) `.r93-card--ctx` 内间距 = 16px
  4) `.zd-sec-h` 整行可点展开 / 折叠

只落 `pages/conversation.html`。
★ CRLF：页面换行全为 `\r\n` ⇒ 运行期先规范化成 LF 再匹配 / 替换，收尾转回 CRLF。
★ 幂等：每条 EDIT 先判“是否已含新串”。
"""
import io, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, u'..', u'..', u'..', u'..'))
PAGES = os.path.join(ROOT, u'pages')

EDITS = [
    (u'card-flush',
     u'.r93-card {\n  position: relative; width: calc(100% - 18px); margin-left: 18px; border-radius: 8px;\n',
     u'.r93-card {\n  position: relative; border-radius: 8px;\n  /* ★ r109 第十三拍 ②：邵先生「`r93-card r93-card--edge` 这种卡片都去掉前面的缩进」。\n     本条原为 `width: calc(100% - 18px); margin-left: 18px`（左缩进 18px）。\n     ⚠ 之前那轮的「取消缩进」其实**只落在 `.r93-todocard`**，`.r93-card` 从未改掉 ——\n       本条的子类（`.r93-card--edge` 等）自身无宽度项 ⇒ 全部继承这 18px。现归零。 */\n',
     1),
    (u'card-full',
     u'.r93-card--full { width: 100%; margin-left: 0; }',
     u'/* ★ r109 第十三拍 ②：上面 `.r93-card` 已归零缩进 ⇒ 本条与之同值。\n   保留选择器不动（调用点仍在 HTML 里；删规则会改特指度链，不必冒这个险）。 */\n.r93-card--full { width: 100%; margin-left: 0; }',
     1),
    (u'zdhost-ready',
     u'html:has(.r93-sk) .zd-host { display: none; }\n.zd-card {',
     u"html:has(.r93-sk):has(.r93-sk) .zd-host { display: none; }\n/* ★ r109 第十三拍 ①：邵先生「`zd-host` 要在**骨架屏加载完成**后，\n   **和对话内容主体一起**显示，不要提前显示」。\n   现状：原来只有上面那条 `:has()` 管「骨架屏在屏期间不显示」；\n   骨架屏 380+320ms 从 DOM 移除后它就失效，面板**立刻**出来 —— 而对话主体还在等\n   `data-r93-app` 置为 `ready`（`.mt-8` 那条的 `opacity: 1` + 0.2s 过渡）⇒ 面板比主体早到 = 「提前显示」。\n   修法：把「显示」也接到**同一个就绪开关**上 —— `data-r93-app` 置为 `ready` 正是脚本在\n   **骨架屏开始退场的那一拍（380ms）**打上的（见下方 JS）⇒ 与主体同拍显形。\n   ⚠ **两条规则同特指度**（都是 0,1,0）⇒ 后者胜 ⇒ 骨架屏期必须用更高优先级压住它\n   （这里叠**两个 `:has()`**）—— 否则 `ready` 一到、骨架屏还在屏上面板就冒出来了（实测踩中）。\n   ★ 不新造状态、不加 JS 计时 ⇒ 与骨架屏时长、主体过渡都不耦合。 */\nhtml[data-r93-app='ready'] .zd-host { display: flex; }\n.zd-card {",
     1),
    (u'bar-white',
     u'.r93-bar {\n  position: absolute; top: 0; left: 0; right: 0; z-index: 10; height: 44px;\n  border-bottom: 1px solid var(--r93-line);\n  background: var(--r93-glass);\n  -webkit-backdrop-filter: blur(12px);\n  backdrop-filter: blur(12px);\n}',
     u'.r93-bar {\n  position: absolute; top: 0; left: 0; right: 0; z-index: 10; height: 44px;\n  border-bottom: 1px solid var(--r93-line);\n  /* ★ r109 第十二拍 ①：邵先生「标题栏 `.r93-bar` 的背景色应该是白色的」。\n     原来走 `--r93-glass`（72% 透的白 + 12px 毛玻璃）⇒ 内容是透出来的、不是「白色」。\n     现在改成**不透明白**（`--color-bg-1`：浅 = #fff / 暗 = #17171a），\n     并将 `backdrop-filter` 一并关掉 —— 底已不透明，留着毛玻璃只会白拿一层合成开销，\n     且会让滚动时透出内容虚影（与「纯白」自相矛盾）。\n     ⚠ `--r93-glass` 变量本身**保留不动**：「滚动到底部」药丸（`.r93-tobottom`）还在用它。\n     ⚠ 暗色档的 `--r93-glass: rgba(35,35,36,0.72)` 也一字不动。 */\n  background: var(--color-bg-1);\n  -webkit-backdrop-filter: none;\n  backdrop-filter: none;\n}',
     1),
    (u'ctx-pad16',
     u'.r93-card--ctx { min-height: 150px; max-height: 240px; overflow-y: auto; overflow-x: hidden; }',
     u'/* ★ r109 第十二拍 ③：邵先生「`.r93-card--ctx` 这种卡片的内间距调整为 16px」。\n   原先本条**没有 padding 声明** ⇒ 实得吃 `.r93-card` 的 `padding: 12px`。\n   ⚠ `min-height: 150px` / `max-height: 240px` / `overflow` 一字未动 ⇒ 卡高上限不变。 */\n.r93-card--ctx { min-height: 150px; max-height: 240px; overflow-y: auto; overflow-x: hidden; padding: 16px; }',
     1),
    (u'sec-css',
     u'.zd-sec-h {\n  display: flex; align-items: center; gap: 6px;\n  box-sizing: border-box; padding: 0 8px;',
     u'.zd-sec-h {\n  display: flex; align-items: center; gap: 6px;\n  box-sizing: border-box; padding: 0 8px;\n  /* ★ r109 第十二拍 ④：整行可点 ⇒ 给整行一个手型（原来是死区、鼠标不变形）。 */\n  cursor: pointer;',
     1),
    (u'sec-js',
     u"      var t = sec.querySelector('.zd-sec-t');\n      if (!t) return;\n      t.addEventListener('click', function () {\n        var closed = sec.classList.toggle('is-closed');\n        t.setAttribute('aria-expanded', closed ? 'false' : 'true');\n      });",
     u"      var t = sec.querySelector('.zd-sec-t');\n      if (!t) return;\n      var row = sec.querySelector('.zd-sec-h');\n      function r109SecToggle() {\n        var closed = sec.classList.toggle('is-closed');\n        t.setAttribute('aria-expanded', closed ? 'false' : 'true');\n      }\n      t.addEventListener('click', function (ev) {\n        /* ★ r109 第十二拍 ④：整行可点 ⇒ 事件会从 `.zd-sec-h` 冒泡上来。\n           点在标题按钮上时由**行**那一份负责，这里早退，避免 toggle 两次。 */\n        if (row && ev.target && ev.target.closest && ev.target.closest('.zd-sec-h') === row) return;\n        r109SecToggle();\n      });\n      /* ★ r109 第十二拍 ④：邵先生「`.zd-sec-h` 这个标题栏支持整行点击展开和折叠」。\n         原来只有标题按钮吃点击，行右侧（`.zd-sec-x` 那一大片）是死区。 */\n      if (row && row !== t) row.addEventListener('click', function (ev) {\n        /* 行内的**独立按钮**（如「暂停目标」那枚 `.zd-ico`）自己吃事件，不触发折展。 */\n        if (ev.target && ev.target.closest && ev.target.closest('button') && ev.target.closest('button') !== t) return;\n        r109SecToggle();\n      });",
     1),
    (u'att-css',
     u'.r93-att {\n  display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 12px;\n  border-radius: 8px; border: 1px solid var(--color-border-1);\n  background: var(--r93-card); color: var(--color-text-1);\n}',
     u'.r93-att {\n  display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 12px;\n  border-radius: 8px; border: 1px solid var(--color-border-1);\n  background: var(--r93-card); color: var(--color-text-1);\n}\n/* ★ r109 第十二拍 ②：附件卡 = **用户上传的本地文件**，可点开右栏浏览内容。\n   hover 只提边框一级（与 `.td-sum-art` 同口径），不加底色 —— 卡本身已有 `--r93-card` 底。 */\n.r93-att[data-r93-att-file] { cursor: pointer; transition: border-color 140ms ease; }\n.r93-att[data-r93-att-file]:hover { border-color: var(--color-border-2); }\n.r93-att[data-r93-att-file]:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }',
     1),
    (u'att-js1',
     u'    \'<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>部门人员名单.xlsx</span>\',\n    \'<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>产品初版设计方案.md</span>\',',
     u'    \'<span class="r93-att r93-t14" data-r93-att-file="部门人员名单.xlsx" role="button" tabindex="0"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>部门人员名单.xlsx</span>\',\n    \'<span class="r93-att r93-t14" data-r93-att-file="产品初版设计方案.md" role="button" tabindex="0"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>产品初版设计方案.md</span>\',',
     1),
    (u'att-js2',
     u'    \'<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">\' + IC(\'fxls\') + \'</span>vscode-light-modern-color-system.xlsx</span>\',',
     u'    \'<span class="r93-att r93-t14" data-r93-att-file="vscode-light-modern-color-system.xlsx" role="button" tabindex="0"><span class="r93-iblk r93-i16">\' + IC(\'fxls\') + \'</span>vscode-light-modern-color-system.xlsx</span>\',',
     1),
    (u'att-drive',
     u"  var artBtns = pane.querySelectorAll('[data-td-art]');",
     u"  /* ★ r109 第十二拍 ②：用户上传的本地文件（`.r93-att[data-r93-att-file]`）\n     —— 点卡片开右栏「预览」页签浏览内容。复用上面 `prevShow` 的**同一套**骨架切换与文案填充，\n     只是数据源换成卡片自己的 `data-r93-att-file`（文件名），不依赖 `.td-sum-art` 那棵子树。\n     ⚠ 附件卡在 `<main>` 里、右栏在 `#av-browse-slot` 里，两者不同子树 ⇒ 委托挂 document。 */\n  (function () {\n    var SIZE_BY_EXT = { xlsx: '表格 · 34 KB', xls: '表格 · 34 KB', csv: '表格 · 8 KB',\n                        md: 'Markdown · 12 KB' };\n    function attShow(el) {\n      if (!prevPane) return;\n      var name = el.getAttribute('data-r93-att-file') || '文件';\n      var ext = (name.split('.').pop() || '').toLowerCase();\n      var kind = (/^(xlsx|xls|csv|tsv)$/).test(ext) ? 'xlsx' : 'md';\n      var ico = el.querySelector('.r93-iblk svg');\n      var pn = prevPane.querySelector('[data-td-prev-name]');\n      var pm = prevPane.querySelector('[data-td-prev-meta]');\n      var pi = prevPane.querySelector('[data-td-prev-ico]');\n      if (pn) pn.textContent = name;\n      if (pm) pm.textContent = (SIZE_BY_EXT[ext] || '文件') + ' · 只读预览';\n      if (pi && ico) pi.innerHTML = ico.outerHTML;\n      var bodies = prevPane.querySelectorAll('[data-td-prev-kind]');\n      for (var q = 0; q < bodies.length; q++) {\n        if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');\n        else bodies[q].setAttribute('hidden', '');\n      }\n      /* ⚠ 与 `prevShow` 同序：**先填内容再 `openTab`**，否则闪一帧旧文件名。 */\n      openTab('preview', { name: name, ico: ico ? ico.outerHTML : '' });\n    }\n    document.addEventListener('click', function (ev) {\n      var el = ev.target && ev.target.closest ? ev.target.closest('[data-r93-att-file]') : null;\n      if (el) attShow(el);\n    });\n    document.addEventListener('keydown', function (ev) {\n      if (ev.key !== 'Enter' && ev.key !== ' ') return;\n      var el = ev.target && ev.target.closest ? ev.target.closest('[data-r93-att-file]') : null;\n      if (!el) return;\n      ev.preventDefault();\n      attShow(el);\n    });\n  })();\n  var artBtns = pane.querySelectorAll('[data-td-art]');",
     1),
]


def run():
    p = os.path.join(PAGES, u'conversation.html')
    raw = io.open(p, 'rb').read()
    t = raw.decode('utf-8').replace(u'\r\n', u'\n')   # ← 全文规范化成 LF
    total = 0
    for name, old, new, want in EDITS:
        # ★ 幂等判据（关键，两次踩坑后定稿）：
        #   纯追加型 EDIT（sec-css / att-css / att-drive）的 `new` = `old` + 追加行
        #   ⇒ `old` 是 `new` 的**严格前缀**，两边计数恒等（都 = 1）
        #   ⇒ 无论用「old 是否消失」还是「old 计数是否等于 new 里的计数」都会**误判为已完成**（第一遍就 [skip]，CSS 根本没落上，实测翻车）。
        #   唯一正确的判据 = **`new` 整体是否已在文里**（追加型跑完后 new 必在；未跑则新增行还没出现）。
        #   ⚠ 反例相反：非追加型（替换型）的 `new` 也可能早就存在（比如 bar-white 的
        #     `background: var(--color-bg-1)` 别处就有）⇒ 必须**两者合取**：
        #     `new in t` **且** `old` 在本 EDIT 的作用域内已归零。
        #   实践（本层 EDITS 全部 `want == 1`）⇒ 判据取：`new in t and t.count(old) == new.count(old)`。
        if (new in t) and (t.count(old) == new.count(old)):
            print(u'  [skip] %-12s 已是目标态' % name)
            continue
        if (old not in t) and (old not in new):
            print(u'  [skip] %-12s 已是目标态' % name)
            continue
        c = t.count(old)
        if c != want:
            print(u'  [FAIL] %-12s 命中 %d 处（期望 %d）' % (name, c, want))
            sys.exit(1)
        t = t.replace(old, new)
        total += c
        print(u'  [ok]   %-12s 替换 %d 处' % (name, c))
    out = t.replace(u'\n', u'\r\n').encode('utf-8')     # ← 收尾转回 CRLF
    if out != raw:
        io.open(p, 'wb').write(out)
    print(u'  >> 共替换 %d 处；md5 = %s' % (total, hashlib.md5(out).hexdigest()))


if __name__ == u'__main__':
    run()
