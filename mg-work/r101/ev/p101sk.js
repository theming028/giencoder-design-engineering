(() => {
  const R = { n: document.querySelectorAll('.r93-sk').length };
  const sk = document.querySelector('.r93-sk');
  if (sk) {
    const b = sk.getBoundingClientRect();
    const pane = document.querySelector('.r93-pane');
    const pb = pane ? pane.getBoundingClientRect() : null;
    R.box = [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)];
    R.paneBox = pb ? [Math.round(pb.left), Math.round(pb.top), Math.round(pb.width), Math.round(pb.height)] : null;
    R.z = getComputedStyle(sk).zIndex;
    R.bg = getComputedStyle(sk).backgroundColor;
    R.lines = sk.querySelectorAll('.giencoder-skeleton-line').length;
    R.titles = sk.querySelectorAll('.giencoder-skeleton-title').length;
    R.avs = sk.querySelectorAll('.giencoder-skeleton-avatar').length;
    const l = sk.querySelector('.giencoder-skeleton-line');
    if (l) { const a = getComputedStyle(l); R.lineAnim = a.animationName + ' ' + a.animationDuration; R.lineBg = a.backgroundImage.slice(0, 60); }
    R.innerW = (function () { const i = sk.querySelector('.r93-sk-in'); return i ? Math.round(i.getBoundingClientRect().width) : null; })();
    const wrap = document.querySelector('.r93-wrap');
    R.wrapW = wrap ? Math.round(wrap.getBoundingClientRect().width) : null;
    R.composer = !!document.querySelector('.r93-conv-host') && !!document.querySelector('textarea');
  }
  return JSON.stringify(R);
})();
