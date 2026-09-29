(() => {
  const PAT = /popup|dropdown|popper|tooltip|overlay|listbox|dialog/i;
  const key = el => {
    const cn = typeof el.className === 'string' ? el.className : '';
    const role = el.getAttribute('role') || '';
    return cn + ' ' + role;
  };
  const snap = () => {
    const arr = [];
    document.querySelectorAll('*').forEach(el => {
      const k = key(el);
      if (!PAT.test(k)) return;
      // 只收"容器型"节点：忽略 option/item 这类子项
      if (/option|menu-item|dropdown-item/i.test(k)) return;
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      arr.push({ cn: (typeof el.className === 'string' ? el.className : '').slice(0, 64),
                 role: el.getAttribute('role') || '', aria: el.getAttribute('aria-label') || '',
                 disp: cs.display, vis: cs.visibility, op: cs.opacity,
                 tr: cs.translate, sx: cs.scale, trs: cs.transition.slice(0, 80),
                 an: cs.animationName, inline: (el.getAttribute('style') || '').slice(0, 70),
                 box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
                 par: el.parentElement ? el.parentElement.tagName : '' });
    });
    return arr;
  };
  const cands = [];
  const seen = new Set();
  document.querySelectorAll('*').forEach(el => {
    const cn = typeof el.className === 'string' ? el.className : '';
    const role = el.getAttribute('role') || '';
    const hs = el.getAttribute('aria-haspopup');
    const ex = el.getAttribute('aria-expanded');
    const hit = hs !== null || ex !== null || role === 'combobox' ||
      /dropdown|select|trigger|chevron|menu-|more|kebab|ellipsis|avatar/i.test(cn);
    if (!hit) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || r.width > 420) return;
    if (seen.has(el)) return; seen.add(el);
    cands.push(el);
  });
  const steps = [];
  let i = -1;
  const tick = () => {
    if (i >= 0) {
      const s = steps[i];
      s.after = snap();
    }
    i++;
    if (i >= cands.length) { window.__CEN = { cands: cands.length, steps: steps }; return; }
    const el = cands[i];
    const r = el.getBoundingClientRect();
    const cn = typeof el.className === 'string' ? el.className : '';
    steps.push({ i: i, tag: el.tagName, cn: cn.slice(0, 64), role: el.getAttribute('role') || '',
                 aria: el.getAttribute('aria-label') || '', tx: (el.textContent || '').trim().slice(0, 20),
                 box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
                 before: snap() });
    try { el.click(); } catch (e) {}
    setTimeout(() => {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
      document.body.click();
      setTimeout(tick, 240);
    }, 260);
  };
  tick();
  return 'cands=' + cands.length;
})()
