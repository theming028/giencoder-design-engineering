(() => {
  const host = document.querySelector('.r93-conv-host');
  const toolsFold = [...host.querySelectorAll('.r93-fold')].find(f => (f.textContent || '').includes('调用 5 个工具'));
  const tree = toolsFold.querySelector(':scope > .r93-fb > .r93-tree');
  const inner = tree.querySelector(':scope > .r93-fold');
  const before = inner.getAttribute('data-open');
  const probe = (tag) => {
    const one = (b) => {
      if (!b) return null;
      const s = b.querySelector('.r93-iblk');
      const r = b.getBoundingClientRect();
      const t = b.querySelector('.r93-t14');
      return { slot: s ? s.className : null, slotW: Math.round(s.getBoundingClientRect().width),
        txt: t ? t.textContent : null, w: Math.round(r.width), h: Math.round(r.height),
        display: getComputedStyle(b).display };
    };
    const rf = inner.getBoundingClientRect();
    return { state: tag, foldH: Math.round(rf.height), fh: one(inner.querySelector(':scope > .r93-fh')),
      fc: one(inner.querySelector(':scope > .r93-fc')),
      treeH: Math.round(tree.getBoundingClientRect().height),
      sumY: Math.round(tree.querySelector('.r93-sumlist').getBoundingClientRect().y),
      cardH: inner.querySelector('.r93-card') ? Math.round(inner.querySelector('.r93-card').getBoundingClientRect().height) : null };
  };
  inner.setAttribute('data-open', before === '1' ? '0' : '1');
  const toggled = probe(before + '->' + inner.getAttribute('data-open'));
  inner.setAttribute('data-open', before);
  const restored = probe('restored ' + inner.getAttribute('data-open'));
  return JSON.stringify({ before, toggled, restored });
})();
