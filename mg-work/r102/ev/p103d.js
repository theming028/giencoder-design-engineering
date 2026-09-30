(function(){
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  var ta = document.querySelector('textarea');
  if(!ta) return 'no ta';
  var out={ta:R(ta), chain:[]};
  var n=ta;
  while(n && n!==document.body){
    var c=getComputedStyle(n);
    out.chain.push({
      t:n.tagName, c:cls(n).slice(0,110), r:R(n),
      ov:c.overflow, sh:c.boxShadow.slice(0,120), ol:c.outline,
      bt:c.borderTopWidth+' '+c.borderTopColor, br:c.borderRadius,
      bg:c.backgroundColor, pad:c.padding, mar:c.margin, pos:c.position, z:c.zIndex
    });
    n=n.parentElement;
  }
  return JSON.stringify(out,null,1);
})()
