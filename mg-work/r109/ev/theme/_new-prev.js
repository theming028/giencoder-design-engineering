  var prevPane = pane.querySelector('#av-browse-pane-preview');
  /* ★ r109 第十五拍 ③④：**一个文件一枚独立页签**。
     改前：`prevShow()` / `attShow()` 都走 `openTab('preview', {name, ico})` —— 命中同名
       `mod="preview"` 就 `activate()` 那**同一枚**页签，只换页签名 / 图标 / 正文。
     邵先生第 ④ 条：「不同的文件在右栏浏览时，要分别打开独立的页签，不要都在一个页签里浏览」
     ⇒ 现在两处都多传一个 `file`（= 文件名），`openTab` 按 `(mod, file)` 建 / 找页签。
     第 ③ 条：「'任务产物'里的卡片文件也要支持点击后展开右栏浏览」—— `.td-sum-art` 卡上
       本来就带 `data-td-art="1"`，本拍把点击委托从「卡里那枚 .td-diff-btn」**扩到整张卡**
       （下面的 document 委托 + `artBtns` 两路都认，点卡任意处都能开）。
     内容填充仍**一字未改**：两套骨架（md / xlsx）由 `data-td-prev-kind` 切、文案填
       `[data-td-prev-name]` / `[data-td-prev-meta]` / `[data-td-prev-ico]`。 */
  /* 把「按 kind 切骨架 + 填标题行」抽成一处 —— `prevShow` / `attShow` 与「点页签切回来」
     三条路径都要它，口径只有一份（改前是两个各自复制了一遍的 body）。 */
  function prevFill(name, meta, icoSvg, kind) {
    if (!prevPane) return;
    var pn = prevPane.querySelector('[data-td-prev-name]');
    var pm = prevPane.querySelector('[data-td-prev-meta]');
    var pi = prevPane.querySelector('[data-td-prev-ico]');
    if (pn) pn.textContent = name;
    if (pm) pm.textContent = meta;
    if (pi && icoSvg) pi.innerHTML = icoSvg;
    var bodies = prevPane.querySelectorAll('[data-td-prev-kind]');
    for (var q = 0; q < bodies.length; q++) {
      if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');
      else bodies[q].setAttribute('hidden', '');
    }
  }
  function prevKindOf(name) {
    return (/\.(xlsx|xls|csv|tsv)$/i).test(name) ? 'xlsx' : 'md';
  }
  /* ★ 第十五拍 ④ 的**记忆体**：页签名 → 该文件的 (meta, ico, kind)。
     `openTab()` 复用已有页签时只改页签名与图标，**不重填正文** ⇒ 从别的模块切回这枚
     文件页签时（`tabActivate` → `activate`），得靠这张表把它自己的内容装回去。
     顺带也是 `displayName()` 里「页签名截断到 14 字」的一致性来源。 */
  var prevFiles = {};
  function prevRemember(name, meta, icoSvg, kind) {
    prevFiles[name] = { meta: meta, ico: icoSvg || '', kind: kind };
  }
  function prevShowFile(name) {
    var rec = prevFiles[name];
    if (!rec) return;
    prevFill(name, rec.meta, rec.ico, rec.kind);
    var ex = tabsEl.querySelector('[data-td-tab][data-td-mod="preview"][data-td-file="' + name + '"]');
    if (ex) tabActivate(ex);
  }
  function prevShow(btn) {
    if (!prevPane) return;
    var host = btn && btn.closest ? btn.closest('.td-sum-art') : null;
    var nmEl = host && host.querySelector('.td-sum-artt b');
    var mtEl = host && host.querySelector('.td-sum-artt i');
    var ico = host && host.querySelector('.td-sum-arti svg');
    var name = nmEl ? nmEl.textContent : '产物';
    var meta = (mtEl ? mtEl.textContent : '') + ' · 只读预览';
    var kind = prevKindOf(name);
    var icoSvg = ico ? ico.outerHTML : '';
    prevFill(name, meta, icoSvg, kind);
    prevRemember(name, meta, icoSvg, kind);
    /* ⚠ 顺序：**先把内容填好再 `openTab`** —— 后者会 `activate()` 让面板显形，
       反过来的话会闪一帧「旧文件名 / 旧骨架」。 */
    openTab('preview', { name: name, ico: icoSvg, file: name });
  }
  /* ★ r109 第十二拍 ②：用户上传的本地文件（`.r93-att[data-r93-att-file]`）
     —— 点卡片开右栏「预览」页签浏览内容。复用上面 `prevShow` 的**同一套**骨架切换与文案填充，
     只是数据源换成卡片自己的 `data-r93-att-file`（文件名），不依赖 `.td-sum-art` 那棵子树。
     ⚠ 附件卡在 `<main>` 里、右栏在 `#av-browse-slot` 里，两者不同子树 ⇒ 委托挂 document。 */
  (function () {
    var SIZE_BY_EXT = { xlsx: '表格 · 34 KB', xls: '表格 · 34 KB', csv: '表格 · 8 KB',
                        md: 'Markdown · 12 KB' };
    function attShow(el) {
      if (!prevPane) return;
      var name = el.getAttribute('data-r93-att-file') || '文件';
      var ext = (name.split('.').pop() || '').toLowerCase();
      var kind = (/^(xlsx|xls|csv|tsv)$/).test(ext) ? 'xlsx' : 'md';
      var ico = el.querySelector('.r93-iblk svg');
      var meta = (SIZE_BY_EXT[ext] || '文件') + ' · 只读预览';
      var icoSvg = ico ? ico.outerHTML : '';
      prevFill(name, meta, icoSvg, kind);
      prevRemember(name, meta, icoSvg, kind);
      /* ⚠ 与 `prevShow` 同序：**先填内容再 `openTab`**，否则闪一帧旧文件名。
         ★ 第十五拍 ④：多传 `file` ⇒ 每个文件一枚独立页签（见顶部注释）。 */
      openTab('preview', { name: name, ico: icoSvg, file: name });
    }
    document.addEventListener('click', function (ev) {
      var el = ev.target && ev.target.closest ? ev.target.closest('[data-r93-att-file]') : null;
      if (el) attShow(el);
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key !== 'Enter' && ev.key !== ' ') return;
      var el = ev.target && ev.target.closest ? ev.target.closest('[data-r93-att-file]') : null;
      if (!el) return;
      ev.preventDefault();
      attShow(el);
    });
    /* ★ r109 第十五拍 ③：**任务产物卡整体可点**（邵先生：「'任务产物'里的卡片文件
       也要支持点击后展开右栏浏览」）。原状只有卡里那枚 `.td-diff-btn`「预览」按钮挂了
       `[data-td-art]` 委托 ⇒ 点卡片空白处没反应。这里把委托挂到**卡本身**
       （`[data-td-art]` 早就在卡上，panel.css 19.0-④ 也早给了它 `cursor: pointer`）。
       ⚠ `prevShow()` 内部用 `btn.closest('.td-sum-art')` 取宿主 ⇒ 传卡或传按钮**等价**，
         所以下面那段 `artBtns` 循环可以原样留着（点按钮时原生 click 冒到 document 也走
         同一函数 ⇒ 连点两次仍是同一枚页签：`openTab` 命中即 `activate`，不重复开）。 */
    document.addEventListener('click', function (ev) {
      var el = ev.target && ev.target.closest ? ev.target.closest('[data-td-art]') : null;
      if (el) prevShow(el);
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key !== 'Enter' && ev.key !== ' ') return;
      var el = ev.target && ev.target.closest ? ev.target.closest('[data-td-art]') : null;
      if (!el) return;
      ev.preventDefault();
      prevShow(el);
    });
  })();
  /* ★ r109 第十五拍 ④：点回一枚**文件页签**时，把它自己的内容装回预览面板。
     `tabActivate` 只负责「点亮哪一枚页签」，面板内容的切换落在这里 —— 委托挂 `tabsEl`
     （页签是动态建 / 删的，挂在容器上才不会随新建丢监听）。 */
  tabsEl.addEventListener('click', function (ev) {
    var tab = ev.target && ev.target.closest ? ev.target.closest('[data-td-tab]') : null;
    if (!tab || (ev.target.closest && ev.target.closest('[data-td-tab-x]'))) return;
    var f = tab.getAttribute('data-td-file');
    if (f) prevShowFile(f);
  });
