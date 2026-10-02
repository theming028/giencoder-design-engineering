(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const cs = e => getComputedStyle(e);
  const out = {};
  var card = q('.td-elnote-card'), ok = q('.td-elnote-ok'), em = q('.td-elnote-hint em');
  var hint = q('.td-elnote-hint');
  out.before = { okTxt: ok.textContent.trim(), emColor: cs(em).color,
                 hintColor: cs(hint).color, cardCtrl: card.classList.contains('is-ctrl') };
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Control', bubbles: true }));
  await W(250);
  out.after = { okTxt: ok.textContent.trim(), emColor: cs(em).color,
                hintColor: cs(hint).color, cardCtrl: card.classList.contains('is-ctrl'),
                okBox: (() => { const r = ok.getBoundingClientRect(); return [r.left, r.width]; })() };
  out.ctrlSeq = 0;
  try { out.ctrlSeq = (window.__ctrlHits || 0); } catch (e) { out.ctrlSeq = -1; }
  return JSON.stringify(out);
})()
