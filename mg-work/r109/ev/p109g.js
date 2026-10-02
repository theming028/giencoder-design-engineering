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
  await W(1000);
  var brw = q('.td-brw');
  out.brwVis = cs(brw).display;
  if (!brw.classList.contains('is-annotating')) { q('.td-url-annot').click(); await W(400); }
  out.isAnnotating = brw.classList.contains('is-annotating');

  var els = qa('.td-page [data-td-el]');
  out.elClasses = els.map(function (e) { return e.className; });
  var target = els.filter(function (e) { return e.className.indexOf('td-page-card') >= 0; })[0] || els[0];
  out.target = target.className;
  target.scrollIntoView({ block: 'center' });
  await W(400);
  target.click();
  await W(400);

  var ta = q('.td-elnote-input');
  out.editState = {
    elnoteHidden: q('.td-elnote').hasAttribute('hidden'),
    taValue: ta.value, taPlaceholder: ta.placeholder,
    pin: q('.td-elnote-pin').textContent.trim(),
    pinDone: q('.td-elnote-pin').classList.contains('is-done'),
    okDisabled: q('.td-elnote-ok').disabled,
    okText: q('.td-elnote-ok').textContent.trim()
  };
  var TEXT = '锚点可拖动验证：这条批注的锚点应当能点开详情、也能拖到任意位置。';
  ta.value = TEXT;
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  await W(300);
  q('.td-elnote-ok').click();
  await W(500);

  var a = q('.td-anchor');
  out.noteText = TEXT;
  out.afterCommit = {
    anchorCount: qa('.td-anchor').length,
    elnoteHidden: q('.td-elnote').hasAttribute('hidden'),
    box: B(a), left: a.style.left, top: a.style.top,
    role: a.getAttribute('role'), tabindex: a.getAttribute('tabindex'),
    aria: a.getAttribute('aria-label'), title: a.title, txt: a.textContent,
    cursor: cs(a).cursor, touchAction: cs(a).touchAction, userSelect: cs(a).userSelect,
    borderRadius: cs(a).borderRadius, bg: cs(a).backgroundColor, zIndex: cs(a).zIndex,
    transProp: cs(a).transitionProperty, transDur: cs(a).transitionDuration,
    width: cs(a).width, height: cs(a).height
  };
  var v = q('.td-brw [data-td-view]');
  out.view = {
    box: B(v), scrollTop: v.scrollTop, scrollLeft: v.scrollLeft,
    clientW: v.clientWidth, clientH: v.clientHeight,
    maxL: v.scrollLeft + v.clientWidth - a.offsetWidth,
    maxT: v.scrollTop + v.clientHeight - a.offsetHeight
  };
  out.anchorCenter = { x: Math.round(B(a).l + B(a).w / 2), y: Math.round(B(a).t + B(a).h / 2) };
  return JSON.stringify(out);
})()
