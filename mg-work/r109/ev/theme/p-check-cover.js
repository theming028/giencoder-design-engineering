(() => {
  const st = document.createElement('style');
  st.id = '__cover';
  st.textContent = `
  html[giencoder-theme='dark'] [role="menu"][aria-label="添加内容"],
  html[giencoder-theme='dark'] [role="listbox"][aria-label="权限选择"],
  html[giencoder-theme='dark'] [role="listbox"][aria-label="技能选择"]{
    background: rgba(var(--gray-1), 0.88) !important;
  }`;
  document.head.appendChild(st);
  return 'ok';
})()
