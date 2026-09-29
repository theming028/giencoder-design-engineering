(()=>{
  const R=document.querySelector('.td-root');
  const cs=getComputedStyle(R);
  const kids=[...R.children].map(c=>({tag:c.tagName.toLowerCase(),cls:String(c.className).slice(0,40),
    w:+c.getBoundingClientRect().width.toFixed(1),disp:getComputedStyle(c).display}));
  const L=document.querySelector('.td-left'), G=document.querySelector('.td-gutter'), Rt=document.querySelector('.td-right'), S=document.querySelector('.td-browse-slot');
  const cs2=e=>{const s=getComputedStyle(e);return {w:+e.getBoundingClientRect().width.toFixed(1),fb:s.flexBasis,fg:s.flexGrow,fs:s.flexShrink,mn:s.minWidth,mx:s.maxWidth,mr:s.marginRight};};
  return {rootW:+R.getBoundingClientRect().width.toFixed(1), rootDir:cs.flexDirection,
    left:cs2(L), gutter:cs2(G), right:cs2(Rt), slot:cs2(S), kids};
})()
