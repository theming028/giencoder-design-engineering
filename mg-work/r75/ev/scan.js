(() => {
  const out = { page: location.pathname.split('/').pop(), list: [] };
  document.querySelectorAll('.giencoder-select').forEach((root, i) => {
    const v = root.querySelector('.giencoder-select-view');
    if (!v) return;
    const r = v.getBoundingClientRect();
    if (r.width === 0) return;                      // ★ 只挑可见控件
    const pop = root.querySelector('.giencoder-select-popup');
    const item = { i: i, view: Math.round(r.x) + ',' + Math.round(r.y), txt: (v.textContent || '').trim().slice(0, 10) };
    if (pop) { const c = getComputedStyle(pop);
      item.pop = { inline: (pop.getAttribute('style') || '').slice(0, 30), disp: c.display, vis: c.visibility, op: c.opacity };
      let a = pop.parentElement, d = 0, chain = [];
      while (a && d < 6) { const cc = getComputedStyle(a); if (cc.display === 'none' || cc.visibility === 'hidden') chain.push(d + ':' + a.tagName + '=' + cc.display + '/' + cc.visibility); a = a.parentElement; d++; }
      item.hiddenAnc = chain.length ? chain : 'none';
    }
    // 其他自定义浮层
    item.others = Array.from(root.querySelectorAll('[role="listbox"], [role="menu"]')).map(e => {
      const c = getComputedStyle(e); return (e.getAttribute('aria-label') || '?') + ':' + (e.getAttribute('style') || '').slice(0, 26) + '|' + c.display + '/' + c.visibility;
    });
    out.list.push(item);
  });
  return JSON.stringify(out);
})()
