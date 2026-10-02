(async () => {
  const out = {};
  const btn = document.querySelector('.r93-umeta [title="重新生成"]') || document.querySelector('[title="重新生成"]');
  if (!btn) { return JSON.stringify({found:false}); }
  out.found = true;
  const r = btn.getBoundingClientRect();
  out.btn = {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)};
  const svg = btn.querySelector('svg');
  out.svg = svg ? svg.getAttribute('viewBox') : null;
  out.svgHTML = svg ? svg.outerHTML : null;
  const sr = svg.getBoundingClientRect();
  out.svgRect = {x:Math.round(sr.x), y:Math.round(sr.y), w:Math.round(sr.width), h:Math.round(sr.height)};
  const cs = getComputedStyle(btn);
  out.btnStyle = {color:cs.color, w:cs.width, h:cs.height, display:cs.display, overflow:cs.overflow};
  const scs = getComputedStyle(svg);
  out.svgStyle = {w:scs.width, h:scs.height, display:scs.display, overflow:scs.overflow};
  const blk = btn.querySelector('.r93-iblk');
  if (blk) { const bc=getComputedStyle(blk); out.blkStyle={w:bc.width,h:bc.height,overflow:bc.overflow}; }

  // --- ink bbox of the real 14x14 render, via canvas ---
  try {
    const s = new XMLSerializer().serializeToString(svg);
    const img = new Image();
    const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s.replace('<svg','<svg width="14" height="14" xmlns="http://www.w3.org/2000/svg"').replace(/currentColor/g,'#868686'));
    await new Promise((res,rej)=>{img.onload=res;img.onerror=rej;img.src=url;});
    const cv=document.createElement('canvas'); cv.width=14; cv.height=14;
    const ctx=cv.getContext('2d'); ctx.drawImage(img,0,0,14,14);
    const d=ctx.getImageData(0,0,14,14).data;
    let x0=99,y0=99,x1=-1,y1=-1,n=0;
    for(let y=0;y<14;y++)for(let x=0;x<14;x++){const a=d[(y*14+x)*4+3]; if(a>10){n++; if(x<x0)x0=x; if(y<y0)y0=y; if(x>x1)x1=x; if(y>y1)y1=y;}}
    out.in14 = {x0:x0,y0:y0,x1:x1,y1:y1,w:x1-x0+1,h:y1-y0+1,ink:n};
  } catch(e) { out.canvasErr = String(e); }

  // --- big overlay for eyeballs ---
  const host = document.createElement('div');
  host.id='regenzoom';
  host.style.cssText='position:fixed;left:8px;top:8px;z-index:99999;background:#fff;padding:12px;display:flex;gap:16px;align-items:flex-start;box-shadow:0 0 0 2px #f00';
  const mk=(scale,label)=>{
    const box=document.createElement('div');
    box.style.cssText='display:flex;flex-direction:column;gap:6px;align-items:center;font:12px monospace;color:#111';
    const holder=document.createElement('div');
    holder.style.cssText='width:'+(14*scale)+'px;height:'+(14*scale)+'px;color:#868686';
    const c=svg.cloneNode(true);
    c.setAttribute('width','100%'); c.setAttribute('height','100%');
    holder.appendChild(c);
    const t=document.createElement('span'); t.textContent=label;
    box.appendChild(holder); box.appendChild(t);
    return box;
  };
  host.appendChild(mk(20,'real svg x20'));
  document.body.appendChild(host);
  out.overlayRect = host.getBoundingClientRect().toJSON();
  return JSON.stringify(out);
})()
