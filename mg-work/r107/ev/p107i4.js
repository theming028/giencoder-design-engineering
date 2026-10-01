(function () {
  var out = {};
  function cs(el, p) { return el ? getComputedStyle(el)[p] : 'ABSENT'; }
  function R(el) { var b = el.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; }
  function trio(el) {
    if (!el) return 'ABSENT';
    var c = getComputedStyle(el);
    return (c.whiteSpace === 'nowrap' && c.overflowX === 'hidden' && c.textOverflow === 'ellipsis') ? 'EL' : (c.whiteSpace + '/' + c.overflowX + '/' + c.textOverflow);
  }

  /* ================= ③ .td-sum-h = 15px ================= */
  out.sumH = Array.prototype.map.call(document.querySelectorAll('.td-sum-h'), function (e) {
    var c = getComputedStyle(e);
    return { fs: c.fontSize, fw: c.fontWeight, lh: c.lineHeight, h: Math.round(e.getBoundingClientRect().height) };
  });

  /* ================= ④⑤ diff 头 / 行 ================= */
  out.diff = Array.prototype.map.call(document.querySelectorAll('[data-td-diff]'), function (art) {
    var p = art.querySelector('.td-diff-path');
    var rows = art.querySelector('.td-diff-rows');
    return {
      open: art.classList.contains('is-open'),
      pathFs: cs(p, 'fontSize'), pathFw: cs(p, 'fontWeight'), pathTrio: trio(p),
      rowsFs: cs(rows, 'fontSize'),
      dr: cs(art.querySelector('.td-dr'), 'fontSize'),
      drNo: cs(art.querySelector('.td-dr-no'), 'fontSize'),
      drT: cs(art.querySelector('.td-dr-t'), 'fontSize'),
      dscC: cs(art.querySelector('.td-dsc-c'), 'fontSize'),
      more: cs(art.querySelector('.td-diff-more'), 'fontSize'),
      drH: (function () { var e = art.querySelector('.td-dr'); return e ? Math.round(e.getBoundingClientRect().height) : null; })(),
      headH: (function () { var e = art.querySelector('.td-diff-h'); return e ? Math.round(e.getBoundingClientRect().height) : null; })()
    };
  });

  /* ================= ⑥① .r107-stats ================= */
  (function () {
    var s = document.querySelector('.r107-stats');
    if (!s) { out.stats = 'ABSENT'; return; }
    var host = s.parentElement, sr = s.getBoundingClientRect(), hr = host.getBoundingClientRect();
    var c = getComputedStyle(s);
    var rg = document.createRange(); rg.selectNodeContents(s);
    var tr = rg.getBoundingClientRect();                        // ★ 文字的真实盒（不是盒子盒）
    var card = host.firstElementChild;
    var cr = card ? card.getBoundingClientRect() : null;
    out.stats = {
      box: [Math.round(sr.x), Math.round(sr.width)],
      text: [Math.round(tr.x), Math.round(tr.width)],
      card: cr ? [Math.round(cr.x), Math.round(cr.width)] : null,
      /* ★ 居中判据 = 文字中心 vs 输入卡中心（不是盒子中心） */
      textVsCardCenter: cr ? Math.round((tr.x + tr.width / 2) - (cr.x + cr.width / 2)) : null,
      textLeftPad: Math.round(tr.x - sr.x),
      sw: s.scrollWidth, cw: s.clientWidth,
      ws: c.whiteSpace, ta: c.textAlign, ov: c.overflowX, te: c.textOverflow,
      clipped: s.scrollWidth > s.clientWidth + 1,
      spillRight: Math.round((sr.x + sr.width) - (hr.x + hr.width))
    };
  })();

  /* ================= ① 白名单三件套 + 真溢出清单 ================= */
  var WL = ['.td-browse-tree-title', '.td-diff-more', '.td-diff-btn', '.td-commit-btn', '.td-commit-t',
    '.td-commit-lb', '.td-note-who', '.td-note-time', '.td-sum-tag', '.td-sum-srct i', '.td-sum-artt i',
    '.td-elnote-t', '.td-url-annot', '.td-page-cta', '.td-page-foot', '.td-rv-commit', '.td-rv-pr'];
  /* 改前就已有三件套的六类（作对照，证明本节没把它们弄坏） */
  var OLD = ['.td-tab-name', '.td-mm-name', '.td-diff-path', '.td-rv-meta', '.td-sum-hint', '.td-browse-crumb-path'];
  function scan(list) {
    var o = {};
    list.forEach(function (sel) {
      var a = document.querySelectorAll(sel);
      var okN = 0, bad = [];
      a.forEach(function (e) {
        var t = trio(e);
        if (t === 'EL') okN++;
        else bad.push(t + '(' + (e.textContent || '').trim().slice(0, 10) + ')');
      });
      o[sel] = { n: a.length, el: okN, bad: bad };
    });
    return o;
  }
  out.wl = scan(WL);
  out.oldCovered = scan(OLD);

  /* 真溢出：窄栏后谁被裁 + 是否省略号 */
  (function () {
    var slot = document.getElementById('av-browse-slot');
    if (slot) slot.style.setProperty('--av-browse-w', '240px');
    var list = [], n = 0;
    document.querySelectorAll('.td-browse *').forEach(function (e) {
      var c = getComputedStyle(e);
      if (c.display === 'none' || e.hasAttribute('hidden')) return;
      var txt = '', has = false;
      for (var i = 0; i < e.childNodes.length; i++) if (e.childNodes[i].nodeType === 3) { txt += e.childNodes[i].nodeValue; has = true; }
      txt = txt.replace(/\s+/g, ' ').trim();
      if (!has || !txt) return;
      if (e.scrollWidth <= e.clientWidth + 1) return;
      n++;
      if (list.length < 12) list.push({ cls: (e.tagName + '.' + String(e.className || '').trim().split(/\s+/).slice(0, 2).join('.')).slice(0, 40), ov: e.scrollWidth - e.clientWidth, te: c.textOverflow, ws: c.whiteSpace, sample: txt.slice(0, 16) });
    });
    out.panel240 = { w: Math.round(document.querySelector('.td-browse').getBoundingClientRect().width), clipN: n, list: list };
    if (slot) slot.style.removeProperty('--av-browse-w');
  })();

  return JSON.stringify(out, null, 1);
})()
