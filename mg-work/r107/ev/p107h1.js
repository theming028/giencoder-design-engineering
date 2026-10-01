(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }

  /* ---------- ⑦ 右栏开合 & 全屏按钮 ---------- */
  var slot = document.getElementById('av-browse-slot');
  var row = slot && slot.parentElement;
  var fs = document.querySelector('.r93-baract[data-r93-fullscreen]');
  var br = document.querySelector('.r93-baract[data-r93-browse]');
  out.rowTag = row ? row.tagName : null;
  out.rowCls = row ? String(row.className) : null;
  out.rowHasOn = row ? row.classList.contains('av-browse-on') : null;
  out.rowContainsFs = !!(row && fs && row.contains(fs));
  out.fsFound = !!fs;
  out.fsR = fs ? r(fs) : null;
  out.fsDisp = fs ? getComputedStyle(fs).display : null;
  out.brFound = !!br;
  out.baractsCls = fs && fs.parentElement ? String(fs.parentElement.className) : null;
  out.baractsN = fs && fs.parentElement ? fs.parentElement.children.length : null;
  out.htmlAttrs = (function () { var s = []; for (var i = 0; i < document.documentElement.attributes.length; i++) s.push(document.documentElement.attributes[i].name); return s.join(','); })();

  /* ---------- ⑤ td-commit-in ---------- */
  var ci = document.querySelector('.td-commit-in');
  if (ci) {
    var card = ci.closest('.td-commit-card');
    var cs = getComputedStyle(ci);
    out.ci = { r: r(ci), disp: cs.display, w: cs.width, mw: cs.maxWidth, box: cs.boxSizing, mb: cs.marginBottom, cls: String(ci.className) };
    if (card) {
      var cc = getComputedStyle(card);
      var cr = card.getBoundingClientRect();
      out.card = { r: [Math.round(cr.left), Math.round(cr.top), Math.round(cr.width), Math.round(cr.height)], pad: cc.padding, w: cc.width };
      out.ciFill = Math.round(ci.getBoundingClientRect().width) + ' / card可用 ' + Math.round(cr.width - parseFloat(cc.paddingLeft) - parseFloat(cc.paddingRight));
    }
    var inp = ci.querySelector('.giencoder-input');
    out.ciInput = inp ? { cls: String(inp.className).slice(0, 90), r: r(inp), w: getComputedStyle(inp).width, flex: getComputedStyle(inp).flex } : null;
    out.ciKids = Array.prototype.map.call(ci.children, function (e) {
      return { tag: e.tagName, cls: String(e.className).slice(0, 50), r: r(e) };
    });
  } else { out.ci = 'NOT FOUND'; }

  /* ---------- ②④ 菜单标题 / 快捷键 ---------- */
  out.caps = [];
  document.querySelectorAll('.td-browse .td-mm-cap, .td-browse .td-ctx-head').forEach(function (e) {
    out.caps.push({ cls: String(e.className).slice(0, 60), t: (e.textContent || '').slice(0, 20), disp: getComputedStyle(e).display, r: r(e) });
  });
  out.keys = [];
  document.querySelectorAll('.td-browse .td-mm-key, .td-browse .td-ctx-key').forEach(function (e) {
    out.keys.push({ cls: String(e.className).slice(0, 60), t: (e.textContent || '').slice(0, 10), disp: getComputedStyle(e).display });
  });
  out.keyInHTML = (function () {
    var n = 0, w = document.createTreeWalker(document.querySelector('.td-browse'), NodeFilter.SHOW_TEXT), x;
    while ((x = w.nextNode())) { if (/[\u2318\u2303\u21e7\u2325]/.test(x.nodeValue)) n++; }
    return n;
  })();

  /* ---------- ③ 选中态 ---------- */
  out.checked = [];
  document.querySelectorAll('.td-browse .giencoder-dropdown-item.is-checked').forEach(function (e) {
    var c = getComputedStyle(e);
    out.checked.push({ t: (e.textContent || '').slice(0, 14), bg: c.backgroundColor, color: c.color, fw: c.fontWeight, aria: e.getAttribute('aria-checked'), role: e.getAttribute('role') });
  });
  out.menus = [];
  document.querySelectorAll('.td-browse .giencoder-dropdown-popup').forEach(function (m) {
    out.menus.push({ cls: String(m.className).slice(0, 70), n: m.children.length, hidden: m.hasAttribute('hidden') });
  });
  out.checkedTotal = document.querySelectorAll('.td-browse .giencoder-dropdown-item.is-checked').length;

  /* ---------- ⑥ 字体 ---------- */
  var bodyF = getComputedStyle(document.body).fontFamily;
  out.bodyFont = bodyF;
  var fam = {};
  document.querySelectorAll('.td-browse *').forEach(function (e) {
    var f = getComputedStyle(e).fontFamily;
    if (f !== bodyF) { fam[f] = (fam[f] || 0) + 1; }
  });
  out.otherFams = fam;

  /* ---------- ① Codex / ChatGPT 可见文本 ---------- */
  out.codex = [];
  var w2 = document.createTreeWalker(document.querySelector('.td-browse') || document.body, NodeFilter.SHOW_TEXT), n2;
  while ((n2 = w2.nextNode())) {
    if (/codex|chat\s?gpt/i.test(n2.nodeValue)) {
      var p = n2.parentElement;
      out.codex.push({ t: n2.nodeValue.trim().slice(0, 60), tag: p.tagName, cls: String(p.className).slice(0, 50) });
    }
  }
  return JSON.stringify(out, null, 1);
})()
