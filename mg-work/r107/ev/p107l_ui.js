/* 第十一拍 ①②：量「划词浮条」与「浏览器地址栏」的现状/改后值。
   前提：右栏已打开且「浏览器」模块已是最前（否则 pill 在 hidden 容器里 focus 无效）。 */
(function () {
  var out = {};

  /* ---- ① .td-selbar ---- */
  var scroll = document.querySelector('.r93-scroll');
  var node = null;
  if (scroll) {
    var walker = document.createTreeWalker(scroll, NodeFilter.SHOW_TEXT, null, false);
    while (walker.nextNode()) {
      var tn = walker.currentNode;
      if (tn.nodeValue && tn.nodeValue.trim().length >= 14 && tn.parentElement &&
          !tn.parentElement.closest('.r93-num')) { node = tn; break; }
    }
  }
  if (node) {
    var r = document.createRange();
    r.setStart(node, 0); r.setEnd(node, Math.min(14, node.nodeValue.length));
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    var rect = r.getBoundingClientRect();
    node.parentElement.dispatchEvent(new MouseEvent('mouseup', { bubbles: true,
      clientX: Math.round(rect.left + 12), clientY: Math.round(rect.top + 6) }));
  }
  var bar = document.querySelector('.td-selbar');
  out.selbar = { exists: !!bar, hidden: bar ? bar.hasAttribute('hidden') : null };
  if (bar && !bar.hasAttribute('hidden')) {
    var bc = getComputedStyle(bar);
    out.selbar.host = { bg: bc.backgroundColor, radius: bc.borderTopLeftRadius };
    out.selbar.btns = [].map.call(bar.querySelectorAll('button'), function (b) {
      var c = getComputedStyle(b);
      var svg = b.querySelector('svg');
      var sp = b.querySelector('span');
      return { txt: (sp ? sp.textContent : b.textContent).trim(), color: c.color,
               svgStroke: svg ? getComputedStyle(svg).stroke : null,
               svgColor: svg ? getComputedStyle(svg).color : null };
    });
  }
  out.tokenText1 = getComputedStyle(document.documentElement).getPropertyValue('--color-text-1').trim();
  out.tokenPrimary6 = getComputedStyle(document.documentElement).getPropertyValue('--color-primary-6').trim();
  out.tokenPrimaryL2 = getComputedStyle(document.documentElement).getPropertyValue('--color-primary-light-2').trim();

  /* ---- ② .td-url-pill ---- */
  var pill = document.querySelector('.td-url-pill');
  out.pill = { exists: !!pill };
  if (pill) {
    var inHidden = !!pill.closest('[hidden]');
    out.pill.inHidden = inHidden;
    var p0 = getComputedStyle(pill);
    out.pill.before = { bg: p0.backgroundColor, shadow: p0.boxShadow, color: p0.color,
                        transition: p0.transitionProperty + ' ' + p0.transitionDuration };
    var inp = pill.querySelector('input');
    inp.focus();
    var p1 = getComputedStyle(pill);
    out.pill.afterFocus = { bg: p1.backgroundColor, shadow: p1.boxShadow,
                            matchesFocusWithin: pill.matches(':focus-within'),
                            activeIsFocused: document.activeElement === inp };
    var lock = pill.querySelector('svg');
    if (lock) out.pill.lockColor = getComputedStyle(lock).color;
    inp.blur();
    var p2 = getComputedStyle(pill);
    out.pill.afterBlur = { bg: p2.backgroundColor, shadow: p2.boxShadow,
                           matchesFocusWithin: pill.matches(':focus-within') };
  }
  return JSON.stringify(out);
})();
