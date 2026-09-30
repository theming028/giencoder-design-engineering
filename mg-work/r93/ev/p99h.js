(function () {
  var a = [].slice.call(document.querySelectorAll('svg')).filter(function (x) {
    return (x.getAttribute('viewBox') || '').indexOf('11.784') === 0 && x.getBoundingClientRect().width > 0;
  });
  if (!a.length) return 'NO';
  var s = a[0], r = s.getBoundingClientRect();
  var p = s.querySelector('path');
  var bb = p ? p.getBBox() : null;
  return JSON.stringify({
    rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)],
    outer: s.outerHTML.slice(0, 160),
    pathD: p ? p.getAttribute('d').slice(0, 60) : null,
    pathFill: p ? p.getAttribute('fill') : null,
    bbox: bb ? { x: +bb.x.toFixed(2), y: +bb.y.toFixed(2), w: +bb.width.toFixed(2), h: +bb.height.toFixed(2) } : null,
    color: getComputedStyle(s).color,
    fill: getComputedStyle(s).fill,
    pathFillComputed: p ? getComputedStyle(p).fill : null,
    opacity: getComputedStyle(s).opacity,
    parentCls: s.parentNode ? s.parentNode.className : null,
    parentColor: s.parentNode ? getComputedStyle(s.parentNode).color : null
  });
})();
