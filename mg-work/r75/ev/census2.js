(() => {
  const PAT = /popup|dropdown|popper|tooltip|overlay|listbox|dialog/i;
  const BAD = /发送|删除|清空|退出|提交|重置|注销|登出|停止|保存|下载/;
  const key = el => {
    const cn = typeof el.className === 'string' ? el.className : '';
    return cn + ' | ' + (el.getAttribute('role') || '') + ' | ' + (el.getAttribute('aria-label') || '');
  };
  const snap = () => {
    const arr = [];
    document.querySelectorAll('*').forEach(el => {
      const k = key(el);
      if (!PAT.test(k)) return;
      if (/option|menu-item|dropdown-item/i.test(k)) return;
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      arr.push([k, cs.display, cs.visibility, cs.opacity, cs.translate, cs.scale,
                cs.animationName, (el.getAttribute('style') || '').slice(0, 80),
                Math.round(r.x) + ',' + Math.round(r.y) + ',' + Math.round(r.width) + 'x' + Math.round(r.height),
                el.parentElement ? el.parentElement.tagName : '']);
    });
    return arr;
  };
  const cands = []; const seen = new Set();
  document.querySelectorAll('*').forEach(el => {
    if (el.tagName === 'SVG' || el.tagName === 'PATH' || el.tagName === 'BODY' || el.tagName === 'HTML') return;
    const cn = typeof el.className === 'string' ? el.className : '';
    const role = el.getAttribute('role') || '';
    const hs = el.getAttribute('aria-haspopup');
    const ex = el.getAttribute('aria-expanded');
    const ti = el.getAttribute('title') || '';
    const hit = hs !== null || ex !== null || role === 'combobox' || role === 'button' ||
      /dropdown|select|trigger|chevron|menu|more|kebab|ellipsis|avatar|cursor-pointer/i.test(cn + ' ' + ti);
    if (!hit) return;
    if (BAD.test((el.textContent || '').slice(0, 40))) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || r.width > 460) return;
    let a = el; while (a) { if (seen.has(a)) return; a = a.parentElement; }
    seen.add(el); cands.push(el);
  });
  const steps = []; let i = -1;
  const tick = () => {
    if (i >= 0) {                       // ★ 先采样，再清理
      const s = steps[i]; s.after = snap();
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, clientX: 5, clientY: 5 }));
      document.body.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: 5, clientY: 5 }));
      document.body.click();
    }
    i++;
    if (i >= cands.length) { window.__CEN = { n: cands.length, steps: steps }; return; }
    const el = cands[i]; const r = el.getBoundingClientRect();
    steps.push({ i: i, tag: el.tagName, cn: (typeof el.className === 'string' ? el.className : '').slice(0, 60),
                 role: el.getAttribute('role') || '', aria: el.getAttribute('aria-label') || '',
                 hs: el.getAttribute('aria-haspopup'), ex: el.getAttribute('aria-expanded'),
                 tx: (el.textContent || '').trim().slice(0, 18),
                 box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
                 before: i === 0 ? snap() : steps[i - 1].after });
    try { el.click(); } catch (e) {}
    setTimeout(tick, 380);
  };
  tick();
  return 'cands=' + cands.length;
})()
