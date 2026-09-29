(() => {
  const trig = document.querySelectorAll('.giencoder-select-view.ws-dropdown-hover')[1]; // 默认权限
  const find = () => document.querySelector('[role="listbox"][aria-label="权限选择"]');
  const out = { t: (trig.textContent || '').trim(), open: [], ghosts: [] };
  trig.click();
  let n = 0;
  const loop = () => {
    const e = find();
    if (e) { const c = getComputedStyle(e);
      out.open.push(Math.round(performance.now() - t0) + ':op=' + c.opacity.slice(0, 5) + '/tr=' + c.translate + '/sx=' + c.scale +
                    '/an=' + e.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join('+')); }
    else out.open.push('absent');
    if (++n < 13) requestAnimationFrame(loop); else doClose();
  };
  const t0 = performance.now();
  const rdGhost = tag => {
    const g = document.querySelector('[data-r74-ghost]');
    if (!g) { out.ghosts.push([tag, 'absent']); return; }
    const gr = g.getBoundingClientRect(); const c = g.firstElementChild;
    const cr = c ? c.getBoundingClientRect() : null;
    const inside = cr ? (cr.x >= gr.x - 2 && cr.y >= gr.y - 2 && cr.x + cr.width <= gr.x + gr.width + 2 && cr.y + cr.height <= gr.y + gr.height + 2) : false;
    out.ghosts.push([tag, 'shell=' + [Math.round(gr.x), Math.round(gr.y), Math.round(gr.width), Math.round(gr.height)].join(',') +
      ' child=' + (cr ? [Math.round(cr.x), Math.round(cr.y), Math.round(cr.width), Math.round(cr.height)].join(',') : '-') +
      ' 内容在外壳内=' + inside + ' op=' + getComputedStyle(g).opacity.slice(0, 5) +
      ' fixed标记=' + (c ? (c.getAttribute('data-r75-fixed') || '-') : '-')]);
  };
  const doClose = () => { rdGhost('close前'); trig.click(); let m = 0;
    const l2 = () => { rdGhost('G' + m); if (++m < 7) requestAnimationFrame(l2); else window.__V2 = out; };
    requestAnimationFrame(l2); };
  requestAnimationFrame(loop);
  return 'started';
})()
