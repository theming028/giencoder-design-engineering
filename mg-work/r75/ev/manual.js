(() => {
  const trig = document.querySelector('.giencoder-select-view');
  const root = trig.closest('.giencoder-select');
  const pop = root.querySelector('.giencoder-select-popup');
  const out = { ance: [], manual: [], react: [] };
  let a = pop.parentElement, d = 0;
  while (a && d < 12) { const c = getComputedStyle(a);
    out.ance.push(d + ' ' + a.tagName + '.' + String(a.className).slice(0, 34) + ' disp=' + c.display + ' vis=' + c.visibility + ' cv=' + (c.contentVisibility || '-') + ' ov=' + c.overflow);
    a = a.parentElement; d++; }
  // ① 手动只加类
  pop.classList.remove('giencoder-popup-open');
  if (pop.getAttribute('style') === '') pop.removeAttribute('style');
  void pop.offsetWidth;
  pop.classList.add('giencoder-popup-open');
  out.manual.push('sync op=' + getComputedStyle(pop).opacity + ' an=' + pop.getAnimations().length +
                  ' disp=' + getComputedStyle(pop).display + ' inline=' + (pop.getAttribute('style') || '-'));
  const t0 = performance.now(); let n = 0;
  const loop = () => {
    const c = getComputedStyle(pop);
    out.manual.push(Math.round(performance.now() - t0) + ':' + c.opacity + '/' + c.translate + '/' + c.scale + '/an=' + pop.getAnimations().map(x => x.animationName || 'T:' + x.transitionProperty).join(','));
    if (++n < 14 && performance.now() - t0 < 300) requestAnimationFrame(loop); else phase2();
  };
  const phase2 = () => {
    pop.classList.remove('giencoder-popup-open'); void pop.offsetWidth;
    setTimeout(() => {   // 回到 React 路径
      trig.click();
      const t1 = performance.now(); let m = 0;
      const loop2 = () => { const c = getComputedStyle(pop);
        out.react.push(Math.round(performance.now() - t1) + ':' + c.opacity + '/' + c.display + '/' + (pop.getAttribute('style') || '-') + '/an=' + pop.getAnimations().map(x => x.animationName || 'T:' + x.transitionProperty).join(','));
        if (++m < 12 && performance.now() - t1 < 300) requestAnimationFrame(loop2); else window.__MAN = out; };
      requestAnimationFrame(loop2);
    }, 200);
  };
  requestAnimationFrame(loop);
  return 'started';
})()
