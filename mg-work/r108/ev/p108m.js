/* 第十二拍取证：① `.td-diff` 卡片化 · ② 文件树抽屉。
   用法：agent-browser eval "window.__M='diff'; <本文件内容>"
   ⚠ 严守两条踩过的坑：
     ① **过渡中取值**（量 `transform/opacity` 必须等过渡走完 —— 由 sh 里的 `wait` 负责分帧）；
     ② **点击与读值分帧**：本文件的 P='tree0' 只负责「点」，读值交给下一次 eval（P='tree1'）。 */
(function () {
  var P = window.__M || 'diff';
  var out = { phase: P };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var box = function (el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };

  /* ---------- ① diff 卡片 ---------- */
  function diffSnap() {
    var body = $('.td-rv-body');
    if (!body) return { present: false };
    var cs = getComputedStyle(body);
    var cards = $$('.td-diff');
    var rects = cards.map(box);
    var gaps = [];
    for (var i = 1; i < rects.length; i++) gaps.push(rects[i].y - (rects[i - 1].y + rects[i - 1].h));
    var c0 = cards[0];
    var cs0 = c0 ? getComputedStyle(c0) : null;
    var rows = c0 ? $('.td-diff-rows', c0) : null;
    var cr = rows ? getComputedStyle(rows) : null;
    return {
      present: true,
      bodyDisplay: cs.display,
      bodyGap: cs.gap,
      bodyPad: cs.padding,
      cardCount: cards.length,
      cards: rects,
      gaps: gaps,
      cardBorderTop: cs0 ? (cs0.borderTopWidth + ' ' + cs0.borderTopStyle + ' ' + cs0.borderTopColor) : null,
      cardBorderBottom: cs0 ? cs0.borderBottomWidth : null,
      cardRadius: cs0 ? cs0.borderTopLeftRadius : null,
      cardBg: cs0 ? cs0.backgroundColor : null,
      cardOverflow: cs0 ? cs0.overflow : null,
      rowsBorderTop: cr ? (cr.borderTopWidth + ' ' + cr.borderTopColor) : null,
      rowsPad: cr ? cr.padding : null,
      noteMargin: (function () {
        var n = c0 ? $('.td-note', c0) : null;
        return n ? getComputedStyle(n).margin : null;
      })()
    };
  }

  /* ---------- ② 文件树抽屉 ---------- */
  function treeSnap() {
    var t = $('[data-td-tree]');
    var btn = $('[data-td-rv-act="tree"]');
    if (!t) return { present: false };
    var panel = $('.td-tree-panel', t);
    var scrim = $('.td-tree-scrim', t);
    var rows = $$('.td-tf', t);
    var vis = rows.filter(function (r) { return getComputedStyle(r).display !== 'none'; });
    var nm = function (r) { var e = $('.td-tf-name', r); return e ? e.textContent : null; };
    return {
      present: true,
      hidden: t.hasAttribute('hidden'),
      open: t.classList.contains('is-open'),
      btnAria: btn ? btn.getAttribute('aria-expanded') : null,
      zIndex: getComputedStyle(t).zIndex,
      panelBox: box(panel),
      panelW: panel ? Math.round(panel.getBoundingClientRect().width) : null,
      panelTransform: panel ? getComputedStyle(panel).transform : null,
      panelRadius: panel ? getComputedStyle(panel).borderLeftColor : null,
      scrimBox: box(scrim),
      scrimOpacity: scrim ? getComputedStyle(scrim).opacity : null,
      paneBox: box($('.td-browse')),
      rowCount: rows.length,
      visibleRows: vis.length,
      visibleNames: vis.map(nm),
      activeName: (function () { var a = $('.td-tf.is-active', t); return a ? nm(a) : null; })(),
      closedDirs: rows.filter(function (r) { return r.classList.contains('is-closed'); }).map(nm),
      hasSearch: !!$('.td-browse-search', t),
      headerText: (function () { var e = $('.td-tree-t', t); return e ? e.textContent : null; })(),
      closeX: $$('[data-td-tree-x]', t).length
    };
  }

  /* 点一下某一行（by name） */
  function clickRow(name) {
    var rows = $$('.td-tf');
    for (var i = 0; i < rows.length; i++) {
      var e = $('.td-tf-name', rows[i]);
      if (e && e.textContent === name && rows[i].offsetParent !== null) {
        rows[i].click();
        return true;
      }
    }
    return false;
  }

  if (P === 'diff') {
    out.diff = diffSnap();
    /* 差集对照：同一份 .td-diff 在改前的旧值（border-bottom 1px / 无圆角 / 无 bg）也一并读出来 */
    var c = $$('.td-diff')[0];
    if (c) {
      var s = getComputedStyle(c);
      out.oldTells = { borderBottomWidth: s.borderBottomWidth, borderBottomStyle: s.borderBottomStyle,
                       borderTopWidth: s.borderTopWidth, radius: s.borderTopLeftRadius,
                       bg: s.backgroundColor };
    }
  }

  if (P === 'tree0') {
    out.treeBefore = treeSnap();
    var b = $('[data-td-rv-act="tree"]');
    out.clicked = !!b;
    if (b) b.click();
    out.ariaAfterClick = b ? b.getAttribute('aria-expanded') : null;
  }
  if (P === 'tree1') out.treeOpen = treeSnap();

  if (P === 'fold') { out.clickedRow = clickRow('games'); }
  if (P === 'tree2') out.treeAfterFold = treeSnap();

  if (P === 'unfold') { out.clickedRow = clickRow('games'); }
  if (P === 'tree2b') out.treeAfterUnfold = treeSnap();

  if (P === 'pick') { out.clickedRow = clickRow('index.html'); }
  if (P === 'tree2c') out.treeAfterPick = treeSnap();

  if (P === 'mask') {
    var sc = $('.td-tree-scrim');
    out.hasScrim = !!sc;
    if (sc) sc.click();
  }
  if (P === 'tree3') {
    out.treeClosed = treeSnap();
    out.paneOpen = !!$('.td-browse') && $('.td-browse').offsetParent !== null;
  }

  if (P === 'reopen') {
    var b2 = $('[data-td-rv-act="tree"]');
    if (b2) b2.click();
  }
  if (P === 'tree4') {
    out.treeReopen = treeSnap();
    out.paneOpen = !!$('.td-browse') && $('.td-browse').offsetParent !== null;
  }
  if (P === 'tree5') {
    out.treeAfterEsc = treeSnap();
    out.paneOpen = !!$('.td-browse') && $('.td-browse').offsetParent !== null;
    out.paneHidden = $('.td-browse') ? $('.td-browse').hasAttribute('hidden') : null;
  }

  /* 点抽屉里的行之后，验证「文件」模块那棵树**没被带坏**（独立类名的判据） */
  if (P === 'regress') {
    var filesTree = $('.td-browse-files');
    out.filesRows = filesTree ? $$('.td-bf', filesTree).length : 0;
    out.filesActive = (function () {
      var a = filesTree ? $('.td-bf.is-active', filesTree) : null;
      var e = a ? $('.td-bf-name', a) : null;
      return e ? e.textContent : null;
    })();
    out.filesHidden = filesTree ? $$('.td-bf.is-hidden', filesTree).length : 0;
    out.drawerRows = $$('.td-tf').length;
    out.drawerHidden = $$('.td-tf.is-hidden').length;
    out.drawerActive = (function () {
      var a = $('.td-tf.is-active');
      var e = a ? $('.td-tf-name', a) : null;
      return e ? e.textContent : null;
    })();
  }

  return JSON.stringify(out);
})();
