(() => {
  function readOne(el) {
    if (!el) return null;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return {
      tag: el.tagName,
      cls: (el.className || '').toString(),
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      bgi: cs.backgroundImage,
      bgSize: cs.backgroundSize,
      bgColor: cs.backgroundColor,
    };
  }
  window.__dots = function () {
    const out = { page: location.pathname.split('/').pop(), theme: document.documentElement.dataset.giDark || '?' };
    // 所有带 dot-bg 类的元素
    const dbs = [...document.querySelectorAll('.dot-bg')];
    out.dotBgEls = dbs.map(readOne);
    // 真正可见的 main
    const main = document.querySelector('main');
    out.main = readOne(main);
    // 扫描全页找含 radial-gradient 背景的元素（可见）
    const rg = [];
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if (cs.backgroundImage && cs.backgroundImage.includes('radial-gradient')) {
        const r = el.getBoundingClientRect();
        if (r.width > 40 && r.height > 40) {
          rg.push({
            tag: el.tagName,
            cls: (el.className || '').toString().slice(0, 120),
            x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            bgi: cs.backgroundImage.slice(0, 160),
            visible: cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0,
          });
        }
      }
    }
    out.radialEls = rg;
    return out;
  };
  return 'ready';
})()
