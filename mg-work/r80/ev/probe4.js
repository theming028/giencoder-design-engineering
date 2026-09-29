(() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
  const CS = el => { if (!el) return null; const c = getComputedStyle(el); return { bg: c.backgroundColor, color: c.color, fs: c.fontSize, fw: c.fontWeight, lh: c.lineHeight, br: c.borderRadius, bd: c.borderColor, bw: c.borderTopWidth, pad: c.padding, gap: c.gap, sh: c.boxShadow, op: c.opacity, pe: c.pointerEvents, disp: c.display }; };
  const host = document.querySelector('header > div[class~="justify-end"]');
  const trig = document.querySelector('.r80-ws-trigger');
  const pop = document.querySelector('.r80-ws-pop');
  const panel = document.querySelector('.r80-ws-panel');
  const items = [...document.querySelectorAll('.r80-ws-item')];
  const out = {
    url: location.pathname,
    ran: window.__r80ws === 1,
    hostFound: !!host,
    hostRect: R(host),
    hostKids: host ? host.children.length : null,
    trigRect: R(trig),
    trigCS: CS(trig),
    trigAria: trig ? trig.getAttribute('aria-expanded') : null,
    logo: trig ? { t: trig.querySelector('.r80-ws-logo').textContent, r: R(trig.querySelector('.r80-ws-logo')), cs: CS(trig.querySelector('.r80-ws-logo')) } : null,
    name: trig ? { t: trig.querySelector('.r80-ws-name').textContent, r: R(trig.querySelector('.r80-ws-name')), cs: CS(trig.querySelector('.r80-ws-name')) } : null,
    pill: trig ? { t: trig.querySelector('.r80-ws-pill').textContent, r: R(trig.querySelector('.r80-ws-pill')), cs: CS(trig.querySelector('.r80-ws-pill')) } : null,
    chev: trig ? R(trig.querySelector('.r80-ws-chev')) : null,
    popHidden: pop ? pop.hidden : null,
    popRect: R(pop),
    popInline: pop ? pop.getAttribute('style') : null,
    popCS: CS(pop),
    panelRect: R(panel),
    panelCS: CS(panel),
    headerName: document.querySelector('header > div[class~="justify-end"]') ? 'ok' : 'no',
    dividerTitle: panel ? (panel.querySelector('.r80-ws-divider span') || {}).textContent : null,
    searchPh: panel ? (panel.querySelector('input') || {}).placeholder : null,
    itemCount: items.length,
    items: items.map(b => ({
      i: b.getAttribute('data-i'),
      sel: b.getAttribute('aria-selected'),
      cls: b.className,
      r: R(b),
      cs: CS(b),
      name: (b.querySelector('.r80-ws-iname') || {}).textContent,
      desc: (b.querySelector('.r80-ws-idesc') || {}).textContent,
      role: (b.querySelector('.r80-ws-ipill') || {}).textContent || null,
      roleRect: R(b.querySelector('.r80-ws-ipill')),
      badge: R(b.querySelector('.r80-ws-ibadge')),
      badgeBg: b.querySelector('.r80-ws-ibadge') ? getComputedStyle(b.querySelector('.r80-ws-ibadge')).backgroundColor : null,
      iconRect: R(b.querySelector('.r80-ws-ibadge svg')),
      nameCS: CS(b.querySelector('.r80-ws-iname')),
      descCS: CS(b.querySelector('.r80-ws-idesc'))
    }))
  };
  return JSON.stringify(out, null, 1);
})()
