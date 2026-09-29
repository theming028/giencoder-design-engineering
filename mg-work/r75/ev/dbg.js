(() => {
  const t = document.querySelectorAll('.giencoder-select-view.ws-dropdown-hover')[1];
  const out = [];
  const rd = tag => {
    const gs = document.querySelectorAll('[data-r74-ghost]');
    if (!gs.length) { out.push([tag, 'ghosts=0']); return; }
    const g = gs[0];
    const as = g.getAnimations();
    out.push([tag, 'n=' + gs.length +
      ' rect=' + [Math.round(g.getBoundingClientRect().x), Math.round(g.getBoundingClientRect().y)].join(',') +
      ' op=' + +getComputedStyle(g).opacity.slice(0, 5) +
      ' anims=' + as.length + ' ' + as.map(a => a.playState + '/' + Math.round(a.currentTime || 0) + '/' +
        (a.effect ? JSON.stringify(a.effect.getKeyframes().map(k => k.opacity)) : '-')).join(' | ') +
      ' childOp=' + (g.firstElementChild ? +getComputedStyle(g.firstElementChild).opacity.slice(0, 5) : '-') +
      ' childVis=' + (g.firstElementChild ? getComputedStyle(g.firstElementChild).visibility : '-')]);
  };
  rd('W'); t.click();
  setTimeout(() => { rd('OPEN'); t.click();
    let n = 0;
    const loop = () => { rd('f' + n); if (++n < 14) requestAnimationFrame(loop); else window.__DBG = out; };
    requestAnimationFrame(loop);
  }, 400);
  return 'started';
})()
