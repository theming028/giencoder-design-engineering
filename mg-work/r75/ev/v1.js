(() => {
  const list = [];
  document.querySelectorAll('.giencoder-select').forEach(r => {
    const v = r.querySelector('.giencoder-select-view');
    if (v && v.getBoundingClientRect().width > 0 && r.querySelector('.giencoder-select-popup')) list.push([r, v]);
  });
  const out = []; let i = 0;
  function step() {
    if (i >= list.length) { window.__V1 = out; return; }
    const v = list[i][1], pop = list[i][0].querySelector('.giencoder-select-popup');
    const rec = { txt: (v.textContent || '').trim().slice(0, 12), open: [], close: [] };
    const snap = (arr, t) => { const c = getComputedStyle(pop);
      arr.push(t + ':' + c.opacity.slice(0, 5) + '/' + c.translate + '/an=' + pop.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join('+')); };
    const t0 = performance.now(); v.click();
    let n = 0;
    const loop = () => { snap(rec.open, Math.round(performance.now() - t0)); if (++n < 11) requestAnimationFrame(loop); else doClose(); };
    const doClose = () => { v.click(); const t1 = performance.now(); let m = 0;
      const l2 = () => { snap(rec.close, Math.round(performance.now() - t1)); if (++m < 11) requestAnimationFrame(l2); else { out.push(rec); i++; setTimeout(step, 280); } };
      requestAnimationFrame(l2); };
    requestAnimationFrame(loop);
  }
  step();
  return 'selects=' + list.length;
})()
