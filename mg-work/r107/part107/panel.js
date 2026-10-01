/* ================================================================================
   ★ r107 · 侧栏模块标签化控制器（会话详情页）
   职责（全部只作用于 `.td-browse` 这一块，不碰页面其它模块）：
     ① 标签增删切换 + 拖拽重排 + `+` 模块菜单
     ② 侧栏「最大化 / 还原」（复用宿主 --av-browse-w，自算 maxPanelW）
     ③ 审查：文件折叠（点头部 = 单个 / 菜单 = 全部⇄展开全部）/ 统一⇄并排 / 对比范围 / 显示选项八项
       / 「折叠 N 行未改动」/ 暂存·撤销 / 复制·定位·PR / 提交·推送下拉 + 提交模态
     ④ 终端：本地回声（不发请求，纯前端演示）
     ⑤ 浏览器：标注态 + 元素评论气泡
     ⑥ 摘要：会话摘要 / 计划 / 来源 / 产物（静态展示 + 复制反馈）
   ⚠ 注册顺序：本文件排在 `browse.js + ctrl-conv.js` **之后**（同一个脚本块）。
     Esc 走 window 捕获段（比 ctrl-conv 的 document 捕获更早），命中才 stopPropagation，
     免得「关菜单」顺手把整条侧栏也关了。
   ⚠ 原「文件」模块的 controller（ctrl-conv.js）一行未改，本文件只接管标签栏与其余模块。
   ================================================================================ */
(function () {
  'use strict';

  var slot = document.getElementById('av-browse-slot');
  if (!slot) return;
  var pane = slot.querySelector('.td-browse');
  if (!pane) return;
  var bar = pane.querySelector('.td-browse-bar');
  var tabsEl = pane.querySelector('.td-browse-tabs');
  if (!bar || !tabsEl) return;

  var STORE_KEY = 'giencoder:r105-browse:v1';   /* 与 ctrl-conv.js 同一个 key（宽度记忆） */
  var DEF_PANEL = 641, MIN_PANEL = 561, MAIN_MIN = 380;

  var X_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="12" height="12" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';

  /* 折叠全部 / 展开全部 —— 同一枚按钮的两个字形（箭头相对 = 收，箭头相背 = 放） */
  var ICO_FOLD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true"><path d="m7 20 5-5 5 5"/><path d="m7 4 5 5 5-5"/></svg>';
  var ICO_UNFOLD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true"><path d="m7 9 5-5 5 5"/><path d="m7 15 5 5 5-5"/></svg>';

  /* ==================== 轻提示（动作类菜单项的反馈；1.4s 自动收） ==================== */
  var toast = document.createElement('div');
  toast.className = 'td-toast';
  toast.setAttribute('hidden', '');
  pane.appendChild(toast);
  var toastTimer = 0;
  function say(text) {
    toast.textContent = text;
    toast.removeAttribute('hidden');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.setAttribute('hidden', ''); }, 1400);
  }

  /* ★ 本轮：四枚下拉 + 右键菜单都改用 DS 的 Dropdown 组件（`.giencoder-dropdown-popup`）后，
     DS 给该组件配了**入场动画**（`opacity/visibility/translate/scale`），并且**默认就是
     `visibility:hidden`** ⇒ 必须靠 `.giencoder-popup-open` 这个唯一开关放行（与站内其它
     DS 弹层同口径，见 PLAYBOOK 规则 6）。忘了加 = 菜单「打开了但看不见」。
     ⚠ DS 骨架里那条 `animation: giencoder-popup-in` 播完会把 `opacity` 打回 0
     ⇒ 由 panel.css 显式 `animation: none` 掉（r93 的 `.r93-ctx` 同款处置）。 */
  var POP_OPEN = 'giencoder-popup-open';

  /* ==================== 标签栏 ==================== */
  function tabs() { return [].slice.call(tabsEl.querySelectorAll('[data-td-tab]')); }
  function syncSingle() {
    var n = tabs().length;
    tabsEl.classList.toggle('is-single', n <= 1);
    for (var i = 0; i < n; i++) {
      var x = tabs()[i].querySelector('[data-td-tab-x]');
      if (x) x.setAttribute('aria-hidden', n <= 1 ? 'true' : 'false');
    }
  }
  function activate(mod) {
    var list = tabs(), i, on, found = false;
    for (i = 0; i < list.length; i++) {
      on = list[i].getAttribute('data-td-mod') === mod;
      list[i].classList.toggle('is-active', on);
      list[i].setAttribute('aria-selected', on ? 'true' : 'false');
      if (on) found = true;
    }
    var panes = [].slice.call(pane.querySelectorAll('.td-browse-body, [data-td-pane]'));
    for (i = 0; i < panes.length; i++) {
      var m = panes[i].classList.contains('td-browse-body') ? 'files' : panes[i].getAttribute('data-td-pane');
      if (m === mod) panes[i].removeAttribute('hidden');
      else panes[i].setAttribute('hidden', '');
    }
    return found;
  }
  function ensureOpen() {
    var row = slot.parentElement;
    if (row && row.classList.contains('av-browse-on')) return;
    var b = document.querySelector('.r93-baract[data-r93-browse]');
    if (b) b.click();
  }
  function bindTab(tab) {
    tab.addEventListener('click', function (e) {
      if (e.target && e.target.closest && e.target.closest('[data-td-tab-x]')) return;
      activate(tab.getAttribute('data-td-mod'));
    });
    tab.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(tab.getAttribute('data-td-mod')); }
    });
    var x = tab.querySelector('[data-td-tab-x]');
    if (x) x.addEventListener('click', function (e) { e.stopPropagation(); closeTab(tab); });
    /* 拖拽重排：pointermove / pointerup 一律挂 window（与站内其它拖拽同口径） */
    tab.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      if (e.target && e.target.closest && e.target.closest('[data-td-tab-x]')) return;
      var startX = e.clientX, moved = false;
      function onMove(ev) {
        if (!moved) {
          if (Math.abs(ev.clientX - startX) < 5) return;
          moved = true;
          tab.classList.add('is-dragging');
          tabsEl.classList.add('is-reordering');
        }
        var list = tabs(), target = null, i;
        for (i = 0; i < list.length; i++) {
          if (list[i] === tab) continue;
          var r = list[i].getBoundingClientRect();
          if (ev.clientX < r.left + r.width / 2) { target = list[i]; break; }
        }
        if (target) { if (target.previousElementSibling !== tab) tabsEl.insertBefore(tab, target); }
        else {
          var last = list[list.length - 1];
          if (last && last !== tab && last.nextElementSibling !== tab) tabsEl.appendChild(tab);
        }
        ev.preventDefault();
      }
      function onUp() {
        window.removeEventListener('pointermove', onMove, true);
        window.removeEventListener('pointerup', onUp, true);
        if (moved) { tab.classList.remove('is-dragging'); tabsEl.classList.remove('is-reordering'); }
      }
      window.addEventListener('pointermove', onMove, true);
      window.addEventListener('pointerup', onUp, true);
      window.addEventListener('blur', onUp);
    });
  }
  function openTab(mod, opts) {
    var ex = tabsEl.querySelector('[data-td-tab][data-td-mod="' + mod + '"]');
    if (ex) { activate(mod); ensureOpen(); return ex; }
    var src = bar.querySelector('[data-td-open-mod="' + mod + '"]');
    var t = document.createElement('div');
    t.className = 'td-browse-tab';
    t.setAttribute('role', 'tab');
    t.setAttribute('data-td-tab', '1');
    t.setAttribute('data-td-mod', mod);
    t.setAttribute('tabindex', '0');
    t.setAttribute('aria-controls', 'av-browse-pane-' + mod);
    var ico = document.createElement('span');
    ico.className = 'td-tab-ico';
    var mi = src && src.querySelector('.td-mm-ico');
    if (mi) ico.innerHTML = mi.innerHTML;
    var nm = document.createElement('span');
    nm.className = 'td-tab-name';
    nm.textContent = (opts && opts.name) || (src && src.querySelector('.td-mm-name').textContent) || mod;
    var x = document.createElement('button');
    x.className = 'td-tab-x';
    x.type = 'button';
    x.tabIndex = -1;
    x.setAttribute('data-td-tab-x', '1');
    x.setAttribute('aria-label', '关闭「' + nm.textContent + '」标签');
    x.innerHTML = X_SVG;
    t.appendChild(ico); t.appendChild(nm); t.appendChild(x);
    tabsEl.appendChild(t);
    bindTab(t);
    syncSingle();
    activate(mod);
    ensureOpen();
    return t;
  }
  function closeTab(tab) {
    var list = tabs(), i = list.indexOf(tab), wasActive = tab.classList.contains('is-active');
    if (list.length <= 1) return;                       /* 最后一枚不给关（关了就整条侧栏没了） */
    if (tab.parentNode) tab.parentNode.removeChild(tab);
    syncSingle();
    if (wasActive) {
      var rest = tabs();
      activate(rest[Math.min(i, rest.length - 1)].getAttribute('data-td-mod'));
    }
  }

  /* 标签批操作（右键菜单用）：一律走 closeTab ⇒ 「只剩一枚不许关」`is-single` 与
     「关掉当前标签后激活谁」的口径只有一份实现，不会出现两处不一致。 */
  function closeOthers(keep) {
    var list = tabs();
    for (var i = 0; i < list.length; i++) if (list[i] !== keep) closeTab(list[i]);
  }
  function closeRight(tab) {
    var list = tabs(), i = list.indexOf(tab), k;
    for (k = list.length - 1; k > i; k--) closeTab(list[k]);
  }
  function closeAll() {
    var list = tabs(), k;
    for (k = list.length - 1; k > 0; k--) closeTab(list[k]);   /* 留住第一枚：全关掉侧栏就空了 */
  }
  function reloadTab(tab) {
    var mod = tab.getAttribute('data-td-mod');
    activate(mod);
    if (mod === 'review' && rvBody) {
      rvBody.classList.add('is-refreshing');
      setTimeout(function () { rvBody.classList.remove('is-refreshing'); }, 420);
    }
    say('已重新加载「' + (ctxTxt(tab.querySelector('.td-tab-name')) || mod) + '」');
  }

  /* ==================== 下拉菜单（四枚共用一套开合口径） ==================== */
  /* ★ r107 返工（真 bug）：搜索根必须是 `.td-browse`（= `pane`），**不能**是
     `.td-browse-bar`（= `bar`）。`.td-rv-opts` 等菜单挂在**各模块自己的工具条**里、
     不在标签栏内 ⇒ 拿 `bar` 当根永远查不到它们 ⇒
     「点空白 / 按 Esc / 选完选项」三条关闭路径全部失效（浮窗只能靠再点一次触发器关）。
     同一根因还有下面 Esc 裁决那一处（详见该处注释）。 */
  var menuPairs = [];
  function closeMenus(except) {
    for (var i = 0; i < menuPairs.length; i++) {
      var p = menuPairs[i];
      if (p.menu === except) continue;
      p.menu.setAttribute('hidden', '');
      p.menu.classList.remove(POP_OPEN);
      if (p.trigger) p.trigger.setAttribute('aria-expanded', 'false');
    }
  }
  /* r107-k2
     三枚 `.td-rv-menu` 的触发器都在**审查模块的工具条**（`.td-mod-bar`）里，而基类规则把菜单
     钉在 `.td-browse` 的 `top: 42px`（= 标签栏下方）⇒ 菜单跑到**触发按钮上方** 34~36px
     （1440 实测 dy = −35.0 / −34.0 / −36.0）。这里在**打开瞬间**按触发器实际几何现场摆位。
     ▸ 与 `.td-ctxmenu` 的 `ctxShow()` / 划词浮条的 `selShow()` 同一套做法（本页既有口径）。
     ▸ 为什么不用纯 CSS / 为什么非这三枚：见 panel.css 第 1 节 `r107-k1` 那段注释。
     ⚠ 必须在 `[hidden]` 摘掉**之后**调用（否则量到 0×0）；
       量宽高用 `offsetWidth/offsetHeight` —— 不受入场 `scale(0.96)` 过渡影响
       （`getBoundingClientRect()` 会把 0.96 乘进去，量出来的宽是错的）。
     ⚠ `.td-mod-menu` 走同一条 `toggleMenu`，但它不带 `.td-rv-menu` ⇒ 这里直接放行，
       保持它原来的 CSS 落位（`top: 42px; left: 64px`）不动。 */
  var RV_GAP = 6, RV_PAD = 4;
  function placeRv(menu, trigger) {
    if (!trigger || !menu.classList.contains('td-rv-menu')) return;
    var host = menu.offsetParent;                     /* = `.td-browse`（position: relative） */
    if (!host) return;
    var hr = host.getBoundingClientRect();
    var ox = hr.left + host.clientLeft;               /* 包含块原点 = padding box 左上角 */
    var oy = hr.top + host.clientTop;
    var tr = trigger.getBoundingClientRect();
    var top = tr.bottom - oy + RV_GAP;                /* 触发器下缘往下 6px */
    var left = tr.left - ox;                          /* 左缘对齐触发器 */
    var maxLeft = host.clientWidth - menu.offsetWidth - RV_PAD;
    if (left > maxLeft) left = maxLeft;               /* 右侧放不下 ⇒ 向左收，贴住面板右内边 */
    if (left < RV_PAD) left = RV_PAD;
    menu.style.top = Math.round(top) + 'px';
    menu.style.left = Math.round(left) + 'px';
    menu.style.right = 'auto';                        /* 不清掉基类的 right，会与 left 一起把盒子拉宽 */
  }

  function toggleMenu(menu, trigger) {
    var willOpen = menu.hasAttribute('hidden');
    closeMenus(willOpen ? menu : null);
    if (willOpen) {
      menu.removeAttribute('hidden');
      menu.classList.add(POP_OPEN);
      if (trigger) trigger.setAttribute('aria-expanded', 'true');
      placeRv(menu, trigger);                         /* r107-k2 */
    } else {
      menu.setAttribute('hidden', '');
      menu.classList.remove(POP_OPEN);
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }
  }
  function bindMenu(triggerSel, menuSel) {
    var t = pane.querySelector(triggerSel), m = pane.querySelector(menuSel);
    if (!t || !m) return null;
    menuPairs.push({ menu: m, trigger: t });
    t.addEventListener('click', function (e) { e.stopPropagation(); toggleMenu(m, t); });
    return m;
  }
  var modMenu = bindMenu('[data-td-add]', '.td-mod-menu');
  var rvOpts = bindMenu('[data-td-rv-opts]', '.td-rv-opts');
  var scopeMenu = bindMenu('[data-td-rv-scope]', '.td-rv-scope-menu');
  var commitMenu = bindMenu('[data-td-commit]', '.td-commit-menu');
  void modMenu; void rvOpts; void scopeMenu; void commitMenu;
  /* 右键菜单没有「触发器」（由 contextmenu 事件在指针处现场摆位），但仍登记进 menuPairs
     ⇒ 与四枚下拉共用一套「点空白 / 按 Esc 一律收起」的口径。 */
  var ctxEl = pane.querySelector('.td-ctxmenu');
  if (ctxEl) menuPairs.push({ menu: ctxEl, trigger: null });
  var openModBtns = bar.querySelectorAll('[data-td-open-mod]');
  for (var om = 0; om < openModBtns.length; om++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        closeMenus(null);
        openTab(b.getAttribute('data-td-open-mod'));
      });
    })(openModBtns[om]);
  }
  document.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('.td-mod-menu, .td-rv-menu, .td-ctxmenu')) return;
    closeMenus(null);
  });

  /* ==================== 最大化 / 还原 ==================== */
  function freeW() {
    var row = slot.parentElement;
    if (!row) return 0;
    var cs = getComputedStyle(row);
    var w = row.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0);
    var kids = row.children, i, c;
    for (i = 0; i < kids.length; i++) {
      c = kids[i];
      if (c === slot || c.id === 'av-browse-split' || c.tagName === 'MAIN') continue;
      w -= c.getBoundingClientRect().width;
    }
    return w;
  }
  function maxPanelW() { return Math.max(MIN_PANEL, Math.round(freeW() - MAIN_MIN)); }
  function storedPanelW() {
    try {
      var d = JSON.parse(localStorage.getItem(STORE_KEY) || 'null') || {};
      if (typeof d.panelW === 'number') return d.panelW;
    } catch (err) {}
    return DEF_PANEL;
  }
  function applyMaxW() {
    var w = maxPanelW();
    slot.style.setProperty('--av-browse-w', w + 'px');
    slot.setAttribute('data-td-maxw', String(w));
  }
  /* ★ 第九拍 ①：按钮上的**字形**也得跟着翻。原实现只翻 aria-pressed / 文案，内联 SVG 的 `d`
     一直是最初那套「四角朝外」⇒ 全屏后按钮看着根本没变（邵先生报的①）。
     两套字形同口径（24 viewBox / stroke-width 2 / 四角折角）：
       MAX = 四角朝外的框角 —— 就是 HTML 里写死那套，运行时**从 DOM 读出来缓存**（不另抄一份免得漂移）；
       MIN = 四角朝内的折角（Lucide `minimize` 的四条，与本页其余图标同源）。
     ⚠ 只改 `d` 属性、不重建节点 ⇒ 不碰 React，按钮的 hover / focus / 键盘可达性一字不变。 */
  var ICON_MIN = ['M8 3v3a2 2 0 0 1-2 2H3', 'M21 8h-3a2 2 0 0 1-2-2V3',
                  'M3 16h3a2 2 0 0 1 2 2v3', 'M16 21v-3a2 2 0 0 1 2-2h3'];
  var maxBtn = bar.querySelector('[data-td-max]');
  var maxPaths = maxBtn ? [].slice.call(maxBtn.querySelectorAll('svg path')) : [];
  var ICON_MAX = maxPaths.map(function (p) { return p.getAttribute('d'); });
  function setMaxIcon(on) {
    var d = on ? ICON_MIN : ICON_MAX;
    for (var i = 0; i < maxPaths.length && i < d.length; i++) maxPaths[i].setAttribute('d', d[i]);
  }
  /* on=true → 最大化；on=false → 还原。
     silent=true：**只退状态、一个像素都不动宽**（拖拽接管时用，见下），否则把宽度写回记忆值。 */
  function setMax(on, silent) {
    if (!maxBtn) return;
    if (on) {
      applyMaxW();
      maxBtn.setAttribute('aria-pressed', 'true');
      maxBtn.setAttribute('title', '还原侧栏宽度');
      maxBtn.setAttribute('aria-label', '还原侧栏宽度');
    } else {
      slot.removeAttribute('data-td-maxw');
      if (!silent) slot.style.setProperty('--av-browse-w', storedPanelW() + 'px');
      maxBtn.setAttribute('aria-pressed', 'false');
      maxBtn.setAttribute('title', '最大化侧栏');
      maxBtn.setAttribute('aria-label', '最大化侧栏');
    }
    setMaxIcon(on);
  }
  if (maxBtn) {
    maxBtn.addEventListener('click', function () {
      setMax(maxBtn.getAttribute('aria-pressed') !== 'true');
    });
  }
  /* ★ 第九拍 ②：**全屏态下按下分栏条 = 放弃全屏**（语义：接下来手动调宽）。
     ⚠ 只清标记 / 还原字形，**不动宽** —— 宽度交给 ctrl-conv 从**实际宽**起算；这里若先把宽度
       写回 641，就变成「一按先跳回默认宽」（正是邵先生看到的「一下就复位」）。
     ⚠ 用**文档级捕获委托**：分栏条由 ctrl-conv 在 place() 时才插进 flex 行，本文件跑得更早，
       那时它可能还不在 DOM 里（同款先例：页头那枚「打开侧栏」也是委托绑的）。 */
  document.addEventListener('pointerdown', function (e) {
    if (!e.target || !e.target.closest || !e.target.closest('#av-browse-split')) return;
    if (slot.hasAttribute('data-td-maxw')) setMax(false, true);
  }, true);
  /* ctrl-conv 的 resize 处理走单层 rAF ⇒ 本处退两层 rAF，保证「最大化态」在它之后落定。
     ★ 第九拍 ②（续）：同一个 handler 里顺手清掉「收起后残留的全屏态」。三个收起入口
       （页头开关 / 侧栏 × / Esc）最终都走 ctrl-conv 的 `setOpen(false)`，而它**必定**
       dispatch 一次 resize ⇒ 在这儿判一下就够了（此时 `.av-browse-on` 已被摘掉）。
       不清的话会留下「宽度是记忆值、按钮却仍是"还原"字形」的错位，且下次 resize 会把右栏
       突然弹回全屏宽。⚠ 用 silent：收起态下写 `--av-browse-w` 没有意义，下次打开时
       ctrl-conv 的 `setOpen(true)` 会按记忆值重设。
       ⚠ 别改成「观察 hostRow 的 class」：那条 flex 行与分栏条都是 ctrl-conv 在 place() 里
         **后插**的，本文件跑得更早 ⇒ 初次观察很可能挂在旧父级上、永不触发（本拍踩过）。 */
  window.addEventListener('resize', function () {
    var row = slot.parentElement;
    if (row && !row.classList.contains('av-browse-on') && slot.hasAttribute('data-td-maxw')) {
      setMax(false, true);
      return;
    }
    if (!slot.hasAttribute('data-td-maxw')) return;
    requestAnimationFrame(function () { requestAnimationFrame(applyMaxW); });
  });

  /* ==================== 审查模块 ==================== */
  var rvBody = pane.querySelector('.td-rv-body');
  var diffs = [].slice.call(pane.querySelectorAll('[data-td-diff]'));

  function setDiffOpen(art, open) {
    art.classList.toggle('is-open', open);
    var h = art.querySelector('[data-td-diff-h]');
    if (h) h.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function openCount() {
    var n = 0;
    for (var i = 0; i < diffs.length; i++) if (diffs[i].classList.contains('is-open')) n++;
    return n;
  }
  for (var d = 0; d < diffs.length; d++) {
    (function (art) {
      var h = art.querySelector('[data-td-diff-h]');
      if (!h) return;
      h.addEventListener('click', function () { setDiffOpen(art, !art.classList.contains('is-open')); syncFoldBtn(); });
    })(diffs[d]);
  }

  /* ★ 任务「折叠全部文件」⇄「展开全部文件」：同一枚菜单项双向切换，文案与字形都跟着翻。
     判据 —— **只要还有折叠着的文件，这一项就是「展开全部文件」**（用户此刻想看到全部）；
     全部展开时才是「折叠全部文件」。单独点某个文件夹头后也会回来同步（上面的 syncFoldBtn）。 */
  var foldBtn = pane.querySelector('[data-td-rv-fold]');
  var foldName = pane.querySelector('[data-td-rv-fold-name]');
  function syncFoldBtn() {
    if (!foldBtn || !foldName) return;
    var toExpand = openCount() < diffs.length;
    foldName.textContent = toExpand ? '展开全部文件' : '折叠全部文件';
    var ico = foldBtn.querySelector('.td-mm-ico');
    if (ico) ico.innerHTML = toExpand ? ICO_UNFOLD : ICO_FOLD;
    foldBtn.setAttribute('aria-expanded', toExpand ? 'false' : 'true');
  }
  if (foldBtn && foldName) {
    foldBtn.addEventListener('click', function () {
      var toExpand = openCount() < diffs.length;
      for (var i = 0; i < diffs.length; i++) setDiffOpen(diffs[i], toExpand);
      syncFoldBtn();
      /* 折叠/展开全部是「动作」不是开关 ⇒ 点完收菜单（与 Codex 的 Collapse all diffs 一致） */
      closeMenus(null);
    });
  }

  /* 「⋯ 折叠 N 行未改动」：展开/收起紧随其后的 `[data-td-more-row]` 行 */
  var moreBtns = pane.querySelectorAll('[data-td-more]');
  for (var m2 = 0; m2 < moreBtns.length; m2++) {
    (function (b) {
      var label = b.textContent.trim();
      b.addEventListener('click', function () {
        var open = b.classList.toggle('is-expanded');
        b.textContent = open ? label.replace('折叠', '展开') : label;
        var n = b.nextElementSibling;
        while (n && n.hasAttribute('data-td-more-row')) {
          if (open) n.removeAttribute('hidden'); else n.setAttribute('hidden', '');
          n = n.nextElementSibling;
        }
      });
    })(moreBtns[m2]);
  }

  /* 统一视图 ⇄ 并排视图 */
  var viewBtns = pane.querySelectorAll('[data-td-rv-view]');
  function setView(mode) {
    if (rvBody) rvBody.classList.toggle('is-split', mode === 'split');
    for (var k = 0; k < viewBtns.length; k++) {
      var on = viewBtns[k].getAttribute('data-td-rv-view') === mode;
      viewBtns[k].setAttribute('aria-checked', on ? 'true' : 'false');
      viewBtns[k].classList.toggle('is-checked', on);
    }
  }
  for (var v = 0; v < viewBtns.length; v++) {
    (function (b) {
      b.addEventListener('click', function () { setView(b.getAttribute('data-td-rv-view')); closeMenus(null); });
    })(viewBtns[v]);
  }

  /* 对比范围下拉（上一轮 / 本分支 / 全部未提交改动） */
  var scopeName = pane.querySelector('[data-td-rv-scope-name]');
  var rangeBtns = pane.querySelectorAll('[data-td-rv-range]');
  for (var rg = 0; rg < rangeBtns.length; rg++) {
    (function (b) {
      b.addEventListener('click', function () {
        var nm = b.querySelector('.td-mm-name');
        if (scopeName && nm) scopeName.textContent = nm.textContent;
        for (var k = 0; k < rangeBtns.length; k++) {
          var on = rangeBtns[k] === b;
          rangeBtns[k].setAttribute('aria-checked', on ? 'true' : 'false');
          rangeBtns[k].classList.toggle('is-checked', on);
        }
        closeMenus(null);
      });
    })(rangeBtns[rg]);
  }

  /* 显示选项里的复选开关：`wrap` / `worddiff` / `hidws` 真生效，其余两个只留勾选态 */
  var TOG_CLASS = { wrap: 'is-wrap', worddiff: 'is-worddiff', hidws: 'is-hidws' };
  var togBtns = pane.querySelectorAll('[data-td-rv-tog]');
  function syncTog(b) {
    var on = b.getAttribute('aria-checked') === 'true';
    b.classList.toggle('is-checked', on);
    var cls = TOG_CLASS[b.getAttribute('data-td-rv-tog')];
    if (cls && rvBody) rvBody.classList.toggle(cls, on);
  }
  for (var tg = 0; tg < togBtns.length; tg++) {
    (function (b) {
      syncTog(b);          /* 初始化：按 markup 的 aria-checked 落类（worddiff 默认开） */
      b.addEventListener('click', function () {
        b.setAttribute('aria-checked', b.getAttribute('aria-checked') === 'true' ? 'false' : 'true');
        syncTog(b);
        /* 复选开关**不收菜单** —— 便于连着设几项（VS Code 同体位）；动作类才收 */
      });
    })(togBtns[tg]);
  }

  /* 动作类：刷新 / 复制 diff / 复制 git apply / 在文件树中定位 / Open PR */
  var ACT_TEXT = {
    refresh: 'diff 已刷新',
    copy: '已复制 diff 到剪贴板',
    reveal: '已在「文件」标签中定位该文件',
    copyapply: '已复制 git apply 命令',
    pr: '已创建 Pull Request（视觉演示）'
  };
  var actBtns = pane.querySelectorAll('[data-td-rv-act]');
  for (var ac = 0; ac < actBtns.length; ac++) {
    (function (b) {
      b.addEventListener('click', function () {
        var kind = b.getAttribute('data-td-rv-act');
        closeMenus(null);
        if (kind === 'reveal') { openTab('files'); say(ACT_TEXT.reveal); return; }
        if (kind === 'refresh' && rvBody) {
          rvBody.classList.add('is-refreshing');
          setTimeout(function () { rvBody.classList.remove('is-refreshing'); }, 420);
        }
        say(ACT_TEXT[kind] || '已执行');
      });
    })(actBtns[ac]);
  }

  /* 每个文件头右侧的「暂存 / 撤销」（Codex review 面板支持 stage / revert） */
  var stageBtns = pane.querySelectorAll('[data-td-stage]');
  for (var sg = 0; sg < stageBtns.length; sg++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        var on = !b.classList.contains('is-staged');
        b.classList.toggle('is-staged', on);
        b.textContent = on ? '已暂存' : '暂存';
        say(on ? '已暂存该文件（视觉演示）' : '已取消暂存');
      });
    })(stageBtns[sg]);
  }
  var revertBtns = pane.querySelectorAll('[data-td-revert]');
  for (var rv = 0; rv < revertBtns.length; rv++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        var art = b.closest('[data-td-diff]');
        if (art) art.classList.toggle('is-reverted');
        say(art && art.classList.contains('is-reverted') ? '已撤销该文件的改动（视觉演示）' : '已恢复该文件的改动');
      });
    })(revertBtns[rv]);
  }

  /* 提交 / 推送下拉 → 提交模态 */
  var commitModal = pane.querySelector('.td-commit');
  var commitBtns = pane.querySelectorAll('[data-td-commit-act]');
  for (var cb = 0; cb < commitBtns.length; cb++) {
    (function (b) {
      b.addEventListener('click', function () {
        var kind = b.getAttribute('data-td-commit-act');
        closeMenus(null);
        if (kind === 'commit') {
          if (commitModal) commitModal.removeAttribute('hidden');
        } else {
          say('已提交并推送到 origin/main（视觉演示）');
        }
      });
    })(commitBtns[cb]);
  }
  var commitXs = pane.querySelectorAll('[data-td-commit-x]');
  for (var cx = 0; cx < commitXs.length; cx++) {
    commitXs[cx].addEventListener('click', function () { if (commitModal) commitModal.setAttribute('hidden', ''); });
  }
  var commitOk = pane.querySelector('[data-td-commit-ok]');
  if (commitOk && commitModal) {
    commitOk.addEventListener('click', function () {
      commitModal.setAttribute('hidden', '');
      say('已提交到本地（视觉演示）');
    });
  }

  /* ==================== 终端模块（本地回声，纯演示） ====================
     ★ 第十一拍 ④（r107-l2）：对照 Codex 官方「多标签终端」补齐。
       体位 —— `bindTerm(el)` 只负责「把一块 `.td-term` 变成可输入的回声终端」；
       标签条只管**显示哪一块**（切 `hidden`），各块的输出与输入各自独立、互不影响。
       ⚠ 旧实现是「一个 `term` 变量 + 闭包 `echo`」；拆成按块绑定后 `echo` 收进各自闭包，
         行为与改前逐字一致（同一份 CANNED 表、同一套 keydown 分支）。 */
  var termSec = pane.querySelector('.td-mod-term');
  var termTabsEl = termSec ? termSec.querySelector('.td-term-tabs') : null;
  var TERM_ICO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="12" height="12" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true"><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/></svg>';
  var CANNED = {
    ls: ['README.md        package.json     pages/', 'mg-work/         assets/          vite.config.js'],
    pwd: ['/e/GienCoder/giencoder-design-engineering'],
    'npm run dev': ['> vite --host', '  VITE v5.4.2  ready in 208 ms', '  ➜  Local:   http://localhost:5173/']
  };
  function termPanes() {
    return termSec ? [].slice.call(termSec.querySelectorAll('[data-td-term-pane]')) : [];
  }
  function activeTerm() {
    var p = termPanes();
    for (var i = 0; i < p.length; i++) if (!p[i].hasAttribute('hidden')) return p[i];
    return p[0] || null;
  }
  function showTerm(id, focus) {
    if (!termTabsEl) return;
    var ts = [].slice.call(termTabsEl.querySelectorAll('[data-td-term-tab]')), i;
    for (i = 0; i < ts.length; i++) {
      var on = ts[i].getAttribute('data-td-term-tab') === id;
      ts[i].classList.toggle('is-active', on);
      ts[i].setAttribute('aria-selected', on ? 'true' : 'false');
    }
    var ps = termPanes();
    for (i = 0; i < ps.length; i++) {
      if (ps[i].getAttribute('data-td-term-pane') === id) ps[i].removeAttribute('hidden');
      else ps[i].setAttribute('hidden', '');
    }
    if (focus) { var a = activeTerm(); if (a) a.focus(); }
  }
  function bindTerm(term) {
    var echo = term.querySelector('[data-td-term-echo]');
    if (!echo) return;
    function termOut(text, dim) {
      var dv = document.createElement('div');
      dv.className = 'td-term-out' + (dim ? ' is-dim' : '');
      dv.textContent = text;
      term.appendChild(dv);
    }
    function newPrompt() {
      var line = document.createElement('div');
      line.className = 'td-term-line';
      line.innerHTML = '<span class="td-term-ps">giencoder-design-engineering</span>'
        + '<span class="td-term-pd">$</span>'
        + '<span class="td-term-echo" data-td-term-echo="1"></span>'
        + '<span class="td-term-caret" data-td-term-caret="1"></span>';
      term.appendChild(line);
      echo = line.querySelector('[data-td-term-echo]');
    }
    term.addEventListener('click', function () { term.focus(); });
    term.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Enter') {
        e.preventDefault();
        var cmd = (echo.textContent || '').trim();
        if (cmd) {
          if (cmd === 'clear') {
            var outs = term.querySelectorAll('.td-term-out');
            for (var i = 0; i < outs.length; i++) outs[i].parentNode.removeChild(outs[i]);
          } else {
            var hit = CANNED[cmd];
            if (hit) { for (var j = 0; j < hit.length; j++) termOut(hit[j], j > 0); }
            else termOut('zsh: command not found: ' + cmd);
          }
        }
        newPrompt();
        term.scrollTop = term.scrollHeight;
        return;
      }
      if (e.key === 'Backspace') {
        e.preventDefault();
        echo.textContent = (echo.textContent || '').slice(0, -1);
        return;
      }
      if (e.key.length === 1) { e.preventDefault(); echo.textContent = (echo.textContent || '') + e.key; }
    });
  }
  var termTabSeq = 2;                 /* 静态已有 t1 / t2 */
  function newTermTab() {
    if (!termSec || !termTabsEl) return null;
    termTabSeq++;
    var id = 't' + termTabSeq;
    var tab = document.createElement('button');
    tab.type = 'button';
    tab.className = 'td-term-tab';
    tab.setAttribute('role', 'tab');
    tab.setAttribute('data-td-term-tab', id);
    tab.setAttribute('aria-selected', 'false');
    tab.innerHTML = '<span class="td-term-tab-ico">' + TERM_ICO + '</span>'
      + '<span class="td-term-tab-nm">终端 ' + termTabSeq + '</span>';
    var add = termTabsEl.querySelector('[data-td-term-add]');
    if (add) termTabsEl.insertBefore(tab, add); else termTabsEl.appendChild(tab);
    var box = document.createElement('div');
    box.className = 'td-term';
    box.setAttribute('tabindex', '0');
    box.setAttribute('data-td-term', '1');
    box.setAttribute('data-td-term-pane', id);
    box.setAttribute('hidden', '');
    box.innerHTML = '<div class="td-term-line"><span class="td-term-ps">giencoder-design-engineering</span>'
      + '<span class="td-term-pd">$</span>'
      + '<span class="td-term-echo" data-td-term-echo="1"></span>'
      + '<span class="td-term-caret" data-td-term-caret="1"></span></div>';
    termSec.appendChild(box);
    bindTerm(box);
    tab.addEventListener('click', function () { showTerm(id, true); });
    showTerm(id, true);
    return tab;
  }
  if (termSec) {
    var termP0 = termPanes(), tp;
    for (tp = 0; tp < termP0.length; tp++) bindTerm(termP0[tp]);
    if (termTabsEl) {
      var termT0 = [].slice.call(termTabsEl.querySelectorAll('[data-td-term-tab]'));
      for (tp = 0; tp < termT0.length; tp++) {
        (function (tb) {
          tb.addEventListener('click', function () { showTerm(tb.getAttribute('data-td-term-tab'), true); });
        })(termT0[tp]);
      }
      var termAdd = termTabsEl.querySelector('[data-td-term-add]');
      if (termAdd) termAdd.addEventListener('click', function () { newTermTab(); });
    }
    /* 静态标记已经摆好（t1 可见、t2 隐藏），这里只是把状态**对齐**一遍，
       不聚焦 —— 否则整页加载完焦点会跑到终端里（右侧面板默认还是隐藏的）。 */
    showTerm('t1', false);
  }

  /* ==================== 浏览器模块（标注态 + 元素评论） ==================== */
  var brw = pane.querySelector('.td-brw');
  var elnote = null;
  if (brw) {
    var view = brw.querySelector('[data-td-view]');
    var annotBar = brw.querySelector('[data-td-annot-bar]');
    var annotBtns = brw.querySelectorAll('[data-td-annot]');
    elnote = document.createElement('div');
    elnote.className = 'td-elnote';
    elnote.setAttribute('hidden', '');
    elnote.innerHTML = '<div class="td-elnote-t">评论元素 <b></b></div>'
      + '<textarea rows="2" aria-label="元素评论" placeholder="这个元素想怎么改？"></textarea>'
      + '<div class="td-elnote-f">'
      + '<button type="button" data-td-elnote-cancel="1">取消</button>'
      + '<button type="button" class="is-primary" data-td-elnote-ok="1">添加评论</button>'
      + '</div>';
    if (view) view.appendChild(elnote);
    function setAnnot(on) {
      brw.classList.toggle('is-annotating', on);
      if (annotBar) { if (on) annotBar.removeAttribute('hidden'); else annotBar.setAttribute('hidden', ''); }
      for (var i = 0; i < annotBtns.length; i++) {
        annotBtns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
      }
      if (!on) elnote.setAttribute('hidden', '');
    }
    for (var ab = 0; ab < annotBtns.length; ab++) {
      annotBtns[ab].addEventListener('click', function () {
        setAnnot(!brw.classList.contains('is-annotating'));
      });
    }
    if (view) {
      view.addEventListener('click', function (e) {
        if (!brw.classList.contains('is-annotating')) return;
        var el = e.target && e.target.closest ? e.target.closest('[data-td-el]') : null;
        if (!el) return;
        var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
        elnote.style.top = (er.bottom - vr.top + view.scrollTop + 8) + 'px';
        var b = elnote.querySelector('.td-elnote-t b');
        if (b) b.textContent = el.className.replace('td-page-card', '卡片').replace('td-page-cta', '主按钮') || '元素';
        elnote.removeAttribute('hidden');
      });
    }
    var noteCancel = elnote.querySelector('[data-td-elnote-cancel]');
    var noteOk = elnote.querySelector('[data-td-elnote-ok]');
    if (noteCancel) noteCancel.addEventListener('click', function () { elnote.setAttribute('hidden', ''); });
    if (noteOk) {
      noteOk.addEventListener('click', function () {
        elnote.setAttribute('hidden', '');
        setAnnot(false);
        say('评论已带入对话（视觉演示）');
      });
    }
    var BRW_TEXT = {
      send: '已把当前页面发到对话（视觉演示）',
      shot: '已复制截图到剪贴板（视觉演示）',
      zoom: '缩放：100%（视觉演示）',
      more: '更多浏览器选项（视觉演示）'
    };
    /* ★ 第十一拍 ④（r107-l2）：官方「一键截图到剪贴板」= 快门白闪。
       ⚠ 闪的是**整个浏览器模块**（`.td-brw`）而不是 `.td-view`：`.td-view` 自己是
         `overflow:auto` 的滚动容器，绝对定位子元素会跟着内容滚走 ⇒ 滚动后就闪不见了。 */
    function shotFlash() {
      brw.classList.remove('is-shot');
      void brw.offsetWidth;                       /* 强制回流：同一个 class 的动画能重播 */
      brw.classList.add('is-shot');
      setTimeout(function () { brw.classList.remove('is-shot'); }, 300);
    }
    var brwActs = pane.querySelectorAll('[data-td-brw-act]');
    for (var ba = 0; ba < brwActs.length; ba++) {
      (function (b) {
        b.addEventListener('click', function () {
          var kind = b.getAttribute('data-td-brw-act');
          if (kind === 'shot') shotFlash();
          say(BRW_TEXT[kind] || '已执行');
        });
      })(brwActs[ba]);
    }
  }

  /* ==================== 摘要模块 ==================== */
  var sumActs = pane.querySelectorAll('[data-td-sum-act]');
  for (var sa = 0; sa < sumActs.length; sa++) {
    sumActs[sa].addEventListener('click', function () { say('已复制会话摘要'); });
  }
  /* ★ 第十一拍 ④（r107-l2）：产物预览层 —— 对照官方「产物查看器」。
     原来「预览」只弹一句 toast、没有任何视觉，属于真缺口；现在打开一层覆盖整块摘要的
     只读预览（文件名 + 元信息 + 骨架：文档 / 表格两套），并给「在系统打开」「关闭」。 */
  var prevEl = pane.querySelector('[data-td-prev]');
  function prevHide() { if (prevEl) prevEl.setAttribute('hidden', ''); }
  function prevShow(btn) {
    if (!prevEl) return;
    var host = btn && btn.closest ? btn.closest('.td-sum-art') : null;
    var nmEl = host && host.querySelector('.td-sum-artt b');
    var mtEl = host && host.querySelector('.td-sum-artt i');
    var ico = host && host.querySelector('.td-sum-arti svg');
    var name = nmEl ? nmEl.textContent : '产物';
    var kind = (/\.(xlsx|xls|csv|tsv)$/i).test(name) ? 'xlsx' : 'md';
    var pn = prevEl.querySelector('[data-td-prev-name]');
    var pm = prevEl.querySelector('[data-td-prev-meta]');
    var pi = prevEl.querySelector('[data-td-prev-ico]');
    if (pn) pn.textContent = name;
    if (pm) pm.textContent = (mtEl ? mtEl.textContent : '') + ' · 只读预览';
    if (pi && ico) pi.innerHTML = ico.outerHTML;
    var bodies = prevEl.querySelectorAll('[data-td-prev-kind]');
    for (var q = 0; q < bodies.length; q++) {
      if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');
      else bodies[q].setAttribute('hidden', '');
    }
    prevEl.removeAttribute('hidden');
  }
  var artBtns = pane.querySelectorAll('[data-td-art]');
  for (var ar = 0; ar < artBtns.length; ar++) {
    (function (b) {
      b.addEventListener('click', function () { prevShow(b); });
    })(artBtns[ar]);
  }
  if (prevEl) {
    var prevXs = prevEl.querySelectorAll('[data-td-prev-x], [data-td-prev-close]');
    for (var px = 0; px < prevXs.length; px++) prevXs[px].addEventListener('click', prevHide);
    var prevOpenBtn = prevEl.querySelector('[data-td-prev-open]');
    if (prevOpenBtn) {
      prevOpenBtn.addEventListener('click', function () { say('已在系统应用中打开（视觉演示）'); });
    }
  }

  /* ==================== 空白包裹（供「隐藏空白」开关压暗） ====================
     只拆**文本节点**再重组，不碰任何 HTML 字符串 ⇒ 代码里已有的实体转义安全。 */
  function wrapWs(root) {
    if (!root) return;
    var cells = root.querySelectorAll('.td-dr-t');
    for (var i = 0; i < cells.length; i++) {
      var el = cells[i];
      if (el.querySelector('.td-dr-ws')) continue;
      var kids = [].slice.call(el.childNodes);
      for (var k = 0; k < kids.length; k++) {
        var node = kids[k];
        if (node.nodeType !== 3) continue;
        var txt = node.nodeValue;
        if (!/ {2,}/.test(txt)) continue;
        var parts = txt.split(/( {2,})/), frag = document.createDocumentFragment();
        for (var p = 0; p < parts.length; p++) {
          if (!parts[p]) continue;
          if (/^ {2,}$/.test(parts[p])) {
            var sp = document.createElement('span');
            sp.className = 'td-dr-ws';
            sp.textContent = parts[p];
            frag.appendChild(sp);
          } else {
            frag.appendChild(document.createTextNode(parts[p]));
          }
        }
        el.replaceChild(frag, node);
      }
    }
  }

  /* ==================== 剪贴板（右键菜单 / 划词浮条共用） ==================== */
  function copyText(text, label) {
    var t = document.createElement('textarea');
    t.value = String(text == null ? '' : text);
    t.setAttribute('readonly', '');
    t.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0;';
    document.body.appendChild(t);
    t.select();
    try { document.execCommand('copy'); } catch (err) { /* file:// 下也可能失败 ⇒ 只提示不报错 */ }
    document.body.removeChild(t);
    say(label);
  }

  /* ==================== 右键菜单（表驱动：一份容器承载七类目标） ====================
     为什么是一份容器：七类目标（标签栏 / 审查文件 / 审查代码行 / 终端 / 浏览器 / 摘要来源 /
     摘要产物 / 计划条目）的菜单结构完全同构（图标 + 名称 + 右侧快捷键），写七份静态 DOM
     等于把 HTML 乘七、以后加一项要改七处。这里按目标现场生成条目，HTML 只留一个空盒子。
     ★ 定位用 `position: fixed` + 指针视口坐标 ⇒ 不受任何模块 `overflow:hidden` 影响，
       也不必知道目标落在哪个模块里（这正是它比「每模块一个绝对定位菜单」省事的地方）。
     ★ 能复用既有 handler 的一律 `元素.click()`（暂存 / 撤销 / 预览 / 折叠全部…），
       不在菜单里重写一遍状态逻辑 —— 否则同一个状态会有两套写法、早晚对不上。 */
  var CTX_SVG_HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true">';
  var CTX_PATH = {
    close: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    refresh: '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>',
    copy: '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    stage: '<circle cx="12" cy="12" r="3.5"/><path d="M3 12h5.5"/><path d="M15.5 12H21"/>',
    undo: '<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>',
    pin: '<circle cx="12" cy="12" r="7"/><path d="M12 2v3"/><path d="M12 19v3"/><path d="M2 12h3"/><path d="M19 12h3"/>',
    code: '<path d="m8 9-3 3 3 3"/><path d="m16 9 3 3-3 3"/><path d="M13 7l-2 10"/>',
    link: '<path d="M14 4h6v6"/><path d="M20 4 10 14"/><path d="M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"/>',
    back: '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    fwd: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    eye: '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6Z"/><circle cx="12" cy="12" r="2.5"/>',
    annot: '<circle cx="12" cy="12" r="9"/><path d="M12 8v8"/><path d="M8 12h8"/>',
    kill: '<path d="M4 7h16"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/><path d="M6 7l1 12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-12"/>',
    msg: '<path d="M21 12a8 8 0 0 1-8 8H7l-4 3v-5.6A8 8 0 0 1 11 4h2a8 8 0 0 1 8 8Z"/>',
    plus: '<path d="M5 12h14"/><path d="M12 5v14"/>',
    all: '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    paste: '<rect x="8" y="3" width="8" height="4" rx="1"/><path d="M6 5H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-1"/>',
    play: '<path d="M7 5l12 7-12 7Z"/>',
    dot: '<circle cx="12" cy="12" r="8"/>',
    ok: '<circle cx="12" cy="12" r="8"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    stop: '<rect x="6" y="6" width="12" height="12" rx="2"/>'
  };
  function ctxIco(k) { return k && CTX_PATH[k] ? CTX_SVG_HEAD + CTX_PATH[k] + '</svg>' : ''; }

  function ctxClick(root, sel) { var b = root && root.querySelector(sel); if (b) b.click(); }
  function ctxTxt(el) { return el ? String(el.textContent || '').trim() : ''; }
  function ctxSelectTerm(host) {
    if (!host || !window.getSelection) { say('已全选终端内容'); return; }
    var rg = document.createRange();
    rg.selectNodeContents(host);
    var s = window.getSelection();
    s.removeAllRanges();
    s.addRange(rg);
    say('已全选终端内容');
  }
  function ctxAnnotEnter() {
    var b = pane.querySelector('.td-url [data-td-annot]');
    var bar = pane.querySelector('[data-td-annot-bar]');
    if (b && bar && bar.hasAttribute('hidden')) b.click();
    say('已进入标注模式，点击页面元素添加评论');
  }
  function ctxFocusNote(art) {
    var note = art && art.querySelector('.td-note');
    if (note && note.scrollIntoView) note.scrollIntoView({ block: 'center' });
    say(note ? '已定位到该文件的评论' : '已在该行添加评论（视觉演示）');
  }

  /* ---- 七类目标的菜单定义（返回 null = 不接管，放行系统右键菜单） ---- */
  function ctxForTab(tab) {
    var nm = ctxTxt(tab.querySelector('.td-tab-name')) || '标签';
    return { head: nm, items: [
      { label: '关闭', key: '⌘W', ico: 'close', act: function () { closeTab(tab); } },
      { label: '关闭其他标签', ico: 'close', act: function () { closeOthers(tab); } },
      { label: '关闭右侧标签', ico: 'close', act: function () { closeRight(tab); } },
      { label: '关闭全部标签', ico: 'close', act: function () { closeAll(); } },
      '-',
      { label: '重新加载此模块', key: '⌘R', ico: 'refresh', act: function () { reloadTab(tab); } }
    ] };
  }
  function ctxForFile(art) {
    var path = ctxTxt(art.querySelector('.td-diff-path')) || '文件';
    var staged = !!(art.querySelector('[data-td-stage].is-staged'));
    var reverted = art.classList.contains('is-reverted');
    var toExpand = openCount() < diffs.length;
    return { head: path, items: [
      { label: staged ? '取消暂存此文件' : '暂存此文件', ico: 'stage', act: function () { ctxClick(art, '[data-td-stage]'); } },
      { label: reverted ? '恢复此文件的改动' : '撤销此文件的改动', ico: 'undo', danger: !reverted, act: function () { ctxClick(art, '[data-td-revert]'); } },
      '-',
      { label: '复制文件路径', ico: 'copy', act: function () { copyText(path, '已复制文件路径'); } },
      { label: '复制 git apply 命令', ico: 'code', act: function () { say(ACT_TEXT.copyapply); } },
      { label: '在文件树中定位', ico: 'pin', act: function () { openTab('files'); say(ACT_TEXT.reveal); } },
      '-',
      { label: toExpand ? '展开全部文件' : '折叠全部文件', ico: toExpand ? 'plus' : 'close', act: function () { if (foldBtn) foldBtn.click(); } }
    ] };
  }
  function ctxForRow(row) {
    var art = row.closest('[data-td-diff]');
    var path = art ? ctxTxt(art.querySelector('.td-diff-path')) : '';
    var line = ctxTxt(row.querySelector('.td-dr-t'));
    return { head: path || '改动行', items: [
      { label: '在此行添加评论', ico: 'msg', act: function () { ctxFocusNote(art); } },
      { label: '复制此行', ico: 'copy', act: function () { copyText(line, '已复制此行'); } },
      { label: '复制文件路径', ico: 'copy', act: function () { copyText(path, '已复制文件路径'); } },
      '-',
      { label: '暂存此文件', ico: 'stage', act: function () { ctxClick(art, '[data-td-stage]'); } },
      { label: '撤销此文件的改动', ico: 'undo', danger: true, act: function () { ctxClick(art, '[data-td-revert]'); } }
    ] };
  }
  function ctxForTerm() {
    var host = activeTerm();
    var cleared = !!(host && host.classList.contains('is-cleared'));
    var curTab = termTabsEl ? ctxTxt(termTabsEl.querySelector('.td-term-tab.is-active .td-term-tab-nm')) : '';
    return { head: '终端 · ' + (curTab || 'giencoder-design-engineering'), items: [
      { label: '复制', key: '⌘C', ico: 'copy', act: function () { var s = window.getSelection(); copyText(s ? String(s) : '', '已复制终端内容'); } },
      { label: '粘贴', key: '⌘V', ico: 'paste', act: function () { say('已粘贴（视觉演示）'); } },
      { label: '全选', key: '⌘A', ico: 'all', act: function () { ctxSelectTerm(host); } },
      '-',
      { label: cleared ? '恢复输出' : '清空', key: '⌃L', ico: cleared ? 'refresh' : 'kill', act: function () {
        if (host) host.classList.toggle('is-cleared');
        say(cleared ? '已恢复终端输出' : '已清空终端（可再点「恢复输出」）');
      } },
      { label: '新建终端标签', ico: 'plus', act: function () {
        var t2 = newTermTab();
        say(t2 ? '已新建终端标签' : '终端不可用');
      } },
      { label: '终止正在运行的进程', ico: 'stop', danger: true, act: function () { say('已终止进程（视觉演示）'); } }
    ] };
  }
  function ctxForBrw(t) {
    var el = t.closest ? t.closest('[data-td-el]') : null;
    var input = pane.querySelector('.td-url-pill input');
    var url = input ? input.value : 'localhost:5173/';
    var items = [];
    if (el) {
      items.push({ label: '标注此元素', ico: 'annot', act: function () { ctxAnnotEnter(); } });
      items.push('-');
    }
    items.push({ label: '后退', key: '⌘[', ico: 'back', act: function () { say('已后退（视觉演示）'); } });
    items.push({ label: '前进', key: '⌘]', ico: 'fwd', act: function () { say('已前进（视觉演示）'); } });
    items.push({ label: '刷新页面', key: '⌘R', ico: 'refresh', act: function () { say('已刷新页面（视觉演示）'); } });
    items.push('-');
    items.push({ label: '复制页面链接', key: '⇧⌘C', ico: 'link', act: function () { copyText('http://' + url, '已复制页面链接'); } });
    items.push({ label: '截图到剪贴板', key: '⇧⌘S', ico: 'pin', act: function () {
      var sb = pane.querySelector('[data-td-brw-act="shot"]');
      if (sb) sb.click();
    } });
    items.push({ label: '在系统浏览器中打开', ico: 'eye', act: function () { say('已在系统浏览器中打开（视觉演示）'); } });
    return { head: 'http://' + url, items: items };
  }
  function ctxForSrc(a) {
    var href = a.getAttribute('href') || '';
    var title = ctxTxt(a.querySelector('.td-sum-srct b')) || href;
    return { head: title, items: [
      { label: '复制链接', ico: 'copy', act: function () { copyText(href, '已复制链接'); } },
      { label: '在右栏浏览器中打开', ico: 'eye', act: function () { openTab('browser'); say('已在右栏浏览器中打开（视觉演示）'); } },
      { label: '在系统浏览器中打开', ico: 'link', act: function () { say('已在系统浏览器中打开（视觉演示）'); } }
    ] };
  }
  function ctxForArt(a) {
    var name = ctxTxt(a.querySelector('.td-sum-artt b')) || '产物';
    return { head: name, items: [
      { label: '预览', ico: 'eye', act: function () { ctxClick(a, '[data-td-art]'); } },
      { label: '复制文件名', ico: 'copy', act: function () { copyText(name, '已复制文件名'); } },
      { label: '在文件树中定位', ico: 'pin', act: function () { openTab('files'); say(ACT_TEXT.reveal); } }
    ] };
  }
  function ctxForPlan(li) {
    return { head: ctxTxt(li).slice(0, 32), items: [
      { label: '标记为已完成', ico: 'ok', act: function () { li.className = 'is-done'; say('已标记为已完成'); } },
      { label: '标记为进行中', ico: 'play', act: function () { li.className = 'is-doing'; say('已标记为进行中'); } },
      { label: '标记为待办', ico: 'dot', act: function () { li.className = ''; say('已标记为待办'); } },
      '-',
      { label: '复制此条', ico: 'copy', act: function () { copyText(ctxTxt(li), '已复制计划条目'); } }
    ] };
  }
  function ctxTarget(t) {
    if (!t || !t.closest) return null;
    var tab = t.closest('.td-browse-tab');
    if (tab) return ctxForTab(tab);
    var row = t.closest('.td-dr, .td-dsc');
    if (row) return ctxForRow(row);
    var art = t.closest('[data-td-diff]');
    if (art) return ctxForFile(art);
    if (t.closest('.td-term')) return ctxForTerm();
    if (t.closest('.td-brw')) return ctxForBrw(t);
    var src = t.closest('.td-sum-src');
    if (src) return ctxForSrc(src);
    var out = t.closest('.td-sum-art');
    if (out) return ctxForArt(out);
    var plan = t.closest('.td-sum-plan li');
    if (plan) return ctxForPlan(plan);
    return null;
  }

  function ctxHide() {
    if (!ctxEl) return;
    ctxEl.setAttribute('hidden', '');
    ctxEl.classList.remove(POP_OPEN);
  }
  function ctxBuild(spec) {
    ctxEl.innerHTML = '';
    if (spec.head) {
      var h = document.createElement('div');
      h.className = 'td-ctx-head';
      h.textContent = spec.head;
      ctxEl.appendChild(h);
    }
    for (var i = 0; i < spec.items.length; i++) {
      var it = spec.items[i];
      if (it === '-') {
        var ln = document.createElement('span');
        ln.className = 'td-mm-line giencoder-dropdown-divider';
        ctxEl.appendChild(ln);
        continue;
      }
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'menuitem');
      b.className = 'td-ctx-item giencoder-dropdown-item' + (it.danger ? ' is-danger' : '');
      var ic = ctxIco(it.ico);
      if (ic) {
        var sp = document.createElement('span');
        sp.className = 'td-mm-ico';
        sp.innerHTML = ic;
        b.appendChild(sp);
      }
      var nm = document.createElement('span');
      nm.className = 'td-mm-name';
      nm.textContent = it.label;
      b.appendChild(nm);
      if (it.key) {
        var kk = document.createElement('span');
        kk.className = 'td-ctx-key';
        kk.textContent = it.key;
        b.appendChild(kk);
      }
      (function (node, fn) {
        node.addEventListener('click', function () { ctxHide(); if (fn) fn(); });
      })(b, it.act);
      ctxEl.appendChild(b);
    }
  }
  function ctxShow(e, spec) {
    if (!ctxEl) return;
    ctxBuild(spec);
    /* 先摆到视口左上角量尺寸，再按指针位置翻边（贴右 / 下缘时向左上展开）
       ⚠ 坐标写成**自定义属性**而不是行内 `left/top`：本页 r93 那条通配适配层带
       `top: auto !important`，连行内样式都压得过 ⇒ 行内 top 会失效、菜单弹到页面外面去。 */
    ctxEl.style.setProperty('--td-ctx-x', '0px');
    ctxEl.style.setProperty('--td-ctx-y', '0px');
    ctxEl.removeAttribute('hidden');
    ctxEl.classList.add(POP_OPEN);
    var w = ctxEl.offsetWidth, h = ctxEl.offsetHeight;
    var x = e.clientX, y = e.clientY;
    if (x + w > window.innerWidth - 8) x = Math.max(8, x - w);
    if (y + h > window.innerHeight - 8) y = Math.max(8, y - h);
    ctxEl.style.setProperty('--td-ctx-x', Math.round(x) + 'px');
    ctxEl.style.setProperty('--td-ctx-y', Math.round(y) + 'px');
  }
  /* 只在右栏内、且命中了受支持的目标时才接管右键；其余一律放行系统菜单
     （不去动页面上其它模块的右键行为 —— 这是「不得改动其他模块」的一部分）。 */
  document.addEventListener('contextmenu', function (e) {
    var spec = null;
    try { if (pane && pane.contains(e.target)) spec = ctxTarget(e.target); } catch (err) { spec = null; }
    if (!spec) return;
    e.preventDefault();
    closeMenus(null);
    ctxShow(e, spec);
  });

  /* ==================== 划词浮条 ====================
     第三拍把「侧边聊天」整段删掉时，连带把这个浮条也删了 —— 但划词本身是通用能力，
     不该跟着一起没。本轮恢复，动作换成两个仍然成立的：「添加到对话」「复制」。
     ★ 选区限定在 `.r93-scroll`（主对话口）内 ⇒ 不干扰右栏、也不干扰顶栏 / aside。 */
  var SEL_COMBO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true">';
  var selbar = null;
  var selText = '';
  function selHide() { if (selbar && !selbar.hasAttribute('hidden')) selbar.setAttribute('hidden', ''); }
  function selEnsure() {
    if (selbar) return selbar;
    selbar = document.createElement('div');
    selbar.className = 'td-selbar';
    selbar.setAttribute('role', 'toolbar');
    selbar.setAttribute('aria-label', '选中内容的操作');
    selbar.setAttribute('hidden', '');
    var add = document.createElement('button');
    add.type = 'button';
    add.className = 'giencoder-btn giencoder-btn-text giencoder-btn-size-small';
    add.innerHTML = SEL_COMBO + '<path d="M5 12h14"/><path d="M12 5v14"/></svg><span>添加到对话</span>';
    var cp = document.createElement('button');
    cp.type = 'button';
    cp.className = 'giencoder-btn giencoder-btn-text giencoder-btn-size-small';
    cp.innerHTML = SEL_COMBO + CTX_PATH.copy + '</svg><span>复制</span>';
    add.addEventListener('click', function () { selToComposer(); });
    cp.addEventListener('click', function () { copyText(selText, '已复制所选内容'); selHide(); });
    selbar.appendChild(add);
    selbar.appendChild(cp);
    document.body.appendChild(selbar);
    return selbar;
  }
  function selShow(rect) {
    selEnsure();
    selbar.style.left = '0px';
    selbar.style.top = '0px';
    selbar.removeAttribute('hidden');
    var w = selbar.offsetWidth, h = selbar.offsetHeight;
    var x = rect.left + rect.width / 2 - w / 2;
    var y = rect.top - h - 8;
    if (y < 8) y = rect.bottom + 8;                       /* 上方放不下 ⇒ 翻到选区下方 */
    x = Math.min(Math.max(8, Math.round(x)), Math.max(8, window.innerWidth - w - 8));
    y = Math.min(Math.round(y), Math.max(8, window.innerHeight - h - 8));
    selbar.style.left = x + 'px';
    selbar.style.top = y + 'px';
  }
  /* 「添加到对话」：往真 composer（`<textarea>`）里插一段引用。
     手段取「focus + `insertText`」而不是直接改 `.value` —— 前者走原生输入路径、
     React 的 onChange 收得到；后者会被 React 的受控值在下一次渲染时抹掉。 */
  function selComposer() {
    var list = document.querySelectorAll('textarea');
    for (var i = 0; i < list.length; i++) {
      var ph = list[i].getAttribute('placeholder') || '';
      if (ph.indexOf('描述你的任务') === 0) return list[i];
    }
    return null;
  }
  function selToComposer() {
    var text = selText;
    selHide();
    var ta = selComposer();
    if (!ta) { say('已添加引用（未找到输入框）'); return; }
    var quote = text.split('\n').map(function (l) { return '> ' + l; }).join('\n') + '\n';
    ta.focus();
    var ok = false;
    try {
      var end = ta.value.length;
      ta.setSelectionRange(end, end);
      ok = document.execCommand('insertText', false, quote);
    } catch (err) { ok = false; }
    if (!ok) {
      var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      setter.call(ta, ta.value + quote);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    say('已添加到对话');
  }
  document.addEventListener('mouseup', function (e) {
    if (selbar && selbar.contains(e.target)) return;
    var sel = window.getSelection();
    var text = sel ? String(sel.toString()) : '';
    if (!text || !text.trim() || !sel.rangeCount) { selHide(); return; }
    if (!e.target || !e.target.closest || !e.target.closest('.r93-scroll')) { selHide(); return; }
    var rect = sel.getRangeAt(0).getBoundingClientRect();
    if (!rect || (!rect.width && !rect.height)) { selHide(); return; }
    selText = text;
    selShow(rect);
  });
  document.addEventListener('mousedown', function (e) {
    if (selbar && selbar.contains(e.target)) return;      /* 浮条自己不算「点了别处」 */
    selHide();
  }, true);
  window.addEventListener('scroll', function () { selHide(); }, true);
  window.addEventListener('resize', selHide);

  /* ==================== 右栏快捷键 ====================
     只绑浏览器**没有抢占**的组合（⌘T / ⌘P 是浏览器级，网页拦不住 ⇒ 不绑，改由 `+` 菜单承担）。 */
  var HOTKEYS = [
    { key: 'G', shift: true, ctrl: true, mod: 'review' },     /* ⇧⌘G 审查 */
    { key: 'E', shift: true, ctrl: true, mod: 'files' },      /* ⇧⌘E 文件 */
    { key: '`', ctrl: true, mod: 'terminal' }                 /* ⌃`  终端 */
  ];
  window.addEventListener('keydown', function (e) {
    if (!(e.ctrlKey || e.metaKey)) return;
    var t = e.target, tag = (t && t.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
    for (var i = 0; i < HOTKEYS.length; i++) {
      var h = HOTKEYS[i];
      if (e.key !== h.key && e.key.toLowerCase() !== h.key.toLowerCase()) continue;
      if (!!h.shift !== e.shiftKey) continue;
      if (!!h.alt) continue;
      e.preventDefault();
      openTab(h.mod);
      return;
    }
  });

  /* ==================== Esc 裁决（window 捕获段，比 ctrl-conv 更早） ==================== */
  window.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var modal = commitModal && !commitModal.hasAttribute('hidden');
    /* ★ 搜索根 = `pane` 不是 `bar`（同 closeMenus）。用 `bar` 时各模块工具条里的菜单永远
       查不到 ⇒ 本处理器在「只有显示选项开着」时直接 `return`，既不 preventDefault 也不
       stopPropagation ⇒ 事件落到 ctrl-conv 的 Esc 上**把整条侧栏关掉**。 */
    var menuOpen = pane.querySelector('.td-mod-menu:not([hidden]), .td-rv-menu:not([hidden]), .td-ctxmenu:not([hidden])');
    var noteOpen = elnote && !elnote.hasAttribute('hidden');
    /* 划词浮条也占一层：先关它，再关菜单，最后才轮到整条侧栏（本轮恢复划词时一并接回）。 */
    var selOpen = selbar && !selbar.hasAttribute('hidden');
    /* ★ 第十一拍 ④（r107-l2）：产物预览层也占一层（不接进来的话，开着预览按 Esc 会
       直接把**整条侧栏**关掉 —— 那是 ctrl-conv.js 的 Esc 在处理）。 */
    var prevOpen = prevEl && !prevEl.hasAttribute('hidden');
    if (!modal && !menuOpen && !noteOpen && !selOpen && !prevOpen) return;
    e.preventDefault();
    e.stopPropagation();
    if (selOpen) { selHide(); return; }
    if (modal) { commitModal.setAttribute('hidden', ''); return; }
    if (menuOpen) { closeMenus(null); return; }
    if (noteOpen) { elnote.setAttribute('hidden', ''); return; }
    if (prevOpen) prevHide();
  }, true);

  /* ==================== 输入卡下方那行统计文字 → 改成真 DOM ====================
     ★ 第六拍 ①：那行「N 轮 · N 步 · …」原本是 r97 ④ 用 CSS `::after` 生成的内容
     （挂在 React 渲染的 `div.mt-8` 上）。**生成内容不在 DOM 里** ⇒ 任何浏览器都无法把
     它纳入选区，鼠标框选不到；改成真节点后即可正常选中（版式由 panel.css 第 10 节复刻）。
     ⚠ 宿主是 React 的地盘，两个坑都要兜：
        ① 重渲染会把这个不认识的节点摘掉 ⇒ 要能自动补回来；
        ② 重挂时 React 会把输入卡插到**末尾**，我们要把自己**再挪回末尾**
           （否则统计行会跑到输入卡上面去）。
     ⇒ 用 MutationObserver 盯着 `document.body` 子树，回调里只做「判存 + 不在末尾就挪」，
       自己造成的 mutation 会再进一次回调、第二次判存即返回 ⇒ 天然收敛，不会打架。
     ⚠ 文案与旧伪元素逐字一致（含两个不换行空格），换掉后视觉零差异。 */
  var STATS_SEL = 'main > div > div.flex-1.justify-center > div.mt-8';
  var STATS_TEXT = '2 轮 · 27 步 · LLM 3m36s · 工具调用 7.2s · 首 token 平均 0.8s · '
    + '159 tok/s · 缓存命中 96% · 输入 1M tok · 输出 31.1K token';

  function statsSync() {
    var host = document.querySelector(STATS_SEL);
    if (!host) return;
    var el = host.querySelector(':scope > .r107-stats');
    if (!el) {
      el = document.createElement('div');
      el.className = 'r107-stats';
      el.textContent = STATS_TEXT;
    }
    if (host.lastElementChild !== el) host.appendChild(el);
  }

  function statsBoot() {
    statsSync();
    new MutationObserver(statsSync).observe(document.body, { childList: true, subtree: true });
  }

  /* ==================== 初始化 ==================== */
  for (var t0 = 0; t0 < tabs().length; t0++) bindTab(tabs()[t0]);
  syncSingle();
  wrapWs(rvBody);
  syncFoldBtn();
  /* ★ 本轮：右栏默认页签 = **摘要**（`_head.html` 里的初始标签也同步换成了摘要）。
     两处必须一致 —— 只改一处会出现「标签高亮摘要、正文却是文件」。 */
  activate('summary');
  /* ★ 第六拍 ①：把输入卡下方那行统计文字从 CSS 伪元素换成真节点（可框选）。 */
  statsBoot();
})();
