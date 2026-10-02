/* r109 第三拍 ③-c：**表面地图** —— 按 DOM 顺序列出所有「有不透明背景」的可见元素，
   并指出**是哪些 CSS 规则**给它上了背景（遍历样式表做 el.matches）。 */
(function () {
  /* 预扫：把「声明了 background-color 的规则」收集起来，便于后面对每个元素做 matches */
  var bgRules = [], s, r, sh, rules;
  for (s = 0; s < document.styleSheets.length; s++) {
    sh = document.styleSheets[s];
    try { rules = sh.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    for (r = 0; r < rules.length; r++) {
      var ru = rules[r];
      if (!ru.selectorText || !ru.style) continue;
      var bc = ru.style.backgroundColor;
      if (!bc) continue;
      bgRules.push({ sel: ru.selectorText, val: bc, sheet: s, idx: r });
    }
  }
  function why(el) {
    var hits = [], i;
    for (i = 0; i < bgRules.length; i++) {
      try { if (el.matches(bgRules[i].sel)) hits.push(bgRules[i].sel.slice(0, 70) + ' -> ' + bgRules[i].val); }
      catch (e) {}
      if (hits.length > 3) break;
    }
    return hits;
  }
  var out = [], i, el, all = document.querySelectorAll('body, body *');
  for (i = 0; i < all.length; i++) {
    el = all[i];
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    var bg = cs.backgroundColor, m = String(bg).match(/[\d.]+/g);
    if (!m || m.length < 3) continue;
    if (m.length >= 4 && +m[3] === 0) continue;
    var rr = el.getBoundingClientRect();
    if (rr.width < 3 || rr.height < 3) continue;
    var cls = (typeof el.className === 'string' ? el.className : (el.getAttribute('class') || '')).trim();
    if (el.tagName === 'SPAN' && !cls) continue;
    out.push({
      tag: el.tagName.toLowerCase(), cls: cls.slice(0, 110),
      inl: (el.getAttribute('style') || '').replace(/\s+/g, ' ').slice(0, 70),
      ibg: (el.style && el.style.backgroundColor) || '',
      bg: bg, box: [Math.round(rr.width), Math.round(rr.height)],
      why: why(el)
    });
    if (out.length > 70) break;
  }
  return JSON.stringify({ page: location.pathname.split('/').pop(), n: out.length, items: out });
})()
