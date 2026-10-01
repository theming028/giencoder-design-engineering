(function () {
  /* 第十四拍·边界与回归探针（与 p108p.js 主链互补）。
     主链验「功能对不对」；本探针验「换个环境还对不对」：
       [A] 面板不遮挡 `.r93-bar` 两枚按钮（elementFromPoint 命中自身）
       [B] 暗色档：面板/胶囊/两枚下拉/轻提示全部由 token 派生（含 §19.x 无硬编码 hex 扫描）
       [C] `--ui-fs = 18` 杠杆：分区头 32 → 41.14、圆序号恒为正圆、卡片不被压平
       [D] 窄档 620：卡片不越右界
       [E] 右栏四枚 `.td-rv-menu` 回归（第 1 节选择器组扩员后一字未变）
     ⚠ 与主链同规矩：点击与读值**分帧**（硬规则 29）。 */
  var M = window.__M;
  var r = { phase: M };
  function R(e) { if (!e) return null; var b = e.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; }
  function R2(e) { if (!e) return null; var b = e.getBoundingClientRect(); return [+b.x.toFixed(2), +b.y.toFixed(2), +b.width.toFixed(2), +b.height.toFixed(2)]; }
  function S(e) { return e ? getComputedStyle(e) : null; }
  /* ★ 可选子部件一律判空（硬规则 10 的探针侧同款）—— 分支菜单没有 `.td-mm-key`，
     直接 `S(el).color` 会 TypeError 且栈只指向 IIFE 收尾行（极难定位）。 */
  function C(e) { var s = S(e); return s ? s.color : null; }
  function BG(e) { var s = S(e); return s ? s.backgroundColor : null; }
  function T(e) { return e ? e.textContent.replace(/\s+/g, ' ').trim() : null; }
  function host() { return document.getElementById('av-zd-status'); }
  function card() { var h = host(); return h ? h.querySelector('[data-zd-card]') : null; }
  function mini() { var h = host(); return h ? h.querySelector('[data-zd-mini]') : null; }

  /* ---------- §19.x 硬编码 hex 扫描（静态，任何相位都能跑） ---------- */
  function hexScan() {
    var out = [];
    [].forEach.call(document.styleSheets, function (ss) {
      var rules = null;
      try { rules = ss.cssRules; } catch (e) { return; }
      if (!rules) return;
      [].forEach.call(rules, function (r0) {
        if (!r0.selectorText) return;
        if (r0.selectorText.indexOf('.zd-') < 0) return;
        var t = r0.cssText || '';
        var m = t.match(/#[0-9a-fA-F]{3,8}\b/g);
        if (m) out.push(r0.selectorText + ' :: ' + m.join(','));
      });
    });
    return out;
  }

  /* ================================================================ [A] 顶栏按钮不被遮挡 */
  if (M === 'bar') {
    var acts = document.querySelector('.r93-baracts');
    var fs = document.querySelector('.r93-baract[data-r93-fullscreen]');
    var bw = document.querySelector('.r93-baract[data-r93-browse]');
    r.actsRect = R(acts);
    function hit(el) {
      if (!el) return { missing: true };
      var b = el.getBoundingClientRect();
      var cx = Math.round(b.x + b.width / 2), cy = Math.round(b.y + b.height / 2);
      var t = document.elementFromPoint(cx, cy);
      return { visible: el.offsetParent !== null, rect: R(el), cx: cx, cy: cy,
               hitTag: t ? t.tagName : null,
               hitSelf: !!(t && (t === el || el.contains(t))),
               hitCls: t && t.className && t.className.baseVal !== undefined ? t.className.baseVal : (t ? String(t.className) : null) };
    }
    r.fs = hit(fs);
    r.browse = hit(bw);
    /* 卡片与顶栏按钮组是否有矩形交叠（有交叠也未必遮挡，故以 elementFromPoint 为准） */
    var c = card(), a = acts;
    if (c && a) {
      var cb = c.getBoundingClientRect(), ab = a.getBoundingClientRect();
      r.overlap = !(cb.right <= ab.left || cb.left >= ab.right || cb.bottom <= ab.top || cb.top >= ab.bottom);
      r.cardTop = Math.round(cb.top); r.actsBottom = Math.round(ab.bottom);
    }
    r.hexLeak = hexScan();
  }

  /* ================================================================ [B] 暗色档 */
  if (M === 'dark') {
    document.documentElement.setAttribute('giencoder-theme', 'dark');
    var h6 = host();
    var c6 = card(), m6 = mini();
    r.card = { bg: S(c6).backgroundColor, border: S(c6).borderTopColor, color: S(c6).color };
    r.name = C(h6.querySelector('.zd-name'));
    r.secT = C(h6.querySelector('.zd-sec-t'));
    r.rowN = C(h6.querySelector('.zd-row-n'));
    r.rowIco = C(h6.querySelector('.zd-row-i'));
    var it6 = h6.querySelector('.zd-it');
    var no6 = h6.querySelector('.zd-it-no');
    r.it = { bg: BG(it6), color: C(it6),
             noBorder: no6 ? S(no6).borderTopColor : null, noColor: C(no6) };
    r.todoLi = C(h6.querySelector('.zd-todo li'));
    r.todoDone = C(h6.querySelector('.zd-todo li.is-done'));
    r.mini = { bg: BG(m6), border: m6 ? S(m6).borderTopColor : null, color: C(m6) };
    var mb = h6.querySelector('.zd-menu-branch');
    r.menu = { bg: BG(mb), border: S(mb).borderTopColor,
               itemColor: C(mb.querySelector('.giencoder-dropdown-item')),
               itemBg: BG(mb.querySelector('.giencoder-dropdown-item')),
               capColor: C(mb.querySelector('.td-mm-cap')),
               keyColor: C(mb.querySelector('.td-mm-key')),      /* 分支菜单无此项 ⇒ null 正常 */
               divider: BG(mb.querySelector('.giencoder-dropdown-divider')) };
    var zt6 = h6.querySelector('.zd-toast');
    r.toast = { bg: BG(zt6), border: S(zt6).borderTopColor, color: C(zt6) };
    r.hexLeak = hexScan();
    /* 视觉判据：暗色下面板 / 弹层应是**深底**（token 已切换），不是白底 */
    r.dark = { cardIsLight: (function () { var a = S(c6).backgroundColor.match(/\d+/g).map(Number); return (a[0] + a[1] + a[2]) / 3 > 128; })(),
               menuIsLight: (function () { var a = S(mb).backgroundColor.match(/\d+/g).map(Number); return (a[0] + a[1] + a[2]) / 3 > 128; })() };
  }

  /* ================================================================ [C] 字号杠杆 */
  if (M === 'fs') {
    document.documentElement.style.setProperty('--ui-fs', '18');
    var h7 = host();
    r.ratio = S(document.documentElement).getPropertyValue('--ui-fs-ratio').trim();
    r.secH = S(h7.querySelector('.zd-sec-h')).height;
    r.headH = S(h7.querySelector('.zd-head')).height;
    r.itPad = S(h7.querySelector('.zd-it')).padding;
    r.itTitleLH = S(h7.querySelector('.zd-it-t')).lineHeight;
    r.itTitleFS = S(h7.querySelector('.zd-it-t')).fontSize;
    /* ③ 圆序号：宽高必须同比（否则成椭圆） */
    var itno = h7.querySelector('.zd-it-no');
    r.itNo = { w: S(itno).width, h: S(itno).height, rect: R2(itno),
               wNum: parseFloat(S(itno).width), hNum: parseFloat(S(itno).height) };
    r.itNoRound = Math.abs(r.itNo.wNum - r.itNo.hNum) < 0.02;
    r.cv = S(h7.querySelector('.zd-cv')).width;
    r.todoLH = S(h7.querySelector('.zd-todo li')).lineHeight;
    r.miniH = S(mini()).height;
    var c7 = card();
    r.cardRect = R(c7);
    r.cardW = S(c7).width;
    r.cardMaxH = S(c7).maxHeight;
    r.opts = { pad: S(h7.querySelector('.zd-sec-b')).padding };
  }

  /* ================================================================ [D] 窄档 620 */
  if (M === 'narrow') {
    var m8 = document.querySelector('main');
    var c8 = card();
    r.vw = window.innerWidth;
    r.mainRect = R(m8);
    r.cardRect = R(c8);
    r.cardW = S(c8).width;
    r.overflowRight = Math.round(c8.getBoundingClientRect().right - m8.getBoundingClientRect().right);
    r.hostMaxW = S(host()).maxWidth;
    r.inView = (function () { var b = c8.getBoundingClientRect(); return b.left >= 0 && b.right <= window.innerWidth; })();
  }

  /* ================================================================ [E] 右栏四枚下拉回归 */
  /* E0：打开右栏 + 审查模块 */
  if (M === 'rv0') {
    r.browseOn = document.getElementById('av-browse-slot').parentElement.classList.contains('av-browse-on');
    r.tabs = [].map.call(document.querySelectorAll('[data-td-tab]'), function (t) { return t.getAttribute('data-td-mod') + (t.classList.contains('is-active') ? ' ✓' : ''); });
    var pane = document.querySelector('.td-browse');
    r.paneRect = R(pane);
    r.menus = [].map.call(pane.querySelectorAll('.td-rv-menu, .td-mod-menu'), function (m) { return m.className.replace(/giencoder-[a-z-]+/g, '').replace(/\s+/g, ' ').trim(); });
  }
  /* 通用：量一枚右栏下拉（骨架 + 条目 + 勾 + 分隔线 + 摆位） */
  function measRv(sel, trigSel) {
    var m = document.querySelector(sel);
    var t = document.querySelector(trigSel);
    if (!m) return { missing: true };
    var o = {
      hidden: m.hasAttribute('hidden'),
      open: m.classList.contains('giencoder-popup-open'),
      display: S(m).display, visibility: S(m).visibility, opacity: S(m).opacity,
      pe: S(m).pointerEvents,
      bg: S(m).backgroundColor, border: S(m).borderTopColor,
      radius: S(m).borderTopLeftRadius, shadow: S(m).boxShadow,
      minW: S(m).minWidth, pad: S(m).padding, gap: S(m).gap, dir: S(m).flexDirection,
      anim: S(m).animationName,
      rect: R(m), rect2: R2(m),
      cap: T(m.querySelector('.td-mm-cap')),
      dividerH: (function () { var d = m.querySelector('.giencoder-dropdown-divider'); return d ? S(d).height : null; })(),
      dividerN: m.querySelectorAll('.giencoder-dropdown-divider').length,
      items: [].map.call(m.querySelectorAll('.giencoder-dropdown-item'), function (b) {
        var cs = S(b);
        return { n: T(b.querySelector('.td-mm-name')), checked: b.classList.contains('is-checked'),
                 pad: cs.padding, radius: cs.borderTopLeftRadius, gap: cs.gap,
                 lh: cs.lineHeight, fs: cs.fontSize,
                 color: cs.color, bg: cs.backgroundColor,
                 mark: b.querySelector('.td-mm-mark') ? S(b.querySelector('.td-mm-mark')).opacity : null,
                 rect: R(b) };
      })
    };
    if (t) {
      o.dy = Math.round(m.getBoundingClientRect().top - t.getBoundingClientRect().bottom);
      o.inView = (function () { var b = m.getBoundingClientRect(); return b.top >= 0 && b.bottom <= window.innerHeight && b.left >= 0 && b.right <= window.innerWidth; })();
      o.trigRect = R(t);
    }
    return o;
  }
  if (M === 'rvs') { r.m = measRv('.td-rv-scope-menu', '[data-td-rv-scope]'); }
  if (M === 'rvsh') {
    /* hover 必须真鼠标悬停后**另起一次 eval** 读数（硬规则 29）：本相位只负责读 */
    var hv = document.querySelector('.td-rv-scope-menu [data-td-rv-range="branch"]');
    r.hovered = hv ? hv.matches(':hover') : null;
    r.bg = hv ? S(hv).backgroundColor : null;
    r.color = hv ? S(hv).color : null;
  }
  if (M === 'rvc') { r.m = measRv('.td-commit-menu', '[data-td-commit]'); }
  if (M === 'rvo') { r.m = measRv('.td-rv-opts', '[data-td-rv-opts]'); }
  if (M === 'rvall') {
    /* 四枚全开（不关前一枚）⇒ 验互斥：同一时刻只应有一枚 not hidden */
    r.openCount = [].filter.call(document.querySelectorAll('.td-rv-menu, .td-mod-menu'), function (m) { return !m.hasAttribute('hidden'); }).length;
    r.zdOpen = [].filter.call(host().querySelectorAll('.zd-menu'), function (m) { return !m.hasAttribute('hidden'); }).length;
  }
  /* 收尾复核：关掉所有右栏下拉后，`.zd-menu` 一族骨架未受第 1 节扩员影响 */
  if (M === 'final') {
    r.zdMenuCls = (function () { var m = host().querySelector('.zd-menu-branch'); return m ? m.className : null; })();
    r.zdMenuSkeleton = (function () {
      var m = host().querySelector('.zd-menu-branch');
      return { minW: S(m).minWidth, radius: S(m).borderTopLeftRadius, pad: S(m).padding,
               shadow: S(m).boxShadow, origin: S(m).transformOrigin, pos: S(m).position };
    })();
    r.zdToastSkeleton = (function () { var z = document.querySelector('.zd-toast'); return { radius: S(z).borderTopLeftRadius, pad: S(z).padding, fs: S(z).fontSize, bg: S(z).backgroundColor }; })();
    r.rvMenuCount = document.querySelectorAll('.td-rv-menu').length;
    r.rvSkeletonUnchanged = (function () {
      var m = document.querySelector('.td-rv-opts');
      return { minW: S(m).minWidth, radius: S(m).borderTopLeftRadius, pad: S(m).padding,
               shadow: S(m).boxShadow, origin: S(m).transformOrigin, anim: S(m).animationName };
    })();
    r.cardRect = R(card());
    r.mainRect = R(document.querySelector('main'));
    r.browseOn = document.getElementById('av-browse-slot').parentElement.classList.contains('av-browse-on');
  }

  return JSON.stringify(r);
})()
