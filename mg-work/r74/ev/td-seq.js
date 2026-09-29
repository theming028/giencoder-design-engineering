(()=>{
  const R=document.querySelector('.td-root');
  const g=s=>document.querySelector(s);
  const btn=()=>[...document.querySelectorAll('.td-right-bar button[aria-pressed]')].find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
  window.__A=[]; window.__B=[];
  function sample(store,ms){
    const t0=performance.now();
    const tick=()=>{
      const sl=g('.td-browse-slot'), ri=g('.td-right'), lf=g('.td-left'), pn=g('.td-browse');
      const cs=ri?getComputedStyle(ri):null;
      store.push({t:Math.round(performance.now()-t0), b:R.classList.contains('is-browse')?1:0,
        kl:R.classList.contains('is-keep-left')?1:0,
        slot:sl?+sl.getBoundingClientRect().width.toFixed(1):-1,
        left:lf?+lf.getBoundingClientRect().width.toFixed(1):-1,
        right:ri?+ri.getBoundingClientRect().width.toFixed(1):-1,
        rr:cs?cs.borderTopRightRadius:'', bw:cs?cs.borderRightWidth:'',
        pc:(pn&&pn.classList.contains('is-closing'))?'CLS':'-'});
      if(performance.now()-t0<ms) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
  const b1=btn(); b1.click(); sample(window.__A,700);
  setTimeout(()=>{ const b2=btn(); b2.click(); sample(window.__B,700); },1200);
  return 'seq:'+b1.getAttribute('aria-label');
})()
