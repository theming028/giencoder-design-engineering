(() => {
  const r = {};
  const add = { btn: document.querySelector('[data-td-add-btn]'), pop: document.querySelector('[data-td-add-pop]'), k: 'td-add-pop' };
  const skl = { btn: document.querySelector('[data-td-skill-btn]'), pop: document.querySelector('[data-td-skill-pop]'), k: 'td-skill-pop' };
  const tipCss = (() => { const e = document.querySelector('.avatar-tooltip'); return e ? getComputedStyle(e).translate : null; })();
  [add, skl].forEach(o => {
    if (!o.btn || !o.pop) { r[o.k] = 'NO DOM'; return; }
    if (o.pop.hasAttribute('hidden')) o.btn.click();   // 打开
    const cs = getComputedStyle(o.pop);
    r[o.k] = {
      phase: 'open',
      hidden: o.pop.hasAttribute('hidden'),
      display: cs.display,
      opacity: cs.opacity,
      translate: cs.translate,
      scale: cs.scale,
      anims: o.pop.getAnimations().map(a => a.transitionProperty || ('@' + a.animationName))
    };
  });
  r['avatar-tooltip_computed_translate'] = tipCss;
  r['avatar-tooltip_transition'] = (() => { const e = document.querySelector('.avatar-tooltip'); if (!e) return null; const c = getComputedStyle(e); return c.transitionProperty + ' / ' + c.transitionDuration + ' / ' + c.transitionDelay; })();
  return r;
})()
