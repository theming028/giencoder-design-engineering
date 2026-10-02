(function () {
  /* 定点解剖：按坐标取元素并逐级上溯，报出「谁在画面」——
     backgroundColor / backgroundImage / boxShadow / backdropFilter / borderColor，
     覆盖 background-color 之外的亮色来源（渐变、内阴影、伪元素由祖先带出）。 */
  var PTS = [
    ['输入框面板中心', 865, 453],
    ['输入框面板边缘', 400, 340],
    ['左侧激活项', 77, 111],
    ['顶部分段控件', 832, 24],
    ['标题栏左（红绿灯）', 40, 17],
    ['顶栏右侧', 1267, 24],
    ['问候语文字', 865, 327],
    ['侧栏空白', 120, 620],
    ['主区空白', 1200, 620]
  ];
  function desc(el) {
    var c = (typeof el.className === 'string' ? el.className : '');
    return el.tagName.toLowerCase() + (c ? '.' + c.trim().split(/\s+/).slice(0, 3).join('.') : '');
  }
  function snap(el) {
    var s = getComputedStyle(el);
    return {
      d: desc(el),
      bg: s.backgroundColor,
      bgi: s.backgroundImage.slice(0, 110),
      sh: s.boxShadow.slice(0, 110),
      bdf: s.backdropFilter || s.webkitBackdropFilter || 'none',
      bd: s.borderTopColor + ' ' + s.borderTopWidth,
      col: s.color
    };
  }
  var out = [];
  PTS.forEach(function (p) {
    var el;
    try { el = document.elementFromPoint(p[1], p[2]); } catch (e) { el = null; }
    if (!el) { out.push({ at: p[0], found: false }); return; }
    var chain = [], c = el, g = 0;
    while (c && g++ < 6) { chain.push(snap(c)); c = c.parentElement; }
    out.push({ at: p[0], xy: [p[1], p[2]], found: true, chain: chain });
  });
  return JSON.stringify({
    page: location.pathname.split('/').pop(),
    attr: document.documentElement.getAttribute('giencoder-theme'),
    pts: out
  });
})()
