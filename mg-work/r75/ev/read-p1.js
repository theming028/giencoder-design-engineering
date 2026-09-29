(() => {
  const L = window.__P1; if (!L) return 'none';
  const ord = []; const map = new Map();
  L.forEach(([tag, t, arr]) => arr.forEach(s => {
    const f = s.split('§');
    const k = f[0];
    if (!map.has(k)) { map.set(k, { k: k, frames: [] }); ord.push(k); }
    map.get(k).frames.push({ tag: tag, t: t, disp: f[1], vis: f[2], op: f[3], tr: f[4], sx: f[5], an: f[6], inline: f[7], box: f[8] });
  }));
  return JSON.stringify(ord.map(k => map.get(k)));
})()
