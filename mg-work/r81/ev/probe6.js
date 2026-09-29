(() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const hdr = document.querySelector('header');
  const left = hdr ? hdr.children[0] : null;
  const tabs = hdr ? hdr.querySelector('[role="tablist"]') : null;
  const right = hdr ? hdr.children[hdr.children.length - 1] : null;
  const kids = left ? [...left.children].map((el, i) => ({
    i,
    tag: el.tagName,
    cls: (el.className || '').slice(0, 90),
    inline: (el.getAttribute('style') || '').slice(0, 90),
    r: R(el)
  })) : [];
  const lights = left && left.children[0];
  const lightKids = lights ? [...lights.children].map(el => ({ aria: el.getAttribute('aria-label'), r: R(el) })) : [];
  const reactHost = left && left.children[1];
  const reactTrig = document.querySelector('.ws-trigger-hover');
  const r80 = document.querySelector('.r80-ws-trigger');
  return JSON.stringify({
    file: location.pathname.split('/').pop(),
    hash: location.hash,
    headerCls: hdr ? hdr.className : null,
    headerRect: R(hdr),
    leftCls: left ? left.className : null,
    leftRect: R(left),
    leftGap: left ? getComputedStyle(left).gap : null,
    leftPad: left ? getComputedStyle(left).padding : null,
    kids,
    lightsRect: R(lights),
    lightsGap: lights ? getComputedStyle(lights).gap : null,
    lightsRect2: lights ? R(lights) : null,
    lightKids,
    reactHostCls: reactHost ? (reactHost.className || '') : null,
    reactHostInline: reactHost ? reactHost.getAttribute('style') : null,
    reactHostRect: R(reactHost),
    reactHostCS: reactHost ? { op: getComputedStyle(reactHost).opacity, pe: getComputedStyle(reactHost).pointerEvents } : null,
    reactTrigCls: reactTrig ? reactTrig.className : null,
    reactTrigRect: R(reactTrig),
    reactTrigCS: reactTrig ? { bg: getComputedStyle(reactTrig).backgroundColor, pad: getComputedStyle(reactTrig).padding, h: getComputedStyle(reactTrig).height, br: getComputedStyle(reactTrig).borderRadius } : null,
    r80Cls: r80 ? r80.className : null,
    r80Rect: R(r80),
    tabsRect: R(tabs),
    rightCls: right ? right.className : null,
    rightRect: R(right),
    rightKids: right ? right.children.length : null,
    vw: innerWidth
  }, null, 1);
})()
