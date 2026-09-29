(()=>{
  const b=document.querySelector('[data-av-chat-toggle]');
  b.click();
  return new Promise(r=>setTimeout(()=>{
    const svg=b.querySelector('svg');
    const cs=svg?getComputedStyle(svg):null;
    r({open:document.documentElement.hasAttribute('data-av-chat-open'),
       state:b.getAttribute('data-r74-state'), ariaExp:b.getAttribute('aria-expanded'),
       label:b.textContent.trim(), iconPaths:svg?[...svg.querySelectorAll('path')].map(p=>p.getAttribute('d')):[],
       anim:svg?svg.getAnimations().map(a=>({n:a.animationName,d:Math.round(a.currentTime)+'/'+a.effect.getTiming().duration})):null,
       origin:cs?cs.transformOrigin:null});
  }, 60));
})()
