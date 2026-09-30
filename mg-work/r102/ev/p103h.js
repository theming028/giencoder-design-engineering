(function(){
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function gv(el,p){ return el?getComputedStyle(el).getPropertyValue(p):null; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  var out={};
  var t14=document.querySelectorAll('.r93-t14'), hist={}, inC={}, outC={};
  [].forEach.call(t14,function(e){ var fs=cs(e,'fontSize'); hist[fs]=(hist[fs]||0)+1;
    var ic=!!e.closest('.r93-card'); (ic?inC:outC)[fs]=((ic?inC:outC)[fs]||0)+1; });
  out.t14={n:t14.length,hist:hist,inCard:inC,outCard:outC};
  var ell=document.querySelectorAll('.r93-t14.r93-ell');
  out.t14ell={n:ell.length,uniq:Array.from(new Set([].map.call(ell,function(e){return cs(e,'fontSize');})))};
  var c1=document.querySelectorAll('.r93-t14.r93-c1');
  out.t14c1={n:c1.length,uniq:Array.from(new Set([].map.call(c1,function(e){return cs(e,'fontSize');})))};
  out.num={n:document.querySelectorAll('.r93-num').length,
           anim:(function(){var n=document.querySelector('.r93-num-i');return n?cs(n,'animationName')+' '+cs(n,'animationDuration'):null;})()};
  var tb=document.querySelector('.r93-tobottom'), bar=document.querySelector('.r93-bar');
  out.glass={pillBg:tb?cs(tb,'backgroundColor'):null, pillBf:tb?cs(tb,'backdropFilter'):null,
             pillVar:gv(tb,'--r93-glass-pill'), pillHVar:gv(tb,'--r93-glass-pill-h'),
             barBg:bar?cs(bar,'backgroundColor'):null, barVar:gv(bar,'--r93-glass')};
  var ag=document.querySelector('.r93-agents'), cp=document.querySelector('.r93-cp'), bot=document.querySelector('.r93-bottom');
  out.agents={agentsEl:!!ag, cpEl:!!cp, bottomRect:bot?R(bot):null, bottomKids:bot?bot.children.length:0,
              kidCls:bot?[].map.call(bot.children,function(k){return cls(k);}):null};
  var hero=document.querySelector("main > div > div.flex-1.justify-center");
  var host=document.querySelector('.r93-conv-host');
  out.hero=hero?{pos:cs(hero,'position'),z:cs(hero,'zIndex'),rect:R(hero)}:null;
  out.host=host?{pos:cs(host,'position'),z:cs(host,'zIndex'),rect:R(host)}:null;
  var folds=document.querySelectorAll('.r93-fold');
  out.folds={n:folds.length,
    hasAnim:[].filter.call(folds,function(f){ var fb=f.querySelector(':scope > .r93-fb'); return fb && cs(fb,'animationName')!=='none'; }).length,
    fb0Cls:cls(folds[0].querySelector(':scope > .r93-fb')),
    maxH:cs(folds[0].querySelector(':scope > .r93-fb'),'maxHeight'),
    trans:cs(folds[0].querySelector(':scope > .r93-fb'),'transition')};
  return JSON.stringify(out,null,1);
})()
