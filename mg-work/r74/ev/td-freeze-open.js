(()=>{
  const btn=[...document.querySelectorAll('.td-right-bar button[aria-pressed]')].find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
  btn.click();
  return new Promise(res=>requestAnimationFrame(()=>requestAnimationFrame(()=>{
    const as=document.getAnimations();
    as.forEach(a=>{try{a.pause()}catch(e){}});
    window.__F=t=>as.map(a=>{try{a.currentTime=t}catch(e){return 'ERR'}}).length;
    window.__N=as.map(a=>(a.animationName||a.transitionProperty)+'@'+Math.round(a.effect.getTiming().duration));
    res({n:as.length, names:window.__N});
  })));
})()
