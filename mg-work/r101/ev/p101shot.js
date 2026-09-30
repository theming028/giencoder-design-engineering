(() => {
  const H = document.querySelector('.r93-conv-host');
  const folds = Array.from(H.querySelectorAll('.r93-fold'));
  var n = 0;
  for (var i = 0; i < folds.length; i++) {
    var ft = folds[i].querySelector('.r93-fh .r93-ft');
    if (ft && (ft.textContent || '').trim() === 'Bash') {
      const h = folds[i].querySelector('.r93-chead');
      if (h) { h.setAttribute('data-r101-shot', 'bash'); n++; }
      const okc = folds[i].querySelectorAll('.r93-okc');
      const copy = folds[i].querySelectorAll('[data-r93-copy]');
      return JSON.stringify({ ok: n, okcInBash: okc.length, copyInBash: copy.length,
        headText: h ? (h.textContent || '').trim().slice(0, 40) : null });
    }
  }
  return JSON.stringify({ ok: n, err: 'no bash fold' });
})();
