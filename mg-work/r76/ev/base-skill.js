/* r76 · base.html：技能选择浮窗在「纵向空间不足」时的几何关系
   输出：header / main / 触发器 / 浮窗 的 rect + 浮窗内联 style + 是否被 main 裁切 */
(async () => {
  const q = s => document.querySelector(s);
  const R = e => { const b = e.getBoundingClientRect(); return { l: +b.left.toFixed(1), t: +b.top.toFixed(1), r: +b.right.toFixed(1), b: +b.bottom.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1) }; };

  /* 触发器 = 输入框里那颗「技能」按钮（精确锚点 aria-label="技能"，别用 textContent
     —— 左导航的「技能 Skills」也含这两个字，点了会跳页） */
  const cands = [...document.querySelectorAll('button[aria-label="技能"]')]
    .filter(b => b.getBoundingClientRect().width > 0);
  const info = { vw: innerWidth, vh: innerHeight, nTrig: cands.length };

  const header = q('header');
  const main = q('main.dot-bg');
  info.header = header ? R(header) : null;
  info.main = main ? R(main) : null;
  info.triggers = cands.map(b => ({ label: (b.getAttribute('aria-label') || b.title || b.textContent || '').trim().slice(0, 16), rect: R(b) }));
  if (!cands.length) return JSON.stringify(info);

  cands[0].click();
  await new Promise(r => setTimeout(r, 450));
  const pop = q('[role="listbox"][aria-label="技能选择"]');
  if (pop) {
    info.pop = R(pop);
    info.popStyle = (pop.getAttribute('style') || '').slice(0, 400);
    info.popParentCls = pop.parentElement ? String(pop.parentElement.className).slice(0, 120) : '';
    const cs = getComputedStyle(pop);
    info.popPos = { position: cs.position, bottom: cs.bottom, top: cs.top };
    /* 被 main 裁切判定 */
    if (main) {
      const m = R(main);
      info.clipTop = +(m.t - info.pop.t).toFixed(1);      /* >0 ⇒ 浮窗顶端超出 main 上缘 */
      info.mainOverflow = getComputedStyle(main).overflow;
    }
    if (header) {
      const h = R(header);
      info.overlapHeader = +(h.b - info.pop.t).toFixed(1); /* >0 ⇒ 与 header 纵向重叠 */
      info.headerZ = getComputedStyle(header).zIndex;
    }
    /* 祖先链上谁在裁切 */
    const chain = [];
    let el = pop.parentElement;
    while (el && el !== document.documentElement) {
      const c = getComputedStyle(el);
      if (c.overflow !== 'visible' && c.overflow !== '') chain.push(el.tagName + '.' + String(el.className).slice(0, 40) + ' {overflow:' + c.overflow + '}');
      el = el.parentElement;
    }
    info.clippers = chain;
  } else info.pop = null;
  return JSON.stringify(info);
})()
