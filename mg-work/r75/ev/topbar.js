(() => {
  const t = document.querySelector('button.ws-trigger-hover');
  const F = [];
  const rd = tag => {
    const d = document.querySelector('body > div[style*="z-index: 1000"]');
    if (!d) { F.push([tag, 'absent']); return; }
    const c = getComputedStyle(d);
    F.push([tag, 'inline="' + (d.getAttribute('style') || '').slice(0, 70) + '" disp=' + c.display + ' vis=' + c.visibility +
            ' op=' + c.opacity.slice(0, 7) + ' tr=' + c.translate + ' sx=' + c.scale +
            ' an=' + d.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join(',')]);
  };
  const fire = (el, type, C) => el.dispatchEvent(new C(type, { bubbles: true, cancelable: true, clientX: 140, clientY: 24, button: 0, buttons: type === 'mousedown' ? 1 : 0 }));
  rd('W'); fire(t, 'pointerdown', PointerEvent); fire(t, 'mousedown', MouseEvent); fire(t, 'pointerup', PointerEvent); fire(t, 'mouseup', MouseEvent); fire(t, 'click', MouseEvent);
  let n = 0;
  const loop = () => { rd('T' + n); if (++n < 12) requestAnimationFrame(loop); else window.__TOP = F; };
  requestAnimationFrame(loop);
  return 'started';
})()
