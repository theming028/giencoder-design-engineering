(()=>{
  const st=document.createElement('style'); st.id='r74-slomo';
  st.textContent=
    '.td-root.is-browse.is-keep-left .td-left{animation-duration:4000ms !important}'+
    '.td-browse-slot{transition-duration:4000ms !important}'+
    '.td-right{transition-duration:4000ms !important}';
  document.head.appendChild(st);
  const btn=[...document.querySelectorAll('.td-right-bar button[aria-pressed]')].find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
  btn.click();                                   /* 先开（同样被放慢 20×） */
  return new Promise(r=>setTimeout(()=>{
    const b2=[...document.querySelectorAll('.td-right-bar button[aria-pressed]')].find(x=>(x.getAttribute('aria-label')||'').indexOf('侧栏')>=0);
    b2.click(); window.__T0=performance.now(); r('慢放 20× 已启动，开始收起');
  },4600));
})()
