(function () {
  var mod = window.__MOD;
  var t = document.querySelector('.td-browse-tabs [data-td-tab][data-td-mod="' + mod + '"]');
  if (t) { t.click(); return 'tab:' + mod; }
  /* 该模块还没有页签 ⇒ 走「+」模块菜单建一枚（与站内既有链路同口径） */
  var b = document.querySelector('[data-td-open-mod="' + mod + '"]');
  if (b) { b.click(); return 'open:' + mod; }
  return 'miss:' + mod;
})()
