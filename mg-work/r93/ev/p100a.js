(() => {
  const R = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return {
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      bg: cs.backgroundColor, color: cs.color, border: cs.borderTopColor,
      bw: cs.borderTopWidth, cursor: cs.cursor, fs: cs.fontSize, lh: cs.lineHeight,
      pad: cs.padding, radius: cs.borderRadius, shadow: cs.boxShadow
    };
  };
  const out = {};
  const host = document.querySelector('.r93-conv-host') || document;

  /* ---- ① ndesc（压缩上下文 / 上下文已压缩 的文字行） ---- */
  out.ndesc = [...host.querySelectorAll('.r93-ndesc')].map(el => {
    const o = R(el);
    o.text = (el.textContent || '').trim().slice(0, 12);
    o.cls = el.className;
    // 祖先里谁带背景？
    let p = el.parentElement, chain = [];
    for (let i = 0; i < 3 && p; i++) { chain.push(p.className + ' bg=' + getComputedStyle(p).backgroundColor); p = p.parentElement; }
    o.ancestors = chain;
    return o;
  });
  // 设计稿对照：note 行本体
  out.note = R(host.querySelector('.r93-note'));
  out.nrow = R(host.querySelector('.r93-nrow'));
  out.nline = R(host.querySelector('.r93-nline'));

  /* ---- ② 「调用 5 个工具」折叠块：展开头 / 折叠头 / 内嵌头 ---- */
  const toolsFold = [...host.querySelectorAll('.r93-fold')].find(f => (f.textContent || '').includes('调用 5 个工具'));
  out.toolsFoldFound = !!toolsFold;
  if (toolsFold) {
    out.toolsOpen = toolsFold.getAttribute('data-open');
    const fh = toolsFold.querySelector(':scope > .r93-fh');
    const fc = toolsFold.querySelector(':scope > .r93-fc');
    const nest = toolsFold.querySelector('.r93-nest');
    const nfh = toolsFold.querySelector('.r93-nest > .r93-fh');
    const slot = (b) => {
      if (!b) return null;
      const s = b.querySelector('.r93-iblk');
      const t = b.querySelector('.r93-ft');
      const cv = b.querySelector('.r93-cv');
      const svg = cv ? cv.querySelector('svg') : null;
      let bb = null;
      try { bb = svg ? svg.getBBox() : null; } catch (e) { bb = null; }
      return {
        btn: R(b), slotCls: s ? s.className : null, slotW: s ? Math.round(s.getBoundingClientRect().width) : null,
        cvCls: cv ? cv.className : null, svgVB: svg ? svg.getAttribute('viewBox') : null,
        svgRendered: svg ? Math.round(svg.getBoundingClientRect().width) : null,
        bbox: bb ? [ +bb.x.toFixed(2), +bb.y.toFixed(2), +bb.width.toFixed(2), +bb.height.toFixed(2) ] : null,
        pathD: svg ? (svg.querySelector('path') ? svg.querySelector('path').getAttribute('d') : null) : null,
        tx: t ? R(t) : null
      };
    };
    out.toolsFh = slot(fh);
    out.toolsFc = slot(fc);
    out.toolsNestFh = slot(nfh);
    out.nestCls = nest ? nest.className : null;
    out.nestMargin = nest ? getComputedStyle(nest).marginLeft : null;
    // 内嵌块结构
    out.nestHTML = nest ? nest.innerHTML.slice(0, 600) : null;
  }

  /* ---- ③ dlist 行 ---- */
  const dl = host.querySelector('.r93-dlist');
  out.dlist = R(dl);
  if (dl) {
    out.drowCount = dl.querySelectorAll('.r93-drow').length;
    out.drow0 = R(dl.querySelector('.r93-drow'));
    out.dname0 = R(dl.querySelector('.r93-drow .r93-dname'));
    out.dmore0 = R(dl.querySelector('.r93-drow .r93-dmore'));
    out.drowAttrs = [...dl.querySelectorAll('.r93-drow')].slice(0, 2).map(r => ({
      cls: r.className, cursor: getComputedStyle(r).cursor,
      hasData: r.hasAttribute('data-r93-row') || r.getAttribute('data-ctx-id') || null
    }));
  }

  /* ---- ④ agent 小卡 ---- */
  out.agents = [...host.querySelectorAll('.r93-agent')].map(a => ({
    cls: a.className, r: R(a)
  }));

  /* ---- ⑤ 滚动到底部 ---- */
  out.tobottom = R(host.querySelector('.r93-tobottom'));

  /* ---- ⑥ sumlist（调用 N 个工具的汇总清单） ---- */
  const sl = host.querySelector('.r93-sumlist');
  out.sumlist = R(sl);
  out.sumHtml = sl ? sl.outerHTML.slice(0, 900) : null;
  out.sumRows = sl ? [...sl.querySelectorAll('.r93-sumrow')].map(r => ({ r: R(r), tx: (r.textContent || '').trim() })) : null;

  /* ---- ⑦ GienX 残留 ---- */
  out.gienx = (document.body.innerHTML.match(/GienX/g) || []).length;

  /* ---- ⑧ r93-card 内字号直方图 ---- */
  const hist = {};
  [...host.querySelectorAll('.r93-card, .r93-card *')].forEach(el => {
    const fs = getComputedStyle(el).fontSize;
    hist[fs] = (hist[fs] || 0) + 1;
  });
  out.cardFsHist = hist;

  return JSON.stringify(out);
})();
