(() => {
  const h = document.querySelector('header');
  const right = h ? h.querySelector(':scope > div.flex.w-60.items-center.justify-end') : null;
  const left = h ? h.querySelector(':scope > div.flex.w-60.items-center.gap-4') : null;
  const inner = left ? left.querySelector(':scope > div:nth-child(2)') : null;
  const r = el => el ? (({x,y,width,height,bottom,left,right,top}) => ({x,y,width,height,bottom,left,right,top}))(el.getBoundingClientRect()) : null;
  const cs = el => el ? getComputedStyle(el) : null;
  const lcs = cs(inner);
  return JSON.stringify({
    url: location.pathname,
    headerHTML: h ? h.outerHTML.replace(/\s+/g,' ').slice(0, 2500) : null,
    rightCluster: r(right),
    rightChildren: right ? right.children.length : null,
    leftCluster: r(left),
    leftInner: r(inner),
    leftInnerOpacity: lcs ? lcs.opacity : null,
    leftInnerPE: lcs ? lcs.pointerEvents : null,
    headerClass: h ? h.className : null,
    wsTrigger: !!document.querySelector('.ws-trigger-hover'),
    wsTriggerRect: r(document.querySelector('.ws-trigger-hover')),
    tabs: [...document.querySelectorAll('header [role=tab]')].map(t => ({t: t.textContent, sel: t.getAttribute('aria-selected'), r: r(t)}))
  });
})()
