(() => {
  const CSS_TEXT = `
  .td-add-pop, .td-skill-pop {
    transition: opacity .16s cubic-bezier(.34,.69,.1,1),
                translate .16s cubic-bezier(.34,.69,.1,1),
                scale .16s cubic-bezier(.34,.69,.1,1),
                display .16s allow-discrete;
  }
  .td-add-pop[hidden], .td-skill-pop[hidden] { opacity: 0; translate: 0 4px; scale: .97; }
  @starting-style {
    .td-add-pop:not([hidden]), .td-skill-pop:not([hidden]) { opacity: 0; translate: 0 4px; scale: .97; }
  }`;
  let st = document.getElementById('probe-r73-pop');
  if (!st) { st = document.createElement('style'); st.id = 'probe-r73-pop'; document.head.appendChild(st); }
  st.textContent = CSS_TEXT;

  const btn = document.querySelector('[data-td-add-btn]');
  const pop = document.querySelector('[data-td-add-pop]');
  if (!btn || !pop) return { err: 'btn/pop not found' };
  if (pop.hasAttribute('hidden')) btn.click();
  const cs = getComputedStyle(pop);
  return {
    hidden: pop.hasAttribute('hidden'),
    disp: cs.display, op: cs.opacity, tr: cs.translate, sc: cs.scale,
    anims: pop.getAnimations().map(a => a.transitionProperty || ('@' + a.animationName)),
    supportsStartingStyle: 'CSSStartingStyleRule' in window,
    supportsAllowDiscrete: CSS.supports('transition-behavior', 'allow-discrete'),
    computedTransition: cs.transitionProperty + ' / ' + cs.transitionDuration
  };
})()
