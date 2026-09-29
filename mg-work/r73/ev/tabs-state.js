(() => {
  const tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
  if (!tl) return 'NO TL';
  const sp = tl.querySelector('span[aria-hidden]');
  const out = { file: location.pathname.split('/').pop(), indicator: sp ? { left: sp.style.left, width: sp.style.width, op: sp.style.opacity } : null, tabs: [] };
  tl.querySelectorAll('[data-tab]').forEach(b => {
    out.tabs.push({ k: b.getAttribute('data-tab'), sel: b.getAttribute('aria-selected'), offLeft: b.offsetLeft, offWidth: b.offsetWidth, txt: b.textContent });
  });
  return out;
})()
