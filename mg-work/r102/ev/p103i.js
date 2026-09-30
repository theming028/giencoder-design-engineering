(function(){
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function gv(el,p){ return el?getComputedStyle(el).getPropertyValue(p):null; }
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)}; }
  var out={theme:document.documentElement.getAttribute('giencoder-theme')||'(none)'};
  var tb=document.querySelector('.r93-tobottom'), bar=document.querySelector('.r93-bar');
  out.pill={bg:tb?cs(tb,'backgroundColor'):null, bf:tb?cs(tb,'backdropFilter'):null,
            v:gv(tb,'--r93-glass-pill'), vh:gv(tb,'--r93-glass-pill-h')};
  out.bar={bg:bar?cs(bar,'backgroundColor'):null, v:gv(bar,'--r93-glass')};
  var t14=document.querySelectorAll('.r93-t14'), hist={};
  [].forEach.call(t14,function(e){ var fs=cs(e,'fontSize'); hist[fs]=(hist[fs]||0)+1; });
  out.t14hist=hist;
  var seg=document.querySelector('.r93-seg');
  out.seg=seg?{h:Math.round(seg.getBoundingClientRect().height),top:cs(seg,'top')}:null;
  out.agentsEl=!!document.querySelector('.r93-agents');
  var bot=document.querySelector('.r93-bottom'); out.bottom=bot?R(bot):null;
  var hero=document.querySelector('main > div > div.flex-1.justify-center');
  out.hero=hero?{pos:cs(hero,'position'),z:cs(hero,'zIndex')}:null;
  var folds=document.querySelectorAll('.r93-fold');
  out.folds={n:folds.length,hasAnim:[].filter.call(folds,function(f){var fb=f.querySelector(':scope > .r93-fb');return fb&&cs(fb,'animationName')!=='none';}).length};
  return JSON.stringify(out,null,1);
})()
