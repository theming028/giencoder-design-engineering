/* r108 第十七拍（第六层补丁）· 现状取证探针。
   相位（window.__M）：base / menuOpen / menu / rvOpen / treeOpen / tree / fs18 / fs14
   ⚠ 「点击」与「读值」分帧（硬规则 29）；⚠ 采集必须同一次 eval 内完成（硬规则 25 ②）。 */
(function () {
  var M = window.__M || 'base';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function act(m) {
    var t = qa('.td-browse-tabs [data-td-tab]').filter(function (x) { return x.getAttribute('data-td-mod') === m; })[0];
    if (t) { t.click(); return 'tab:' + m; }
    var b = qa('[data-td-open-mod="' + m + '"]')[0];
    if (b) { b.click(); return 'open:' + m; }
    return 'miss:' + m;
  }
  function barH() { var b = q('.td-browse-bar'); return b ? Math.round(b.getBoundingClientRect().height) : null; }

  var out = {};
  if (M === 'base') {
    out.browse = r(q('.td-browse'));
    out.bar = r(q('.td-browse-bar'));
    out.barH = barH();
    out.addBtn = r(q('[data-td-add]'));
    out.tabs = qa('.td-browse-tabs [data-td-tab]').map(function (t) { return [t.getAttribute('data-td-mod'), r(t)]; });
    out.brwActs = qa('[data-td-brw-act]').map(function (b) { return b.getAttribute('data-td-brw-act'); });
    out.rows = qa('.td-diff-rows').map(function (e) { return [e.className, e.querySelectorAll('.td-dr,.td-dsc').length]; });
    out.moreBtns = qa('[data-td-more]').map(function (b) { return b.textContent.trim(); });
    out.moreRow = qa('[data-td-more-row]').length;
    out.treeR = r(q('.td-tree'));
  }
  if (M === 'menuOpen') { var b0 = q('[data-td-add]'); if (b0) b0.click(); out.clicked = !!b0; }
  if (M === 'menu') {
    var m = q('.td-mod-menu'), a = q('[data-td-add]');
    out.menu = r(m); out.addBtn = r(a);
    out.hidden = m ? m.hasAttribute('hidden') : null;
    out.menuCls = m ? m.className : null;
    out.inlineStyle = m ? (m.getAttribute('style') || '') : null;
    out.offsetParent = m && m.offsetParent ? m.offsetParent.className : null;
    if (m && a) {
      var mb = m.getBoundingClientRect(), ab = a.getBoundingClientRect();
      out.dx = Math.round(mb.left - ab.left);
      out.dy = Math.round(mb.top - ab.bottom);
    }
  }
  if (M === 'menuClose') { var b1 = q('[data-td-add]'); if (b1) b1.click(); out.clicked = !!b1; }
  if (M === 'addTabs') {
    /* 多开两个页签，看 `+` 是否右移、菜单是否跟着走 */
    act('terminal'); act('browser');
    out.act = 'terminal+browser';
    out.tabs = qa('.td-browse-tabs [data-td-tab]').map(function (t) { return t.getAttribute('data-td-mod'); });
    out.addBtn = r(q('[data-td-add]'));
  }
  if (M === 'rvOpen') { out.act = act('review'); }
  if (M === 'treeOpen') { var t0 = q('[data-td-rv-act="tree"]'); if (t0) t0.click(); out.clicked = !!t0; }
  if (M === 'tree') {
    out.tree = r(q('.td-tree'));
    out.scrim = r(q('.td-tree-scrim'));
    out.panel = r(q('.td-tree-panel'));
    out.bar = r(q('.td-browse-bar'));
    out.browse = r(q('.td-browse'));
    out.treeTop = q('.td-tree') ? getComputedStyle(q('.td-tree')).top : null;
  }
  if (M === 'treeClose') { var x0 = q('.td-tree [data-td-tree-x]'); if (x0) x0.click(); out.clicked = !!x0; }
  if (M === 'fs18') { document.documentElement.style.setProperty('--ui-fs', '18'); out.barH = barH(); out.uiFs = getComputedStyle(document.documentElement).getPropertyValue('--ui-fs'); }
  if (M === 'fs14') { document.documentElement.style.removeProperty('--ui-fs'); out.barH = barH(); out.uiFs = getComputedStyle(document.documentElement).getPropertyValue('--ui-fs'); }
  return JSON.stringify(out);
})()
