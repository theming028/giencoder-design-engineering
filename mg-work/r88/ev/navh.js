(function(){
  var items=[].slice.call(document.querySelectorAll('.r85-navi'));
  var cs=function(b){return getComputedStyle(b).backgroundColor;};
  var r0=items[0].getBoundingClientRect();
  var root=document.documentElement;
  return JSON.stringify({
    x:+r0.x.toFixed(0), y:+(r0.y+r0.height/2).toFixed(0),
    unsel: items.map(function(b){return b.getAttribute('data-set-tab')+'='+cs(b);}),
    varNavi: getComputedStyle(root).getPropertyValue('--r88-navi-active').trim(),
    ruleHover: (function(){ var ss=document.getElementById('r88-set-css').textContent;
      var m=/\.r85-navi:hover\s*\{[^}]*\}/.exec(ss); return m?m[0]:null; })(),
    ruleCur: (function(){ var ss=document.getElementById('r88-set-css').textContent;
      var m=/\.r85-navi\[aria-current='true'\]\s*\{\s*background:[^;]*;/.exec(ss); return m?m[0]:null; })(),
    head: [].slice.call(document.styleSheets).map(function(s){return s.href||'(inline)';}).length
  });
})()
