(() => {
  const want = { x: 352, y: 416 };
  let trig = null, best = 1e9;
  document.querySelectorAll('[role="combobox"], .giencoder-select-view').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return;
    const d = Math.abs(r.x - want.x) + Math.abs(r.y - want.y);
    if (d < best) { best = d; trig = el; }
  });
  if (!trig) return 'NO-TRIGGER';
  const root = trig.closest('.giencoder-select') || trig.parentElement;
  const pop = root.querySelector('.giencoder-select-popup');
  if (!pop) return 'NO-POPUP';
  const rd = el => {
    const cs = getComputedStyle(el);
    const a = el.getAnimations ? el.getAnimations().map(x => (x.animationName || 'T:' + x.transitionProperty) + '@' + Math.round(x.effect ? (x.effect.getTiming().duration) : 0)).join('|') : '';
    return { op: cs.opacity, tr: cs.translate, sx: cs.scale, disp: cs.display, vis: cs.visibility, an: a };
  };
  const log = [];
  const t0 = performance.now();
  const sample = tag => log.push(Object.assign({ tag: tag, t: Math.round(performance.now() - t0) }, rd(pop)));
  sample('before');
  trig.click();
  [0, 16, 32, 48, 64, 90, 120, 160, 220].forEach(d => setTimeout(() => sample('open'), d));
  setTimeout(() => {
    sample('open-settled');
    trig.click();
    [0, 16, 32, 48, 64, 90, 120, 160, 220].forEach(d => setTimeout(() => sample('close'), d));
    setTimeout(() => {
      sample('close-settled');
      window.__SEL = log;
    }, 260);
  }, 320);
  return 'started:' + (root.className || '') + ' popupCls=' + pop.className;
})()
