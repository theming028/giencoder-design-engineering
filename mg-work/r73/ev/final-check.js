(() => {
  const isBtn = el => {
    const tag = el.tagName.toLowerCase();
    if (tag === 'button' || tag === 'a' || el.getAttribute('role') === 'button') return true;
    return /btn|button|-tb$|-upbtn|refresh|pagination-item|close-btn|main-edit|-link$|round-btn|browse-add|browse-ico|expand-btn|coop-btn/.test(el.className || '');
  };
  let n4 = 0, n6 = 0;
  const offenders = [];
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return;
    const r = cs.borderTopLeftRadius;
    if (r === '4px' && isBtn(el)) { n4++; if (offenders.length < 6) offenders.push(el.className.slice(0, 50)); }
    if (r === '6px' && isBtn(el)) n6++;
  });
  const pop = document.querySelector('[data-td-add-pop]');
  const pc = pop ? getComputedStyle(pop) : null;
  return {
    file: location.pathname.split('/').pop(),
    btn4px: n4, btn6px: n6, offenders: offenders,
    addPopTransition: pc ? pc.transitionProperty + ' / ' + pc.transitionDuration : null,
    hasRelay: !!document.getElementById('r73-tab-relay'),
    hasPopupCss: !!document.getElementById('r73-popup-css'),
    hasRadiusCss: !!document.getElementById('r73-radius-css')
  };
})()
