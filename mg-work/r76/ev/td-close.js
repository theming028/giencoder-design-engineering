/* r76 · 任务详情：展开 → 收起，逐帧记录 .td-right 的精确几何（浮点），
   用于判定「td-browse-slot 关闭后 td-right 回弹」。
   一次调用内闭环（agent-browser eval 支持 await）。 */
(async () => {
  const g = s => document.querySelector(s);
  const R = g('.td-root');
  const btn = () => [...document.querySelectorAll('.td-right-bar button[aria-pressed]')]
    .find(x => (x.getAttribute('aria-label') || '').indexOf('侧栏') >= 0);

  const snap = () => {
    const ri = g('.td-right'), sl = g('.td-browse-slot'), lf = g('.td-left');
    const rb = ri.getBoundingClientRect();
    const cs = getComputedStyle(ri);
    return {
      b: R.classList.contains('is-browse') ? 1 : 0,
      kl: R.classList.contains('is-keep-left') ? 1 : 0,
      pc: (g('.td-browse') && g('.td-browse').classList.contains('is-closing')) ? 1 : 0,
      rL: +rb.left.toFixed(2), rR: +rb.right.toFixed(2), rW: +rb.width.toFixed(2),
      sW: sl ? +sl.getBoundingClientRect().width.toFixed(2) : -1,
      lW: lf ? +lf.getBoundingClientRect().width.toFixed(2) : -1,
      brw: cs.borderRightWidth, rr: cs.borderTopRightRadius,
      tf: cs.transform
    };
  };

  const rec = (ms) => new Promise(res => {
    const out = [], t0 = performance.now();
    const tick = () => {
      out.push(Object.assign({ t: Math.round(performance.now() - t0) }, snap()));
      if (performance.now() - t0 < ms) requestAnimationFrame(tick); else res(out);
    };
    requestAnimationFrame(tick);
  });

  const b1 = btn();
  if (!b1) return 'NOBTN';
  b1.click();
  await new Promise(r => setTimeout(r, 700));       /* 等展开稳定 */
  const open = snap();
  const b2 = btn();
  if (!b2) return 'NOBTN2';
  b2.click();
  const seq = await rec(700);
  await new Promise(r => setTimeout(r, 300));
  const rest = snap();
  return JSON.stringify({ vw: innerWidth, vh: innerHeight, open, seq, rest });
})()
