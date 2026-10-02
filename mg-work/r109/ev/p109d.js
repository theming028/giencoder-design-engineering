(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  var en = q('.td-elnote');
  var ok = q('.td-elnote-ok');
  out.okTxtAtCommit = ok.textContent.trim();
  ok.click();
  await W(400);
  out.noteHidden = en.hasAttribute('hidden');
  out.isAnnotating = q('.td-brw').classList.contains('is-annotating');
  out.barVisible = !q('[data-td-annot-bar]').hasAttribute('hidden');
  var anchors = qa('.td-anchor');
  out.anchorCount = anchors.length;
  if (anchors.length) {
    var a = anchors[0], t = q('.td-page-card');
    out.anchor = { box: B(a), txt: a.textContent, bg: cs(a).backgroundColor,
                   color: cs(a).color, fs: cs(a).fontSize, fw: cs(a).fontWeight,
                   lh: cs(a).lineHeight, br: cs(a).borderRadius,
                   bw: cs(a).borderTopWidth, bc: cs(a).borderTopColor };
    out.anchorVsTarget = { dRight: R(B(a).l + B(a).w - B(t).l - B(t).w),
                           dTop: R(B(a).t - B(t).t) };
    out.anchorInView = !!a.closest('[data-td-view]');
  }
  // 重开一次气泡：pin 应变成稿3 的实心态、输入框回填
  q('.td-page-card').click();
  await W(300);
  var pin = q('.td-elnote-pin');
  out.reopen = { isDone: pin.classList.contains('is-done'), num: pin.textContent,
                 bg: cs(pin).backgroundColor, color: cs(pin).color,
                 dotContent: getComputedStyle(pin, '::after').content,
                 taVal: q('.td-elnote-input').value,
                 hasText: q('.td-elnote-card').classList.contains('has-text'),
                 okDisabled: q('.td-elnote-ok').disabled,
                 cardH: q('.td-elnote-card').getBoundingClientRect().height,
                 taH: q('.td-elnote-input').getBoundingClientRect().height,
                 taInlineH: q('.td-elnote-input').style.height };
  return JSON.stringify(out);
})()
