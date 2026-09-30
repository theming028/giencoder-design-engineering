(function () {
  var out = {};
  function cs(el, p) { return el ? getComputedStyle(el)[p] : null; }
  function box(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [+b.x.toFixed(1), +b.y.toFixed(1), +b.width.toFixed(1), +b.height.toFixed(1)]; }

  /* 1. 普通按钮：是否已换成 DS Button */
  var btns = [].slice.call(document.querySelectorAll('.r85-btn'));
  out.buttons = btns.map(function (b) {
    return {
      text: b.textContent,
      cls: b.className,
      h: +b.getBoundingClientRect().height.toFixed(1),
      w: +b.getBoundingClientRect().width.toFixed(1),
      radius: cs(b, 'borderTopLeftRadius'),
      bg: cs(b, 'backgroundColor'),
      border: cs(b, 'borderTopColor'),
      color: cs(b, 'color'),
      shadow: cs(b, 'boxShadow')
    };
  });

  /* 2. 外观分段控件 */
  var seg = [].slice.call(document.querySelectorAll('.r85-seg > button'));
  out.seg = seg.map(function (b) {
    return {
      text: b.textContent,
      cls: b.className,
      pressed: b.getAttribute('aria-pressed'),
      wh: [+b.getBoundingClientRect().width.toFixed(1), +b.getBoundingClientRect().height.toFixed(1)],
      border: cs(b, 'borderTopWidth') + ' ' + cs(b, 'borderTopStyle') + ' ' + cs(b, 'borderTopColor'),
      radius: cs(b, 'borderTopLeftRadius'),
      bg: cs(b, 'backgroundColor')
    };
  });

  /* 3. 导航选中态：文字色 + 字重 */
  var navis = [].slice.call(document.querySelectorAll('.r85-navi'));
  out.nav = navis.map(function (n) {
    var sp = n.querySelector('span');
    return {
      t: sp ? sp.textContent : null,
      cur: n.getAttribute('aria-current'),
      bg: cs(n, 'backgroundColor'),
      spanColor: cs(sp, 'color'),
      spanWeight: cs(sp, 'fontWeight'),
      svgColor: cs(n.querySelector('svg'), 'color')
    };
  });

  /* 4. select：宽度自适应 + 右对齐（右缘应贴行右缘） */
  out.selects = [].slice.call(document.querySelectorAll('.r85-ctl > .giencoder-select')).map(function (s) {
    var view = s.querySelector('.giencoder-select-view');
    var row = s.closest('.r85-row');
    var txt = s.querySelector('.giencoder-select-view-text');
    return {
      txt: txt ? txt.textContent : null,
      w: +s.getBoundingClientRect().width.toFixed(1),
      h: +s.getBoundingClientRect().height.toFixed(1),
      radius: cs(view, 'borderTopLeftRadius'),
      boxShadow: cs(view, 'boxShadow'),
      inlineW: s.style.width || '(无)',
      truncated: txt ? txt.scrollWidth > txt.clientWidth : null,
      rowRight: row ? +row.getBoundingClientRect().right.toFixed(1) : null,
      ctlRight: +s.closest('.r85-ctl').getBoundingClientRect().right.toFixed(1)
    };
  });

  /* 5. 全局字号机制 */
  var html = document.documentElement;
  out.fs = {
    uiFs: getComputedStyle(html).getPropertyValue('--ui-fs').trim(),
    ratio: getComputedStyle(html).getPropertyValue('--ui-fs-ratio').trim(),
    inlineSet: html.style.getPropertyValue('--ui-fs') || '(未设)',
    tokenBody3: getComputedStyle(html).getPropertyValue('--font-size-body-3').trim(),
    sliderThumbX: (function () { var t = document.querySelector('.r85-sl-thumb'); return t ? t.style.left : null; })(),
    lsValue: (function () { try { return localStorage.getItem('gi-ui-fs'); } catch (e) { return 'ERR'; } })()
  };
  /* 外壳（React 渲染）与页面自绘各取一个样本 */
  out.fs.samples = {
    shellTopbar: (function () { var e = document.querySelector('header, .topbar, [class*="topbar"]'); return e ? cs(e, 'fontSize') : null; })(),
    navSpan: (function () { var e = document.querySelector('.r85-navi span'); return e ? cs(e, 'fontSize') : null; })(),
    title: (function () { var e = document.querySelector('.r85-title'); return e ? cs(e, 'fontSize') : null; })(),
    rowDesc: (function () { var e = document.querySelector('.r85-d'); return e ? cs(e, 'fontSize') : null; })(),
    body: cs(document.body, 'fontSize'),
    btnH: (function () { var e = document.querySelector('.r85-btn'); return e ? cs(e, 'height') : null; })()
  };

  /* 6. 页面整体几何（用于回归比对） */
  out.page = box(document.querySelector('.r85-page'));
  out.cards = [].slice.call(document.querySelectorAll('.r85-card')).map(function (c) { return +c.getBoundingClientRect().height.toFixed(1); });
  out.navHost = box(document.querySelector('.r85-nav-host'));
  out.aside = box(document.querySelector('aside'));

  return JSON.stringify(out, null, 1);
})()
