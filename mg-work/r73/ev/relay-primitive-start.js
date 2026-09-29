(() => {
  /* 在真实页面上复演接力原语：钉位(transition:none, translate=dx) → rAF×2 → 交还过渡并 translate:0
     唯一差别：把过渡拉长到 3000ms —— 200ms 的窗口截图工具抓不住，拉长只为「可采样 + 可截图」。 */
  const tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
  const sp = tl && tl.querySelector('span[aria-hidden]');
  if (!sp) return 'NO SPAN';
  const tlR = tl.getBoundingClientRect();
  const nowLeft = sp.getBoundingClientRect().left - tlR.left;   /* 相对 tablist，与出发页记录同口径 */
  const dx = 2 - nowLeft;                     /* 假装从「基础工作台」(2px) 滑过来 */
  const SPRING = 'cubic-bezier(.34,1.56,.64,1)';

  sp.style.transition = 'none';
  sp.style.translate = dx + 'px 0px';
  window.__r73 = { file: location.pathname.split('/').pop(), dx: dx, samples: [], anims: [] };

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      sp.style.transition = 'translate 3000ms ' + SPRING;
      sp.style.translate = '0px 0px';
      window.__r73.anims = sp.getAnimations().map(a => a.transitionProperty + ' ' + a.effect.getTiming().duration + 'ms');
      const t0 = performance.now();
      const tick = () => {
        const r = sp.getBoundingClientRect();
        const tl2 = tl.getBoundingClientRect();
        window.__r73.samples.push(Math.round((r.left - tl2.left) * 10) / 10);
        if (performance.now() - t0 < 3600) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  });
  return 'armed for ' + location.pathname.split('/').pop() + ' dx=' + dx;
})()
