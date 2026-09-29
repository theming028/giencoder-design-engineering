(() => {
  const m = document.querySelector('main.dot-bg');
  const r = m.getBoundingClientRect();
  /* main 左下空白区（避开中间那张白色输入卡） */
  const x = r.left + 90, y = r.top + r.height - 110;
  const t = document.elementFromPoint(x, y);
  t.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, clientX: x, clientY: y, pointerId: 1 }));
  const g = m.querySelector('.r74-ripple');
  if (!g) return 'NO RIPPLE';
  g.getAnimations().forEach(a => { a.pause(); a.currentTime = window.__CT || 300; });
  const cs = getComputedStyle(g);
  return { hit: t.tagName + '.' + String(t.className).slice(0, 30), clickX: Math.round(x), clickY: Math.round(y),
           r: cs.getPropertyValue('--r74-rip-r'), op: cs.opacity };
})()
