(function () {
  var scroll = document.querySelector('.r93-scroll');
  var bar0 = document.querySelector('.td-selbar');
  var out = { barExistsBefore: !!bar0 };
  if (bar0) out.barHiddenBefore = bar0.hasAttribute('hidden');

  /* 造一个真实选区：找 `.r93-scroll` 里第一个够长的文本节点 */
  var node = null, host = null;
  var walker = document.createTreeWalker(scroll, NodeFilter.SHOW_TEXT, null, false);
  while (walker.nextNode()) {
    var t = walker.currentNode;
    if (t.nodeValue && t.nodeValue.trim().length >= 14) { node = t; host = t.parentElement; break; }
  }
  if (!node) return JSON.stringify({ err: 'no text node' });
  out.sample = node.nodeValue.trim().slice(0, 18);

  var r = document.createRange();
  r.setStart(node, 0);
  r.setEnd(node, Math.min(14, node.nodeValue.length));
  var s = window.getSelection();
  s.removeAllRanges();
  s.addRange(r);
  var rect = r.getBoundingClientRect();

  host.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: Math.round(rect.left + 12), clientY: Math.round(rect.top + 6) }));

  var bar = document.querySelector('.td-selbar');
  out.bar = !!bar;
  if (!bar) return JSON.stringify(out);
  out.hidden = bar.hasAttribute('hidden');
  var br = bar.getBoundingClientRect();
  out.barRect = [Math.round(br.x), Math.round(br.y), Math.round(br.width), Math.round(br.height)];
  out.selRect = [Math.round(rect.x), Math.round(rect.y), Math.round(rect.width)];
  out.above = br.y + br.height <= rect.y + 1;               /* 应浮在选区上方 */
  out.btns = [].map.call(bar.querySelectorAll('button'), function (b) { return b.textContent.trim(); });
  out.btnCls = bar.querySelector('button').className;
  var bc = getComputedStyle(bar);
  out.barBox = { bg: bc.backgroundColor, r: bc.borderTopLeftRadius, shadow: bc.boxShadow.slice(0, 30), pad: bc.paddingTop };

  /* ①「添加到对话」 */
  var ta = [].filter.call(document.querySelectorAll('textarea'), function (e) {
    return (e.getAttribute('placeholder') || '').indexOf('描述你的任务') === 0;
  })[0];
  out.taFound = !!ta;
  out.taBefore = ta ? ta.value.length : null;
  bar.querySelector('button').click();
  out.taAfter = ta ? ta.value.length : null;
  out.taTail = ta ? ta.value.slice(-24) : null;
  out.toast1 = document.querySelector('.td-toast') ? document.querySelector('.td-toast').textContent : null;
  out.hiddenAfterAdd = document.querySelector('.td-selbar').hasAttribute('hidden');

  /* ②「复制」按钮存在性 + 收起 */
  s.removeAllRanges();
  s.addRange(r);
  host.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: Math.round(rect.left + 12), clientY: Math.round(rect.top + 6) }));
  var bar2 = document.querySelector('.td-selbar');
  out.reopen = !bar2.hasAttribute('hidden');
  bar2.querySelectorAll('button')[1].click();
  out.toast2 = document.querySelector('.td-toast') ? document.querySelector('.td-toast').textContent : null;
  out.hiddenAfterCopy = bar2.hasAttribute('hidden');

  /* ③ 再开一次，验 Esc 只收浮条、不关整条侧栏 */
  s.removeAllRanges();
  s.addRange(r);
  host.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: Math.round(rect.left + 12), clientY: Math.round(rect.top + 6) }));
  var bar3 = document.querySelector('.td-selbar');
  out.opened3 = !bar3.hasAttribute('hidden');
  window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  out.hiddenAfterEsc = bar3.hasAttribute('hidden');
  out.panelStillOn = !!document.querySelector('.av-browse-on');
  return JSON.stringify(out);
})()
