(() => {
  const P = window.__P || { x: 352, y: 416 };
  let trig = null, best = 1e9;
  document.querySelectorAll('[role="combobox"], .giencoder-select-view, [aria-expanded]').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return;
    const d = Math.abs(r.x - P.x) + Math.abs(r.y - P.y);
    if (d < best) { best = d; trig = el; }
  });
  if (!trig) return 'NO-TRIGGER';
  const root = trig.closest('.giencoder-select') || trig.parentElement;
  const pop = root.querySelector('.giencoder-select-popup');
  if (!pop) return 'NO-POPUP';
  const rd = () => {
    const cs = getComputedStyle(pop);
    const a = pop.getAnimations().map(x => x.animationName || 'T:' + x.transitionProperty).join('|');
    return { cls: pop.className, st: (pop.getAttribute('style') || '').slice(0, 140),
             op: cs.opacity, tr: cs.translate, sx: cs.scale, disp: cs.display, an: a };
  };
  const log = []; const t0 = performance.now();
  const S = tag => log.push(Object.assign({ tag, t: Math.round(performance.now() - t0) }, rd()));
  S('before'); trig.click();
  [0, 20, 60, 120, 200].forEach(d => setTimeout(() => S('open'), d));
  setTimeout(() => { S('settled'); trig.click();
    [0, 20, 60, 120, 200].forEach(d => setTimeout(() => S('close'), d));
    setTimeout(() => { S('closed'); window.__SEL = log; }, 260);
  }, 340);
  return 'OK ' + trig.tagName + '.' + String(trig.className).slice(0, 60);
})()
