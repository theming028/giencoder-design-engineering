/* ================================================================================
   ★ r105 ③：文件预览栏控制器（**会话详情页**版）
   上游 = `mg-work/r102/part105/browse.js` 的控制器段（数字分身 avatar.html，第 69~71 轮）。
   HTML / CSS / 右键菜单三件与数字分身**逐字同源**；只有本控制器按本页布局改写。
   为什么要改写（两页的 flex 行结构不同）：
     · 数字分身：shell flex 行 = … <main> → .av-chat-gutter → <aside 抽屉>，
       预览栏挂**抽屉右侧**，宽度预算里要扣掉「会话栏宽 --av-chat-w + 接缝 GAP」，
       并且要等抽屉脚本先把 gutter / 抽屉挂好才 place()；
     · 本页：会话内容**就在 main 里**，没有抽屉也没有 gutter ⇒ 预览栏直接接在 main 之后，
       宽度预算只扣「main 的舒适下限 MAIN_MIN」。
   其余一律沿用上游实现：分栏条拖动 / 双击复位 / 键盘微调 / 文件树开合与选中 /
   crumb 右侧两个按钮 / Esc 裁决（先右键菜单、后预览栏）/ 布局记忆 /
   MutationObserver 补挂 / 宽度变量 --av-browse-w。
   ⚠ 宽度记忆的 localStorage key 换成 `giencoder:r105-browse:v1`（与数字分身分开，不串味）。
   ================================================================================ */
(function () {
  var KEY = 'giencoder:r105-browse:v1';
  /* 默认宽 641；MIN_PANEL = 561 = 文件树 MIN_TREE(240) + 分栏条 1 + 代码区 MIN_CODE(320)
     —— 与「内部两栏最小宽之和」自洽（口径同数字分身第 71 轮第 4 项的修正）。
     MAIN_MIN = 380：main 被挤到多窄就不再让了。 */
  var DEF_PANEL = 641, MIN_PANEL = 561, MAIN_MIN = 380;
  var DEF_TREE = 296, MIN_TREE = 240, MIN_CODE = 320;

  var slot = document.getElementById('av-browse-slot');
  if (!slot) return;
  var pane = null, splitMain = null, hostRow = null, hostMain = null;
  /* 生效宽：每次由期望宽 + 当前可用宽重钳，可被临时压缩 */
  var panelW = DEF_PANEL, treeW = DEF_TREE;
  /* 期望宽（用户意图）：只由「恢复记忆 / 拖动 / 双击复位 / 键盘」改写 ⇒ 视口变大能自动长回来 */
  var wantPanel = DEF_PANEL, wantTree = DEF_TREE;
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
  /* 页头那枚「打开侧栏」（本页自己的按钮，不是数字分身顶栏里的那枚） */
  function toggleBtn() { return document.querySelector('.r93-baract[data-r93-browse]'); }
  function browseOpen() { return !!(hostRow && hostRow.classList.contains('av-browse-on')); }

  /* ==================== 挂载：shell flex 行里 main 之后的最后一个子项 ==================== */
  function place() {
    if (hostRow && hostRow.isConnected && splitMain && splitMain.parentElement === hostRow
        && slot.parentElement === hostRow
        && splitMain.previousElementSibling === hostMain
        && slot.previousElementSibling === splitMain) return true;
    hostRow = document.querySelector('div:has(> main)');
    if (!hostRow) return false;                       /* React 还没渲染出 shell 行 */
    hostMain = hostRow.querySelector(':scope > main') || hostRow.querySelector('main');
    if (!hostMain) return false;
    splitMain = document.getElementById('av-browse-split');
    pane = slot.querySelector('.td-browse');
    if (!splitMain || !pane) return false;
    hostRow.insertBefore(splitMain, hostMain.nextSibling);
    hostRow.insertBefore(slot, splitMain.nextSibling);
    slot.classList.add('av-slot-placed');             /* 挂进 flex 行后才渲染（CSS 门） */
    bindAll();
    clampNow();
    return true;
  }

  /* ==================== 宽度：① 预览栏 ② 文件目录 ==================== */
  /* 可分配给 main + 分栏条 + 预览栏 的总宽 = 行内容宽 − 其它 flex 子项（本页只有左导航 aside） */
  function freeW() {
    if (!hostRow) return 0;
    var cs = getComputedStyle(hostRow);
    var w = hostRow.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0);
    [].forEach.call(hostRow.children, function (c) {
      if (c === hostMain || c === splitMain || c === slot) return;
      w -= c.getBoundingClientRect().width;
    });
    return w;
  }
  function maxPanelW() { return Math.max(MIN_PANEL, Math.round(freeW() - MAIN_MIN)); }
  function setPanelW(w, persist) {
    wantPanel = Math.round(w);
    panelW = Math.round(clamp(wantPanel, MIN_PANEL, maxPanelW()));
    slot.style.setProperty('--av-browse-w', panelW + 'px');
    if (splitMain) {
      splitMain.setAttribute('aria-valuenow', String(panelW));
      splitMain.setAttribute('aria-valuemin', String(MIN_PANEL));
      splitMain.setAttribute('title', '拖动调整文件预览栏宽度（最小 ' + MIN_PANEL + 'px）· 双击复位');
    }
    if (persist) writeStore({ panelW: wantPanel });
    return panelW;
  }
  function maxTree() {
    var sw = slot.getBoundingClientRect().width || panelW;
    return Math.max(MIN_TREE, Math.round(sw - 1 - MIN_CODE));
  }
  function setTree(w, persist) {
    wantTree = Math.round(w);
    treeW = Math.round(clamp(wantTree, MIN_TREE, maxTree()));
    pane.style.setProperty('--td-browse-tree-w', treeW + 'px');
    var st = pane.querySelector('[data-td-split="tree"]');
    if (st) {
      st.setAttribute('aria-valuenow', String(treeW));
      st.setAttribute('aria-valuemin', String(MIN_TREE));
      st.setAttribute('title', '拖动调整文件目录宽度（最小 ' + MIN_TREE + 'px）· 双击复位');
    }
    if (persist) writeStore({ treeW: wantTree });
    return treeW;
  }
  function clampNow() {
    if (!hostRow) return;
    setPanelW(wantPanel, false);
    setTree(wantTree, false);
  }
  /* 让外壳按新的可用宽重算（外壳监听 window resize，此处不改它的代码） */
  function syncLayout() { try { window.dispatchEvent(new Event('resize')); } catch (e) {} }

  /* ==================== 展开 / 收起（纯宽度过渡，与左导航 aside 同款） ==================== */
  function setOpen(on) {
    if (!place()) return;
    var isOn = hostRow.classList.contains('av-browse-on');
    if (on === isOn && !pane.classList.contains('is-closing')) return;
    var btn = toggleBtn();
    if (on) {
      if (pane._browseT) { clearTimeout(pane._browseT); pane._browseT = null; }
      pane.classList.remove('is-closing');
      hostRow.classList.add('av-browse-on');
      if (btn) { btn.setAttribute('aria-pressed', 'true'); btn.setAttribute('title', '关闭侧栏'); btn.setAttribute('aria-label', '关闭侧栏'); }
      setPanelW(wantPanel, false);
      setTree(wantTree, false);
      syncLayout();
      setTimeout(syncLayout, 260);                    /* 左导航 200ms 收拢结束、可用宽定型后再校一次 */
      return;
    }
    if (pane.classList.contains('is-closing')) return;
    /* 收起不播 keyframes —— 摘掉状态类后由 `.td-browse-slot` 的 flex-basis 过渡自然收拢。
       is-closing 只作 JS 防抖标记（无对应 CSS）；期间再点开会在上方分支里清掉定时器并平滑反向。 */
    pane.classList.add('is-closing');
    hostRow.classList.remove('av-browse-on');
    if (btn) { btn.setAttribute('aria-pressed', 'false'); btn.setAttribute('title', '打开侧栏'); btn.setAttribute('aria-label', '打开侧栏'); }
    pane._browseT = setTimeout(function () {
      pane._browseT = null;
      pane.classList.remove('is-closing');
      syncLayout();
    }, 220);
    syncLayout();
  }

  /* ==================== 一次性绑定 ==================== */
  function bindSplit(el, kind) {
    if (!el) return;
    var dragging = false, startX = 0, startPanel = 0, startTree = 0;
    el.addEventListener('pointerdown', function (e) {
      if (!browseOpen() || e.button !== 0) return;
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
      writeStore(kind === 'panel' ? { panelW: wantPanel } : { treeW: wantTree });
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

    var close = pane.querySelector('[data-td-browse-close]');
    if (close) close.addEventListener('click', function () { setOpen(false); });

    bindSplit(splitMain, 'panel');
    bindSplit(pane.querySelector('[data-td-split="tree"]'), 'tree');

    /* ---------- crumb 右侧两按钮（与数字分身同款） ---------- */
    var body = pane.querySelector('.td-browse-body');
    var tgl = pane.querySelector('[data-td-tree-toggle]');
    if (tgl && body) {
      tgl.addEventListener('click', function () {
        var hidden = body.classList.toggle('is-no-tree');
        tgl.setAttribute('aria-pressed', hidden ? 'false' : 'true');
        var label = hidden ? '显示文件目录' : '隐藏文件目录';
        tgl.setAttribute('aria-label', label);
        tgl.setAttribute('title', label);
        if (!hidden) setTree(wantTree, false);
      });
    }
    var openBtn = pane.querySelector('[data-td-open-browser]');
    var crumb = pane.querySelector('.td-browse-crumb-path');
    if (openBtn) {
      openBtn.addEventListener('click', function () {
        var name = crumb && crumb.textContent ? crumb.textContent.split('/').pop().trim() : '';
        if (!name) return;
        /* 与数字分身同口径：映射到仓库根的同名文件（本页在 pages/ 下）。
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
    if (typeof d.panelW === 'number') { panelW = d.panelW; wantPanel = d.panelW; }
    if (typeof d.treeW === 'number') { treeW = d.treeW; wantTree = d.treeW; }
    clampNow();

    if (!ctxBound) {
      ctxBound = true;
      try { bindBrowseContextMenu(); } catch (e) {}
    }
  }

  /* ==================== 页头那枚「打开侧栏」 ====================
     用**捕获阶段的文档级委托**而不是直接 bind —— 宿主 `.r93-conv-host`（连同这枚按钮）是本页脚本
     稍后才建出来的，本 IIFE 在解析期执行时按钮还不在 DOM 里（先例：r86 / r88 的捕获阶段拦截）。 */
  document.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    if (!t.closest('.r93-baract[data-r93-browse]')) return;
    setOpen(!browseOpen());
  }, true);

  /* ==================== Esc 裁决（捕获段）====================
     顺序：① 右键菜单 → ② 预览栏 → ③ 全屏（★ r105 ③ 新增）。吃掉即 stopImmediatePropagation，
     避免一次 Esc 连关两层。
     ⚠ 全屏那层**不直接改 `<html data-r93-full>`** —— 状态由 r102 主脚本持有（它同时要翻
       按钮上的 aria-pressed / title / aria-label，并派发 resize 让外壳与预览栏重算）。
       本脚本更晚注册，直接调函数会反序 ⇒ 走自定义事件 `r93:fullscreen`。 */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (document.documentElement.hasAttribute('data-td-ctx-open')) {
      e.preventDefault(); e.stopImmediatePropagation();
      document.dispatchEvent(new CustomEvent('td:close-ctx'));
      return;
    }
    if (browseOpen()) {
      e.preventDefault(); e.stopImmediatePropagation();
      setOpen(false);
      return;
    }
    if (document.documentElement.hasAttribute('data-r93-full')) {
      e.preventDefault(); e.stopImmediatePropagation();
      document.dispatchEvent(new CustomEvent('r93:fullscreen', { detail: { on: false } }));
    }
  }, true);

  /* 视口变化重钳位 */
  var raf = 0;
  window.addEventListener('resize', function () {
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () { raf = 0; if (browseOpen()) clampNow(); });
  });

  if (!place()) {
    var mo0 = new MutationObserver(function () { if (place()) mo0.disconnect(); });
    mo0.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { mo0.disconnect(); }, 8000);
  }
  /* 常驻观察：React 若把节点移除/移动，立刻插回（place() 命中即早退，开销可忽略） */
  var moKeep = new MutationObserver(function () { place(); });
  moKeep.observe(document.body, { childList: true, subtree: true });
})();
