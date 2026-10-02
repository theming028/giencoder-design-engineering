// r109 第十拍 · 描边令牌双档实测
window.__btok = function () {
  var de = document.documentElement;
  var cs = getComputedStyle(de);
  function g(n) { return (cs.getPropertyValue(n) || '').trim(); }
  var out = {
    theme: de.getAttribute('giencoder-theme') || '(none)',
    bodyTheme: (document.body && document.body.getAttribute('giencoder-theme')) || '(none)',
    hasBlock: !!document.getElementById('r109-border-css')
  };
  var all = document.querySelectorAll('style');
  out.styleCount = all.length;
  out.blockIdx = -1;
  for (var i = 0; i < all.length; i++) {
    if (all[i].id === 'r109-border-css') out.blockIdx = i;
  }
  var names = ['--gray-1', '--gray-2', '--gray-3', '--gray-4',
               '--color-border-1', '--color-border-2', '--color-border-3',
               '--color-bg-1'];
  out.v = {};
  for (var k = 0; k < names.length; k++) out.v[names[k]] = g(names[k]);

  // 真实元素实测：第一个「有描边且颜色非透明」的元素
  var cands = document.querySelectorAll('[class*="border"]');
  out.sample = null;
  for (var j = 0; j < cands.length && !out.sample; j++) {
    var e = cands[j];
    var st = getComputedStyle(e);
    var bc = st.borderTopColor, bw = st.borderTopWidth;
    if (bw && bw !== '0px' && bc && bc !== 'rgba(0, 0, 0, 0)' && bc !== 'transparent') {
      out.sample = { cls: String(e.className || '').slice(0, 50), bc: bc, bw: bw };
    }
  }
  return out;
};
window.__btok
