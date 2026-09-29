(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const t = document.querySelector('.r81-ws-trigger');
  const out = { has: !!t };
  if (!t) return JSON.stringify(out);
  const r = t.getBoundingClientRect();
  out.idle = { rect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join(','), bg:getComputedStyle(t).backgroundColor, exp:t.getAttribute('aria-expanded') };
  t.click(); await wait(60);
  out.open = { bg:getComputedStyle(t).backgroundColor, exp:t.getAttribute('aria-expanded') };
  const pop = document.querySelector('.r81-ws-pop');
  const pr = pop.getBoundingClientRect();
  out.pop = [Math.round(pr.x),Math.round(pr.y),Math.round(pr.width),Math.round(pr.height)].join(',');
  out.popVsTrig = { dLeft: Math.round(pr.left - r.left), dTop: Math.round(pr.top - r.bottom) };
  out.items = pop.querySelectorAll('.r81-ws-item').length;
  out.sel = pop.querySelectorAll('.r81-ws-item[aria-selected="true"]').length;
  out.visibleTriggers = document.querySelectorAll('.r81-ws-trigger').length;
  document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
  await wait(40);
  out.closed = pop.hidden;
  out.bgAfterClose = getComputedStyle(t).backgroundColor;
  return JSON.stringify(out);
})()
