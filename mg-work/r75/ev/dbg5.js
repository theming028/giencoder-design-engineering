(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const qa = s => [...document.querySelectorAll(s)];
  const vis = el => { const c = getComputedStyle(el), r = el.getBoundingClientRect();
    return c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) >= 0.05 && r.width > 12 && r.height > 12; };
  const out = [];

  // ---- 1) 手工建空壳 ----
  const shellA = document.createElement('div');
  shellA.setAttribute('data-r74-ghost', '1');
  shellA.style.cssText = 'position:fixed;left:0;top:0;width:100px;height:100px;z-index:1000;pointer-events:none;overflow:hidden;';
  document.body.appendChild(shellA);
  out.push('A 空壳: anims=' + shellA.getAnimations().length +
    ' matchesB=' + shellA.matches('[role="listbox"][aria-label="权限选择"]') +
    ' animName=' + getComputedStyle(shellA).animationName +
    ' zidx=' + getComputedStyle(shellA).zIndex);

  // ---- 2) 手工建带 listbox 内胆的壳 ----
  const shellB = document.createElement('div');
  shellB.setAttribute('data-r74-ghost', '1');
  shellB.style.cssText = 'position:fixed;left:0;top:0;width:280px;height:126px;z-index:1000;pointer-events:none;overflow:hidden;';
  shellB.innerHTML = '<div role="listbox" aria-label="权限选择" style="position:absolute;left:0;top:0;width:280px;height:126px"><span>x</span></div>';
  document.body.appendChild(shellB);
  const k = shellB.firstElementChild;
  out.push('B 带listbox内胆: shellA anims=' + shellB.getAnimations().length +
    ' effectTargetIsShell=' + JSON.stringify(shellB.getAnimations().map(a => a.effect && a.effect.target === shellB)) +
    ' subtree=true -> ' + shellB.getAnimations({ subtree: true }).length +
    ' | kid anims=' + k.getAnimations().length +
    ' kidAnimName=' + getComputedStyle(k).animationName +
    ' kidPos=' + getComputedStyle(k).position);
  shellA.remove(); shellB.remove();

  // ---- 3) 真 ghost：逐条比对 target ----
  const trig = qa('[aria-haspopup]').filter(vis).find(e => /默认权限/.test(e.textContent || ''));
  trig.click(); await wait(430);
  const seen = [];
  const obs = new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => {
    if (n.nodeType === 1 && n.getAttribute && n.getAttribute('data-r74-ghost')) seen.push(n);
  })));
  obs.observe(document.body, { childList: true });
  trig.click();
  await wait(50); obs.disconnect();
  const g = seen[0];
  if (!g) return out.join('\n') + '\nNO_GHOST';
  const as = g.getAnimations();
  out.push('真ghost: cssText=' + JSON.stringify(g.getAttribute('style')));
  out.push('  shell.matches(B)=' + g.matches('[role="listbox"][aria-label="权限选择"]') +
    ' matches(listbox)=' + g.matches('[role="listbox"]') +
    ' matches(fixed1000)=' + g.matches('body > div[style*="position: fixed"][style*="z-index: 1000"]'));
  out.push('  getAnimations()=' + as.length + ' {subtree:true}=' + g.getAnimations({ subtree: true }).length);
  as.forEach((a, i) => out.push('  a' + i + ' = ' + a.constructor.name + '/' + (a.animationName || a.transitionProperty || '-') +
    ' targetIsShell=' + (a.effect && a.effect.target === g) +
    ' targetTag=' + (a.effect && a.effect.target ? a.effect.target.tagName + '|' + ((a.effect.target.className || '') + '').slice(0, 24) + '|aria=' + (a.effect.target.getAttribute('aria-label') || '-') : '-')));
  out.push('  shell computed animationName=' + getComputedStyle(g).animationName);
  return out.join('\n');
})()
