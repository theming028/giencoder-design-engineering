(function(){
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  var out={};
  var cands = document.querySelectorAll('textarea, input, [contenteditable="true"], [contenteditable=""], [contenteditable=plaintext-only], [role="textbox"]');
  out.n = cands.length;
  out.list = [].map.call(cands, function(e){ return {t:e.tagName, c:cls(e).slice(0,80), ce:e.getAttribute('contenteditable'), ph:e.getAttribute('placeholder'), r:R(e)}; });
  /* 找 placeholder 文本所属 */
  var all = document.querySelectorAll('div,p,span');
  var hit=[];
  [].forEach.call(all, function(e){
    if(e.children.length===0 && (e.textContent||'').indexOf('描述你的任务')>=0){ hit.push({c:cls(e).slice(0,80), r:R(e), txt:(e.textContent||'').slice(0,30)}); }
  });
  out.ph = hit;
  /* 从命中点往上找 composer 根：找带 border-radius>=8 且 width>600 的祖先 */
  if(hit.length){
    var n=hit[0] ? document.querySelectorAll('div,p,span') : null;
    var e=null;
    [].forEach.call(all, function(x){ if(!e && x.children.length===0 && (x.textContent||'').indexOf('描述你的任务')>=0) e=x; });
    var arr=[], k=e;
    while(k && k!==document.body){
      var c=getComputedStyle(k);
      arr.push({t:k.tagName,c:cls(k).slice(0,80),r:R(k),ov:c.overflow,sh:c.boxShadow.slice(0,90),bd:c.borderTopWidth+' '+c.borderTopColor,br:c.borderRadius,bg:c.backgroundColor});
      k=k.parentElement;
    }
    out.chain = arr;
  }
  return JSON.stringify(out,null,1);
})()
