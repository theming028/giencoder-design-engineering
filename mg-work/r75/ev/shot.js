(() => {
  const mode = window.__M;
  const qa = s => [...document.querySelectorAll(s)];
  const vis = el => { const c = getComputedStyle(el), r = el.getBoundingClientRect();
    return c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) >= 0.05 && r.width > 12 && r.height > 12; };
  const trig = qa('[aria-haspopup]').filter(vis).find(e => /默认权限/.test(e.textContent || ''));
  if (!trig) return 'NO_TRIG';
  const rb = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };

  if (mode === 'open') {
    trig.click();
    return new Promise(r => setTimeout(() => {
      const e = document.querySelector('[role="listbox"][aria-label="权限选择"]');
      document.getAnimations().forEach(a => { try { a.pause(); } catch (e) { } });
      r(JSON.stringify({ mode: 'open', rect: e ? rb(e) : null, op: e ? getComputedStyle(e).opacity : '-' }));
    }, 430));
  }
  // close：关掉后冻结 ghost 首帧
  trig.click();
  return new Promise(r => requestAnimationFrame(() => {
    const g = document.querySelector('[data-r74-ghost]');
    if (!g) { r('NO-GHOST'); return; }
    const as = g.getAnimations();
    document.getAnimations().forEach(a => { try { a.pause(); a.currentTime = 0; } catch (e) { } });
    r(JSON.stringify({ mode: 'close', ghost: rb(g), op: getComputedStyle(g).opacity,
      anims: as.length, kid: g.firstElementChild ? rb(g.firstElementChild) : null,
      kidOp: g.firstElementChild ? getComputedStyle(g.firstElementChild).opacity : '-' }));
  }));
})()
