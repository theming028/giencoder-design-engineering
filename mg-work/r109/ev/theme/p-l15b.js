(function () {
  /* r109 第十五拍 · 批注链路深验：
     ① 输入文字 → 卡变 has-text、按钮变「添加」可用
     ② 点「添加」→ 锚点落盘、气泡收起、**仍在批注态**（l1 ④）
     ③ 锚点位置 = 点击点中心（l3 ①）
     ④ 点锚点 → 气泡以编辑态重开、按钮变「保存」（l3 ①/l2 ④）
     ⑤ Ctrl 按住 → 按钮变「发送」（l1 ④） */
  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  var out = {};
  var brw = q('.td-brw'), view = q('[data-td-view]', brw);
  /* 确保进批注态 */
  var ab = q('.td-url-annot', brw);
  if (ab && !brw.classList.contains('is-annotating')) ab.click();

  var el = q('[data-td-el]', brw);
  var vr = view.getBoundingClientRect();
  var r = el.getBoundingClientRect();
  var cx = Math.round(r.left + 30), cy = Math.round(r.top + 14);
  el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, clientX: cx, clientY: cy }));

  var note = q('.td-elnote', brw);
  var ta = q('.td-elnote-input', note);
  var ok = q('[data-td-elnote-ok]', note);
  /* ★ 等一次重排后再量 —— 摘 `[hidden]` + `noteGrow()` 在同一 tick 之外才量得到几何。 */
  return new Promise(function (resolve) {
  out.before = { hidden: note.hasAttribute('hidden'), okDisabled: ok.disabled, okText: ok.textContent };
  /* ★ 真量：气泡左边缘 vs 点击点的**内容坐标**（l3 ① 的唯一判据）。 */
  out.originVsClick = {
    clickContentX: cx - vr.left + view.scrollLeft,
    clickContentY: cy - vr.top + view.scrollTop,
    noteLeftPx: Math.round(parseFloat(note.style.left || '0')),
    noteTopPx: Math.round(parseFloat(note.style.top || '0')),
    noteH: note.offsetHeight
  };

  /* ① 输入 */
  ta.value = '这里的间距再大一点';
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  out.typed = {
    hasText: q('.td-elnote-card', note).classList.contains('has-text'),
    okDisabled: ok.disabled, okText: ok.textContent,
    taHeight: ta.style.height
  };

  /* ② 提交 */
  ok.click();
  out.afterCommit = {
    noteHidden: note.hasAttribute('hidden'),
    stillAnnotating: brw.classList.contains('is-annotating'),
    annotLabel: (q('.td-url-annot span', brw) || {}).textContent,
    anchors: qa('.td-anchor', brw).map(function (a) {
      return { text: a.textContent, left: a.style.left, top: a.style.top,
               role: a.getAttribute('role'), tabindex: a.getAttribute('tabindex'),
               title: a.title, cursor: getComputedStyle(a).cursor };
    })
  };
  /* ③ 锚点中心 vs 点击点（内容坐标） */
  var a0 = qa('.td-anchor', brw)[0];
  out.anchorVsClick = a0 ? {
    clickContentX: cx - vr.left + view.scrollLeft,
    clickContentY: cy - vr.top + view.scrollTop,
    anchorCenterX: Math.round(parseFloat(a0.style.left) + a0.offsetWidth / 2),
    anchorCenterY: Math.round(parseFloat(a0.style.top) + a0.offsetHeight / 2)
  } : null;

  /* ④ 点锚点 → 编辑态 */
  if (a0) a0.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  out.afterAnchorClick = {
    noteHidden: note.hasAttribute('hidden'),
    okText: ok.textContent,
    taValue: ta.value,
    noteLeft: note.style.left, noteTop: note.style.top
  };

  /* ⑤ Ctrl 联动 */
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Control', bubbles: true }));
  out.afterCtrl = { okText: ok.textContent, cardCtrl: q('.td-elnote-card', note).classList.contains('is-ctrl') };
  document.dispatchEvent(new KeyboardEvent('keyup', { key: 'Control', bubbles: true }));
  out.afterCtrlUp = { okText: ok.textContent };
  resolve(JSON.stringify(out, null, 1));
  });
})()
