(function () {
  /* 列出本页的「子屏入口」= 点了会换主内容区的那几个按钮（只读）。
     规则：① 有 `.r85-navi`（设置页自己的左栏）⇒ 用它；
           ② 否则取左栏三个模块按钮（数字分身 / 自动化 / 技能 Skills）。 */
  function path(el) {
    var p = [], n = 0;
    while (el && el.nodeType === 1 && el !== document.body && n < 4) {
      var s = el.tagName.toLowerCase();
      if (el.id) s += '#' + el.id;
      else {
        var c = (typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
        if (c) s += '.' + c;
      }
      p.unshift(s); el = el.parentElement; n++;
    }
    return p.join('>');
  }
  function center(el) {
    var r = el.getBoundingClientRect();
    return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
  }
  function vis(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width > 40 && r.height > 16 && r.y > 40;
  }
  var out = [], NAVI = document.querySelectorAll('.r85-navi'), i;
  if (NAVI.length) {
    for (i = 0; i < NAVI.length; i++) {
      if (!vis(NAVI[i])) continue;
      var t = NAVI[i].textContent.replace(/\s+/g, ' ').trim();
      out.push({ label: t, sel: path(NAVI[i]), ...center(NAVI[i]) });
    }
  } else {
    var MODS = ['数字分身', '自动化', '技能 Skills'];
    var bs = document.querySelectorAll('body button');
    for (i = 0; i < bs.length; i++) {
      var tx = bs[i].textContent.replace(/\s+/g, ' ').trim();
      if (MODS.indexOf(tx) >= 0 && vis(bs[i])) out.push({ label: tx, sel: path(bs[i]), ...center(bs[i]) });
      if (out.length >= 3) break;
    }
  }
  return JSON.stringify({ n: out.length, items: out });
})()
