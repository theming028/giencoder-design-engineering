(function () {
  var h = document.querySelector('.r93-conv-host');
  function R(e) {
    if (!e) return null;
    var b = e.getBoundingClientRect();
    return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)];
  }
  var bar = h.querySelector('.r93-bar');
  var pane = h.querySelector('.r93-pane');
  var sc = h.querySelector('.r93-scroll');
  var wrap = h.querySelector('.r93-wrap');
  var cs = getComputedStyle(bar);
  var out = {
    host: R(h), bar: R(bar), pane: R(pane), scroll: R(sc), wrap: R(wrap),
    barBg: cs.backgroundColor, barPos: cs.position, barZ: cs.zIndex,
    barOverflow: cs.overflow, barBackdrop: cs.backdropFilter || cs.webkitBackdropFilter,
    hostPos: getComputedStyle(h).position,
    scGutter: getComputedStyle(sc).scrollbarGutter,
    scPad: getComputedStyle(sc).padding,
    wrapPad: getComputedStyle(wrap).padding,
    scrollTop: sc.scrollTop, scrollH: sc.scrollHeight, clientH: sc.clientHeight
  };
  /* 折叠头：结构 + 现有子元素宽度 */
  var fc = h.querySelector('.r93-fold[data-open="0"] > .r93-fc');
  out.fc = fc ? {
    box: R(fc),
    fs: getComputedStyle(fc).fontSize,
    gap: getComputedStyle(fc).gap,
    kids: [].map.call(fc.children, function (k) { return k.className + '|' + R(k)[2] + 'x' + R(k)[3]; })
  } : null;
  /* .r93-fb 的开关方式 */
  var fbOpen = h.querySelector('.r93-fold[data-open="1"] > .r93-fb');
  var fbClosed = h.querySelector('.r93-fold[data-open="0"] > .r93-fb');
  out.fbOpen = fbOpen ? getComputedStyle(fbOpen).display + '/' + getComputedStyle(fbOpen).animationName : null;
  out.fbClosed = fbClosed ? getComputedStyle(fbClosed).display : null;
  /* .r93-diff */
  var d = h.querySelector('.r93-diff');
  out.diff = d ? {
    box: R(d),
    dheadActs: [].map.call(d.querySelectorAll('.r93-dacts > *'), function (b) { return b.className.split(' ').slice(-1)[0] + '|' + R(b)[2] + 'x' + R(b)[3]; }),
    rows: d.querySelectorAll('.r93-drow').length,
    more: d.querySelectorAll('.r93-dmore').length
  } : null;
  /* 骨架屏（若还在） */
  var sk = h.querySelector('.r93-sk');
  out.sk = sk ? { box: R(sk), card: R(sk.querySelector('.r93-sk-card')), cardBg: getComputedStyle(sk.querySelector('.r93-sk-card')).backgroundColor } : null;
  return JSON.stringify(out);
})()
