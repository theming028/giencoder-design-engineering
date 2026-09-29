(() => {
  const host = document.querySelector('header div:has(> button[aria-label="切换侧边栏"])');
  if (!host) return { file: location.pathname.split('/').pop(), err: 'NO HOST' };
  const hr = host.getBoundingClientRect();
  const items = [...host.children].map(c => {
    const r = c.getBoundingClientRect();
    const cs = getComputedStyle(c);
    return { tag: c.tagName, label: c.getAttribute('aria-label') || '(line)', x: Math.round(r.x - hr.x), w: Math.round(r.width), order: cs.order };
  });
  items.sort((a, b) => a.x - b.x);
  return { file: location.pathname.split('/').pop(), hostX: Math.round(hr.x), hostW: Math.round(hr.width),
           seq: items.map(i => i.label + '@' + i.x + '(w' + i.w + ',order' + i.order + ')') };
})()
