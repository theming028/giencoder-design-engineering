/* r109 第三拍 ③-c 诊断：**为什么 body 底色/字色不吃 token**。
   枚举所有样式表里 selectorText 命中 body（或 html/:root）且声明了 background/color 的规则，
   连同 computed 的 token 值一起返回。 */
(function () {
  var root = document.documentElement;
  var out = {
    page: location.pathname.split('/').pop(),
    cs: getComputedStyle(root),
    vars: {}, body: {}, hits: [], sheets: []
  };
  ['--color-bg-1','--color-bg-2','--color-bg-3','--color-text-1','--color-text-2','--color-fill-1','--gray-1','--gray-10'].forEach(function (k) {
    out.vars[k] = out.cs.getPropertyValue(k).trim();
  });
  var bs = getComputedStyle(document.body);
  out.body = { bg: bs.backgroundColor, color: bs.color, cls: document.body.className,
               inline: document.body.getAttribute('style') || '' };
  for (var s = 0; s < document.styleSheets.length; s++) {
    var sh = document.styleSheets[s], rules;
    out.sheets.push({ i: s, n: (sh.href || '(inline)').slice(-40), count: 0 });
    try { rules = sh.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    out.sheets[s].count = rules.length;
    for (var r = 0; r < rules.length; r++) {
      var ru = rules[r];
      if (!ru.selectorText || !ru.cssText) continue;
      var sel = ru.selectorText;
      if (!/(^|[\s,>+~])(body|html|:root)\b/.test(sel) && sel !== 'body' && sel !== 'html' && sel !== ':root') continue;
      var txt = ru.cssText;
      if (!/background|color/.test(txt)) continue;
      out.hits.push({ s: s, r: r, sel: sel.slice(0, 90), css: txt.slice(0, 220).replace(/\s+/g, ' ') });
      if (out.hits.length > 40) break;
    }
  }
  return JSON.stringify(out);
})()
