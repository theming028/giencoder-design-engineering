(() => {
  const host = document.querySelector('.kb-radio');
  const out = { has: !!host };
  if (!host) return JSON.stringify(out);
  const hr = host.getBoundingClientRect();
  out.host = [Math.round(hr.x),Math.round(hr.y),Math.round(hr.width),Math.round(hr.height)].join(',');
  out.hostCS = { pos:getComputedStyle(host).position, bg:getComputedStyle(host).backgroundColor, radius:getComputedStyle(host).borderRadius, left:getComputedStyle(host).left, top:getComputedStyle(host).top };
  out.btns = [...host.querySelectorAll('.kb-radio-btn')].map(b => {
    const r = b.getBoundingClientRect();
    const cs = getComputedStyle(b);
    return { txt:b.textContent.trim().slice(0,8), goto:b.getAttribute('data-goto'), on:b.classList.contains('is-on'),
      rect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join(','),
      off:[b.offsetLeft,b.offsetTop,b.offsetWidth,b.offsetHeight].join(','),
      bg:cs.backgroundColor, bd:cs.borderColor, bw:cs.borderWidth, pad:cs.padding, radius:cs.borderRadius, gap:cs.gap, color:cs.color };
  });
  out.hostOff = [host.offsetLeft, host.offsetTop, host.offsetWidth, host.offsetHeight].join(',');
  out.parent = host.parentElement ? host.parentElement.className : null;
  out.parentCS = host.parentElement ? { pos:getComputedStyle(host.parentElement).position, tag:host.parentElement.tagName } : null;
  return JSON.stringify(out);
})()
