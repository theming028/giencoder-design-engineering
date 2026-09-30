(function(){
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  var out={open:[], scs:[]};
  var all=document.querySelectorAll('body *');
  [].forEach.call(all,function(e){
    var c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden') return;
    var isPop = e.className && /popup|dropdown|menu|overlay/i.test(cls(e).toString());
    if(isPop && (parseFloat(c.zIndex)||0) >= 5){
      out.open.push({cls:cls(e).toString().slice(0,80), z:c.zIndex, op:c.opacity, rect:R(e)});
    }
    // 检测会创建层叠上下文的祖先（针对 composer 区域内的浮层）
  });
  // composer 内所有 popup 的祖先链
  var ps=document.querySelectorAll('.giencoder-select-popup, .skills-popup-overlay, [class*="dropdown-popup"]');
  out.chains=[];
  [].forEach.call(ps,function(p){
    var c=getComputedStyle(p);
    if(c.display==='none') return;
    var chain=[], e=p, n=0;
    while(e&&e!==document.documentElement&&n<10){
      var cc=getComputedStyle(e);
      chain.push({tag:e.tagName.toLowerCase(), cls:cls(e).toString().slice(0,70), pos:cc.position, z:cc.zIndex, ov:cc.overflow,
                  tf:cc.transform==='none'?'':cc.transform.slice(0,20), op:cc.opacity, f:cc.filter==='none'?'':'F', wc:cc.willChange});
      e=e.parentElement; n++;
    }
    out.chains.push({self:cls(p).toString().slice(0,50), z:c.zIndex, op:c.opacity, rect:R(p), chain:chain});
  });
  return JSON.stringify(out,null,1);
})()
