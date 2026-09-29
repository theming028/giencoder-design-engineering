(() => {
  const m = document.querySelector('main.dot-bg');
  const r = m.getBoundingClientRect();
  const x = r.left + r.width * 0.5, y = r.top + r.height * 0.7;
  const t = document.elementFromPoint(x, y);
  t.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, clientX: x, clientY: y, pointerId: 1 }));
  return { x: Math.round(x), y: Math.round(y), hit: t.tagName + '.' + String(t.className).slice(0, 40) };
})()
