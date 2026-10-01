/* 回归：拖「文件目录」分栏条（down 在条上、move/up 落在 body） */
(function () {
  var slot = document.getElementById('av-browse-slot');
  var pane = slot.querySelector('.td-browse');
  var split = document.querySelector('[data-td-split="tree"]');
  var o = (window.__j = window.__j || { steps: [] });
  if (!split) { o.steps.push({ tag: 'no tree split' }); return 'no tree split'; }
  function ev(target, x, y, type, btn, btns) {
    target.dispatchEvent(new PointerEvent(type, {
      bubbles: true, cancelable: true, clientX: x, clientY: y,
      pointerId: 2, pointerType: 'mouse', isPrimary: true, button: btn, buttons: btns
    }));
  }
  function tw() {
    return (pane.style.getPropertyValue('--td-browse-tree-w') || getComputedStyle(pane).getPropertyValue('--td-browse-tree-w').trim() || '?');
  }
  var r = split.getBoundingClientRect();
  var cx = Math.round(r.x + r.width / 2), cy = Math.round(r.y + Math.min(r.height / 2, 300));
  var tree = document.querySelector('.td-browse-tree');
  o.steps.push({ tag: 'tree-T0', treeW: tw(), treeRectW: Math.round(tree.getBoundingClientRect().width), splitX: Math.round(r.x) });
  ev(split, cx, cy, 'pointerdown', 0, 1);
  o.steps.push({ tag: 'tree-T1 down', treeW: tw() });
  ev(document.body, cx + 40, cy, 'pointermove', -1, 1);
  o.steps.push({ tag: 'tree-T2 move(+40)→body', treeW: tw(), treeRectW: Math.round(tree.getBoundingClientRect().width) });
  ev(document.body, cx + 40, cy, 'pointerup', 0, 0);
  o.steps.push({ tag: 'tree-T3 up→body', treeW: tw(), treeRectW: Math.round(tree.getBoundingClientRect().width) });
  return 'ok';
})()
