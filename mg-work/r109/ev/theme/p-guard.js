(function () {
  var t = window.__giTheme;
  var de = document.documentElement;
  function tok() {
    var cs = getComputedStyle(de);
    return {
      bg1: cs.getPropertyValue('--color-bg-1').trim(),
      text1: cs.getPropertyValue('--color-text-1').trim()
    };
  }
  var shell = document.querySelector('.flex.h-dvh');
  var aside = document.querySelector('aside');
  var r = {
    page: location.pathname.split('/').pop(),
    hasApi: !!t,
    supported: t && t.supported ? t.supported() : null,
    mode0: t ? t.get() : null,
    attr0: de.getAttribute('giencoder-theme'),
    tok0: tok()
  };
  if (t) t.set('dark');
  r.mode1 = t ? t.get() : null;
  r.attr1 = de.getAttribute('giencoder-theme');
  r.data1 = de.getAttribute('data-gi-theme');
  r.tok1 = tok();
  r.shellBg = shell ? getComputedStyle(shell).backgroundColor : null;
  r.asideBg = aside ? getComputedStyle(aside).backgroundColor : null;
  r.bodyBg = getComputedStyle(document.body).backgroundColor;
  r.bodyFg = getComputedStyle(document.body).color;
  r.darkPaint = t && t.isDark ? t.isDark() : null;
  if (t) t.set('light');
  return JSON.stringify(r);
})()
