(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  var pane = document.querySelector('.r93-pane');
  var scroll = document.querySelector('.r93-scroll');
  var card = null, cands = document.querySelectorAll('main div');
  for (var i = 0; i < cands.length; i++) {
    var cl = cands[i].className || '';
    if (typeof cl === 'string' && cl.indexOf('rounded-[16px]') >= 0 && cl.indexOf('bg-white') >= 0) { card = cands[i]; break; }
  }
  var sr = scroll.getBoundingClientRect();
  out.vw = window.innerWidth;
  out.pane = pane ? r(pane) : null;
  out.scrollClient = [scroll.clientWidth, scroll.scrollWidth];
  out.scrollBox = [Math.round(sr.left), Math.round(sr.right)];
  out.card = card ? r(card) : null;
  // 技能浮窗
  var sk = document.querySelector('[aria-label="技能选择"]');
  out.skill = sk ? { r: r(sk), w: getComputedStyle(sk).width, open: sk.getAttribute('style') ? true : false } : null;
  // alert
  out.alerts = [];
  document.querySelectorAll('.r93-alert').forEach(function (e) {
    var es = r(e), ov = [];
    var p = e.parentElement;
    while (p && p !== document.body) { var pr = p.getBoundingClientRect(); ov.push((p.className || p.tagName).toString().slice(0, 22) + ':' + Math.round(pr.width)); p = p.parentElement; if (ov.length > 4) break; }
    out.alerts.push({
      r: es, sw: e.scrollWidth, cw: e.clientWidth, ch: e.clientHeight, sh: e.scrollHeight,
      h: getComputedStyle(e).height,
      overRight: Math.round(es.left + es.width - sr.right),
      overLeft: Math.round(sr.left - es.left),
      chain: ov
    });
  });
  return JSON.stringify(out);
})()
