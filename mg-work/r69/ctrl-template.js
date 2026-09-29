/* ================================================================================
   ★ 第 69 轮：文件预览栏（.td-browse）—— 从「研发工作台 › 任务详情页」全要素移植
   三件套：① 同源 HTML（#av-browse-slot，含顶栏 / 文件目录树 / 代码预览 / 两条分栏条）
           ② 同源 CSS（#av-browse-css）
           ③ 同源 JS：右键菜单 bindBrowseContextMenu（逐字移植）+ 本控制器（按本页布局改写）
   与详情页的布局差异（决定了控制器为何要重写，而非照搬）：
     · 数字分身没有 .td-root 三栏；AI 会话栏是本页自己的 .av-chat-drawer（宽度走 --av-chat-w），
       预览栏插在它右侧，成为 shell flex 行（div:has(> main)）的最后一个子项；
     · 「让位对象」不是详情页的 .td-left，而是 shell 自己的「左导航 aside」（React 内联宽 256px）
       → 用 .av-browse-on 收宽度（200ms，沿用外壳自带 transition-all）；
     · 预览栏宽度走**本页独立变量** --av-browse-w（默认 641 = 树 240 + 分栏条 1 + 代码 400），
       不与详情页的 --td-browse-right-w 混用，避免布局记忆串味。
   本脚本必须插在 #av-chat-js **之前**：Esc 裁决靠注册顺序，预览栏要能先吃掉这一层。
   ================================================================================ */

/* ---------- 轻提示：DS Message（与详情页 tdToast 同构造，元素名沿用 .td-dp-msg） ---------- */
var AV_MSG_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
  '<circle cx="7" cy="7" r="6.2" fill="currentColor"/>' +
  '<path d="M4.3 7.2l1.9 1.9 3.5-3.7" stroke="var(--color-white)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

function avToast(text) {
  var box = document.querySelector('.td-dp-msg');
  if (!box) {
    box = document.createElement('div');
    box.className = 'td-dp-msg';
    box.innerHTML = '<div class="giencoder-message" role="status">' +
      '<span class="giencoder-message-icon" aria-hidden="true">' + AV_MSG_SVG + '</span>' +
      '<span class="giencoder-message-content"></span></div>';
    box.hidden = true;
    document.body.appendChild(box);
  }
  box.querySelector('.giencoder-message-content').textContent = text;
  box.hidden = false;
  clearTimeout(box._t);
  box._t = setTimeout(function () { box.hidden = true; }, 2400);
}

/* 右键菜单段用它判断「浏览态是否打开」—— 直接查类名，与该段原来的 .td-root.is-browse 等价 */
function avBrowseOpen() { return !!document.querySelector('.av-browse-on'); }

/*__CTX__*/

(function () {
  var KEY = 'giencoder:av-browse:v1';
  var GAP = 8;                                   /* 与 .av-chat-gutter 净占位同值 */
  var DEF_PANEL = 641, MIN_PANEL = 641, MAIN_MIN = 240;
  var DEF_TREE = 296, MIN_TREE = 240, MIN_CODE = 320;

  var slot = document.getElementById('av-browse-slot');
  if (!slot) return;
  var pane = null, splitMain = null;
  var hostRow = null, hostMain = null, gutter = null, drawer = null;
  var panelW = DEF_PANEL, treeW = DEF_TREE;
  var bound = false, ctxBound = false;

  function readStore() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null') || {}; } catch (e) { return {}; }
  }
  function writeStore(patch) {
    var d = readStore();
    for (var k in patch) { if (Object.prototype.hasOwnProperty.call(patch, k)) d[k] = patch[k]; }
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {}
  }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  /* ==================== 挂载：shell flex 行的最后一个子项 ====================
     行的 DOM 顺序由抽屉脚本先建立：… <main> → .av-chat-gutter → <aside 抽屉>；
     本脚本再往后接 [分栏条 td-split="main"] → [预览栏 slot]。
     抽屉脚本不认识本节点，故两边各挂一个常驻 MutationObserver；place() 命中即早退、不产生新变更，
     不会互激。 */
  function place() {
    if (hostRow && hostRow.isConnected
        && drawer && drawer.parentElement === hostRow
        && splitMain && splitMain.parentElement === hostRow
        && slot.parentElement === hostRow
        && splitMain.previousElementSibling === drawer
        && slot.previousElementSibling === splitMain) return true;
    hostRow = document.querySelector('div:has(> main)');
    if (!hostRow) return false;
    hostMain = hostRow.querySelector(':scope > main') || hostRow.querySelector('main');
    if (!hostMain) return false;
    gutter = hostRow.querySelector('.av-chat-gutter');
    drawer = document.getElementById('av-chat-drawer');
    if (!gutter || !drawer || drawer.parentElement !== hostRow) return false;   /* 等抽屉脚本先挂好 */
    splitMain = document.getElementById('av-browse-split');
    pane = slot.querySelector('.td-browse');
    if (!splitMain || !pane) return false;
    hostRow.insertBefore(splitMain, drawer.nextSibling);
    hostRow.insertBefore(slot, splitMain.nextSibling);
    bindAll();
    clampNow();
    return true;
  }

  /* ==================== 宽度：① 预览栏 ② 文件目录 ==================== */
  /* 可分配给 main + gutter + 抽屉 + 分栏条 + 预览栏 的总宽 = 行内容宽 − 其它 flex 子项（左导航等） */
  function freeW() {
    if (!hostRow) return 0;
    var cs = getComputedStyle(hostRow);
    var w = hostRow.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0);
    Array.prototype.forEach.call(hostRow.children, function (c) {
      if (c === hostMain || c === gutter || c === drawer || c === splitMain || c === slot) return;
      w -= c.getBoundingClientRect().width;
    });
    return w;
  }
  function chatW() {
    var v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--av-chat-w'));
    return isNaN(v) ? 480 : v;
  }
  function maxPanelW() { return Math.max(MIN_PANEL, Math.round(freeW() - chatW() - GAP - MAIN_MIN)); }
  function setPanelW(w, persist) {
    panelW = Math.round(clamp(w, MIN_PANEL, maxPanelW()));
    slot.style.setProperty('--av-browse-w', panelW + 'px');
    if (splitMain) {
      splitMain.setAttribute('aria-valuenow', String(panelW));
      splitMain.setAttribute('aria-valuemin', String(MIN_PANEL));
      splitMain.setAttribute('title', '拖动调整文件预览栏宽度（最小 ' + MIN_PANEL + 'px）· 双击复位');
    }
    if (persist) writeStore({ panelW: panelW });
    return panelW;
  }
  function maxTree() {
    var sw = slot.getBoundingClientRect().width || panelW;
    return Math.max(MIN_TREE, Math.round(sw - 1 - MIN_CODE));
  }
  function setTree(w, persist) {
    treeW = Math.round(clamp(w, MIN_TREE, maxTree()));
    pane.style.setProperty('--td-browse-tree-w', treeW + 'px');
    var st = pane.querySelector('[data-td-split="tree"]');
    if (st) {
      st.setAttribute('aria-valuenow', String(treeW));
      st.setAttribute('aria-valuemin', String(MIN_TREE));
      st.setAttribute('title', '拖动调整文件目录宽度（最小 ' + MIN_TREE + 'px）· 双击复位');
    }
    if (persist) writeStore({ treeW: treeW });
    return treeW;
  }
  function clampNow() {
    if (!hostRow) return;
    setPanelW(panelW, false);
    setTree(treeW, false);
  }
  /* 让 AI 会话栏脚本按新的可用宽重算钳位（它监听 window resize 并做 rAF 节流；此处不改它的代码） */
  function syncLayout() { try { window.dispatchEvent(new Event('resize')); } catch (e) {} }

  /* ==================== 展开 / 收起（含微动效，与详情页同款） ==================== */
  function setOpen(on) {
    if (!place()) return;
    var isOn = hostRow.classList.contains('av-browse-on');
    if (on === isOn && !pane.classList.contains('is-closing')) return;
    var btn = drawer.querySelector('[data-td-browse-toggle]');
    if (on) {
      if (pane._browseT) { clearTimeout(pane._browseT); pane._browseT = null; }
      pane.classList.remove('is-closing');
      hostRow.classList.add('av-browse-on');
      if (btn) btn.setAttribute('aria-pressed', 'true');
      setPanelW(panelW, false);
      setTree(treeW, false);
      syncLayout();
      setTimeout(syncLayout, 260);              /* 左导航 200ms 收拢结束、可用宽定型后再校一次 */
      return;
    }
    if (pane.classList.contains('is-closing')) return;
    var done = function () {
      pane._browseT = null;
      pane.classList.remove('is-closing');
      hostRow.classList.remove('av-browse-on');
      if (btn) btn.setAttribute('aria-pressed', 'false');
      syncLayout();
      setTimeout(syncLayout, 260);
    };
    pane.classList.add('is-closing');
    pane._browseT = setTimeout(done, 240);
    pane.addEventListener('animationend', function onEnd(e) {
      if (e.target !== pane) return;            /* 过滤内层跟手位移动画的冒泡 */
      clearTimeout(pane._browseT);
      pane.removeEventListener('animationend', onEnd);
      done();
    });
  }

  /* ==================== 一次性绑定 ==================== */
  function bindSplit(el, kind) {
    if (!el) return;
    var dragging = false, startX = 0, startPanel = 0, startTree = 0;
    el.addEventListener('pointerdown', function (e) {
      if (!avBrowseOpen() || e.button !== 0) return;
      dragging = true;
      startX = e.clientX; startPanel = panelW; startTree = treeW;
      el.classList.add('is-dragging');
      hostRow.classList.add('is-col-dragging');
      if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    el.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      if (kind === 'panel') setPanelW(startPanel - (e.clientX - startX), false);
      else setTree(startTree + (e.clientX - startX), false);
    });
    function end() {
      if (!dragging) return;
      dragging = false;
      el.classList.remove('is-dragging');
      hostRow.classList.remove('is-col-dragging');
      writeStore(kind === 'panel' ? { panelW: panelW } : { treeW: treeW });
    }
    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
    el.addEventListener('dblclick', function () {
      if (kind === 'panel') setPanelW(DEF_PANEL, true); else setTree(DEF_TREE, true);
    });
    el.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 48 : 16;
      if (e.key === 'ArrowLeft') { e.preventDefault(); if (kind === 'panel') setPanelW(panelW + step, true); else setTree(treeW - step, true); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); if (kind === 'panel') setPanelW(panelW - step, true); else setTree(treeW + step, true); }
    });
  }

  function bindAll() {
    if (bound) return;
    bound = true;

    var btn = drawer.querySelector('[data-td-browse-toggle]');
    if (btn) btn.addEventListener('click', function () { setOpen(!avBrowseOpen()); });
    var close = pane.querySelector('[data-td-browse-close]');
    if (close) close.addEventListener('click', function () { setOpen(false); });

    bindSplit(splitMain, 'panel');
    bindSplit(pane.querySelector('[data-td-split="tree"]'), 'tree');

    /* ---------- crumb 右侧两按钮（与详情页同款） ---------- */
    var body = pane.querySelector('.td-browse-body');
    var tgl = pane.querySelector('[data-td-tree-toggle]');
    if (tgl && body) {
      tgl.addEventListener('click', function () {
        var hidden = body.classList.toggle('is-no-tree');
        tgl.setAttribute('aria-pressed', hidden ? 'false' : 'true');
        var label = hidden ? '显示文件目录' : '隐藏文件目录';
        tgl.setAttribute('aria-label', label);
        tgl.setAttribute('title', label);
        if (!hidden) setTree(treeW, false);
      });
    }
    var openBtn = pane.querySelector('[data-td-open-browser]');
    var crumb = pane.querySelector('.td-browse-crumb-path');
    if (openBtn) {
      openBtn.addEventListener('click', function () {
        var name = crumb && crumb.textContent ? crumb.textContent.split('/').pop().trim() : '';
        if (!name) return;
        /* 与详情页同口径：映射到仓库根的同名文件（本页在 pages/ 下）→ ../index.html 真实存在。
           ⚠️ 内置 http 预览里 ../ 会落到 static-html 根 —— file:// 直开是标准用法。 */
        window.open(new URL('../' + name, location.href).href, '_blank', 'noopener');
      });
    }

    /* ---------- 文件树：展开/折叠 + 选中 ---------- */
    function refresh() {
      var rows = pane.querySelectorAll('.td-bf'), i;
      for (i = 0; i < rows.length; i++) {
        var p = rows[i].dataset.parent || '', ok = true;
        while (p) {
          var pr = pane.querySelector('.td-bf[data-node="' + p + '"]');
          if (!pr || pr.classList.contains('is-closed')) { ok = false; break; }
          p = pr.dataset.parent || '';
        }
        rows[i].classList.toggle('is-hidden', !ok);
      }
    }
    function toggleDir(row) {
      var closed = row.classList.toggle('is-closed');
      row.setAttribute('aria-expanded', closed ? 'false' : 'true');
      refresh();
    }
    function selectFile(row) {
      var old = pane.querySelector('.td-bf.is-active');
      if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
      row.classList.add('is-active');
      row.setAttribute('aria-selected', 'true');
    }
    var files = pane.querySelector('.td-browse-files');
    if (files) {
      files.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
        if (!row) return;
        if (row.classList.contains('is-dir')) toggleDir(row); else selectFile(row);
      });
      files.addEventListener('keydown', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
        if (!row || row !== e.target) return;
        var isDir = row.classList.contains('is-dir'), closed = row.classList.contains('is-closed');
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          if (isDir) toggleDir(row); else selectFile(row);
        } else if (e.key === 'ArrowRight' && isDir && closed) { e.preventDefault(); toggleDir(row); }
        else if (e.key === 'ArrowLeft' && isDir && !closed) { e.preventDefault(); toggleDir(row); }
      });
    }

    /* ---------- 恢复本页布局记忆 ---------- */
    var d = readStore();
    if (typeof d.panelW === 'number') panelW = d.panelW;
    if (typeof d.treeW === 'number') treeW = d.treeW;
    clampNow();

    if (!ctxBound) {
      ctxBound = true;
      try { bindBrowseContextMenu(); } catch (e) {}
    }
  }

  /* ==================== Esc 裁决（捕获段，注册在抽屉脚本之前 → 先吃一层） ====================
     顺序：① 右键菜单 → ② 预览栏。自己吃掉即 stopImmediatePropagation，避免一次 Esc 把 AI 会话栏也收掉。 */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (document.documentElement.hasAttribute('data-td-ctx-open')) {
      e.preventDefault(); e.stopImmediatePropagation();
      document.dispatchEvent(new CustomEvent('td:close-ctx'));
      return;
    }
    if (avBrowseOpen()) {
      e.preventDefault(); e.stopImmediatePropagation();
      setOpen(false);
    }
  }, true);

  /* AI 会话栏收起时，预览栏一并收起（否则会留下一块孤立的文件预览） */
  new MutationObserver(function () {
    if (!document.documentElement.hasAttribute('data-av-chat-open') && avBrowseOpen()) setOpen(false);
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-av-chat-open'] });

  /* 视口变化重钳位 */
  var raf = 0;
  window.addEventListener('resize', function () {
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () { raf = 0; if (avBrowseOpen()) clampNow(); });
  });

  if (!place()) {
    var mo0 = new MutationObserver(function () { if (place()) mo0.disconnect(); });
    mo0.observe(document.body, { childList: true, subtree: true });
  }
  var moKeep = new MutationObserver(function () { place(); });
  moKeep.observe(document.body, { childList: true, subtree: true });
})();
