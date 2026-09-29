(() => {
  const mode = window.__M;
  if (mode === 'open') {
    const t = document.querySelectorAll('.giencoder-select-view.ws-dropdown-hover')[1];
    t.click();
    return new Promise(r => setTimeout(() => {
      const e = document.querySelector('[role="listbox"][aria-label="权限选择"]');
      const rc = e.getBoundingClientRect();
      window.__RECT = [Math.round(rc.x), Math.round(rc.y), Math.round(rc.width), Math.round(rc.height)];
      r(JSON.stringify(window.__RECT));
    }, 400));
  }
  // close → 冻结 ghost 首帧
  const t = document.querySelectorAll('.giencoder-select-view.ws-dropdown-hover')[1];
  t.click();
  return new Promise(r => requestAnimationFrame(() => {
    const g = document.querySelector('[data-r74-ghost]');
    if (!g) { r('NO-GHOST'); return; }
    const a = g.getAnimations()[0];
    if (a) { a.pause(); a.currentTime = 0; }
    const rc = g.getBoundingClientRect();
    r(JSON.stringify({ ghost: [Math.round(rc.x), Math.round(rc.y), Math.round(rc.width), Math.round(rc.height)],
                       op: getComputedStyle(g).opacity, paused: !!a }));
  }));
})()
