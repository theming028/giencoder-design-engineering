/* r109 第八拍补测 · settings 页下拉（.giencoder-select 家族）专用探针
   为什么单开：__trig 的通用候选把 giencoder-select-view 排在 r81-ws-trigger / ws-trigger-hover 之后，
   那两类若先命中就会点到侧栏，永远点不开 select 浮层。
   本探针：① 枚举 select-view / popup 几何 ② 提供 scrollIntoView 后的可点坐标 ③ 枚举浮层内 option。 */
(function () {
  function R(e) { var r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; }

  /* 枚举下拉触发器与浮层现状 */
  window.__selprobe = function () {
    var out = [], v = document.querySelectorAll('.giencoder-select-view'), i, r;
    out.push('views=' + v.length);
    for (i = 0; i < v.length; i++) {
      r = R(v[i]);
      out.push('  v' + i + ' rect=' + r.join(',') +
        ' tab=' + v[i].getAttribute('tabindex') +
        ' role=' + v[i].getAttribute('role') +
        ' txt=' + (v[i].innerText || '').replace(/\s+/g, ' ').slice(0, 20));
    }
    var p = document.querySelectorAll('.giencoder-select-popup');
    out.push('popups=' + p.length);
    for (i = 0; i < p.length; i++) {
      var st = getComputedStyle(p[i]); r = R(p[i]);
      out.push('  p' + i + ' cls=' + (p[i].getAttribute('class') || '').slice(0, 70) +
        ' vis=' + st.visibility + ' op=' + st.opacity + ' rect=' + r.join(',') +
        ' opts=' + p[i].querySelectorAll('.giencoder-select-option').length);
    }
    return JSON.stringify(out);
  };

  /* 取第 idx 个触发器中心点；先 scrollIntoView 保证在视口内（视口外坐标点不到） */
  window.__selview = function (idx) {
    var v = document.querySelectorAll('.giencoder-select-view');
    if (!v.length) return JSON.stringify([]);
    var e = v[idx || 0];
    e.scrollIntoView({ block: 'center' });
    var r = e.getBoundingClientRect();
    return JSON.stringify([{
      x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
      w: Math.round(r.width), h: Math.round(r.height),
      bg: getComputedStyle(e).backgroundColor, bc: getComputedStyle(e).borderTopColor,
      t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 20)
    }]);
  };

  /* 通用：取任意选择器第 idx 件的中心点（先 scrollIntoView，保证在视口内可 hover） */
  window.__center = function (sel, idx) {
    var all = document.querySelectorAll(sel);
    if (!all.length) return JSON.stringify([]);
    var i = Math.min(idx || 0, all.length - 1), e = all[i];
    e.scrollIntoView({ block: 'center' });
    var r = e.getBoundingClientRect(), st = getComputedStyle(e);
    return JSON.stringify([{
      n: all.length,
      x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
      w: Math.round(r.width), h: Math.round(r.height),
      bg: st.backgroundColor, color: st.color,
      t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 22)
    }]);
  };

  /* ★ 读「谁真正在 :hover」—— 不用面积法：浮层与下方控件矩形重叠时，
     __bgAt 会按「面积最小」选中被浮层盖住的下层元素（已踩：读成 v2 的 view-text）。
     浏览器按 z-order 把 :hover 给最上层 ⇒ 直接问 :hover 是谁最可靠。 */
  window.__hovered = function (sub) {
    var all = document.querySelectorAll(sub || '.giencoder-select-option'), out = [];
    for (var i = 0; i < all.length; i++) {
      var e = all[i];
      if (!e.matches(':hover')) continue;
      var st = getComputedStyle(e), r = e.getBoundingClientRect();
      out.push({
        cls: (e.getAttribute('class') || '').slice(0, 60),
        bg: st.backgroundColor, color: st.color, bc: st.borderTopColor,
        x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
        w: Math.round(r.width), h: Math.round(r.height),
        t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 14)
      });
    }
    return JSON.stringify(out);
  };

  /* 枚举「已展开浮层」内的选项（含 scrollIntoView；返回真实可点坐标） */
  window.__selopts = function () {
    var ps = document.querySelectorAll('.giencoder-select-popup'), out = [];
    for (var i = 0; i < ps.length; i++) {
      var st = getComputedStyle(ps[i]);
      if (st.visibility === 'hidden' || st.opacity === '0' || st.display === 'none') continue;
      var os = ps[i].querySelectorAll('.giencoder-select-option');
      for (var j = 0; j < os.length; j++) {
        var e = os[j], r = e.getBoundingClientRect();
        if (r.width < 20 || r.height < 8) continue;
        out.push({
          x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
          w: Math.round(r.width), h: Math.round(r.height),
          bg: getComputedStyle(e).backgroundColor,
          c: (e.getAttribute('class') || '').slice(0, 60),
          t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 16)
        });
      }
    }
    return JSON.stringify(out);
  };
})();
