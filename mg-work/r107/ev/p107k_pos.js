/* 第十拍探针：四枚下拉的「触发器 vs 菜单」几何对照
   判据：
     dy      = 菜单.top  - 触发器.bottom   （期望 ≈ 一个 gap，且 > 0 = 在下方）
     水平包含 = 触发器.left/right 与菜单.left/right 的关系（期望菜单水平覆盖触发器）
   输出 JSON 数组，每项 = 一枚菜单的一帧。
*/
(function () {
  var panes = ['td-mod-menu', 'td-rv-scope-menu', 'td-rv-opts', 'td-commit-menu'];
  var trigs = ['[data-td-add]', '[data-td-rv-scope]', '[data-td-rv-opts]', '[data-td-commit]'];
  function r(el) {
    if (!el) return null;
    var b = el.getBoundingClientRect();
    return { t: +b.top.toFixed(1), l: +b.left.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1),
             r: +b.right.toFixed(1), b2: +b.bottom.toFixed(1) };
  }
  var out = [];
  for (var i = 0; i < panes.length; i++) {
    var m = document.querySelector('.' + panes[i]);
    var t = document.querySelector(trigs[i]);
    var mb = r(m), tb = r(t);
    var row = { menu: panes[i], trig: trigs[i], tRect: tb, mRect: mb };
    if (mb && tb) {
      row.dy = +(mb.t - tb.b2).toFixed(1);            /* >0 = 菜单在按钮下方 */
      row.dxLeft = +(mb.l - tb.l).toFixed(1);         /* 0 = 左缘对齐 */
      row.dxRight = +(tb.r - mb.r).toFixed(1);        /* 0 = 右缘对齐 */
      row.coversH = (mb.l <= tb.l + 0.5) && (mb.r >= tb.r - 0.5);
    }
    /* 面板容器（定位参照）与工具条，作为坐标系参照 */
    var pane = document.querySelector('.td-browse');
    var bar = document.querySelector('.td-mod-bar');
    row.paneRect = r(pane);
    row.modBarRect = r(bar);
    row.hidden = !!(m && m.hasAttribute('hidden'));
    /* 计算样式：看定位归属 */
    if (m) {
      var cs = getComputedStyle(m);
      row.cs = { pos: cs.position, top: cs.top, left: cs.left, right: cs.right, z: cs.zIndex };
    }
    /* 触发器的祖先链（判断它挂在哪个容器里） */
    var chain = [], e = t;
    while (e && chain.length < 6) { chain.push(e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ').filter(Boolean).slice(0, 2).join('.') : '')); e = e.parentElement; }
    row.trigChain = chain.join(' < ');
    out.push(row);
  }
  return JSON.stringify(out);
})()
