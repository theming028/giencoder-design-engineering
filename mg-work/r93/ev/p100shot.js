(() => {
  const f = [...document.querySelectorAll('.r93-fold')].find(x => (x.textContent || '').includes('调用 5 个工具'));
  if (!f) return 'NOTFOUND';
  f.scrollIntoView({ block: 'start' });
  const r = f.getBoundingClientRect();
  return JSON.stringify({ y: Math.round(r.y), h: Math.round(r.height) });
})();
