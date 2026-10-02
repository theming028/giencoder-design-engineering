(async () => {
  /* r109 第三拍 ① 编辑态读数：真鼠标点开**已存在**的锚点后，
     按钮文案必须是「保存」（不是「添加」），且气泡仍钉在锚点上。 */
  const q = (s, r) => (r || document).querySelector(s);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  var a = q('.td-anchor'), en = q('.td-elnote');
  out.elnoteHidden = en.hasAttribute('hidden');
  out.okText = q('.td-elnote-ok').textContent.trim();
  out.cancelDisplay = getComputedStyle(q('.td-elnote-cancel')).display;
  out.taValue = q('.td-elnote-input').value;
  out.pin = q('.td-elnote-pin').textContent.trim();
  out.pinDone = q('.td-elnote-pin').classList.contains('is-done');
  out.okDisabled = q('.td-elnote-ok').disabled;
  out.bubbleDTop = R(B(en).t - (B(a).t + B(a).h));
  out.bubbleLeftDx = R(B(en).l - B(a).l);
  out.anchorCount = document.querySelectorAll('.td-anchor').length;
  return JSON.stringify(out);
})()
