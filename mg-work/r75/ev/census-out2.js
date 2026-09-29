(() => {
  const C = window.__CEN; if (!C) return 'none';
  const vis = o => o[1] !== 'none' && (o[2] !== 'hidden' || o[3] !== '0') && o[8].split(',')[2] !== '0x0';
  const out = [];
  C.steps.forEach(s => {
    const bm = new Map(); (s.before || []).forEach(o => bm.set(o[0], o));
    const opened = [];
    (s.after || []).forEach(o => {
      const b = bm.get(o[0]);
      const nv = vis(o), wv = b ? vis(b) : false;
      if (nv && !wv) opened.push({ k: o[0], disp: o[1], vis: o[2], op: o[3], tr: o[4], sx: o[5], an: o[6], inline: o[7], box: o[8], par: o[9] });
    });
    out.push({ i: s.i, trig: s.tag + '.' + s.cn + ' [' + s.aria + '] "' + s.tx + '" @' + s.box[0] + ',' + s.box[1] + ' hs=' + s.hs + ' ex=' + s.ex, opened: opened });
  });
  return JSON.stringify(out);
})()
