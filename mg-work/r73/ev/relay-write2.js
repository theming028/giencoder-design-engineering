(() => {
  const b = document.querySelector('[data-tab="base"]');
  if (!b) return 'NO TAB';
  b.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  let v = null;
  try { v = sessionStorage.getItem('r73-tab-relay'); } catch (e) { v = 'ERR'; }
  return { wrote: v };
})()
