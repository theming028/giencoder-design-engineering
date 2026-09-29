(() => {
  const CSS = `
  .giencoder-select-popup {
    display: block !important;
    transition: opacity 160ms cubic-bezier(0.34,0.69,0.1,1),
                translate 160ms cubic-bezier(0.34,0.69,0.1,1),
                scale 160ms cubic-bezier(0.34,0.69,0.1,1),
                visibility 0s 160ms;
  }
  .giencoder-select-popup.giencoder-popup-open {
    transition: opacity 160ms cubic-bezier(0.34,0.69,0.1,1),
                translate 160ms cubic-bezier(0.34,0.69,0.1,1),
                scale 160ms cubic-bezier(0.34,0.69,0.1,1),
                visibility 0s;
  }`;
  const st = document.createElement('style'); st.id = 'r75-try'; st.textContent = CSS;
  document.head.appendChild(st);
  const trig = document.querySelector('.giencoder-select-view');
  const root = trig.closest('.giencoder-select');
  const pop = root.querySelector('.giencoder-select-popup');
  const F = [];
  const rd = tag => { const c = getComputedStyle(pop);
    F.push([tag, Math.round(performance.now() - t0), c.opacity.slice(0, 7), c.translate, c.scale, c.display, c.visibility.slice(0, 4),
            pop.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join('+')]); };
  const t0 = performance.now();
  rd('W'); trig.click();
  let n = 0;
  const loop = () => { rd('OPEN'); if (++n < 22) requestAnimationFrame(loop); else ph2(); };
  const ph2 = () => {
    trig.click(); const t1 = performance.now(); let m = 0;
    const l2 = () => { const c = getComputedStyle(pop);
      F.push(['CLOSE', Math.round(performance.now() - t1), c.opacity.slice(0, 7), c.translate, c.scale, c.display, c.visibility.slice(0, 4),
              pop.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join('+')]);
      if (++m < 22) requestAnimationFrame(l2); else window.__TRY = F; };
    requestAnimationFrame(l2);
  };
  requestAnimationFrame(loop);
  return 'injected';
})()
