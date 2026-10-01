(function () {
  /* 枚举 .td-browse 里所有「文字叶子」（自己有直接文本、元素子节点只有 svg/path 图标）
     —— 这是「哪些类需要省略号」的权威清单。 */
  function isIcon(n) {
    if (n.nodeType !== 1) return false;
    var t = n.tagName.toLowerCase();
    return t === 'svg' || t === 'path' || t === 'use' || t === 'circle' || t === 'rect' || t === 'line' || t === 'polyline';
  }
  var groups = {};
  document.querySelectorAll('.td-browse *').forEach(function (e) {
    var txt = '', otherEl = 0;
    for (var i = 0; i < e.childNodes.length; i++) {
      var n = e.childNodes[i];
      if (n.nodeType === 3) txt += n.nodeValue;
      else if (isIcon(n)) { /* 忽略 */ }
      else otherEl++;
    }
    txt = txt.replace(/\s+/g, ' ').trim();
    if (!txt) return;
    var c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden') return;
    var cls = String(e.className || '').trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.');
    var k = e.tagName + (cls ? '.' + cls : '') + (otherEl ? ' [+' + otherEl + '子元素]' : '');
    if (!groups[k]) groups[k] = { n: 0, ws: c.whiteSpace, te: c.textOverflow, ox: c.overflowX, ovf: c.overflow, mw: c.minWidth, sample: '', maxlen: 0 };
    groups[k].n++;
    groups[k].maxlen = Math.max(groups[k].maxlen, txt.length);
    if (!groups[k].sample) groups[k].sample = txt.slice(0, 24);
  });
  return JSON.stringify({ n: Object.keys(groups).length, groups: groups }, null, 1);
})()
