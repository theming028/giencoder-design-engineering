(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  var bodyF = getComputedStyle(document.body).fontFamily;
  out.bodyFont = bodyF;

  /* ---------- ⑥ 字体统一：右栏内所有元素都应落到全局默认族 ---------- */
  var fam = {}, bad = [], badN = 0;
  document.querySelectorAll('.td-browse *').forEach(function (e) {
    var f = getComputedStyle(e).fontFamily;
    if (f !== bodyF) { fam[f] = (fam[f] || 0) + 1; badN++; if (bad.length < 8) bad.push(e.tagName + '.' + String(e.className).slice(0, 40)); }
  });
  out.fontBadN = badN;
  out.fontBadFams = fam;
  out.fontBadSample = bad;
  out.fontTotal = document.querySelectorAll('.td-browse *').length;
  /* 抽样四枚关键元素 */
  out.fontSample = {};
  [['.td-term', 'term'], ['.td-dr', 'diffRow'], ['.td-diff-path', 'diffPath'], ['.td-commit-num', 'commitNum'],
   ['.td-url-pill input', 'urlInput'], ['.td-commit-in .giencoder-input', 'branchInput'],
   ['.td-browse-pre', 'filesePre'], ['.td-code-tx', 'codeTx']].forEach(function (p) {
    var e = document.querySelector(p[0]);
    out.fontSample[p[1]] = e ? (getComputedStyle(e).fontFamily === bodyF ? 'OK' : getComputedStyle(e).fontFamily.slice(0, 50)) : 'ABSENT';
  });

  /* ---------- ⑤ 提交卡输入框拉通 ---------- */
  var ci = document.querySelector('.td-commit-in');
  if (ci) {
    var card = ci.closest('.td-commit-card'), cc = getComputedStyle(card), cr = card.getBoundingClientRect();
    var avail = Math.round(cr.width - parseFloat(cc.paddingLeft) - parseFloat(cc.paddingRight));
    out.ci = { r: r(ci), disp: getComputedStyle(ci).display, avail: avail, gap: Math.round(avail - ci.getBoundingClientRect().width) };
    var sib = ['.td-commit-h', '.td-commit-lb', '.td-commit-msg', '.td-commit-f'];
    out.ciSib = sib.map(function (s) { var e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().width) : null; });
  } else { out.ci = 'ABSENT'; }

  /* ---------- ③ 选中态底色 ---------- */
  out.checked = [];
  document.querySelectorAll('.td-browse .giencoder-dropdown-item.is-checked').forEach(function (e) {
    var c = getComputedStyle(e);
    out.checked.push({ t: (e.textContent || '').trim().slice(0, 12), bg: c.backgroundColor, color: c.color });
  });
  out.checkedN = out.checked.length;

  /* ---------- ②④ 标题 / 快捷键已隐藏 ---------- */
  function disp(sel) {
    var e = document.querySelector(sel);
    return e ? getComputedStyle(e).display : 'ABSENT';
  }
  out.capDisp = disp('.td-browse .td-mm-cap');
  out.keyDisp = disp('.td-browse .td-mm-key');
  out.capRect = (function () { var e = document.querySelector('.td-browse .td-mm-cap'); return e ? r(e) : null; })();
  out.keyRect = (function () { var e = document.querySelector('.td-browse .td-mm-key'); return e ? r(e) : null; })();
  /* 菜单自身高度（改前 + 菜单 6 项 + 1 标题；改后应矮一行、宽度不收） */
  out.menus = Array.prototype.map.call(document.querySelectorAll('.td-browse .giencoder-dropdown-popup'), function (m) {
    return { cls: String(m.className).replace('giencoder-dropdown-popup', '').trim().slice(0, 34), n: m.children.length, w: Math.round(m.getBoundingClientRect().width), h: Math.round(m.getBoundingClientRect().height) };
  });

  /* ---------- ① 可见竞品名 ---------- */
  out.codexText = [];
  var w = document.createTreeWalker(document.querySelector('.td-browse'), NodeFilter.SHOW_TEXT), n;
  while ((n = w.nextNode())) { if (/codex|chat\s?gpt/i.test(n.nodeValue)) out.codexText.push(n.nodeValue.trim().slice(0, 50)); }
  out.codexTextN = out.codexText.length;
  out.codexAttr = (function () {
    var c = 0;
    document.querySelectorAll('.td-browse *').forEach(function (e) {
      for (var i = 0; i < e.attributes.length; i++) {
        var a = e.attributes[i];
        if (a.name !== 'href' && /codex|chat\s?gpt/i.test(a.value)) c++;
      }
    });
    return c;
  })();

  /* ---------- ⑦ 全屏按钮 ---------- */
  var fs = document.querySelector('.r93-baract[data-r93-fullscreen]');
  var slot = document.getElementById('av-browse-slot'), row = slot && slot.parentElement;
  out.fs = fs ? { disp: getComputedStyle(fs).display, r: r(fs) } : 'ABSENT';
  out.fsBtnN = document.querySelectorAll('.r93-baract[data-r93-fullscreen]').length;
  out.rowHasOn = row ? row.classList.contains('av-browse-on') : null;
  out.browseBtnDisp = (function () { var b = document.querySelector('.r93-baract[data-r93-browse]'); return b ? getComputedStyle(b).display : 'ABSENT'; })();
  out.baractsKids = (function () { var p = fs && fs.parentElement; return p ? p.children.length : null; })();
  return JSON.stringify(out, null, 1);
})()
