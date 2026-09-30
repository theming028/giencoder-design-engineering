(() => {
  const q = s => Array.from(document.querySelectorAll(s));
  const box = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; };
  const out = {};
  out.fh = q('.r93-fh').slice(0, 3).map(el => {
    const cs = getComputedStyle(el);
    const ft = el.querySelector('.r93-ft'), cv = el.querySelector('.r93-cv');
    return { box: box(el), color: cs.color, bg: cs.backgroundColor,
      ft: ft ? getComputedStyle(ft).color : null, cv: cv ? getComputedStyle(cv).color : null };
  });
  out.fc = q('.r93-fc').slice(0, 3).map(el => {
    const cs = getComputedStyle(el);
    return { box: box(el), color: cs.color, bg: cs.backgroundColor };
  });
  out.t12l = q('.r93-t12l').slice(0, 8).map(el => {
    const cs = getComputedStyle(el);
    return { t: (el.textContent || '').slice(0, 16), fs: cs.fontSize, color: cs.color };
  });
  out.ib = q('.r93-ib').slice(0, 6).map(el => {
    const cs = getComputedStyle(el);
    return { box: box(el), title: el.getAttribute('title'), bg: cs.backgroundColor, color: cs.color, sh: cs.boxShadow };
  });
  out.cv = q('.r93-cv').slice(0, 5).map(el => {
    const cs = getComputedStyle(el), svg = el.querySelector('svg');
    return { slot: box(el), slotW: cs.width,
      svgW: svg ? getComputedStyle(svg).width : null,
      svgRect: svg ? [Math.round(svg.getBoundingClientRect().width), Math.round(svg.getBoundingClientRect().height)] : null };
  });
  out.okc = q('.r93-okc').map(el => ({ box: box(el), ctx: (el.parentElement.textContent || '').slice(0, 34) }));
  out.c3ic = q('.r93-iblk.r93-c3').slice(0, 6).map(el => ({ box: box(el), ctx: (el.parentElement.textContent || '').slice(0, 24) }));
  out.fm = q('.r93-t12l.r93-fm.r93-ell').slice(0, 5).map(el => {
    const cs = getComputedStyle(el);
    return { t: (el.textContent || '').slice(0, 22), fs: cs.fontSize, color: cs.color, lh: cs.lineHeight };
  });
  out.sb = q('.r93-sb').map(el => {
    const cs = getComputedStyle(el);
    return { box: box(el), sh: cs.boxShadow, bg: cs.backgroundColor, bd: cs.borderTopColor };
  });
  out.art = q('.r93-artcard').slice(0, 4).map(el => ({ box: box(el), t: (el.textContent || '').slice(0, 20) }));
  const sc = document.querySelector('.r93-scroll');
  out.scroll = sc ? { box: box(sc), sh: sc.scrollHeight, ch: sc.clientHeight, st: sc.scrollTop,
    mask: getComputedStyle(sc).maskImage, bg: getComputedStyle(sc).backgroundColor } : null;
  const pane = document.querySelector('.r93-pane[data-r93-pane]');
  out.pane = pane ? { box: box(pane), bg: getComputedStyle(pane).backgroundColor } : null;
  const host = document.querySelector('.r93-conv-host');
  out.hostBg = host ? getComputedStyle(host).backgroundColor : null;
  const main = document.querySelector('main');
  out.mainBg = main ? getComputedStyle(main).backgroundColor : null;
  const bottom = document.querySelector('.r93-bottom');
  out.bottom = bottom ? { box: box(bottom), bg: getComputedStyle(bottom).backgroundColor } : null;
  out.chead = q('.r93-chead').slice(0, 6).map(el => ({ box: box(el), t: (el.textContent || '').slice(0, 20) }));
  return JSON.stringify(out);
})();
