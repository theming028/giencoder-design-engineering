(() => {
  const inp = document.querySelector('input.ws-search-input');
  const portal = inp ? inp.closest('body > div') : null;
  if (!portal) return JSON.stringify({ err: 'no portal' });
  const list = portal.querySelector('div[style*="top: 94px"]');
  const btns = [...portal.querySelectorAll('button')];
  const one = btns.find(b => b.textContent.indexOf('团队的空间') >= 0) || btns[1];
  const strip = el => {
    const c = el.cloneNode(true);
    c.querySelectorAll('svg').forEach(s => { s.innerHTML = '…'; });
    return c.outerHTML.replace(/\s+/g, ' ');
  };
  const CS = el => { const c = getComputedStyle(el); return { color: c.color, fs: c.fontSize, fw: c.fontWeight, lh: c.lineHeight, w: c.width, h: c.height, pos: c.position, left: c.left, top: c.top, right: c.right, bg: c.backgroundColor, bd: c.borderColor, bw: c.borderTopWidth, br: c.borderRadius, gap: c.gap, txt: c.textAlign, ws: c.whiteSpace, ov: c.overflow }; };
  const desc = [];
  if (one) {
    const walk = (el, d) => {
      desc.push({ d, tag: el.tagName, cls: (el.className || '').toString().slice(0, 30), own: [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('|'), s: CS(el) });
      [...el.children].forEach(c => walk(c, d + 1));
    };
    walk(one, 0);
  }
  return JSON.stringify({ listStyle: list ? CS(list) : null, itemHTML: one ? strip(one) : null, desc }, null, 1);
})()
