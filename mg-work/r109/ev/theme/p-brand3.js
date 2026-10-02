// r109 第十一拍 · 实测：品牌 LOGO 的 <img> 在浅/暗两档的**视觉呈现**
// 关键词：<img src=data:image/svg+xml> 内部 fill 是**图片像素**，外部 CSS 无法用 [fill=] 选中！
window.__brand3 = function () {
  var out = { imgs: [], probes: [] };
  var ims = document.querySelectorAll('img');
  for (var i = 0; i < ims.length; i++) {
    var r = ims[i].getBoundingClientRect();
    if (r.width < 100) continue;
    var st = getComputedStyle(ims[i]);
    // 尝试裁一条水平线采样：用 canvas 读该 img 的像素（同源 data-URI 可行）
    var rec = {
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      filter: st.filter, opacity: st.opacity,
      mixBlend: st.mixBlendMode,
      parentFilter: ims[i].parentElement ? getComputedStyle(ims[i].parentElement).filter : '',
      // 该 img 是否命中某条 [fill=] 规则？—— 不可能，但反向验证：
      matchesFill: ims[i].matches ? ims[i].matches('[fill="#1E1E1E"]') : null
    };
    // canvas 采样（取中间高度那一行）
    try {
      var cv = document.createElement('canvas');
      cv.width = rec.w; cv.height = rec.h;
      var cx = cv.getContext('2d');
      cx.drawImage(ims[i], 0, 0, rec.w, rec.h);
      var row = cx.getImageData(0, Math.floor(rec.h / 2), rec.w, 1).data;
      var cc = {};
      for (var k = 0; k < row.length; k += 4) {
        if (row[k + 3] < 32) continue;
        var key = row[k] + ',' + row[k + 1] + ',' + row[k + 2];
        cc[key] = (cc[key] || 0) + 1;
      }
      rec.rowColors = Object.keys(cc).map(function (kk) { return kk + '×' + cc[kk]; }).slice(0, 14);
    } catch (e) { rec.canvasErr = String(e).slice(0, 80); }
    out.imgs.push(rec);
  }
  // 现存的 [fill="#1E1E1E"] 规则到底命中了谁？
  out.hit1E = document.querySelectorAll('[fill="#1E1E1E"]').length;
  out.hit1F = document.querySelectorAll('[fill="#1F1F1F"]').length;
  out.hit6B = document.querySelectorAll('[fill="#6B6B6B"]').length;
  out.theme = document.documentElement.getAttribute('giencoder-theme') || '(none)';
  return out;
};
'ok'
