(function () {
  var out = { mode: (window.__giTheme && window.__giTheme.mode) || '?', theme: document.documentElement.getAttribute('giencoder-theme'), items: [], bad: [], probe: 'model-dd' };
  var root = document.querySelector('[role="menu"], .model-dropdown-menu');
  if (!root) {
    // 退一步：全页找带 model-dropdown-menu-item 的元素
    var any = document.querySelector('.model-dropdown-menu-item');
    if (!any) { out.err = 'no-dropdown'; return JSON.stringify(out); }
    root = any.parentElement;
  }
  out.rootTag = root.className || root.tagName;
  out.rootBg = getComputedStyle(root).backgroundColor;
  var els = document.querySelectorAll('.model-dropdown-menu-item');
  out.n = els.length;
  Array.prototype.forEach.call(els, function (el, i) {
    if (i > 12) return;
    var cs = getComputedStyle(el);
    var span = el.querySelector('span');
    var scs = span ? getComputedStyle(span) : null;
    var path = el.querySelector('path');
    var pcs = path ? getComputedStyle(path) : null;
    var rect = el.getBoundingClientRect();
    var o = {
      i: i,
      txt: (el.textContent || '').trim().slice(0, 18),
      w: Math.round(rect.width), h: Math.round(rect.height),
      bg: cs.backgroundColor,
      spanColor: scs ? scs.color : null,
      pathFill: pcs ? pcs.fill : null,
      pathAttr: path ? path.getAttribute('fill') : null
    };
    out.items.push(o);
    [o.bg, o.spanColor, o.pathFill].forEach(function (v) {
      if (v && v.indexOf('rgb(0, 0, 0)') === 0) out.bad.push(o.txt + ':' + v);
    });
  });
  // 也把页面里所有 var() 未解析的 SVG/文本颜色扫一遍
  out.unresolved = 0;
  Array.prototype.forEach.call(document.querySelectorAll('[style*="var("]'), function (el) {
    var cs = getComputedStyle(el);
    ['color', 'backgroundColor', 'fill', 'stroke'].forEach(function (k) {
      var v = cs[k];
      if (v && (v === '' || v.indexOf('var(') >= 0)) out.unresolved++;
    });
  });
  return JSON.stringify(out);
})()
