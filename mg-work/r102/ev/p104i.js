(function(){
  var cs=function(e,p){ return e?getComputedStyle(e)[p]:null; };
  var gv=function(e,p){ return e?getComputedStyle(e).getPropertyValue(p).trim():null; };
  var root=document.documentElement;
  var out={theme:root.getAttribute('giencoder-theme')};
  var v=function(n){ return getComputedStyle(root).getPropertyValue(n).trim(); };
  ['--r93-ok','--r93-ioc','--r93-ioc2','--r93-warn-ic','--r93-tag-ic','--r93-dim','--r93-meta','--r93-sh','--r93-sbsh','--r93-glass','--r93-glass-pill'].forEach(function(n){ out[n]=v(n); });
  out.agentsCSS=(function(){ var t=0; for(var i=0;i<document.styleSheets.length;i++){ try{ var r=document.styleSheets[i].cssRules; for(var j=0;j<r.length;j++){ if(r[j].selectorText && /r93-agent|r93-cp\b/.test(r[j].selectorText)) t++; } }catch(e){} } return t; })();
  var sb=document.querySelector('.r93-sb'), tb=document.querySelector('.r93-tobottom'), pop=document.querySelector('.r93-pop');
  out.sbShadow=cs(sb,'boxShadow'); out.tbShadow=cs(tb,'boxShadow'); out.popShadow=cs(pop,'boxShadow');
  out.folds=document.querySelectorAll('.r93-fold').length;
  out.open1=document.querySelectorAll('.r93-fold[data-r93-open="1"]').length;
  out.open0=document.querySelectorAll('.r93-fold[data-r93-open="0"]').length;
  return JSON.stringify(out,null,1);
})()
