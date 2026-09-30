(function () {
  var out = { page: location.pathname.split('/').pop(), items: [] };
  var sels = [].slice.call(document.querySelectorAll('.giencoder-select'));
  for (var i = 0; i < sels.length; i++) {
    var s = sels[i];
    var v = s.querySelector('.giencoder-select-view');
    var b = s.getBoundingClientRect();
    if (b.width < 1 && sels.length > 6) continue;   // 跳掉折叠/隐藏的
    out.items.push({
      cls: (s.className || '').toString(),
      box: [+b.width.toFixed(1), +b.height.toFixed(1)],
      selStyleAttr: s.getAttribute('style') || '(无)',
      viewCls: v ? (v.className || '').toString() : '(无 view)',
      viewStyleAttr: v ? (v.getAttribute('style') || '(无)') : '(无 view)',
      viewRadius: v ? getComputedStyle(v).borderTopLeftRadius : null,
      viewShadow: v ? getComputedStyle(v).boxShadow : null,
      ringVar: v ? (getComputedStyle(v).getPropertyValue('--select-ring') || '(未定义)').trim() : null,
      txt: (s.querySelector('.giencoder-select-view-text') || {}).textContent || null,
      outer: s.outerHTML.slice(0, 230)
    });
  }
  return JSON.stringify(out, null, 1);
})()
