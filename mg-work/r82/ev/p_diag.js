(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const st = document.querySelector('.kb-stat--coop');
  if (st) st.click();
  await wait(600);
  const coop = document.querySelector('.kb-coop');
  const dlg = document.querySelector('.kb-coop-dialog');
  const host = document.querySelector('main');
  const info = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    return { cls:(e.className||'').toString().slice(0,40), rect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join(','),
      off:[e.offsetLeft,e.offsetTop,e.offsetWidth,e.offsetHeight].join(','), pos:cs.position, transform:cs.transform,
      parent:(e.parentElement&&e.parentElement.tagName+'.'+(e.parentElement.className||'').toString().slice(0,22)) }; };
  return JSON.stringify({ coop:info(coop), dlg:info(dlg), main: host?info(host):null,
    coopOffsetParent: coop.offsetParent ? coop.offsetParent.tagName+'.'+(coop.offsetParent.className||'').toString().slice(0,24) : null,
    dlgOffsetParent: dlg.offsetParent ? dlg.offsetParent.tagName+'.'+(dlg.offsetParent.className||'').toString().slice(0,24) : null });
})()
