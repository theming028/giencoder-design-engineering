/* 阶段快照：累积到 window.__j（同一次页面会话内多次调用） */
(function () {
  var slot = document.getElementById('av-browse-slot');
  var split = document.getElementById('av-browse-split');
  var row = slot ? slot.parentElement : null;
  var btn = document.querySelector('[data-td-max]');
  var o = (window.__j = window.__j || { steps: [] });
  var mainEl = document.querySelector('main');

  function rectOf(el) {
    if (!el) return 'none';
    var r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.width)];
  }
  function cls(el) { return el ? (el.getAttribute('class') || '') : '-'; }

  var s = {
    i: o.steps.length,
    inlineW: slot ? (slot.style.getPropertyValue('--av-browse-w') || '(none)') : 'no-slot',
    maxw: slot ? (slot.getAttribute('data-td-maxw') || '(none)') : '-',
    slotRect: rectOf(slot),
    rowCls: cls(row),
    rowRect: rectOf(row),
    mainRect: rectOf(mainEl),
    splitRect: rectOf(split),
    splitDisp: split ? getComputedStyle(split).display : '-',
    splitPE: split ? getComputedStyle(split).pointerEvents : '-',
    btnPressed: btn ? btn.getAttribute('aria-pressed') : '-',
    btnTitle: btn ? btn.getAttribute('title') : '-',
    btnAria: btn ? btn.getAttribute('aria-label') : '-',
    btnNs: btn ? btn.querySelectorAll('svg path').length : -1,
    btnD: btn ? Array.prototype.map.call(btn.querySelectorAll('svg path'), function (p) { return p.getAttribute('d'); }).join(' | ') : '-'
  };
  if (split) {
    var r = split.getBoundingClientRect();
    var hit = document.elementFromPoint(r.x + r.width / 2, r.y + Math.min(r.height / 2, 300));
    s.hitAtSplit = hit ? (hit.tagName + '.' + (hit.getAttribute('class') || '')) : 'null';
  }
  s.avW = slot ? getComputedStyle(slot).getPropertyValue('--av-browse-w').trim() : '-';
  s.slotBasis = slot ? getComputedStyle(slot).flexBasis : '-';
  o.steps.push(s);
  return 'snap#' + s.i;
})()
