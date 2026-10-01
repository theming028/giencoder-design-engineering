/* 第十一拍 ④ 取证：终端多标签 / 浏览器截图 / 产物预览层。
   用法：agent-browser eval "window.__M='sum1'; <本文件内容>"
   每次量测前必须重新 open（agent-browser 的 eval 不保证上一次的 DOM 状态）。 */
(function () {
  var P = window.__M || 'sum1';
  var out = { phase: P };
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };
  var box = function (el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return [Math.round(r.width), Math.round(r.height)];
  };

  /* ---------- 终端快照 ---------- */
  function termSnap() {
    var wrap = $('.td-term-tabs');
    var tabs = $$('[data-td-term-tab]');
    var panes = $$('[data-td-term-pane]');
    var act = null, i;
    for (i = 0; i < panes.length; i++) if (!panes[i].hasAttribute('hidden')) act = panes[i];
    return {
      tabsBar: !!wrap,
      tabsBarH: wrap ? Math.round(wrap.getBoundingClientRect().height) : null,
      tabCount: tabs.length,
      tabs: tabs.map(function (t) {
        return { id: t.getAttribute('data-td-term-tab'),
                 name: (t.querySelector('.td-term-tab-nm') || {}).textContent,
                 active: t.classList.contains('is-active') };
      }),
      paneCount: panes.length,
      visiblePanes: panes.filter(function (p) { return !p.hasAttribute('hidden'); })
        .map(function (p) { return p.getAttribute('data-td-term-pane'); }),
      paneDetail: panes.map(function (p) {
        return { id: p.getAttribute('data-td-term-pane'), hidden: p.hasAttribute('hidden'),
                 outs: p.querySelectorAll('.td-term-out').length,
                 hasEcho: !!p.querySelector('[data-td-term-echo]'),
                 hasCaret: !!p.querySelector('[data-td-term-caret]') };
      }),
      activeOuts: act ? act.querySelectorAll('.td-term-out').length : 0,
      activeName: (function () {
        var t = $('.td-term-tab.is-active .td-term-tab-nm');
        return t ? t.textContent : null;
      })(),
      addBtn: !!$('[data-td-term-add]')
    };
  }

  /* ---------- 产物预览快照 ---------- */
  function prevSnap() {
    var prev = $('[data-td-prev]');
    var pane = $('.td-sum');
    if (!prev) return { present: false };
    var md = prev.querySelector('[data-td-prev-kind="md"]');
    var xs = prev.querySelector('[data-td-prev-kind="xlsx"]');
    return {
      present: true,
      hidden: prev.hasAttribute('hidden'),
      name: ($('[data-td-prev-name]') || {}).textContent,
      meta: ($('[data-td-prev-meta]') || {}).textContent,
      icoHasSvg: !!$('[data-td-prev-ico] svg'),
      mdHidden: md ? md.hasAttribute('hidden') : null,
      xlsxHidden: xs ? xs.hasAttribute('hidden') : null,
      paneBox: box(pane),
      prevBox: box(prev),
      covers: box(pane) && box(prev) &&
              box(pane)[0] === box(prev)[0] && box(pane)[1] === box(prev)[1],
      bg: getComputedStyle(prev).backgroundColor,
      closeBtn: !!$('[data-td-prev-close]'),
      openBtn: !!$('[data-td-prev-open]'),
      sheetRows: xs ? xs.querySelectorAll('.td-pv-row').length : 0,
      mdBars: md ? md.querySelectorAll('.td-pv-bar').length : 0
    };
  }

  if (P.indexOf('sum') === 0) {
    out.artsBefore = $$('[data-td-art]').length;
    out.previewBefore = prevSnap();
    if (P === 'sum1') {
      var a1 = $$('[data-td-art]')[0];
      if (a1) a1.click();
      out.previewAfter = prevSnap();
    } else if (P === 'sum2') {
      var a2 = $$('[data-td-art]')[1];
      if (a2) a2.click();
      out.previewAfter = prevSnap();
    } else if (P === 'sumx') {
      var cx = $('[data-td-prev-close]');
      if (cx) cx.click();
      out.previewAfter = prevSnap();
    }
  }

  if (P === 'term') out.term = termSnap();

  if (P === 'term2') {
    var t2 = $('[data-td-term-tab="t2"]');
    if (t2) t2.click();
    out.term = termSnap();
    out.activeElement = document.activeElement ? document.activeElement.className : null;
  }

  if (P === 'term3') {
    var ad = $('[data-td-term-add]');
    if (ad) ad.click();
    out.term = termSnap();
  }

  if (P === 'shot') {
    var b = $('[data-td-brw-act="shot"]');
    var brw = $('.td-brw');
    out.exists = !!b;
    out.label = b ? b.getAttribute('aria-label') : null;
    out.title = b ? b.getAttribute('title') : null;
    out.urlBox = box($('.td-url'));
    out.pillBox = box($('.td-url-pill'));
    if (b && brw) {
      b.click();
      out.flashed = brw.classList.contains('is-shot');
      out.animDur = getComputedStyle(brw, '::after').animationDuration;
      out.animName = getComputedStyle(brw, '::after').animationName;
      var tst = $('.td-toast');
      out.toast = tst && !tst.hasAttribute('hidden') ? tst.textContent : '';
    }
  }

  if (P === 'shot2') {
    var brw2 = $('.td-brw');
    out.flashedAfter400 = brw2 ? brw2.classList.contains('is-shot') : null;
  }

  return JSON.stringify(out);
})();
