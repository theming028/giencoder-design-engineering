(() => {
  const trig = document.querySelector('.giencoder-select-view');
  const root = trig.closest('.giencoder-select');
  const pop = root.querySelector('.giencoder-select-popup');
  const F = [];
  const t0 = performance.now();
  const rd = tag => { const c = getComputedStyle(pop);
    F.push([tag, Math.round(performance.now() - t0), c.opacity, c.translate, c.scale, c.display, c.visibility,
            pop.getAnimations().map(a => (a.animationName || 'T:' + a.transitionProperty)).join('+')]); };
  let n = 0;
  const loop = () => { rd('O'); if (++n < 26 && performance.now() - t0 < 420) requestAnimationFrame(loop); else phase2(); };
  const phase2 = () => {
    trig.click();
    const t1 = performance.now(); let m = 0;
    const loop2 = () => { const c = getComputedStyle(pop);
      F.push(['C', Math.round(performance.now() - t1), c.opacity, c.translate, c.scale, c.display, c.visibility,
              pop.getAnimations().map(a => (a.animationName || 'T:' + a.transitionProperty)).join('+')]);
      if (++m < 26 && performance.now() - t1 < 420) requestAnimationFrame(loop2); else window.__RAF = F; };
    requestAnimationFrame(loop2);
  };
  rd('W'); trig.click(); requestAnimationFrame(loop);
  return 'started';
})()
