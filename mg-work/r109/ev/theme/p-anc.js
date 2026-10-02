/* r109 ③-c 定点诊断 2：找出 `aside` 子树上 `--foreground` / `--background` 在哪一层被改写。 */
(function () {
  var out = { page: location.pathname.split('/').pop() };
  out.sheets = [];
  for (var s = 0; s < document.styleSheets.length; s++) {
    var sh = document.styleSheets[s], n = -1, head = [];
    try {
      var rs = sh.cssRules; n = rs ? rs.length : -1;
      if (rs) for (var i = 0; i < Math.min(2, rs.length); i++) head.push(rs[i].cssText.slice(0, 90));
    } catch (e) { head = ['ERR ' + e]; }
    out.sheets.push({ i: s, id: (sh.ownerNode && sh.ownerNode.id) || '', n: n, head: head });
  }
  var a = document.querySelector('aside');
  out.asideFound = !!a;
  out.chain = [];
  var el = a;
  while (el && el.nodeType === 1) {
    var cs = getComputedStyle(el);
    out.chain.push({
      tag: el.tagName.toLowerCase(),
      cls: (typeof el.className === 'string' ? el.className : '').slice(0, 70),
      inl: (el.getAttribute('style') || '').replace(/\s+/g, ' ').slice(0, 100),
      fg: cs.getPropertyValue('--foreground').trim(),
      bgv: cs.getPropertyValue('--background').trim(),
      color: cs.color, bg: cs.backgroundColor,
      td: cs.transitionDuration, tp: cs.transitionProperty.slice(0, 40)
    });
    el = el.parentElement;
  }
  /* body / html 的 color 也一并取 */
  out.bodyColor = getComputedStyle(document.body).color;
  out.bodyFg = getComputedStyle(document.body).getPropertyValue('--foreground').trim();
  /* aside 的 transition 目标值：临时关掉过渡再读一次 */
  if (a) {
    a.style.transition = 'none';
    void a.offsetWidth;
    var cs2 = getComputedStyle(a);
    out.asideNoTransition = { bg: cs2.backgroundColor, color: cs2.color,
                              fg: cs2.getPropertyValue('--foreground').trim() };
    a.style.transition = '';
  }
  return JSON.stringify(out);
})()
