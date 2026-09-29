(() => {
  window.__bp = { t0: performance.now(), s: [] };
  const g = s => document.querySelector(s);
  const tick = () => {
    const r = g('.td-root'), ri = g('.td-right'), sl = g('.td-browse-slot'), pn = g('.td-browse'), lf = g('.td-left');
    window.__bp.s.push({
      t: Math.round(performance.now() - window.__bp.t0),
      b: r && r.classList.contains('is-browse') ? 1 : 0,
      left: lf ? Math.round(lf.getBoundingClientRect().width) : -1,
      right: ri ? Math.round(ri.getBoundingClientRect().width) : -1,
      slot: sl ? Math.round(sl.getBoundingClientRect().width) : -1,
      pane: pn ? Math.round(pn.getBoundingClientRect().width) : -1,
      pc: pn && pn.classList.contains('is-closing') ? 'CLS' : '-'
    });
    if (performance.now() - window.__bp.t0 < 900) requestAnimationFrame(tick);
  };
  const b = [...document.querySelectorAll('.td-root button')].find(x => (x.getAttribute('aria-label') || '').indexOf(window.__LBL) === 0);
  if (!b) return 'NO BTN for ' + window.__LBL + ' :: ' + [...document.querySelectorAll('.td-root button')].map(x => x.getAttribute('aria-label')).join('|');
  b.click();
  requestAnimationFrame(tick);
  return 'started:' + window.__LBL;
})()
