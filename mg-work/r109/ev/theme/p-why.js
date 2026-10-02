(function () {
  /* 「谁给它上的色」：给定选择器，报出 computed 值 + 把**所有命中该元素的 CSS 规则**
     列出来（按文档顺序），并回读关键 token 的当前值。 */
  var TOK = ['--color-bg-5', '--color-bg-1', '--color-text-1', '--btn-bg',
             '--color-fill-2', '--gray-7', '--color-fill-3'];

  function tokvals(el) {
    var cs = getComputedStyle(el), o = {};
    TOK.forEach(function (k) { o[k] = cs.getPropertyValue(k).trim(); });
    return o;
  }
  function probe(sel) {
    var el;
    try { el = document.querySelector(sel); } catch (e) { return { sel: sel, err: String(e) }; }
    if (!el) return { sel: sel, found: false };
    var cs = getComputedStyle(el);
    var hits = [];
    for (var i = 0; i < document.styleSheets.length; i++) {
      var ss = document.styleSheets[i];
      var rules;
      try { rules = ss.cssRules; } catch (e) { continue; }
      if (!rules) continue;
      for (var j = 0; j < rules.length; j++) {
        var r = rules[j];
        if (!r.selectorText) continue;
        var m = false;
        try { m = el.matches(r.selectorText); } catch (e) { m = false; }
        if (!m) continue;
        var st = r.style;
        var decl = [];
        for (var k = 0; k < st.length; k++) {
          var p = st[k];
          if (/^(background|color|border|--btn-bg|box-shadow|opacity|filter)/.test(p)) {
            decl.push(p + ': ' + st.getPropertyValue(p));
          }
        }
        if (!decl.length) continue;
        hits.push({ sheet: (ss.ownerNode && ss.ownerNode.id) || ('#' + i),
                    sel: r.selectorText.slice(0, 120), decl: decl.join(' | ').slice(0, 260) });
      }
    }
    return {
      sel: sel, found: true, tag: el.tagName.toLowerCase(),
      cls: (typeof el.className === 'string' ? el.className : ''),
      inline: el.getAttribute('style') || '',
      bg: cs.backgroundColor, color: cs.color, bgImage: cs.backgroundImage.slice(0, 90),
      tok: tokvals(el), hits: hits
    };
  }

  var out = [];
  ['.giencoder-btn-secondary.mb-2', '.r85-ic', '.r85-sl-thumb'].forEach(function (s) { out.push(probe(s)); });

  /* 兜底：找出 computed color 恰好是 rgb(31, 31, 31) 的元素 */
  var sp = [], all = document.querySelectorAll('body *');
  for (var i2 = 0; i2 < all.length; i2++) {
    var e = all[i2];
    if (getComputedStyle(e).color !== 'rgb(31, 31, 31)') continue;
    var r2 = e.getBoundingClientRect();
    if (!(r2.width > 0 && r2.height > 0)) continue;
    sp.push({
      tag: e.tagName.toLowerCase(),
      cls: (typeof e.className === 'string' ? e.className : '').slice(0, 110),
      inline: (e.getAttribute('style') || '').slice(0, 160),
      text: (e.textContent || '').trim().slice(0, 40),
      size: [Math.round(r2.width), Math.round(r2.height)]
    });
    if (sp.length >= 6) break;
  }
  return JSON.stringify({
    page: location.pathname.split('/').pop(),
    attr: document.documentElement.getAttribute('giencoder-theme'),
    probes: out, thirtyone: sp
  });
})()
