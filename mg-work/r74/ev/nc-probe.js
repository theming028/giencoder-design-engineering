(() => {
  const out = [];
  document.querySelectorAll('button, a').forEach(el => {
    const t = (el.textContent || '').trim();
    if (t.indexOf('新会话') < 0) return;
    if (el.closest('[class*="td-right"]') || el.getAttribute('aria-label') === '新会话') {
      if (el.getAttribute('aria-label') === '新会话') return; // 只取文字按钮
    }
    const r = el.getBoundingClientRect();
    if (r.width < 40) return;
    const cs = getComputedStyle(el);
    out.push({
      cls: (typeof el.className === 'string' ? el.className : '').slice(0, 100),
      rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
      bg: cs.backgroundColor, radius: cs.borderRadius, border: cs.borderWidth + ' ' + cs.borderColor,
      shadow: cs.boxShadow.slice(0, 90),
      font: cs.fontSize + '/' + cs.fontWeight, color: cs.color,
      disp: cs.display, justify: cs.justifyContent, pad: cs.padding,
      children: [...el.children].map(c => {
        const cr = c.getBoundingClientRect();
        const ccs = getComputedStyle(c);
        return { tag: c.tagName, cls: (typeof c.className === 'string' ? c.className : '').slice(0, 40),
                 txt: (c.textContent || '').trim().slice(0, 12),
                 x: Math.round(cr.x - r.x), w: Math.round(cr.width), h: Math.round(cr.height),
                 ml: ccs.marginLeft, mr: ccs.marginRight, pos: ccs.position };
      })
    });
  });
  return { file: location.pathname.split('/').pop(), n: out.length, items: out };
})()
