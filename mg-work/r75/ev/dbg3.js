(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const rafx = () => new Promise(r => requestAnimationFrame(r));
  const qa = s => [...document.querySelectorAll(s)];
  const box = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const vis = el => { const c = getComputedStyle(el), r = el.getBoundingClientRect();
    return c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) >= 0.05 && r.width > 12 && r.height > 12; };

  const out = [];

  // 触发器枚举（去重 + 只看可见）
  const set = new Set();
  qa('[aria-haspopup],[aria-expanded],[role="combobox"]').forEach(e => { if (vis(e)) set.add(e); });
  const trig = [...set];
  out.push('TRIGGERS=' + trig.length);

  for (let i = 0; i < trig.length; i++) {
    const t = trig[i];
    const desc = '[' + i + '] ' + (t.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 18) +
      ' | role=' + (t.getAttribute('role') || '-') + ' popup=' + (t.getAttribute('aria-haspopup') || '-');
    out.push('── ' + desc);
    // 先清干净
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    await wait(260);

    t.click();
    await wait(420);

    // 找可见浮层
    const cands = qa('[role="menu"],[role="listbox"],body > div[style*="position: fixed"]').filter(e => vis(e) && !e.closest('[data-r74-ghost]'));
    out.push('   OPEN layers=' + cands.length + ' ' + cands.map(e =>
      '{tag:' + e.tagName + ' role:' + (e.getAttribute('role') || '-') + ' cls:' + (e.className || '').toString().slice(0, 30) +
      ' box:' + box(e) + ' inSEL:' + (e.matches('[role="menu"],[role="listbox"]') || (e.parentElement === document.body && /position:\s*fixed/.test(e.getAttribute('style') || ''))) + '}').join(' '));

    // 关闭
    t.click();
    for (let n = 0; n < 14; n++) {
      await rafx();
      const gs = qa('[data-r74-ghost]');
      if (!gs.length) { if (n === 0 || n === 13) out.push('   f' + n + ' ghosts=0'); continue; }
      const g = gs[gs.length - 1], gc = getComputedStyle(g), kid = g.firstElementChild;
      const kb = kid ? kid.getBoundingClientRect() : null, gb = g.getBoundingClientRect();
      const kc = kid ? getComputedStyle(kid) : null;
      out.push('   f' + n + ' ghosts=' + gs.length +
        ' shell[' + gc.opacity.slice(0, 5) + ' ' + box(g) + ' anims=' + g.getAnimations().length + ']' +
        ' kid[' + (kid ? kc.opacity.slice(0, 5) + ' ' + box(kid) + ' an=' + kid.getAnimations().length +
          ' pos=' + kc.position + '/' + kc.left + '/' + kc.top : '-') + ']' +
        ' inside=' + (!!kid && kb.top >= gb.top - 1 && kb.bottom <= gb.bottom + 1));
    }
  }
  return out.join('\n');
})()
