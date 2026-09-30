(function () {
  function R(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { x: +r.x.toFixed(2), y: +r.y.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) };
  }
  function cs(el, ps) {
    if (!el) return null;
    var c = getComputedStyle(el), o = {};
    ps.forEach(function (p) { o[p] = c[p]; });
    return o;
  }
  function rel(r, o) { return r ? { x: +(r.x - o.x).toFixed(2), y: +(r.y - o.y).toFixed(2), w: r.w, h: r.h } : null; }

  var page = document.querySelector('.r88-arch');
  var out = { ok: !!page, nav: [], slider: null };
  if (!page) {
    out.html = document.body.innerHTML.length;
    return JSON.stringify(out);
  }
  var O = page.getBoundingClientRect();
  out.origin = { x: +O.x.toFixed(2), y: +O.y.toFixed(2) };
  out.pageHost = R(document.querySelector('.r85-page-host'));
  out.mainInner = R(document.querySelector('main > div'));

  out.rel = {
    head: rel(R(page.querySelector('.r88-arch-head')), O),
    title: rel(R(page.querySelector('.r88-arch-title')), O),
    sub: rel(R(page.querySelector('.r88-arch-sub')), O),
    clear: rel(R(page.querySelector('.r88-arch-clear')), O),
    bar: rel(R(page.querySelector('.r88-arch-bar')), O),
    search: rel(R(page.querySelector('.r88-arch-search')), O),
    proj: rel(R(page.querySelector('.r88-arch-proj')), O),
    list: rel(R(page.querySelector('.r88-arch-list')), O),
    empty: rel(R(page.querySelector('.r88-arch-empty')), O)
  };
  out.clearCS = cs(page.querySelector('.r88-arch-clear'),
    ['width', 'height', 'padding', 'borderWidth', 'borderRadius', 'backgroundColor', 'color', 'fontSize', 'lineHeight']);
  out.searchCS = cs(page.querySelector('.r88-arch-search'),
    ['height', 'borderRadius', 'padding', 'borderColor', 'backgroundColor']);
  out.projCS = cs(page.querySelector('.r88-arch-proj .giencoder-select-view'),
    ['height', 'borderRadius', 'padding', 'borderColor']);

  var rows = [].slice.call(page.querySelectorAll('.r88-arch-row'));
  out.rows = rows.map(function (r) {
    var t = r.querySelector('.r88-arch-t'), m = r.querySelector('.r88-arch-m');
    var mic = r.querySelector('.r88-arch-mic'), mp = r.querySelector('.r88-arch-mproj');
    var dot = r.querySelector('.r88-arch-dot'), mu = r.querySelector('.r88-arch-mu'), mt = r.querySelector('.r88-arch-time');
    var acts = r.querySelector('.r88-arch-acts');
    return {
      box: rel(R(r), O),
      t: rel(R(t), O), m: rel(R(m), O),
      mic: rel(R(mic), O), mp: rel(R(mp), O), dot: rel(R(dot), O), mu: rel(R(mu), O), mt: rel(R(mt), O),
      acts: rel(R(acts), O),
      btn: [].slice.call(r.querySelectorAll('.r88-arch-act')).map(function (b) { return rel(R(b), O); }),
      line: R(r) && getComputedStyle(r, '::before').backgroundColor
    };
  });
  out.listCS = cs(page.querySelector('.r88-arch-list'), ['background', 'borderRadius', 'padding', 'outline', 'outlineOffset']);
  out.rowCS = cs(rows[0], ['padding', 'height', 'boxSizing']);
  out.tCS = cs(rows[0].querySelector('.r88-arch-t'), ['fontSize', 'lineHeight', 'color']);
  out.mCS = cs(rows[0].querySelector('.r88-arch-m'), ['fontSize', 'lineHeight', 'color', 'marginTop']);
  out.actCS = cs(rows[0].querySelector('.r88-arch-act'), ['width', 'height', 'borderColor', 'borderRadius', 'backgroundColor', 'color']);
  out.titleCS = cs(page.querySelector('.r88-arch-title'), ['fontSize', 'lineHeight', 'color', 'fontWeight']);
  out.subCS = cs(page.querySelector('.r88-arch-sub'), ['fontSize', 'lineHeight', 'color']);
  out.micCS = cs(rows[0].querySelector('.r88-arch-mic svg'), ['width', 'height']);
  out.emptyCS = cs(page.querySelector('.r88-arch-empty'), ['display']);
  out.bodyFS = getComputedStyle(document.documentElement).getPropertyValue('--ui-fs');

  // 每页导航项：hover 底色 vs 选中底色（r88 ①）
  var navis = [].slice.call(document.querySelectorAll('.r85-navi'));
  out.nav = navis.map(function (b) {
    return {
      tab: b.getAttribute('data-set-tab'),
      cur: b.getAttribute('aria-current'),
      bg: getComputedStyle(b).backgroundColor,
      ic: b.querySelector('svg') ? getComputedStyle(b.querySelector('svg')).color : null
    };
  });
  out.navHoverBg = getComputedStyle(document.querySelector('.r85-navi'), '')[0] ? null : null;
  var st = document.getElementById('r88-set-css');
  out.navHoverRule = /\.r85-navi:hover\{[^}]*\}/.exec(st ? st.textContent : '');

  return JSON.stringify(out);
})()
