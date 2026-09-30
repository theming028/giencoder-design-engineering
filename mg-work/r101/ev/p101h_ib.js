(() => {
  const el = document.querySelector('.r93-ib');
  if (!el) return JSON.stringify({ err: 'no .r93-ib' });
  const cs = getComputedStyle(el);
  return JSON.stringify({
    title: el.getAttribute('title'), bg: cs.backgroundColor, color: cs.color,
    sh: cs.boxShadow, bd: cs.borderTopWidth + ' ' + cs.borderTopColor
  });
})();
