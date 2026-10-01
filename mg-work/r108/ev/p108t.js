/* r108 第十七拍（第六层补丁）· 四条真机取证。
   相位（window.__M）：base / menuOpen / read / menuClose / openTabs / fs18 / fs14
                        rvOpen / treeOpen / treeRead / treeClose / brwShot / rvRows
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
  /* 菜单几何：菜单左缘/上缘 − 触发器左缘/下缘（对齐好的话 dx ≈ 0、dy = 6） */
  function menuGeom() {
    var m = q('.td-mod-menu'), a = q('[data-td-add]');
    if (!m || !a) return null;
    var mb = m.getBoundingClientRect(), ab = a.getBoundingClientRect();
    return {
      addBtn: [Math.round(ab.left), Math.round(ab.top), Math.round(ab.width), Math.round(ab.height)],
      menu: [Math.round(mb.left), Math.round(mb.top), Math.round(mb.width), Math.round(mb.height)],
      dx: Math.round(mb.left - ab.left),
      dy: Math.round(mb.top - ab.bottom),
      hidden: m.hasAttribute('hidden'),
      open: m.classList.contains('giencoder-popup-open'),
      inline: (m.getAttribute('style') || ''),
      offsetParent: m.offsetParent ? m.offsetParent.className : null,
      sidebarOn: !!(q('.td-browse') && q('.td-browse').className.indexOf('av-browse-on') >= 0)
    };
  }

  var out = {};
  if (M === 'base') {
    out.browse = r(q('.td-browse'));
    out.bar = r(q('.td-browse-bar'));
    out.brwActs = qa('[data-td-brw-act]').map(function (b) { return b.getAttribute('data-td-brw-act'); });
    out.shotEls = qa('[data-td-brw-act="shot"], [data-td-brw-act="zoom"], [data-td-brw-act="send"]').length;
    out.rows = qa('.td-diff-rows').map(function (e) {
      return [e.className, e.querySelectorAll('.td-dr,.td-dsc').length];
    });
  }
  if (M === 'menuOpen') { var b0 = q('[data-td-add]'); if (b0) b0.click(); out.clicked = !!b0; }
  if (M === 'read') { out.g = menuGeom(); }
  if (M === 'menuClose') { var b1 = q('[data-td-add]'); if (b1) b1.click(); out.clicked = !!b1; }
  if (M === 'openTabs') {
    act('terminal'); act('browser'); act('review');
    out.tabs = qa('.td-browse-tabs [data-td-tab]').map(function (t) { return t.getAttribute('data-td-mod'); });
  }
  if (M === 'fs18') { document.documentElement.style.setProperty('--ui-fs', '18'); out.uiFs = '18'; }
  if (M === 'fs14') { document.documentElement.style.removeProperty('--ui-fs'); out.uiFs = '14'; }
  if (M === 'rvOpen') { out.act = act('review'); }
  if (M === 'treeOpen') { var t0 = q('[data-td-rv-act="tree"]'); if (t0) t0.click(); out.clicked = !!t0; }
  if (M === 'treeRead') {
    var tr = q('.td-tree'), bar = q('.td-browse-bar'), br = q('.td-browse');
    out.tree = r(tr); out.bar = r(bar); out.browse = r(br);
    out.scrim = r(q('.td-tree-scrim')); out.panel = r(q('.td-tree-panel'));
    out.treeTop = tr ? getComputedStyle(tr).top : null;
    if (tr && bar) {
      var tb = tr.getBoundingClientRect(), bb = bar.getBoundingClientRect();
      out.treeTopVsBarBottom = Math.round(tb.top - bb.bottom);   /* 0 = 正好贴着标题栏下缘 */
      out.scrimTopVsBarBottom = Math.round(q('.td-tree-scrim').getBoundingClientRect().top - bb.bottom);
    }
  }
  if (M === 'treeClose') { var x0 = q('.td-tree-scrim'); if (x0) x0.click(); out.clicked = !!x0; }
  if (M === 'rvRows') {
    var body = q('.td-rv-body');
    out.bodyScrollH = body ? body.scrollHeight : null;
    out.bodyClientH = body ? body.clientHeight : null;
    out.rows = qa('.td-diff-rows').map(function (e) {
      var vis = 0, all = e.querySelectorAll('.td-dr,.td-dsc');
      for (var i = 0; i < all.length; i++) if (!all[i].hasAttribute('hidden')) vis++;
      return [e.className, all.length, vis];
    });
    out.openDiffs = qa('.td-diff.is-open').length;
  }
  return JSON.stringify(out);
})()
