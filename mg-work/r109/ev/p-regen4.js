(async () => {
  const out = {};
  const um = document.querySelector('.r93-umeta');
  if (!um) return JSON.stringify({found:false});
  out.found = true;
  const btns = um.querySelectorAll('.r93-ib');
  out.btns = [];
  btns.forEach(b=>{
    const c=getComputedStyle(b);
    const s=b.querySelector('svg');
    out.btns.push({title:b.getAttribute('title'),
      color:c.color, bg:c.backgroundColor,
      svgColor: s?getComputedStyle(s).color:null,
      vb: s?s.getAttribute('viewBox'):null,
      d: s?s.innerHTML.slice(0,150):null,
      rect: (r=>({x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}))(b.getBoundingClientRect())
    });
  });
  const t12 = um.querySelector('.r93-t12');
  if (t12) out.timeColor = getComputedStyle(t12).color;
  // clone the row into a zoomed overlay
  const host=document.createElement('div');
  host.id='umzoom';
  host.style.cssText='position:fixed;left:6px;top:6px;z-index:99999;background:#fff;padding:10px;box-shadow:0 0 0 2px #f00';
  const inner=document.createElement('div');
  inner.style.cssText='zoom:7';
  inner.appendChild(um.cloneNode(true));
  host.appendChild(inner);
  document.body.appendChild(host);
  out.zoomRect = host.getBoundingClientRect().toJSON();
  return JSON.stringify(out);
})()
