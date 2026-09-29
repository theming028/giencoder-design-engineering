(() => {
  /* 点「非当前选中」的页签，同步读回接力数据：既验证脚本解析无误，也验证捕获监听已挂上 */
  const tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
  if (!tl) return { err: 'NO TL' };
  const cur = tl.querySelector('[data-tab][aria-selected="true"]');
  const other = [...tl.querySelectorAll('[data-tab]')].find(b => b !== cur);
  if (!other) return { err: 'NO OTHER TAB' };
  const before = sessionStorage.getItem('r73-tab-relay');
  other.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  let v = null;
  try { v = sessionStorage.getItem('r73-tab-relay'); } catch (e) { v = 'ERR'; }
  return { file: location.pathname.split('/').pop(), cur: cur.getAttribute('data-tab'), clicked: other.getAttribute('data-tab'), wrote: v };
})()
