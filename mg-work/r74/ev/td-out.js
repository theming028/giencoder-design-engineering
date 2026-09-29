(()=>{ const f=s=>(s||[]).map(x=>x.t+'|b'+x.b+'|kl'+x.kl+'|slot '+x.slot+'|left '+x.left+'|right '+x.right+'|rr '+x.rr+'|bw '+x.bw+'|'+x.pc);
  return 'OPEN\n'+f(window.__A).filter(l=>{const t=+l.split('|')[0];return t<400;}).join('\n')+'\n\nCLOSE\n'+f(window.__B).filter(l=>{const t=+l.split('|')[0];return t<420;}).join('\n'); })()
