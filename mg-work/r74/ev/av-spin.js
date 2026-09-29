(()=>{const t=Number(window.__T||0);
 const svg=document.querySelector('[data-av-chat-toggle] svg');
 const as=svg.getAnimations(); as.forEach(a=>{try{a.pause();a.currentTime=t}catch(e){}});
 const cs=getComputedStyle(svg);
 return {t:t,n:as.length,name:as.map(a=>a.animationName).join(','),transform:cs.transform,origin:cs.transformOrigin};})()
