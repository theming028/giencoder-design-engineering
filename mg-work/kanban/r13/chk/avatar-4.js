
(function () {
  /* 把 <template> 里的还原标记填进 React 渲染出的空壳 .av-main。
     React 对 .av-main 没有子节点声明（bundle 已改为 <div class="av-main">），
     因此这里写入的 DOM 不会被 React 协调覆盖。 */
  var tpl = document.getElementById('av-main-tpl');
  if (!tpl) return;
  var HTML = tpl.innerHTML;
  function mount() {
    var host = document.querySelector('.av-main');
    if (!host) return false;
    if (host.getAttribute('data-av-main-ready') === '1') return true;
    host.innerHTML = HTML;
    host.setAttribute('data-av-main-ready', '1');
    return true;
  }
  if (!mount()) {
    /* React 首帧可能晚于本脚本 */
    var mo = new MutationObserver(function () { if (mount()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
