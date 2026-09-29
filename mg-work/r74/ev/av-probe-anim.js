(()=>{
  const st=document.createElement('style'); st.id='r74-probe';
  /* 与页面规则同一条关键帧、同一条曲线，只是换成常驻选择器 + 6000ms 便于冻结取帧 */
  st.textContent='.r74-face-glyph{transform-origin:50% 78% !important;'
   +'animation:r74-face-wiggle 6000ms cubic-bezier(0.36,0.07,0.19,0.97) 1 !important}';
  document.head.appendChild(st);
  return new Promise(r=>requestAnimationFrame(()=>{
    const g=document.querySelector('.av-main-avatar-face').firstElementChild;
    const as=g.getAnimations(); as.forEach(a=>a.pause());
    window.__G={g:g,as:as};
    window.__P=p=>{const t=p*60; as.forEach(a=>{a.currentTime=t});
      const b=g.getBoundingClientRect();
      return {p:p, h:+b.height.toFixed(2), w:+b.width.toFixed(2),
              frames:as[0].effect.getKeyframes().map(f=>f.offset+':'+(f.rotate||f.transform)).join(' ')};};
    r({n:as.length,name:getComputedStyle(g).animationName,
       frames:as[0].effect.getKeyframes().map(f=>({o:f.offset,rot:f.rotate,tr:f.transform}))});
  }));
})()
