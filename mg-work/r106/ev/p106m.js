(function () {
  var L = [];
  function rd(sel) {
    var e = document.querySelector(sel);
    if (!e) return null;
    var r = e.getBoundingClientRect();
    return { x: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width) };
  }
  var on = !!document.querySelector('.av-browse-on');
  L.push('【' + window.innerWidth + 'x' + window.innerHeight + ' | 预览栏 ' + (on ? 'ON' : 'OFF') + '】');

  var wrap = rd('.r93-wrap'), bot = rd('.r93-bottom'), bub = rd('.r93-bub'), bubi = rd('.r93-bubi');
  L.push('  .r93-wrap   ' + JSON.stringify(wrap));
  L.push('  .r93-bottom ' + JSON.stringify(bot));
  L.push('  .r93-bub    ' + JSON.stringify(bub) +
    (bub && wrap ? '   -> 溢出 wrap 右缘 ' + (bub.r - wrap.r) + 'px' : ''));
  L.push('  .r93-bubi   ' + JSON.stringify(bubi));
  var eb = document.querySelector('.r93-bubi');
  if (eb) {
    var cs = getComputedStyle(eb);
    L.push('  .r93-bubi BG=' + cs.backgroundColor + ' computed.width=' + cs.width);
  }

  var hits = [], all = document.querySelectorAll('body *'), i;
  for (i = 0; i < all.length; i++) {
    var w = all[i].getBoundingClientRect().width;
    if (w >= 700 && w <= 760) {
      var cls = (all[i].className && all[i].className.toString) ? all[i].className.toString() : '';
      hits.push(all[i].tagName.toLowerCase() + (cls ? '.' + cls.split(/\s+/).slice(0, 2).join('.') : '') + '=' + Math.round(w));
      if (hits.length > 12) break;
    }
  }
  L.push('  宽 700~760 命中: ' + (hits.length ? hits.join(' | ') : '无'));

  // 命中 .r93-bub 且含 width 的声明（直接扫 <style> 文本，file:// 下最稳）
  var rules = [], sheets = document.querySelectorAll('style');
  for (var k = 0; k < sheets.length; k++) {
    var txt = (sheets[k].textContent || '').replace(/\/\*[\s\S]*?\*\//g, ' ');
    if (txt.indexOf('r93-bub') < 0) continue;
    var braces = txt.split('{');
    for (var j = 1; j < braces.length; j++) {
      var sel = braces[j - 1].split('}').pop();
      var body = braces[j].split('}')[0];
      if (sel.indexOf('r93-bub') < 0) continue;
      var m = /(^|;)\s*width\s*:\s*([^;]+)/.exec(body);
      if (m) rules.push(sel.trim().replace(/\s+/g, ' ') + ' { width:' + m[2].trim() + ' }');
    }
  }
  L.push('  .r93-bub 的 width 规则: ' + (rules.length ? rules.join('  ||  ') : '无'));
  return L.join('\n');
})()
