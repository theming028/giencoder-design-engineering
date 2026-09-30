(() => {
  const R = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      color: cs.color, bg: cs.backgroundColor, border: cs.borderTopColor, bw: cs.borderTopWidth,
      cursor: cs.cursor, fs: cs.fontSize, radius: cs.borderRadius, pad: cs.padding };
  };
  const host = document.querySelector('.r93-conv-host') || document;
  const out = {};

  /* ① GienX 残留 + 助手名 */
  out.gienxCount = (document.body.innerHTML.match(/GienX/g) || []).length;
  out.giencoderCount = (document.body.innerHTML.match(/GienCoder/g) || []).length;
  const ahd = host.querySelector('.r93-ahd .r93-t14b');
  out.ahdName = ahd ? ahd.textContent : null;
  out.ububGien = (host.querySelector('.r93-card--quiz .r93-c2') || {}).textContent || null;

  /* ② .r93-card 内字号直方图 */
  const hist = {};
  [...host.querySelectorAll('.r93-card, .r93-card *')].forEach(el => {
    const fs = getComputedStyle(el).fontSize;
    hist[fs] = (hist[fs] || 0) + 1;
  });
  out.cardFsHist = hist;
  out.cardSelfFs = host.querySelector('.r93-card') ? getComputedStyle(host.querySelector('.r93-card')).fontSize : null;
  // 抽样：代码卡里的 pre / chead
  out.preFs = host.querySelector('.r93-card .r93-pre') ? getComputedStyle(host.querySelector('.r93-card .r93-pre')).fontSize : null;
  out.cpathFs = host.querySelector('.r93-card .r93-chead .r93-t12') ? getComputedStyle(host.querySelector('.r93-card .r93-chead .r93-t12')).fontSize : null;

  /* ③ 滚动到底部（默认态） */
  out.tobottom = R(host.querySelector('.r93-tobottom'));

  /* ④ dlist 行 */
  const dl = host.querySelector('.r93-dlist');
  out.dlist = R(dl);
  out.drow0 = R(dl && dl.querySelector('.r93-drow'));
  out.drowCursorList = [...dl.querySelectorAll('.r93-drow')].map(r => getComputedStyle(r).cursor);

  /* ⑤ agent 卡（默认态） */
  out.agents = [...host.querySelectorAll('.r93-agent')].map(a => ({ cls: a.className, r: R(a) }));

  /* ⑥ ndesc 胶囊 */
  out.ndesc = [...host.querySelectorAll('.r93-ndesc')].map(el => {
    const o = R(el);
    o.text = (el.textContent || '').trim().slice(0, 10);
    return o;
  });

  /* ⑦⑧ 层级树 */
  const toolsFold = [...host.querySelectorAll('.r93-fold')].find(f => (f.textContent || '').includes('调用 5 个工具'));
  out.toolsFold = toolsFold ? { open: toolsFold.getAttribute('data-open'), r: R(toolsFold) } : null;
  const tree = toolsFold ? toolsFold.querySelector(':scope > .r93-fb > .r93-tree') : null;
  out.tree = tree ? R(tree) : null;
  out.treeLineBg = tree ? getComputedStyle(tree, '::before').backgroundColor : null;
  out.treeLineW = tree ? getComputedStyle(tree, '::before').width : null;
  const inner = tree ? tree.querySelector(':scope > .r93-fold') : null;
  out.innerFold = inner ? { open: inner.getAttribute('data-open'), r: R(inner), mt: getComputedStyle(inner).marginTop } : null;
  const slotOf = (b) => {
    if (!b) return null;
    const s = b.querySelector('.r93-iblk');
    const svg = s ? s.querySelector('svg') : null;
    const t = b.querySelector('.r93-ft') || b.querySelector('.r93-t14');
    return { slotCls: s ? s.className : null, slotW: s ? Math.round(s.getBoundingClientRect().width) : null,
      svgVB: svg ? svg.getAttribute('viewBox') : null,
      svgR: svg ? Math.round(svg.getBoundingClientRect().width) : null,
      text: t ? t.textContent : null, r: R(b) };
  };
  out.innerHead = inner ? slotOf(inner.querySelector(':scope > .r93-fh')) : null;
  out.innerCol = inner ? slotOf(inner.querySelector(':scope > .r93-fc')) : null;
  out.outerHead = toolsFold ? slotOf(toolsFold.querySelector(':scope > .r93-fh')) : null;
  out.outerCol = toolsFold ? slotOf(toolsFold.querySelector(':scope > .r93-fc')) : null;
  // 内嵌代码卡落点
  const icard = inner ? inner.querySelector('.r93-card') : null;
  out.innerCard = icard ? R(icard) : null;
  // 4 行清单
  out.sumlist = tree ? R(tree.querySelector('.r93-sumlist')) : null;
  out.sumRows = tree ? [...tree.querySelectorAll('.r93-sumrow')].map(r => {
    const o = R(r);
    o.elbowBg = getComputedStyle(r, '::before').backgroundColor;
    o.elbowW = getComputedStyle(r, '::before').width;
    o.elbowLeft = getComputedStyle(r, '::before').left;
    o.elbowTop = getComputedStyle(r, '::before').top;
    return o;
  }) : null;
  out.innerElbow = inner ? { w: getComputedStyle(inner, '::before').width,
                             left: getComputedStyle(inner, '::before').left,
                             top: getComputedStyle(inner, '::before').top,
                             bg: getComputedStyle(inner, '::before').backgroundColor } : null;
  // 每层左缘（层级缩进：L0 / L1 / L2）
  out.indent = {
    L0: toolsFold ? Math.round(toolsFold.querySelector(':scope > .r93-fh').getBoundingClientRect().x) : null,
    L1: out.innerHead ? out.innerHead.r.x : null,
    L2: out.innerCard ? out.innerCard.x : null,
    sumRow: out.sumRows ? out.sumRows[0].x : null
  };
  return JSON.stringify(out);
})();
