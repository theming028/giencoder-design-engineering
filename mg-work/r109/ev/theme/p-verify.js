(function () {
  /* ★ 过渡冻结免疫：先钉死 transition/animation，再切档、再强制回流、再量。
     否则 `transition: all .2s` 的元素在自动化环境里可能停在**起始值**上，
     把「已经改对了」读成「没生效」（探针假失败第 ② 类：过渡中取值）。 */
  function noTrans() {
    if (document.getElementById('probe-notrans')) return;
    var s = document.createElement('style');
    s.id = 'probe-notrans';
    s.textContent = '*,*::before,*::after{transition:none!important;animation:none!important;}';
    (document.head || document.documentElement).appendChild(s);
  }

  function lum(c) {
    var m = String(c).match(/[\d.]+/g);
    if (!m || m.length < 3) return null;
    function f(x) { x = x / 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }
    return 0.2126 * f(+m[0]) + 0.7152 * f(+m[1]) + 0.0722 * f(+m[2]);
  }
  function vis(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function snapshot(tag) {
    void document.documentElement.offsetHeight;      /* 强制回流 */
    var de = document.documentElement;
    var cs = getComputedStyle(de), bs = getComputedStyle(document.body);
    var tok = {};
    ['--color-bg-1', '--color-bg-2', '--color-text-1', '--color-fill-1', '--color-white']
      .forEach(function (k) { tok[k] = cs.getPropertyValue(k).trim(); });

    var map = {}, i, el, all = document.querySelectorAll('body *');
    for (i = 0; i < all.length; i++) {
      el = all[i];
      if (!vis(el)) continue;
      var s = getComputedStyle(el);
      var lb = lum(s.backgroundColor), lf = lum(s.color);
      var needBg = (lb !== null && lb > 0.55 && +s.opacity > 0.5);
      var needFg = (lf !== null && lf < 0.20);
      if (!needBg && !needFg) continue;
      var cls = (typeof el.className === 'string' ? el.className : '');
      var inl = el.getAttribute('style') || '';
      var key = cls + '@@' + inl;
      if (map[key]) { map[key].n++; continue; }
      map[key] = {
        n: 1, tag: el.tagName.toLowerCase(), cls: cls.slice(0, 150),
        bg: s.backgroundColor, fg: s.color, inl: inl.slice(0, 120),
        needBg: needBg, needFg: needFg,
        box: [Math.round(el.getBoundingClientRect().width), Math.round(el.getBoundingClientRect().height)]
      };
    }
    var items = [];
    for (var k in map) if (map.hasOwnProperty(k)) items.push(map[k]);
    items.sort(function (a, b) { return b.n - a.n; });

    return {
      mode: tag,
      attr: de.getAttribute('giencoder-theme'),
      dataAttr: de.getAttribute('data-gi-theme'),
      colorScheme: cs.colorScheme,
      tokens: tok,
      bodyBg: bs.backgroundColor,
      bodyFg: bs.color,
      htmlBg: cs.backgroundColor,
      vis: document.visibilityState,
      groups: items.length,
      brightBg: items.filter(function (x) { return x.needBg; }).slice(0, 22),
      darkFg: items.filter(function (x) { return x.needFg; }).slice(0, 22)
    };
  }

  var out = {};
  noTrans();
  document.documentElement.removeAttribute('giencoder-theme');
  out.light = snapshot('light');
  window.__giTheme.set('dark');
  noTrans();
  out.dark = snapshot('dark');
  window.__giTheme.set('light');
  noTrans();
  return JSON.stringify(out);
})()
