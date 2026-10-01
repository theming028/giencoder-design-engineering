(function () {
  var out = {};
  var pre = document.querySelector('.r93-pre');
  out.preExists = !!pre;
  if (pre) {
    out.preFont = getComputedStyle(pre).fontFamily;
    var chain = [], n = pre;
    while (n && n.tagName !== 'HTML') {
      chain.push(n.tagName + '.' + (typeof n.className === 'string' ? n.className.split(' ')[0] : '') + ' => ' + getComputedStyle(n).fontFamily.slice(0, 40));
      n = n.parentElement;
    }
    out.chain = chain;
    out.preTxt = (pre.textContent || '').slice(0, 30);
  }
  out.bodyFont = getComputedStyle(document.body).fontFamily;
  out.htmlFont = getComputedStyle(document.documentElement).fontFamily;
  out.rootVar = getComputedStyle(document.documentElement).getPropertyValue('--font-family');
  // 统计页面上 .r93-pre 的数量与各自字体（验证「全部同族」）
  var ps = document.querySelectorAll('.r93-pre');
  out.preCount = ps.length;
  var fams = {};
  ps.forEach(function (e) { var f = getComputedStyle(e).fontFamily.slice(0, 30); fams[f] = (fams[f] || 0) + 1; });
  out.preFams = fams;
  return JSON.stringify(out);
})()
