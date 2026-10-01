/* 第十一拍 ③：读时间线结果（配合 p107l_time.js 的 rAF 轮询器） */
(function () {
  var T = window.__L11T || {};
  var sk = document.querySelector('.r93-sk');
  var out = {
    tSkOut: T.tSkOut == null ? null : Math.round(T.tSkOut),
    tSkGone: T.tSkGone == null ? null : Math.round(T.tSkGone),
    tNumVisible: T.tNum == null ? null : Math.round(T.tNum),
    gapSkToNum: (T.tSkGone != null && T.tNum != null) ? Math.round(T.tNum - T.tSkGone) : null,
    late: T.late,
    skStillInDom: !!sk,
    numAnim: null
  };
  var list = document.querySelectorAll('.r93-num-i');
  for (var i = 0; i < list.length; i++) {
    var host = list[i].closest ? list[i].closest('.r93-t14') : null;
    if (host && host.textContent.indexOf('调用') === 0) {
      var c = getComputedStyle(list[i]);
      out.numAnim = { text: list[i].textContent, ni: list[i].style.getPropertyValue('--r93-ni'),
                      delay: c.animationDelay, dur: c.animationDuration, fill: c.animationFillMode,
                      name: c.animationName };
      break;
    }
  }
  out.numCount = document.querySelectorAll('.r93-num-i').length;
  return JSON.stringify(out);
})();
