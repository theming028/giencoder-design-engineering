// r109 第十一拍 · 全页扫描：找出「GIENC⇄DER」到底是啥（文本/图片/内联SVG）
window.__scan = function () {
  var out = { imgs: [], svgs: [], bgimgs: [], texts: [] };
  // 1) 所有 <img>
  var ims = document.querySelectorAll('img');
  for (var i = 0; i < ims.length; i++) {
    var r = ims[i].getBoundingClientRect();
    if (r.width < 20 || r.height < 8) continue;
    out.imgs.push({ src: (ims[i].src || '').slice(-60), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
  }
  // 2) 所有 svg（宽 > 40）
  var ss = document.querySelectorAll('svg');
  for (var j = 0; j < ss.length; j++) {
    var sr = ss[j].getBoundingClientRect();
    if (sr.width < 40 || sr.height < 8) continue;
    var ps = ss[j].querySelectorAll('path,rect,circle,polygon,text');
    var fills = [];
    for (var k = 0; k < ps.length && k < 6; k++) {
      fills.push(String(ps[k].getAttribute('fill') || getComputedStyle(ps[k]).fill).slice(0, 34));
    }
    out.svgs.push({ x: Math.round(sr.x), y: Math.round(sr.y), w: Math.round(sr.width), h: Math.round(sr.height), n: ps.length, fills: fills, vb: ss[j].getAttribute('viewBox') || '' });
  }
  // 3) 背景图元素（宽>40 且 y<400）
  var all = document.querySelectorAll('body *');
  for (var m = 0; m < all.length; m++) {
    var st = getComputedStyle(all[m]);
    if (st.backgroundImage && st.backgroundImage !== 'none' && /url\(/.test(st.backgroundImage)) {
      var rr = all[m].getBoundingClientRect();
      if (rr.width < 60 || rr.height < 30) continue;
      out.bgimgs.push({ cls: String(all[m].className || '').slice(0, 40), bi: st.backgroundImage.slice(0, 90), x: Math.round(rr.x), y: Math.round(rr.y), w: Math.round(rr.width), h: Math.round(rr.height) });
    }
  }
  // 4) 含 GIENC 文本（含隐藏/父级）
  var t2 = document.querySelectorAll('*');
  for (var q = 0; q < t2.length; q++) {
    var own = '';
    for (var c = 0; c < t2[q].childNodes.length; c++) if (t2[q].childNodes[c].nodeType === 3) own += t2[q].childNodes[c].nodeValue;
    if (/GIENC|工作台/i.test(own)) {
      var rq = t2[q].getBoundingClientRect(), sq = getComputedStyle(t2[q]);
      out.texts.push({ t: own.trim().slice(0, 26), tag: t2[q].tagName, cls: String(t2[q].className && t2[q].className.baseVal !== undefined ? t2[q].className.baseVal : t2[q].className || '').slice(0, 40), x: Math.round(rq.x), y: Math.round(rq.y), w: Math.round(rq.width), h: Math.round(rq.height), color: sq.color, fs: sq.fontSize, ff: sq.fontFamily.slice(0, 40) });
    }
  }
  return out;
};
'ok'
