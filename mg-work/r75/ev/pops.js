(() => {
  const out = [];
  document.querySelectorAll('*').forEach(el => {
    const cn = typeof el.className === 'string' ? el.className : '';
    if (!/popup|dropdown|popper|menu$|-menu\b|overlay|panel|portal/i.test(cn)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return;
    const r = el.getBoundingClientRect();
    out.push({ tag: el.tagName, cls: cn.slice(0, 80), disp: cs.display, vis: cs.visibility,
               op: cs.opacity, zw: cs.zIndex, box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
               par: el.parentElement ? el.parentElement.tagName + '.' + String(el.parentElement.className).slice(0, 30) : '' });
  });
  return JSON.stringify(out.slice(0, 40), null, 1);
})()
