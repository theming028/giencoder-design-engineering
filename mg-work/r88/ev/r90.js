(function () {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {
      x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(2), h: +r.height.toFixed(2),
      pad: cs.padding, radius: cs.borderRadius, bg: cs.backgroundColor, bc: cs.borderColor,
      col: cs.color, fs: cs.fontSize, lh: cs.lineHeight, box: cs.boxShadow.slice(0, 60),
      cls: (el.className || '').toString().slice(0, 120)
    };
  }
  var out = {};
  var aside = document.querySelector('aside');
  var host = document.querySelector('.r85-nav-host');
  if (aside && host) {
    var A = aside.getBoundingClientRect(), H = host.getBoundingClientRect();
    out.aside = { x: A.x, w: A.width };
    out.host = { w: +H.width.toFixed(1), relL: +(H.x - A.x).toFixed(1), relR: +((A.x + A.width) - (H.x + H.width)).toFixed(1) };
    var nav = document.querySelector('.r85-nav').getBoundingClientRect();
    out.nav = { w: +nav.width.toFixed(1), relL: +(nav.x - A.x).toFixed(1), relR: +((A.x + A.width) - (nav.x + nav.width)).toFixed(1) };
    var nv = document.querySelector('.r85-navi');
    if (nv) {
      var N = nv.getBoundingClientRect();
      out.navi = { w: +N.width.toFixed(1), relL: +(N.x - A.x).toFixed(1), relR: +((A.x + A.width) - (N.x + N.width)).toFixed(1) };
    }
  }
  var p = document.querySelector('.r88-arch');
  if (!p) { out.err = 'arch page missing'; return JSON.stringify(out); }
  var P = p.getBoundingClientRect();
  function rel(el) { var b = box(el); if (!b) return b; b.rx = +(b.x - P.x).toFixed(1); b.ry = +(b.y - P.y).toFixed(1); return b; }

  out.clear = rel(p.querySelector('.r88-arch-clear'));
  out.search = rel(p.querySelector('.r88-arch-search'));
  out.proj = rel(p.querySelector('.r88-arch-proj'));
  var pre = p.querySelector('.r88-sel-prefix');
  out.prefix = rel(pre);
  if (pre) {
    var svg = pre.querySelector('svg');
    out.prefixSvg = rel(svg);
    out.prefixSvgViewBox = svg.getAttribute('viewBox');
  }
  var row = p.querySelector('.r88-arch-row');
  out.row = rel(row);
  var act = row ? row.querySelector('.r88-arch-act') : null;
  out.act = rel(act);
  var acts = row ? row.querySelector('.r88-arch-acts') : null;
  out.acts = rel(acts);
  var acts2 = row ? row.querySelectorAll('.r88-arch-act') : [];
  if (acts2.length >= 2) {
    var b0 = acts2[0].getBoundingClientRect(), b1 = acts2[1].getBoundingClientRect();
    out.actPair = {
      a: [+b0.x.toFixed(1), +b0.y.toFixed(1), +b0.width.toFixed(2), +b0.height.toFixed(2)],
      b: [+b1.x.toFixed(1), +b1.y.toFixed(1), +b1.width.toFixed(2), +b1.height.toFixed(2)],
      gap: +(b1.x - (b0.x + b0.width)).toFixed(1),
      rightEdge: +(b1.x + b1.width - P.x).toFixed(1)
    };
    out.actFmt = {
      cls: acts2[0].className,
      radius: getComputedStyle(acts2[0]).borderRadius,
      bc: getComputedStyle(acts2[0]).borderColor,
      bg: getComputedStyle(acts2[0]).backgroundColor,
      col: getComputedStyle(acts2[0]).color,
      shadow: getComputedStyle(acts2[0]).boxShadow.slice(0, 70),
      iconSvgs: acts2[0].querySelectorAll('svg').length
    };
  }
  var ic = p.querySelector('.r88-arch-mic svg');
  if (ic) { out.micSvg = { vb: ic.getAttribute('viewBox'), w: +ic.getBoundingClientRect().width.toFixed(1) }; out.micPath = ic.innerHTML.slice(0, 200); }
  out.pageW = +P.width.toFixed(1);
  return JSON.stringify(out);
})()
