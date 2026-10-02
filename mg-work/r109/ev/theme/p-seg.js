(function () {
  /* r109 第三拍 ③-b：设置页「外观」分段控件的**几何 + 文案 + 选中态**。
     只读，不点。取每枚按钮的**中心点**（真鼠标点击用）—— 判据必须来自真鼠标，
     合成 click 不经过 pointerdown（见 P3.57⑧）。 */
  var seg = document.querySelector('.r85-seg');
  if (!seg) return JSON.stringify({ ok: false, why: 'no .r85-seg' });
  var out = [], i, b, r;
  for (i = 0; i < seg.children.length; i++) {
    b = seg.children[i];
    r = b.getBoundingClientRect();
    out.push({
      i: i,
      label: (b.textContent || '').trim(),
      cls: typeof b.className === 'string' ? b.className : '',
      pressed: b.getAttribute('aria-pressed'),
      cx: Math.round(r.left + r.width / 2),
      cy: Math.round(r.top + r.height / 2),
      box: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]
    });
  }
  return JSON.stringify({ ok: true, n: seg.children.length, items: out });
})()
