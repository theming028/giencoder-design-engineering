/* 第十一拍 ③：数字动效真实时间线。
   在页面加载后**立刻**装一个 rAF 轮询器，记录三个时间点（都相对 performance timeOrigin）：
     tNum  = 目标数字（「调用 5 个工具」里那枚 `5`）首次 opacity > 0.5 的时刻
     tSkGone = `.r93-sk` 骨架屏从 DOM 消失的时刻
     tSkOut  = 骨架屏被加 `.is-out`（开始淡出）的时刻
   若首次轮询时数字**已经可见**，说明探针起跑太晚 ⇒ tNum 记为首轮时间并标注 late=1。 */
(function () {
  var T = { t0: performance.now(), tNum: null, tSkOut: null, tSkGone: null, late: 0, ni: null, probe: null };
  function target() {
    var list = document.querySelectorAll('.r93-num-i');
    for (var i = 0; i < list.length; i++) {
      var el = list[i];
      var host = el.closest ? el.closest('.r93-t14') : null;
      if (host && host.textContent.indexOf('调用') === 0) { T.ni = el.style.getPropertyValue('--r93-ni'); return el; }
    }
    return null;
  }
  var sk0 = document.querySelector('.r93-sk');
  var el0 = target();
  if (el0 && parseFloat(getComputedStyle(el0).opacity) > 0.5) { T.tNum = T.t0; T.late = 1; }
  if (!sk0) { T.tSkGone = T.t0; }
  (function poll() {
    if (T.tNum == null) {
      var el = target();
      if (el && parseFloat(getComputedStyle(el).opacity) > 0.5) T.tNum = performance.now();
    }
    var sk = document.querySelector('.r93-sk');
    if (sk && T.tSkOut == null && sk.classList.contains('is-out')) T.tSkOut = performance.now();
    if (!sk && T.tSkGone == null && T.tSkOut != null) T.tSkGone = performance.now();
    if (T.tNum != null && T.tSkGone != null) { window.__L11T = T; return; }
    if (performance.now() < 12000) requestAnimationFrame(poll);
    else window.__L11T = T;
  })();
  window.__L11T = T;
  return 'armed';
})();
