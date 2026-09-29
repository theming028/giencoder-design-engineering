(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const rafx = () => new Promise(r => requestAnimationFrame(r));
  const q = s => document.querySelector(s);
  const qa = s => [...document.querySelectorAll(s)];

  // 可见的 select 触发器（只挑真正显示出来的，排除隐藏副本）
  const trig = qa('.giencoder-select').filter(r => {
    const v = r.querySelector('.giencoder-select-view');
    return v && v.getBoundingClientRect().width > 0 && r.querySelector('.giencoder-select-popup');
  })[1];
  if (!trig) return 'NO_TRIG';
  const view = trig.querySelector('.giencoder-select-view');
  const pop = trig.querySelector('.giencoder-select-popup');
  const out = [];
  const box = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };

  // ---- 1) 打开 ----
  view.click();
  await wait(420);
  const cs = getComputedStyle(pop);
  out.push('OPEN pop rect=' + box(pop) + ' op=' + cs.opacity +
    ' anims=' + pop.getAnimations().map(a => (a.animationName || 'T:' + a.transitionProperty)).join('+') +
    ' disp=' + cs.display + ' inlineStyle=' + JSON.stringify(pop.getAttribute('style')));

  // ---- 2) 关闭 -> 逐帧看 ghost ----
  view.click();
  for (let n = 0; n < 14; n++) {
    await rafx();
    const gs = qa('[data-r74-ghost]');
    if (!gs.length) { out.push('f' + n + ' ghosts=0'); continue; }
    const g = gs[gs.length - 1];
    const gc = getComputedStyle(g);
    const kid = g.firstElementChild;
    const kc = kid ? getComputedStyle(kid) : null;
    const as = g.getAnimations();
    out.push('f' + n + ' n=' + gs.length +
      ' shellbox=' + box(g) + ' shellOp=' + gc.opacity.slice(0, 5) +
      ' shellAnims=' + as.length + '[' + as.map(a => JSON.stringify(a.effect ? a.effect.getKeyframes().map(k => k.opacity) : '-') + '@' + Math.round(a.currentTime || 0)).join('|') + ']' +
      ' kid=' + (kid ? box(kid) : '-') +
      ' kidOp=' + (kc ? kc.opacity.slice(0, 5) : '-') +
      ' kidAnims=' + (kid ? kid.getAnimations().length : '-') +
      ' kidInlinePos=' + (kid ? JSON.stringify(kid.getAttribute('style') || '').slice(0, 60) : '-') +
      ' inside=' + (kid ? (kid.getBoundingClientRect().top >= g.getBoundingClientRect().top - 1 &&
                           kid.getBoundingClientRect().bottom <= g.getBoundingClientRect().bottom + 1) : '-'));
  }
  return out.join('\n');
})()
