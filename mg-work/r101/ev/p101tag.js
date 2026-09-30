(() => {
  const H = document.querySelector('.r93-conv-host');
  const t = (el, s) => { const e = el ? el.querySelector(s) : null; return e ? (e.textContent || '').trim() : null; };
  // 展开态的折叠头：取第 2 个（Bash / 深度思考 之类有 meta 的更好看），退化为第 1 个
  const fhs = Array.from(H.querySelectorAll('.r93-fold > .r93-fh'));
  const fh = fhs[1] || fhs[0];
  if (fh) fh.setAttribute('data-r101-fh', '1');
  // 用户消息里的图标按钮（第一枚 = 重新生成）
  const ib = H.querySelector('.r93-umeta .r93-ib');
  if (ib) ib.setAttribute('data-r101-ib', '1');
  // 任务产物第一张卡
  const art = H.querySelector('.r93-artcard');
  if (art) art.setAttribute('data-r101-art', '1');
  // 状态条
  const sb = H.querySelector('.r93-sb');
  if (sb) sb.setAttribute('data-r101-sb', '1');
  // 压缩上下文那一行
  const zip = H.querySelector('.r93-spin');
  if (zip) zip.setAttribute('data-r101-zip', '1');
  return JSON.stringify({
    fh: !!fh, fhText: t(fh, '.r93-ft'), fhMeta: t(fh, '.r93-fm'),
    ib: !!ib, art: !!art, artName: art ? art.getAttribute('data-r93-artname') : null,
    sb: !!sb, zip: !!zip
  });
})();
