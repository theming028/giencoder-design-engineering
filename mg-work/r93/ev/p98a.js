(function () {
  function r(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function rr(s) { return r(document.querySelector(s)); }
  function cs(el, p) { return el ? getComputedStyle(el)[p] : null; }
  var o = { vw: window.innerWidth, vh: window.innerHeight };

  /* ---- ① 对话内容区字号分布（.r93-wrap 内） ---- */
  var wrap = document.querySelector('.r93-wrap');
  var dist = {};
  Array.prototype.forEach.call(wrap.querySelectorAll('*'), function (e) {
    var has = false;
    Array.prototype.forEach.call(e.childNodes, function (n) { if (n.nodeType === 3 && n.textContent.trim()) has = true; });
    if (!has) return;
    var fs = getComputedStyle(e).fontSize;
    dist[fs] = (dist[fs] || 0) + 1;
  });
  o.wrapFontSizeDist = dist;

  var t14 = [];
  Array.prototype.forEach.call(wrap.querySelectorAll('.r93-t14, .r93-t14m, .r93-t14b'), function (e) {
    t14.push({ cls: e.className, fs: cs(e, 'fontSize'), lh: cs(e, 'lineHeight'), txt: (e.textContent || '').trim().slice(0, 18) });
  });
  o.t14s = t14;

  /* ---- ② rateline 下方间距 ---- */
  var rl = document.querySelector('.r93-rateline');
  var rlIt = rl ? rl.closest('.r93-it') : null;
  o.rateline = {
    rect: r(rl), it: r(rlIt),
    itMarginTop: cs(rlIt, 'marginTop'), itMarginBottom: cs(rlIt, 'marginBottom'),
    isLast: rlIt ? (rlIt === rlIt.parentNode.lastElementChild) : null,
    nextSib: rlIt && rlIt.nextElementSibling ? rlIt.nextElementSibling.className : null
  };
  o.wrapPad = { top: cs(wrap, 'paddingTop'), bottom: cs(wrap, 'paddingBottom') };
  o.scrollRect = rr('.r93-scroll');
  o.wrapRect = r(wrap);
  // 内容盒底 - rateline 底 = 「下方间距」实测
  if (rlIt) {
    var wb = wrap.getBoundingClientRect(), rb = rlIt.getBoundingClientRect();
    o.gapBelowRateline = Math.round(wb.bottom - parseFloat(cs(wrap, 'paddingBottom')) - rb.bottom);
  }

  /* ---- ③ 改动汇总卡 ---- */
  var d = document.querySelector('.r93-diff');
  o.diff = {
    rect: r(d), bg: cs(d, 'backgroundColor'), border: cs(d, 'borderTopColor'),
    bw: cs(d, 'borderTopWidth'), radius: cs(d, 'borderTopLeftRadius'), pad: cs(d, 'padding')
  };
  o.dhead = rr('.r93-dhead');
  o.dheadCS = { h: cs(document.querySelector('.r93-dhead'), 'height') };
  var dl = document.querySelector('.r93-dlist');
  o.dlist = { rect: r(dl), bg: cs(dl, 'backgroundColor'), h: cs(dl, 'height'), margin: cs(dl, 'margin'), overflow: cs(dl, 'overflowY') };
  var dr = document.querySelector('.r93-drow');
  o.drow = {
    rect: r(dr), h: cs(dr, 'height'), bt: cs(dr, 'borderTopColor'), bw2: cs(dr, 'borderTopWidth'),
    padding: cs(dr, 'padding')
  };
  o.drowCount = document.querySelectorAll('.r93-drow').length;
  o.dname = { color: cs(document.querySelector('.r93-dname'), 'color'), fs: cs(document.querySelector('.r93-dname'), 'fontSize') };
  var p1 = document.querySelector('.r93-diff .r93-plus'), m1 = document.querySelector('.r93-diff .r93-minus');
  o.plus = { color: cs(p1, 'color'), fs: cs(p1, 'fontSize') };
  o.minus = { color: cs(m1, 'color'), fs: cs(m1, 'fontSize') };
  var dmore = document.querySelector('.r93-dmore');
  o.dmore = { rect: r(dmore), bg: cs(dmore, 'backgroundColor'), border: cs(dmore, 'borderTopColor'), radius: cs(dmore, 'borderTopLeftRadius') };
  var db = document.querySelector('.r93-dbtn');
  o.dbtn = {
    rect: r(db), h: cs(db, 'height'), bg: cs(db, 'backgroundColor'), border: cs(db, 'borderTopColor'),
    bw: cs(db, 'borderTopWidth'), radius: cs(db, 'borderTopLeftRadius'), pad: cs(db, 'padding'),
    gap: cs(db, 'gap'), fs: cs(db, 'fontSize'), color: cs(db, 'color'), cls: db.className
  };
  var dh1 = document.querySelector('.r93-dh1');
  o.dh1 = { rect: r(dh1), gap: cs(dh1, 'gap') };
  o.dacts = { rect: rr('.r93-dacts'), gap: cs(document.querySelector('.r93-dacts'), 'gap') };
  var dt = document.querySelector('.r93-dtitle');
  o.dtitle = { rect: r(dt), color: cs(dt, 'color'), fs: cs(dt, 'fontSize') };
  // 卡内文本的 x 位置（右对齐列）
  o.dnum = Array.prototype.map.call(document.querySelectorAll('.r93-dnum'), function (e) { return r(e); });
  o.dnames = Array.prototype.map.call(document.querySelectorAll('.r93-dname'), function (e) { return [r(e)[0], (e.textContent || '').trim()]; });

  /* 滚动条元素（设计稿有 6x128 thumb） */
  o.hasThumbEl = !!document.querySelector('.r93-diff [class*=scroll], .r93-diff [class*=sb]');

  /* ---- 变量 ---- */
  var root = getComputedStyle(document.documentElement);
  o.vars = {
    border1: root.getPropertyValue('--color-border-1').trim(),
    border2: root.getPropertyValue('--color-border-2').trim(),
    card: root.getPropertyValue('--r93-card').trim(),
    edge: root.getPropertyValue('--r93-edge').trim(),
    success6: root.getPropertyValue('--color-success-6').trim(),
    danger6: root.getPropertyValue('--color-danger-6').trim(),
    primary6: root.getPropertyValue('--color-primary-6').trim(),
    fill2: root.getPropertyValue('--color-fill-2').trim()
  };
  return JSON.stringify(o, null, 1);
})();
