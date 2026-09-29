(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const rb = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const findPortal = () => [...document.querySelectorAll('body > div')]
    .find(e => /position:\s*fixed/.test(e.getAttribute('style') || '') && /z-index:\s*1000/.test(e.getAttribute('style') || ''));
  const btn = document.querySelector('button.ws-trigger-hover');
  if (!btn) return 'NO_BTN';
  btn.click();
  for (let t = 0; t <= 900; t += 100) {
    const p = findPortal();
    if (p) {
      const c = getComputedStyle(p);
      out.push('t=' + t + ' box=' + rb(p) + ' op=' + c.opacity.slice(0, 4) +
        ' anim=' + c.animationName + ' anims=' + p.getAnimations().length +
        ' kids=' + p.children.length + ' txt=' + JSON.stringify((p.textContent || '').trim().slice(0, 26)));
    } else out.push('t=' + t + ' portal=none');
    await wait(100);
  }
  const p0 = findPortal();
  out.push('关闭前 box=' + (p0 ? rb(p0) : 'none'));
  const seen = [];
  const obs = new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => {
    if (n.nodeType === 1 && n.getAttribute && n.getAttribute('data-r74-ghost')) seen.push(n);
  })));
  obs.observe(document.body, { childList: true });
  btn.click();
  await wait(120); obs.disconnect();
  out.push('关闭后 ghost=' + seen.length + (seen[0] ? ' box=' + rb(seen[0]) : ''));
  const p1 = findPortal();
  out.push('关闭后 portal=' + (p1 ? rb(p1) : 'none'));
  return out.join('\n');
})()
