JSON.stringify((function () {
  function box(el) { var b = el.getBoundingClientRect(); return [+b.x.toFixed(1), +b.y.toFixed(1), +b.width.toFixed(1), +b.height.toFixed(1)]; }
  var r = {};

  /* ---- ① aside 定宽 + 拖拽条已被中和 ---- */
  var aside = document.querySelector('aside');
  if (aside) {
    var as = getComputedStyle(aside);
    r.aside = { box: box(aside), inlineW: aside.style.width, cssW: as.width, ariaHidden: aside.getAttribute('aria-hidden') };
  }
  var sep = document.querySelector('[role="separator"][aria-label="调整菜单宽度"]');
  r.sep = sep ? { exists: true, display: getComputedStyle(sep).display, box: box(sep) } : { exists: false };

  /* ---- ③ select：必须是 DS 标准结构 ---- */
  var sels = [].slice.call(document.querySelectorAll('.giencoder-select'));
  r.selCount = sels.length;
  r.sels = sels.map(function (s) {
    var v = s.querySelector('.giencoder-select-view');
    var pop = s.querySelector('.giencoder-select-popup');
    var cs = v ? getComputedStyle(v) : null;
    return {
      w: +s.getBoundingClientRect().width.toFixed(1),
      box: box(s),
      view: !!v,
      role: v ? v.getAttribute('role') : null,
      expanded: v ? v.getAttribute('aria-expanded') : null,
      text: (s.querySelector('.giencoder-select-view-text') || {}).textContent || null,
      suffix: !!s.querySelector('.giencoder-select-suffix'),
      arrow: !!s.querySelector('.giencoder-select-arrow'),
      clear: !!s.querySelector('.giencoder-select-clear'),
      popup: !!pop,
      popupOpen: pop ? pop.classList.contains('giencoder-popup-open') : null,
      optCount: pop ? pop.querySelectorAll('.giencoder-select-option').length : 0,
      optSel: pop ? pop.querySelectorAll('.giencoder-select-option-selected').length : 0,
      hasValue: s.classList.contains('giencoder-select-has-value'),
      viewH: cs ? cs.height : null,
      viewBd: cs ? cs.borderTopWidth + ' ' + cs.borderTopColor : null,
      viewR: cs ? cs.borderTopLeftRadius : null,
      viewPad: cs ? cs.paddingLeft + ' / ' + cs.paddingRight : null
    };
  });
  r.legacy = {
    selBtn: document.querySelectorAll('.r85-sel').length,
    menu: document.querySelectorAll('.r85-menu').length
  };

  /* ---- ② 卡片分割线颜色 ---- */
  var rows = [].slice.call(document.querySelectorAll('.r85-card .r85-row'));
  var lines = [];
  for (var i = 0; i < rows.length; i++) {
    var pb = getComputedStyle(rows[i], '::before');
    if (pb.content !== 'none' && pb.backgroundColor !== 'rgba(0, 0, 0, 0)') lines.push({ i: i, bg: pb.backgroundColor, h: pb.height });
  }
  r.lines = lines;

  /* ---- ④ 行图标底 ---- */
  var ic = document.querySelector('.r85-ic');
  if (ic) { var ics = getComputedStyle(ic); r.ic = { bg: ics.backgroundColor, box: box(ic), r: ics.borderTopLeftRadius }; }

  /* ---- 复核 r85 成果未漂移 ---- */
  r.page = document.querySelector('.r85-page') ? box(document.querySelector('.r85-page')) : null;
  r.nav = document.querySelector('.r85-nav-host') ? box(document.querySelector('.r85-nav-host')) : null;
  r.cards = [].slice.call(document.querySelectorAll('.r85-card')).map(box);
  return r;
})())
