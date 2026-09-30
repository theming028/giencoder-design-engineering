(() => {
  const H = document.querySelector('.r93-conv-host');
  const rx = el => { const b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const card = document.querySelector('[data-r101-art]') || H.querySelector('.r93-artcard');
  if (!card) return JSON.stringify({ err: 'no artcard' });
  const cr = card.getBoundingClientRect();
  const x = Math.round(cr.left + 60), y = Math.round(cr.top + 24);
  card.dispatchEvent(new MouseEvent('contextmenu',
    { bubbles: true, cancelable: true, button: 2, clientX: x, clientY: y }));
  const menu = document.querySelector('.r93-ctx.giencoder-dropdown-popup');
  if (!menu) return JSON.stringify({ err: 'menu not built' });
  const items = Array.from(menu.querySelectorAll('.giencoder-dropdown-item'));
  const labels = items.map(i => i.querySelector('.r93-ctx-label').textContent);
  const arrows = items.map(i => !!i.querySelector('.giencoder-dropdown-arrow'));
  const ow = items[items.length - 1];
  ow.dispatchEvent(new PointerEvent('pointerover', { bubbles: true }));
  const sub = document.querySelector('.r93-ctx.giencoder-dropdown-submenu-popup');
  let subInfo = null;
  if (sub) {
    subInfo = { box: rx(sub), open: sub.classList.contains('giencoder-popup-open'),
                labels: Array.from(sub.querySelectorAll('.r93-ctx-label')).map(e => e.textContent),
                icoW: getComputedStyle(sub.querySelector('.r93-ctx-ico')).width };
  }
  const first = items[0];
  return JSON.stringify({
    cardBox: [Math.round(cr.left), Math.round(cr.top), Math.round(cr.width), Math.round(cr.height)],
    cursor: [x, y],
    menuBox: rx(menu), menuOpen: menu.classList.contains('giencoder-popup-open'),
    labels: labels, arrows: arrows,
    rowPad: getComputedStyle(first).padding, rowFs: getComputedStyle(first).fontSize,
    icoW: getComputedStyle(first.querySelector('.r93-ctx-ico')).width,
    divider: menu.querySelectorAll('.giencoder-dropdown-divider').length,
    sub: subInfo
  });
})();
