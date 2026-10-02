(async () => {
  /* r109 第三拍 ① 预备：进批注态 → 选中目标块 → 滚到视口中心 → 交出目标几何。
     ⚠ 不在本探针里 click（① 的判据要的是**真实点击点**）⇒ 点击由编排脚本用真鼠标发。 */
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const out = {};
  var om = q('[data-td-open-mod="browser"]');
  if (om) om.click();
  await W(1100);
  var brw = q('.td-brw');
  out.brwVis = getComputedStyle(brw).display;
  if (!brw.classList.contains('is-annotating')) { q('.td-url-annot').click(); await W(500); }
  out.isAnnotating = brw.classList.contains('is-annotating');

  /* 目标：一段**又长又宽**的正文块 —— 点它的**左端**才能看出「原点跟着点击点走」 */
  var els = qa('.td-page [data-td-el]');
  var target = els.filter(e => e.className.indexOf('td-page-card') >= 0)[0] || els[0];
  out.target = target.className;
  target.scrollIntoView({ block: 'center' });
  await W(450);
  out.targetBox = B(target);
  var v = q('.td-brw [data-td-view]');
  out.viewBox = B(v);
  out.viewScrollTop = +v.scrollTop.toFixed(2);
  out.viewScrollLeft = +v.scrollLeft.toFixed(2);
  /* 点击点：目标块**左起 56px、上起 22px**（明显偏离中心 ⇒ 中心落点和左上落点可分） */
  out.click = { x: Math.round(out.targetBox.l + 56), y: Math.round(out.targetBox.t + 22) };
  out.targetCenter = { x: Math.round(out.targetBox.l + out.targetBox.w / 2),
                       y: Math.round(out.targetBox.t + out.targetBox.h / 2) };
  out.existingAnchors = qa('.td-anchor').length;
  return JSON.stringify(out);
})()
