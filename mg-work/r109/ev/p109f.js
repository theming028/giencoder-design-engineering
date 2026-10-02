(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};

  /* ==================== ② 终端模块字号（先做，避免与 ① 的开关互相干扰）==================== */
  var om = q('[data-td-open-mod="browser"]');
  if (om) om.click();
  await W(1000);
  var root = cs(document.documentElement);
  out.tokens = {
    uiFs: root.getPropertyValue('--ui-fs').trim(),
    ratio: root.getPropertyValue('--ui-fs-ratio').trim(),
    body1: root.getPropertyValue('--font-size-body-1').trim(),
    body2: root.getPropertyValue('--font-size-body-2').trim()
  };
  var tAll = qa('.td-term');
  out.termCount = tAll.length;
  out.termFs = tAll.map(function (e) { return cs(e).fontSize; });
  out.termLh = tAll.map(function (e) { return cs(e).lineHeight; });
  out.tabs = qa('.td-term-tabs').map(function (e) { return cs(e).fontSize; });
  out.tab = qa('.td-term-tab').map(function (e) { return cs(e).fontSize; });
  out.tabadd = qa('.td-term-tabadd').map(function (e) { return cs(e).fontSize; });
  var t0 = q('.td-term'), tabs0 = q('.td-term-tabs'), tab0 = q('.td-term-tab'), add0 = q('.td-term-tabadd');
  out.boxes = {
    term: t0 ? B(t0) : null, termScrollH: t0 ? t0.scrollHeight : null, termClientH: t0 ? t0.clientHeight : null,
    tabs: tabs0 ? B(tabs0) : null, tab: tab0 ? B(tab0) : null, tabadd: add0 ? B(add0) : null
  };
  out.caret = q('.td-term-caret') ? B(q('.td-term-caret')) : null;
  /* 溢出判据：正文块内滚 / 标签条不被撑高 */
  out.noOverflow = {
    termScrolls: t0 ? t0.scrollHeight > t0.clientHeight + 1 : null,
    tabsH: tabs0 ? R(B(tabs0).h) : null,
    tabH: tab0 ? R(B(tab0).h) : null,
    tabaddH: add0 ? R(B(add0).h) : null
  };

  /* ==================== ③ 重新生成图标 ==================== */
  var rg = q('.r93-ib.r93-bt[title="重新生成"]');
  out.regenCount = qa('.r93-ib.r93-bt[title="重新生成"]').length;
  out.regen = rg ? (function () {
    var svg = rg.querySelector('svg'), ps = rg.querySelectorAll('path');
    return {
      box: B(rg), iblk: B(rg.querySelector('.r93-iblk')), svgBox: svg ? B(svg) : null,
      viewBox: svg ? svg.getAttribute('viewBox') : null,
      d: Array.prototype.slice.call(ps).map(function (p) { return p.getAttribute('d'); }),
      strokeW: ps[0] ? ps[0].getAttribute('stroke-width') : null,
      strokeCap: ps[0] ? ps[0].getAttribute('stroke-linecap') : null,
      fill0: ps[0] ? ps[0].getAttribute('fill') : null,
      fill1: ps[1] ? ps[1].getAttribute('fill') : null
    };
  })() : null;
  var html = document.documentElement.outerHTML;
  out.oldPathGone = html.indexOf('M13.9 9.4') < 0;
  out.newPathThere = html.indexOf('M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5') >= 0;
  /* IC() 全表内还有没有别的 regen 残影 */
  out.oldPathAnywhere = (function () { var n = 0, i = 0;
    while ((i = html.indexOf('M13.9 9.4', i)) >= 0) { n++; i++; } return n; })();
  if (rg) rg.scrollIntoView({ block: 'center' });
  await W(400);
  out.regenAfterScroll = rg ? B(rg) : null;

  /* ==================== ① 右栏展开 ⇒ zd-host 自动折叠为胶囊 ==================== */
  var slot = q('#av-browse-slot');
  var hostRow = document.querySelector('div:has(> main)');
  var toggle = q('.r93-baract[data-r93-browse]');
  var zdCard = q('[data-zd-card]'), zdMini = q('[data-zd-mini]');
  out.zd = {
    slotFound: !!slot, hostRowFound: !!hostRow,
    slotParentIsRow: !!(slot && hostRow && slot.parentElement === hostRow),
    slotParentCls: slot && slot.parentElement ? slot.parentElement.className : null,
    cardFound: !!zdCard, miniFound: !!zdMini,
    cardParent: zdCard ? zdCard.parentElement.id || zdCard.parentElement.className : null,
    toggleFound: !!toggle
  };
  var snap = function (tag) {
    return {
      tag: tag, on: !!(hostRow && hostRow.classList.contains('av-browse-on')),
      cardHidden: zdCard.hasAttribute('hidden'), miniHidden: zdMini.hasAttribute('hidden'),
      cardOpacity: cs(zdCard).opacity, miniOpacity: cs(zdMini).opacity,
      cardBox: B(zdCard), miniBox: B(zdMini),
      aria: toggle.getAttribute('aria-pressed')
    };
  };
  /* 归一到「右栏关闭」 */
  if (hostRow.classList.contains('av-browse-on')) { toggle.click(); await W(1000); }
  out.z0_closed = snap('closed');
  toggle.click(); await W(1100);                      /* 展开 → 应折成胶囊 */
  out.z1_opened = snap('opened');
  toggle.click(); await W(1100);                      /* 再收起 → 反向不应自动摊回 */
  out.z2_reclosed = snap('reclosed');
  /* 再展开一次，确认不是「只生效一次」 */
  toggle.click(); await W(1100);
  out.z3_openAgain = snap('openAgain');

  out.docOverflowX = document.documentElement.scrollWidth - window.innerWidth;
  return JSON.stringify(out);
})()
