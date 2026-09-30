(function () {
  function r(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function rr(s) { return r(document.querySelector(s)); }
  var o = { vw: window.innerWidth, vh: window.innerHeight };

  /* ① .r93-card 内字号分布 */
  var dist = {};
  document.querySelectorAll('.r93-card').forEach(function (cd) {
    Array.prototype.forEach.call(cd.querySelectorAll('*'), function (e) {
      var has = false;
      Array.prototype.forEach.call(e.childNodes, function (n) { if (n.nodeType === 3 && n.textContent.trim()) has = true; });
      if (!has) return;
      var fs = getComputedStyle(e).fontSize;
      dist[fs] = (dist[fs] || 0) + 1;
    });
  });
  o.cardFontSizeDist = dist;
  var c1 = document.querySelector('.r93-card');
  o.cardSample = {
    t12c: getComputedStyle(c1.querySelector('.r93-t12c') || c1).fontSize,
    pre: getComputedStyle(document.querySelector('.r93-card .r93-pre') || c1).fontSize,
    t12: getComputedStyle(document.querySelector('.r93-card .r93-t12') || c1).fontSize
  };
  /* 卡高对照（确认未溢出） */
  o.cardHeights = Array.prototype.map.call(document.querySelectorAll('.r93-card'), function (e) {
    return [Math.round(e.getBoundingClientRect().height), e.scrollHeight - e.clientHeight];
  });

  /* ② 滚动到底部 */
  var tb = document.querySelector('.r93-tobottom');
  o.tobottom = {
    rect: r(tb), radius: getComputedStyle(tb).borderTopLeftRadius,
    color: getComputedStyle(tb).color, self: getComputedStyle(tb).color
  };
  var k = [];
  Array.prototype.forEach.call(tb.querySelectorAll('span'), function (s) {
    k.push({ cls: s.className, color: getComputedStyle(s).color, fs: getComputedStyle(s).fontSize, txt: (s.textContent || '').trim() });
  });
  o.tobottomSpans = k;
  o.tobottomSvg = tb.querySelector('svg') ? getComputedStyle(tb.querySelector('svg')).color : null;

  /* ③ 横向基准 */
  o.w = {
    scroll: [document.querySelector('.r93-scroll').clientWidth, document.querySelector('.r93-scroll').offsetWidth],
    pane: rr('.r93-pane'), wrap: rr('.r93-wrap'), bottom: rr('.r93-bottom'), sb: rr('.r93-sb'),
    comet: rr('.r93-agents'), composer: rr('main > div > div.flex-1.justify-center > div.mt-8 > div'),
    mt8: rr('main > div > div.flex-1.justify-center > div.mt-8'),
    card: rr('.r93-card'), alert: rr('.r93-alert'), bub: rr('.r93-bub')
  };
  var ag = document.querySelectorAll('.r93-agent');
  o.agents = Array.prototype.map.call(ag, function (e) { return r(e); });
  o.agentRowSpan = ag.length ? [Math.round(ag[0].getBoundingClientRect().left), Math.round(ag[ag.length - 1].getBoundingClientRect().right)] : null;

  /* ④ 底部统计行 */
  var m = document.querySelector('main > div > div.flex-1.justify-center > div.mt-8');
  var cs = getComputedStyle(m, '::after');
  o.meta = {
    content: (cs.content || '').slice(0, 130), fontSize: cs.fontSize, lineHeight: cs.lineHeight,
    color: cs.color, whiteSpace: cs.whiteSpace, mt8Height: Math.round(m.getBoundingClientRect().height)
  };
  o.doc = [document.documentElement.scrollWidth, document.documentElement.clientWidth, document.documentElement.scrollHeight, window.innerHeight];
  return JSON.stringify(o);
})();
