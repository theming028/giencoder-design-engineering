(function () {
  var pane = document.querySelector('.td-browse');
  var m = pane.querySelector('.td-mod-menu');
  var hit = [];
  for (var i = 0; i < document.styleSheets.length; i++) {
    var ss = document.styleSheets[i], rules;
    try { rules = ss.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    for (var j = 0; j < rules.length; j++) {
      var r = rules[j];
      if (!r.selectorText) continue;
      if (r.selectorText.indexOf('td-mod-menu') < 0) continue;
      hit.push({ media: r.parentRule ? r.parentRule.conditionText || 'nested' : null, sel: r.selectorText, css: r.style.cssText.slice(0, 120) });
    }
  }
  return JSON.stringify({
    attrHidden: m.hasAttribute('hidden'),
    idlHidden: m.hidden,
    matchesSel: m.matches('.td-mod-menu[hidden]'),
    display: getComputedStyle(m).display,
    head: m.outerHTML.slice(0, 150),
    rules: hit
  });
})()
