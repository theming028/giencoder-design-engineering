(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const rafx = () => new Promise(r => requestAnimationFrame(r));
  const qa = s => [...document.querySelectorAll(s)];
  const vis = el => { const c = getComputedStyle(el), r = el.getBoundingClientRect();
    return c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) >= 0.05 && r.width > 12 && r.height > 12; };
  const box = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const out = [];

  // 注入候选：把 ghost 外壳自身也纳入「无动画」
  const st = document.createElement('style');
  st.id = 'r75-probe-shell';
  st.textContent = '[data-r74-ghost]{animation:none !important;}';
  document.head.appendChild(st);
  out.push('injected [data-r74-ghost]{animation:none !important}');

  const trig = qa('[aria-haspopup]').filter(vis).find(e => /默认权限/.test(e.textContent || ''));
  trig.click(); await wait(430);

  const seen = [];
  const obs = new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => {
    if (n.nodeType === 1 && n.getAttribute && n.getAttribute('data-r74-ghost')) seen.push(n);
  })));
  obs.observe(document.body, { childList: true });
  trig.click();
  await wait(30); obs.disconnect();
  const g = seen[0];
  if (!g) return out.join('\n') + '\nNO_GHOST';
  out.push('shell computed animationName=' + getComputedStyle(g).animationName +
    ' (期望 none)');
  for (let n = 0; n < 12; n++) {
    const as = g.getAnimations(), kid = g.firstElementChild;
    out.push('n' + n + ' op=' + getComputedStyle(g).opacity.slice(0, 5) + ' box=' + box(g) +
      ' anims=' + as.length + '[' + as.map(a => (a.animationName || 'WAAPI') + '@' + Math.round(a.currentTime || 0)).join('|') + ']' +
      ' kidOp=' + (kid ? getComputedStyle(kid).opacity.slice(0, 5) : '-') +
      ' kidAnims=' + (kid ? kid.getAnimations().length : '-') +
      ' inside=' + (kid ? kid.getBoundingClientRect().top >= g.getBoundingClientRect().top - 1 : '-'));
    await rafx();
  }
  st.remove();
  return out.join('\n');
})()
