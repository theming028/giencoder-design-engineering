(() => {
  const m = document.querySelector('main.dot-bg');
  const r = m.getBoundingClientRect();
  const x = r.left + r.width * 0.42, y = r.top + r.height * 0.62;
  const t = document.elementFromPoint(x, y);
  t.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, clientX: x, clientY: y, pointerId: 1 }));
  const g = m.querySelector('.r74-ripple');
  if (!g) return 'NO RIPPLE';
  const anims = g.getAnimations();
  const out = [];
  anims.forEach(a => { a.pause(); a.currentTime = window.__CT || 260; out.push(a.animationName + '@' + a.currentTime); });
  const cs = getComputedStyle(g);
  return { at: window.__CT, anims: out, ripR: cs.getPropertyValue('--r74-rip-r'), op: cs.opacity, mask: (cs.maskImage || '').slice(0, 120) };
})()
