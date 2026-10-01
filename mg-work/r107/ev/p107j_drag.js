/* 合成拖拽：第一轮 move 派发到分栏条本身；第二轮 move/up 派发到 body（模拟指针离开元素）
   —— 直接检验「pointermove/pointerup 是否已挂到 window」 */
(function () {
  var slot = document.getElementById('av-browse-slot');
  var split = document.getElementById('av-browse-split');
  var o = (window.__j = window.__j || { steps: [] });
  function mark(tag, extra) {
    var s = {
      i: o.steps.length, tag: tag,
      inlineW: slot.style.getPropertyValue('--av-browse-w') || '(none)',
      maxw: slot.getAttribute('data-td-maxw') || '(none)',
      slotW: Math.round(slot.getBoundingClientRect().width),
      rowCls: (slot.parentElement.getAttribute('class') || '').indexOf('is-col-dragging') >= 0 ? 'dragging' : '-',
      splitCls: split.getAttribute('class') || ''
    };
    if (extra) for (var k in extra) s[k] = extra[k];
    o.steps.push(s);
  }
  function ev(target, x, y, type, btn, btns) {
    target.dispatchEvent(new PointerEvent(type, {
      bubbles: true, cancelable: true, clientX: x, clientY: y,
      pointerId: 1, pointerType: 'mouse', isPrimary: true,
      button: btn, buttons: btns
    }));
  }
  var r = split.getBoundingClientRect();
  var cx = Math.round(r.x + r.width / 2), cy = Math.round(r.y + Math.min(r.height / 2, 300));

  /* ---- 第一轮：全程走分栏条（判「起点是否等于实际宽」） ---- */
  mark('R1-T0 拖前', { cx: cx, cy: cy });
  ev(split, cx, cy, 'pointerdown', 0, 1);
  mark('R1-T1 down');
  ev(split, cx - 120, cy, 'pointermove', -1, 1);
  mark('R1-T2 move(-120)');
  ev(split, cx - 120, cy, 'pointerup', 0, 0);
  mark('R1-T3 up');

  /* ---- 第二轮：down 在分栏条，move/up 落在 body（判「是否挂到 window」） ---- */
  r = split.getBoundingClientRect();
  cx = Math.round(r.x + r.width / 2); cy = Math.round(r.y + Math.min(r.height / 2, 300));
  ev(split, cx, cy, 'pointerdown', 0, 1);
  mark('R2-T1 down（指针在分栏条上）');
  ev(document.body, cx + 80, cy, 'pointermove', -1, 1);
  mark('R2-T2 move(+80) 派发到 body');
  ev(document.body, cx + 80, cy, 'pointerup', 0, 0);
  mark('R2-T3 up 派发到 body');

  return 'dragged';
})()
