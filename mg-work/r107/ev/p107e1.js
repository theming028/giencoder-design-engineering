(function () {
  var pane = document.querySelector('.td-browse');
  var out = {};
  function R(el, tag) {
    if (!el) { out[tag] = null; return; }
    var c = getComputedStyle(el), r = el.getBoundingClientRect();
    out[tag] = {
      cls: String(el.className).slice(0, 96), hidden: el.hasAttribute('hidden'),
      vis: c.visibility, op: c.opacity, disp: c.display, pos: c.position,
      bg: c.backgroundColor, bw: c.borderTopWidth, brd: c.borderTopColor,
      rad: c.borderTopLeftRadius, sh: c.boxShadow.slice(0, 46), pad: c.padding,
      w: Math.round(r.width * 100) / 100, h: Math.round(r.height * 100) / 100,
      x: Math.round(r.x), y: Math.round(r.y),
      left: c.left, right: c.right, top: c.top, bottom: c.bottom,
      ovfY: c.overflowY, maxH: c.maxHeight, minW: c.minWidth
    };
  }
  /* ① 切到审查模块，并关掉 + 菜单 */
  pane.querySelector('[data-td-open-mod="review"]').click();
  pane.querySelector('[data-td-add]').click();
  R(pane.querySelector('[data-td-rv-opts]'), 'optsBtn');
  /* ② 打开「显示选项」菜单 */
  pane.querySelector('[data-td-rv-opts]').click();
  var m = pane.querySelector('.td-rv-opts');
  R(m, 'optsMenu');
  var items = m.querySelectorAll('.td-mm-item');
  out.items = items.length;
  R(items[0], 'item0');
  out.itemCls = [];
  for (var i = 0; i < items.length; i++) out.itemCls.push(String(items[i].className));
  out.rows = [];
  for (var j = 0; j < items.length; j++) {
    var rr = items[j].getBoundingClientRect();
    out.rows.push(Math.round(rr.y) + ':' + Math.round(rr.height) + ':' + Math.round(rr.width));
  }
  out.scroll = { sh: m.scrollHeight, ch: m.clientHeight, sw: m.scrollWidth, cw: m.clientWidth };
  /* ③ 分隔线 / 快捷键 / 勾 三种自绘槽位 */
  var ln = m.querySelector('.td-mm-line'), ky = m.querySelector('.td-mm-key'), mk = m.querySelector('.td-mm-mark');
  if (ln) { var lr = ln.getBoundingClientRect(); out.line = { y: Math.round(lr.y), w: Math.round(lr.width), h: Math.round(lr.height), bg: getComputedStyle(ln).backgroundColor }; }
  if (ky) { var kr = ky.getBoundingClientRect(); out.key = { w: Math.round(kr.width), fs: getComputedStyle(ky).fontSize, color: getComputedStyle(ky).color }; }
  if (mk) { var mr = mk.getBoundingClientRect(); out.mark = { w: Math.round(mr.width), op: getComputedStyle(mk).opacity }; }
  pane.querySelector('[data-td-rv-opts]').click();
  /* ④ 对照：+ 菜单（同一套 panel.css） */
  pane.querySelector('[data-td-add]').click();
  R(pane.querySelector('.td-mod-menu'), 'modMenu');
  R(pane.querySelector('.td-mod-menu .td-mm-item'), 'modItem0');
  pane.querySelector('[data-td-add]').click();
  /* ⑤ 级联诊断：哪些规则在抢 .td-mm-item 的 background */
  var hits = [];
  try {
    var sheets = document.styleSheets;
    for (var s = 0; s < sheets.length; s++) {
      var rs;
      try { rs = sheets[s].cssRules; } catch (e) { continue; }
      for (var q = 0; q < rs.length; q++) {
        var rule = rs[q], sel = rule.selectorText || '';
        if (!sel || !/td-mm-item|td-ctx-item/.test(sel)) continue;
        if (!/background/.test(rule.style && rule.style.cssText || '')) continue;
        hits.push({ sheet: s + '#' + q, sel: sel.slice(0, 110), bg: rule.style.getPropertyValue('background') });
      }
    }
  } catch (e) { hits.push('ERR ' + e.message); }
  out.bgRules = hits;
  return JSON.stringify(out);
})()
