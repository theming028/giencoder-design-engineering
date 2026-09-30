(function () {
  function R(e) {
    if (!e) return null;
    var b = e.getBoundingClientRect();
    return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)];
  }
  var h = document.querySelector('.r93-conv-host');
  var out = {};
  var bar = h.querySelector('.r93-bar');
  var sc = h.querySelector('.r93-scroll');
  var cs = getComputedStyle(bar);
  out.host = R(h); out.bar = R(bar); out.scroll = R(sc);
  out.barPos = cs.position; out.barBg = cs.backgroundColor; out.barZ = cs.zIndex;
  out.barBd = cs.backdropFilter || cs.webkitBackdropFilter;
  out.scrollPad = getComputedStyle(sc).padding;
  var hd = document.querySelector('header[class*="h-12"]');
  var hs = getComputedStyle(hd);
  out.hdr = { size: hs.backgroundSize, pos: hs.backgroundPosition, img: hs.backgroundImage.slice(0, 48), box: R(hd) };
  var af = getComputedStyle(h.querySelector('.r93-tbsticky'), '::after');
  out.fade = { h: af.height, bottom: af.bottom, bg: af.backgroundImage.slice(0, 62) };
  var fb = h.querySelector('.r93-fold[data-open="1"] > .r93-fb');
  var fs = getComputedStyle(fb);
  out.foldAnim = fs.animationName + ' / ' + fs.animationDuration + ' / ' + fs.animationTimingFunction;
  var cv = h.querySelector('.r93-fold[data-open="1"] > .r93-fh .r93-cv');
  out.cvTrans = cv ? getComputedStyle(cv).transitionProperty + ' ' + getComputedStyle(cv).transitionDuration + ' ' + getComputedStyle(cv).transitionTimingFunction : null;
  out.foldOpen = h.querySelectorAll('.r93-fold[data-open="1"]').length;
  out.foldClosed = h.querySelectorAll('.r93-fold[data-open="0"]').length;
  var fc = h.querySelector('.r93-fold[data-open="0"] > .r93-fc');
  if (fc) {
    var arrow = fc.querySelector('.r93-fchev');
    var prev = arrow ? arrow.previousElementSibling : null;
    out.fc = {
      box: R(fc),
      kids: [].slice.call(fc.children).map(function (k) { return k.className + '|' + R(k)[2] + 'x' + R(k)[3]; }),
      gapToPrev: (arrow && prev) ? Math.round(arrow.getBoundingClientRect().left - prev.getBoundingClientRect().right) : null,
      arrowBox: R(arrow),
      arrowOp: arrow ? getComputedStyle(arrow).opacity : null,
      arrowTrans: arrow ? getComputedStyle(arrow).transitionProperty : null
    };
  }
  out.diffMenus = document.querySelectorAll('.r93-ctx').length;
  out.sk = h.querySelectorAll('.r93-sk').length;
  return JSON.stringify(out);
})()
