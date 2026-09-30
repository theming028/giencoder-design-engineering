(function () {
  function r(el) {
    if (!el) return null;
    var b = el.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)];
  }
  function cs(el, props) {
    if (!el) return null;
    var c = getComputedStyle(el), o = {};
    props.forEach(function (p) { o[p] = c[p]; });
    return o;
  }
  var out = {};

  // ① r93-bubi
  var bubi = document.querySelector('.r93-bubi');
  out.bubi = { rect: r(bubi), cs: cs(bubi, ['maxHeight', 'overflowY', 'overflow']) };

  // ② r93-card 内文本字号
  var cards = document.querySelectorAll('.r93-card');
  out.cardCount = cards.length;
  var fonts = {};
  Array.prototype.forEach.call(cards, function (c, i) {
    var t = (c.textContent || '').trim().slice(0, 22);
    fonts['card' + i + ' <' + t + '>'] = getComputedStyle(c).fontSize;
    // 直接子文本节点若有无类名的 span，取其字号
  });
  out.cardFonts = fonts;

  // 无类名字号的采样：遍历 card 内所有 span，统计 font-size 分布
  var dist = {};
  Array.prototype.forEach.call(cards, function (c) {
    Array.prototype.forEach.call(c.querySelectorAll('span,div,a'), function (s) {
      var f = getComputedStyle(s).fontSize;
      var cls = s.className || '(none)';
      dist[f] = dist[f] || {};
      dist[f][cls] = (dist[f][cls] || 0) + 1;
    });
  });
  out.cardFontDist = dist;

  // ③ r93-card--edge 宽度
  var edges = document.querySelectorAll('.r93-card--edge');
  out.edgeCount = edges.length;
  out.edges = Array.prototype.map.call(edges, function (e, i) {
    return {
      i: i,
      rect: r(e),
      inlineW: e.style.width || '',
      csW: getComputedStyle(e).width,
      text: (e.textContent || '').trim().slice(0, 26),
      parent: e.parentElement ? (e.parentElement.className || '') : ''
    };
  });

  // ④ r93-rateline
  var rl = document.querySelector('.r93-rateline');
  out.rateline = { rect: r(rl), cs: cs(rl, ['gap', 'alignItems']) };
  if (rl) {
    out.rateKids = Array.prototype.map.call(rl.children, function (k) {
      return {
        cls: k.className || k.tagName,
        rect: r(k),
        color: getComputedStyle(k).color,
        fs: getComputedStyle(k).fontSize,
        text: (k.textContent || '').trim().slice(0, 20)
      };
    });
    // 深一层
    var deep = [];
    Array.prototype.forEach.call(rl.querySelectorAll('*'), function (k) {
      var t = (k.textContent || '').trim();
      if (k.children.length === 0 || k.tagName === 'svg') {
        deep.push({
          tag: k.tagName, cls: (k.className && k.className.baseVal !== undefined) ? ('svg:' + k.className.baseVal) : (k.className || ''),
          rect: r(k), color: getComputedStyle(k).color, fs: getComputedStyle(k).fontSize,
          txt: t.slice(0, 16)
        });
      }
    });
    out.rateDeep = deep;
  }

  // ⑤ 需求采访区块
  var quiz = [];
  document.querySelectorAll('.r93-t14').forEach(function (e) {
    var t = (e.textContent || '').trim();
    if (t.indexOf('你要把') === 0 || t.indexOf('这个 GienX') === 0 || t.indexOf('环境中已装') === 0
      || t.indexOf('无视它') === 0 || t.indexOf('任务数据希望') === 0 || t.indexOf('未回答') === 0) {
      quiz.push({ cls: e.className, color: getComputedStyle(e).color, fs: getComputedStyle(e).fontSize, txt: t.slice(0, 26) });
    }
  });
  out.quiz = quiz;

  // ⑥ 全页 .r93-t14 的颜色分布（评估全局改色影响面）
  var t14 = {};
  document.querySelectorAll('.r93-t14').forEach(function (e) {
    var c = getComputedStyle(e).color;
    var key = c + ' | ' + (e.className || '');
    t14[key] = (t14[key] || 0) + 1;
  });
  out.t14dist = t14;

  // ⑦ 内联 840 宽文本块
  out.inline840 = Array.prototype.map.call(document.querySelectorAll('.r93-wrap [style*="width:840px"], .r93-wrap [style*="width: 840px"]'), function (e) {
    return { cls: e.className, rect: r(e), text: (e.textContent || '').slice(0, 24) };
  });

  // ⑧ wrap / main
  out.wrap = r(document.querySelector('.r93-wrap'));
  out.main = r(document.querySelector('main'));

  return JSON.stringify(out);
})();
