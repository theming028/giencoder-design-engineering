(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  var ci = document.querySelector('.td-commit-in');
  if (ci) {
    var card = ci.closest('.td-commit-card');
    var cs = getComputedStyle(ci), cr = card.getBoundingClientRect(), cc = getComputedStyle(card);
    out.cardR = r(card);
    out.availW = Math.round(cr.width - parseFloat(cc.paddingLeft) - parseFloat(cc.paddingRight));
    out.ciR = r(ci); out.ciWcss = cs.width; out.ciDisp = cs.display; out.ciFlex = cs.flex;
    out.gap = Math.round(out.availW - out.ciR[2]);
    out.wrapperCS = { pad: cs.padding, box: cs.boxSizing, gap: cs.gap, maxW: cs.maxWidth, minW: cs.minWidth };
    var inp = ci.querySelector('.giencoder-input');
    out.inpR = r(inp); out.inpFlex = getComputedStyle(inp).flex; out.inpW = getComputedStyle(inp).width;
    var pre = ci.querySelector('.giencoder-input-prefix');
    out.preR = r(pre);
    out.kids = Array.prototype.map.call(ci.children, function (e) { return { cls: String(e.className).slice(0, 40), r: r(e) }; });
  } else { out.ci = 'NOT FOUND'; }
  var msg = document.querySelector('.td-commit-msg');
  out.msgR = msg ? r(msg) : null;
  var lb = document.querySelector('.td-commit-lb');
  out.lbR = lb ? r(lb) : null;
  var f = document.querySelector('.td-commit-f');
  out.fR = f ? r(f) : null;
  var h = document.querySelector('.td-commit-h');
  out.hR = h ? r(h) : null;
  out.commitHidden = (function () { var d = document.querySelector('.td-commit'); return d ? d.hasAttribute('hidden') : null; })();
  out.tabsNow = Array.prototype.map.call(document.querySelectorAll('.td-browse-tab'), function (t) { return (t.textContent || '').trim().slice(0, 8); });
  return JSON.stringify(out, null, 1);
})()
