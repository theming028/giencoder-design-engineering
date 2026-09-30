JSON.stringify((function () {
  function clip(s, n) { s = String(s || '').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n) + '…' : s; }
  var out = {};
  var aside = document.querySelector('aside');
  var main = document.querySelector('main');
  out.viewport = innerWidth + 'x' + innerHeight;
  out.mainRect = main ? (function (r) { return [r.x, r.y, r.width, r.height]; })(main.getBoundingClientRect()) : null;
  out.mainKids = main ? [].slice.call(main.children).map(function (c) {
    return { tag: c.tagName, cls: clip(c.className, 110), rect: (function (r) { return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; })(c.getBoundingClientRect()) };
  }) : null;
  out.mainInnerKids = (main && main.firstElementChild) ? [].slice.call(main.firstElementChild.children).map(function (c) {
    return { tag: c.tagName, cls: clip(c.className, 110), rect: (function (r) { return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; })(c.getBoundingClientRect()) };
  }) : null;

  // aside 全量按钮
  var btns = aside ? [].slice.call(aside.querySelectorAll('button')) : [];
  out.nAsideBtn = btns.length;
  out.asideBtn = btns.slice(0, 26).map(function (b, i) {
    var r = b.getBoundingClientRect();
    return { i: i, cls: clip(b.className, 90), txt: clip(b.textContent, 46), rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)] };
  });
  // aside 直接子层
  out.asideTree = aside ? (function walk(el, d) {
    if (d > 3) return [];
    var o = [];
    [].slice.call(el.children).forEach(function (c) {
      var r = c.getBoundingClientRect();
      o.push({ d: d, tag: c.tagName, cls: clip(c.className, 80), rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)] });
      o = o.concat(walk(c, d + 1));
    });
    return o;
  })(aside, 0) : null;
  // localStorage 可用的路由 API
  out.lskeys = Object.keys(localStorage);
  out.hash = location.hash;
  return out;
})())
