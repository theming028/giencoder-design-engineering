(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const snap = tag => {
    const kids = [...document.body.children];
    out.push('--- ' + tag + ' body.children=' + kids.length);
    kids.forEach((e, i) => {
      const c = getComputedStyle(e), r = e.getBoundingClientRect();
      out.push('  ' + i + ' ' + e.tagName + ' pos=' + c.position + ' z=' + c.zIndex +
        ' box=' + [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(',') +
        ' vis=' + c.visibility + ' op=' + c.opacity.slice(0, 4) +
        ' cls=' + ((e.className || '') + '').slice(0, 24) +
        ' style=' + JSON.stringify((e.getAttribute('style') || '').slice(0, 90)));
    });
  };
  const btn = document.querySelector('button.ws-trigger-hover');
  if (!btn) return 'NO_BTN';
  snap('点前');
  btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
  btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
  btn.click();
  await wait(520);
  snap('点后');
  return out.join('\n');
})()
