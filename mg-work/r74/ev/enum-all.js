(() => {
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.position !== 'absolute' && cs.position !== 'fixed') return;
    const r = el.getBoundingClientRect();
    const vis = cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
    out.push({
      tag: el.tagName,
      cls: (typeof el.className === 'string' ? el.className : '').slice(0, 70),
      pos: cs.position, z: cs.zIndex, disp: cs.display, vis: cs.visibility, op: cs.opacity,
      anim: cs.animationName === 'none' ? '' : cs.animationName + '/' + cs.animationDuration,
      trans: cs.transitionProperty === 'all' && cs.transitionDuration === '0s' ? '' : (cs.transitionProperty + '/' + cs.transitionDuration).slice(0, 60),
      rect: Math.round(r.x) + ',' + Math.round(r.y) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height),
      shown: vis && r.width > 0
    });
  });
  const seen = new Set();
  return out.filter(o => { const k = o.cls + o.z + o.pos; if (seen.has(k)) return false; seen.add(k); return true; });
})()
