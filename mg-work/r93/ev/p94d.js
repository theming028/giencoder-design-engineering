(function () {
  function rect(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(el, pe) { return getComputedStyle(el, pe || null); }
  function cls(el) { var c = el.className; return (c && c.baseVal !== undefined) ? c.baseVal : (c || ''); }
  var out = {};
  var bar = document.querySelector('.r93-bar'), cap = document.querySelector('.r93-seg-cap'), seg = document.querySelector('.r93-seg'), more = document.querySelector('.r93-morebtn');
  out.bar = bar ? rect(bar) : null; out.cap = cap ? rect(cap) : null; out.seg = seg ? rect(seg) : null; out.more = more ? rect(more) : null;
  if (bar && cap) {
    var b = bar.getBoundingClientRect(), c = cap.getBoundingClientRect();
    out.capCenterDelta = Math.round((c.left + c.width / 2) - (b.left + b.width / 2));
  }
  var wrap = document.querySelector('.r93-wrap');
  out.wrap = wrap ? { r: rect(wrap), ws: cs(wrap).width, minw: cs(wrap).minWidth, padL: cs(wrap).paddingLeft } : null;
  var bub = document.querySelector('.r93-bub'); out.bub = bub ? rect(bub) : null;
  var card = document.querySelector('.r93-card'); out.card = card ? rect(card) : null;
  var main = document.querySelector('main');
  out.mainBI = cs(main).backgroundImage;
  out.mainBefDisp = cs(main, '::before').display;
  var mt8 = document.querySelector('main .flex-1.justify-center > div.mt-8');
  var outer = mt8 ? mt8.children[0] : null;
  out.outer = outer ? { r: rect(outer), bg: cs(outer).backgroundColor, bi: cs(outer).backgroundImage.slice(0, 60), pad: cs(outer).padding, br: cs(outer).borderRadius, kids: outer.children.length } : null;
  if (outer) {
    out.outerKid = [];
    for (var i = 0; i < outer.children.length; i++) out.outerKid.push({ c: cls(outer.children[i]).slice(0, 55), d: cs(outer.children[i]).display, r: rect(outer.children[i]) });
  }
  var ctx = document.querySelector('.r93-card--ctx');
  out.ctx = ctx ? { r: rect(ctx), mh: cs(ctx).maxHeight, oy: cs(ctx).overflowY, sh: ctx.scrollHeight, ch: ctx.clientHeight } : null;
  out.vsb = document.querySelectorAll('.r93-vsb').length;
  out.doc = [document.documentElement.scrollWidth, document.documentElement.scrollHeight];
  out.win = [window.innerWidth, window.innerHeight];
  return JSON.stringify(out);
})()
