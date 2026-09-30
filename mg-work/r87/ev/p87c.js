(function () {
  var out = {};
  function cs(el, p) { return el ? getComputedStyle(el)[p] : null; }
  function n2(v) { return v == null ? null : +v.toFixed(1); }

  var de = document.documentElement;
  var gv = function (p) { return getComputedStyle(de).getPropertyValue(p).trim(); };
  out.uiFs = gv('--ui-fs');
  out.ratio = gv('--ui-fs-ratio');
  out.inlineSet = de.style.getPropertyValue('--ui-fs') || '(未设)';
  out.tokenBody3 = gv('--font-size-body-3');
  out.tokenBody = gv('--font-size-body');
  out.tokenTitle2 = gv('--font-size-title-2');

  /* 实际生效字号样本（应等比放大） */
  out.samples = {
    shellTopbar: (function () { var e = document.querySelector('header, .topbar, [class*="topbar"]'); return e ? cs(e, 'fontSize') : null; })(),
    navSpan: (function () { var e = document.querySelector('.r85-navi span'); return e ? cs(e, 'fontSize') : null; })(),
    title: (function () { var e = document.querySelector('.r85-title'); return e ? cs(e, 'fontSize') : null; })(),
    rowLabel: (function () { var e = document.querySelector('.r85-t'); return e ? cs(e, 'fontSize') : null; })(),
    rowDesc: (function () { var e = document.querySelector('.r85-d'); return e ? cs(e, 'fontSize') : null; })(),
    body: cs(document.body, 'fontSize'),
    btnText: (function () { var e = document.querySelector('.r85-btn'); return e ? cs(e, 'fontSize') : null; })(),
    btnH: (function () { var e = document.querySelector('.r85-btn'); return e ? cs(e, 'height') : null; })(),
    selViewH: (function () { var e = document.querySelector('.giencoder-select-view'); return e ? cs(e, 'minHeight') : null; })()
  };

  /* 控件高度是否跟随（应与字号同步长高） */
  out.ctlHeights = {
    btn: (function () { var e = document.querySelector('.r85-btn'); return e ? n2(e.getBoundingClientRect().height) : null; })(),
    segBtn: (function () { var e = document.querySelector('.r85-seg > button'); return e ? n2(e.getBoundingClientRect().height) : null; })(),
    select: (function () { var e = document.querySelector('.r85-ctl > .giencoder-select'); return e ? n2(e.getBoundingClientRect().height) : null; })(),
    navi: (function () { var e = document.querySelector('.r85-navi'); return e ? n2(e.getBoundingClientRect().height) : null; })()
  };

  /* select 触发框：min-height 是否已跟随（本次修复点） */
  out.selectView = (function () {
    var v = document.querySelector('.r85-ctl > .giencoder-select .giencoder-select-view');
    if (!v) return null;
    var c = getComputedStyle(v);
    return {
      minHeight: c.minHeight, height: n2(v.getBoundingClientRect().height),
      radius: c.borderTopLeftRadius, shadow: c.boxShadow,
      ring: (c.getPropertyValue('--select-ring') || '(未定义)').trim()
    };
  })();

  /* 外壳顶栏（React）实际字号 + 行高是否同步 —— 尾风覆盖的修复点 */
  out.shell = (function () {
    var e = document.querySelector('.text-sm, header, .topbar');
    if (!e) return null;
    var c = getComputedStyle(e);
    return { cls: (e.className || '').toString().slice(0, 40), fontSize: c.fontSize, lineHeight: c.lineHeight };
  })();

  /* 页面级横向溢出 */
  out.page = {
    docScrollW: de.scrollWidth, docClientW: de.clientWidth,
    overflowX: de.scrollWidth - de.clientWidth,
    bodyScrollW: document.body.scrollWidth, bodyClientW: document.body.clientWidth
  };

  /* 逐元素「内容被裁」（overflow != visible 且 scroll > client） */
  var bad = [], all = document.querySelectorAll('*');
  for (var i = 0; i < all.length; i++) {
    var el = all[i];
    if (el.closest && el.closest('.giencoder-select-popup')) continue;
    if (el.tagName === 'HTML' || el.tagName === 'BODY') continue;
    var c = getComputedStyle(el);
    if (c.display === 'none' || c.visibility === 'hidden') continue;
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    var ox = el.scrollWidth - el.clientWidth, oy = el.scrollHeight - el.clientHeight;
    var hx = c.overflowX !== 'visible' && ox > 1;
    var hy = c.overflowY !== 'visible' && oy > 1;
    if (hx || hy) {
      var cls = (el.className || '').toString().trim().split(/\s+/).slice(0, 2).join('.');
      bad.push({
        sel: el.tagName.toLowerCase() + (cls ? '.' + cls : ''),
        ox: ox, oy: oy, w: Math.round(r.width), h: Math.round(r.height),
        ov: c.overflowX + '/' + c.overflowY,
        text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 26)
      });
    }
  }
  out.clippedCount = bad.length;
  out.clipped = bad.slice(0, 30);

  /* 行盒是否被压扁（文本节点实际高度 > 容器高度 ⇒ 裁字） */
  var tight = [];
  var texts = document.querySelectorAll('.r85-t, .r85-d, .r85-navi span, .giencoder-btn, .r85-value, .r85-title');
  for (var j = 0; j < texts.length; j++) {
    var e2 = texts[j];
    var b = e2.getBoundingClientRect();
    var lh = parseFloat(getComputedStyle(e2).lineHeight) || 0;
    if (lh && b.height + 0.6 < lh) {
      tight.push({ sel: (e2.className || e2.tagName).toString().slice(0, 30), h: n2(b.height), lh: n2(lh), t: (e2.textContent || '').trim().slice(0, 20) });
    }
  }
  out.lineTightCount = tight.length;
  out.lineTight = tight.slice(0, 20);

  return JSON.stringify(out, null, 1);
})()
