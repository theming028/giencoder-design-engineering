/* r99 复查 C：umeta 图标几何 + rateline 线↔⋯ 间距 */
(function () {
  var out = {};
  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function R(e) { if (!e) return null; var r = e.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; }
  function g(e, p) { return e ? getComputedStyle(e)[p] : null; }
  function fx(e) { return e ? getComputedStyle(e).transform : null; }
  function vbx(s) { return s ? { vb: s.getAttribute('viewBox'), w: s.getAttribute('width'), h: s.getAttribute('height') } : null; }

  /* ---- A. umeta 图标几何 + CSS 规则原文 ---- */
  var um = q('.r93-umeta');
  var cssTxt = q('#r93-conv-css') ? q('#r93-conv-css').textContent : '';
  out.A = { html: um ? um.innerHTML.replace(/\s+/g, ' ').slice(0, 900) : null };
  out.A.icons = um ? qa('.r93-iblk', um).map(function (b) {
    var s = q('svg', b);
    return {
      cls: b.className,
      box: R(b), boxW: g(b, 'width'), boxH: g(b, 'height'),
      svg: R(s), svgW: g(s, 'width'), svgH: g(s, 'height'), svgOf: g(s, 'overflow')
    };
  }) : null;
  out.A.rules = ['.r93-iblk', '.r93-i14', '.r93-iblk > svg', '.r93-iblk>svg', '.r93-i12', '.r93-i16'].map(function (sel) {
    var re = new RegExp('\\' + sel.replace(/\./g, '\\.').replace(/ /g, '\\s*') + '\\s*\\{[^}]*\\}', 'g');
    var m = cssTxt.match(re);
    return sel + ' => ' + (m ? m.join(' | ') : 'NOT FOUND');
  });
  out.A.vb = um ? qa('.r93-iblk.r93-i14 > svg', um).map(function (s) { return vbx(s); }) : null;

  /* ---- B. rateline：线 与 ⋯ 的真实相对位置 ---- */
  var rl = q('.r93-rateline');
  if (rl) {
    var r0 = rl.getBoundingClientRect();
    var lines = qa('.r93-rline', rl);
    var more = q('.r93-rateline > .r93-rbtn', rl);
    var rate = q('.r93-rrate', rl);
    var grp = q('.r93-rgrp', rl);
    out.B = {
      row: R(rl),
      grp: grp ? [Math.round(grp.getBoundingClientRect().left - r0.left), Math.round(grp.getBoundingClientRect().right - r0.left)] : null,
      line1: lines[0] ? [Math.round(lines[0].getBoundingClientRect().left - r0.left), Math.round(lines[0].getBoundingClientRect().right - r0.left)] : null,
      rate: rate ? [Math.round(rate.getBoundingClientRect().left - r0.left), Math.round(rate.getBoundingClientRect().right - r0.left)] : null,
      line2: lines[1] ? [Math.round(lines[1].getBoundingClientRect().left - r0.left), Math.round(lines[1].getBoundingClientRect().right - r0.left)] : null,
      more: more ? [Math.round(more.getBoundingClientRect().left - r0.left), Math.round(more.getBoundingClientRect().right - r0.left)] : null,
      gapLine2More: (lines[1] && more) ? Math.round(more.getBoundingClientRect().left - lines[1].getBoundingClientRect().right) : null,
      moreML: more ? g(more, 'marginLeft') : null,
      line2ML: lines[1] ? g(lines[1], 'marginLeft') : null,
      rateML: rate ? g(rate, 'marginLeft') : null
    };
  }

  /* ---- C. 复制按钮图标（点击前）---- */
  var ib = q('.r93-umeta .r93-ib');
  out.C = ib ? { html: ib.innerHTML.replace(/\s+/g, ' ').slice(0, 300), rect: R(ib), color: g(ib, 'color') } : null;

  /* ---- D. 前端 15px 图标的字号档（页内所有 i14 的 parent 尺寸核对）---- */
  out.D = qa('.r93-iblk.r93-i14').slice(0, 8).map(function (b) {
    var s = q('svg', b);
    return { cls: b.className, b: R(b), s: R(s), vb: s ? s.getAttribute('viewBox') : null };
  });

  return JSON.stringify(out);
})();
