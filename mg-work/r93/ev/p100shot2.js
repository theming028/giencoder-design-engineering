(() => {
  const host = document.querySelector('.r93-conv-host');
  const f = [...host.querySelectorAll('.r93-fold')].find(x => (x.textContent || '').includes('调用 5 个工具'));
  f.scrollIntoView({ block: 'start' });
  window.scrollBy(0, -60);
  const r = f.getBoundingClientRect();
  return JSON.stringify({ y: Math.round(r.y), h: Math.round(r.height) });
})();
