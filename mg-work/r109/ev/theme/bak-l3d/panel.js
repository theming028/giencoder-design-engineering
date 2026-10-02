/* ================================================================================
   ★ r107 · 侧栏模块标签化控制器（会话详情页）
   职责（全部只作用于 `.td-browse` 这一块，不碰页面其它模块）：
     ① 标签增删切换 + 拖拽重排 + `+` 模块菜单
     ② （★ r108-l7 ②：原「侧栏最大化 / 还原」已按邵先生要求整段删除，见下方留痕注释）
     ③ 审查：文件折叠（点头部 = 单个 / 菜单 = 全部⇄展开全部）/ 统一⇄并排 / 对比范围 / 显示选项八项
       / 「折叠 N 行未改动」/ 暂存·撤销 / 复制·定位·PR / 提交·推送下拉 + 提交模态
     ④ 终端：本地回声（不发请求，纯前端演示）
     ⑤ 浏览器：标注态 + 元素评论气泡
     ⑥ 摘要：会话摘要 / 计划 / 来源 / 产物（静态展示 + 复制反馈）
     ⑦ 通用：划词浮条（★ r108-l8 ① 起覆盖**整个右栏**，不再只限主对话口）
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

  /* ⚠ 右栏宽度（`--av-browse-w`）与其记忆 key `giencoder:r105-browse:v1` 的**拖拽 / 持久化**
     一直归宿主 `ctrl-conv.js`（它自算上下限）。
     ★ r108-l7 ②：原先这里还声明 `DEF_PANEL / MIN_PANEL / MAIN_MIN / STORE_KEY` 供
       「最大化 / 还原」自算宽度；该功能整段删除后它们已无消费者，一并清掉。 */

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
    if (ex) {
      /* ★ 第十六拍 ①：**复用已有页签时要同步页签名与图标**。产物预览是「同一枚页签
         承载多个文件」（连点两个产物只更新内容），不同步就会出现「页签写着 .md、
         正文是 .xlsx 表格」的自相矛盾。
         ⚠ 只在本调用方给了 `opts` 时才改：`+` 菜单 / 右键菜单那几处不传 `opts`
           ⇒ 不会误改「文件 / 审查 / 终端 / 浏览器」的页签名。 */
      if (opts) {
        var nmx = ex.querySelector('.td-tab-name');
        if (nmx && opts.name) nmx.textContent = opts.name;
        var icx = ex.querySelector('.td-tab-ico');
        if (icx && opts.ico) icx.innerHTML = opts.ico;
        var xx = ex.querySelector('[data-td-tab-x]');
        if (xx && opts.name) xx.setAttribute('aria-label', '关闭「' + opts.name + '」标签');
      }
      activate(mod); ensureOpen(); return ex;
    }
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
    /* ★ 第十六拍 ①：`opts.ico`（一段 svg 字符串）优先 —— 「产物预览」这个页签没有
       对应的 `+` 模块菜单项（`src` 恒为 null），图标只能由调用方给（取自产物行
       自己的 `.td-sum-arti svg`）。 */
    if (opts && opts.ico) ico.innerHTML = opts.ico;
    else if (mi) ico.innerHTML = mi.innerHTML;
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
     ★★ r108-l6 ①：`.td-mod-menu` 原先走同一条 `toggleMenu` 却被这里「直接放行」，吃的是
       基类 CSS 里写死的 `left: 64px` ⇒ 它的触发器 `+` 一随页签数量右移，两者就脱钩
       （1440 三枚页签实测 dx = −218px）。⇒ 白名单改成 `PLACE_ABS`，两类都按几何现场摆位。
       ⚠ 别用「排除法」：`.td-ctxmenu`（`position: fixed` 跟指针）与 `.zd-menu`（在
         `.zd-host` 里、另一个包含块）都不能吃这套算法，必须显式列白名单。 */
  var RV_GAP = 6, RV_PAD = 4;
  /* ★ r108-l6 ①：可现场摆位的两族 —— `.td-mod-menu`（标签栏 `+`）/ `.td-rv-menu`（审查工具条）。 */
  var PLACE_ABS = ['td-mod-menu', 'td-rv-menu'];
  function placeRv(menu, trigger) {
    if (!trigger) return;
    var placeable = false;
    for (var pa = 0; pa < PLACE_ABS.length; pa++) {
      if (menu.classList.contains(PLACE_ABS[pa])) { placeable = true; break; }
    }
    if (!placeable) return;
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
      /* ★★ r108-l8 ②（邵先生：「菜单出现的瞬间会有闪烁或跳动或位移现象，不够自然」）：
         根因 = **「摘 `[hidden]`」与「挂开态类」挤在同一个 tick**。
         `[hidden]` 生效时元素是 `display:none`，浏览器**拿不到「改前样式」** ⇒ 紧随其后的
         `display:none → flex` 那次样式变更里，`opacity / translate / scale` 的过渡被
         **静默跳过**。真机 rAF 逐帧采样（关态采 4 帧 → 第 5 帧点开 → 再采 30 帧）证实：
           · `menu.getAnimations()` **恒为 `[]`**；
           · `opacity / translate / scale` 在**同一帧内**直接从基态落到终态。
         ⇒ 契约里那条 0.2s spring 入场**从未运行过**，观感就是「硬切弹出来」。
         ⇒ 下面四行拆两步：① 摘 `[hidden]`（元素进入 `display:flex` + 基态
            `opacity:0 / visibility:hidden / translate:0 4px / scale:.96`，仍然不可见）；
            ② `void menu.offsetWidth` **强制重排** —— 逼浏览器把上面那份「改前样式」记账；
            ③ `placeRv()` 摆位（在「第一帧可见」之前定好 ⇒ **零位移**）；
            ④ 最后才挂 `.giencoder-popup-open` ⇒ 过渡正常起跑。
         同机同页对照实测（两例写法只差一行强制重排）：
           · 旧写法：anims = `[]`，首帧即 `opacity:1 / translate:0px / scale:1`；
           · 新写法：anims = `opacity:running|scale:running|translate:running`，逐帧
             `opacity` 0 → .189 → .428 → .676 → .821 → .894 → … → 1（约 12 帧 ≈ 0.2s），
             且 `scale` 过冲到 `1.0039` 再回落 = 契约那条 spring 的回弹。
         ⚠ 只改「开」这一侧。关的一侧仍是摘类 + `[hidden]`（立即 `display:none`）——
           本拍**不引入退场延迟**，免得与 Esc 分层、连点重开这些既有路径抢时序
           （那些路径都把 `[hidden]` 当**唯一状态位**在用）。
         ⚠ 本修法对共用本函数的四枚下拉（`.td-mod-menu` / `.td-rv-scope-menu` /
           `.td-commit-menu` / `.td-rv-opts`）一并生效 —— 它们本来就是**同一条代码路径**、
           共享同一段 CSS 过渡，属于同一个修复面。
         ⚠ 另有两处**同型缺陷但走别的函数**，本拍按「不改不必涉及的模块」**不动**：
           右键菜单 `ctxShow()` 与 `.zd-menu` 的 `placeZdMenu()`（同样是「摘 `[hidden]` +
           挂类」同一 tick）⇒ 它们的入场也仍是硬切。要一并对齐说一声。 */
      menu.removeAttribute('hidden');
      void menu.offsetWidth;
      placeRv(menu, trigger);                         /* r107-k2 */
      menu.classList.add(POP_OPEN);
      if (trigger) trigger.setAttribute('aria-expanded', 'true');
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

  /* ★ r108-l7 ②：这里原有「最大化 / 还原」**整段** —— `freeW()` / `maxPanelW()` /
     `applyMaxW()` / `storedPanelW()` / `setMaxIcon()` / `setMax()`，加上按钮的 click
     监听、分栏条上的 `pointerdown` 捕获监听、以及 `resize` 两条监听。
     邵先生「把 `td-browse-bar` 栏的「最大化侧栏」按钮去掉」—— 按钮是**唯一入口** ⇒
     整段立刻变成不可达代码（`setMax` 首行那句 `if (!maxBtn) return;` 之后再也走不到）。
     ★ 判据支撑：`data-td-maxw` 全仓**只有本文件**读（已 grep 过 `pages/`、各 `part` 目录、
       以及全部 css / js / py），删掉不会有第二个消费者落单。
     ⚠ 宽度记忆（`--av-browse-w` + key `giencoder:r105-browse:v1`）的**拖拽与持久化**
       一直归宿主 `ctrl-conv.js`，本段删掉不影响它。 */

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
        /* ★ 第十二拍 ②：`tree` = 文件树抽屉的开关。抽屉自带开合与视觉反馈 ⇒ 这里放行，
           否则会落到下面那句 `say(ACT_TEXT[kind] || '已执行')` 上弹一个没意义的「已执行」
           （ACT_TEXT 表里没有 tree 这一项）。 */
        if (kind === 'tree') return;
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
    /* ★ r109-l1 ④（邵先生的三张 MasterGo 稿，`file=193158744355579` / `page_id=1119:15374`）：
         稿1 `1409:18319` 初始态 356×48 —— pin 24×24 + 12 缝 + 卡 320×48（占位 + 禁用「添加」）
         稿2 `1204:18467` 输入态 356×108 —— 卡 = 输入区 + 12 缝 + 底行（提示 + 取消 + 添加）
         稿3 `1409:18332` 已批注锚点 24×24 —— 与 pin 同形，实心主色 + 白数字
       结构 = `pin` 与 `card` **两个兄弟**（pin 要能独立切「已批注」实心态），几何全在 panel.css。
       ⚠ 旧版的 `.td-elnote-t`（「评论元素 xx」标题）/ `.td-elnote-f`（26 高、圆角 6、透明底）
         整套退役：稿子里没有标题行，两枚按钮也换成了 DS 组件。 */
    elnote.innerHTML =
      '<span class="td-elnote-pin" aria-hidden="true"></span>'
      + '<div class="td-elnote-card">'
      + '<textarea class="td-elnote-input" rows="1" aria-label="元素评论" placeholder="输入你的注释"></textarea>'
      + '<div class="td-elnote-foot">'
      + '<span class="td-elnote-hint">Enter添加，<em>Ctrl+Enter发送</em></span>'
      + '<span class="td-elnote-acts">'
      + '<button type="button" class="td-elnote-cancel giencoder-btn giencoder-btn-size-small '
      + 'giencoder-btn-secondary" data-td-elnote-cancel="1">取消</button>'
      + '<button type="button" class="td-elnote-ok giencoder-btn giencoder-btn-size-small '
      + 'giencoder-btn-primary" data-td-elnote-ok="1" disabled>添加</button>'
      + '</span></div></div>';
    if (view) view.appendChild(elnote);
    var noteCard = elnote.querySelector('.td-elnote-card');
    var notePin = elnote.querySelector('.td-elnote-pin');
    var noteTa = elnote.querySelector('.td-elnote-input');
    var noteOk = elnote.querySelector('[data-td-elnote-ok]');
    var noteCancel = elnote.querySelector('[data-td-elnote-cancel]');
    var noteList = [];        /* 已批注：`{ el, n, text, anchor }`，n = 下标 + 1 */
    var noteCur = null;       /* 气泡此刻挂在哪个 `[data-td-el]` 上 */
    var noteCtrlOn = false;
    /* ★ r109-l3 ①：**本次批注的唯一原点**。
       邵先生：「添加批注的点击触发点与输入批注的容器 `td-elnote` 没有在一个原点，位置漂移
       太远，需要做到**在哪里点击就在哪里添加**，包括预览批注的也是一样」。
       口径 = `.td-view` 的**内容坐标**（`clientX/Y − view.getBoundingClientRect() + scroll`），
       与锚点内联 `left/top`、与气泡内联 `left/top` **同一套坐标系** ⇒ 三者可以直接加减。
       两个写入点：
         · 点元素发起批注（`.td-view` 的 click 监听）⇒ 写**点击点**；
         · 点已有锚点看详情（`anchorOpen`）      ⇒ 写**锚点自己的位置**（「预览批注的也是一样」）。
       读出点：`noteEdit()`（气泡左边缘）与 `noteDrop()`（锚点中心）。
       ⚠ 缺省 `null` ⇒ 两条老路径都退回 r93 起的读法（被标注元素右上角），只在非点选路径下发生。 */
    var noteAt = null;

    function noteFind(el) {
      for (var i = 0; i < noteList.length; i++) if (noteList[i].el === el) return noteList[i];
      return null;
    }
    /* ★ r109-l2 ④：**反查** —— 从锚点找回它那一条批注。
       （`noteList` 里的 `rec.el` 是单向的：被标注元素 → 批注；点锚点这一头走它。） */
    function noteOfAnchor(a) {
      for (var i = 0; i < noteList.length; i++) if (noteList[i].anchor === a) return noteList[i];
      return null;
    }
    /* 卡高 = 12 + 输入区 + 12 + 底行 28 + 12（空态锁 48）。
       邵先生「按行数算，1 行=86」⇒ 输入区高 = 行数 × 行高；行高从 computed 取，
       `--ui-fs` 换档时自动跟着走。超过 200 的部分由卡片 `max-height` + 输入区自滚兜住
       （卡片是纵列 + 输入区 `min-height:0`，触顶时它才是那个被收缩的件）。 */
    function noteGrow() {
      var has = noteTa.value.replace(/\s+/g, '') !== '';
      noteCard.classList.toggle('has-text', has);
      if (noteOk) noteOk.disabled = !has;
      if (!has) { noteTa.style.height = ''; return; }
      noteTa.style.height = 'auto';
      noteTa.style.height = noteTa.scrollHeight + 'px';
    }
    /* ★ r109-l1 ④：Ctrl 联动 —— 邵先生「按钮 + 提示都变」+「字不变，只高亮后半句」。
       按钮 添加 ⇄ 发送 在这里，提示后半句的高亮交给 `.is-ctrl`（panel.css）。 */
    function noteCtrl(on) {
      noteCtrlOn = on;
      noteCard.classList.toggle('is-ctrl', on);
      /* ★ r109-l3 ①（邵先生：「编辑态时原来的"添加"文案需变为"保存"」）：
         已经是**编辑一条既有批注**（`noteCur` 查得到记录）⇒ 按钮恒为「保存」，
         与 Ctrl 无关 —— Ctrl 那档是「把一条**新**意见发送进对话」的语义，不是「改一条老意见」。
         ★ 文案统一在这**一个函数**里收口：`noteEdit()` 与文档级的 Ctrl keydown / keyup
           都只调它 ⇒ 不存在「编辑态下按一下 Ctrl 就翻回『添加』」的漏洞。
         ⚠ 调用顺序依赖：`noteEdit()` 里是「先 `noteCur = el`、后 `noteCtrl(...)`」，
           所以这里查 `noteCur` 已经是最新的那条。 */
      if (noteOk) {
        noteOk.textContent = (noteCur && noteFind(noteCur)) ? '保存' : (on ? '发送' : '添加');
      }
    }
    function setAnnot(on) {
      brw.classList.toggle('is-annotating', on);
      if (annotBar) { if (on) annotBar.removeAttribute('hidden'); else annotBar.setAttribute('hidden', ''); }
      for (var i = 0; i < annotBtns.length; i++) {
        annotBtns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
        /* ★ r109-l1 ③：工具条那枚「标注」进入批注态后改文案为「退出批注」。
           ⚠ 只认 `.td-url-annot` —— 标注条里那枚「完成」也带 `data-td-annot`，不动它。 */
        if (annotBtns[i].classList.contains('td-url-annot')) {
          var lb = annotBtns[i].querySelector('span');
          if (lb) lb.textContent = on ? '退出批注' : '标注';
        }
      }
      if (!on) { elnote.setAttribute('hidden', ''); noteCur = null; }
    }
    for (var ab = 0; ab < annotBtns.length; ab++) {
      annotBtns[ab].addEventListener('click', function () {
        setAnnot(!brw.classList.contains('is-annotating'));
      });
    }
    /* 打开气泡：该元素**已有**批注 ⇒ pin 直接是稿3 的实心态、输入框回填原文；
       没有 ⇒ 稿1 的初始态（占位 + 禁用「添加」）。
       ★★ 顺序是硬的：**先摘 `[hidden]` 再 `noteGrow()`**。
       真机踩过（本拍第一版）：`noteGrow()` 里用 `ta.scrollHeight` 定高，而气泡此刻还在
       `display: none` 下 ⇒ `scrollHeight` **恒为 0** ⇒ 回填的长文本被压成 0 高，
       重开气泡只剩底行（卡片 48 而不是 86+）。与硬规则「摘 `[hidden]` + 挂开态类必须在
       同一 tick 之外留一次重排」同族 —— 隐藏元素量不出几何。 */
    function noteEdit(el, at) {
      var prev = noteFind(el);
      /* ★ r109-l2 ④：`at` = **定位参照物**，默认 = 被标注元素自己。
         点锚点看详情时传的是**锚点**：气泡落在锚点下方。锚点可以拖到任意位置
         （本层 ⑤），若还按「被标注元素」定位，拖远之后气泡会跟锚点脱开。 */
      var ref = at || el;
      noteCur = el;
      noteTa.value = prev ? prev.text : '';
      notePin.textContent = prev ? String(prev.n) : '';
      notePin.classList.toggle('is-done', !!prev);
      noteCtrl(noteCtrlOn);
      /* ★ r109-l2 ⑤（配套）：锚点可以拖到任意位置（本层 ⑤）⇒ 气泡不能只顾「锚点下方」。
         `.td-elnote` 是 `.td-view`（`overflow: auto`）的**子件** ⇒ 锚点贴到底边时，
         `top = 锚点底缘 + 8` 会把气泡整块推出生效区、被裁得一点不剩
         —— 真机实测（锚点拖到 `.td-view` 右下角后点开）：气泡 `top` 超出可视底 116px、
         `visibleH = -8`、`fullyHidden = true`。需求 ⑤「锚点可任意拖动」是**因**、
         气泡被裁是**果** ⇒ 这条夹取是 ⑤ 的必要配套，不是另开一摊。
         夹取口径：气泡始终留在 `.td-view` 的**可视带** `[scrollTop, scrollTop + clientHeight]` 内。
         ⚠ 先摘 `[hidden]` 再量高：隐藏态 `offsetHeight` 恒为 0 ⇒ 量不出真实高、夹取失效。
           l1 的判据本来就是「先摘 `[hidden]` 再 `noteGrow()`」——顺序不动，只是把定位挪到其后。
         ⚠ 写 `top` 挪到摘 `[hidden]` 之后**不会**引入位移动画：`.td-elnote` 自身没有
           `transition`（真机实测 `transitionDuration: 0s`），只有 pin 的 `background-color`
           与两枚按钮各自有过渡。
         ⚠ 只在「锚点贴近底边」时生效：常规位置真机实测仍是 `气泡顶 = 锚点底 + 8`。 */
      elnote.removeAttribute('hidden');
      noteGrow();
      var er = ref.getBoundingClientRect(), vr = view.getBoundingClientRect();
      var top = er.bottom - vr.top + view.scrollTop + 8;
      var vTop = view.scrollTop, vBot = view.scrollTop + view.clientHeight;
      var h = elnote.offsetHeight;
      if (h && view.clientHeight && top + h > vBot) top = vBot - h;
      if (top < vTop) top = vTop;
      elnote.style.top = Math.round(top) + 'px';
      /* ★ r109-l3 ①：**水平也跟同一原点走**（邵先生：「没有在一个原点，位置漂移太远」）。
         原状：`.td-elnote` 的 `left` 是 CSS 里写死的 `12px`（`left: 12px;`）⇒ 不论锚点在哪、
         点的是哪儿，气泡**永远贴着 `.td-view` 的左边**，与原点能差出几百 px。
         本拍：气泡**左边缘**对齐原点 `noteAt.x`（缺省则退回参照物 `ref` 的左边缘），
         再夹进 `.td-view` 的可视带 —— 与上面 `top` 的夹取同一口径、同一坐标系。
         ⚠ 只加一条内联 `left`（内联优先于 CSS 的 `12px`），CSS 那条保留为**未定位时的初值**；
           气泡的宽度 / radius / 内距 / 三稿几何一字未动。
         ⚠ 宽度在**摘掉 `[hidden]` 之后**量（同 `top` 那条的教训：隐藏态 `offsetWidth` 恒为 0）。 */
      var vLeft = view.scrollLeft, vRight = view.scrollLeft + view.clientWidth;
      var left = noteAt ? noteAt.x : (er.left - vr.left + view.scrollLeft);
      var w = elnote.offsetWidth;
      if (w && view.clientWidth && left + w > vRight) left = vRight - w;
      if (left < vLeft) left = vLeft;
      elnote.style.left = Math.round(left) + 'px';
    }
    /* 锚点（稿3）：初始落在被标注元素的**右上角**（−12 = 让 24×24 的锚点中心咬住那个角）。
       ⚠ 稿子只给了锚点长相、没给落点 ⇒ 取「右上角」这个通行读法（Figma 批注同款），
         若有偏差请邵先生指定。
       ★ r109-l2 ④⑤：锚点从「只读标记」升级成**可交互对象** ——
         · 点它 / 键盘 Enter·Space ⇒ 以**编辑态**打开这条批注的详情（回填原文 + pin 显示
           编号 + 「添加」可用）= `noteEdit(rec.el, a)` 一次调用；
         · 拖它 ⇒ 任意挪位置（pointer 事件 + `window` 上的 move/up，与标签重排同口径）。
       ★ 拖动与点击**共用同一次 pointer 序列** ⇒ 用 4px 阈值分流：超过阈值才算「拖过」，
         松手后那一下 `click` 被 `_tdMoved` 吃掉（否则每拖一次都顺手弹一次气泡）。
       ⚠ 位置夹取用 `.td-view` 的**可视区**（`scrollLeft + clientWidth`）：绝对定位子件是
         跟着内容滚的，不夹的话可以把锚点拖到视野外、再也点不到。
       ⚠ 拖动**不写 `noteList`**：位置就在内联 `left/top` 里，是这个元素唯一的位置真身。 */
    var ANCHOR_MIN = 4;                       /* 拖动阈值：与标签重排的 5px 同量级 */
    /* 把 (left, top) 夹进 `.td-view` 的可视区，并直接落到 `a.style` 上。
       ⚠ 隐藏态（模块没被激活 ⇒ `clientWidth === 0`）量不出可视区 ⇒ 原样落位、不要夹
         （`noteDrop` 只在用户与浏览器模块交互时才跑，正常不会命中这一支，留作防御）。 */
    function anchorPlace(a, left, top) {
      if (!view.clientWidth || !view.clientHeight) {
        a.style.left = Math.round(left) + 'px'; a.style.top = Math.round(top) + 'px'; return;
      }
      var w = a.offsetWidth || 0, h = a.offsetHeight || 0;
      var minL = view.scrollLeft, minT = view.scrollTop;
      var maxL = minL + view.clientWidth - w, maxT = minT + view.clientHeight - h;
      if (maxL < minL) maxL = minL;
      if (maxT < minT) maxT = minT;
      a.style.left = Math.round(Math.min(Math.max(left, minL), maxL)) + 'px';
      a.style.top = Math.round(Math.min(Math.max(top, minT), maxT)) + 'px';
    }
    /* 打开某个锚点对应的批注详情（编辑态）。反查不到就什么都不做 —— 锚点永远是
       `noteCommit()` 里 `push` 之后才落盘的，理论上必能反查到。 */
    function anchorOpen(a) {
      var rec = noteOfAnchor(a);
      if (!rec) return;
      /* ★ r109-l3 ①：**「预览批注的也是一样」** —— 点锚点看详情时，原点就是**锚点自己**。
         既有的 r109-l2 ④ 已经把「定位参照物」传成锚点（气泡落在锚点**下方**），
         但水平那一路当时还是 CSS 的 `left: 12px` ⇒ 锚点拖到右侧时，气泡仍在左边弹出来。
         这里把 `noteAt` 覆盖成锚点位置 ⇒ 与「点元素发起批注」共用**同一条定位路径**
         （`noteEdit()` 里那两个夹取完全一致），不再分叉。 */
      var ar = a.getBoundingClientRect(), vr = view.getBoundingClientRect();
      noteAt = { x: ar.left - vr.left + view.scrollLeft,
                 y: ar.top - vr.top + view.scrollTop };
      noteEdit(rec.el, a);
    }
    function bindAnchor(a) {
      a.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return;
        e.preventDefault();                 /* 别把光标下的文字拖成选区 */
        e.stopPropagation();                /* 免得透过 `.td-view` 冒到标注态那层点击 */
        a._tdMoved = false;
        var sx = e.clientX, sy = e.clientY;
        var sl = parseFloat(a.style.left) || 0, st = parseFloat(a.style.top) || 0;
        function onMove(ev) {
          var dx = ev.clientX - sx, dy = ev.clientY - sy;
          if (!a._tdMoved) {
            if (Math.abs(dx) < ANCHOR_MIN && Math.abs(dy) < ANCHOR_MIN) return;
            a._tdMoved = true;
            a.classList.add('is-dragging');
          }
          anchorPlace(a, sl + dx, st + dy);
          ev.preventDefault();
        }
        /* 一次性拆净四支：`pointerup` 正常收尾；`pointercancel` / `blur` 兜「手势被系统
           抢走」与「切走窗口」两种断线（站内其它拖拽同口径）。 */
        function onEnd() {
          window.removeEventListener('pointermove', onMove, true);
          window.removeEventListener('pointerup', onEnd, true);
          window.removeEventListener('pointercancel', onEnd, true);
          window.removeEventListener('blur', onEnd, true);
          a.classList.remove('is-dragging');
        }
        window.addEventListener('pointermove', onMove, true);
        window.addEventListener('pointerup', onEnd, true);
        window.addEventListener('pointercancel', onEnd, true);
        window.addEventListener('blur', onEnd, true);
      });
      a.addEventListener('click', function (e) {
        e.stopPropagation();
        /* 刚拖过 ⇒ 这一下 `click` 是拖动的尾巴、不是「点开」。消费掉标记后返回。 */
        if (a._tdMoved) { a._tdMoved = false; return; }
        anchorOpen(a);
      });
      /* 键盘可达：给了 `role="button"` 就必须配 Enter / Space，否则读屏用户点不开。 */
      a.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); anchorOpen(a); }
      });
    }
    function noteDrop(el, n, at) {
      var a = document.createElement('span');
      a.className = 'td-anchor';
      a.textContent = String(n);
      /* ★ r109-l2 ④：锚点**不再是纯装饰** ⇒ 摘掉 r109-l1 挂的 `aria-hidden="true"`
         （那时它确实只是个标记，挂 aria-hidden 是对的），换成真正的按钮语义。 */
      a.setAttribute('role', 'button');
      a.setAttribute('tabindex', '0');
      a.setAttribute('aria-label', '查看第 ' + n + ' 条批注');
      a.title = '点击查看批注 · 拖动可挪位置';
      view.appendChild(a);                  /* 先入 DOM —— `anchorPlace` 要量它的几何 */
      /* ★ r109-l3 ①：**锚点落在「本次点击点」**（`at` = 内容坐标，见 `noteAt`）。
         锚点 24×24 ⇒ `−12` = 让它的**中心**咬住那个点（「在哪里点击就在哪里添加」）。
         ⚠ 旧读法（r93 起）= 被标注元素的**右上角 −12**：它假设「用户点的是元素右上角」，
           点长段落左端时锚点就飘到了段落右端 —— 正是邵先生说的「位置漂移太远」。
         ⚠ `at` 缺省 ⇒ 退回旧读法，只在「非点选路径」下发生（防御，正常不会命中）。
         ⚠ `anchorPlace` 的夹取照旧：拖/落到 `.td-view` 可视区边界会被夹住。 */
      if (at) {
        anchorPlace(a, at.x - 12, at.y - 12);
      } else {
        var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
        anchorPlace(a, er.right - vr.left + view.scrollLeft - 12,
                    er.top - vr.top + view.scrollTop - 12);
      }
      bindAnchor(a);
      return a;
    }
    function noteCommit() {
      if (!noteCur) return;
      var text = noteTa.value.replace(/\s+/g, '');
      if (!text) return;
      var rec = noteFind(noteCur);
      if (rec) { rec.text = text; }
      else {
        rec = { el: noteCur, n: noteList.length + 1, text: text, anchor: null };
        rec.anchor = noteDrop(noteCur, rec.n, noteAt);
        noteList.push(rec);
      }
      elnote.setAttribute('hidden', '');
      noteCur = null;
      /* ★ r109-l3 ①：原点用完即弃 —— 下一次批注一定由「新的点击」或「新的锚点」重写它，
         不清就会让「先点 A 处提交、再键盘触发一次编辑」这类路径误用上一处坐标。 */
      noteAt = null;
      /* ★ r109-l1 ④：**不再** `setAnnot(false)`。稿3 的存在说明「加完一条留在批注模式」
         才是原意 —— 加完就退出的话，锚点根本来不及被看到。锚点常驻：它跟 Figma 批注
         一样是「页面上已经存在的意见」，不随批注模式开合。 */
      say('评论已带入对话（视觉演示）');
    }
    if (view) {
      view.addEventListener('click', function (e) {
        if (!brw.classList.contains('is-annotating')) return;
        var el = e.target && e.target.closest ? e.target.closest('[data-td-el]') : null;
        if (!el) return;
        /* ★ r109-l3 ①：**记下点击点**（转成 `.td-view` 的内容坐标）—— 它就是本条批注的原点。
           ⚠ `e.clientX/Y` 是**视口坐标**，锚点与气泡用的是**内容坐标** ⇒ 必须 `− viewRect + scroll`。
           ⚠ 键盘 Enter 触发的合成 `click` 两个坐标都是 0 ⇒ 认作「没有点击点」，退回旧读法
             （否则锚点会被扔到 `.td-view` 的左上角）。 */
        if (e.clientX || e.clientY) {
          var vr0 = view.getBoundingClientRect();
          noteAt = { x: e.clientX - vr0.left + view.scrollLeft,
                     y: e.clientY - vr0.top + view.scrollTop };
        } else {
          noteAt = null;
        }
        noteEdit(el);
      });
    }
    /* ⚠ 气泡挂在 `.td-view` 里 ⇒ 它自己的点击会冒到上面那条 view 监听上，
       点「取消」会顺手把气泡重新打开。断在气泡这一层。 */
    elnote.addEventListener('click', function (e) { e.stopPropagation(); });
    noteTa.addEventListener('input', noteGrow);
    /* 稿2 的提示写的是「Enter添加，Ctrl+Enter发送」⇒ 两种回车都落到同一枚提交上
       （本页是静态演示，两者的差别只在文案）。顺手拦掉换行，免得输入框里长出一行。 */
    noteTa.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); noteCommit(); }
    });
    if (noteCancel) noteCancel.addEventListener('click', function () {
      elnote.setAttribute('hidden', ''); noteCur = null;
    });
    if (noteOk) noteOk.addEventListener('click', noteCommit);
    /* ★ r109-l1 ④：Ctrl 按住 / 松开。挂在 `document` 上 —— 邵先生的演示说的是「按下
       ctrl 键」即可，不该限定焦点在输入框里。`blur` 兜底（切走窗口时归位，免得卡在
       「发送」态）。 */
    document.addEventListener('keydown', function (e) { if (e.key === 'Control') noteCtrl(true); });
    document.addEventListener('keyup', function (e) { if (e.key === 'Control') noteCtrl(false); });
    window.addEventListener('blur', function () { noteCtrl(false); });
    var BRW_TEXT = {
      more: '更多浏览器选项（视觉演示）'
    };
    /* ★ r108-l6 ②：这里原有 `send` / `shot` / `zoom` 三条 —— 对应的三枚工具条图标按钮
       已按邵先生「不需要，请去掉」整块移除 ⇒ 它们、以及为 `shot` 服务的 `shotFlash()`
       快门（连同 CSS 18-②）一并删掉，不留死代码。右端的「更多」保留。
       ⚠ 右键菜单里那条「截图到剪贴板」（`ctxForBrw`）是**另一处**功能，不是「工具条图标
         按钮」⇒ 按「不得改动不必涉及的模块」保留；但它原来靠 `sb.click()` 借工具条按钮的
         力 ⇒ 那里改成直接给轻提示（免留指向已删元素的死引用）。 */
    var brwActs = pane.querySelectorAll('[data-td-brw-act]');
    for (var ba = 0; ba < brwActs.length; ba++) {
      (function (b) {
        b.addEventListener('click', function () {
          say(BRW_TEXT[b.getAttribute('data-td-brw-act')] || '已执行');
        });
      })(brwActs[ba]);
    }
  }

  /* ==================== 摘要模块 ==================== */
  var sumActs = pane.querySelectorAll('[data-td-sum-act]');
  for (var sa = 0; sa < sumActs.length; sa++) {
    sumActs[sa].addEventListener('click', function () { say('已复制会话摘要'); });
  }
  /* ★ 第十六拍 ①：产物预览从「覆盖整块摘要的浮层」改为**右栏自己的一个页签**。
     上一版是 `.td-sum-prev`（`position: absolute; inset: 0` 盖住 `.td-mod.td-sum`）——
     那种载体自带一套开关，跟标签栏状态机各说各话：切到别的模块、或把摘要页签关掉，
     它还在原地（而 `.td-mod.td-sum { position: relative }` 只为它一个人存在）。
     这一版把预览做成 `#av-browse-pane-preview`（`data-td-pane="preview"`）：
     开关 / 切换 / 关闭 / 拖拽重排全部由标签栏那一套（`openTab` / `activate` /
     `closeTab`）裁决。两套骨架（md / xlsx）与文案填充逻辑**一字未改**，只换了宿主。
     ⚠ 「同一枚预览页签复用」：连点两个产物不会开出两枚标签，第二个只更新页签名与
       正文（`openTab` 命中同名 `mod` 时走 `activate` 分支，与「文件 / 审查 …」同口径）。 */
  var prevPane = pane.querySelector('#av-browse-pane-preview');
  function prevShow(btn) {
    if (!prevPane) return;
    var host = btn && btn.closest ? btn.closest('.td-sum-art') : null;
    var nmEl = host && host.querySelector('.td-sum-artt b');
    var mtEl = host && host.querySelector('.td-sum-artt i');
    var ico = host && host.querySelector('.td-sum-arti svg');
    var name = nmEl ? nmEl.textContent : '产物';
    var kind = (/\.(xlsx|xls|csv|tsv)$/i).test(name) ? 'xlsx' : 'md';
    var pn = prevPane.querySelector('[data-td-prev-name]');
    var pm = prevPane.querySelector('[data-td-prev-meta]');
    var pi = prevPane.querySelector('[data-td-prev-ico]');
    if (pn) pn.textContent = name;
    if (pm) pm.textContent = (mtEl ? mtEl.textContent : '') + ' · 只读预览';
    if (pi && ico) pi.innerHTML = ico.outerHTML;
    var bodies = prevPane.querySelectorAll('[data-td-prev-kind]');
    for (var q = 0; q < bodies.length; q++) {
      if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');
      else bodies[q].setAttribute('hidden', '');
    }
    /* ⚠ 顺序：**先把内容填好再 `openTab`** —— 后者会 `activate()` 让面板显形，
       反过来的话会闪一帧「旧文件名 / 旧骨架」。 */
    openTab('preview', { name: name, ico: ico ? ico.outerHTML : '' });
  }
  var artBtns = pane.querySelectorAll('[data-td-art]');
  for (var ar = 0; ar < artBtns.length; ar++) {
    (function (b) {
      b.addEventListener('click', function () { prevShow(b); });
    })(artBtns[ar]);
  }
  /* 面板工具条上的两枚动作 —— 关闭改由页签自己的 `×`（`closeTab` 那段现有逻辑）。
     ★ r108-l7 ①（邵先生：把「在系统打开」拆成两个按钮）：原一枚语义过载 —— 分不清是
       「另存一份」还是「在文件管理器里定位」⇒ 拆成「另存为」与「打开所在文件夹」两枚。
       ⚠ 仍是**纯静态演示**（各给一句轻提示），不引入任何真实文件系统调用。 */
  if (prevPane) {
    var prevSaveBtn = prevPane.querySelector('[data-td-prev-save]');
    if (prevSaveBtn) prevSaveBtn.addEventListener('click', function () { say('已另存为到本地（视觉演示）'); });
    var prevRevealBtn = prevPane.querySelector('[data-td-prev-reveal]');
    if (prevRevealBtn) prevRevealBtn.addEventListener('click', function () { say('已在文件管理器中定位该文件（视觉演示）'); });
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
      /* r108-l6 ②：工具条那枚相机按钮已删 ⇒ 不再借它的力（原 `sb.click()` 会指向空元素）。 */
      say('已复制截图到剪贴板（视觉演示）');
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
     ★ 选区范围（★ r108-l8 ① 扩容）：`.r93-scroll`（主对话口）**∪** `.td-browse`
       （整个右栏 —— 摘要 / 审查 diff 代码 / 终端 / 浏览器 / 文件树与代码区 / 预览）。
       顶栏与左侧导航 aside 仍不在范围内。 */
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
    /* ★ r108-l8 ①（邵先生：「整个右栏 `td-browse` 所有的文本（含代码）被鼠标框选后，
       都要在上方显示浮动工具条（添加到对话、复制）」）：
       原判据只放行主对话口 `.r93-scroll` ⇒ 右栏里划词**浮条根本不弹**。
       真机实测（1440×900，真实鼠标拖选，非合成事件）：审查 diff 的代码行能选中
       （`Selection.toString()` 拿到 `'   <aside class="td-browse" …>\n89\n− …'` 这类多行内容）、
       摘要那行小字也能选中，但 `.td-selbar` **从未被创建**（`selbarExists = false`）。
       ⇒ 放行根扩成「`.r93-scroll` ∪ `.td-browse`」，覆盖右栏全部模块
         （摘要 / 审查 diff 代码 / 终端 / 浏览器 / 文件树与代码区 / 预览）。
       ⚠ 两者是**并列的 flex 兄弟**、互不包含（1440 实测：`.r93-scroll` [13,49,778,604] 与
         `.td-browse` [791,48,641,844]）⇒ 不会互相误判；主对话口原有划词能力一字未动。
       ⚠ 页签名（`.td-browse-tab`）与文件树行名（`.td-bf`）本来就带 `user-select: none`
         （它们是「控件」不是「内容」）⇒ 那两处仍拖不出选区，属既有口径、本拍不动。 */
    var selHost = (e.target && e.target.closest)
      ? e.target.closest('.r93-scroll, .td-browse') : null;
    if (!selHost) { selHide(); return; }
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
    /* ★ 第十六拍 ①：产物预览**不再占一层** —— 它已经是右栏的一个页签（`data-td-pane`），
       与「审查 / 终端 / 浏览器 / 摘要」同级，Esc 一律落到 ctrl-conv 那条（关整条侧栏）。
       ⚠ 上一版这里是 `var prevOpen = prevEl && ...`：浮层删掉后 `prevEl` 就成了解析不到
         的标识符 ⇒ 按一次 Esc 直接抛 `ReferenceError`（本层跨层自检逮到）。 */
    /* ★ 第十二拍 ②：文件树抽屉也占一层 —— 顺序与 z-index 同序
       （提交模态 40 → 抽屉 35 → 菜单 30）。不接进来的话，开着抽屉按 Esc 会直接
       落到 ctrl-conv 的 Esc 上**把整条侧栏关掉**。 */
    var treeOpen = treeEl && !treeEl.hasAttribute('hidden');
    if (!modal && !menuOpen && !noteOpen && !selOpen && !treeOpen) return;
    e.preventDefault();
    e.stopPropagation();
    if (selOpen) { selHide(); return; }
    if (modal) { commitModal.setAttribute('hidden', ''); return; }
    if (treeOpen) { treeHide(); return; }
    if (menuOpen) { closeMenus(null); return; }
    if (noteOpen) { elnote.setAttribute('hidden', ''); return; }
    /* ★ 第十六拍 ①：原 `if (prevOpen) prevHide();` 已随浮层一并删掉 —— 预览成了页签，
       这一层不再有它的活儿；继续往下走 = ctrl-conv 关整条侧栏，正是模块页签该有的行为。 */
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

  /* ==================== 文件树抽屉（第十二拍 ②） ====================
     对照 Codex「文件」入口补的一件：审查工具条里「在文件树中定位」**右侧**那枚按钮，
     点开 = 从右栏右缘滑入一层文件树抽屉，**不打断当前正在看的模块**（不必切到「文件」标签）。
     ★★ 树行用**独立类名 `td-tf`**（不是 `td-bf`）：ctrl-conv.js 的
        `pane.querySelectorAll('.td-bf')` 作用域是整个 `.td-browse`，复用同名类会把抽屉里的
        行一并接管（refresh / selectFile 互相打架；且它那个 `files` 变量只绑**第一个**
        `.td-browse-files` ⇒ 抽屉里的行点了没反应）。这里重写一套同语义的展开/折叠 + 选中。
     ⚠ 「点那枚按钮」必须 stopPropagation：否则会冒到下面 document 那条 closeMenus 上，
        把刚开的抽屉当「点了别处」立刻关掉。
     ⚠ 开 / 关都走 `hidden` + `is-open` 两条（CSS 那边的过渡需要「先摘 hidden 再挂类」的
        两帧节奏）⇒ 这里显式 `void offsetWidth` 强制一次 reflow 当分帧。 */
  var treeEl = pane.querySelector('[data-td-tree]');
  var treeFiles = treeEl ? treeEl.querySelector('.td-tree-files') : null;
  var treeBtn = pane.querySelector('[data-td-rv-act="tree"]');

  /* 展开 / 折叠：只认「祖先链上有没有 closed 的目录」（与 ctrl-conv 的 refresh() 同口径），
     作用域锁在抽屉自己这棵树里。 */
  function treeRefresh() {
    if (!treeFiles) return;
    var rows = treeFiles.querySelectorAll('.td-tf'), i;
    for (i = 0; i < rows.length; i++) {
      var p = rows[i].dataset.parent || '', ok = true;
      while (p) {
        var pr = treeFiles.querySelector('.td-tf[data-node="' + p + '"]');
        if (!pr || pr.classList.contains('is-closed')) { ok = false; break; }
        p = pr.dataset.parent || '';
      }
      rows[i].classList.toggle('is-hidden', !ok);
    }
  }

  function treeShow() {
    if (!treeEl || !treeEl.hasAttribute('hidden')) return;
    treeEl.removeAttribute('hidden');
    void treeEl.offsetWidth;                       /* 强制 reflow ⇒ 让下一行成为「下一帧」 */
    treeEl.classList.add('is-open');
    if (treeBtn) treeBtn.setAttribute('aria-expanded', 'true');
    treeRefresh();
  }

  function treeHide() {
    if (!treeEl || treeEl.hasAttribute('hidden')) return;
    treeEl.classList.remove('is-open');
    if (treeBtn) treeBtn.setAttribute('aria-expanded', 'false');
    /* 等过渡播完（220ms）再摘 `hidden` —— 否则关闭动作是「瞬间消失」，看不出抽屉在滑出；
       期间若又被打开（`is-open` 回到身上），这一下就不摘。 */
    setTimeout(function () {
      if (!treeEl.classList.contains('is-open')) treeEl.setAttribute('hidden', '');
    }, 240);
  }

  if (treeEl) {
    if (treeBtn) {
      treeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (treeEl.hasAttribute('hidden')) treeShow(); else treeHide();
      });
    }
    var treeXs = treeEl.querySelectorAll('[data-td-tree-x]');
    for (var tx = 0; tx < treeXs.length; tx++) {
      treeXs[tx].addEventListener('click', function (e) { e.stopPropagation(); treeHide(); });
    }
    if (treeFiles) {
      treeFiles.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.td-tf') : null;
        if (!row) return;
        if (row.classList.contains('is-dir')) {
          var closed = row.classList.toggle('is-closed');
          row.setAttribute('aria-expanded', closed ? 'false' : 'true');
          treeRefresh();
        } else {
          var old = treeFiles.querySelector('.td-tf.is-active');
          if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
          row.classList.add('is-active');
          row.setAttribute('aria-selected', 'true');
        }
      });
      treeRefresh();
    }
    /* 点右栏里别处 = 收抽屉（与右栏四枚下拉共用「点空白收起」的口径）。
       ⚠ 判据用 `.td-tree`（抽屉整层）而不是 `.td-tree-panel`：点遮罩时由 scrim 自己的
         处理器关，这里放行即可。 */
    document.addEventListener('click', function (e) {
      if (treeEl.hasAttribute('hidden')) return;
      if (e.target && e.target.closest && e.target.closest('.td-tree')) return;
      treeHide();
    });
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

/* ==================== 任务信息面板（第十三拍 ⑥） ==================== */
/* 复刻 ZCode 右上角状态面板的**交互骨架**：① 每个分区标题可折/展；② 头部「收起为胶囊」；
   ③ 点胶囊摊回面板。面板本体是 `_mods.html` 里的静态 DOM（`#av-zd-status`），初始挂在右栏
   `<aside class="td-browse">` 内（跟随静态注入的体位）—— 这里把它**整体搬进 `<main>`**，
   这样 `absolute top-0 right-16 pt-16` 量到的才是「对话界面右上角」（上游同款体位）。 */
(function () {
  var host = document.getElementById('av-zd-status');
  if (!host) return;
  if (host.getAttribute('data-zd-ready') === '1') return;   /* 幂等：同一份 DOM 只初始化一次 */
  host.setAttribute('data-zd-ready', '1');

  function place() {
    var main = document.querySelector('main');
    if (!main) return false;
    if (host.parentNode !== main) main.appendChild(host);
    return true;
  }
  /* React 首帧可能还没渲染出 <main> ⇒ 等一次 DOM 变化再挂（与右栏补挂同一范式）。 */
  if (!place()) {
    var mo = new MutationObserver(function () { if (place()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
    window.setTimeout(function () { place(); mo.disconnect(); }, 4000);
  }

  var card = host.querySelector('[data-zd-card]');
  var mini = host.querySelector('[data-zd-mini]');

  /* ① 分区折/展：只切 `.is-closed`（可见性由 CSS 裁决，JS 不写内联 display） */
  var secs = host.querySelectorAll('[data-zd-sec]');
  for (var i = 0; i < secs.length; i++) {
    (function (sec) {
      var t = sec.querySelector('.zd-sec-t');
      if (!t) return;
      t.addEventListener('click', function () {
        var closed = sec.classList.toggle('is-closed');
        t.setAttribute('aria-expanded', closed ? 'false' : 'true');
      });
    })(secs[i]);
  }

  /* ==================== 第十四拍 ① Git 工具三行：接上交互 ====================
     上游（`packages/ui/src/v4/ConversationStatusPanel.tsx` 的 `GitStatusSection`）：
       · `changes` 行  → `onOpenGitReview()`                       = 打开 git 审查
       · `branch` 行   → `<GitBranchSwitcher>`                      = 分支下拉
       · `commitPush` 行 → `<GitActionMenu triggerLayout="status-row">` = 提交 / 推送
     本页落地（全部是静态交互）：
       · 更改           复用右栏自己的「打开模块」链路（建 / 激活「审查」标签 + 自动展开侧栏）
       · 分支 / 提交     就地弹 DS Dropdown（`_mods.html` 里那两枚 `.zd-menu`）
     ⚠ 菜单必须在**触发行的 click 里 `stopPropagation`**：本 IIFE 末尾那条 document click
       负责「点空白一律收起」，不挡住的话菜单会在同一次点击里被自己关掉。 */
  var gitReview = card ? card.querySelector('[data-zd-git="review"]') : null;
  var gitBranch = card ? card.querySelector('[data-zd-git="branch"]') : null;
  var gitCommit = card ? card.querySelector('[data-zd-git="commit"]') : null;
  var branchVal = card ? card.querySelector('[data-zd-branch]') : null;

  /* 轻提示（动作类反馈；1.4s 自动收，与右栏 `.td-toast` 同口径） */
  var ztoast = host.querySelector('.zd-toast');
  var ztimer = 0;
  function zsay(text) {
    if (!ztoast) return;
    ztoast.textContent = text;
    ztoast.removeAttribute('hidden');
    if (ztimer) clearTimeout(ztimer);
    ztimer = setTimeout(function () { ztoast.setAttribute('hidden', ''); }, 1400);
  }

  var POP_OPEN = 'giencoder-popup-open';
  var menuBranch = host.querySelector('.zd-menu-branch');
  var menuCommit = host.querySelector('.zd-menu-commit');
  var zdMenus = [];
  if (menuBranch) zdMenus.push(menuBranch);
  if (menuCommit) zdMenus.push(menuCommit);

  function zdMenuShow(m) {
    for (var i = 0; i < zdMenus.length; i++) if (!zdMenus[i].hasAttribute('hidden')) return true;
    return false;
  }
  function closeZdMenus(except) {
    for (var i = 0; i < zdMenus.length; i++) {
      var m = zdMenus[i];
      if (m === except) continue;
      m.setAttribute('hidden', '');
      m.classList.remove(POP_OPEN);
    }
    if (gitBranch) gitBranch.setAttribute('aria-expanded', menuBranch === except ? 'true' : 'false');
    if (gitCommit) gitCommit.setAttribute('aria-expanded', menuCommit === except ? 'true' : 'false');
  }
  /* 摆放：垂直 = 触发行下缘 + 6px（与右栏 `placeRv()` 同口径）；水平 = 右对齐卡片右缘。
     ⚠ 必须在 `[hidden]` 摘掉**之后**调用（否则量到 0×0）；
       量宽高用 `offsetWidth` —— 不受入场 `scale(0.96)` 影响（`getBoundingClientRect()` 会乘进去）。 */
  var ZD_GAP = 6;
  function placeZdMenu(menu, trigger) {
    var hr = host.getBoundingClientRect();
    var tr = trigger.getBoundingClientRect();
    var top = tr.bottom - hr.top + ZD_GAP;
    var left = host.clientWidth - menu.offsetWidth;      /* 右对齐卡片右缘 */
    if (left < 0) left = 0;                              /* 菜单比卡片宽 ⇒ 贴左缘 */
    menu.style.top = Math.round(top) + 'px';
    menu.style.left = Math.round(left) + 'px';
    menu.style.right = 'auto';
  }
  function toggleZdMenu(menu, trigger) {
    if (!menu) return;
    var willOpen = menu.hasAttribute('hidden');
    closeZdMenus(willOpen ? menu : null);
    if (willOpen) {
      menu.removeAttribute('hidden');
      menu.classList.add(POP_OPEN);
      placeZdMenu(menu, trigger);
    } else {
      menu.setAttribute('hidden', '');
      menu.classList.remove(POP_OPEN);
    }
  }

  /* · 更改 → 复用右栏那条链路：`[data-td-open-mod="review"]` 的 click 会建 / 激活标签，
     并且内部 `ensureOpen()` 会在侧栏收起时点一下「打开侧栏」。**不自己写一套 openTab**，
     免得与右栏的标签状态机各说各话。兜底：连模块项都没了就只开侧栏。 */
  if (gitReview) gitReview.addEventListener('click', function (e) {
    e.stopPropagation();
    closeZdMenus(null);
    var op = document.querySelector('[data-td-open-mod="review"]');
    if (op) { op.click(); return; }
    var toggle = document.querySelector('.r93-baract[data-r93-browse]');
    if (toggle) toggle.click();
  });
  if (gitBranch) gitBranch.addEventListener('click', function (e) {
    e.stopPropagation();
    toggleZdMenu(menuBranch, gitBranch);
  });
  if (gitCommit) gitCommit.addEventListener('click', function (e) {
    e.stopPropagation();
    toggleZdMenu(menuCommit, gitCommit);
  });

  /* 分支项：选中即换行内显示（radio 型 ⇒ 勾 + 主色文字，见 panel.css 第 1 节） */
  var brItems = host.querySelectorAll('[data-zd-br]');
  for (var bi = 0; bi < brItems.length; bi++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        for (var k = 0; k < brItems.length; k++) {
          var on = brItems[k] === b;
          brItems[k].classList.toggle('is-checked', on);
          brItems[k].setAttribute('aria-checked', on ? 'true' : 'false');
        }
        var name = b.getAttribute('data-zd-br');
        if (branchVal) branchVal.textContent = name;
        closeZdMenus(null);
        zsay('已切换到 ' + name + '（视觉演示）');
      });
    })(brItems[bi]);
  }
  var brNew = host.querySelector('[data-zd-br-new]');
  if (brNew) brNew.addEventListener('click', function (e) {
    e.stopPropagation();
    closeZdMenus(null);
    zsay('已打开创建分支（视觉演示）');
  });
  /* 提交菜单：文案对齐本页既有 `.td-commit-menu`（右栏那份是同一个上游组件的落地） */
  var cmItems = host.querySelectorAll('[data-zd-commit]');
  for (var ci = 0; ci < cmItems.length; ci++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        var push = b.getAttribute('data-zd-commit') === 'push';
        closeZdMenus(null);
        zsay(push ? '已提交并推送到 origin/main（视觉演示）' : '已提交到本地（视觉演示）');
      });
    })(cmItems[ci]);
  }
  /* 点空白一律收起（菜单内部不关） */
  document.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('.zd-menu')) return;
    closeZdMenus(null);
  });
  /* ★ Esc：挂 `window` **捕获段**（比任何 `document` 捕获段都早），且**只有真的消费掉了
     这一下才 `stopPropagation`** —— 否则「关菜单」会静默漏给下游，把整条侧栏 / 面板一起关掉
     （右栏 r107 那条 Esc 处理器踩过同型的坑，见 panel.js 第 1272 行那段注释）。 */
  window.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!zdMenuShow()) return;
    e.preventDefault();
    e.stopPropagation();
    closeZdMenus(null);
  }, true);

  /* ==================== 第十四拍 ④ 面板 ⇄ 胶囊（带弹性微动效） ====================
     上一版是「点一下立刻 hidden ⇒ 硬切」。这一版：先给离场件挂 `.is-zd-out`
     （CSS 里是 170ms 淡出 + 微缩），到点再 `hidden` 并给入场件挂 `.is-zd-in`
     （CSS 里是 spring 回弹的关键帧）。计时器都存起来 ⇒ 连点不会留下半截状态。 */
  var zdOutTimer = 0, zdInTimer = 0;
  function zdSwap(from, to) {
    if (!from || !to) return;
    if (zdOutTimer) clearTimeout(zdOutTimer);
    if (zdInTimer) clearTimeout(zdInTimer);
    from.classList.add('is-zd-out');
    zdOutTimer = setTimeout(function () {
      from.setAttribute('hidden', '');
      from.classList.remove('is-zd-out');
      to.removeAttribute('hidden');
      to.classList.add('is-zd-in');
      zdInTimer = setTimeout(function () { to.classList.remove('is-zd-in'); }, 380);
    }, 180);
  }
  function toMini() { closeZdMenus(null); zdSwap(card, mini); }
  function toCard() { zdSwap(mini, card); }
  var minBtn = card ? card.querySelector('[data-zd-min]') : null;
  if (minBtn) minBtn.addEventListener('click', toMini);
  if (mini) mini.addEventListener('click', toCard);

  /* ==================== r109-l2 ① 右栏展开 ⇒ 自动折叠为胶囊 ====================
     邵先生：「当右栏展开时，"zd-host"容器会自动折叠为迷你按钮状态」。
     ▸ 信号源 = **`.av-browse-on`**：由宿主 `ctrl-conv.js` 的 `setOpen()` 唯一写入，打在
       **外壳 flex 行**上（`div:has(> main)` = `#av-browse-slot` 的父级）。宿主自己就拿它
       当判据（`browseOpen()` / `if (browseOpen())`）⇒ 这是该状态的**唯一真身**，
       不是又造一个。
     ▸ 为什么不盯「右栏标签切换（`openTab` / `activate`）」：切标签时右栏**本来就是展开的**，
       需求是「展开**时**折叠」而不是「每切一次标签折一次」—— 盯标签会在用户手动摊回
       卡片之后，一换标签又给折回去。
     ▸ 为什么不 hook 那枚开关按钮的 click：收起右栏有**三条**路径（开关按钮 / Esc /
       面板自带的 `[data-td-browse-close]`），且 `ensureOpen()` 还会合成 `b.click()`
       ⇒ hook click 必漏。观察状态类才是收敛点。
     ▸ **反向不自动摊回卡片**：邵先生只说了「展开时折叠」。收起右栏不该替用户改变他
       手动选定的形态（他可能就是一直要看胶囊）。
     ▸ 时序直接复用既有 `toMini()`（`zdSwap` 的 180ms 离场 + 260ms 入场关键帧），不另写
       一套；`toMini()` 自带 `closeZdMenus(null)`，顺带把可能开着的 zd 下拉收掉。
     ⚠ `#av-browse-slot` 挂进外壳 flex 行是宿主 `place()` **异步**做的（React 首帧晚于
       本脚本）⇒ 用一个 `childList` 观察器兜到「行出现 / 被 React 重挂」那一刻；回调里
       只做「读 parentElement + 比身份」，命中即早退，开销可忽略（宿主自己也挂着同型的
       常驻 `moKeep`）。 */
  var browseSlot = document.getElementById('av-browse-slot');
  var zdRowEl = null, zdRowOn = null, zdRowMo = null;
  function zdRowCheck() {
    if (!zdRowEl) return;
    var on = zdRowEl.classList.contains('av-browse-on');
    if (on === zdRowOn) return;
    zdRowOn = on;
    if (on) toMini();                       /* 只在「开」这一侧动手 */
  }
  function zdRowSync() {
    var row = browseSlot ? browseSlot.parentElement : null;
    if (!row) return;
    if (row !== zdRowEl) {                  /* 首次挂上 / React 重挂 ⇒ 换观察对象 */
      if (zdRowMo) zdRowMo.disconnect();
      zdRowEl = row;
      /* 挂载这一刻就把状态记下来：**首帧已是展开态 ⇒ 直接折叠**；
         若记成 null，下一次无关的 class 变更会被误判成「刚打开」。 */
      zdRowOn = row.classList.contains('av-browse-on');
      zdRowMo = new MutationObserver(zdRowCheck);
      zdRowMo.observe(row, { attributes: true, attributeFilter: ['class'] });
      if (zdRowOn) toMini();
      return;
    }
    zdRowCheck();
  }
  if (browseSlot) {
    zdRowSync();
    var zdRowMo0 = new MutationObserver(zdRowSync);
    zdRowMo0.observe(document.body, { childList: true, subtree: true });
  }
})();
