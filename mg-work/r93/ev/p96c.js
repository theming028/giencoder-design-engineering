(function () {
  var bubi = document.querySelector('.r93-bubi');
  var out = { before: { rect: null, maxH: getComputedStyle(bubi).maxHeight, ovY: getComputedStyle(bubi).overflowY } };
  var b = bubi.getBoundingClientRect();
  out.before.rect = [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)];
  out.before.sh = bubi.scrollHeight; out.before.ch = bubi.clientHeight;

  // 临时把正文复制到很长（只放文本节点，不改 DOM 结构）
  var span = bubi.querySelector('.r93-ubt');
  var bak = span.textContent;
  span.textContent = new Array(26).join(bak + ' ');   // ×25
  out.afterGrow = { sh: bubi.scrollHeight, ch: bubi.clientHeight, scrollable: bubi.scrollHeight > bubi.clientHeight };
  var b2 = bubi.getBoundingClientRect();
  out.afterGrow.rect = [Math.round(b2.left), Math.round(b2.top), Math.round(b2.width), Math.round(b2.height)];
  // 滚到底
  bubi.scrollTop = 99999;
  out.afterGrow.scrolledTo = bubi.scrollTop;

  // 还原
  span.textContent = bak;
  out.restored = { sh: bubi.scrollHeight, ch: bubi.clientHeight };
  return JSON.stringify(out);
})();
