(function () {
  var d = document.getElementById('av-chat-drawer');
  var it = d.querySelectorAll('.av-hs-item')[2];
  it.classList.add('is-confirm');
  var hits = [];
  for (var i = 0; i < document.styleSheets.length; i++) {
    var ss = document.styleSheets[i], rules;
    try { rules = ss.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    for (var j = 0; j < rules.length; j++) {
      var r = rules[j];
      if (!r.selectorText) continue;
      if (r.selectorText.indexOf('av-hs-item') < 0) continue;
      if (!/background/.test(r.cssText || '')) continue;
      var m = false;
      try { m = it.matches(r.selectorText); } catch (e) {}
      hits.push({
        sel: r.selectorText,
        bg: r.style.getPropertyValue('background') || r.style.getPropertyValue('background-color'),
        matches: m,
        sheet: i
      });
    }
  }
  return JSON.stringify({ computed: getComputedStyle(it).backgroundColor, inline: it.getAttribute('style'), hits: hits });
})()
