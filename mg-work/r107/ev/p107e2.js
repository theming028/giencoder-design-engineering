(function () {
  var pane = document.querySelector('.td-browse');
  var out = {};
  function R(el, tag) {
    if (!el) { out[tag] = null; return; }
    var c = getComputedStyle(el), r = el.getBoundingClientRect();
    out[tag] = {
      cls: String(el.className).slice(0, 88), hidden: el.hasAttribute('hidden'),
      vis: c.visibility, op: c.opacity, disp: c.display, pos: c.position,
      bg: c.backgroundColor, bw: c.borderTopWidth, rad: c.borderTopLeftRadius,
      sh: c.boxShadow.slice(0, 34), pad: c.padding, gap: c.gap, anim: c.animationName,
      w: Math.round(r.width * 100) / 100, h: Math.round(r.height * 100) / 100,
      x: Math.round(r.x), y: Math.round(r.y), ovfY: c.overflowY, maxH: c.maxHeight
    };
  }
  /* ① 「+」菜单（此刻已由脚本打开且真鼠标 hover 在第二个条目上） */
  var m = pane.querySelector('.td-mod-menu');
  R(m, 'modMenu');
  var its = m.querySelectorAll('.giencoder-dropdown-item');
  out.modItems = [];
  for (var i = 0; i < its.length; i++) {
    var ic = getComputedStyle(its[i]), ir = its[i].getBoundingClientRect();
    out.modItems.push({
      t: its[i].textContent.trim().slice(0, 6), hover: its[i].matches(':hover'),
      bg: ic.backgroundColor, pad: ic.padding, rad: ic.borderTopLeftRadius,
      lh: ic.lineHeight, fs: ic.fontSize, gap: ic.gap, bd: ic.borderTopWidth,
      h: Math.round(ir.height * 100) / 100
    });
  }
  R(m.querySelector('.td-mm-cap'), 'cap');
  R(m.querySelector('.td-mm-ico'), 'ico');
  pane.querySelector('[data-td-add]').click();
  out.afterCloseHidden = m.hasAttribute('hidden');
  out.afterClosePopOpen = m.classList.contains('giencoder-popup-open');

  /* ② 审查模块三枚下拉 */
  pane.querySelector('[data-td-open-mod="review"]').click();
  pane.querySelector('[data-td-add]').click();
  var opts = pane.querySelector('.td-rv-opts');
  pane.querySelector('[data-td-rv-opts]').click();
  R(opts, 'optsMenu');
  out.optsItems = opts.querySelectorAll('.giencoder-dropdown-item').length;
  var sel = opts.querySelector('.giencoder-dropdown-item.is-checked');
  R(sel, 'optsChecked');
  out.checkedMark = sel && sel.querySelector('.td-mm-mark') ? getComputedStyle(sel.querySelector('.td-mm-mark')).opacity : null;
  R(opts.querySelector('.giencoder-dropdown-divider'), 'optsDivider');
  pane.querySelector('[data-td-rv-opts]').click();
  var scope = pane.querySelector('.td-rv-scope-menu');
  pane.querySelector('[data-td-rv-scope]').click();
  R(scope, 'scopeMenu');
  out.scopeItems = scope.querySelectorAll('.giencoder-dropdown-item').length;
  pane.querySelector('[data-td-rv-scope]').click();
  var cm = pane.querySelector('.td-commit-menu');
  pane.querySelector('[data-td-commit]').click();
  R(cm, 'commitMenu');
  out.commitItems = cm.querySelectorAll('.giencoder-dropdown-item').length;
  pane.querySelector('[data-td-commit]').click();

  /* ③ 右键菜单（造一个 contextmenu 事件） */
  var tgt = pane.querySelector('.td-sum-src') || pane.querySelector('.td-browse-tab');
  tgt.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 980, clientY: 320 }));
  var ctx = pane.querySelector('.td-ctxmenu');
  R(ctx, 'ctxMenu');
  out.ctxItems = ctx.querySelectorAll('.giencoder-dropdown-item').length;
  R(ctx.querySelector('.td-ctx-head'), 'ctxHead');
  out.ctxFirst = ctx.querySelector('.giencoder-dropdown-item') ? ctx.querySelector('.giencoder-dropdown-item').textContent.trim() : null;
  document.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  out.ctxClosed = ctx.hasAttribute('hidden');

  /* ④ 全页残留：menu / select 族的类名应为 0（只数 HTML 宿主，注释不算） */
  out.residue = {
    'giencoder-select-popup': pane.querySelectorAll('.giencoder-select-popup').length,
    'giencoder-menu-item': pane.querySelectorAll('.giencoder-menu-item').length,
    'giencoder-menu-icon': pane.querySelectorAll('.giencoder-menu-icon').length,
    'dropdown-popup': pane.querySelectorAll('.giencoder-dropdown-popup').length,
    'dropdown-item': pane.querySelectorAll('.giencoder-dropdown-item').length,
    'dropdown-divider': pane.querySelectorAll('.giencoder-dropdown-divider').length
  };
  return JSON.stringify(out);
})()
