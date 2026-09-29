(() => {
  const CSS = `
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
  const st = document.createElement('style');
  st.id = 'probe-r73-pop';
  st.textContent = CSS;
  document.head.appendChild(st);

  const btn = document.querySelector('[data-td-add-btn]');
  const pop = document.querySelector('[data-td-add-pop]');
  if (!btn || !pop) return { err: 'btn/pop not found' };

  btn.click();
  const cs1 = getComputedStyle(pop);
  const anims1 = pop.getAnimations().map(a => a.transitionProperty || a.animationName);

  return new Promise(res => {
    setTimeout(() => {
      const cs2 = getComputedStyle(pop);
      res({
        afterClick: { hidden: pop.hasAttribute('hidden'), disp: cs1.display, op: cs1.opacity, tr: cs1.translate, sc: cs1.scale, anims: anims1 },
        after260ms: { disp: cs2.display, op: cs2.opacity, tr: cs2.translate, sc: cs2.scale },
        supports: {
          startingStyle: CSS.supports('selector(:has(*))') && 'CSSStartingStyleRule' in window,
          allowDiscrete: CSS.supports('transition-behavior', 'allow-discrete')
        }
      });
    }, 260);
  });
})()
