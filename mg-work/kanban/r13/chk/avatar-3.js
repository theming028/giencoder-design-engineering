
(function () {
  var drawer = document.getElementById('av-chat-drawer');
  if (!drawer) return;
  var root = document.documentElement;
  var mask = document.querySelector('[data-av-chat-mask]');
  var wrap = drawer;            /* 模块本体用 wrap 作用域，这里指向抽屉 */

  /* ==================================================================
     模块本体：对话框三个弹层（add / skill / select）
     构建期从 pages/task-detail.html 的 bindDetail() 原样抽出，禁手改。
     行为：点「添加」→ 上方弹出菜单；点「技能」→ 上方技能面板；
           点「标准模式 / 大模型」→ DS Select 弹层（唯一开关类 .giencoder-popup-open）；
           点外部 → 全关；Esc 由本脚本统一裁决（见下）。
     ================================================================== */
/* ================= 对话框三个弹层（★ 第 28 轮第 4 项） =================
       行为对齐 pages/base.html 实测：
         · 点「添加」按钮 → 在按钮上方弹出 180×92 菜单（两项 + 分隔线）；再点按钮关闭；
         · 点「技能」按钮 → 在对话框上方弹出 760×320 面板（Goal + 技能列表 + 底部两个按钮）；
         · 点「大模型 / 标准模式」视图 → 展开 DS Select 弹层；
         · 点菜单项 / 技能行 / 模型项 → **只关闭弹层**（base 实测：不写 textarea、也没有隐藏的
           input[type=file]，所以「添加本地文件」这里同样只关闭，保持一致）；
         · 点弹层外部 → 全部关闭；
         · Esc → 全部关闭。⚠️ base 里 Esc 不关技能面板，但本页 Esc 是「返回任务看板」的全局快捷键，
           必须先吃掉这次 Esc，否则会误跳转 → 用自定义事件 td:close-popovers 与页尾脚本约定（见 TAIL）。 */
    var opAdd = null, opSkill = null, opSel = null;
    function popFlag() { document.documentElement.toggleAttribute('data-td-pop-open', !!(opAdd || opSkill || opSel)); }
    function closeAdd() { if (!opAdd) return; opAdd.pop.hidden = true; opAdd.btn.setAttribute('aria-expanded', 'false'); opAdd = null; popFlag(); }
    function closeSkill() { if (!opSkill) return; opSkill.pop.hidden = true; opSkill.btn.setAttribute('aria-expanded', 'false'); opSkill = null; popFlag(); }
    /* ⚠️ DS Select 弹层的开合唯一开关是 `.giencoder-popup-open`（ui-controls.css），
       不要用内联 display（display:block 但 opacity:0/visibility:hidden ⇒ 看不见）。 */
    function closeSel() { if (!opSel) return; opSel.pop.classList.remove('giencoder-popup-open'); opSel.view.setAttribute('aria-expanded', 'false'); opSel = null; popFlag(); }
    function closePops() { closeAdd(); closeSkill(); closeSel(); }

    var addBtn = wrap.querySelector('[data-td-add-btn]');
    var addPop = wrap.querySelector('[data-td-add-pop]');
    if (addBtn && addPop) {
      addBtn.addEventListener('click', function () {
        closeSkill(); closeSel();
        if (opAdd) { closeAdd(); return; }
        addPop.hidden = false;
        addBtn.setAttribute('aria-expanded', 'true');
        opAdd = { btn: addBtn, pop: addPop }; popFlag();
        var f = addPop.querySelector('[role="menuitem"]');
        if (f) f.focus();
      });
      Array.prototype.forEach.call(addPop.querySelectorAll('[role="menuitem"]'), function (it) {
        it.addEventListener('click', function () { closeAdd(); });
      });
    }

    var skillBtn = wrap.querySelector('[data-td-skill-btn]');
    var skillPop = wrap.querySelector('[data-td-skill-pop]');
    if (skillBtn && skillPop) {
      skillBtn.addEventListener('click', function () {
        closeAdd(); closeSel();
        if (opSkill) { closeSkill(); return; }
        skillPop.hidden = false;
        skillBtn.setAttribute('aria-expanded', 'true');
        opSkill = { btn: skillBtn, pop: skillPop }; popFlag();
      });
      Array.prototype.forEach.call(skillPop.querySelectorAll('.td-skill-row'), function (row) {
        row.addEventListener('click', function () { closeSkill(); });
      });
      var skillX = skillPop.querySelector('[data-td-skill-close]');
      if (skillX) skillX.addEventListener('click', function () { closeSkill(); skillBtn.focus(); });
    }

    /* 大模型 / 标准模式：DS Select 契约结构 —— 视图点击开合、选项点击选中并回写文案 */
    Array.prototype.forEach.call(wrap.querySelectorAll('.td-composer .giencoder-select'), function (sel) {
      var view = sel.querySelector('.giencoder-select-view');
      var pop = sel.querySelector('.giencoder-select-popup');
      if (!view || !pop) return;
      view.addEventListener('click', function () {
        closeAdd(); closeSkill();
        if (opSel && opSel.pop === pop) { closeSel(); return; }
        closeSel();
        pop.classList.add('giencoder-popup-open');
        view.setAttribute('aria-expanded', 'true');
        opSel = { view: view, pop: pop }; popFlag();
      });
      view.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); view.click(); }
      });
      Array.prototype.forEach.call(pop.querySelectorAll('.giencoder-select-option'), function (opt) {
        opt.addEventListener('click', function () {
          if (opt.classList.contains('giencoder-select-option-disabled')) return;
          Array.prototype.forEach.call(pop.querySelectorAll('.giencoder-select-option'), function (o) {
            o.classList.remove('giencoder-select-option-selected');
            o.setAttribute('aria-selected', 'false');
          });
          opt.classList.add('giencoder-select-option-selected');
          opt.setAttribute('aria-selected', 'true');
          var txt = view.querySelector('.giencoder-select-view-text');
          if (txt) txt.textContent = opt.textContent.trim();
          closeSel();
        });
      });
    });

    /* 点弹层与触发器以外的任何地方 → 全部关闭
       ⚠️ 「技能」按钮本身不在 .giencoder-select 里，必须单独列出，否则它的 click 会先打开面板、
          紧接着冒泡到 document 又被立刻关掉。 */
    document.addEventListener('click', function (e) {
      if (!opAdd && !opSkill && !opSel) return;
      if (e.target.closest && e.target.closest('.td-add-pop, .td-skill-pop, .giencoder-select, [data-td-skill-btn]')) return;
      closePops();
    });
    document.addEventListener('td:close-popovers', closePops);

  /* ==================== 抽屉开合 ====================
     ⚠️ 属性必须分成两个，不能共用一个（第 34 轮踩坑）：
       · `html[data-av-chat-open]`  = 抽屉的**开合状态**，写在 <html> 上，供 CSS 驱动动画；
       · `[data-av-chat-toggle]`    = **触发器**标记，只写在按钮上。
     若两者共用一个属性名，`e.target.closest('[data-av-chat-open]')` 会顺着祖先链
     命中 <html> 本身 —— 于是「抽屉打开时，抽屉内任何一次点击都会把它关掉」
     实测栈：closeChat ← toggleChat ← 点击「技能」按钮。 */
  function isOpen() { return root.hasAttribute('data-av-chat-open'); }
  function syncTriggers() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-av-chat-toggle]'), function (b) {
      b.setAttribute('aria-expanded', isOpen() ? 'true' : 'false');
    });
  }
  function openChat() {
    root.setAttribute('data-av-chat-open', '');
    drawer.setAttribute('aria-hidden', 'false');
    syncTriggers();
  }
  function closeChat() {
    closePops();                       /* 模块内：关掉可能开着的弹层 */
    root.removeAttribute('data-av-chat-open');
    drawer.setAttribute('aria-hidden', 'true');
    syncTriggers();
  }
  function toggleChat() { isOpen() ? closeChat() : openChat(); }

  /* 触发器：事件委托，兼容脚本注入的按钮 */
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest && e.target.closest('[data-av-chat-toggle]');
    if (!t) return;
    e.preventDefault();
    toggleChat();
  }, true);
  if (mask) mask.addEventListener('click', closeChat);

  /* ==================== 全屏（复用模块顶栏的全屏按钮） ==================== */
  var fsBtn = drawer.querySelector('[data-td-fullscreen]');
  function setFs(on) {
    drawer.classList.toggle('is-fullscreen', !!on);
    if (fsBtn) {
      fsBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      fsBtn.setAttribute('title', on ? '退出全屏' : '全屏');
      fsBtn.setAttribute('aria-label', on ? '退出全屏' : '全屏');
    }
  }
  if (fsBtn) fsBtn.addEventListener('click', function () {
    setFs(!drawer.classList.contains('is-fullscreen'));
  });
  /* 抽屉没有可拖动的分栏，故不提供「折叠」入口；此处只保证模块自带的
     折叠态按钮（.td-collapsed）若被程序置态后仍可恢复。 */
  var expBtn = drawer.querySelector('[data-td-expand]');
  if (expBtn) expBtn.addEventListener('click', function () {
    drawer.classList.remove('is-collapsed');
  });

  /* ==================== Esc 裁决（捕获阶段，先于外壳的全局快捷键） ====================
     顺序：① 模块弹层 → ② 全屏 → ③ 抽屉。每级只吃掉一层，避免一次 Esc 全关。 */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (opAdd || opSkill || opSel) { closePops(); e.preventDefault(); e.stopPropagation(); return; }
    if (drawer.classList.contains('is-fullscreen')) { setFs(false); e.preventDefault(); e.stopPropagation(); return; }
    if (isOpen()) { closeChat(); e.preventDefault(); e.stopPropagation(); }
  }, true);

  /* ==================== 触发器注入（内容标题行，全页唯一） ==================== */
  var ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide size-3.5" aria-hidden="true"><path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg>' + '通过对话完善数字分身';
  function injectTrigger() {
    var row = document.querySelector('div.flex.items-start.justify-between');
    if (!row) return false;
    if (row.querySelector('[data-av-chat-toggle]')) return true;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'giencoder-btn giencoder-btn-secondary giencoder-btn-size-default av-chat-trigger';
    btn.setAttribute('data-av-chat-toggle', '1');
    btn.setAttribute('aria-controls', 'av-chat-drawer');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = ICON;
    var primary = row.querySelector('.giencoder-btn-primary');
    if (primary) row.insertBefore(btn, primary); else row.appendChild(btn);
    return true;
  }
  if (!injectTrigger()) {
    /* React 首帧可能晚于本脚本：等它挂载完再注入（注入成功即断开观察器） */
    var mo = new MutationObserver(function () {
      if (injectTrigger()) mo.disconnect();
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
