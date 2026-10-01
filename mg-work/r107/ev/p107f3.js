(function () {
  var out = {};
  // 1) 找到 ::after 挂着统计行的宿主（用计算样式里的 content 反查，不靠易碎的 > 链）
  var all = document.querySelectorAll('main *'), host = null;
  for (var i = 0; i < all.length; i++) {
    var c = getComputedStyle(all[i], '::after').content || '';
    if (c.indexOf('tok/s') >= 0) { host = all[i]; break; }
  }
  out.hostFound = !!host;
  if (!host) return JSON.stringify(out);
  out.hostCls = (host.className || '').slice(0, 100);
  var hr = host.getBoundingClientRect();
  out.hostRect = [Math.round(hr.left), Math.round(hr.top), Math.round(hr.width), Math.round(hr.height)];
  out.afterContent = (getComputedStyle(host, '::after').content || '').slice(0, 80);
  out.hostTextContent = (host.textContent || '').trim().slice(0, 60);
  out.hostChildCount = host.childElementCount;

  // 2) 统计行的视觉位置：host 是 flex-col，::after 是第 2 个 flex 项 ⇒ 取 host 底部那条
  var kids = host.children;
  var last = kids[kids.length - 1].getBoundingClientRect();
  var y = Math.round(last.bottom + 8 + 8);           // 卡底 + gap8 + 行高一半
  var x1 = Math.round(hr.left + 60), x2 = Math.round(hr.left + hr.width - 60);
  out.probeY = y; out.probeX = [x1, x2];

  // 3) elementFromPoint：谁在最上面
  var top = document.elementFromPoint(x1, y);
  out.topEl = top ? { tag: top.tagName, cls: (typeof top.className === 'string' ? top.className : '').slice(0, 70),
                      us: getComputedStyle(top).userSelect, pe: getComputedStyle(top).pointerEvents } : null;

  // 4) 模拟真鼠标拖选（与浏览器内部同机制）：caretRangeFromPoint ×2 → setBaseAndExtent
  function drag(xa, xb, yy) {
    var r1 = document.caretRangeFromPoint(xa, yy), r2 = document.caretRangeFromPoint(xb, yy);
    if (!r1 || !r2) return { err: 'no caretRange' };
    var sel = window.getSelection();
    sel.setBaseAndExtent(r1.startContainer, r1.startOffset, r2.startContainer, r2.startOffset);
    var s = sel.toString();
    return {
      picked: s.slice(0, 60), len: s.length,
      n1: r1.startContainer.nodeName, o1: r1.startOffset,
      n2: r2.startContainer.nodeName, o2: r2.startOffset
    };
  }
  out.dragStats = drag(x1, x2, y);

  // 5) 对照组：在输入框 placeholder 那行（真 DOM 文本）上做同样的拖选
  var ta = host.querySelector('textarea');
  if (ta) {
    var tr = ta.getBoundingClientRect();
    ta.value = '这是一段用于验证框选能力的样本文字';
    var cy = Math.round(tr.top + 14);
    out.dragTextarea = drag(Math.round(tr.left + 4), Math.round(tr.left + 120), cy);
  }

  // 6) 再验一次：把整段 ::after 内容的范围做 selectNodeContents
  var rg = document.createRange();
  rg.selectNodeContents(host);
  out.selectNodeContents = { len: rg.toString().length, txt: rg.toString().slice(0, 60) };

  return JSON.stringify(out);
})()
