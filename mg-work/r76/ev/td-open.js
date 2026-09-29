/* r76 · 任务详情：普通态 → 展开 的逐帧几何（判定展开是否也瞬移） */
(async () => {
  const g = s => document.querySelector(s);
  const R = g('.td-root');
  const btn = () => [...document.querySelectorAll('.td-right-bar button[aria-pressed]')]
    .find(x => (x.getAttribute('aria-label') || '').indexOf('侧栏') >= 0);
  const rect = e => { const b = e.getBoundingClientRect(); return [+b.left.toFixed(1), +b.right.toFixed(1), +b.width.toFixed(1)]; };

  const before = (() => {
    const ri = g('.td-right'), lf = g('.td-left'), sl = g('.td-browse-slot');
    return { r: rect(ri), l: rect(lf), s: sl ? rect(sl) : null, brw: getComputedStyle(ri).width };
  })();

  const out = [], t0 = performance.now();
  const tick = () => {
    const ri = g('.td-right'), lf = g('.td-left'), sl = g('.td-browse-slot');
    out.push({ t: Math.round(performance.now() - t0), r: rect(ri), l: rect(lf),
      s: sl ? rect(sl) : null, cls: R.className.split(' ').filter(c => c.startsWith('is-')).join(',') });
    if (performance.now() - t0 < 500) requestAnimationFrame(tick);
  };
  btn().click();
  requestAnimationFrame(tick);
  await new Promise(r => setTimeout(r, 600));
  return JSON.stringify({ before, seq: out });
})()
