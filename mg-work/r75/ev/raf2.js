(() => {
  // 只挑「可见」的 select（rect.width>0），避免选中隐藏副本
  let root = null, v = null;
  document.querySelectorAll('.giencoder-select').forEach(r => {
    const x = r.querySelector('.giencoder-select-view');
    if (x && x.getBoundingClientRect().width > 0 && !root) { root = r; v = x; }
  });
  if (!root) return 'NO-VISIBLE-SELECT';
  const pop = root.querySelector('.giencoder-select-popup');
  if (!pop) return 'NO-POPUP';
  const old = document.getElementById('r75-try'); if (old) old.remove();
  const MODE = window.__MODE || 'none';
  if (MODE !== 'none') {
    const st = document.createElement('style'); st.id = 'r75-try';
    let css = '';
    if (MODE === 'disp' || MODE === 'both') css += '.giencoder-select-popup{display:block !important;}\n';
    if (MODE === 'both') css += '.giencoder-select-popup{transition:opacity 160ms cubic-bezier(0.34,0.69,0.1,1),translate 160ms cubic-bezier(0.34,0.69,0.1,1),scale 160ms cubic-bezier(0.34,0.69,0.1,1),visibility 0s 160ms;}\n.giencoder-select-popup.giencoder-popup-open{transition:opacity 160ms cubic-bezier(0.34,0.69,0.1,1),translate 160ms cubic-bezier(0.34,0.69,0.1,1),scale 160ms cubic-bezier(0.34,0.69,0.1,1),visibility 0s;}\n';
    st.textContent = css; document.head.appendChild(st);
  }
  const F = [];
  const rd = tag => { const c = getComputedStyle(pop);
    F.push(tag + ' ' + Math.round(performance.now() - t0) + 'ms op=' + c.opacity.slice(0, 6) + ' tr=' + c.translate + ' an=' + pop.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join('+')); };
  const t0 = performance.now();
  rd('W'); v.click();
  let n = 0;
  const loop = () => { rd('O'); if (++n < 9) requestAnimationFrame(loop); else ph2(); };
  const ph2 = () => { v.click(); const t1 = performance.now(); let m = 0;
    const l2 = () => { const c = getComputedStyle(pop);
      F.push('C ' + Math.round(performance.now() - t1) + 'ms op=' + c.opacity.slice(0, 6) + ' tr=' + c.translate + ' an=' + pop.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join('+'));
      if (++m < 9) requestAnimationFrame(l2); else window.__R2 = { mode: MODE, page: location.pathname.split('/').pop(), txt: (v.textContent || '').trim().slice(0, 10), closed: 'disp=' + getComputedStyle(pop).display + ' inline=' + (pop.getAttribute('style') || '-'), F: F }; };
    requestAnimationFrame(l2); };
  requestAnimationFrame(loop);
  return 'started ' + (v.textContent || '').trim().slice(0, 10);
})()
