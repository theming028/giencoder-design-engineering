/* r76 · 收起过程截图序列：在指定时刻把页面「冻结」住再截图。
   用法：window.__SHOT = [0,100,200,240,260,320]（毫秒）
   agent-browser 侧每帧：eval 设 window.__SEEK → eval 读状态 → screenshot */
(async () => {
  const R = document.querySelector('.td-root');
  const btn = () => [...document.querySelectorAll('.td-right-bar button[aria-pressed]')]
    .find(x => (x.getAttribute('aria-label') || '').indexOf('侧栏') >= 0);
  const cs = getComputedStyle(R);
  const vars = {};
  ['--td-right-w', '--td-browse-right-w', '--td-left-keep-w', '--td-left-min', '--td-gap']
    .forEach(v => vars[v] = cs.getPropertyValue(v).trim());

  const mode = window.__M || 'open';
  if (mode === 'open') {
    if (!R.classList.contains('is-browse')) btn().click();
    return JSON.stringify({ vars, act: 'opened' });
  }
  if (mode === 'start') {
    /* 点关闭，并立即把所有相关过渡/动画暂停在 t=0 —— 用 WAAPI 逐个 pause */
    btn().click();
    await new Promise(r => requestAnimationFrame(r));
    const all = document.getAnimations ? document.getAnimations() : [];
    window.__AN = all.map(a => { try { a.pause(); a.currentTime = 0; } catch (e) {} return a; });
    return JSON.stringify({ vars, anims: all.length });
  }
  if (mode === 'seek') {
    const t = Number(window.__T || 0);
    let n = 0;
    (window.__AN || []).forEach(a => { try { a.currentTime = t; n++; } catch (e) {} });
    /* 非 WAAPI 的 CSS transition 无法 seek —— 用 getAnimations 拿到的 CSSAnimation 可以，
       CSSTransition 也支持 currentTime。 */
    return JSON.stringify({ t: t, seeked: n });
  }
  return 'ERRMODE';
})()
