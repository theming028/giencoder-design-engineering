(async () => {
  const W = (ms) => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = (e) => getComputedStyle(e);
  const out = {};
  out.href = location.href;
  out.openModBtns = qa('[data-td-open-mod]').map(b => b.getAttribute('data-td-open-mod'));
  out.tabs = qa('[data-td-tab]').map(b => b.getAttribute('data-td-mod'));
  var panes = qa('.av-browse-pane, [id^=av-browse-pane]');
  out.panes = panes.map(p => [p.id, p.hasAttribute('hidden'), cs(p).display]);
  out.brw = !!q('.td-brw');
  var b = q('.td-brw');
  if (b) {
    out.brwHiddenSelf = b.hasAttribute('hidden');
    out.brwBox = (() => { const r = b.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })();
    out.brwDisplay = cs(b).display;
  }
  out.rail = qa('.td-browse-ico, [data-td-rail], .r93-baract').slice(0, 8).map(x => [x.className, (x.textContent || '').trim().slice(0, 10)]);
  return JSON.stringify(out);
})()
