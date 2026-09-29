(() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
  const CS = (el, p) => el ? getComputedStyle(el, p) : null;
  const box = el => { const c = CS(el); if (!c) return null; return { bg: c.backgroundColor, bd: c.borderColor, bw: c.borderTopWidth, br: c.borderRadius, sh: c.boxShadow, color: c.color, fs: c.fontSize, fw: c.fontWeight, lh: c.lineHeight, pad: c.padding, gap: c.gap, disp: c.display, op: c.opacity }; };
  const inp = document.querySelector('input[placeholder]');
  const portal = inp ? inp.closest('body > div') : null;
  const items = [...document.querySelectorAll('.ws-item-hover')].map(e => ({ t: e.textContent, r: R(e), b: box(e) }));
  const kids = portal ? [...portal.querySelectorAll('*')].slice(0, 40).map(e => ({ tag: e.tagName, cls: (e.className || '').toString().slice(0, 40), t: (e.childElementCount === 0 ? e.textContent : '').slice(0, 20), r: R(e), b: box(e) })) : null;
  return JSON.stringify({
    url: location.pathname,
    portalRect: R(portal),
    portalStyle: portal ? { inline: portal.getAttribute('style'), cs: box(portal) } : null,
    input: inp ? { ph: inp.placeholder, r: R(inp), b: box(inp), cs: CS(inp) ? { color: CS(inp).color, fs: CS(inp).fontSize } : null } : null,
    itemCount: items.length,
    items,
    portalHTML: portal ? portal.outerHTML.replace(/\s+/g, ' ').slice(0, 7000) : null
  }, null, 1);
})()
