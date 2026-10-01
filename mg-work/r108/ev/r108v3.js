/* r108 第十九拍 · ② 对照实验
   A = 现状写法（摘 `[hidden]` + 加开态类，同一 tick）
   B = 两步写法（摘 `[hidden]` → 强制重排 → 加开态类）
   每例逐帧记录：opacity / translate / scale / getAnimations / 是否首帧就是终态。 */
(function () {
  var M = window.__M || 'x';
  var m = document.querySelector('.td-mod-menu');
  var trg = document.querySelector('[data-td-add]');
  function close() { m.setAttribute('hidden', ''); m.classList.remove('giencoder-popup-open'); }

  function sample(n, tag, log) {
    var c = getComputedStyle(m);
    log.push([n, tag, c.opacity, c.translate, c.scale, c.visibility,
      m.getAnimations().map(function (a) { return (a.transitionProperty || a.animationName || '?') + ':' + a.playState; }).join('|')]);
  }
  function runCase(name, twoStep) {
    return new Promise(function (res) {
      close();
      var log = []; var n = 0;
      function tick() {
        if (n === 3) {
          m.removeAttribute('hidden');
          if (twoStep) { void m.offsetWidth; }          /* ★ 强制重排 = 建立「改前样式」 */
          m.classList.add('giencoder-popup-open');
        }
        sample(n, n === 3 ? 'open' : (n < 3 ? 'pre' : 'post'), log);
        n++;
        if (n < 22) requestAnimationFrame(tick);
        else res({ name: name, twoStep: twoStep, log: log });
      }
      requestAnimationFrame(tick);
    });
  }
  if (M === 'exp') {
    window.__EXP = null;
    runCase('A 现状', false).then(function (a) {
      return new Promise(function (r) { setTimeout(function () { r(a); }, 300); });
    }).then(function (a) {
      return runCase('B 两步', true).then(function (b) { window.__EXP = [a, b]; });
    });
    return { phase: 'exp', started: 1 };
  }
  if (M === 'expRead') { return { phase: 'expRead', exp: window.__EXP }; }
  /* 复原成「关态」（别把页面留在开态） */
  if (M === 'expReset') { close(); return { phase: 'expReset', hidden: m.hasAttribute('hidden') }; }
  return { phase: M, err: 'unknown phase' };
})();
