(() => {
  const btn = document.querySelector('[data-td-add-btn]');
  const pop = document.querySelector('[data-td-add-pop]');
  if (!btn || !pop) return { err: 'not found' };
  if (!pop.hasAttribute('hidden')) btn.click();      // 关闭
  const cs = getComputedStyle(pop);
  return {
    hidden: pop.hasAttribute('hidden'),
    dispDuringClose: cs.display,
    op: cs.opacity, tr: cs.translate, sc: cs.scale,
    anims: pop.getAnimations().map(a => a.transitionProperty || ('@' + a.animationName))
  };
})()
