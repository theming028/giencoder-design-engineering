(function(){
  var s=document.querySelector('.r88-arch-proj');
  var view=s.querySelector('.giencoder-select-view');
  var pre=s.querySelector('.r88-sel-prefix');
  var svg=pre.querySelector('svg');
  var txt=s.querySelector('.giencoder-select-view-text');
  var suf=s.querySelector('.giencoder-select-suffix');
  var R=function(e){var r=e.getBoundingClientRect();return {x:+r.x.toFixed(2),w:+r.width.toFixed(2)};};
  var cs=function(e,ps){var c=getComputedStyle(e),o={};ps.forEach(function(p){o[p]=c[p]});return o;};
  return JSON.stringify({
    view:R(view), viewCS:cs(view,['padding','gap','borderLeftWidth','columnGap','fontSize']),
    pre:R(pre), preCS:cs(pre,['marginRight','marginLeft','width','display','gap']),
    svg:R(svg),
    txt:R(txt), txtCS:cs(txt,['marginLeft','marginRight','padding','fontSize']),
    suf:R(suf), sufCS:cs(suf,['marginLeft','marginRight'])
  });
})()
