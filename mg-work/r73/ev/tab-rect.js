(() => {
  const tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
  if (!tl) return 'NO TL';
  const sp = tl.querySelector('span[aria-hidden]');
  const tr = tl.getBoundingClientRect();
  const sr = sp ? sp.getBoundingClientRect() : null;
  const sel = tl.querySelector('[data-tab][aria-selected="true"]');
  const srr = sel ? sel.getBoundingClientRect() : null;
  const cs = sp ? getComputedStyle(sp) : null;
  return {
    file: location.pathname.split('/').pop(),
    selKey: sel ? sel.getAttribute('data-tab') : null,
    spRendered: sr ? [Math.round(sr.left - tr.left), Math.round(sr.width)] : null,
    selRendered: srr ? [Math.round(srr.left - tr.left), Math.round(srr.width)] : null,
    spInlineLeft: sp ? sp.style.left : null,
    spComputedLeft: cs ? cs.left : null,
    spTranslate: cs ? cs.translate : null,
    spStyleTranslate: sp ? sp.style.translate : null
  };
})()
