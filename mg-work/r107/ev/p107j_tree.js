/* 回归：① 列出标签；② 打开「文件」模块；③ 拖「文件目录」分栏条（down 在条上、move/up 落在 body） */
(function () {
  var slot = document.getElementById('av-browse-slot');
  var o = (window.__j = window.__j || { steps: [] });
  function mark(tag, extra) {
    var s = { i: o.steps.length, tag: tag };
    if (extra) for (var k in extra) s[k] = extra[k];
    o.steps.push(s);
  }
  mark('tabs', {
    mods: [].slice.call(document.querySelectorAll('[data-td-tab]')).map(function (t) { return t.getAttribute('data-td-mod'); }),
    panes: [].slice.call(document.querySelectorAll('[data-td-pane]')).map(function (t) { return t.getAttribute('data-td-pane'); })
  });
  var fileTab = document.querySelector('[data-td-tab][data-td-mod="files"]')
    || document.querySelector('[data-td-tab][data-td-mod="file"]');
  if (!fileTab) { mark('no files tab'); return 'no files tab'; }
  fileTab.click();
  var split = document.querySelector('[data-td-split="tree"]');
  if (!split) { mark('no tree split'); return 'no tree split'; }
  var pane = slot.querySelector('.td-browse');
  function ev(target, x, y, type, btn, btns) {
    target.dispatchEvent(new PointerEvent(type, {
      bubbles: true, cancelable: true, clientX: x, clientY: y,
      pointerId: 2, pointerType: 'mouse', isPrimary: true, button: btn, buttons: btns
    }));
  }
  function treeW() {
    return getComputedStyle(pane).getPropertyValue('--td-browse-tree-w').trim()
      || Math.round(document.querySelector('.td-browse-tree').getBoundingClientRect().width) + 'px';
  }
  var r = split.getBoundingClientRect();
  var cx = Math.round(r.x + r.width / 2), cy = Math.round(r.y + Math.min(r.height / 2, 300));
  mark('tree-T0', { treeW: treeW(), splitRect: [Math.round(r.x), Math.round(r.width)] });
  ev(split, cx, cy, 'pointerdown', 0, 1);
  mark('tree-T1 down', { treeW: treeW() });
  ev(document.body, cx + 40, cy, 'pointermove', -1, 1);
  mark('tree-T2 move(+40) 到 body', { treeW: treeW() });
  ev(document.body, cx + 40, cy, 'pointerup', 0, 0);
  mark('tree-T3 up 到 body', { treeW: treeW() });
  return 'tree dragged';
})()
