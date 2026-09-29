(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const R = e => { const r = e.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join(','); };
  const st = document.querySelector('.kb-stat--coop');
  const out = { hasStat: !!st };
  if (st) st.click();
  await wait(500);
  const coop = document.querySelector('.kb-coop');
  const dlg = document.querySelector('.kb-coop-dialog');
  const lw = document.querySelector('.r82-coop-wing--l');
  const rw = document.querySelector('.r82-coop-wing--r');
  out.coopClass = coop ? coop.className : null;
  out.dlg = dlg ? R(dlg) : null;
  out.lw = lw ? R(lw) : null;
  out.rw = rw ? R(rw) : null;
  out.wingCount = document.querySelectorAll('.r82-coop-wing').length;
  if (lw && dlg) {
    const d = dlg.getBoundingClientRect(), l = lw.getBoundingClientRect(), rr = rw.getBoundingClientRect();
    out.align = { lwRight_vs_dlgLeft: Math.round(d.left - l.right), lwTop_vs_dlgTop: Math.round(l.top - d.top),
                  rwLeft_vs_dlgRight: Math.round(rr.left - d.right), rwTop_vs_dlgTop: Math.round(rr.top - d.top) };
    out.wingCS = { w: l.width.toFixed(2), h: l.height.toFixed(2), filter: getComputedStyle(lw).filter, z: getComputedStyle(lw).zIndex };
    out.pathFill = getComputedStyle(lw.querySelector('path')).fill;
    out.pathFillOpacity = getComputedStyle(lw.querySelector('path')).fillOpacity;
    out.pathD = lw.querySelector('path').getAttribute('d');
    out.parentIsCoop = lw.parentElement === coop;
  }
  return JSON.stringify(out);
})()
