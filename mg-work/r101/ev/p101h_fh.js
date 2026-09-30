(() => {
  const el = document.querySelector('.r93-fh');
  if (!el) return JSON.stringify({ err: 'no .r93-fh' });
  const cs = getComputedStyle(el);
  const ft = el.querySelector('.r93-ft'), cv = el.querySelector('.r93-cv');
  const lb = el.closest('.r93-fold');
  const fc = lb ? lb.querySelector('.r93-fc') : null;
  return JSON.stringify({
    fh_bg: cs.backgroundColor, fh_color: cs.color,
    ft_color: ft ? getComputedStyle(ft).color : null,
    cv_color: cv ? getComputedStyle(cv).color : null,
    fc_bg: fc ? getComputedStyle(fc).backgroundColor : null,
    fc_color: fc ? getComputedStyle(fc).color : null
  });
})();
