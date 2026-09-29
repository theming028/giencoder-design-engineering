/* r76 · 需求 4 验收探针：技能浮窗在纵向不足时是否还被裁
   断言项：
     over        = main.t - pop.t          （>0 ⇒ 浮窗顶超出 main 上缘 = 被裁）
     clipTop     = main.t - pop.t          同上（别名，沿用旧口径）
     maxH        = 计算出的 max-height     （期望 50vh - 120px）
     popH        = 浮窗实际高
     listScroll  = 内层列表 clientHeight / scrollHeight（期望 client < scroll ⇒ 可滚）
     popDisplay  = 期望 block
     动画        = 命中 r74-pop-in 的动画条目数（进场动效不得被 max-height 影响）
   另记 header / main / 触发器 / 浮窗 的 rect，便于人读。 */
(async () => {
  const q = s => document.querySelector(s);
  const R = e => { const b = e.getBoundingClientRect(); return { l: +b.left.toFixed(1), t: +b.top.toFixed(1), r: +b.right.toFixed(1), b: +b.bottom.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1) }; };
  const wait = ms => new Promise(r => setTimeout(r, ms));

  const out = { vw: innerWidth, vh: innerHeight, vhHalf: +(innerHeight / 2).toFixed(1) };
  const header = q('header'), main = q('main.dot-bg');
  out.header = header ? R(header) : null;
  out.main = main ? R(main) : null;

  const trig = [...document.querySelectorAll('button[aria-label="技能"]')]
    .filter(b => b.getBoundingClientRect().width > 0)[0];
  if (!trig) return JSON.stringify({ err: 'no trigger' });
  out.trig = R(trig);

  trig.click();
  await wait(450);
  const pop = q('[role="listbox"][aria-label="技能选择"]');
  if (!pop) return JSON.stringify({ err: 'no popup' });

  out.pop = R(pop);
  const cs = getComputedStyle(pop);
  out.popDisplay = cs.display;
  out.popOverflowY = cs.overflowY;
  out.maxHeight = cs.maxHeight;
  out.expectMaxH = +(innerHeight * 0.5 - 120).toFixed(1);
  out.maxHMatch = Math.abs(parseFloat(cs.maxHeight) - out.expectMaxH) < 0.6;
  out.popInner = (function () {
    const inner = pop.firstElementChild;
    return inner ? { h: +inner.getBoundingClientRect().height.toFixed(1), clientH: inner.clientHeight, scrollH: inner.scrollHeight } : null;
  })();
  out.listScrollable = !!(out.popInner && out.popInner.scrollH > out.popInner.clientH + 1 &&
    ['auto', 'scroll'].includes(getComputedStyle(pop.firstElementChild).overflowY));

  if (main) {
    const m = R(main);
    out.over = +(m.t - out.pop.t).toFixed(1);          /* >0 被裁在 main 上缘之外 */
    out.under = +(out.pop.b - m.b).toFixed(1);         /* >0 被裁在 main 下缘之外 */
    out.mainOverflow = getComputedStyle(main).overflow;
  }
  if (header) {
    const h = R(header);
    out.overlapHeader = +(h.b - out.pop.t).toFixed(1); /* >0 与 header 纵向重叠 */
  }
  out.anims = pop.getAnimations().map(a => (a.animationName || a.transitionProperty || '?') + '@' + (a.effect && a.effect.getTiming ? a.effect.getTiming().duration : '?')).join(',');
  return JSON.stringify(out);
})()
