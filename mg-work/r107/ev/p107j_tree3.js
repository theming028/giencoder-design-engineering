/* 回归：先把右栏拉宽（保证树有可增空间），再拖「文件目录」分栏条 */
(function () {
  var slot = document.getElementById('av-browse-slot');
  var pane = slot.querySelector('.td-browse');
  var pSplit = document.getElementById('av-browse-split');
  var tSplit = document.querySelector('[data-td-split="tree"]');
  var tree = document.querySelector('.td-browse-tree');
  var o = (window.__j = window.__j || { steps: [] });
  function ev(target, x, y, type, btn, btns) {
    target.dispatchEvent(new PointerEvent(type, {
      bubbles: true, cancelable: true, clientX: x, clientY: y,
      pointerId: 3, pointerType: 'mouse', isPrimary: true, button: btn, buttons: btns
    }));
  }
  function log(tag) {
    o.steps.push({
      tag: tag,
      panelW: Math.round(slot.getBoundingClientRect().width),
      treeW: Math.round(tree.getBoundingClientRect().width)
    });
  }
  /* ---- 1) 用「预览栏分栏条」把右栏拉到 ~900 ---- */
  var r = pSplit.getBoundingClientRect();
  var cx = Math.round(r.x + r.width / 2), cy = Math.round(r.y + 300);
  log('P0');
  ev(pSplit, cx, cy, 'pointerdown', 0, 1);
  ev(document.body, cx - (900 - Math.round(slot.getBoundingClientRect().width)), cy, 'pointermove', -1, 1);
  ev(document.body, cx, cy, 'pointerup', 0, 0);
  log('P1 右栏拉宽后');

  /* ---- 2) 拖「文件目录」分栏条 +40 ---- */
  r = tSplit.getBoundingClientRect();
  cx = Math.round(r.x + r.width / 2); cy = Math.round(r.y + Math.min(r.height / 2, 200));
  log('T0');
  ev(tSplit, cx, cy, 'pointerdown', 0, 1);
  log('T1 down');
  ev(document.body, cx + 40, cy, 'pointermove', -1, 1);
  log('T2 move(+40)→body');
  ev(document.body, cx + 40, cy, 'pointerup', 0, 0);
  log('T3 up→body');
  return 'ok';
})()
