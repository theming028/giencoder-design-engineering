(function () {
  function lum(c) {
    var m = String(c).match(/[\d.]+/g);
    if (!m || m.length < 3) return null;
    function f(x) { x = x / 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }
    return 0.2126 * f(+m[0]) + 0.7152 * f(+m[1]) + 0.0722 * f(+m[2]);
  }
  function vis(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  var map = {}, i, el, all = document.querySelectorAll('body *');
  for (i = 0; i < all.length; i++) {
    el = all[i];
    if (!vis(el)) continue;
    var cs = getComputedStyle(el);
    var lb = lum(cs.backgroundColor), lf = lum(cs.color);
    var needBg = (lb !== null && lb > 0.55);
    var needFg = (lf !== null && lf < 0.20);
    if (!needBg && !needFg) continue;
    var cls = (typeof el.className === 'string' ? el.className : '');
    var inl = el.getAttribute('style') || '';
    var key = cls + '@@' + inl;
    if (map[key]) { map[key].n++; continue; }
    map[key] = {
      n: 1, tag: el.tagName.toLowerCase(), cls: cls.slice(0, 170), inline: inl.slice(0, 150),
      bg: cs.backgroundColor, fg: cs.color,
      box: [Math.round(el.getBoundingClientRect().width), Math.round(el.getBoundingClientRect().height)],
      needBg: needBg, needFg: needFg,
      ibg: el.style.backgroundColor || '', ic: el.style.color || ''
    };
  }
  var items = [];
  for (var k in map) if (map.hasOwnProperty(k)) items.push(map[k]);
  items.sort(function (a, b) { return b.n - a.n; });
  return JSON.stringify({ page: location.pathname.split('/').pop(), groups: items.length, items: items.slice(0, 55) });
})()
