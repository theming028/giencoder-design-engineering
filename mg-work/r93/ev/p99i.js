(function () {
  var a = [].slice.call(document.querySelectorAll('svg')).filter(function (x) {
    return x.innerHTML.indexOf('matrix(-1,0,0,1,26,0)') >= 0;
  });
  if (!a.length) return 'NO';
  var s = a[a.length - 1];
  s.scrollIntoView({ block: 'center' });
  var r = s.getBoundingClientRect();
  var p = s.querySelector('path');
  return 'rect ' + [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)].join(',') +
    ' n=' + a.length + ' vb=' + s.getAttribute('viewBox') + ' fill=' + getComputedStyle(p).fill;
})();
