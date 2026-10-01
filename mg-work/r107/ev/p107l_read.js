/* 第十一拍 ①②③：读时间线结果 + 量 selbar / url-pill 现状。 */
(function () {
  var out = {};
  var T = window.__L11T;
  if (T) {
    var o = T.t0 != null ? 0 : 0;
    out.timeline = {
      startOfProbe: Math.round(T.t0),
      tSkOut: T.tSkOut == null ? null : Math.round(T.tSkOut),
      tSkGone: T.tSkGone == null ? null : Math.round(T.tSkGone),
      tNumVisible: T.tNum == null ? null : Math.round(T.tNum),
      late: T.late,
      ni: T.ni,
      /* 关键差值：骨架屏消失 → 数字可见 之间的空窗 */
      gapSkToNum: (T.tSkGone != null && T.tNum != null) ? Math.round(T.tNum - T.tSkGone) : null,
      totalLoadToNum: T.tNum == null ? null : Math.round(T.tNum)
    };
  }
  /* 数字的动画参数（CSS 侧真值） */
  var list = document.querySelectorAll('.r93-num-i');
  for (var i = 0; i < list.length; i++) {
    var host = list[i].closest ? list[i].closest('.r93-t14') : null;
    if (host && host.textContent.indexOf('调用') === 0) {
      var c = getComputedStyle(list[i]);
      out.numAnim = { text: list[i].textContent, ni: list[i].style.getPropertyValue('--r93-ni'),
                      delay: c.animationDelay, dur: c.animationDuration, name: c.animationName, fill: c.animationFillMode };
      var pc = getComputedStyle(host);
      out.numHost = { cls: host.className, color: pc.color, fs: pc.fontSize };
      break;
    }
  }
  /* 数一下全页被包了多少枚 */
  out.numCount = document.querySelectorAll('.r93-num-i').length;
  var maxNi = 0;
  [].forEach.call(document.querySelectorAll('.r93-num-i'), function (e) {
    var v = parseInt(e.style.getPropertyValue('--r93-ni') || '0', 10);
    if (v > maxNi) maxNi = v;
  });
  out.maxNi = maxNi;

  /* ---- ① .td-selbar：造真实选区把浮条叫出来 ---- */
  var scroll = document.querySelector('.r93-scroll');
  var node = null;
  var walker = document.createTreeWalker(scroll, NodeFilter.SHOW_TEXT, null, false);
  while (walker.nextNode()) {
    var tn = walker.currentNode;
    if (tn.nodeValue && tn.nodeValue.trim().length >= 14 && tn.parentElement && !tn.parentElement.closest('.r93-num')) { node = tn; break; }
  }
  if (node) {
    var r = document.createRange();
    r.setStart(node, 0); r.setEnd(node, Math.min(14, node.nodeValue.length));
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    var rect = r.getBoundingClientRect();
    (node.parentElement).dispatchEvent(new MouseEvent('mouseup', { bubbles: true,
      clientX: Math.round(rect.left + 12), clientY: Math.round(rect.top + 6) }));
  }
  var bar = document.querySelector('.td-selbar');
  out.selbar = { exists: !!bar, hidden: bar ? bar.hasAttribute('hidden') : null };
  if (bar && !bar.hasAttribute('hidden')) {
    var bc = getComputedStyle(bar);
    out.selbar.host = { bg: bc.backgroundColor, border: bc.borderTopColor, radius: bc.borderTopLeftRadius };
    out.selbar.btns = [].map.call(bar.querySelectorAll('button'), function (b) {
      var c = getComputedStyle(b);
      var svg = b.querySelector('svg');
      var sp = b.querySelector('span');
      return {
        txt: (sp ? sp.textContent : b.textContent).trim(),
        btnColor: c.color,
        spanColor: sp ? getComputedStyle(sp).color : null,
        svgStroke: svg ? getComputedStyle(svg).stroke : null,
        svgColor: svg ? getComputedStyle(svg).color : null,
        cls: b.className
      };
    });
    out.selbarToken = { text1: getComputedStyle(document.documentElement).getPropertyValue('--color-text-1').trim() };
  }

  /* ---- ② .td-url-pill：需要先打开右栏的 browser 模块 ---- */
  var pill = document.querySelector('.td-url-pill');
  out.pill = { exists: !!pill, hidden: pill ? !!pill.closest('[hidden]') : null };
  if (pill) {
    var p0 = getComputedStyle(pill), i0 = getComputedStyle(pill.querySelector('input'));
    out.pill.before = { bg: p0.backgroundColor, shadow: p0.boxShadow, border: p0.borderTopWidth + ' ' + p0.borderTopColor,
                        color: p0.color, radius: p0.borderTopLeftRadius, inputColor: i0.color, outline: i0.outlineStyle };
    var inp = pill.querySelector('input');
    inp.focus();
    var p1 = getComputedStyle(pill), i1 = getComputedStyle(inp);
    out.pill.afterFocus = { bg: p1.backgroundColor, shadow: p1.boxShadow, border: p1.borderTopWidth + ' ' + p1.borderTopColor,
                            color: p1.color, inputColor: i1.color, outline: i1.outlineStyle,
                            matched: pill.matches(':focus-within') };
    inp.blur();
    out.pill.hasFocusWithinRule = 'n/a';
  }
  return JSON.stringify(out);
})();
