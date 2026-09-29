(()=>{const t=Number(window.__T||0);
 const g=document.querySelector('.av-main-avatar-face').firstElementChild;
 const as=g.getAnimations(); as.forEach(a=>{try{a.pause();a.currentTime=t}catch(e){}});
 return {n:as.length, t:t, name:as.map(a=>a.animationName).join(','), ct:as.map(a=>Math.round(a.currentTime)).join(',')};})()
