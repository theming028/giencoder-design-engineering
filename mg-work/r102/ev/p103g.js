(function(){
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  var out={};
  /* ①② 字号 */
  var t14=document.querySelectorAll('.r93-t14'), hist={}, inC={}, outC={};
  [].forEach.call(t14,function(e){ var fs=cs(e,'fontSize'); hist[fs]=(hist[fs]||0)+1;
    var ic=!!e.closest('.r93-card'); (ic?inC:outC)[fs]=((ic?inC:outC)[fs]||0)+1; });
  out.t14={n:t14.length,hist:hist,inCard:inC,outCard:outC};
  var ell=document.querySelectorAll('.r93-t14.r93-ell');
  out.t14ell={n:ell.length,uniq:[...new Set([].map.call(ell,function(e){return cs(e,'fontSize');}))]};
  var c1=document.querySelectorAll('.r93-t14.r93-c1');
  out.t14c1={n:c1.length,uniq:[...new Set([].map.call(c1,function(e){return cs(e,'fontSize');}))]};
  /* 数字动效仍在 */
  out.num={n:document.querySelectorAll('.r93-num').length,
           anim:document.querySelector('.r93-num-i')?cs(document.querySelector('.r93-num-i'),'animationName')+cs(document.querySelector('.r93-num-i'),'animationDuration'):null};
  /* ③ 药丸 / 标题栏底色 */
  var tb=document.querySelector('.r93-tobottom'), bar=document.querySelector('.r93-bar');
  out.glass={pillBg:tb?cs(tb,'backgroundColor'):null,pillBf:tb?cs(tb,'backdropFilter'):null,
             pillVar:tb?cs(tb).getPropertyValue('--r93-glass-pill'):null,
             barBg:bar?cs(bar,'backgroundColor'):null, barVar:bar?cs(bar).getPropertyValue('--r93-glass'):null};
  /* ④ agents 行 */
  var ag=document.querySelector('.r93-agents'), cp=document.querySelector('.r93-cp'), bot=document.querySelector('.r93-bottom');
  out.agents={agentsEl:!!ag, cpEl:!!cp, bottomRect:bot?R(bot):null, bottomKids:bot?bot.children.length:0,
              bottomKidCls:bot?[].map.call(bot.children,function(k){return cls(k);}):null};
  /* ⑤ hero 层级 */
  var hero=document.querySelector("main > div > div.flex-1.justify-center");
  out.hero=hero?{pos:cs(hero,'position'),z:cs(hero,'zIndex'),rect:R(hero)}:null;
  var host=document.querySelector('.r93-conv-host');
  out.host=host?{pos:cs(host,'position'),z:cs(host,'zIndex'),rect:R(host)}:null;
  /* ⑥ 折叠 */
  var folds=document.querySelectorAll('.r93-fold');
  out.folds={n:folds.length,
    hasAnim:[].filter.call(folds,function(f){ var fb=f.querySelector(':scope > .r93-fb'); return fb && cs(fb,'animationName')!=='none'; }).length,
    fb1:cls(folds[0].querySelector(':scope > .r93-fb')),
    maxH:cs(folds[0].querySelector(':scope > .r93-fb')).maxHeight,
    trans:cs(folds[0].querySelector(':scope > .r93-fb')).transition.slice(0,200)};
  return JSON.stringify(out,null,1);
})()
