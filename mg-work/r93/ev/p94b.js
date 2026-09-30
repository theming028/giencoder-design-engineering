(function () {
  function rect(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cls(el) { var c = el.className; return (c && c.baseVal !== undefined) ? c.baseVal : (c || ''); }
  function info(el, depth) {
    var cs = getComputedStyle(el);
    var o = { t: el.tagName.toLowerCase(), c: cls(el), r: rect(el) };
    var bi = cs.backgroundImage;
    if (bi && bi !== 'none') o.bi = bi.slice(0, 110);
    if (cs.opacity !== '1') o.op = cs.opacity;
    if (cs.position !== 'static') o.pos = cs.position;
    if (cs.display !== 'block' && cs.display !== 'flex') o.dis = cs.display;
    if (depth > 0) { o.k = []; for (var i = 0; i < el.children.length; i++) o.k.push(info(el.children[i], depth - 1)); }
    return o;
  }
  var out = {};
  var hero = document.querySelector('main > div > div.flex-1.justify-center');
  out.hero = hero ? { r: rect(hero), cls: cls(hero) } : null;
  var mt8 = document.querySelector('main .flex-1.justify-center > div.mt-8');
  out.mt8 = mt8 ? info(mt8, 3) : null;
  var bar = document.querySelector('.r93-bar');
  out.bar = bar ? { r: rect(bar), cls: cls(bar) } : null;
  var cap = document.querySelector('.r93-seg-cap');
  out.cap = cap ? { r: rect(cap), nw: Math.round(cap.getBoundingClientRect().width) } : null;
  var seg = document.querySelector('.r93-seg');
  out.seg = seg ? { r: rect(seg) } : null;
  var more = document.querySelector('.r93-morebtn');
  out.more = more ? { r: rect(more) } : null;
  var wrap = document.querySelector('.r93-wrap');
  out.wrap = wrap ? { r: rect(wrap), ws: getComputedStyle(wrap).width, minw: getComputedStyle(wrap).minWidth } : null;
  var host = document.querySelector('.r93-conv-host');
  out.host = host ? { r: rect(host) } : null;
  var card = document.querySelector('.r93-card--ctx');
  out.ctx = card ? { r: rect(card), mh: getComputedStyle(card).maxHeight, sh: card.scrollHeight, ch: card.clientHeight } : null;
  out.vsbs = document.querySelectorAll('.r93-vsb').length;
  out.win = [window.innerWidth, window.innerHeight];
  out.doc = [document.documentElement.scrollWidth, document.documentElement.scrollHeight];
  return JSON.stringify(out);
})()
