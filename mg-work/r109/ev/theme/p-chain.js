(function () {
  /* 逐级上溯：对若干代表元素，从元素一路走到 <html>，读 DS 语义 token 的**当前解析值**，
     报出「值发生变化的层」⇒ 定位是谁把 token 改写回了浅色档。 */
  var TOK = ['--color-text-1', '--color-text-3', '--color-text-4',
             '--color-fill-1', '--color-bg-1', '--color-bg-2', '--color-border-1'];

  function read(el) {
    var cs = getComputedStyle(el), o = {};
    TOK.forEach(function (k) { o[k] = cs.getPropertyValue(k).trim(); });
    o.__color = cs.color;
    o.__bg = cs.backgroundColor;
    return o;
  }
  function desc(el) {
    var cls = (typeof el.className === 'string' ? el.className : '');
    return el.tagName.toLowerCase() + (cls ? '.' + cls.trim().split(/\s+/).slice(0, 3).join('.') : '');
  }

  var SELS = [
    '.r85-ic', '.r85-sl-tick.is-on', '.r85-sl-thumb', '.r85-sl-done',
    '.td-code-k', '.td-code-s', '.av-link', '.av-item-desc', '.av-line', '.av-row-sub',
    'svg', '.new-chat-btn'
  ];

  var out = [];
  SELS.forEach(function (sel) {
    var el;
    try { el = document.querySelector(sel); } catch (e) { el = null; }
    if (!el) { out.push({ sel: sel, found: false }); return; }
    var chain = [], cur = el, guard = 0, prev = null;
    while (cur && guard++ < 40) {
      var v = read(cur);
      var diff = [];
      if (prev) TOK.forEach(function (k) { if (v[k] !== prev[k]) diff.push(k); });
      chain.push({
        tag: cur.tagName.toLowerCase(), d: desc(cur), diff: diff,
        vals: v, inl: (cur.getAttribute('style') || '').slice(0, 150),
        sheetHit: null
      });
      prev = v;
      cur = cur.parentElement;
    }
    out.push({ sel: sel, found: true, chain: chain });
  });

  /* 另外：定位那个内联 color: rgb(30,30,30) 的元素 */
  var inl = null;
  var all = document.querySelectorAll('body *');
  for (var i = 0; i < all.length; i++) {
    var st = all[i].getAttribute('style') || '';
    if (st.indexOf('rgb(30, 30, 30)') >= 0) { inl = all[i]; break; }
  }
  var inlChain = null;
  if (inl) {
    inlChain = [];
    var c = inl, g = 0, pv = null;
    while (c && g++ < 40) {
      var vv = read(c);
      var dd = [];
      if (pv) TOK.forEach(function (k) { if (vv[k] !== pv[k]) dd.push(k); });
      inlChain.push({
        tag: c.tagName.toLowerCase(), d: desc(c), diff: dd, vals: vv,
        inl: (c.getAttribute('style') || '').slice(0, 200)
      });
      pv = vv; c = c.parentElement;
    }
  }

  var de = getComputedStyle(document.documentElement);
  return JSON.stringify({
    page: location.pathname.split('/').pop(),
    attr: document.documentElement.getAttribute('giencoder-theme'),
    html: read(document.documentElement),
    body: read(document.body),
    probes: out,
    inl30: inlChain
  });
})()
