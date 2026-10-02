(function () {
  /* 在**页面内**用 rAF/定时器密集采样，避免 CLI eval 往返延迟把窗口错过。
     记录三项：骨架屏是否在文档、data-r93-app 值、.zd-host 计算 display。 */
  if (window.__l13built) return JSON.stringify({ cached: 1, samples: window.__l13samples });
  window.__l13samples = [];
  var t0 = performance.now();
  function snap(tag) {
    var host = document.querySelector('.zd-host');
    window.__l13samples.push({
      t: Math.round(performance.now() - t0),
      tag: tag,
      sk: !!document.querySelector('.r93-sk'),
      app: document.documentElement.getAttribute('data-r93-app'),
      disp: host ? getComputedStyle(host).display : null
    });
  }
  /* 立即抓一帧（此时应在骨架屏期） */
  snap('now');
  var stops = [50, 120, 200, 300, 380, 420, 500, 600, 700, 800, 1000, 1300, 1800];
  for (var i = 0; i < stops.length; i++) {
    (function (ms) { setTimeout(function () { snap('+' + ms); }, ms); })(stops[i]);
  }
  window.__l13built = 1;
  return JSON.stringify({ built: 1, t0: Math.round(t0) });
})()
