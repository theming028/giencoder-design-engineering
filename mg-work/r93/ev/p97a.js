(function () {
  function r(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(el, p) { if (!el) return null; var s = getComputedStyle(el); return p.map(function (k) { return s[k]; }).join(' / '); }
  var o = {};

  /* ---------- A. .r93-card 内所有文本的字号分布 ---------- */
  var dist = {};
  document.querySelectorAll('.r93-card').forEach(function (cd) {
    Array.prototype.forEach.call(cd.querySelectorAll('*'), function (e) {
      var hasText = false;
      Array.prototype.forEach.call(e.childNodes, function (n) { if (n.nodeType === 3 && n.textContent.trim()) hasText = true; });
      if (!hasText) return;
      var fs = getComputedStyle(e).fontSize;
      var key = fs + ' | ' + (e.tagName.toLowerCase()) + '.' + (e.className || '(anon)');
      if (!dist[key]) dist[key] = { n: 0, sample: '' };
      dist[key].n++;
      if (!dist[key].sample) dist[key].sample = e.textContent.trim().slice(0, 22);
    });
  });
  o.cardFontDist = dist;

  /* ---------- B. 卡片清单 + 字号 ---------- */
  o.cards = Array.prototype.map.call(document.querySelectorAll('.r93-card, .r93-todocard, .r93-diff, .r93-artcard'), function (e, i) {
    return { i: i, cls: e.className, rect: r(e), fs: getComputedStyle(e).fontSize };
  });

  /* ---------- C. 滚动到底部按钮 ---------- */
  var tb = document.querySelector('.r93-tobottom');
  if (tb) {
    o.tobottom = {
      rect: r(tb),
      radius: getComputedStyle(tb).borderTopLeftRadius,
      bg: getComputedStyle(tb).backgroundColor,
      border: getComputedStyle(tb).borderTopWidth + ' ' + getComputedStyle(tb).borderTopColor,
      shadow: getComputedStyle(tb).boxShadow,
      self: getComputedStyle(tb).color,
      pad: getComputedStyle(tb).paddingLeft + '/' + getComputedStyle(tb).paddingTop
    };
    o.tobottomKids = Array.prototype.map.call(tb.querySelectorAll('*'), function (k) {
      return { tag: k.tagName, cls: (k.className.baseVal !== undefined) ? 'svg' : (k.className || ''), color: getComputedStyle(k).color, fs: getComputedStyle(k).fontSize, txt: (k.textContent || '').trim() };
    });
  }

  /* ---------- D. 横向：内容块 vs 底部 vs composer ---------- */
  var sel = {
    wrap: '.r93-wrap', bottom: '.r93-bottom', sb: '.r93-sb', cp: '.r93-cp', agents: '.r93-agents',
    card1: '.r93-card', todocard: '.r93-todocard', note: '.r93-note', alert: '.r93-alert',
    diff: '.r93-diff', arts: '.r93-arts', artcard: '.r93-artcard', rateline: '.r93-rateline',
    bub: '.r93-bub'
  };
  o.horiz = {};
  Object.keys(sel).forEach(function (k) { o.horiz[k] = r(document.querySelector(sel[k])); });

  var mt8 = document.querySelector('main > div > div.flex-1.justify-center > div.mt-8');
  if (mt8) {
    o.mt8 = { cls: mt8.className, rect: r(mt8), kids: mt8.children.length, display: getComputedStyle(mt8).display, dir: getComputedStyle(mt8).flexDirection, gap: getComputedStyle(mt8).gap };
    o.mt8kid = Array.prototype.map.call(mt8.children, function (c) { return { tag: c.tagName, cls: c.className, rect: r(c) }; });
    var outer = mt8.firstElementChild;
    o.composerOuter = { rect: r(outer), bg: getComputedStyle(outer).backgroundColor, pad: getComputedStyle(outer).padding };
    var card = outer && outer.querySelector('div.relative, [class*="rounded-\\[16px\\]"]');
    o.composerCard = card ? { cls: card.className, rect: r(card), bg: getComputedStyle(card).backgroundColor } : null;
    /* 卡内所有直接子块 */
    if (card) {
      o.composerCardKids = Array.prototype.map.call(card.children, function (c) { return { tag: c.tagName, cls: c.className, rect: r(c) }; });
    }
  }

  /* ---------- E. 底部 meta 行是否存在 ---------- */
  var html = document.documentElement.innerHTML;
  o.hasMeta = html.indexOf('缓存命中') >= 0;
  o.hasTok = html.indexOf('tok/s') >= 0;
  o.hasRounds = html.indexOf('轮 ·') >= 0;
  /* 底部最后几个元素 */
  var main = document.querySelector('main');
  var inner = main && main.querySelector(':scope > div');
  if (inner) {
    o.innerKids = Array.prototype.map.call(inner.children, function (c) {
      return { tag: c.tagName, cls: (c.className || '').slice(0, 90), rect: r(c), txt: (c.textContent || '').trim().slice(0, 30) };
    });
  }

  o.doc = [document.documentElement.scrollWidth, document.documentElement.clientWidth, document.documentElement.scrollHeight, window.innerHeight];
  return JSON.stringify(o);
})();
