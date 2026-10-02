(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  var om = q('[data-td-open-mod="browser"]');
  if (om) om.click();
  await W(800);
  var brw = q('.td-brw');
  out.brwVis = brw ? cs(brw).display : null;
  var view = q('.td-brw [data-td-view]');
  var bar = q('[data-td-annot-bar]');
  out.barCount = qa('[data-td-annot-bar]').length;
  out.pageBlankCount = qa('.td-page-blank').length;
  out.barHiddenBefore = bar.hasAttribute('hidden');
  var ua = q('.td-url-annot');
  out.uaLabelBefore = ua.textContent.trim();
  out.uaBgBefore = cs(ua).backgroundColor;
  ua.click();
  await W(400);
  out.isAnnotating = brw.classList.contains('is-annotating');
  out.barHiddenAfter = bar.hasAttribute('hidden');
  var vb = B(view), bb = B(bar);
  out.bar = { box: bb, dTop: R(bb.t - vb.t), position: cs(bar).position, top: cs(bar).top,
              bottom: cs(bar).bottom, bg: cs(bar).backgroundColor };
  out.barIsFirstChild = view.firstElementChild === bar;
  out.uaLabelAfter = ua.textContent.trim();
  out.uaBgAfter = cs(ua).backgroundColor;
  out.uaColorAfter = cs(ua).color;
  out.uaBorderAfter = cs(ua).borderTopColor;
  var els = qa('.td-page [data-td-el]');
  out.els = els.map(e => e.className);
  var target = els.filter(e => e.className.indexOf('td-page-card') >= 0)[0] || els[0];
  out.target = target ? target.className : null;
  target.click();
  await W(400);
  var en = q('.td-elnote');
  out.noteHidden = en.hasAttribute('hidden');
  out.noteBox = B(en);
  out.noteDomOrder = Array.prototype.slice.call(en.children).map(c => c.className);
  var pin = q('.td-elnote-pin'), card = q('.td-elnote-card'), ta = q('.td-elnote-input');
  out.pin = { box: B(pin), br: cs(pin).borderRadius, bw: cs(pin).borderTopWidth,
              bg: cs(pin).backgroundColor, bc: cs(pin).borderTopColor, mt: cs(pin).marginTop };
  out.card = { box: B(card), pad: cs(card).paddingTop, br: cs(card).borderRadius,
               bd: cs(card).borderTopWidth, dir: cs(card).flexDirection, h: cs(card).height,
               maxh: cs(card).maxHeight, bg: cs(card).backgroundColor,
               hasText: card.classList.contains('has-text'), shadow: cs(card).boxShadow };
  out.cardDx = R(B(card).l - B(en).l);
  out.ta = { box: B(ta), lh: cs(ta).lineHeight, fs: cs(ta).fontSize, ph: ta.placeholder,
             color: cs(ta).color };
  out.taDx = R(B(ta).l - B(card).l);
  var ok = q('.td-elnote-ok'), cancel = q('.td-elnote-cancel'), hint = q('.td-elnote-hint');
  out.ok = { box: B(ok), txt: ok.textContent.trim(), disabled: ok.disabled,
             bg: cs(ok).backgroundColor, color: cs(ok).color, fs: cs(ok).fontSize,
             h: cs(ok).height, pad: cs(ok).paddingLeft, br: cs(ok).borderRadius,
             sh: cs(ok).boxShadow };
  out.okRightInset = R(B(card).l + B(card).w - (B(ok).l + B(ok).w));
  out.okDx = R(B(ok).l - B(card).l);
  out.cancelDisplay = cs(cancel).display;
  out.hintDisplay = cs(hint).display;
  out.anchorCount = qa('.td-anchor').length;
  // 供截图用：把目标滚进视野，气泡跟着（气泡绝对定位在 .td-view 里、会随滚动走）
  return JSON.stringify(out);
})()
