(() => {
  const out = {};
  // ① 权限选择：开 → 关 的节点存在性
  const perm = document.querySelectorAll('.giencoder-select-view.ws-dropdown-hover')[1];
  const find = () => document.querySelector('[role="listbox"][aria-label="权限选择"]');
  out.perm0 = !!find();
  perm.click();
  setTimeout(() => {
    const e = find();
    out.permOpen = e ? { inline: (e.getAttribute('style') || '').slice(0, 90), an: e.getAnimations().map(a => a.animationName || 'T:' + a.transitionProperty).join(','),
                          trs: getComputedStyle(e).transition.slice(0, 90), disp: getComputedStyle(e).display, vis: getComputedStyle(e).visibility, op: getComputedStyle(e).opacity } : null;
    perm.click();
    setTimeout(() => {
      const e2 = find();
      out.permClose = e2 ? { inDom: true, disp: getComputedStyle(e2).display, vis: getComputedStyle(e2).visibility, op: getComputedStyle(e2).opacity } : { inDom: false };
      window.__REST = out;
    }, 300);
  }, 300);
  return 'started';
})()
