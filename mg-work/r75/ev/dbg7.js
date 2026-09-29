(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const rafx = () => new Promise(r => requestAnimationFrame(r));
  const qa = s => [...document.querySelectorAll(s)];
  const box = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const vis = el => { const c = getComputedStyle(el), r = el.getBoundingClientRect();
    return c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) >= 0.05 && r.width > 12 && r.height > 12; };
  const out = [];

  // 0) 正常态：不应存在任何 ghost 外壳
  out.push('初始 ghost 数 = ' + qa('[data-r74-ghost]').length + '（应 0）');
  out.push('初始 [data-r74-ghost] * 命中元素数 = ' + qa('[data-r74-ghost] *').length + '（应 0）');

  // 1) 顶栏「切换空间」按钮 = header 内 div.relative 下的非「切换侧边栏」按钮
  const side = document.querySelector('button[aria-label="切换侧边栏"]');
  const wrap = side ? side.closest('div.relative') : null;
  const btns = wrap ? [...wrap.querySelectorAll('button')] : [];
  const trig = btns.find(b => b.getAttribute('aria-label') !== '切换侧边栏' && !b.querySelector('svg[data-x]'));
  const cand = trig || btns.find(b => b !== side);
  out.push('顶栏按钮数=' + btns.length + ' 选中=' + (cand ? (cand.getAttribute('aria-label') || '(无标签)') : 'NONE'));
  if (!cand) return out.join('\n') + '\nNO_TRIG';

  cand.click();
  await wait(430);
  const layer = qa('body > div[style*="position: fixed"]').filter(vis).find(e => !e.getAttribute('data-r74-ghost'));
  out.push('OPEN 门户=' + (layer ? box(layer) + ' style=' + JSON.stringify((layer.getAttribute('style') || '').slice(0, 110)) : 'none') +
    ' animName=' + (layer ? getComputedStyle(layer).animationName : '-'));

  const seen = [];
  const obs = new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => {
    if (n.nodeType === 1 && n.getAttribute && n.getAttribute('data-r74-ghost')) seen.push(n);
  })));
  obs.observe(document.body, { childList: true });
  cand.click();
  await wait(30); obs.disconnect();
  const g = seen[0];
  if (!g) return out.join('\n') + '\nNO_GHOST';
  out.push('ghost: ' + box(g) + ' style=' + JSON.stringify((g.getAttribute('style') || '').slice(0, 130)));
  out.push('  matches(①号规则 fixed+1000) = ' + g.matches('body > div[style*="position: fixed"][style*="z-index: 1000"]') +
    ' computedAnimName=' + getComputedStyle(g).animationName + '（应 none）');
  for (let n = 0; n < 11; n++) {
    const kid = g.firstElementChild;
    out.push('  n' + n + ' op=' + getComputedStyle(g).opacity.slice(0, 5) + ' box=' + box(g) +
      ' anims=' + g.getAnimations().length +
      ' kidOp=' + (kid ? getComputedStyle(kid).opacity.slice(0, 5) : '-') +
      ' kidAnims=' + (kid ? kid.getAnimations().length : '-') +
      ' inside=' + (kid ? kid.getBoundingClientRect().top >= g.getBoundingClientRect().top - 1 : '-'));
    await rafx();
  }
  return out.join('\n');
})()
