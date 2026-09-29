(() => {
  const all = [...document.querySelectorAll('button')].filter(b => (b.textContent || '').indexOf('新会话') >= 0 && b.getBoundingClientRect().width > 40);
  if (!all.length) return 'NONE';
  const b = all[0];
  const br = b.getBoundingClientRect();
  const cs = getComputedStyle(b);
  const kids = [...b.childNodes].map(n => {
    if (n.nodeType === 3) return { t: 'TEXT', v: n.nodeValue.trim(), w: (() => { const rg = document.createRange(); rg.selectNodeContents(n); return Math.round(rg.getBoundingClientRect().width); })() };
    const r = n.getBoundingClientRect(), c = getComputedStyle(n);
    return { t: n.tagName, cls: String(n.className).slice(0, 30), x: Math.round(r.x - br.x), w: Math.round(r.width), h: Math.round(r.height),
             ml: c.marginLeft, mr: c.marginRight, pos: c.position, right: c.right, font: c.fontSize + '/' + c.fontWeight, color: c.color,
             kids: [...n.children].map(k => ({ t: k.tagName, txt: (k.textContent || '').trim().slice(0, 4), w: Math.round(k.getBoundingClientRect().width), h: Math.round(k.getBoundingClientRect().height), color: getComputedStyle(k).color, font: getComputedStyle(k).fontSize + '/' + getComputedStyle(k).fontWeight })) };
  });
  return { file: location.pathname.split('/').pop(), bw: Math.round(br.width), cls: String(b.className),
           gap: cs.gap, justify: cs.justifyContent, pad: cs.padding, font: cs.fontSize + '/' + cs.fontWeight, color: cs.color, kids };
})()
