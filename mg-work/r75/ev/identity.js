(() => {
  const trig = document.querySelector('.giencoder-select-view');
  const root = trig.closest('.giencoder-select');
  const pops = () => Array.from(root.querySelectorAll('.giencoder-select-popup'));
  const p0 = pops()[0];
  p0.dataset.r75mark = 'MK';
  window.__NODE = p0;
  const rd = el => {
    const c = getComputedStyle(el);
    return { mark: el.dataset.r75mark || '-', same: el === window.__NODE, cls: el.className.replace('giencoder-select-popup', 'P'),
             disp: c.display, vis: c.visibility, op: c.opacity, tr: c.translate, sx: c.scale,
             tp: c.transitionProperty.replace(/,\s*/g, ','), td: c.transitionDuration.replace(/,\s*/g, ','),
             tf: c.transitionTimingFunction.slice(0, 60).replace(/,\s*/g, ','), tb: c.transitionBehavior,
             an: el.getAnimations().map(a => (a.animationName || 'T:' + a.transitionProperty) + '/' + Math.round(a.effect.getTiming().duration)).join(' ') };
  };
  const out = { before: pops().map(rd), beforeCount: pops().length, rootCls: root.className };
  trig.click();
  [15, 40, 90, 150, 250].forEach(d => setTimeout(() => {
    const ps = pops();
    out['t' + d] = { n: ps.length, list: ps.map(rd) };
  }, d));
  setTimeout(() => { window.__ID = out; }, 340);
  return 'ok count=' + out.beforeCount;
})()
