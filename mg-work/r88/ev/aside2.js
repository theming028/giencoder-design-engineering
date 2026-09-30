(function () {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    var cs = getComputedStyle(el);
    return {
      x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1),
      pad: cs.paddingTop + ' ' + cs.paddingRight + ' ' + cs.paddingBottom + ' ' + cs.paddingLeft,
      gap: cs.gap, radius: cs.borderRadius
    };
  }
  var out = {};
  var aside = document.querySelector('aside');
  if (!aside) return JSON.stringify({ err: 'no aside' });
  var A = box(aside);
  out.aside = A;

  /* 拿 aside 内第一个“像会话项”的元素（有图标 + 文字、宽 < aside 宽） */
  var cand = [].slice.call(aside.querySelectorAll('button,[role="button"],a')).filter(function (el) {
    var b = el.getBoundingClientRect();
    return b.width > 120 && b.width < A.w - 4 && b.height >= 24 && b.height <= 80;
  });
  if (cand.length) {
    var el = cand[0], b = box(el);
    b.relL = +(b.x - A.x).toFixed(1);
    b.relR = +((A.x + A.w) - (b.x + b.w)).toFixed(1);
    b.text = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 20);
    out.item = b;
    /* 内部第一个 svg 与第一个文本子节点的 x */
    var svg = el.querySelector('svg');
    if (svg) { var sb = svg.getBoundingClientRect(); b.iconX = +(sb.x - A.x).toFixed(1); b.iconW = +sb.width.toFixed(1); }
    var spans = [].slice.call(el.querySelectorAll('span,div')).filter(function (s) { return (s.textContent || '').trim(); });
    if (spans.length) { var tb = spans[spans.length - 1].getBoundingClientRect(); b.textX = +(tb.x - A.x).toFixed(1); }
  }
  /* 设置页：导航宿主与导航项 */
  var host = document.querySelector('.r85-nav-host');
  if (host) {
    var hb = box(host); hb.relL = +(hb.x - A.x).toFixed(1); hb.relR = +((A.x + A.w) - (hb.x + hb.w)).toFixed(1);
    out.navHost = hb;
    var nav = box(document.querySelector('.r85-nav'));
    nav.relL = +(nav.x - A.x).toFixed(1); nav.relR = +((A.x + A.w) - (nav.x + nav.w)).toFixed(1);
    out.nav = nav;
    var nv = document.querySelector('.r85-navi');
    if (nv) {
      var nb = box(nv); nb.relL = +(nb.x - A.x).toFixed(1); nb.relR = +((A.x + A.w) - (nb.x + nb.w)).toFixed(1);
      out.navi = nb;
      var ns = nv.querySelector('span');
      if (ns) nb.textX = +(ns.getBoundingClientRect().x - A.x).toFixed(1);
    }
    var gt = document.querySelector('.r85-gt');
    if (gt) { var gb = box(gt); gb.relL = +(gb.x - A.x).toFixed(1); out.gt = gb; }
  }
  return JSON.stringify(out);
})()
