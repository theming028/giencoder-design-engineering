/* 第十五拍 ⑤ 的**真实时序**取证：`open` 之后立刻装一个 rAF 采样器，
   记录「骨架屏还在不在」与「`.zd-host` 的 display」两条时间线。
   ⚠ 与 `skgate`（造/删假骨架屏的确定性判据）互补：这条证明**真机加载期**的行为。
   ⚠ 整段必须写在**同一次 eval** 内（跨调用就漏掉整段过渡 —— 硬规则 29）。 */
(function () {
  var host = document.querySelector('.zd-host');
  if (!host) return { err: 'no .zd-host' };
  var T = [], t0 = performance.now();
  function sk() { return document.querySelector('.r93-sk'); }
  (function tick() {
    var d = getComputedStyle(host).display;
    var last = T[T.length - 1];
    if (!last || last[1] !== d) T.push([Math.round(performance.now() - t0), d, !!sk()]);
    if (performance.now() - t0 < 1500) requestAnimationFrame(tick);
    else window.__TL = T;
  })();
  return { startedAt: Math.round(performance.now()), skNow: !!sk(),
           displayNow: getComputedStyle(host).display };
})()
