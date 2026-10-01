/* r108 第十九拍 · 回归重测（改了 `toggleMenu` 的时序 ⇒ 必须把依赖它的旧路径全量重跑）
   覆盖：① 四枚下拉都能开且位置对（含是否真的跑过渡）；② Esc 分层（关菜单不关侧栏）；
        ③ `+` 菜单选完能切模块；④ 右键菜单仍可用；⑤ 收起侧栏仍可用；⑥ 页签切换仍可用。 */
(function () {
  var M = window.__M || 'x';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(e, p) { return e ? getComputedStyle(e)[p] : null; }
  var out = { phase: M };

  function act(mod) {
    var t = qa('.td-browse-tabs [data-td-tab]').filter(function (x) {
      return x.getAttribute('data-td-mod') === mod;
    })[0];
    if (t) { t.click(); return 'tab:' + mod; }
    var o = q('[data-td-open-mod="' + mod + '"]');
    if (o) { o.click(); return 'open:' + mod; }
    return 'miss:' + mod;
  }
  function menuInfo(sel, label) {
    var m = q(sel);
    if (!m) return { label: label, miss: 1 };
    var open = !m.hasAttribute('hidden');
    return { label: label, open: open, box: r(m), off: [m.offsetLeft, m.offsetTop],
      vis: cs(m, 'visibility'), op: cs(m, 'opacity'),
      anims: m.getAnimations().map(function (a) { return a.transitionProperty || a.animationName; }).join('|'),
      clueless: m.style.left + '/' + m.style.top };
  }
  /* 触发器下缘与菜单上缘的差（判「菜单在触发器下方 6px」这条旧口径还在不在） */
  function dy(trigSel, menuSel) {
    var t = q(trigSel), m = q(menuSel);
    if (!t || !m || m.hasAttribute('hidden')) return null;
    return Math.round(m.getBoundingClientRect().top - t.getBoundingClientRect().bottom);
  }

  if (M === 'openSide') { out.done = act('review'); }
  if (M === 'base') {
    out.browse = r(q('.td-browse'));
    out.sidebarOn = /av-browse-on/.test((q('.td-browse') && q('.td-browse').parentElement ? q('.td-browse').parentElement.parentElement.className : '') || '');
    out.tabs = qa('.td-browse-tabs [data-td-tab]').map(function (t) { return t.getAttribute('data-td-mod'); });
  }
  /* ① 四枚下拉：逐个开 → 读；再关 */
  if (M === 'openMod') { var b = q('[data-td-add]'); if (b) b.click(); out.clicked = 1; }
  /* ★ 硬规则 25 ②：判「过渡到底跑没跑」必须在**同一次 eval 内**点开 + 立刻读
     （拆成两次 eval 时 700ms 早把 0.2s 的过渡跑完了 ⇒ `getAnimations()` 空 = 假阴性）。 */
  if (M === 'peekMod') { var p1 = q('[data-td-add]'); if (p1) p1.click();
    out.anims = q('.td-mod-menu').getAnimations().map(function (a) { return a.transitionProperty; }).join('|');
    out.op0 = cs(q('.td-mod-menu'), 'opacity'); out.sc0 = cs(q('.td-mod-menu'), 'scale'); }
  if (M === 'peekOpts') { var p2 = q('[data-td-rv-opts]'); if (p2) p2.click();
    out.anims = q('.td-rv-opts').getAnimations().map(function (a) { return a.transitionProperty; }).join('|');
    out.op0 = cs(q('.td-rv-opts'), 'opacity'); }
  if (M === 'peekScope') { var p3 = q('[data-td-rv-scope]'); if (p3) p3.click();
    out.anims = q('.td-rv-scope-menu').getAnimations().map(function (a) { return a.transitionProperty; }).join('|');
    out.op0 = cs(q('.td-rv-scope-menu'), 'opacity'); }
  if (M === 'peekCommit') { var p4 = q('[data-td-commit]'); if (p4) p4.click();
    out.anims = q('.td-commit-menu').getAnimations().map(function (a) { return a.transitionProperty; }).join('|');
    out.op0 = cs(q('.td-commit-menu'), 'opacity'); }
  if (M === 'readMod') { out.mod = menuInfo('.td-mod-menu', 'mod'); out.modDy = dy('[data-td-add]', '.td-mod-menu');
    out.items = qa('.td-mod-menu .td-mm-item').map(function (i) { var n = i.querySelector('.td-mm-name'); return n ? n.textContent : '?'; }); }
  if (M === 'openOpts') { var b2 = q('[data-td-rv-opts]'); if (b2) b2.click(); out.clicked = 1; }
  if (M === 'readOpts') { out.opts = menuInfo('.td-rv-opts', 'opts'); out.optsDy = dy('[data-td-rv-opts]', '.td-rv-opts'); }
  if (M === 'openScope') { var b3 = q('[data-td-rv-scope]'); if (b3) b3.click(); out.clicked = 1; }
  if (M === 'readScope') { out.scope = menuInfo('.td-rv-scope-menu', 'scope'); out.scopeDy = dy('[data-td-rv-scope]', '.td-rv-scope-menu'); }
  if (M === 'openCommit') { var b4 = q('[data-td-commit]'); if (b4) b4.click(); out.clicked = 1; }
  if (M === 'readCommit') { out.commit = menuInfo('.td-commit-menu', 'commit'); out.commitDy = dy('[data-td-commit]', '.td-commit-menu'); }
  if (M === 'closeAll') {
    var b5 = q('[data-td-add]'); if (b5 && !q('.td-mod-menu').hasAttribute('hidden')) b5.click();
    var b6 = q('[data-td-rv-opts]'); if (b6 && !q('.td-rv-opts').hasAttribute('hidden')) b6.click();
    var b7 = q('[data-td-rv-scope]'); if (b7 && !q('.td-rv-scope-menu').hasAttribute('hidden')) b7.click();
    var b8 = q('[data-td-commit]'); if (b8 && !q('.td-commit-menu').hasAttribute('hidden')) b8.click();
    out.openLeft = qa('.giencoder-dropdown-popup').filter(function (m) { return !m.hasAttribute('hidden'); }).length;
  }
  /* ② Esc 分层：只开「显示选项」时按 Esc ⇒ 菜单收、侧栏留（相位只报「此刻」的状态，
     按 Esc 前后各调一次，由外部比对） */
  if (M === 'openOptsOnly') { var c1 = q('[data-td-rv-opts]'); if (c1) c1.click(); out.clicked = 1; }
  if (M === 'escState') {
    var sb = q('.td-browse').parentElement.parentElement;
    out.sidebarOn = /av-browse-on/.test(sb.className);
    out.optsOpen = !q('.td-rv-opts').hasAttribute('hidden');
    out.openMenus = qa('.giencoder-dropdown-popup').filter(function (m) { return !m.hasAttribute('hidden'); })
      .map(function (m) { return m.className.split(' ')[0]; });
  }
  /* ③ `+` 菜单选完能切模块 */
  if (M === 'pickTerm') {
    var it = q('.td-mod-menu [data-td-open-mod="terminal"]');
    if (it) { it.click(); out.picked = 1; }
  }
  if (M === 'paneState') {
    out.activeTab = (function () { var t = q('.td-browse-tabs .is-active'); return t ? t.getAttribute('data-td-mod') : null; })();
    out.visiblePanes = qa('[data-td-pane]').filter(function (p) { return !p.hasAttribute('hidden'); }).map(function (p) { return p.getAttribute('data-td-pane'); });
    out.allMenusClosed = qa('.giencoder-dropdown-popup').every(function (m) { return m.hasAttribute('hidden'); });
  }
  /* ④ 右键菜单仍可用（合成 contextmenu，与前几拍同法） */
  if (M === 'ctxOpen') {
    var row = q('.td-rv-body .td-dr') || q('.td-rv-body .td-diff');
    if (row) {
      var bb = row.getBoundingClientRect();
      row.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true,
        clientX: Math.round(bb.left + 40), clientY: Math.round(bb.top + 10) }));
      out.fired = 1;
    }
  }
  if (M === 'ctxRead') { out.ctx = menuInfo('.td-ctxmenu', 'ctx'); }
  /* ⑤ 收起侧栏 */
  if (M === 'closeSidebar') { var c2 = q('[data-td-browse-close]'); if (c2) c2.click(); out.clicked = 1; }
  if (M === 'sidebarState') {
    var sb2 = q('.td-browse').parentElement.parentElement;
    out.sidebarOn = /av-browse-on/.test(sb2.className);
    out.browse = r(q('.td-browse'));
  }
  /* ⑥ 页签切换 */
  if (M === 'switchTab') { out.done = act('summary'); }
  return out;
})();
