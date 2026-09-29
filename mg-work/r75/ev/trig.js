(() => {
  const out = [];
  const pat = /combobox|giencoder-select|ws-dropdown|dropdown|trigger|chevron|filter/i;
  document.querySelectorAll('*').forEach(el => {
    const cn = typeof el.className === 'string' ? el.className : '';
    const role = el.getAttribute('role') || '';
    const exp = el.getAttribute('aria-expanded');
    const key = cn + '|' + role + '|' + (exp === null ? '' : exp);
    if (!pat.test(key)) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.width > 900) return;
    out.push({ i: out.length, tag: el.tagName, cls: cn.slice(0, 70), role: role, exp: exp,
               box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
               tx: (el.textContent || '').trim().slice(0, 24) });
  });
  return JSON.stringify(out.slice(0, 40), null, 1);
})()
