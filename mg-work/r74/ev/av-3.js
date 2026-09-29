(()=>{
  const b=document.querySelector('[data-av-chat-toggle]');
  const glyph=document.querySelector('.av-main-avatar-face').firstElementChild;
  const cs=getComputedStyle(glyph);
  const an=glyph.getAnimations().map(a=>({n:a.animationName,ct:Math.round(a.currentTime),st:a.playState}));
  return {name:cs.animationName,dur:cs.animationDuration,origin:cs.transformOrigin,anims:an,
          glyphHTML:glyph.outerHTML.slice(0,60)};
})()
