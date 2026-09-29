(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const R = e => { const r = e.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join(','); };
  const host = document.querySelector('.kb-radio');
  const out = { has: !!host };
  if (!host) return JSON.stringify(out);
  const thumb = host.querySelector('.kb-radio-thumb');
  out.hostClass = host.className;
  out.host = R(host);
  out.thumb = thumb ? R(thumb) : null;
  out.thumbCS = thumb ? { pos:getComputedStyle(thumb).position, bg:getComputedStyle(thumb).backgroundColor, bd:getComputedStyle(thumb).borderColor, radius:getComputedStyle(thumb).borderRadius, trans:getComputedStyle(thumb).transitionDuration } : null;
  out.btns = [...host.querySelectorAll('.kb-radio-btn')].map(b => ({
    txt:b.textContent.trim().slice(0,6), goto:b.getAttribute('data-goto'), on:b.classList.contains('is-on'), rect:R(b), ico:!!b.querySelector('.kb-radio-ico')
  }));
  out.thumbMatchesOn = thumb ? (R(thumb) === (out.btns.find(b=>b.on)||{}).rect) : null;
  // 点另一个 tab：等 130ms 读滑动中间态
  const other = host.querySelector('.kb-radio-btn:not(.is-on)[data-goto]');
  out.clickTarget = other ? other.getAttribute('data-goto') : null;
  if (other) {
    other.click();
    await wait(130);
    out.midThumb = R(thumb);
    out.midExpanded = { l: thumb.style.left, w: thumb.style.width };
    out.sessionFrom = sessionStorage.getItem('giencoder-kb-tab-from');
  }
  return JSON.stringify(out);
})()
