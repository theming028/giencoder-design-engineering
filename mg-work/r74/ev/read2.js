(() => {
  const out = []; let prev = null;
  for (const o of window.__bp.s) {
    if (prev && ['b','left','right','slot','pane','pc','rc'].every(k => o[k] === prev[k])) { prev = o; continue; }
    out.push(o); prev = o;
  }
  return out;
})()
