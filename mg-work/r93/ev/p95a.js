(function () {
  function rect(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function R(el) { return el ? rect(el) : null; }
  function cs(el, pe) { return getComputedStyle(el, pe || null); }
  function cls(el) { var c = el.className; return (c && c.baseVal !== undefined) ? c.baseVal : (c || ''); }
  var out = {};
  out.vw = window.innerWidth;
  out.main = R(document.querySelector('main'));
  var wrap = document.querySelector('.r93-conv-host .r93-wrap');
  out.wrap = wrap ? { r: R(wrap), w: cs(wrap).width, minw: cs(wrap).minWidth, pad: cs(wrap).padding, bs: cs(wrap).boxSizing } : null;
  out.scroll = R(document.querySelector('.r93-conv-host .r93-scroll'));
  out.blocks = [];
  var wnodes = wrap ? wrap.children : [];
  for (var i = 0; i < wnodes.length; i++) {
    var it = wnodes[i], k = it.firstElementChild || it;
    out.blocks.push({ c: cls(k).slice(0, 62), it: cls(it).slice(0, 20), r: R(k), w: cs(k).width, ml: cs(k).marginLeft });
  }
  var bot = document.querySelector('.r93-conv-host .r93-bottom');
  out.bottom = bot ? { r: R(bot), pad: cs(bot).padding } : null;
  out.botKids = [];
  if (bot) for (var j = 0; j < bot.children.length; j++) { var c = bot.children[j]; out.botKids.push({ c: cls(c).slice(0, 50), r: R(c), w: cs(c).width, ml: cs(c).marginLeft }); }
  var mt8 = document.querySelector('main .flex-1.justify-center > div.mt-8');
  var outer = mt8 ? mt8.children[0] : null;
  out.outer = outer ? { r: R(outer), w: cs(outer).width, pad: cs(outer).padding, bg: cs(outer).backgroundColor } : null;
  out.outerKids = [];
  if (outer) for (var m = 0; m < outer.children.length; m++) { var k2 = outer.children[m]; out.outerKids.push({ c: cls(k2).slice(0, 60), d: cs(k2).display, r: R(k2), w: cs(k2).width }); }
  var ctx = document.querySelector('.r93-card--ctx');
  out.ctx = ctx ? { r: R(ctx), w: cs(ctx).width, ml: cs(ctx).marginLeft } : null;
  out.full = (function () { var e = document.querySelector('.r93-card--full'); return e ? { r: R(e), w: cs(e).width } : null; })();
  out.todo = (function () { var e = document.querySelector('.r93-todocard'); return e ? { r: R(e), w: cs(e).width } : null; })();
  out.bub = (function () { var e = document.querySelector('.r93-bub'); return e ? { r: R(e), w: cs(e).width } : null; })();
  out.doc = [document.documentElement.scrollWidth, document.documentElement.scrollHeight];
  out.win = [window.innerWidth, window.innerHeight];
  return JSON.stringify(out);
})()
