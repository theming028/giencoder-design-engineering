(function () {
  function R(el) { if (!el) return null; var r = el.getBoundingClientRect(); return [Math.round(r.x * 10) / 10, Math.round(r.y * 10) / 10, Math.round(r.width * 10) / 10, Math.round(r.height * 10) / 10]; }
  var h = document.querySelector('.r93-conv-host');
  if (!h) return JSON.stringify({ err: 'no host' });
  var q = function (s) { return h.querySelector(s); };
  var out = {
    host: R(h),
    bar: R(q('.r93-bar')),
    seg: R(q('.r93-seg')),
    cap: R(q('.r93-seg-cap')),
    more: R(q('.r93-morebtn')),
    scroll: R(q('.r93-scroll')),
    wrap: R(q('.r93-wrap')),
    bub: R(q('.r93-bub')),
    bubi: R(q('.r93-bubi')),
    attrow1: R(q('.r93-attrow')),
    att1: R(h.querySelectorAll('.r93-att')[0]),
    umeta: R(q('.r93-umeta')),
    asst: R(q('.r93-asst')),
    fold1: R(h.querySelectorAll('.r93-fold')[0]),
    fh1: R(h.querySelectorAll('.r93-fold')[0].querySelector('.r93-fh')),
    card1: R(q('.r93-card')),
    bottom: R(q('.r93-bottom')),
    sb: R(q('.r93-sb')),
    cp: R(q('.r93-cp')),
    input: R(q('.r93-input')),
    agents: R(q('.r93-agents')),
    agent1: R(h.querySelectorAll('.r93-agent')[0]),
    ta: R(q('.r93-ta')),
    arts: R(q('.r93-arts')),
    artcard: R(q('.r93-artcard')),
    diff: R(q('.r93-diff')),
    dro: R(q('.r93-drow')),
    note: R(q('.r93-note')),
    alert: R(q('.r93-alert')),
    scrollH: q('.r93-scroll').scrollHeight,
    clientH: q('.r93-scroll').clientHeight,
    foldN: h.querySelectorAll('.r93-fold').length
  };
  return JSON.stringify(out);
})()
