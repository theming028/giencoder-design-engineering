(function () {
  var out = {};
  function walk(el, depth, max) {
    var r = el.getBoundingClientRect();
    var c = getComputedStyle(el);
    return {
      d: depth,
      tag: el.tagName,
      cls: (typeof el.className === 'string' ? el.className : '').slice(0, 90),
      txt: (el.childElementCount ? '' : (el.textContent || '').trim().slice(0, 60)),
      wh: Math.round(r.width) + 'x' + Math.round(r.height),
      xy: Math.round(r.left) + ',' + Math.round(r.top),
      us: c.userSelect, pe: c.pointerEvents, pos: c.position, z: c.zIndex,
      disp: c.display, ov: c.overflow,
      kids: depth < max ? Array.prototype.map.call(el.children, function (k) { return walk(k, depth + 1, max); }) : []
    };
  }
  var card = null;
  var all = document.querySelectorAll('main div');
  for (var i = 0; i < all.length; i++) {
    var cl = all[i].className || '';
    if (typeof cl === 'string' && cl.indexOf('rounded-[16px]') >= 0 && cl.indexOf('bg-white') >= 0) { card = all[i]; break; }
  }
  out.cardFound = !!card;
  if (card) {
    out.tree = walk(card, 0, 3);
  }
  return JSON.stringify(out);
})()
