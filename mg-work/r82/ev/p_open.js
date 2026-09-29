(() => {
  const out = {};
  const st = document.querySelector('.kb-stat--coop');
  out.hasStat = !!st;
  if (st) { st.click(); }
  const coop = document.querySelector('.kb-coop');
  out.hidden = coop ? coop.hidden : null;
  const dlg = document.querySelector('.kb-coop-dialog');
  if (dlg) { const r = dlg.getBoundingClientRect(); out.dlg = [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join(','); }
  out.vp = innerWidth + 'x' + innerHeight;
  return JSON.stringify(out);
})()
