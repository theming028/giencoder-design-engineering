/* r76 · base.html：技能浮窗的可用纵向空间随视口的变化规律
   用法：window.__W 设宽度、window.__H 设高度由外层循环控制（这里只读当前视口） */
(async () => {
  const R = e => { const b = e.getBoundingClientRect(); return { t: +b.top.toFixed(1), b: +b.bottom.toFixed(1), h: +b.height.toFixed(1), l: +b.left.toFixed(1), w: +b.width.toFixed(1) }; };
  const main = document.querySelector('main.dot-bg');
  const bt = document.querySelector('button[aria-label="技能"]');
  const trig = R(bt);
  bt.click();
  await new Promise(r => setTimeout(r, 400));
  const p = document.querySelector('[role="listbox"][aria-label="技能选择"]');
  const card = p ? p.offsetParent : null;
  const cardR = card ? R(card) : null;
  const pR = R(p);
  const list = p ? p.querySelector('.skill-pop-list') : null;
  return JSON.stringify({
    vw: innerWidth, vh: innerHeight,
    mainT: R(main).t, mainB: R(main).b, mainH: R(main).h,
    trigT: trig.t,
    cardT: cardR && cardR.t, cardH: cardR && cardR.h,
    popT: pR.t, popB: pR.b, popH: pR.h,
    over: +(R(main).t - pR.t).toFixed(1),      /* >0 ⇒ 超出 main 上缘 */
    avail: +(cardR.t - 8 - R(main).t).toFixed(1),  /* 理论可用高 */
    listH: list ? +list.getBoundingClientRect().height.toFixed(1) : null,
    popH_inline: p ? p.style.height : null
  });
})()
