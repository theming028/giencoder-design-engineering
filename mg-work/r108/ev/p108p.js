(function () {
  var M = window.__M;
  var r = { phase: M };
  function R(e) { if (!e) return null; var b = e.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; }
  function S(e) { return e ? getComputedStyle(e) : null; }
  function T(e) { return e ? e.textContent.replace(/\s+/g, ' ').trim() : null; }
  function host() { return document.getElementById('av-zd-status'); }
  function card() { var h = host(); return h ? h.querySelector('[data-zd-card]') : null; }
  function mini() { var h = host(); return h ? h.querySelector('[data-zd-mini]') : null; }
  function menuB() { var h = host(); return h ? h.querySelector('.zd-menu-branch') : null; }
  function menuC() { var h = host(); return h ? h.querySelector('.zd-menu-commit') : null; }

  /* ============================== 静态结构 ============================== */
  if (M === 'static') {
    var h = host(), c = card();
    var main = document.querySelector('main');
    r.hostInMain = !!(h && main && h.parentNode === main);
    r.mainRect = R(main);
    r.cardRect = R(c);
    r.secs = h ? h.querySelectorAll('[data-zd-sec]').length : 0;
    r.secKinds = h ? [].map.call(h.querySelectorAll('[data-zd-sec]'), function (s) { return s.getAttribute('data-zd-sec'); }) : [];
    r.planGone = !document.querySelector('[data-zd-sec="plan"]');
    r.planRowGone = !document.querySelector('.zd-row-n') || !/右栏复刻方案/.test(document.body.textContent);
    r.secTitles = h ? [].map.call(h.querySelectorAll('.zd-sec-t'), T) : [];
    r.secX = h ? [].map.call(h.querySelectorAll('.zd-sec-x'), T) : [];
    r.rows = h ? [].map.call(h.querySelectorAll('.zd-row'), T) : [];
    r.gitRows = h ? [].map.call(h.querySelectorAll('[data-zd-git]'), function (b) {
      return { k: b.getAttribute('data-zd-git'), haspopup: b.getAttribute('aria-haspopup'), exp: b.getAttribute('aria-expanded'), text: T(b) };
    }) : [];
    /* ③ 目标：迭代行几何与图标 */
    var its = h ? h.querySelectorAll('.zd-it') : [];
    r.itCount = its.length;
    r.it = [].map.call(its, function (e) {
      var cs = S(e);
      var svg = e.querySelector('svg');
      var no = e.querySelector('.zd-it-no');
      var t = e.querySelector('.zd-it-t');
      return {
        pad: cs.paddingTop + '/' + cs.paddingRight + '/' + cs.paddingBottom + '/' + cs.paddingLeft,
        radius: cs.borderTopLeftRadius,
        gap: cs.gap,
        align: cs.alignItems,
        bg: cs.backgroundColor,
        hasNo: !!no, noRect: R(no), noBorder: no ? S(no).borderTopColor : null, noColor: no ? S(no).color : null,
        hasIco: !!svg, icoRect: R(svg), icoColor: svg ? S(svg).color : null,
        /* 上游 GoalStatusSection 未完成项用 lucide `goal`（3 条子路径） */
        icoPaths: svg ? [].map.call(svg.querySelectorAll('path'), function (p) { return p.getAttribute('d'); }) : [],
        titleLH: t ? S(t).lineHeight : null, titleFS: t ? S(t).fontSize : null,
        cnt: T(e.querySelector('.zd-it-c')), txt: T(t)
      };
    });
    /* ③ trailing 的 `·` 与暂停钮 */
    var sep = h ? h.querySelector('.zd-sep') : null;
    r.sepText = T(sep);
    r.sepColor = sep ? S(sep).color : null;
    var pause = h ? h.querySelector('[data-zd-sec="goal"] .zd-ico') : null;
    r.pauseRect = R(pause);
    r.pauseSvgRect = R(pause ? pause.querySelector('svg') : null);
    r.pausePaths = pause ? [].map.call(pause.querySelectorAll('rect'), function (x) { return x.getAttribute('x') + ',' + x.getAttribute('y') + ',' + x.getAttribute('width') + ',' + x.getAttribute('height') + ',rx=' + x.getAttribute('rx'); }) : [];
    /* ③ 分区头 / 折叠箭头 / 收起钮 */
    var sh = h ? h.querySelector('.zd-sec-h') : null;
    r.secH = sh ? { h: S(sh).height, pad: S(sh).padding, gap: S(sh).gap, fs: S(sh).fontSize } : null;
    var cv = h ? h.querySelector('.zd-cv') : null;
    r.cv = cv ? { w: S(cv).width, h: S(cv).height, rect: R(cv), opacity: S(cv).opacity, transition: S(cv).transitionProperty + ' ' + S(cv).transitionDuration } : null;
    var minBtn = h ? h.querySelector('[data-zd-min]') : null;
    r.minBtn = { rect: R(minBtn), svgRect: R(minBtn ? minBtn.querySelector('svg') : null), cls: minBtn ? minBtn.className : null,
                 paths: minBtn ? [].map.call(minBtn.querySelectorAll('path'), function (p) { return p.getAttribute('d'); }) : [] };
    /* ① 两枚菜单 + 轻提示 */
    r.menuCount = h ? h.querySelectorAll('.zd-menu').length : 0;
    r.menuBranch = { hidden: menuB() ? menuB().hasAttribute('hidden') : null, rect: R(menuB()), cls: menuB() ? menuB().className : null,
                     parent: menuB() && menuB().parentNode ? menuB().parentNode.id : null,
                     items: menuB() ? [].map.call(menuB().querySelectorAll('[data-zd-br]'), function (b) { return b.getAttribute('data-zd-br') + (b.classList.contains('is-checked') ? ' ✓' : ''); }) : [] };
    r.menuCommit = { hidden: menuC() ? menuC().hasAttribute('hidden') : null,
                     items: menuC() ? [].map.call(menuC().querySelectorAll('[data-zd-commit]'), T) : [] };
    var zt = h ? h.querySelector('.zd-toast') : null;
    r.toast = { has: !!zt, hidden: zt ? zt.hasAttribute('hidden') : null, text: T(zt) };
    r.miniHidden = mini() ? mini().hasAttribute('hidden') : null;
    /* ⑨ 兜底：卡片在 main 内、不越右界 */
    r.cardRightGap = (main && c) ? Math.round((main.getBoundingClientRect().right) - c.getBoundingClientRect().right) : null;
  }

  /* ============================== ① 更改 → 打开右栏审查 ============================== */
  if (M === 'rev0' || M === 'rev1') {
    var slot = document.getElementById('av-browse-slot');
    var row = slot ? slot.parentElement : null;
    r.browseOn = row ? row.classList.contains('av-browse-on') : null;
    var pane = document.querySelector('.td-browse');
    r.paneRect = R(pane);
    r.tabs = [].map.call(document.querySelectorAll('[data-td-tab]'), function (t) { return t.getAttribute('data-td-mod') + (t.classList.contains('is-active') ? ' ✓' : ''); });
    var rvp = document.getElementById('av-browse-pane-review');
    r.reviewHidden = rvp ? rvp.hasAttribute('hidden') : null;
    r.reviewRect = R(rvp);
    r.mainRect = R(document.querySelector('main'));
    r.cardRect = R(card());
  }

  /* ============================== ① 分支菜单 ============================== */
  if (M === 'br1') {
    var m = menuB(), t0 = document.querySelector('[data-zd-git="branch"]');
    r.hidden = m ? m.hasAttribute('hidden') : null;
    r.open = m ? m.classList.contains('giencoder-popup-open') : null;
    r.display = m ? S(m).display : null;
    r.visibility = m ? S(m).visibility : null;
    r.opacity = m ? S(m).opacity : null;
    r.rect = R(m); r.triggerRect = R(t0);
    r.pe = m ? S(m).pointerEvents : null;
    r.bg = m ? S(m).backgroundColor : null;
    r.border = m ? S(m).borderTopColor : null;
    r.minW = m ? S(m).minWidth : null;
    r.pad = m ? S(m).padding : null;
    r.items = m ? [].map.call(m.querySelectorAll('.giencoder-dropdown-item'), function (b) {
      var cs = S(b);
      return { n: T(b.querySelector('.td-mm-name')), checked: b.classList.contains('is-checked'), pad: cs.padding, radius: cs.borderTopLeftRadius,
               color: cs.color, bg: cs.backgroundColor, mark: b.querySelector('.td-mm-mark') ? S(b.querySelector('.td-mm-mark')).opacity : null,
               rect: R(b) };
    }) : [];
    r.cap = m ? T(m.querySelector('.td-mm-cap')) : null;
    r.divider = m ? (m.querySelector('.giencoder-dropdown-divider') ? S(m.querySelector('.giencoder-dropdown-divider')).height : null) : null;
    /* 摆位判据：菜单上缘 = 触发行下缘 + 6 */
    r.dy = (m && t0) ? Math.round(m.getBoundingClientRect().top - t0.getBoundingClientRect().bottom) : null;
    r.dxRight = (m && t0) ? Math.round(m.getBoundingClientRect().right - t0.getBoundingClientRect().right) : null;
    r.inView = m ? (function () { var b = m.getBoundingClientRect(); return b.top >= 0 && b.bottom <= window.innerHeight && b.left >= 0 && b.right <= window.innerWidth; })() : null;
  }
  if (M === 'br2') {
    var m2 = menuB();
    r.hidden = m2 ? m2.hasAttribute('hidden') : null;
    r.open = m2 ? m2.classList.contains('giencoder-popup-open') : null;
    r.branchText = T(document.querySelector('[data-zd-branch]'));
    r.checked = m2 ? [].map.call(m2.querySelectorAll('[data-zd-br]'), function (b) { return b.getAttribute('data-zd-br') + (b.classList.contains('is-checked') ? ' ✓' : ''); }) : [];
    var zt2 = document.querySelector('.zd-toast');
    r.toastHidden = zt2 ? zt2.hasAttribute('hidden') : null;
    r.toastText = T(zt2);
    r.toastRect = R(zt2);
    r.toastBg = zt2 ? S(zt2).backgroundColor : null;
    r.rowAria = document.querySelector('[data-zd-git="branch"]').getAttribute('aria-expanded');
  }

  /* ============================== ① 提交菜单 ============================== */
  if (M === 'cm1') {
    var m3 = menuC(), t3 = document.querySelector('[data-zd-git="commit"]');
    r.hidden = m3 ? m3.hasAttribute('hidden') : null;
    r.open = m3 ? m3.classList.contains('giencoder-popup-open') : null;
    r.rect = R(m3); r.triggerRect = R(t3);
    r.items = m3 ? [].map.call(m3.querySelectorAll('[data-zd-commit]'), function (b) {
      return { k: b.getAttribute('data-zd-commit'), text: T(b), key: T(b.querySelector('.td-mm-key')), rect: R(b) };
    }) : [];
    r.dy = (m3 && t3) ? Math.round(m3.getBoundingClientRect().top - t3.getBoundingClientRect().bottom) : null;
    r.inView = m3 ? (function () { var b = m3.getBoundingClientRect(); return b.top >= 0 && b.bottom <= window.innerHeight && b.left >= 0 && b.right <= window.innerWidth; })() : null;
    r.branchMenuHidden = menuB() ? menuB().hasAttribute('hidden') : null;
  }
  if (M === 'cm2') {
    var zt3 = document.querySelector('.zd-toast');
    r.menuHidden = menuC() ? menuC().hasAttribute('hidden') : null;
    r.toastHidden = zt3 ? zt3.hasAttribute('hidden') : null;
    r.toastText = T(zt3);
    r.rowAria = document.querySelector('[data-zd-git="commit"]').getAttribute('aria-expanded');
  }
  /* 外点 / Esc 关闭 */
  if (M === 'cm3') {
    r.branchHidden = menuB() ? menuB().hasAttribute('hidden') : null;
    r.commitHidden = menuC() ? menuC().hasAttribute('hidden') : null;
    r.browseOn = document.getElementById('av-browse-slot').parentElement.classList.contains('av-browse-on');
    r.zcardHidden = card() ? card().hasAttribute('hidden') : null;
  }

  /* ============ ④ 折展弹性：rAF 采样（同一 eval 内装采样器 + 触发） ============ */
  if (M === 'foldStart') {
    var sec = document.querySelector('[data-zd-sec="git"]');
    var body = sec.querySelector('.zd-sec-b');
    var inner = body.firstElementChild;
    r.beforeClosed = sec.classList.contains('is-closed');
    var arr = []; window.__S = arr;
    var t0b = performance.now();
    (function tick() {
      var cb = S(body), ci = S(inner);
      arr.push([Math.round(performance.now() - t0b),
                parseFloat(cb.gridTemplateRows) || 0,
                Math.round(parseFloat(ci.opacity) * 1000) / 1000,
                ci.translate, ci.scale]);
      if (performance.now() - t0b < 520) requestAnimationFrame(tick);
    })();
    sec.querySelector('.zd-sec-t').click();
    r.afterClosed = sec.classList.contains('is-closed');
  }
  if (M === 'foldRead') {
    var s = window.__S || [];
    r.n = s.length;
    r.samples = s;
    var hts = s.map(function (x) { return x[1]; });
    r.maxH = Math.max.apply(null, hts);
    r.lastH = hts[hts.length - 1];
    r.firstH = hts[0];
    r.overshoot = Math.round((r.maxH - r.lastH) * 100) / 100;
    var sec2 = document.querySelector('[data-zd-sec="git"]');
    r.closed = sec2.classList.contains('is-closed');
    r.aria = sec2.querySelector('.zd-sec-t').getAttribute('aria-expanded');
    r.bodyDisplay = S(sec2.querySelector('.zd-sec-b')).display;
  }

  /* ============ ④ 面板 ⇄ 胶囊弹性：rAF 采样 ============ */
  if (M === 'miniOutStart') {
    var c4 = card();
    var a4 = []; window.__S2 = a4;
    var t4 = performance.now();
    (function tick2() {
      var cs = S(c4);
      a4.push([Math.round(performance.now() - t4), Math.round(parseFloat(cs.opacity) * 1000) / 1000, cs.scale, cs.translate]);
      if (performance.now() - t4 < 320) requestAnimationFrame(tick2);
    })();
    document.querySelector('[data-zd-min]').click();
    r.clicked = true;
  }
  if (M === 'miniOutRead') {
    var s4 = window.__S2 || [];
    r.n = s4.length; r.samples = s4;
    r.opMin = Math.min.apply(null, s4.map(function (x) { return x[1]; }));
    r.opLast = s4.length ? s4[s4.length - 1][1] : null;
    r.cardHidden = card() ? card().hasAttribute('hidden') : null;
    r.miniHidden = mini() ? mini().hasAttribute('hidden') : null;
    r.miniRect = R(mini());
    r.miniText = T(mini());
    r.miniBorder = mini() ? S(mini()).borderTopColor : null;
    r.miniRadius = mini() ? S(mini()).borderTopLeftRadius : null;
  }
  if (M === 'miniInStart') {
    var c5 = card();
    var a5 = []; window.__S3 = a5;
    var t5 = performance.now();
    (function tick3() {
      var cs = S(c5);
      a5.push([Math.round(performance.now() - t5), Math.round(parseFloat(cs.opacity) * 1000) / 1000, cs.scale, cs.translate, R(c5)]);
      if (performance.now() - t5 < 620) requestAnimationFrame(tick3);
    })();
    mini().click();
    r.clicked = true;
  }
  if (M === 'miniInRead') {
    var s5 = window.__S3 || [];
    r.n = s5.length;
    r.samples = s5;
    /* ⚠ `scale` 的 computed 值在**无变换时是 `none`**（parseFloat → NaN）⇒ 若 rAF 末帧
       落在入场类被摘掉之后，`lastScale` 会误报 0（本轮真出现过）。⇒ 只统计有效数字，
       并额外报一个「终态 computed scale」把这两件事分开。 */
    var sc = s5.map(function (x) { return parseFloat(x[2]); })
               .filter(function (v) { return !isNaN(v); });
    r.maxScale = sc.length ? Math.round(Math.max.apply(null, sc) * 10000) / 10000 : null;
    r.lastScale = sc.length ? sc[sc.length - 1] : null;
    r.settledScale = S(card()).scale;
    r.cardHidden = card() ? card().hasAttribute('hidden') : null;
    r.miniHidden = mini() ? mini().hasAttribute('hidden') : null;
    r.cardRect = R(card());
    r.gitClosedKept = document.querySelector('[data-zd-sec="git"]').classList.contains('is-closed');
  }

  /* ============ 暗色档 ============ */
  if (M === 'dark') {
    document.documentElement.setAttribute('giencoder-theme', 'dark');
    var c6 = card(), h6 = host();
    r.card = c6 ? { bg: S(c6).backgroundColor, border: S(c6).borderTopColor } : null;
    var nm = h6.querySelector('.zd-name');
    r.name = nm ? S(nm).color : null;
    var t6 = h6.querySelector('.zd-sec-t');
    r.secT = t6 ? S(t6).color : null;
    var it6 = h6.querySelector('.zd-it');
    r.it = it6 ? { color: S(it6).color, hoverBg: null } : null;
    var tl = h6.querySelector('.zd-todo li');
    r.todo = tl ? S(tl).color : null;
    r.mini = { bg: S(mini()).backgroundColor, border: S(mini()).borderTopColor };
    r.mn = menuB() ? { bg: S(menuB()).backgroundColor, border: S(menuB()).borderTopColor } : null;
    r.toast = (function () { var z = h6.querySelector('.zd-toast'); return { bg: S(z).backgroundColor, border: S(z).borderTopColor, color: S(z).color }; })();
    r.hexLeak = null;
  }

  /* ============ 字号杠杆 ============ */
  if (M === 'fs') {
    var h7 = host();
    r.ratio = S(document.documentElement).getPropertyValue('--ui-fs-ratio').trim();
    r.secH = S(h7.querySelector('.zd-sec-h')).height;
    r.itPad = S(h7.querySelector('.zd-it')).padding;
    r.itTitleLH = S(h7.querySelector('.zd-it-t')).lineHeight;
    r.itTitleFS = S(h7.querySelector('.zd-it-t')).fontSize;
    r.cardRect = R(card());
    r.cv = S(h7.querySelector('.zd-cv')).width;
    r.todoLH = S(h7.querySelector('.zd-todo li')).lineHeight;
  }

  /* ============ 窄档 ============ */
  if (M === 'narrow') {
    var m8 = document.querySelector('main');
    r.mainRect = R(m8);
    r.cardRect = R(card());
    r.overflowRight = Math.round(card().getBoundingClientRect().right - m8.getBoundingClientRect().right);
  }

  return JSON.stringify(r);
})()
