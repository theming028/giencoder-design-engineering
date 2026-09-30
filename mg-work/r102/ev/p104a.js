(function(){
  function cs(el,p){ return el?getComputedStyle(el)[p]:null; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  function D(el){
    if(!el||!el.tagName) return null;
    return {tag:el.tagName.toLowerCase(), cls:cls(el).toString().slice(0,110), pos:cs(el,'position'), z:cs(el,'zIndex'),
            ov:cs(el,'overflow'), tf:cs(el,'transform'), op:cs(el,'opacity'), f:cs(el,'filter'),
            wc:cs(el,'willChange'), iso:cs(el,'isolation'), rect:R(el)};
  }
  var out={};
  var main=document.querySelector('main');
  out.mainChild=[]; if(main){ [].forEach.call(main.children,function(c){ out.mainChild.push(D(c)); }); }
  var inner=main?main.querySelector(':scope > div'):null;
  out.innerChild=[]; if(inner){ [].forEach.call(inner.children,function(c){ out.innerChild.push(D(c)); }); }
  var host=document.querySelector('.r93-conv-host');
  out.hostChain=[]; (function(e){ while(e&&e!==document.body.parentNode){ out.hostChain.push(D(e)); e=e.parentElement; } })(host);
  // 找 composer：含 textarea 的最近容器
  var ta=document.querySelector('textarea')||document.querySelector('[contenteditable="true"]');
  out.ta=D(ta);
  out.taChain=[]; (function(e){ var n=0; while(e&&n<12){ out.taChain.push(D(e)); e=e.parentElement; n++; } })(ta);
  // 可能的浮窗
  out.pops={};
  ['skills-popup-overlay','skills-popup','giencoder-select-popup','giencoder-dropdown-popup','giencoder-popup'].forEach(function(k){
    var els=document.querySelectorAll('.'+k);
    out.pops[k]={n:els.length, first:els[0]?D(els[0]):null};
  });
  // 页面里所有 fixed/absolute 且 z-index 数字的元素（取前 40）
  var all=document.querySelectorAll('body *'), tuned=[];
  [].forEach.call(all,function(e){ var c=getComputedStyle(e); if(c.position!=='static'&&c.zIndex!=='auto'){ tuned.push(D(e)); } });
  out.positioned=tuned.length;
  out.top=tuned.slice(0,60);
  return JSON.stringify(out,null,1);
})()
