(async () => {
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  var a = q('.td-anchor'), en = q('.td-elnote');
  out.tag = 'afterClick';
  out.anchorCount = qa('.td-anchor').length;
  out.elnoteHidden = en.hasAttribute('hidden');
  out.taValue = q('.td-elnote-input').value;
  out.pin = q('.td-elnote-pin').textContent.trim();
  out.pinDone = q('.td-elnote-pin').classList.contains('is-done');
  out.okText = q('.td-elnote-ok').textContent.trim();
  out.okDisabled = q('.td-elnote-ok').disabled;
  out.cancelDisplay = cs(q('.td-elnote-cancel')).display;
  out.hintDisplay = cs(q('.td-elnote-hint')).display;
  out.elnoteBox = B(en);
  out.anchorBox = B(a);
  /* ④ 的定位判据：气泡按**锚点**定位 ⇒ 气泡顶缘 = 锚点底缘 + 8 */
  out.bubbleDTop = R(B(en).t - (B(a).t + B(a).h));
  out.bubbleLeftDx = R(B(en).l - B(a).l);
  out.viewScrollTop = q('.td-brw [data-td-view]').scrollTop;
  var v = q('.td-brw [data-td-view]'), vb = B(v), eb = B(en);
  out.viewBox = vb;
  out.elnoteTransition = { prop: cs(en).transitionProperty, dur: cs(en).transitionDuration };
  out.clip = {
    bubbleBottomBelowView: R(eb.t + eb.h - (vb.t + vb.h)),
    bubbleRightBeyondView: R(eb.l + eb.w - (vb.l + vb.w)),
    visibleH: R(Math.min(eb.t + eb.h, vb.t + vb.h) - Math.max(eb.t, vb.t)),
    fullyHidden: eb.t >= vb.t + vb.h - 0.5
  };
  out.anchorCenter = { x: Math.round(B(a).l + B(a).w / 2), y: Math.round(B(a).t + B(a).h / 2) };
  return JSON.stringify(out);
})()
