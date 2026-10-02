/* r109 第三拍 ③-b 侦察：一次 eval 里**同时**取浅色档与暗色档的
   · 机制状态（档位 / html 属性 / localStorage / body 底色 / 设置页三枚按钮的 aria-pressed）
   · 对比度扫描：暗色档下「文字与最近不透明底色」对比度 < 3 的可见文本节点
   · 浅底块扫描：暗色档下背景仍然很亮的**可见**元素（白底/浅灰底残留）
   返回 { light: {...}, dark: {...} } —— 一次调用拿两档，省掉一半截图。 */
(function () {
  var root = document.documentElement;
  function lum(c) {
    var m = String(c).match(/[\d.]+/g);
    if (!m || m.length < 3) return null;
    function f(x) { x = x / 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }
    return 0.2126 * f(+m[0]) + 0.7152 * f(+m[1]) + 0.0722 * f(+m[2]);
  }
  function bgOf(el) {
    var n = el;
    while (n && n.nodeType === 1) {
      var c = getComputedStyle(n).backgroundColor;
      var m = String(c).match(/[\d.]+/g);
      if (m && m.length >= 3 && (m.length < 4 || +m[3] > 0.5)) return c;
      n = n.parentElement;
    }
    return getComputedStyle(document.body).backgroundColor;
  }
  function cls(el) {
    if (typeof el.className === 'string' && el.className) {
      return '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
    }
    return el.tagName.toLowerCase();
  }
  function visible(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function scan() {
    var low = [], bright = [], i, el, cs;
    var all = document.querySelectorAll('body *');
    for (i = 0; i < all.length; i++) {
      el = all[i];
      if (!visible(el)) continue;
      cs = getComputedStyle(el);
      /* 亮底残留：暗色档下背景亮度 > 0.75 的可见块 */
      var L = lum(cs.backgroundColor);
      if (L !== null && L > 0.75) {
        var r0 = el.getBoundingClientRect();
        bright.push({ sel: cls(el), bg: cs.backgroundColor,
                      box: [Math.round(r0.width), Math.round(r0.height)] });
        if (bright.length > 40) break;
      }
      /* 低对比度文本：只看「直接含非空文本节点」的元素 */
      var hasText = false, k;
      for (k = 0; k < el.childNodes.length; k++) {
        var nd = el.childNodes[k];
        if (nd.nodeType === 3 && nd.textContent.replace(/\s/g, '')) { hasText = true; break; }
      }
      if (!hasText) continue;
      var lf = lum(cs.color), lb = lum(bgOf(el));
      if (lf === null || lb === null) continue;
      var hi = Math.max(lf, lb), lo = Math.min(lf, lb);
      var ratio = (hi + 0.05) / (lo + 0.05);
      if (ratio < 3) {
        low.push({ t: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 22),
                   sel: cls(el), fg: cs.color, bg: bgOf(el),
                   r: Math.round(ratio * 100) / 100 });
        if (low.length > 40) break;
      }
    }
    return { lowText: low, brightBg: bright };
  }
  function snap(mode) {
    if (window.__giTheme) window.__giTheme.set(mode);
    var seg = document.querySelector('.r85-seg'), segs = null;
    if (seg) {
      segs = [];
      for (var i = 0; i < seg.children.length; i++) {
        segs.push(seg.children[i].getAttribute('aria-pressed'));
      }
    }
    var sc = scan();
    var stored = null;
    try { stored = localStorage.getItem('gi-ui-theme'); } catch (e) { stored = 'ERR'; }
    return {
      mode: (window.__giTheme && window.__giTheme.get()) || 'NO-API',
      attr: root.getAttribute('giencoder-theme'),
      dataAttr: root.getAttribute('data-gi-theme'),
      stored: stored,
      colorScheme: getComputedStyle(root).colorScheme,
      bodyBg: getComputedStyle(document.body).backgroundColor,
      titleColor: getComputedStyle(document.body).color,
      segPressed: segs,
      lowCount: sc.lowText.length,
      lowText: sc.lowText,
      brightCount: sc.brightBg.length,
      brightBg: sc.brightBg
    };
  }
  var out = { page: location.pathname.split('/').pop(), light: snap('light'), dark: snap('dark') };
  if (window.__giTheme) window.__giTheme.set('light');   /* 侦察完复位，别把后面的页带偏 */
  return JSON.stringify(out);
})()
