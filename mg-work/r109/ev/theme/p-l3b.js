(async () => {
  /* r109 第三拍 ① 读数（**提交前**）：此刻还没有 `.td-anchor`（锚点在提交时才落），
     所以要判的是**气泡**：气泡左边缘是否咬住「本次真实点击点」。
     点击点由编排脚本用 `window.__CLICK = {x, y}`（视口坐标）注入。
     全部换算到 `.td-view` 的**内容坐标**，消掉滚动。 */
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  var v = q('.td-brw [data-td-view]');
  var vb = B(v), sl = v.scrollLeft, st = v.scrollTop;
  const C = e => { var b = B(e); return { l: R(b.l - vb.l + sl), t: R(b.t - vb.t + st), w: b.w, h: b.h }; };

  var en = q('.td-elnote');
  out.viewScroll = { left: sl, top: st };
  out.viewBox = vb;
  out.elnoteHidden = en.hasAttribute('hidden');
  out.bubble = C(en);
  out.bubbleSize = { w: en.offsetWidth, h: en.offsetHeight };
  out.bubbleCssLeft = cs(en).left;
  var c = window.__CLICK;
  if (c) {
    out.clickViewport = c;
    out.clickContent = { x: R(c.x - vb.l + sl), y: R(c.y - vb.t + st) };
    out.dLeft = R(C(en).l - out.clickContent.x);          /* 期望 ≈ 0 */
  }
  /* 新增态（还没有这条批注的记录）⇒ 按钮文案应为「添加」 */
  out.okText = q('.td-elnote-ok').textContent.trim();
  out.cancelText = q('.td-elnote-cancel').textContent.trim();
  out.cancelDisplay = cs(q('.td-elnote-cancel')).display;
  out.hintDisplay = cs(q('.td-elnote-hint')).display;
  out.taValue = q('.td-elnote-input').value;
  out.taPlaceholder = q('.td-elnote-input').placeholder;
  out.pin = q('.td-elnote-pin').textContent.trim();
  out.pinDone = q('.td-elnote-pin').classList.contains('is-done');
  out.anchorCount = qa('.td-anchor').length;
  return JSON.stringify(out);
})()
