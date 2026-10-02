// r109 第十一拍 · 顶栏左侧（x<340, y<56）**枚举全部元素**，按 x 排序，带 computed 着色
// 目的：定位 x≈89~102 / x=120 / x≈193~287 这几簇是谁
window.__el = function () {
  var out = [];
  var all = document.querySelectorAll('header *, header');
  for (var i = 0; i < all.length; i++) {
    var e = all[i], r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.x > 360 || r.y > 56) continue;
    var st = getComputedStyle(e);
    var rec = {
      tag: e.tagName,
      cls: String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className || '').slice(0, 46),
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      color: st.color,
      fill: st.fill,
      bg: st.backgroundColor,
      txt: (e.children.length === 0 ? (e.textContent || '') : '').slice(0, 14)
    };
    // svg 内 path 的 fill（含原始 attr，能看出用的是哪个变量）
    if (e.tagName.toLowerCase() === 'svg') {
      var ps = e.querySelectorAll('path,rect,circle,polygon,ellipse');
      rec.parts = [];
      for (var j = 0; j < ps.length && j < 8; j++) {
        var a = ps[j].getAttribute('fill');
        rec.parts.push({
          raw: a === null ? '(null)' : String(a).slice(0, 34),
          fill: getComputedStyle(ps[j]).fill
        });
      }
    }
    out.push(rec);
  }
  out.sort(function (a, b) { return a.x - b.x || a.w - b.w; });
  return out;
};
'ok'
