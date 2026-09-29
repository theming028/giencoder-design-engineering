(() => {
  const r = {};
  const add = { btn: document.querySelector('[data-td-add-btn]'), pop: document.querySelector('[data-td-add-pop]'), k: 'td-add-pop' };
  const skl = { btn: document.querySelector('[data-td-skill-btn]'), pop: document.querySelector('[data-td-skill-pop]'), k: 'td-skill-pop' };
  [add, skl].forEach(o => {
    if (!o.btn || !o.pop) { r[o.k] = 'NO DOM'; return; }
    if (!o.pop.hasAttribute('hidden')) o.btn.click();   // 关闭
    const cs = getComputedStyle(o.pop);
    r[o.k] = {
      phase: 'close',
      hidden: o.pop.hasAttribute('hidden'),
      displayDuringClose: cs.display,
      opacity: cs.opacity,
      translate: cs.translate,
      scale: cs.scale,
      anims: o.pop.getAnimations().map(a => a.transitionProperty || ('@' + a.animationName))
    };
  });
  return r;
})()
