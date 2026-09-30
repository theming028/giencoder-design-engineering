(function(){
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ if(!el) return null; var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  function D(el){ if(!el) return null; var c=getComputedStyle(el); return {cls:cls(el).toString().slice(0,70),pos:c.position,z:c.zIndex,disp:c.display,ov:c.overflow,rect:R(el)}; }
  var out={};
  var host=document.querySelector('.r93-conv-host');
  out.host=D(host);
  out.hostKids=[]; [].forEach.call(host.children,function(k){ out.hostKids.push(D(k)); });
  out.panes=[]; [].forEach.call(document.querySelectorAll('.r93-pane'),function(p){ var o=D(p); o.hidden=p.hidden; out.panes.push(o); });
  out.hero=D(document.querySelector('main > div > div.flex-1.justify-center'));
  out.box=D(document.querySelector('main > div > div.flex-1.justify-center > div.mt-8'));
  out.bottom=D(document.querySelector('.r93-bottom'));
  var sk=document.querySelector('.r93-sk'); out.sk=D(sk);
  return JSON.stringify(out,null,1);
})()
