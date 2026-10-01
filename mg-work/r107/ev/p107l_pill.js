/* 第十一拍 ②：聚焦地址栏，等过渡走完（400ms）再存读数 —— 避免量到 transition 起点。
   前提：右栏已开、且「浏览器」模块在最前。 */
(function () {
  var pill = document.querySelector('.td-url-pill');
  if (!pill) return 'no pill';
  var inp = pill.querySelector('input');
  var lock = pill.querySelector('svg');
  var R = { inHidden: !!pill.closest('[hidden]') };
  function snap(tag) {
    var c = getComputedStyle(pill);
    R[tag] = { bg: c.backgroundColor, shadow: c.boxShadow, color: c.color,
               focusWithin: pill.matches(':focus-within'),
               lock: lock ? getComputedStyle(lock).color : null,
               boxH: Math.round(pill.getBoundingClientRect().height) };
  }
  snap('before');
  inp.focus();
  setTimeout(function () {
    snap('focused');
    inp.blur();
    setTimeout(function () {
      snap('afterBlur');
      window.__L11P = R;
    }, 400);
  }, 400);
  return 'armed';
})();
