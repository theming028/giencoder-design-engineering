/* r76 · 验收 3：数字分身 main 内容的「亮相」动效
   fill: both ⇒ 动画播完后仍留在时间轴上，可以回拨 currentTime 复现任意帧。
   window.__M = 'probe' | 'seek'（seek 用 window.__T） */
(async () => {
  const SEL = '.av-main-head, .av-main-rule, .av-main-grid > *, .av-main-rows > *, .av-main-foot';
  const els = [...document.querySelectorAll(SEL)];
  const M = window.__M || 'probe';

  if (M === 'probe') {
    const rows = els.map((e, i) => {
      const ans = e.getAnimations().filter(a => a.animationName === 'r76-av-in');
      const a = ans[0];
      const cs = getComputedStyle(e);
      return {
        i,
        cls: String(e.className).split(' ')[0] || e.tagName,
        n: ans.length,
        delay: a ? a.effect.getTiming().delay : null,
        dur: a ? a.effect.getTiming().duration : null,
        play: a ? a.playState : '-',
        op: cs.opacity, tr: cs.translate,
        firstKf: a ? JSON.stringify(a.effect.getKeyframes()[0].toJSON ? a.effect.getKeyframes()[0] : {}) : '-'
      };
    });
    return JSON.stringify({
      count: els.length,
      rows,
      reduced: matchMedia('(prefers-reduced-motion: reduce)').matches
    });
  }

  if (M === 'seek') {
    const t = Number(window.__T || 0);
    let n = 0;
    els.forEach(e => e.getAnimations().forEach(a => {
      if (a.animationName !== 'r76-av-in') return;
      try { a.pause(); a.currentTime = t; n++; } catch (err) {}
    }));
    await new Promise(r => requestAnimationFrame(r));
    await new Promise(r => requestAnimationFrame(r));
    const ops = els.map(e => +parseFloat(getComputedStyle(e).opacity).toFixed(2));
    return 'seek ' + t + ' → 命中 ' + n + ' 条；各块 opacity = [' + ops.join(', ') + ']';
  }
  return 'ERRMODE';
})()
