(() => {
  /* 模拟真实点击「研发工作台」页签：window 捕获记录必须先于 document 捕获的跳转兜底 */
  const b = document.querySelector('[data-tab="dev"]');
  if (!b) return 'NO TAB';
  b.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  let v = null;
  try { v = sessionStorage.getItem('r73-tab-relay'); } catch (e) { v = 'ERR ' + e; }
  return { wrote: v, curSel: (document.querySelector('[data-tab][aria-selected="true"]') || {}).getAttribute ? document.querySelector('[data-tab][aria-selected="true"]').getAttribute('data-tab') : '?' };
})()
