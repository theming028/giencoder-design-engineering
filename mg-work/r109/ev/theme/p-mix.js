(function () {
  /* r109 第四拍 · 侦察：**暗色档下仍然「发亮」的元素**是谁？
     —— 不靠像素聚簇猜，直接读 DOM：自己的不透明底色 / 渐变里的亮色 / 边框亮色。
     ⚠ 只读，不改任何样式（除了钉死 transition，防止读到过渡中间值）。 */
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
  function alpha(c) {
    var m = String(c).match(/[\d.]+/g);
    if (!m) return 1;
    if (m.length > 3) return +m[3];
    return 1;
  }
  function path(el) {
    var p = [], n = 0;
    while (el && el.nodeType === 1 && el !== document.body && n < 5) {
      var s = el.tagName.toLowerCase();
      if (el.id) s += '#' + el.id;
      else {
        var c = (typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
        if (c) s += '.' + c;
      }
      p.unshift(s); el = el.parentElement; n++;
    }
    return p.join('>');
  }
  function vis(el, cs) {
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width >= 1 && r.height >= 1;
  }
  function push(arr, o) { arr.push(o); }
  function rec(el, cs, kind, val, extra) {
    var r = el.getBoundingClientRect();
    var t = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 26);
    var o = {
      k: kind, v: String(val).slice(0, 60), sel: path(el),
      w: Math.round(r.width), h: Math.round(r.height),
      x: Math.round(r.x), y: Math.round(r.y + window.scrollY),
      a: Math.round(r.width * r.height), txt: t,
      /* ★ 定性用：这个色到底是**内联样式**给的，还是样式表给的？
         —— 内联的只能靠 `!important` 压，样式表的要走 token 改写。判据不同、修法不同。 */
      st: (el.getAttribute('style') || '').slice(0, 130),
      cls: String(el.className || '').slice(0, 90)
    };
    if (extra) for (var k in extra) o[k] = extra[k];
    push(ARR, o);
  }

  noTrans();
  window.__giTheme.set('dark');
  noTrans();
  void document.documentElement.offsetHeight;

  /* ★ 自证：必须在**暗色态**取样，否则报出来的「亮面」是浅色档的，判据全废。 */
  var DE = getComputedStyle(document.documentElement);
  var SANITY = {
    attr: document.documentElement.getAttribute('giencoder-theme'),
    dataGiDark: document.documentElement.getAttribute('data-gi-dark'),
    bg1: DE.getPropertyValue('--color-bg-1').trim(),
    htmlBg: DE.backgroundColor,
    bodyBg: getComputedStyle(document.body).backgroundColor,
    colorScheme: DE.colorScheme
  };

  var ARR = [];
  window.__ARR = ARR;
  var all = document.querySelectorAll('body *'), i, el, cs;
  for (i = 0; i < all.length; i++) {
    el = all[i];
    cs = getComputedStyle(el);
    if (!vis(el, cs)) continue;

    /* ① 自己有不透明亮底色 ⇒ 「浅色残留块」 */
    var lb = lum(cs.backgroundColor);
    if (lb !== null && lb > 0.55 && alpha(cs.backgroundColor) > 0.5) {
      rec(el, cs, 'bg', cs.backgroundColor);
    }
    /* ② 半透明亮底（遮罩/叠色）—— 单独记，避免被当成整块误判 */
    else if (lb !== null && lb > 0.55 && alpha(cs.backgroundColor) > 0.10) {
      rec(el, cs, 'bgA', cs.backgroundColor);
    }

    /* ③ 渐变里的亮色 */
    var bgi = cs.backgroundImage;
    if (bgi && bgi !== 'none') {
      var cols = bgi.match(/rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}/g) || [];
      for (var j = 0; j < cols.length; j++) {
        var lj = lum(cols[j]);
        if (lj !== null && lj > 0.55 && alpha(cols[j]) > 0.35) {
          rec(el, cs, 'bgimg', cols[j], { img: bgi.slice(0, 90) });
          break;
        }
      }
    }

    /* ④ 亮边框（1px 亮线在暗底上非常扎眼） */
    var bw = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderRightWidth)
           + parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderLeftWidth);
    if (bw > 0) {
      var bl = lum(cs.borderTopColor);
      if (bl !== null && bl > 0.55 && alpha(cs.borderTopColor) > 0.3) {
        rec(el, cs, 'border', cs.borderTopColor);
      }
    }

    /* ⑤ 亮 box-shadow（"发光"卡） */
    var sh = cs.boxShadow;
    if (sh && sh !== 'none') {
      var cs2 = sh.match(/rgba?\([^)]*\)/g) || [];
      for (var m = 0; m < cs2.length; m++) {
        var lm = lum(cs2[m]);
        if (lm !== null && lm > 0.70 && alpha(cs2[m]) > 0.10) {
          rec(el, cs, 'shadow', cs2[m], { img: sh.slice(0, 70) });
          break;
        }
      }
    }
  }

  /* ⑥ 兜底：暗色下字色比底色还浅到不可读（对比 < 1.6） */
  var low = [];
  for (i = 0; i < all.length; i++) {
    el = all[i]; cs = getComputedStyle(el);
    if (!vis(el, cs)) continue;
    var t2 = (el.textContent || '').trim();
    if (!t2 || el.children.length) continue;
    var lf = lum(cs.color);
    if (lf === null) continue;
    /* 找最近的不透明底 */
    var p = el, lbg = null;
    while (p && p !== document.documentElement) {
      var l2 = lum(getComputedStyle(p).backgroundColor);
      if (l2 !== null && alpha(getComputedStyle(p).backgroundColor) > 0.5) { lbg = l2; break; }
      p = p.parentElement;
    }
    if (lbg === null) continue;
    var hi = Math.max(lf, lbg), lo = Math.min(lf, lbg);
    var ratio = (hi + 0.05) / (lo + 0.05);
    if (ratio < 1.6) {
      var rr = el.getBoundingClientRect();
      low.push({ sel: path(el), fg: cs.color, bg: lbg, ratio: +ratio.toFixed(2),
                 txt: t2.replace(/\s+/g, ' ').slice(0, 24), w: Math.round(rr.width), h: Math.round(rr.height),
                 st: (el.getAttribute('style') || '').slice(0, 110),
                 cls: String(el.className || '').slice(0, 80) });
    }
  }
  low.sort(function (a, b) { return a.ratio - b.ratio; });

  ARR.sort(function (a, b) { return b.a - a.a; });
  var cnt = {};
  ARR.forEach(function (o) { cnt[o.k] = (cnt[o.k] || 0) + 1; });
  window.__giTheme.set('light');
  return JSON.stringify({
    sanity: SANITY,
    counts: cnt, total: ARR.length,
    items: ARR.slice(0, 150),
    lowContrast: low.slice(0, 40)
  });
})()
