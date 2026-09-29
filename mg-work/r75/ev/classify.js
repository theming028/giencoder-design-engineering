(() => {
  const res = { url: location.pathname.split('/').pop(), pops: [] };
  document.querySelectorAll('.giencoder-select-popup').forEach(p => {
    const cs = getComputedStyle(p);
    res.pops.push({ inline: p.getAttribute('style') || '', disp: cs.display, vis: cs.visibility,
                    op: cs.opacity, tr: cs.translate, sx: cs.scale,
                    trs: cs.transition.replace(/\s+/g, ' ').slice(0, 150) });
  });
  // 找出第一个 select 触发器并点开采样
  const trig = document.querySelector('.giencoder-select-view');
  if (!trig) { res.note = 'no-trigger'; return JSON.stringify(res); }
  const root = trig.closest('.giencoder-select');
  const pop = root ? root.querySelector('.giencoder-select-popup') : null;
  if (!pop) { res.note = 'no-popup'; return JSON.stringify(res); }
  const seq = []; const t0 = performance.now();
  const rd = () => { const c = getComputedStyle(pop); return Math.round(performance.now() - t0) + ':' + c.opacity + '/' + c.translate + '/' + c.scale + '/' + c.display + '/an=' + pop.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join(','); };
  seq.push('before ' + rd());
  trig.click();
  [20, 60, 110, 170, 240].forEach(d => setTimeout(() => seq.push('open ' + rd()), d));
  setTimeout(() => { trig.click(); [20, 60, 110, 170, 240].forEach(d => setTimeout(() => seq.push('close ' + rd()), d));
    setTimeout(() => { window.__CL = { res: res, seq: seq, cls: pop.className }; }, 320); }, 340);
  return JSON.stringify(res) + ' | seq pending';
})()
