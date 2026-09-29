(() => {
  const out = [];
  const all = document.querySelectorAll('*');
  for (const el of all) {
    const cn = typeof el.className === 'string' ? el.className : '';
    const role = el.getAttribute('role') || '';
    const lab = el.getAttribute('aria-label') || '';
    const key = cn + ' ' + role + ' ' + lab;
    if (!/popup|dropdown|popper|tooltip|overlay|dialog/i.test(key)) continue;
    if (!/popup|dropdown|popper|tooltip|overlay|dialog/i.test(key)) continue;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const anim = el.getAnimations ? el.getAnimations().map(a => a.animationName || (a.transitionProperty ? 'T:' + a.transitionProperty : '?')).join(',') : '';
    out.push({
      tag: el.tagName, cls: cn.slice(0, 90), role: role, lab: lab,
      vis: cs.visibility, op: cs.opacity, tr: cs.translate, sx: cs.scale,
      disp: cs.display, trs: cs.transition.slice(0, 120), an: anim,
      box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
      par: el.parentElement ? (el.parentElement.tagName + '.' + String(el.parentElement.className || '').slice(0, 40)) : 'null'
    });
  }
  return JSON.stringify(out, null, 1);
})()
