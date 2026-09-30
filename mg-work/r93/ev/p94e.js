(function () {
  function rect(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(el) { return getComputedStyle(el); }
  var out = {};
  var host = document.querySelector('.r93-conv-host'); out.host = host ? rect(host) : null;
  var sc = document.querySelector('.r93-scroll'); out.scroll = sc ? rect(sc) : null;
  var tb = document.querySelector('.r93-tbsticky'); out.tbWrap = tb ? rect(tb) : null;
  var btn = document.querySelector('.r93-tobottom'); out.tbBtn = btn ? rect(btn) : null;
  out.tbStyle = tb ? { pos: cs(tb).position, bottom: cs(tb).bottom, z: cs(tb).zIndex } : null;
  var hero = document.querySelector('main > div > div.flex-1.justify-center'); out.hero = hero ? rect(hero) : null;
  var ctx = document.querySelector('.r93-card--ctx');
  if (ctx) {
    var body = ctx.querySelector('.r93-ctxbody');
    var before = { sh: ctx.scrollHeight, ch: ctx.clientHeight, h: rect(ctx)[3] };
    var clone = body.cloneNode(true);
    clone.setAttribute('data-r94-probe', '1');
    ctx.appendChild(clone);
    var after = { sh: ctx.scrollHeight, ch: ctx.clientHeight, h: rect(ctx)[3] };
    ctx.scrollTop = 99999;
    var st = ctx.scrollTop;
    ctx.removeChild(clone);
    out.ctxOverflow = { before: before, after: after, scrollTopAfter: st, scrollable: after.sh > after.ch };
  }
  return JSON.stringify(out);
})()
