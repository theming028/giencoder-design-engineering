(() => {
  const H = document.querySelector('.r93-conv-host');
  const cs = el => getComputedStyle(el);
  const r = el => { const b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const folds = Array.from(H.querySelectorAll('.r93-fold[data-open="1"]'));
  const f = folds[1] || folds[0];
  if (!f) return JSON.stringify({ err: 'no open fold' });
  const head = f.querySelector(':scope > .r93-fh');
  const ft = head.querySelector('.r93-ft');
  const slot = head.querySelector('.r93-cv');
  const svg = slot.querySelector('svg');
  const before = { open: f.getAttribute('data-open'), ftBox: r(ft), ftX: Math.round(ft.getBoundingClientRect().left),
                   slotBox: r(slot), slotW: cs(slot).width, svgW: cs(svg).width, svgBox: r(svg) };
  head.click();                                   /* 真实折叠 */
  const fc = f.querySelector(':scope > .r93-fc');
  const label = fc.querySelector('.r93-t14');
  const ico = fc.querySelector('.r93-c3');
  const after = { open: f.getAttribute('data-open'), fhDisplay: cs(head).display, fcDisplay: cs(fc).display,
                  fxBox: r(fc), labelBox: r(label), labelX: Math.round(label.getBoundingClientRect().left),
                  icoBox: ico ? r(ico) : null, icoW: ico ? cs(ico).width : null };
  fc.setAttribute('data-r101-fc', '1');
  return JSON.stringify({ foldText: (head.querySelector('.r93-ft').textContent || '').trim(),
                          before, after, dx: after.labelX - before.ftX });
})();
