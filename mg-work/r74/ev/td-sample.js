(()=>{
  const R=document.querySelector('.td-root');
  const btns=[...document.querySelectorAll('.td-right-bar button[aria-pressed]')];
  const b=btns.find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
  if(!b) return 'NOBTN:'+btns.map(x=>x.getAttribute('aria-label')).join('|');
  const g=s=>document.querySelector(s);
  window.__S=[]; const t0=performance.now();
  const tick=()=>{
    const sl=g('.td-browse-slot'), ri=g('.td-right'), lf=g('.td-left'), pn=g('.td-browse');
    const cs=ri?getComputedStyle(ri):null;
    window.__S.push({t:Math.round(performance.now()-t0),
      b:R.classList.contains('is-browse')?1:0,
      kl:R.classList.contains('is-keep-left')?1:0,
      slot:sl?+sl.getBoundingClientRect().width.toFixed(1):-1,
      left:lf?+lf.getBoundingClientRect().width.toFixed(1):-1,
      right:ri?+ri.getBoundingClientRect().width.toFixed(1):-1,
      rr:cs?cs.borderTopRightRadius:'', bw:cs?cs.borderRightWidth:'',
      pc:(pn&&pn.classList.contains('is-closing'))?'CLS':'-'});
    if(performance.now()-t0<700) requestAnimationFrame(tick);
  };
  b.click(); requestAnimationFrame(tick);
  return 'clicked:'+b.getAttribute('aria-label')+' browse='+(R.classList.contains('is-browse')?1:0);
})()
