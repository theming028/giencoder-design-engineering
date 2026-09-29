(async () => {
  const w = ms => new Promise(r => setTimeout(r, ms));
  const host = document.querySelector('.kb-radio');
  const thumb = host.querySelector('.kb-radio-thumb');
  const other = host.querySelector('.kb-radio-btn:not(.is-on)[data-goto]');
  const rec = [];
  const R = e => { const r = e.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.width)].join('/'); };
  rec.push('idle thumb=' + R(thumb));
  other.click();
  for (const d of [60, 110, 160]) { await w(d === 60 ? 60 : 50); rec.push('t+' + d + ' thumb=' + R(thumb)); }
  return rec.join(' | ');
})()
