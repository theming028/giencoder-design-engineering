(function () {
  var pane = document.querySelector('.td-browse');
  var m = pane.querySelector('.td-mod-menu');
  var out = [];
  function walk(rules, media) {
    for (var j = 0; j < rules.length; j++) {
      var r = rules[j];
      if (r.cssRules && !r.selectorText) { walk(r.cssRules, (r.conditionText || r.name || media)); continue; }
      if (!r.selectorText) continue;
      var st = r.style;
      if (!st) continue;
      var decl = [];
      ['display', 'position', 'top', 'bottom', 'visibility', 'opacity'].forEach(function (p) {
        if (st.getPropertyValue(p)) decl.push(p + ':' + st.getPropertyValue(p) + (st.getPropertyPriority(p) ? '!' : ''));
      });
      if (!decl.length) continue;
      var ok = false;
      try { ok = m.matches(r.selectorText); } catch (e) { ok = false; }
      if (!ok) continue;
      out.push({ m: media, sel: r.selectorText.slice(0, 90), d: decl.join(';') });
    }
  }
  for (var i = 0; i < document.styleSheets.length; i++) {
    var ss = document.styleSheets[i], rules;
    try { rules = ss.cssRules; } catch (e) { continue; }
    if (rules) walk(rules, null);
  }
  return JSON.stringify({
    display: getComputedStyle(m).display,
    attr: m.hasAttribute('hidden'),
    matched: out
  });
})()
