(function () {
  var root = document.documentElement;
  var cs = getComputedStyle(root);
  var out = {
    page: location.pathname.split('/').pop(),
    attr: root.getAttribute('giencoder-theme'),
    tok_bg1: cs.getPropertyValue('--color-bg-1').trim(),
    tok_bg2: cs.getPropertyValue('--color-bg-2').trim(),
    tok_text1: cs.getPropertyValue('--color-text-1').trim(),
    tok_gray1: cs.getPropertyValue('--gray-1').trim(),
    tok_fill1: cs.getPropertyValue('--color-fill-1').trim(),
    themeRules: []
  };
  var sheets = document.styleSheets, i, j;
  for (i = 0; i < sheets.length; i++) {
    var rules;
    try { rules = sheets[i].cssRules; } catch (e) { continue; }
    for (j = 0; j < rules.length; j++) {
      var r = rules[j];
      if (!r.selectorText || r.selectorText.indexOf('giencoder-theme') < 0) continue;
      if (!r.style) continue;
      var v = r.style.getPropertyValue('--color-bg-1');
      if (v) out.themeRules.push({ sheet: i, idx: j, sel: r.selectorText.slice(0, 90), bg1: v.trim() });
    }
  }
  var rootRules = [];
  for (i = 0; i < sheets.length; i++) {
    var rs; try { rs = sheets[i].cssRules; } catch (e) { continue; }
    for (j = 0; j < rs.length; j++) {
      var r2 = rs[j];
      if (!r2.selectorText || !r2.style) continue;
      if (!r2.style.getPropertyValue('--color-bg-1')) continue;
      rootRules.push({ sheet: i, idx: j, sel: r2.selectorText.slice(0, 60), bg1: r2.style.getPropertyValue('--color-bg-1').trim() });
    }
  }
  out.allBg1Rules = rootRules;
  var body = document.body;
  out.bodyClass = (typeof body.className === 'string' ? body.className : '').slice(0, 120);
  out.bodyInlineBg = body.style.backgroundColor || '(none)';
  var shell = document.querySelector('.flex.h-dvh') || body.firstElementChild;
  if (shell) {
    out.shellClass = (typeof shell.className === 'string' ? shell.className : '').slice(0, 200);
    out.shellBg = getComputedStyle(shell).backgroundColor;
    out.shellInline = shell.getAttribute('style') || '(none)';
  }
  return JSON.stringify(out);
})()
