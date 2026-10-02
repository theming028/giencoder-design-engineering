// r109 第十一拍 · 提取 base 页品牌 LOGO 的完整 data-URI + 其外层的 filter/背景
window.__brand2 = function () {
  var out = [];
  var ims = document.querySelectorAll('img');
  for (var i = 0; i < ims.length; i++) {
    var r = ims[i].getBoundingClientRect();
    if (r.width < 100) continue;
    var st = getComputedStyle(ims[i]);
    out.push({
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      cls: String(ims[i].className || '').slice(0, 60),
      alt: ims[i].alt || '',
      filter: st.filter,
      opacity: st.opacity,
      srcLen: (ims[i].src || '').length,
      srcHead: (ims[i].src || '').slice(0, 260),
      srcTail: (ims[i].src || '').slice(-320)
    });
    // 父链
    var chain = [], cur = ims[i].parentElement;
    while (cur && chain.length < 5) {
      var cst = getComputedStyle(cur);
      chain.push({
        tag: cur.tagName,
        cls: String(cur.className && cur.className.baseVal !== undefined ? cur.className.baseVal : cur.className || '').slice(0, 44),
        bg: cst.backgroundColor,
        filter: cst.filter,
        color: cst.color
      });
      cur = cur.parentElement;
    }
    out[out.length - 1].chain = chain;
    out[out.length - 1].srcFull = ims[i].src;
  }
  return out;
};
'ok'
