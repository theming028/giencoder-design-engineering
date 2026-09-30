(function () {
  var p = document.querySelector('.r88-arch');
  if (!p) return JSON.stringify({ err: 'no arch' });
  function c(el) { return el ? getComputedStyle(el).color : null; }
  var out = {};
  var row = p.querySelector('.r88-arch-row');
  var acts = row.querySelectorAll('.r88-arch-act');
  out.def = [].slice.call(acts).map(function (b) {
    return { act: b.getAttribute('data-act'), btnCol: getComputedStyle(b).color,
             iconCol: c(b.querySelector('svg')), bc: getComputedStyle(b).borderColor,
             bg: getComputedStyle(b).backgroundColor, r: getComputedStyle(b).borderRadius,
             w: +b.getBoundingClientRect().width.toFixed(2) };
  });
  var r3 = p.querySelectorAll('.r88-arch-row')[2];
  var a3 = r3.querySelectorAll('.r88-arch-act');
  out.row3 = [].slice.call(a3).map(function (b) {
    return { act: b.getAttribute('data-act'), w: +b.getBoundingClientRect().width.toFixed(2),
             col: getComputedStyle(b).color, iconDisplay: getComputedStyle(b.querySelector('svg')).display,
             spanDisplay: getComputedStyle(b.querySelector('span')).display };
  });
  out.iconPath = acts[0].querySelector('svg').innerHTML.slice(0, 160);
  return JSON.stringify(out);
})()
