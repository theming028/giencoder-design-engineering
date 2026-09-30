(function(){
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  var out = {};

  var bot = document.querySelector('.r93-bottom');
  var host = document.querySelector('.r93-conv-host');
  out.hostRect = host?R(host):null;
  out.bottomRect = bot?R(bot):null;

  /* hero（外壳 React 的居中容器） */
  var hero = document.querySelector("main > div > div.flex-1.justify-center");
  out.hero = hero ? { rect:R(hero), display:cs(hero,'display'), flex:cs(hero,'flex'), justify:cs(hero,'justifyContent'), align:cs(hero,'alignItems'),
                      pad:cs(hero,'padding'), ov:cs(hero,'overflow'), mt:cs(hero,'marginTop'), mb:cs(hero,'marginBottom') } : null;

  function chain(el, stopAt){
    var arr=[], n=el;
    while(n && n!==document.documentElement){
      arr.push({ t:n.tagName, c:cls(n).slice(0,70), r:R(n), ov:cs(n,'overflow'), pad:cs(n,'padding'), mar:cs(n,'margin'),
                 br:cs(n,'borderRadius'), sh:cs(n,'boxShadow').slice(0,80), pos:cs(n,'position') });
      if(n===stopAt) break;
      n=n.parentElement;
    }
    return arr;
  }

  var ce = document.querySelector('[contenteditable]');
  out.ce = ce ? { rect:R(ce), cls:cls(ce).slice(0,120), chain: chain(ce, document.body) } : null;

  /* 找 composer 的根（含 focus ring 的那个盒）：从 contenteditable 往上找第一个带 box-shadow 或 border 的容器 */
  if(ce){
    var n=ce, found=[];
    while(n && n!==document.body){
      var c=getComputedStyle(n);
      if(c.boxShadow!=='none' || c.borderTopWidth!=='0px'){
        found.push({t:n.tagName, c:cls(n).slice(0,90), r:R(n), sh:c.boxShadow, bd:c.borderTopWidth+' '+c.borderTopColor, br:c.borderRadius});
      }
      n=n.parentElement;
    }
    out.ceRings = found;
  }

  /* 空隙：.r93-bottom 底 → composer 外框顶 */
  if(bot && ce){
    var wrap = ce.closest('div.mt-8') || ce.parentElement;
    out.gap = { bottomB: R(bot).b, wrapTop: R(wrap).y, wrapCls: cls(wrap).slice(0,90), gap: R(wrap).y - R(bot).b };
  }

  return JSON.stringify(out, null, 1);
})()
