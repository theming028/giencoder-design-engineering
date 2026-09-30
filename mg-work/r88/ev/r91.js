(function () {
  function snap(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {
      x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(2), h: +r.height.toFixed(2),
      bg: cs.backgroundColor, radius: cs.borderRadius, col: cs.color,
      cls: (el.className || '').toString().slice(0, 90)
    };
  }
  var out = {};
  out.back = snap(document.querySelector('.r85-back'));
  out.navi = [].slice.call(document.querySelectorAll('.r85-navi')).map(function (b) {
    var s = snap(b);
    s.tab = b.getAttribute('data-set-tab');
    s.cur = b.getAttribute('aria-current');
    s.iconCol = getComputedStyle(b.querySelector('svg')).color;
    s.textCol = getComputedStyle(b.querySelector('span')).color;
    return s;
  });

  // 行尾图标按钮（需在「已归档任务」页签下才存在）
  var p = document.querySelector('.r88-arch');
  if (p) {
    var acts = p.querySelectorAll('.r88-arch-row')[0].querySelectorAll('.r88-arch-act');
    out.act = [].slice.call(acts).map(function (b) {
      var s = snap(b);
      s.act = b.getAttribute('data-act');
      s.iconCol = b.querySelector('svg') ? getComputedStyle(b.querySelector('svg')).color : null;
      s.btnCol = getComputedStyle(b).color;
      s.iconDisplay = b.querySelector('svg') ? getComputedStyle(b.querySelector('svg')).display : null;
      return s;
    });
    // 该行被 hover 时（展开态）的颜色
    var r3 = p.querySelectorAll('.r88-arch-row')[2];
    if (r3) {
      var a3 = r3.querySelectorAll('.r88-arch-act');
      out.actRow3Hover = [].slice.call(a3).map(function (b) {
        return { act: b.getAttribute('data-act'), w: +b.getBoundingClientRect().width.toFixed(2),
                 col: getComputedStyle(b).color, iconDisplay: getComputedStyle(b.querySelector('svg')).display };
      });
    }
  }
  return JSON.stringify(out);
})()
