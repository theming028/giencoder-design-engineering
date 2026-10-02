/* r109 第三拍 ③-c 定点诊断：暗色档下
   ① 注入块在不在、规则条数、前两条规则原文
   ② 关键 token 在 html / 深层元素上的 computed 值
   ③ 关键元素（外壳 / 侧栏 / 主面板 / 白卡）的 computed 底色 + 命中它底色的**全部规则**
   ④ `[class~="bg-[#F4F5F6]"]` 到底能不能命中侧栏 */
(function () {
  var root = document.documentElement;
  var out = { page: location.pathname.split('/').pop(), attr: root.getAttribute('giencoder-theme') };
  out.sheets = [];
  var darkSheet = null, s, r, sh, rules;
  for (s = 0; s < document.styleSheets.length; s++) {
    sh = document.styleSheets[s];
    var id = (sh.ownerNode && sh.ownerNode.id) || '';
    out.sheets.push({ i: s, id: id, n: (sh.href || '(inline)').slice(-30) });
    if (id === 'r109-dark-css') darkSheet = sh;
  }
  if (darkSheet) {
    try {
      rules = darkSheet.cssRules;
      out.darkRules = rules.length;
      out.darkHead = [];
      for (r = 0; r < Math.min(4, rules.length); r++) out.darkHead.push(rules[r].cssText.slice(0, 150));
      out.darkTail = [];
      for (r = Math.max(0, rules.length - 3); r < rules.length; r++) out.darkTail.push(rules[r].cssText.slice(0, 150));
    } catch (e) { out.darkErr = String(e); }
  } else { out.darkErr = 'NO DARK SHEET'; }

  var KEYS = ['--color-text-1', '--gray-10', '--color-bg-1', '--color-fill-1', '--foreground', '--background', '--border', '--card'];
  function vars(el) {
    var cs = getComputedStyle(el), o = {};
    for (var i = 0; i < KEYS.length; i++) o[KEYS[i]] = cs.getPropertyValue(KEYS[i]).trim();
    return o;
  }
  out.htmlVars = vars(root);
  out.bodyVars = vars(document.body);

  /* 收集「声明 background-color 的规则」 */
  var bgRules = [];
  for (s = 0; s < document.styleSheets.length; s++) {
    sh = document.styleSheets[s];
    try { rules = sh.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    for (r = 0; r < rules.length; r++) {
      var ru = rules[r];
      if (!ru.selectorText || !ru.style) continue;
      var bc = ru.style.backgroundColor, im = ru.style.getPropertyPriority('background-color');
      if (!bc) continue;
      bgRules.push({ sel: ru.selectorText, val: bc, imp: im || '', i: (sh.ownerNode && sh.ownerNode.id) || 's' + s });
    }
  }
  function why(el) {
    var hits = [], k;
    for (k = 0; k < bgRules.length; k++) {
      try { if (el.matches(bgRules[k].sel)) hits.push(bgRules[k].val + (bgRules[k].imp ? '!' : '') + '  <' + bgRules[k].sel.slice(0, 62) + '>  [' + bgRules[k].i + ']'); }
      catch (e) {}
      if (hits.length > 5) break;
    }
    return hits;
  }
  out.probe = [];
  var TARGETS = ['.flex.h-dvh', 'aside', 'main', '.bg-white', '.flex.min-h-0.flex-1', '.new-chat-btn', '.bg-white\\/50'];
  for (var ti = 0; ti < TARGETS.length; ti++) {
    var el = null;
    try { el = document.querySelector(TARGETS[ti]); } catch (e) { el = null; }
    if (!el) { out.probe.push({ sel: TARGETS[ti], found: false }); continue; }
    out.probe.push({
      sel: TARGETS[ti], found: true, tag: el.tagName.toLowerCase(),
      cls: (typeof el.className === 'string' ? el.className : '').slice(0, 90),
      bg: getComputedStyle(el).backgroundColor, color: getComputedStyle(el).color,
      why: why(el)
    });
  }
  /* 直接验：[class~="bg-[#F4F5F6]"] 能否命中 */
  var a = document.querySelector('aside');
  out.attrSelTest = a ? {
    cls: a.getAttribute('class').slice(0, 120),
    match_tilde: a.matches('[class~="bg-[#F4F5F6]"]'),
    match_star: a.matches('[class*="bg-[#F4F5F6]"]')
  } : null;
  return JSON.stringify(out);
})()
