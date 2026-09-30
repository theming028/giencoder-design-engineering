(function () {
  function r(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function rr(s) { return r(document.querySelector(s)); }
  function cs(el, p) { return el ? getComputedStyle(el)[p] : null; }
  function q(s) { return document.querySelector(s); }
  var o = { vw: window.innerWidth, vh: window.innerHeight };

  /* ---- ① 字号 15px ---- */
  var wrap = q('.r93-wrap');
  var dist = {};
  Array.prototype.forEach.call(wrap.querySelectorAll('*'), function (e) {
    var has = false;
    Array.prototype.forEach.call(e.childNodes, function (n) { if (n.nodeType === 3 && n.textContent.trim()) has = true; });
    if (!has) return;
    var fs = getComputedStyle(e).fontSize;
    dist[fs] = (dist[fs] || 0) + 1;
  });
  o.wrapFontSizeDist = dist;
  o.t14Samples = ['.r93-t14', '.r93-t14m', '.r93-t14b'].map(function (c) {
    var e = wrap.querySelector(c) || document.querySelector(c);
    return { cls: c, found: !!e, fs: e ? getComputedStyle(e).fontSize : null, lh: e ? getComputedStyle(e).lineHeight : null };
  });
  /* 卡内必须仍是 13px（r97 ① 不能被吃掉） */
  var cd = q('.r93-card .r93-t14') || q('.r93-card');
  o.cardInner = { sel: cd ? cd.className : null, fs: cd ? getComputedStyle(cd).fontSize : null };

  /* ---- ② rateline 下方间距 ---- */
  var rlIt = q('.r93-rateline').closest('.r93-it');
  var wb = wrap.getBoundingClientRect();
  o.rateline = {
    it: r(rlIt), mt: cs(rlIt, 'marginTop'), mb: cs(rlIt, 'marginBottom'),
    wrapPadBottom: cs(wrap, 'paddingBottom'), wrapPadTop: cs(wrap, 'paddingTop'),
    gapBelow: Math.round(wb.bottom - parseFloat(cs(wrap, 'paddingBottom')) - rlIt.getBoundingClientRect().bottom)
  };

  /* ---- ③ 改动汇总卡 ---- */
  var d = q('.r93-diff');
  o.diff = { rect: r(d), bg: cs(d, 'backgroundColor'), border: cs(d, 'borderTopColor'), radius: cs(d, 'borderTopLeftRadius'), pad: cs(d, 'padding'), overflow: cs(d, 'overflow') };
  var dh = q('.r93-dhead');
  o.dhead = { rect: r(dh), h: cs(dh, 'height'), bg: cs(dh, 'backgroundColor'), bb: cs(dh, 'borderBottomColor'), bbw: cs(dh, 'borderBottomWidth'), pad: cs(dh, 'padding') };
  var dl = q('.r93-dlist');
  o.dlist = { rect: r(dl), bg: cs(dl, 'backgroundColor'), h: cs(dl, 'height'), margin: cs(dl, 'margin') };
  o.dsb = rr('.r93-dsb');
  o.dsbCS = { w: cs(q('.r93-dsb'), 'width'), h: cs(q('.r93-dsb'), 'height'), bg: cs(q('.r93-dsb'), 'backgroundColor'), radius: cs(q('.r93-dsb'), 'borderTopLeftRadius') };
  var rows = document.querySelectorAll('.r93-drow');
  o.drow = {
    rect: r(rows[0]), h: cs(rows[0], 'height'), gap: cs(rows[0], 'gap'), pad: cs(rows[0], 'padding'),
    bt: cs(rows[0], 'borderTopColor'),
    firstBtWidth: cs(rows[0], 'borderTopWidth'), secondBtWidth: cs(rows[1], 'borderTopWidth'),
    count: rows.length
  };
  o.dname = { rect: r(q('.r93-dname')), color: cs(q('.r93-dname'), 'color'), fs: cs(q('.r93-dname'), 'fontSize') };
  o.dtitle = { rect: r(q('.r93-dtitle')), color: cs(q('.r93-dtitle'), 'color'), fs: cs(q('.r93-dtitle'), 'fontSize') };
  o.plus = { color: cs(q('.r93-diff .r93-plus'), 'color'), fs: cs(q('.r93-diff .r93-plus'), 'fontSize') };
  o.minus = { color: cs(q('.r93-diff .r93-minus'), 'color') };
  o.dmore = { rect: r(q('.r93-dmore')), color: cs(q('.r93-dmore'), 'color'), shadow: cs(q('.r93-dmore'), 'boxShadow') };
  o.dbtn = { rect: r(q('.r93-dbtn')), w: cs(q('.r93-dbtn'), 'width'), pad: cs(q('.r93-dbtn'), 'padding') };
  o.dacts = rr('.r93-dacts');
  o.dh1 = rr('.r93-dh1');
  o.dh2 = rr('.r93-dh2');

  /* 右边界对齐账：卡内右沿 / 数字列右沿 / ⋯ 盒右沿 */
  var dR = r(d);
  o.align = {
    cardInnerRight: dR[0] + dR[2] - 1,
    moreRight: (function () { var b = r(q('.r93-dmore')); return b[0] + b[2]; })(),
    numRight: (function () { var b = r(q('.r93-dnum')); return b[0] + b[2]; })(),
    nameLeft: r(q('.r93-dname'))[0]
  };
  return JSON.stringify(o, null, 1);
})();
