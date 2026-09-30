(function () {
  function cs(el, ps) {
    if (!el) return null;
    var c = getComputedStyle(el), o = {};
    ps.forEach(function (p) { o[p] = c[p]; });
    return o;
  }
  function R(el) { if (!el) return null; var r = el.getBoundingClientRect(); return { x: +r.x.toFixed(2), y: +r.y.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; }

  var page = document.querySelector('.r88-arch');
  if (!page) return JSON.stringify({ ok: false, html: document.body.innerHTML.length });

  var O = page.getBoundingClientRect();
  var out = { ok: true };

  /* ① 标题字号 vs r85-title */
  function fz(sel) {
    var el = document.querySelector(sel);
    if (!el) return null;
    var c = getComputedStyle(el);
    var r = el.getBoundingClientRect();
    return { fontSize: c.fontSize, lineHeight: c.lineHeight, fontWeight: c.fontWeight,
             fontFamily: c.fontFamily.slice(0, 24), h: +r.height.toFixed(2), w: +r.width.toFixed(2) };
  }
  out.archTitle = fz('.r88-arch-title');
  out.r85Title = fz('.r85-title');
  out.archHead = R(page.querySelector('.r88-arch-head'));
  out.archSub = fz('.r88-arch-sub');

  /* ② 卡片圆角 + 分隔线颜色 */
  function radius(sel) {
    var el = document.querySelector(sel);
    if (!el) return null;
    var c = getComputedStyle(el);
    return { borderRadius: c.borderRadius, bg: c.backgroundColor, outline: c.outlineWidth + ' ' + c.outlineStyle + ' ' + c.outlineColor, outlineOffset: c.outlineOffset };
  }
  out.archList = radius('.r88-arch-list');
  out.archEmpty = radius('.r88-arch-empty');
  out.r85Cards = [].slice.call(document.querySelectorAll('.r85-card')).map(function (c) { return getComputedStyle(c).borderRadius; });
  var row2 = page.querySelectorAll('.r88-arch-row')[1];
  out.archRowLine = row2 ? getComputedStyle(row2, '::before').backgroundColor : null;

  /* ③ 行内元信息图标 */
  var mic = page.querySelector('.r88-arch-mic');
  var svg = mic ? mic.querySelector('svg') : null;
  out.mic = {
    box: R(mic),
    svgBox: R(svg),
    viewBox: svg ? svg.getAttribute('viewBox') : null,
    d: svg ? [].slice.call(svg.querySelectorAll('path')).map(function (p) { return p.getAttribute('d'); }) : null,
    strokeWidth: svg ? [].slice.call(svg.querySelectorAll('path')).map(function (p) { return getComputedStyle(p).strokeWidth; }) : null,
    cs: cs(svg, ['width', 'height', 'flexShrink', 'display'])
  };
  var m = page.querySelector('.r88-arch-m');
  out.metaLine = fz('.r88-arch-m');
  out.metaChildren = [].slice.call(m.children).map(function (c) {
    var r = c.getBoundingClientRect();
    return c.className + ' x=' + +(r.x - O.x).toFixed(2) + ' w=' + +r.width.toFixed(2) + ' h=' + +r.height.toFixed(2);
  });

  /* ---- 切到「系统设置」页，验证 .r85-card / .r85-title（共用关系） ---- */
  var navSys = document.querySelector("[data-set-tab='system']");
  if (navSys) {
    navSys.click();
    var sysTitle = document.querySelector('.r85-title');
    out.sys = {
      title: sysTitle ? { fontSize: getComputedStyle(sysTitle).fontSize, lineHeight: getComputedStyle(sysTitle).lineHeight, fontWeight: getComputedStyle(sysTitle).fontWeight } : null,
      cards: [].slice.call(document.querySelectorAll('.r85-card')).map(function (c) { return getComputedStyle(c).borderRadius; })
    };
    var navArch = document.querySelector("[data-set-tab='archived']");
    if (navArch) navArch.click();
  }
  out.pageH = +O.height.toFixed(2);
  out.pageW = +O.width.toFixed(2);
  return JSON.stringify(out);
})()
