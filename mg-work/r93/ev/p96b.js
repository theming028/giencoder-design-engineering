(function () {
  function r(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function c(el, p) { if (!el) return null; var s = getComputedStyle(el); return p.map(function (k) { return s[k]; }).join(' / '); }
  var o = {};

  // ① bubi
  var bubi = document.querySelector('.r93-bubi');
  o.bubi = { rect: r(bubi), maxH: getComputedStyle(bubi).maxHeight, ovY: getComputedStyle(bubi).overflowY };
  // 溢出取证：临时双倍内容
  var bak = bubi.innerHTML;
  bubi.innerHTML = bak + bak;
  o.bubiOverflow = { scrollHeight: bubi.scrollHeight, clientHeight: bubi.clientHeight, scrollable: bubi.scrollHeight > bubi.clientHeight };
  bubi.innerHTML = bak;
  o.bubiRestore = { scrollHeight: bubi.scrollHeight, clientHeight: bubi.clientHeight };

  // ② card 字号
  var cards = document.querySelectorAll('.r93-card');
  o.cardFS = getComputedStyle(cards[0]).fontSize;
  var noCls = [];
  Array.prototype.forEach.call(cards, function (cd) {
    Array.prototype.forEach.call(cd.querySelectorAll('*'), function (e) {
      if (!e.className && e.children.length === 0 && (e.textContent || '').trim()) {
        noCls.push({ tag: e.tagName, fs: getComputedStyle(e).fontSize, txt: e.textContent.trim().slice(0, 18) });
      }
    });
  });
  o.cardNoClassText = noCls.slice(0, 8);
  o.cardNoClassCount = noCls.length;

  // ③ quiz 区块
  o.quiz = [];
  document.querySelectorAll('.r93-t14').forEach(function (e) {
    var t = (e.textContent || '').trim();
    if (/^(你要把|这个 GienX|环境中已装|无视它|任务数据希望|未回答)/.test(t)) {
      o.quiz.push({ cls: e.className, color: getComputedStyle(e).color, fs: getComputedStyle(e).fontSize, txt: t.slice(0, 20) });
    }
  });

  // ④ edge 卡
  o.edges = Array.prototype.map.call(document.querySelectorAll('.r93-card--edge'), function (e) {
    return { rect: r(e), inlineW: e.style.width || '(none)', text: (e.textContent || '').trim().slice(0, 22) };
  });

  // ⑤ rateline
  var rl = document.querySelector('.r93-rateline');
  o.rateline = { rect: r(rl), gap: getComputedStyle(rl).gap };
  var kids = [];
  Array.prototype.forEach.call(rl.querySelectorAll('*'), function (k) {
    var b = k.getBoundingClientRect();
    var cs = getComputedStyle(k);
    kids.push({
      tag: k.tagName, cls: (k.className && k.className.baseVal !== undefined) ? 'svg' : (k.className || ''),
      x: Math.round(b.left), w: Math.round(b.width), h: Math.round(b.height),
      color: cs.color, fs: cs.fontSize, bg: cs.backgroundColor,
      txt: (k.textContent || '').trim().slice(0, 14)
    });
  });
  o.rateAll = kids;

  // 全页 .r93-t14 颜色分布
  var dist = {};
  document.querySelectorAll('.r93-t14').forEach(function (e) {
    var k = getComputedStyle(e).color + ' | ' + (e.className || '');
    dist[k] = (dist[k] || 0) + 1;
  });
  o.t14dist = dist;

  o.doc = [document.documentElement.scrollWidth, document.documentElement.clientWidth];
  return JSON.stringify(o);
})();
