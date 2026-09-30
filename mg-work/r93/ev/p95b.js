(function () {
  function rect(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(el, pe) { return getComputedStyle(el, pe || null); }
  function cls(el) { var c = el.className; return (c && c.baseVal !== undefined) ? c.baseVal : (c || ''); }
  var out = {};
  out.vw = innerWidth;
  var sc = document.querySelector('.r93-conv-host .r93-scroll');
  out.scroll = { r: rect(sc), cw: sc.clientWidth, ow: sc.offsetWidth, gutter: cs(sc).scrollbarGutter, sbw: sc.offsetWidth - sc.clientWidth };
  var wrap = document.querySelector('.r93-conv-host .r93-wrap');
  out.wrap = { r: rect(wrap), w: cs(wrap).width, pad: cs(wrap).padding };
  var bot = document.querySelector('.r93-conv-host .r93-bottom');
  out.bottom = { r: rect(bot), w: cs(bot).width };
  out.botKids = [];
  if (bot) for (var i = 0; i < bot.children.length; i++) { var k = bot.children[i]; out.botKids.push({ c: cls(k).slice(0, 30), r: rect(k), w: cs(k).width }); }
  out.itBlocks = [];
  var wn = wrap ? wrap.children : [];
  for (var j = 0; j < wn.length; j++) { out.itBlocks.push({ c: cls(wn[j]).slice(0, 30), r: rect(wn[j]) }); }
  function one(sel) { var e = document.querySelector(sel); return e ? { c: cls(e).slice(0, 46), r: rect(e), w: cs(e).width } : null; }
  out.ctx = one('.r93-card--ctx');
  out.todo = one('.r93-todocard');
  out.bub = one('.r93-bub');
  out.alert = one('.r93-alert');
  out.diff = one('.r93-diff');
  out.arts = one('.r93-arts');
  out.artcard = one('.r93-artcard');
  out.note = one('.r93-note');
  out.tb = one('.r93-tbsticky');
  out.tbbtn = one('.r93-tobottom');
  var mt8 = document.querySelector('main .flex-1.justify-center > div.mt-8');
  var outer = mt8 ? mt8.children[0] : null;
  out.outer = outer ? { r: rect(outer), w: cs(outer).width } : null;
  var ta = document.querySelector('main .flex-1.justify-center textarea');
  if (ta) { var p = ta.closest('div.relative'); out.inputCard = { c: cls(p).slice(0, 50), r: rect(p), w: cs(p).width }; }
  out.doc = [document.documentElement.scrollWidth, document.documentElement.scrollHeight];
  out.win = [innerWidth, innerHeight];
  return JSON.stringify(out);
})()
