(() => {
  /* 采样顶栏滑块 left 随时间的取值：判断「2px」是稳态还是挂载过程中的瞬时值 */
  window.__t = { file: location.pathname.split('/').pop(), s: [] };
  const t0 = performance.now();
  const tick = () => {
    const tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
    const sp = tl && tl.querySelector('span[aria-hidden]');
    const cur = tl && tl.querySelector('[data-tab][aria-selected="true"]');
    window.__t.s.push([Math.round(performance.now() - t0), sp ? sp.style.left : '-', cur ? cur.getAttribute('data-tab') : '-']);
    if (performance.now() - t0 < 1600) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  return 'sampling ' + window.__t.file;
})()
