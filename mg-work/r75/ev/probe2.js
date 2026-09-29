(() => {
  const list = document.querySelectorAll(window.__T);
  const t = list[window.__TI || 0];
  if (!t) return 'NO-TRIGGER ' + window.__T + ' n=' + list.length;
  const PAT = /popup|dropdown|popper|tooltip|overlay|listbox|dialog|menu/i;
  const sk = el => {
    const cn = typeof el.className === 'string' ? el.className : '';
    return (cn + '|' + (el.getAttribute('role') || '') + '|' + (el.getAttribute('aria-label') || '')).slice(0, 80);
  };
  const sample = () => {
    const arr = [];
    document.querySelectorAll('*').forEach(el => {
      const k = sk(el);
      if (!PAT.test(k)) return;
      if (/option$|-item|option-list/i.test(k)) return;
      const cs = getComputedStyle(el);
      const a = el.getAnimations().map(x => x.animationName || 'T:' + x.transitionProperty).join('|');
      const r = el.getBoundingClientRect();
      arr.push(k + '§' + cs.display + '§' + cs.visibility + '§' + cs.opacity + '§' + cs.translate + '§' + cs.scale +
               '§' + a + '§' + (el.getAttribute('style') || '').slice(0, 70) + '§' + Math.round(r.x) + ',' + Math.round(r.y) + ',' + Math.round(r.width) + 'x' + Math.round(r.height));
    });
    return arr;
  };
  const log = []; const t0 = performance.now();
  log.push(['before', 0, sample()]);
  t.click();
  [10, 26, 45, 70, 100, 140, 190, 250, 330].forEach(d => setTimeout(() => log.push(['open', Math.round(performance.now() - t0), sample()]), d));
  setTimeout(() => { t.click();
    [10, 26, 45, 70, 100, 140, 190, 250, 330].forEach(d => setTimeout(() => log.push(['close', Math.round(performance.now() - t0), sample()]), d));
    setTimeout(() => { window.__P1 = log; }, 420);
  }, 430);
  return 'ok n=' + list.length + ' i=' + (window.__TI || 0) + ' ' + t.tagName + '.' + String(t.className).slice(0, 44);
})()
