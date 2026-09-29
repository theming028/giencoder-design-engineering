(()=>{
  const g=document.querySelector('.av-main-avatar-face').firstElementChild;
  const cs=getComputedStyle(g);
  const an=g.getAnimations().map(a=>({n:a.animationName,ct:Math.round(a.currentTime),st:a.playState}));
  return {name:cs.animationName,dur:cs.animationDuration,origin:cs.transformOrigin,anims:an};
})()
