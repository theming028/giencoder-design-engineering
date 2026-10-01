/* r108 第十六拍 · 三条真机探针（相位式；`window.__M` 选相位）。
   ⚠ 只读为主；两处「临时造物」都会在同一次 eval 里还原（假红块 / 采样器）。
   ⚠ 安全取值：任何 querySelector 都可能落空（上一轮真被 TypeError 打爆过）。 */
(function () {
  var M = window.__M;
  var R = { m: M };

  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function S(el, p) { return el ? getComputedStyle(el)[p] : null; }
  function rect(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)];
  }

  var host = q('.zd-host');
  var card = q('[data-zd-card]');
  var mini = q('[data-zd-mini]');
  var pane = q('.td-browse');
  var prevPane = q('#av-browse-pane-preview');

  /* 标签栏快照 */
  function tabInfo() {
    return qa('.td-browse-tabs [data-td-tab]').map(function (t) {
      var nm = q('.td-tab-name', t);
      return {
        mod: t.getAttribute('data-td-mod'),
        name: nm ? nm.textContent : null,
        active: t.classList.contains('is-active'),
        ico: !!q('.td-tab-ico svg', t),
        x: !!q('[data-td-tab-x]', t),
        ctl: t.getAttribute('aria-controls')
      };
    });
  }
  function paneInfo() {
    return qa('.td-browse [data-td-pane], .td-browse .td-browse-body').map(function (p) {
      return {
        mod: p.classList.contains('td-browse-body') ? 'files' : p.getAttribute('data-td-pane'),
        hidden: p.hasAttribute('hidden'),
        display: S(p, 'display')
      };
    });
  }
  function prevInfo() {
    if (!prevPane) return null;
    var bar = q('.td-mod-bar', prevPane);
    var barH = bar ? Math.round(bar.getBoundingClientRect().height) : null;
    function body(kind) {
      var b = q('[data-td-prev-kind="' + kind + '"]', prevPane);
      return b ? { display: S(b, 'display'), hidden: b.hasAttribute('hidden') } : null;
    }
    return {
      hidden: prevPane.hasAttribute('hidden'),
      display: S(prevPane, 'display'),
      rect: rect(prevPane),
      barH: barH,
      name: (q('[data-td-prev-name]', prevPane) || {}).textContent,
      meta: (q('[data-td-prev-meta]', prevPane) || {}).textContent,
      icoSvg: !!q('[data-td-prev-ico] svg', prevPane),
      md: body('md'), xlsx: body('xlsx'),
      openBtn: !!q('[data-td-prev-open]', prevPane)
    };
  }
  /* 侧栏四个模块工具条高度（本模块必须与它们对齐） */
  function barHeights() {
    return qa('.td-browse [data-td-pane] > .td-mod-bar').map(function (b) {
      var sec = b.parentElement;
      return { mod: sec.getAttribute('data-td-pane'), h: Math.round(b.getBoundingClientRect().height) };
    });
  }
  function clickArt(i) {
    var a = qa('.td-browse [data-td-art]')[i];
    if (!a) return 'no-art' + i;
    var b = q('.td-diff-btn', a);
    if (!b) return 'no-btn' + i;
    b.click();
    return 'clicked' + i;
  }

  /* ---------------- base：③ 毛玻璃 + ② 锚点 + ① 旧浮层归零 ---------------- */
  if (M === 'base') {
    R.host = { display: S(host, 'display'), rect: rect(host) };
    /* ⚠ 侧栏初始可能是**收起**态（`ensureOpen()` 就是为此存在）⇒ 首帧量到的
       `.td-browse` / 面板矩形会是「滑入中」的位置。这里把开关状态也记下来，
       免得把「过渡中取值」误判成「面板跑到视口外」（硬规则 29）。 */
    R.slot = (function () {
      var s = q('#av-browse-slot');
      return s && s.parentElement
        ? { cls: s.parentElement.className, browseRect: rect(q('.td-browse')), vw: window.innerWidth }
        : null;
    })();
    R.glass = [
      ['card', leaf(card)],
      ['mini', leaf(mini)],
      ['menuBranch', leaf(q('.zd-menu-branch'))],
      ['menuCommit', leaf(q('.zd-menu-commit'))],
      ['toast', leaf(q('.zd-toast'))]
    ];
    R.glassSupport = {
      backdrop: window.CSS && CSS.supports ? CSS.supports('backdrop-filter', 'blur(2px)') : 'n/a',
      webkit: window.CSS && CSS.supports ? CSS.supports('-webkit-backdrop-filter', 'blur(2px)') : 'n/a',
      colorMix: window.CSS && CSS.supports ? CSS.supports('color', 'color-mix(in srgb, #fff 50%, transparent)') : 'n/a'
    };
    R.origin = {
      card: S(card, 'transformOrigin'), mini: S(mini, 'transformOrigin'),
      menu: S(q('.zd-menu-branch'), 'transformOrigin')
    };
    R.anim = {
      cardTransition: S(card, 'transition'),
      cardInAnim: S(card, 'animationName')
    };
    R.tabs0 = tabInfo();
    R.panes0 = paneInfo();
    R.residue = {
      overlay: !!q('.td-sum-prev'),
      overlaySel: !!q('[data-td-prev]'),
      paneCount: qa('#av-browse-pane-preview').length,
      sumPos: S(q('.td-mod.td-sum'), 'position'),
      prevElGlobal: typeof window.prevEl
    };
    R.artButtons = qa('.td-browse [data-td-art]').length;
  }
  function leaf(el) {
    if (!el) return null;
    return {
      bg: S(el, 'backgroundColor'),
      bdf: S(el, 'backdropFilter') || S(el, 'webkitBackdropFilter'),
      hidden: el.hasAttribute('hidden'),
      display: S(el, 'display'),
      rect: rect(el)
    };
  }

  /* ---------------- 侧栏安定后复量（把「过渡中取值」剔掉） ---------------- */
  if (M === 'slot') {
    var s2 = q('#av-browse-slot');
    R.cls = s2 && s2.parentElement ? s2.parentElement.className : null;
    R.browseRect = rect(q('.td-browse'));
    R.vw = window.innerWidth;
    R.prev = prevInfo();
    R.bars = barHeights();
    R.tabs = tabInfo();
  }

  /* ---------------- ① 预览页签 ---------------- */
  if (M === 'pvA') { R.act = clickArt(0); }
  if (M === 'pvB') { R.act = clickArt(1); }
  if (M === 'pvC') {
    var xt = q('[data-td-mod="preview"] [data-td-tab-x]');
    R.act = xt ? 'x-click' : 'no-x';
    if (xt) xt.click();
  }
  if (M === 'pvD') {
    R.a = clickArt(1);
    var sum = q('[data-td-mod="summary"]');
    if (sum) sum.click();
    R.afterSummary = 1;
  }
  if (M === 'pvE') {
    var pvt = q('[data-td-mod="preview"]');
    R.act = pvt ? 'tab-click' : 'no-preview-tab';
    if (pvt) pvt.click();
    /* 顺带：预览页签的面板必须有 `data-td-pane`，且被 activate 正常裁决 */
    R.tabList = tabInfo();
    R.panes = paneInfo();
    R.prev = prevInfo();
    R.bars = barHeights();
  }
  if (/^pv[ABCD]$/.test(M)) {
    R.tabs = tabInfo();
    R.panes = paneInfo();
    R.prev = prevInfo();
    R.bars = barHeights();
    R.tabCount = qa('.td-browse-tabs [data-td-tab]').length;
    R.prevTabCount = qa('.td-browse-tabs [data-td-tab][data-td-mod="preview"]').length;
    R.sumTag = (q('.td-sum-tag') || {}).textContent;
  }

  /* ---------------- ② 收 / 展：同一次 eval 内「点 + 采样」 ---------------- */
  function sampler(triggerSel, span) {
    var rec = [];
    var t0 = performance.now();
    var btn = q(triggerSel);
    if (!btn) return 'no-trigger';
    function tick() {
      var cs = card ? getComputedStyle(card) : null;
      var ms = mini ? getComputedStyle(mini) : null;
      if (cs) {
        rec.push([Math.round(performance.now() - t0),
                  cs.scale, cs.translate, cs.opacity,
                  card.hasAttribute('hidden') ? 'H' : 'c',
                  mini ? (mini.hasAttribute('hidden') ? 'h' : 'm') : '-',
                  cs.animationName, ms ? ms.transformOrigin : null]);
      }
      if (performance.now() - t0 < span) requestAnimationFrame(tick);
      else finish();
    }
    function finish() {
      /* 压缩：只留「状态四元组变化」的帧 */
      var out = [], last = null;
      for (var i = 0; i < rec.length; i++) {
        var k = rec[i][1] + '|' + rec[i][2] + '|' + rec[i][3] + '|' + rec[i][4] + '|' + rec[i][5] + '|' + rec[i][6];
        if (k !== last) { out.push(rec[i]); last = k; }
      }
      window.__REC = out;
      window.__RECN = rec.length;
    }
    requestAnimationFrame(tick);
    btn.click();
    return 'started';
  }
  if (M === 'swapOut') {
    R.before = { cardOrigin: S(card, 'transformOrigin'), cardScale: S(card, 'scale'),
                 cardT: S(card, 'translate'), miniHidden: mini ? mini.hasAttribute('hidden') : null,
                 cardRect: rect(card) };
    R.act = sampler('[data-zd-min]', 820);
  }
  if (M === 'swapIn') {
    R.act = sampler('[data-zd-mini]', 820);
  }
  if (M === 'swapEnd') {
    R.rec = window.__REC || null;
    R.recN = window.__RECN || 0;
    R.now = {
      cardHidden: card ? card.hasAttribute('hidden') : null,
      cardOrigin: S(card, 'transformOrigin'),
      miniHidden: mini ? mini.hasAttribute('hidden') : null,
      miniOrigin: S(mini, 'transformOrigin'),
      miniRect: rect(mini),
      cardRect: rect(card)
    };
  }

  /* ---------------- ③ 毛玻璃的像素取证：临时在卡片正下方塞一块纯红 ---------------- */
  if (M === 'glassOn') {
    var r0 = card ? card.getBoundingClientRect() : null;
    var old = q('#zzGlass');
    if (old) old.parentNode.removeChild(old);
    var d = document.createElement('div');
    d.id = 'zzGlass';
    d.setAttribute('style', 'position:fixed;left:' + Math.round(r0.left) + 'px;top:' + Math.round(r0.top)
      + 'px;width:' + Math.round(r0.width) + 'px;height:' + Math.round(Math.min(180, r0.height))
      + 'px;background:#FF0000;z-index:5;pointer-events:none');
    document.body.appendChild(d);
    R.block = rect(d);
    R.cardRect = rect(card);
    R.sampleAt = [Math.round(r0.left + r0.width / 2), Math.round(r0.top + 60)];
  }
  if (M === 'glassOff') {
    var z = q('#zzGlass');
    if (z) z.parentNode.removeChild(z);
    R.removed = !q('#zzGlass');
  }

  /* ---------------- 边界档 ---------------- */
  if (M === 'dark') {
    R.theme = document.documentElement.getAttribute('giencoder-theme');
    R.glass = [['card', leaf(card)], ['mini', leaf(mini)], ['menuBranch', leaf(q('.zd-menu-branch'))]];
    R.origin = { card: S(card, 'transformOrigin') };
  }
  if (M === 'fs') {
    R.uiFs = S(document.documentElement, '--ui-fs');
    R.glass = [['card', leaf(card)]];
    R.tabs = tabInfo();
    R.bars = barHeights();
  }

  return JSON.stringify(R);
})();
