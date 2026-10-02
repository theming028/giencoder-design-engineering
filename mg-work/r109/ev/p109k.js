(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};

  /* ========== ① 右栏展开 ⇒ zd-host 自动折叠为胶囊（**未碰任何开关的初态**下测） ========== */
  var slot = q('#av-browse-slot');
  var hostRow = document.querySelector('div:has(> main)');
  var toggle = q('.r93-baract[data-r93-browse]');
  var zdCard = q('[data-zd-card]'), mini = q('[data-zd-mini]');
  out.zd = {
    slotFound: !!slot, hostRowFound: !!hostRow,
    slotParentIsRow: !!(slot && hostRow && slot.parentElement === hostRow),
    slotParentCls: slot && slot.parentElement ? slot.parentElement.className : null,
    cardParent: zdCard.parentElement.id, miniParent: mini.parentElement.id,
    toggleAria: toggle.getAttribute('aria-pressed'), toggleTitle: toggle.title
  };
  var snap = function (tag) {
    return { tag: tag, on: hostRow.classList.contains('av-browse-on'),
      cardHidden: zdCard.hasAttribute('hidden'), miniHidden: mini.hasAttribute('hidden'),
      cardBox: B(zdCard), miniBox: B(mini),
      cardCls: zdCard.className, miniCls: mini.className, aria: toggle.getAttribute('aria-pressed') };
  };
  out.a0_fresh = snap('fresh');                 /* 页面初态：右栏默认是开还是关？ */
  if (zdCard.hasAttribute('hidden')) { mini.click(); await W(700); }
  out.a1_cardShown = snap('cardShown');         /* 手动摊成卡片 */
  toggle.click(); await W(1200);                /* 展开右栏 ⇒ 期望自动折叠 */
  out.a2_openPane = snap('openPane');
  mini.click(); await W(700);                   /* 用户手动又摊回卡片 */
  out.a3_userUnfold = snap('userUnfold');
  toggle.click(); await W(1200);                /* 收起右栏 ⇒ 期望**不**自动折回 */
  out.a4_closePane = snap('closePane');

  /* ========== ② 终端模块：字号 13px + 真盒子 + 无溢出 ========== */
  var ot = q('[data-td-open-mod="terminal"]'); if (ot) ot.click();
  await W(1100);
  var pane = q('#av-browse-pane-terminal');
  out.termPane = pane ? { hidden: pane.hasAttribute('hidden'), display: cs(pane).display } : null;
  var root = cs(document.documentElement);
  out.tokens = {
    uiFs: root.getPropertyValue('--ui-fs').trim(),
    ratio: root.getPropertyValue('--ui-fs-ratio').trim(),
    body1: root.getPropertyValue('--font-size-body-1').trim(),
    body2: root.getPropertyValue('--font-size-body-2').trim()
  };
  out.termFs = qa('.td-term').map(function (e) { return cs(e).fontSize; });
  out.tabsFs = cs(q('.td-term-tabs')).fontSize;
  out.tabFs = qa('.td-term-tab').map(function (e) { return cs(e).fontSize; });
  out.tabaddFs = cs(q('.td-term-tabadd')).fontSize;
  var t0 = q('.td-term'), tabs0 = q('.td-term-tabs'), tab0 = q('.td-term-tab'),
      add0 = q('.td-term-tabadd'), nm0 = q('.td-term-tab-nm');
  out.term = { box: B(t0), fs: cs(t0).fontSize, lh: cs(t0).lineHeight,
               scrollH: t0.scrollHeight, clientH: t0.clientHeight,
               overflowY: t0.scrollHeight > t0.clientHeight + 1,
               scrollW: t0.scrollWidth, clientW: t0.clientWidth };
  out.tabs = { box: B(tabs0), minH: cs(tabs0).minHeight, fs: cs(tabs0).fontSize };
  out.tab = { box: B(tab0), height: cs(tab0).height, fs: cs(tab0).fontSize };
  out.tabNm = { box: B(nm0), scrollW: nm0.scrollWidth, clientW: nm0.clientWidth,
                clipped: nm0.scrollWidth > nm0.clientWidth + 1, text: nm0.textContent.trim() };
  out.tabadd = { box: B(add0), w: cs(add0).width, h: cs(add0).height, fs: cs(add0).fontSize };
  out.caret = { box: B(q('.td-term-caret')), w: cs(q('.td-term-caret')).width,
                h: cs(q('.td-term-caret')).height };

  /* ========== ③ 重新生成图标（真机几何 + 旧路径归零） ========== */
  var rg = q('.r93-ib.r93-bt[title="重新生成"]');
  if (rg) rg.scrollIntoView({ block: 'center' });
  await W(400);
  out.regen = rg ? (function () {
    var svg = rg.querySelector('svg'), ps = rg.querySelectorAll('path');
    return { box: B(rg), iblk: B(rg.querySelector('.r93-iblk')), svgBox: B(svg),
             viewBox: svg.getAttribute('viewBox'),
             d: Array.prototype.slice.call(ps).map(function (p) { return p.getAttribute('d'); }),
             strokeW: ps[0].getAttribute('stroke-width'), cap: ps[0].getAttribute('stroke-linecap'),
             fill0: ps[0].getAttribute('fill'), fill1: ps[1].getAttribute('fill'),
             color: cs(svg).color, transDur: cs(rg).transitionDuration };
  })() : null;
  out.regenCount = qa('.r93-ib.r93-bt[title="重新生成"]').length;
  var html = document.documentElement.outerHTML;
  out.oldPathGone = html.indexOf('M13.9 9.4') < 0;
  out.newPathThere = html.indexOf('M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5') >= 0;
  out.docOverflowX = document.documentElement.scrollWidth - window.innerWidth;
  return JSON.stringify(out);
})()
