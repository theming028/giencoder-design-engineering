(() => {
  const pop = document.querySelector('[data-td-add-pop]');
  const btn = document.querySelector('[data-td-add-btn]');
  if (!pop || !btn) return 'NO DOM';
  if (pop.hasAttribute('hidden')) btn.click();          // 打开
  const cs = getComputedStyle(pop);
  return { phase: 'open', hidden: pop.hasAttribute('hidden'), display: cs.display,
           opacity: cs.opacity, translate: cs.translate, scale: cs.scale,
           anims: pop.getAnimations().map(a => a.transitionProperty || ('@' + a.animationName)) };
})()
