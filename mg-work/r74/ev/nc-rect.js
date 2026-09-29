(()=>{const b=[...document.querySelectorAll('button')].find(x=>(x.textContent||'').indexOf('新会话')>=0&&x.getBoundingClientRect().width>40);
 if(!b) return 'NONE';
 const r=b.getBoundingClientRect(); const cs=getComputedStyle(b);
 return {file:location.pathname.split('/').pop(),x:r.left,y:r.top,w:r.width,h:r.height,
  fs:cs.fontSize,bg:cs.backgroundColor,bd:cs.borderTopWidth+' '+cs.borderTopColor,sh:cs.boxShadow,
  after:(()=>{const a=getComputedStyle(b,'::after');return a.content+'|'+a.fontSize+'|'+a.right+'|'+a.color})(),
  before:(()=>{const a=getComputedStyle(b,'::before');return a.width+'x'+a.height+'|'+a.marginRight})()};})()
