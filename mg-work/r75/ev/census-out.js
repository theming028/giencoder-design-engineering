(() => {
  const C = window.__CEN; if (!C) return 'none';
  const visible = o => o.disp !== 'none' && (o.vis !== 'hidden' || o.op !== '0') && !(o.box[2] === 0 && o.box[3] === 0);
  const k = o => o.cn + '|' + o.role + '|' + o.aria + '|' + o.par;
  const out = [];
  C.steps.forEach(s => {
    const bm = new Map(); s.before.forEach(o => bm.set(k(o), o));
    const opened = [];
    s.after.forEach(o => {
      const b = bm.get(k(o));
      const nowVis = visible(o), wasVis = b ? visible(b) : false;
      if (nowVis && !wasVis) opened.push({
        cn: o.cn, role: o.role, aria: o.aria, disp: o.disp, vis: o.vis, op: o.op,
        tr: o.tr, sx: o.sx, inline: o.inline, trs: o.trs, an: o.an,
        box: o.box, par: o.par, newInDom: !b });
    });
    out.push({ i: s.i, trig: s.tag + '.' + s.cn + ' [' + s.aria + '] "' + s.tx + '" @' + s.box[0] + ',' + s.box[1],
               box: s.box, opened: opened });
  });
  return JSON.stringify(out);
})()
