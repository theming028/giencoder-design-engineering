(function () {
  var out = {};
  // ---- A. 隔离测试：真文本 vs 伪元素，同一位置、同一手法 ----
  var st = document.createElement('style');
  st.textContent = '#zzA::after{content:"PSEUDO-SELECT-ME";}';
  document.head.appendChild(st);
  var box = document.createElement('div');
  box.id = 'zzBox';
  box.style.cssText = 'position:fixed;left:60px;top:460px;z-index:2147483647;background:#fff;font-size:14px;line-height:22px;';
  box.innerHTML = '<div id="zzA"></div><div id="zzB">REAL-SELECT-ME</div>';
  document.body.appendChild(box);
  function drag(xa, xb, yy) {
    var r1 = document.caretRangeFromPoint(xa, yy), r2 = document.caretRangeFromPoint(xb, yy);
    if (!r1 || !r2) return { err: 'no caret' };
    var sel = window.getSelection();
    sel.setBaseAndExtent(r1.startContainer, r1.startOffset, r2.startContainer, r2.startOffset);
    return { picked: sel.toString(), n1: r1.startContainer.nodeName, o1: r1.startOffset };
  }
  var a = document.getElementById('zzA').getBoundingClientRect();
  var b = document.getElementById('zzB').getBoundingClientRect();
  out.A_pseudo = drag(Math.round(a.left + 2), Math.round(a.right - 2), Math.round(a.top + 11));
  out.B_real = drag(Math.round(b.left + 2), Math.round(b.right - 2), Math.round(b.top + 11));
  out.A_rect = [Math.round(a.left), Math.round(a.top), Math.round(a.width), Math.round(a.height)];
  out.B_rect = [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)];
  box.remove(); st.remove();

  // ---- B. ③ 两个容器的现状：所有 .giencoder-select / .giencoder-select-popup ----
  var sel = [];
  document.querySelectorAll('.giencoder-select').forEach(function (e) {
    var r = e.getBoundingClientRect();
    var pop = e.querySelector(':scope > [role="menu"], :scope > .giencoder-select-popup, :scope > .giencoder-select-dropdown');
    var pr = pop ? pop.getBoundingClientRect() : null;
    sel.push({
      cls: (e.className || '').slice(0, 60),
      inlineStyle: (e.getAttribute('style') || '').slice(0, 120),
      wh: Math.round(r.width) + 'x' + Math.round(r.height),
      x: Math.round(r.left),
      popCls: pop ? (pop.className || '').slice(0, 60) : null,
      popWH: pr ? Math.round(pr.width) + 'x' + Math.round(pr.height) : null,
      popInline: pop ? (pop.getAttribute('style') || '').slice(0, 200) : null,
      popCS: pop ? (function () { var c = getComputedStyle(pop); return { w: c.width, minW: c.minWidth, maxW: c.maxWidth, pos: c.position, left: c.left, right: c.right, box: c.boxSizing }; })() : null
    });
  });
  out.selects = sel;

  // ---- C. .r93-alert 现状 ----
  var al = [];
  document.querySelectorAll('.r93-alert').forEach(function (e) {
    var r = e.getBoundingClientRect();
    var c = getComputedStyle(e);
    var par = e.parentElement.getBoundingClientRect();
    al.push({
      wh: Math.round(r.width) + 'x' + Math.round(r.height),
      x: Math.round(r.left),
      parentWH: Math.round(par.width) + 'x' + Math.round(par.height),
      parentCls: (e.parentElement.className || '').slice(0, 50),
      cs: { w: c.width, h: c.height, ov: c.overflow, ws: c.whiteSpace },
      childScroll: e.scrollWidth + '/' + e.clientWidth,
      txt: (e.textContent || '').trim().slice(0, 50)
    });
  });
  out.alerts = al;
  return JSON.stringify(out);
})()
