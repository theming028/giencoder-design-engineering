/* r108 第十九拍 · ② 菜单入场取证 v2
   比 v1 多问三件事：
   ▸ 关态 `/ 开态` 的 computed `display`（判「`[hidden]` 到底压不压得住 `.giencoder-dropdown-popup{display:flex}`」）
   ▸ 每帧 `menu.getAnimations()`（判「过渡到底跑没跑」）
   ▸ 侧栏真正滑进视口之后再点 `+`（用户实际场景） */
(function () {
  var M = window.__M || 'x';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(e, p) { return e ? getComputedStyle(e)[p] : null; }
  var out = { phase: M };

  function act(mod) {
    var t = qa('.td-browse-tabs [data-td-tab]').filter(function (x) {
      return x.getAttribute('data-td-mod') === mod;
    })[0];
    if (t) { t.click(); return 'tab:' + mod; }
    var o = q('[data-td-open-mod="' + mod + '"]');
    if (o) { o.click(); return 'open:' + mod; }
    return 'miss:' + mod;
  }

  if (M === 'openSide') {
    out.done = [act('terminal'), act('browser'), act('review')];
    out.browse = r(q('.td-browse'));
    out.slot = r(q('.td-browse-slot'));
  }
  if (M === 'in') {
    out.browse = r(q('.td-browse'));
    out.addBtn = r(q('[data-td-add]'));
    var m = q('.td-mod-menu');
    out.menuDisplay = cs(m, 'display');
    out.menuVis = cs(m, 'visibility');
    out.menuHidden = m.hasAttribute('hidden');
    out.menuAnims = m.getAnimations().map(function (a) {
      return (a.transitionProperty || a.animationName || '?') + ':' + a.playState;
    });
    out.r93Scroll = r(q('.r93-scroll'));
  }
  /* 采样：display / visibility / opacity / translate / scale / offsetLeft / offsetTop /
           getAnimations / 触发器 rect（判「菜单有没有在关态就占位」） */
  if (M === 'arm2') {
    var mm = q('.td-mod-menu'), trg = q('[data-td-add]');
    var log = []; var n = 0;
    window.__LOG2 = log;
    function samp(tag) {
      var c = getComputedStyle(mm);
      var tr = trg.getBoundingClientRect();
      log.push([n, tag, c.display, c.visibility, c.opacity, c.translate, c.scale,
        mm.offsetLeft, mm.offsetTop, mm.offsetWidth, mm.offsetHeight,
        mm.hasAttribute('hidden') ? 0 : 1,
        /giencoder-popup-open/.test(mm.className) ? 1 : 0,
        mm.style.left || '', mm.style.top || '',
        mm.getAnimations().map(function (a) { return (a.transitionProperty || a.animationName || '?'); }).join('|'),
        Math.round(tr.left), Math.round(tr.top)]);
    }
    function tick() {
      if (n === 4 && trg) trg.click();
      samp(n < 4 ? 'pre' : (n === 4 ? 'click' : 'post'));
      n++;
      if (n < 34) requestAnimationFrame(tick); else window.__ARM2DONE = 1;
    }
    requestAnimationFrame(tick);
  }
  if (M === 'read2') { out.done = window.__ARM2DONE || 0; out.log = window.__LOG2; }

  /* 关态再验一次「`[hidden]` 压不压得住」：只摘 `[hidden]`、不加开态类 */
  if (M === 'probeHidden') {
    var m3 = q('.td-mod-menu');
    out.before = [cs(m3, 'display'), cs(m3, 'visibility'), m3.hasAttribute('hidden')];
    m3.removeAttribute('hidden');
    out.afterShow = [cs(m3, 'display'), cs(m3, 'visibility'), cs(m3, 'opacity'), r(m3)];
    m3.setAttribute('hidden', '');
  }
  return out;
})();
