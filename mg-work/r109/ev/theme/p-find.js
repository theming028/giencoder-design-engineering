// r109 第十一拍 · DOM 探找：① 波点背景（radial-gradient / url 图）② 顶栏 LOGO 的黑灰着色
// 用法：agent-browser eval "$(cat p-find.js)"  → 定义 window.__find / __logo / __hdr
window.__find = function () {
  var out = [];
  var all = document.querySelectorAll('*');
  for (var i = 0; i < all.length; i++) {
    var e = all[i], st = getComputedStyle(e);
    var bi = st.backgroundImage || '';
    if (!bi || bi === 'none') continue;
    var isDot = /radial-gradient/.test(bi);
    var isImg = /url\(/.test(bi);
    if (!isDot && !isImg) continue;
    var r = e.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    out.push({
      tag: e.tagName,
      cls: String(e.className || '').slice(0, 60),
      id: e.id || '',
      kind: isDot ? 'dot' : 'img',
      bi: bi.slice(0, 150),
      bsize: st.backgroundSize || '',
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height)
    });
  }
  return out;
};

// 顶栏 LOGO：找视口顶部区域内（y < 70）的 svg / img，并读出实际着色
window.__logo = function () {
  var out = [];
  var cands = document.querySelectorAll('svg, img, [class*="logo" i], [class*="brand" i]');
  for (var i = 0; i < cands.length; i++) {
    var e = cands[i], r = e.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) continue;
    if (r.y > 80) continue;              // 只看顶栏
    var st = getComputedStyle(e);
    var rec = {
      tag: e.tagName,
      cls: String(e.className || '').slice(0, 50),
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      color: st.color, fill: st.fill, bg: st.backgroundColor,
      bi: (st.backgroundImage || '').slice(0, 80)
    };
    // svg 内部 path 的着色（前 6 个）
    var ps = e.querySelectorAll ? e.querySelectorAll('path,rect,circle,polygon') : [];
    rec.parts = [];
    for (var j = 0; j < ps.length && j < 6; j++) {
      var pst = getComputedStyle(ps[j]);
      rec.parts.push({
        t: ps[j].tagName,
        fill: pst.fill,
        stroke: pst.stroke,
        fa: (ps[j].getAttribute('fill') || '').slice(0, 40)
      });
    }
    out.push(rec);
  }
  return out;
};

// 顶栏（header）本身
window.__hdr = function () {
  var hs = document.querySelectorAll('header');
  var out = [];
  for (var i = 0; i < hs.length; i++) {
    var e = hs[i], st = getComputedStyle(e), r = e.getBoundingClientRect();
    out.push({
      cls: String(e.className || '').slice(0, 60),
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      bg: st.backgroundColor,
      bi: (st.backgroundImage || '').slice(0, 170),
      bsize: st.backgroundSize || ''
    });
  }
  return out;
};
'ok'
