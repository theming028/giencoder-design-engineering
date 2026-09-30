(function () {
  function cs(el, pe) { return getComputedStyle(el, pe || null); }
  function rect(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cls(el) { var c = el.className; return (c && c.baseVal !== undefined) ? c.baseVal : (c || ''); }
  function bg(el, pe) {
    if (!el) return null;
    var s = cs(el, pe);
    return { bi: (s.backgroundImage || '').slice(0, 160), bg: s.backgroundColor, bs: s.backgroundSize, pos: s.position, z: s.zIndex, op: s.opacity, disp: s.display };
  }
  var out = {};
  var m = document.querySelector('main');
  out.mainCls = cls(m);
  out.main = bg(m);
  out.mainBefore = bg(m, '::before');
  out.mainAfter = bg(m, '::after');
  var hero = document.querySelector('main > div > div.flex-1.justify-center');
  out.hero = { r: rect(hero), bg: cs(hero).backgroundColor, bi: cs(hero).backgroundImage.slice(0, 110) };
  var wrap = document.querySelector('.r93-wrap');
  out.wrap = { bg: cs(wrap).backgroundColor };
  var rg = [];
  Array.prototype.forEach.call(document.querySelectorAll('*'), function (el) {
    var s = getComputedStyle(el);
    if (s.backgroundImage && s.backgroundImage.indexOf('radial-gradient') >= 0) rg.push({ c: cls(el).slice(0, 95), r: rect(el) });
  });
  out.radialAll = rg.slice(0, 14);
  return JSON.stringify(out);
})()
