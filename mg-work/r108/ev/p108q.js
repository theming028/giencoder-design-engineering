/* r108 第十五拍 · 六条真机探针（相位式；`window.__M` 选相位）。
   ⚠ 本文件只读 + 临时造/删一个假骨架屏；不改产品代码。
   ⚠ 安全取值：任何 `document.querySelector` 都可能落空（上一轮真被 TypeError 打爆过）。 */
(function () {
  var M = window.__M;
  var R = { m: M };

  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function S(el, p) { return el ? getComputedStyle(el)[p] : null; }
  function S2(el, p, pseudo) { return el ? getComputedStyle(el, pseudo)[p] : null; }
  function rect(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)];
  }
  function px(v) { return v === null || v === undefined ? null : String(v); }

  var host = q('.zd-host');
  var card = q('[data-zd-card]');
  var mini = q('[data-zd-mini]');
  var secs = qa('.zd-sec');

  /* ---------------- base：① ③ ④ ⑥ 的静态读数 ---------------- */
  if (M === 'base') {
    R.hostDisplay = S(host, 'display');
    R.cardHidden = card ? card.hasAttribute('hidden') : null;

    /* ① 三个分区标题的 computed */
    R.secT = secs.map(function (s) {
      var t = q('.zd-sec-t', s);
      return {
        kind: s.getAttribute('data-zd-sec'),
        text: t ? t.textContent.trim() : null,
        fs: S(t, 'fontSize'), fw: S(t, 'fontWeight'), color: S(t, 'color'),
        lh: S(t, 'lineHeight'), disp: S(t, 'display'),
        cv: !!q('.zd-cv', s)
      };
    });

    /* ⑥ 分区头 trailing：默认（展开）应 display:none */
    R.secX_default = secs.map(function (s) {
      var x = q('.zd-sec-x', s);
      return {
        kind: s.getAttribute('data-zd-sec'),
        closed: s.classList.contains('is-closed'),
        display: S(x, 'display'), flex: S(x, 'flex'),
        text: x ? x.textContent.trim() : null
      };
    });

    /* ③ 目标：只应剩一条，且是「进行中 3/4」那条 */
    var goal = q('.zd-sec[data-zd-sec="goal"]');
    R.goal = {
      rows: qa('.zd-it', goal).length,
      no: qa('.zd-it-no', goal).length,
      icon: qa('.zd-it-i', goal).length,
      texts: qa('.zd-it-t', goal).map(function (p) { return p.textContent.trim(); }),
      counts: qa('.zd-it-c', goal).map(function (p) { return p.textContent.trim(); })
    };

    /* ④ 进程三态 */
    var lis = qa('.zd-todo li');
    R.todo = lis.map(function (li) {
      return {
        cls: li.className,
        text: li.textContent.trim().slice(0, 20),
        color: S(li, 'color'),
        deco: S(li, 'textDecorationLine'),
        before: {
          bg: S2(li, 'backgroundColor', '::before'),
          bc: S2(li, 'borderTopColor', '::before'),
          op: S2(li, 'opacity', '::before'),
          rect: rect(li)
        },
        after: {
          content: S2(li, 'content', '::after'),
          bt: S2(li, 'borderTopColor', '::after'),
          bl: S2(li, 'borderLeftColor', '::after'),
          radius: S2(li, 'borderRadius', '::after'),
          anim: S2(li, 'animationName', '::after'),
          dur: S2(li, 'animationDuration', '::after'),
          tf: S2(li, 'transform', '::after')
        }
      };
    });

    /* ② 操作图标：清点（hover 读数另起相位） */
    R.icos = qa('.zd-ico').map(function (b) {
      return { title: b.getAttribute('title'), disp: S(b, 'display'),
               bg: S(b, 'backgroundColor'), color: S(b, 'color'),
               radius: S(b, 'borderRadius'), cursor: S(b, 'cursor'),
               rect: rect(b), hidden: b.hasAttribute('hidden') };
    });
    R.icoN = qa('.zd-ico').length;
    return R;
  }

  /* ---------------- sp0 / sp1：④ 进行中那段弧**在转**吗？（两次采样取角度） ---------------- */
  if (M === 'sp0' || M === 'sp1') {
    var doing = q('.zd-todo li.is-doing');
    var m = S2(doing, 'transform', '::after');
    R.doingTransform = m;
    var n = m && m.match(/matrix\(([^)]+)\)/);
    if (n) {
      var v = n[1].split(',').map(parseFloat);
      R.angleDeg = Math.round(Math.atan2(v[1], v[0]) * 180 / Math.PI);
    } else { R.angleDeg = null; }
    R.animName = S2(doing, 'animationName', '::after');
    R.animDur = S2(doing, 'animationDuration', '::after');
    R.animIter = S2(doing, 'animationIterationCount', '::after');
    R.t = Math.round(performance.now());
    return R;
  }

  /* ---------------- ico0 / ico1：② hover 前后（hover 读数必须另起一次 eval） ---------------- */
  if (M === 'ico0' || M === 'ico1') {
    R.host = qa('.zd-ico').map(function (b, i) {
      return { i: i, title: b.getAttribute('title'),
               bg: S(b, 'backgroundColor'), color: S(b, 'color'),
               isHover: b.matches(':hover') };
    });
    return R;
  }

  /* ---------------- collapse：⑥ 折叠态应显示 trailing ---------------- */
  if (M === 'collapse' || M === 'expand') {
    R.secX = secs.map(function (s) {
      var x = q('.zd-sec-x', s);
      var b = q('.zd-sec-b', s);
      return { kind: s.getAttribute('data-zd-sec'),
               closed: s.classList.contains('is-closed'),
               xDisplay: S(x, 'display'),
               bodyRows: S(b, 'gridTemplateRows'),
               aria: q('.zd-sec-t', s) ? q('.zd-sec-t', s).getAttribute('aria-expanded') : null };
    });
    return R;
  }

  /* ---------------- skgate：⑤ 骨架屏门控（造一个假 `.r93-sk`，读完就删） ---------------- */
  if (M === 'skgate') {
    R.hasSupports = (typeof CSS !== 'undefined' && CSS.supports)
        ? CSS.supports('selector(html:has(.r93-sk))') : 'noCSS';
    /* ⚠ `:has()` 不被支持时 `querySelector` 会**抛 SyntaxError** ⇒ 必须包住，
       否则整条探针挂在这里、看起来像「产品坏了」（探针假失败第 ① 类）。 */
    function hasMatch() {
      try { return !!document.querySelector('html:has(.r93-sk)'); }
      catch (e) { return 'unsupported:' + e.name; }
    }
    R.skInDoc = !!q('.r93-sk');
    R.displayBefore = S(host, 'display');           /* 正常态：应 flex */
    R.ruleMatchedBefore = hasMatch();

    var fake = document.createElement('div');
    fake.className = 'r93-sk';
    fake.setAttribute('aria-hidden', 'true');
    document.body.appendChild(fake);
    R.ruleMatchedAfter = hasMatch();
    R.displayAfter = S(host, 'display');            /* 应 none */
    R.cardRectWhenHidden = rect(card);              /* display:none ⇒ 全 0 */

    fake.parentNode.removeChild(fake);
    R.displayRestored = S(host, 'display');         /* 应回到 flex */
    R.cardRectRestored = rect(card);
    return R;
  }

  /* ---------------- 暗色 / 大字号 / 窄档 回归 ---------------- */
  if (M === 'dark') {
    R.secTtitle = S(q('.zd-sec-t'), 'color');
    R.secTfg = S(q('.zd-sec-t'), 'webkitTextFillColor');
    R.card = { bg: S(card, 'backgroundColor'), border: S(card, 'borderTopColor'),
               color: S(card, 'color') };
    R.ico0 = { bg: S(q('.zd-ico'), 'backgroundColor'), color: S(q('.zd-ico'), 'color') };
    R.todoDoneColor = S(q('.zd-todo li.is-done'), 'color');
    R.todoDoingArc = S2(q('.zd-todo li.is-doing'), 'borderTopColor', '::after');
    R.dark = document.documentElement.getAttribute('giencoder-theme');
    /* hex 扫描：只查 `.zd-*` 规则（本轮新增的三处必须在 token 体系内） */
    var hex = [];
    for (var i = 0; i < document.styleSheets.length; i++) {
      var ss = document.styleSheets[i], rules;
      try { rules = ss.cssRules; } catch (e) { continue; }
      if (!rules) continue;
      for (var j = 0; j < rules.length; j++) {
        var r = rules[j];
        if (r.selectorText && r.selectorText.indexOf('.zd-') >= 0 &&
            r.style && r.style.cssText && /#[0-9a-fA-F]{3,8}\b/.test(r.style.cssText)) {
          hex.push(r.selectorText + ' :: ' + r.style.cssText.slice(0, 120));
        }
      }
    }
    R.hexLeak = hex;
    return R;
  }

  if (M === 'fs') {
    R.uiFs = getComputedStyle(document.documentElement).getPropertyValue('--ui-fs').trim();
    var t = q('.zd-sec-t');
    R.secT = { fs: S(t, 'fontSize'), lh: S(t, 'lineHeight'), h: S(t, 'height'), fw: S(t, 'fontWeight') };
    R.secH = { h: S(q('.zd-sec-h'), 'height'), minH: S(q('.zd-sec-h'), 'minHeight') };
    var ib = q('.zd-ico');
    R.ico = { w: S(ib, 'width'), h: S(ib, 'height') };
    R.card = rect(card);
    var d = q('.zd-todo li.is-doing');
    R.doingArcW = S2(d, 'width', '::after');
    R.doingArcH = S2(d, 'height', '::after');
    return R;
  }

  if (M === 'narrow') {
    R.main = rect(q('main'));
    R.card = rect(card);
    var m = q('main'), r = m ? m.getBoundingClientRect() : null;
    var c = card ? card.getBoundingClientRect() : null;
    R.overflowRight = (r && c) ? Math.round(c.right - r.right) : null;
    R.inView = c ? (c.left >= 0 && c.right <= window.innerWidth) : null;
    R.vw = window.innerWidth;
    return R;
  }

  R.err = '未知相位 ' + M;
  return R;
})()
