(() => {
  function bg(el) {
    if (!el) return null;
    const cs = getComputedStyle(el);
    return { bg: cs.backgroundColor, bgi: cs.backgroundImage, bd: cs.backdropFilter };
  }
  window.__ev = function () {
    const out = { page: location.pathname.split('/').pop(), themeAttr: document.documentElement.getAttribute('giencoder-theme') || '(none)' };
    // 下拉面板类
    const sels = {
      selectPopup: '.giencoder-select-popup',
      skillsPopup: '.skills-popup-bg',
      tdSkill: '.td-skill-pop',
      mainDot: 'main.dot-bg',
      anyDot: '.dot-bg',
    };
    out.panels = {};
    for (const k in sels) {
      const el = document.querySelector(sels[k]);
      out.panels[k] = { found: !!el, ...(bg(el) || {}) };
    }
    // 计算 main.dot-bg 的实际背景图
    const m = document.querySelector('main.dot-bg');
    out.mainDotBgImg = m ? getComputedStyle(m).backgroundImage.slice(0, 120) : null;
    return out;
  };
  return 'ready';
})()
