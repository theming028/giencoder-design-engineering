(() => {
  // 真机验证：给 html 打标记后，只有该页的 .dot-bg 背景被清掉
  const st = document.createElement('style');
  st.id = '__dotstest';
  st.textContent = 'html[data-r109-page="settings"] .dot-bg{background-image:none !important;}';
  document.head.appendChild(st);
  document.documentElement.setAttribute('data-r109-page', 'settings');
  const m = document.querySelector('main');
  window.__t = function () {
    return { bgi: getComputedStyle(m).backgroundImage, attr: document.documentElement.getAttribute('data-r109-page') };
  };
  return 'ok';
})()
