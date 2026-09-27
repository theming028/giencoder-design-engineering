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