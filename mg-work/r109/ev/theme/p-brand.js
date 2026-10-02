// r109 第十一拍 · 定位 base 页中央的 GIENC⇄DER 品牌大标题
// 输出：元素矩形 + 内部每个 span/path 的文本与着色 + 用的原始属性
window.__brand = function () {
  var out = [];
  // 找含 "GIENC" 文本的元素（大小写不敏感，可能在 textContent 或 innerHTML）
  var all = document.querySelectorAll('body *');
  var hits = [];
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    if (e.children.length) continue;            // 只看叶子
    var t = (e.textContent || '').trim();
    if (/GIENC|DER|工作台/i.test(t) && t.length < 24) hits.push(e);
  }
  // 向上聚合到共同容器
  for (var j = 0; j < hits.length; j++) {
    var e = hits[j], cur = e, chain = [];
    while (cur && chain.length < 6) {
      chain.push(cur.tagName + (cur.className ? '.' + String(cur.className && cur.className.baseVal !== undefined ? cur.className.baseVal : cur.className).split(' ')[0] : ''));
      cur = cur.parentElement;
    }
    var r = e.getBoundingClientRect(), st = getComputedStyle(e);
    out.push({
      txt: (e.textContent || '').trim().slice(0, 20),
      tag: e.tagName,
      cls: String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className || '').slice(0, 50),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      color: st.color,
      fs: st.fontSize, fw: st.fontWeight,
      chain: chain.join(' < ')
    });
  }
  // 同时：找 x 500~820, y 180~240 内所有 svg path
  var svgs = document.querySelectorAll('svg');
  var paths = [];
  for (var k = 0; k < svgs.length; k++) {
    var sr = svgs[k].getBoundingClientRect();
    if (sr.x < 480 || sr.x > 830 || sr.y < 170 || sr.y > 245) continue;
    var ps = svgs[k].querySelectorAll('path,rect,circle,polygon');
    var rec = { svgx: Math.round(sr.x), svgy: Math.round(sr.y), svgw: Math.round(sr.width), svgh: Math.round(sr.height), parts: [] };
    for (var m = 0; m < ps.length && m < 10; m++) {
      rec.parts.push({
        fill: getComputedStyle(ps[m]).fill,
        raw: String(ps[m].getAttribute('fill') || '').slice(0, 40),
        cls: String(ps[m].getAttribute('class') || '').slice(0, 30)
      });
    }
    paths.push(rec);
  }
  return { texts: out, svgs: paths };
};
'ok'
