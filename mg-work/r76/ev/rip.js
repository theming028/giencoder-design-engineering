/* r76 · 波点涟漪取帧：在 blank 处派发一次 pointerdown，然后把 .r74-ripple 的
   动画暂停并 seek 到 window.__T 毫秒 → 外层截图。
   一次调用只做一件事（截图必须由 CLI 出），所以由 window.__M 分相。 */
(async () => {
  const M = window.__M || 'fire';
  const host = document.querySelector('main.dot-bg');
  if (!host) return 'NO main.dot-bg';

  if (M === 'fire') {
    const r = host.getBoundingClientRect();
    /* 选一个「远离输入卡」的空白点：main 左下角内缩 140px */
    const x = Math.round(r.left + 140), y = Math.round(r.bottom - 140);
    host.dispatchEvent(new PointerEvent('pointerdown', {
      clientX: x, clientY: y, bubbles: true, cancelable: true, pointerId: 1
    }));
    await new Promise(r2 => requestAnimationFrame(r2));
    const el = host.querySelector('.r74-ripple');
    if (!el) return JSON.stringify({ ok: 0, why: 'no .r74-ripple' });
    const an = el.getAnimations()[0];
    if (!an) return JSON.stringify({ ok: 0, why: 'no animation' });
    an.pause();
    window.__RIP = el; window.__RAN = an;
    const cs = getComputedStyle(el);
    return JSON.stringify({
      ok: 1, at: [x, y], hostRect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)],
      dur: an.effect.getTiming().duration, dotSize: cs.backgroundSize,
      dotColor: cs.backgroundImage.slice(0, 120)
    });
  }
  if (M === 'seek') {
    const t = Number(window.__T || 0);
    if (!window.__RAN) return 'NO RAN';
    window.__RAN.currentTime = t;
    await new Promise(r2 => requestAnimationFrame(r2));
    await new Promise(r2 => requestAnimationFrame(r2));
    return 'seek ' + t + ' ok';
  }
  if (M === 'kill') {
    document.querySelectorAll('.r74-ripple').forEach(e => e.remove());
    return 'killed';
  }
  return 'ERRMODE';
})()
