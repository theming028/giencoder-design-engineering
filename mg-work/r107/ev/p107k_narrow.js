/* 第十拍 窄栏探针：菜单是否完全落在 `.td-browse` 面板内（左右都不越界、不被裁） */
(function () {
  var host = document.querySelector('.td-browse');
  if (!host) return JSON.stringify({ err: 'no .td-browse' });
  var hr = host.getBoundingClientRect();
  var out = { panelW: +hr.width.toFixed(1), panelL: +hr.left.toFixed(1), panelR: +hr.right.toFixed(1),
              slotVar: getComputedStyle(document.getElementById('av-browse-slot')).getPropertyValue('--av-browse-w').trim(),
              menus: [] };
  var pairs = [['td-rv-scope-menu', '[data-td-rv-scope]'], ['td-rv-opts', '[data-td-rv-opts]'], ['td-commit-menu', '[data-td-commit]']];
  for (var i = 0; i < pairs.length; i++) {
    var m = document.querySelector('.' + pairs[i][0]);
    var t = document.querySelector(pairs[i][1]);
    if (!m || !t) continue;
    var mb = m.getBoundingClientRect(), tb = t.getBoundingClientRect();
    var modRect = m.closest('.td-mod') ? m.closest('.td-mod').getBoundingClientRect() : null;
    out.menus.push({
      name: pairs[i][0],
      open: !m.hasAttribute('hidden'),
      mT: +mb.top.toFixed(1), mL: +mb.left.toFixed(1), mR: +mb.right.toFixed(1), mW: +mb.width.toFixed(1), mH: +mb.height.toFixed(1),
      tL: +tb.left.toFixed(1), tB: +tb.bottom.toFixed(1),
      /* 判据 */
      inPanelL: mb.left >= hr.left - 0.5,
      inPanelR: mb.right <= hr.right + 0.5,
      inModL: modRect ? mb.left >= modRect.left - 0.5 : null,   /* `.td-mod{overflow:hidden}` 会裁 */
      inModR: modRect ? mb.right <= modRect.right + 0.5 : null,
      insideMod: modRect ? (mb.left >= modRect.left - 0.5 && mb.right <= modRect.right + 0.5 &&
                            mb.top >= modRect.top - 0.5 && mb.bottom <= modRect.bottom + 0.5) : null,
      dy: +(mb.top - tb.bottom).toFixed(1)
    });
  }
  return JSON.stringify(out);
})()
