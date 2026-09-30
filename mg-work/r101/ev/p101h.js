(() => {
  const cs = el => el ? getComputedStyle(el) : null;
  const r = el => { const b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const fh = document.querySelector('[data-r101-fh]');
  const ib = document.querySelector('[data-r101-ib]');
  const fc = document.querySelector('[data-r101-fc]');
  const g = (el, s) => el ? el.querySelector(s) : null;
  return JSON.stringify({
    // ① 展开头 hover：底色应为透明、前景保持正文色
    fh_bg: cs(fh) ? cs(fh).backgroundColor : null,
    fh_color: cs(fh) ? cs(fh).color : null,
    ft_color: cs(g(fh, '.r93-ft')) ? cs(g(fh, '.r93-ft')).color : null,
    fm_color: cs(g(fh, '.r93-fm')) ? cs(g(fh, '.r93-fm')).color : null,
    // ① 折叠头 hover：底色透明 + 图标/文字提到正文色
    fc_display: cs(fc) ? cs(fc).display : null,
    fc_bg: cs(fc) ? cs(fc).backgroundColor : null,
    fc_color: cs(fc) ? cs(fc).color : null,
    fc_ico: cs(g(fc, '.r93-c3')) ? cs(g(fc, '.r93-c3')).color : null,
    fc_t14: cs(g(fc, '.r93-t14')) ? cs(g(fc, '.r93-t14')).color : null,
    fc_fm: cs(g(fc, '.r93-fm')) ? cs(g(fc, '.r93-fm')).color : null,
    // ③ 图标按钮 hover
    ib_bg: cs(ib) ? cs(ib).backgroundColor : null,
    ib_sh: cs(ib) ? cs(ib).boxShadow : null,
    ib_color: cs(ib) ? cs(ib).color : null,
    box: { fh: fh ? r(fh) : null, ib: ib ? r(ib) : null }
  });
})();
