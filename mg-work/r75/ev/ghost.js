(() => {
  const t = document.querySelector('button[aria-haspopup="menu"]');
  const F = [];
  const rd = tag => {
    const g = document.querySelector('[data-r74-ghost]');
    if (!g) { F.push([tag, 'G-absent']); return; }
    const gr = g.getBoundingClientRect();
    const c = g.firstElementChild;
    const cr = c ? c.getBoundingClientRect() : null;
    const cc = c ? getComputedStyle(c) : null;
    F.push([tag, 'ghost=' + [Math.round(gr.x), Math.round(gr.y), Math.round(gr.width), Math.round(gr.height)].join(',') +
      ' child=' + (cr ? [Math.round(cr.x), Math.round(cr.y), Math.round(cr.width), Math.round(cr.height)].join(',') : '-') +
      ' childPos=' + (cc ? cc.position + '/' + cc.top + '/' + cc.overflow : '-') +
      ' ghostOp=' + getComputedStyle(g).opacity.slice(0, 5)]);
  };
  rd('W'); t.click();                       // 打开
  setTimeout(() => {
    rd('OPEN');
    t.click();                              // 关闭 → 触发 ghost
    let n = 0;
    const loop = () => { rd('G' + n); if (++n < 8) requestAnimationFrame(loop); else { window.__G = F; } };
    requestAnimationFrame(loop);
  }, 320);
  return 'started';
})()
