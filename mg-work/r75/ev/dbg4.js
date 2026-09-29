(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const rafx = () => new Promise(r => requestAnimationFrame(r));
  const qa = s => [...document.querySelectorAll(s)];
  const box = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const vis = el => { const c = getComputedStyle(el), r = el.getBoundingClientRect();
    return c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) >= 0.05 && r.width > 12 && r.height > 12; };
  const desc = a => {
    const t = a.effect && a.effect.target;
    return [a.constructor.name,
      a.animationName || a.transitionProperty || '-',
      'play=' + a.playState,
      't=' + Math.round(a.currentTime || 0),
      'target=' + (t ? t.tagName + '.' + ((t.className || '') + '').trim().split(/\s+/)[0] + (t.getAttribute('data-r74-ghost') ? '[GHOST]' : '') + (t.getAttribute('aria-label') ? '[' + t.getAttribute('aria-label') + ']' : '') : '-')
    ].join('/');
  };
  const out = [];

  // 打开「默认权限」
  const trig = qa('[aria-haspopup]').filter(vis).find(e => /默认权限/.test(e.textContent || ''));
  if (!trig) return 'NO_TRIG';
  trig.click();
  await wait(430);
  const layer = qa('[role="listbox"]').filter(vis).filter(e => !e.closest('[data-r74-ghost]'))
    .find(e => e.getBoundingClientRect().width > 200);
  out.push('OPEN layer=' + (layer ? box(layer) + ' aria=' + layer.getAttribute('aria-label') : 'none'));

  // 关闭 + 等 ghost 出现的那一帧开始采样
  const seen = [];
  const obs = new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => {
    if (n.nodeType === 1 && n.getAttribute && n.getAttribute('data-r74-ghost')) seen.push(n);
  })));
  obs.observe(document.body, { childList: true });
  trig.click();
  await wait(40);
  obs.disconnect();
  const g = seen[0];
  out.push('ghostCreated=' + !!g + (g ? ' box=' + box(g) : ''));
  if (g) {
    // 已经过去 ~40ms，先看当前状态
    for (let n = 0; n < 8; n++) {
      const gc = getComputedStyle(g), kid = g.firstElementChild;
      const as = g.getAnimations();
      out.push('n' + n + ' shellOp=' + gc.opacity.slice(0, 5) + ' anims=' + as.length +
        '\n      ' + as.map(desc).join('\n      ') +
        '\n      kidOp=' + (kid ? getComputedStyle(kid).opacity.slice(0, 5) : '-') +
        ' kidAnims=' + (kid ? kid.getAnimations().length : '-') +
        ' kidAnimNames=' + (kid ? JSON.stringify(kid.getAnimations().map(a => a.animationName || a.transitionProperty)) : '-') +
        ' kidMatchB=' + (kid ? kid.matches('[role="listbox"][aria-label="权限选择"]') : '-') +
        ' kidAn= ' + (kid ? getComputedStyle(kid).animationName : '-'));
      await rafx();
    }
  }
  return out.join('\n');
})()
