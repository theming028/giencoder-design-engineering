(()=>{
  const m=document.querySelector('main.dot-bg'); if(!m) return 'NOMAIN';
  const r=m.getBoundingClientRect();
  const x=r.left+120, y=r.top+r.height-140;
  m.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:x,clientY:y,pointerId:1,isPrimary:true}));
  return new Promise(res=>requestAnimationFrame(()=>{
    const el=document.querySelector('.r74-ripple');
    if(!el) return res('NOELEM');
    const as=el.getAnimations(); as.forEach(a=>{try{a.pause()}catch(e){}});
    window.__RF=t=>{as.forEach(a=>{try{a.currentTime=t}catch(e){}});
      const cs=getComputedStyle(el);
      return {t:t,r:cs.getPropertyValue('--r74-rip-r'),cap:cs.getPropertyValue('--r74-rip-cap'),
              op:cs.opacity,x:cs.getPropertyValue('--r74-rip-x'),y:cs.getPropertyValue('--r74-rip-y'),
              dur:as.map(a=>a.effect.getTiming().duration).join(','),n:as.length};};
    res({pt:[Math.round(x),Math.round(y)],main:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],n:as.length});
  }));
})()
