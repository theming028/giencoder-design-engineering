(() => {
  const r = document.querySelector('.td-root');
  const right = document.querySelector('.td-right');
  const slot = document.querySelector('.td-browse-slot');
  const pane = document.querySelector('.td-browse');
  const btns = [...document.querySelectorAll('.td-root button')].filter(b => b.hasAttribute('aria-pressed'));
  return {
    hasRoot: !!r, hasRight: !!right, hasSlot: !!slot, hasPane: !!pane,
    rootCls: r ? r.className : '',
    btns: btns.map(b => ({ cls: String(b.className).slice(0, 70), pressed: b.getAttribute('aria-pressed'), label: (b.getAttribute('aria-label') || b.textContent || '').trim().slice(0, 20) })),
    rightW: right ? Math.round(right.getBoundingClientRect().width) : -1,
    slotW: slot ? Math.round(slot.getBoundingClientRect().width) : -1,
    rightTrans: right ? getComputedStyle(right).transitionProperty + '/' + getComputedStyle(right).transitionDuration : '',
    slotTrans: slot ? getComputedStyle(slot).transitionProperty + '/' + getComputedStyle(slot).transitionDuration : '',
    paneAnim: pane ? getComputedStyle(pane).animationName + '/' + getComputedStyle(pane).animationDuration : ''
  };
})()
