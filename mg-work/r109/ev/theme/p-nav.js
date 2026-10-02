(function () {
  /* 列出「左栏可点项」= 页面内的多个子屏入口（只读，不点击）。 */
  function path(el) {
    var p = [], n = 0;
    while (el && el.nodeType === 1 && el !== document.body && n < 4) {
      var s = el.tagName.toLowerCase();
      if (el.id) s += '#' + el.id;
      else {
        var c = (typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
        if (c) s += '.' + c;
      }
      p.unshift(s); el = el.parentElement; n++;
    }
    return p.join('>');
  }
  var out = [], all = document.querySelectorAll('body *'), i, el, r, cs, t;
  for (i = 0; i < all.length; i++) {
    el = all[i];
    r = el.getBoundingClientRect();
    if (r.width < 60 || r.height < 18 || r.height > 60) continue;
    if (r.x > 300) continue;                       /* 只取左栏 */
    if (r.y < 50) continue;                        /* 跳过顶栏 */
    cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    t = (el.textContent || '').replace(/\s+/g, ' ').trim();
    if (!t || t.length > 16) continue;
    if (el.children.length > 2) continue;
    out.push({ t: t, sel: path(el), x: Math.round(r.x), y: Math.round(r.y),
               w: Math.round(r.width), h: Math.round(r.height),
               role: el.getAttribute('role') || '', tag: el.tagName.toLowerCase(),
               cls: (typeof el.className === 'string' ? el.className : '').slice(0, 70) });
  }
  /* 去重：同一 y 只留最外层 */
  out.sort(function (a, b) { return a.y - b.y || b.w - a.w; });
  var keep = [], seen = {};
  out.forEach(function (o) {
    var k = o.y + '|' + o.t;
    if (seen[k]) return;
    seen[k] = 1; keep.push(o);
  });
  return JSON.stringify({ n: keep.length, items: keep });
})()
