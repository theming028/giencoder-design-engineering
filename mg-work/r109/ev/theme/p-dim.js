(function () {
  /* r109 第四拍 · 侦察（新增，补齐 `p-mix.js` 的盲区）：
     **暗色档下「深色压深色」的矢量图形**是谁？

     ★ 为什么必须单独做：`p-mix.js` 的 ⑥ 分支只查**纯文本节点**（`el.textContent && !el.children.length`），
       而品牌词标 / 图标字形是 `<svg><path fill="…">` —— **没有 textContent** ⇒ 全部漏掉。
       本拍实测证据：`base` 页暗色档下，词标 `GIENC⊕DER` 的 path `fill` 是 `rgb(30, 30, 30)`，
       而它所在的面是 `rgb(35, 35, 36)` ⇒ 对比 **1.05**，肉眼等于看不见；
       而 `p-mix.js` 对该页报 `lowContrast = 0` ⇒ **探针假阴性**（见 PLAYBOOK「探针假失败八类」第 5 类「选择器/判据层级错」）。
     ⇒ 本条与前一条是**镜像关系**：①找「暗底上发亮的面」，⑦找「暗底上发暗的图形」。

     ⚠ 只读，不改任何样式（唯一例外：钉死 transition，避免读到过渡中间值）。 */
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
    return m.length > 3 ? +m[3] : 1;
  }
  function path(el) {
    var p = [], n = 0;
    while (el && el.nodeType === 1 && el !== document.body && n < 5) {
      var s = el.tagName.toLowerCase();
      if (el.id) s += '#' + el.id;
      else {
        var c = (typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
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
  function nearestOpaqueBg(el) {
    /* ★★ 不能用「祖先链上第一个不透明底」—— 本拍实测的**假阳性根源**：
       工作空间图标是「绝对定位的色块 `<div>`（是 svg 的**兄弟**）+ 其上叠一个绝对定位的 `<svg>`」，
       于是祖先链上第一个不透明底是**顶栏**（暗 `rgb(23,23,26)`），而不是图形**实际压着的**那个色块
       ⇒ 一个「深字压在浅紫块上」（完全正常）会被报成「深压深 ratio 1.17」。
       ⇒ 判据改成**栈式命中测试**：取图形中心点，用 `elementsFromPoint` 拿该点的元素栈，
         取**第一个比自己更靠下、且有不透明底**的元素 —— 那才是肉眼看到的「背板」。 */
    var r = el.getBoundingClientRect();
    var cx = Math.min(window.innerWidth - 1, Math.max(0, r.x + r.width / 2));
    var cy = Math.min(window.innerHeight - 1, Math.max(0, r.y + r.height / 2));
    var stack = [];
    try { stack = document.elementsFromPoint(cx, cy); } catch (e) { stack = []; }
    var seen = false;
    for (var i = 0; i < stack.length; i++) {
      var q = stack[i];
      if (q === el || el.contains(q)) { seen = true; continue; }
      if (!seen) continue;                     /* 只从自己之后开始找背板 */
      var c = getComputedStyle(q).backgroundColor;
      if (alpha(c) > 0.5) return { v: c, l: lum(c), by: q, via: 'stack' };
    }
    /* 退路：祖先链（当 hit-test 拿不到时） */
    var p = el, n = 0;
    while (p && p !== document.documentElement && n < 12) {
      var c2 = getComputedStyle(p).backgroundColor;
      if (alpha(c2) > 0.5) return { v: c2, l: lum(c2), by: p, via: 'ancestor' };
      p = p.parentElement; n++;
    }
    return null;
  }

  noTrans();
  window.__giTheme.set('dark');
  noTrans();
  void document.documentElement.offsetHeight;

  var DE = getComputedStyle(document.documentElement);
  var SANITY = {
    attr: document.documentElement.getAttribute('giencoder-theme'),
    dataGiDark: document.documentElement.getAttribute('data-gi-dark'),
    bg1: DE.getPropertyValue('--color-bg-1').trim(),
    htmlBg: DE.backgroundColor,
    colorScheme: DE.colorScheme
  };

  var ARR = [];
  var all = document.querySelectorAll('svg, svg *, path, use, g, rect, circle, polygon');
  var darkGlyphs = 0;
  for (var i = 0; i < all.length; i++) {
    var el = all[i], cs = getComputedStyle(el);
    if (!vis(el, cs)) continue;
    /* svg 容器自身没有 fill 的语义（继承给子件）⇒ 只看真正带 fill 的图形件 */
    var fv = cs.fill;
    if (!fv || fv === 'none') continue;
    if (String(el.getAttribute('fill') || '') === 'none') continue;
    var lf = lum(fv);
    if (lf === null || alpha(fv) <= 0.5) continue;
    if (lf >= 0.25) continue;                 /* 只找「深填充」 */
    darkGlyphs++;
    var bg = nearestOpaqueBg(el);
    if (!bg || bg.l === null) continue;
    var hi = Math.max(lf, bg.l), lo = Math.min(lf, bg.l);
    var ratio = (hi + 0.05) / (lo + 0.05);
    if (ratio < 1.6) {
      var r = el.getBoundingClientRect();
      ARR.push({
        sel: path(el),
        fill: fv,
        fillAttr: String(el.getAttribute('fill') || ''),
        bg: bg.v,
        bgBy: path(bg.by), via: bg.via,
        ratio: +ratio.toFixed(2),
        x: Math.round(r.x), y: Math.round(r.y + window.scrollY),
        w: Math.round(r.width), h: Math.round(r.height),
        a: Math.round(r.width * r.height)
      });
    }
  }
  ARR.sort(function (a, b) { return a.ratio - b.ratio || b.a - a.a; });
  window.__giTheme.set('light');
  return JSON.stringify({
    sanity: SANITY, darkGlyphs: darkGlyphs,
    total: ARR.length, items: ARR.slice(0, 120)
  });
})()
