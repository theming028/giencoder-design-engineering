(() => {
  const trig = document.querySelector('.r81-ws-trigger');
  const pop = document.querySelector('.r81-ws-pop');
  const panel = document.querySelector('.r81-ws-panel');
  const list = document.querySelector('.r81-ws-list');
  trig.click();
  const pr = pop.getBoundingClientRect(), pa = panel.getBoundingClientRect();
  return JSON.stringify({
    vp: innerWidth + 'x' + innerHeight,
    pop: [Math.round(pr.x), Math.round(pr.y), Math.round(pr.width), Math.round(pr.height)].join(','),
    panelH: Math.round(pa.height),
    popInView: pr.right <= innerWidth && pr.bottom <= innerHeight && pr.left >= 0 && pr.top >= 0,
    listScrollable: list.scrollHeight > list.clientHeight,
    hOverflow: document.documentElement.scrollWidth > innerWidth
  });
})()
