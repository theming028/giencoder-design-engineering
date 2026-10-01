/* r106 ④c 判据：四列（wrap / bottom / composer / 骨架屏）相对外部容器 .r93-pane 的左右内间距 */
(function () {
  var L = [];
  function R(sel) {
    var e = document.querySelector(sel);
    if (!e) return null;
    var r = e.getBoundingClientRect();
    return { x: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width) };
  }
  function pad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }

  var on = !!document.querySelector('.av-browse-on');
  L.push('【' + window.innerWidth + 'x' + window.innerHeight + ' | 预览栏 ' + (on ? 'ON' : 'OFF') + '】');

  var pane = R('.r93-pane');
  L.push('  pane      ' + JSON.stringify(pane));

  var cols = [
    ['wrap', '.r93-wrap'],
    ['bottom', '.r93-bottom'],
    ['composer', 'main > div > div.flex-1.justify-center > div.mt-8 > div'],
    ['sk-in', '.r93-sk-in']
  ];
  for (var i = 0; i < cols.length; i++) {
    var b = R(cols[i][1]);
    if (!b) { L.push('  ' + pad(cols[i][0], 9) + ' (不存在)'); continue; }
    var li = pane ? (b.x - pane.x) : null;
    var ri = pane ? (pane.r - b.r) : null;
    L.push('  ' + pad(cols[i][0], 9) + ' ' + JSON.stringify(b) +
      '   距 pane 左 ' + li + ' / 右 ' + ri);
  }
  var bub = R('.r93-bub');
  L.push('  bub       ' + JSON.stringify(bub) + '   距 pane 左 ' + (bub && pane ? bub.x - pane.x : '') +
    ' / 右 ' + (bub && pane ? pane.r - bub.r : ''));
  return L.join('\n');
})()
