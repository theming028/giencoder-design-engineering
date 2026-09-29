(()=>{
  const btn=[...document.querySelectorAll('.td-right-bar button[aria-pressed]')].find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
  btn.click();                                   /* 开 */
  return new Promise(res=>setTimeout(()=>{
    const b2=[...document.querySelectorAll('.td-right-bar button[aria-pressed]')].find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
    b2.click();                                  /* 关 */
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      const as=document.getAnimations();
      as.forEach(a=>{try{a.pause()}catch(e){}});
      window.__F=t=>{let n=0;as.forEach(a=>{try{a.currentTime=t;n++}catch(e){}});return n};
      res({n:as.length,names:as.map(a=>(a.animationName||a.transitionProperty)+'@'+Math.round(a.effect.getTiming().duration))});
    }));
  },700));
})()
