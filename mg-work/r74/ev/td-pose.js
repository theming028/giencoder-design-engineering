(()=>{ const t=Number(window.__T||0); window.__F(t);
  return new Promise(r=>requestAnimationFrame(()=>{
    const g=s=>document.querySelector(s);
    const R=g('.td-root');
    const px=e=>{const b=e.getBoundingClientRect();return Math.round(b.left)+'..'+Math.round(b.right)};
    r({t:t, slot:px(g('.td-browse-slot')), chat:px(g('.td-right')), left:px(g('.td-left')),
       slotW:Math.round(g('.td-browse-slot').getBoundingClientRect().width),
       chatW:Math.round(g('.td-right').getBoundingClientRect().width)});
  })); })()
