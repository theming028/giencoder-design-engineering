(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }

  // 布局锚点
  var root = document.querySelector('.av-browse-on') || document.documentElement;
  out.onFlag = !!document.querySelector('.av-browse-on');
  var pane = document.querySelector('.r93-pane');
  var scroll = document.querySelector('.r93-scroll');
  var wrap = document.querySelector('.r93-wrap');
  var card = null;
  var cands = document.querySelectorAll('main div');
  for (var i = 0; i < cands.length; i++) {
    var cl = cands[i].className || '';
    if (typeof cl === 'string' && cl.indexOf('rounded-[16px]') >= 0 && cl.indexOf('bg-white') >= 0) { card = cands[i]; break; }
  }
  out.pane = pane ? r(pane) : null;
  out.scroll = scroll ? [scroll.clientWidth, scroll.scrollWidth] : null;
  out.wrap = wrap ? r(wrap) : null;
  out.card = card ? r(card) : null;

  // .r93-alert 逐条
  out.alerts = [];
  document.querySelectorAll('.r93-alert').forEach(function (e) {
    var cs = getComputedStyle(e);
    var kids = [];
    Array.prototype.forEach.call(e.children, function (k) {
      kids.push({ cls: (k.className || '').slice(0, 26), r: r(k), sh: k.scrollWidth, cw: k.clientWidth });
    });
    out.alerts.push({
      r: r(e), box: [e.clientWidth, e.scrollWidth, e.clientHeight, e.scrollHeight],
      h: cs.height, minH: cs.minHeight, ofx: cs.overflowX, ofy: cs.overflowY, ws: cs.whiteSpace,
      kids: kids
    });
  });

  // 技能浮窗（aria-label=技能选择）——开态才量得到
  var sk = document.querySelector('[aria-label="技能选择"]');
  if (sk) {
    var c = getComputedStyle(sk);
    out.skill = {
      r: r(sk), inline: (sk.getAttribute('style') || '').slice(0, 260),
      w: c.width, minW: c.minWidth, maxW: c.maxWidth, pos: c.position,
      offsetParent: sk.offsetParent ? (sk.offsetParent.className || sk.offsetParent.tagName).toString().slice(0, 60) : null,
      offsetPW: sk.offsetParent ? Math.round(sk.offsetParent.getBoundingClientRect().width) : null,
      top: c.top, bottom: c.bottom, left: c.left, transform: c.transform,
      box: [sk.clientWidth, sk.scrollWidth, sk.clientHeight, sk.scrollHeight]
    };
  } else out.skill = 'NOT_FOUND';
  return JSON.stringify(out);
})()
