(() => {
  const rx = /(popup|dropdown|popover|tooltip|menu|pop|picker|panel|ctx|more|skill-pop)/i;
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    const cn = (typeof el.className === 'string' ? el.className : '') || '';
    const role = el.getAttribute('role') || '';
    const isCand = rx.test(cn) || /^(menu|listbox|dialog|tooltip)$/.test(role);
    if (!isCand) return;
    const cs = getComputedStyle(el);
    const pos = cs.position;
    if (pos !== 'absolute' && pos !== 'fixed') return;
    const r = el.getBoundingClientRect();
    out.push({
      cls: cn.slice(0, 90),
      role: role,
      hidden: el.hasAttribute('hidden'),
      op: cs.opacity,
      vis: cs.visibility,
      disp: cs.display,
      tp: cs.transitionProperty,
      td: cs.transitionDuration,
      anim: cs.animationName + ' ' + cs.animationDuration,
      z: cs.zIndex,
      wh: Math.round(r.width) + 'x' + Math.round(r.height)
    });
  });
  const seen = new Set();
  return out.filter(o => { const k = o.cls + '|' + o.z; if (seen.has(k)) return false; seen.add(k); return true; });
})()
