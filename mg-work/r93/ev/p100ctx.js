(() => {
  const box = document.querySelector('.r93-ctx');
  if (!box) return JSON.stringify({ exists: false });
  const r = box.getBoundingClientRect();
  return JSON.stringify({ exists: true, open: box.classList.contains('giencoder-popup-open'),
    w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y),
    items: box.querySelectorAll('.giencoder-dropdown-item').length,
    dividers: box.querySelectorAll('.giencoder-dropdown-divider').length });
})();
