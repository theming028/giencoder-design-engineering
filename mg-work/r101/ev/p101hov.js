(() => {
  // ★ 决定性 hover 读数：`matches(':hover')` 直接回答「hover 到底有没有生效」——
  //   只看底色是分不清「规则改了」还是「根本没 hover 上」的（透明既可能是命中规则、也可能是默认态）。
  const cs = el => el ? getComputedStyle(el) : null;
  const g = (el, s) => el ? el.querySelector(s) : null;
  const col = (el, s) => { const e = g(el, s); return e ? cs(e).color : null; };
  const fh = document.querySelector('[data-r101-fh]');
  const fc = document.querySelector('[data-r101-fc]');
  const ib = document.querySelector('[data-r101-ib]');
  const out = {};
  if (fh) out.fh = { hov: fh.matches(':hover'), bg: cs(fh).backgroundColor, color: cs(fh).color,
                     ico: col(fh, '.r93-cv'), ft: col(fh, '.r93-ft'), fm: col(fh, '.r93-fm') };
  if (fc) out.fc = { hov: fc.matches(':hover'), bg: cs(fc).backgroundColor, color: cs(fc).color,
                     ico: col(fc, '.r93-c3'), t14: col(fc, '.r93-t14'), fm: col(fc, '.r93-fm') };
  if (ib) out.ib = { hov: ib.matches(':hover'), bg: cs(ib).backgroundColor, sh: cs(ib).boxShadow,
                     color: cs(ib).color };
  return JSON.stringify(out);
})();
