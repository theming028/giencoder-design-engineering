(() => {
  const out = [];
  document.querySelectorAll('[aria-haspopup], [aria-expanded], [role="combobox"]').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    out.push({ tag: el.tagName,
      cn: (typeof el.className === 'string' ? el.className : '').slice(0, 56),
      hs: el.getAttribute('aria-haspopup'), ex: el.getAttribute('aria-expanded'),
      role: el.getAttribute('role') || '', aria: el.getAttribute('aria-label') || '',
      ctl: el.getAttribute('aria-controls') || '',
      box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
      tx: (el.textContent || '').trim().slice(0, 16) });
  });
  return JSON.stringify(out, null, 1);
})()
