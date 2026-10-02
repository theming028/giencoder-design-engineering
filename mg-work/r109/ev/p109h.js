(async () => {
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const out = {};
  var a = q('.td-anchor'), v = q('.td-brw [data-td-view]');
  out.box = B(a);
  out.left = a.style.left; out.top = a.style.top;
  out.leftNum = parseFloat(a.style.left); out.topNum = parseFloat(a.style.top);
  out.isDragging = a.classList.contains('is-dragging');
  out.transDur = cs(a).transitionDuration;
  out.elnoteHidden = q('.td-elnote').hasAttribute('hidden');
  out.expectMax = { L: v.scrollLeft + v.clientWidth - a.offsetWidth,
                    T: v.scrollTop + v.clientHeight - a.offsetHeight };
  var ar = B(a), vr = B(v);
  out.inView = ar.l >= vr.l - 0.5 && ar.t >= vr.t - 0.5 &&
               ar.l + ar.w <= vr.l + vr.w + 0.5 && ar.t + ar.h <= vr.t + vr.h + 0.5;
  out.docOverflowX = document.documentElement.scrollWidth - window.innerWidth;
  out.anchorCenter = { x: Math.round(ar.l + ar.w / 2), y: Math.round(ar.t + ar.h / 2) };
  return JSON.stringify(out);
})()
