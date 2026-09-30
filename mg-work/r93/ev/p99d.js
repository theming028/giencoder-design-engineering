/* r99 取证：打开 r93-drow 的右键菜单（保持展开），供截图 */
(function () {
  var rows = document.querySelectorAll('.r93-drow');
  if (!rows.length) return 'NO_ROW';
  var row = rows[Math.min(2, rows.length - 1)];
  var r = row.getBoundingClientRect();
  row.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: Math.round(r.left + 120), clientY: Math.round(r.top + 10) }));
  var box = document.querySelector('.r93-ctx');
  return box ? 'OPEN ' + JSON.stringify(box.getBoundingClientRect()) : 'NOT_OPEN';
})();
