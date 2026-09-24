/* ═══════════════════════════════════════════════════════════════
 * ui-kits 共享控件交互（Select / DatePicker）
 * 来源：组件标准实现（giencoder/preview/component-select.html、
 *       giencoder/preview/component-date-picker.html），与组件规范页行为一致；
 *       仅差异：模板页面板默认收起（preview 为静态演示默认展开）
 * 依赖：components.css + ui-controls.css
 * ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ─────────── Select 选择器交互 ───────────
   * 1. 点击触发框展开/收起弹层（display + 过渡动画，同步 aria-expanded）
   * 2. 点击选项：互斥高亮 giencoder-select-option-selected，同步触发框文本并收起；disabled 不可选
   * 3. 点击外部收起全部弹层
   */
  document.querySelectorAll('.giencoder-select').forEach(function (sel) {
    if (sel.classList.contains('giencoder-select-disabled')) return;
    var view = sel.querySelector('.giencoder-select-view');
    var popup = sel.querySelector('.giencoder-select-popup');
    if (!view || !popup) return;
    var options = Array.prototype.slice.call(popup.querySelectorAll('.giencoder-select-option'));

    function isPopupOpen(p) { return !!p && p.classList.contains('giencoder-popup-open'); }
    function openPopup(p) {
      if (!p) { return; }
      if (p._closeTimer) { clearTimeout(p._closeTimer); p._closeTimer = null; }
      p.style.display = '';
      var token = (p._animToken = (p._animToken || 0) + 1);
      requestAnimationFrame(function () {
        if (!p.isConnected || p._animToken !== token) { return; }
        p.classList.add('giencoder-popup-open');
      });
    }
    function closePopup(p) {
      if (!p) { return; }
      var token = (p._animToken = (p._animToken || 0) + 1);
      p.classList.remove('giencoder-popup-open');
      if (p._closeTimer) { clearTimeout(p._closeTimer); }
      p._closeTimer = setTimeout(function () {
        p._closeTimer = null;
        if (!p.isConnected || p._animToken !== token) { return; }
        p.style.display = 'none';
      }, 200);
    }
    function isOpen() { return isPopupOpen(popup); }
    function open() { openPopup(popup); view.setAttribute('aria-expanded', 'true'); }
    function close() { closePopup(popup); view.setAttribute('aria-expanded', 'false'); }

    view.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (isOpen()) close(); else open();
    });

    options.forEach(function (opt) {
      opt.addEventListener('click', function (ev) {
        ev.stopPropagation();
        if (opt.classList.contains('giencoder-select-option-disabled')) return;
        options.forEach(function (o) {
          o.classList.remove('giencoder-select-option-selected');
          o.setAttribute('aria-selected', 'false');
        });
        opt.classList.add('giencoder-select-option-selected');
        opt.setAttribute('aria-selected', 'true');
        var textEl = view.querySelector('.giencoder-select-view-text');
        if (textEl) textEl.textContent = opt.textContent;
        close();
      });
    });
  });

  document.addEventListener('click', function (ev) {
    document.querySelectorAll('.giencoder-select').forEach(function (sel) {
      var popup = sel.querySelector('.giencoder-select-popup');
      if (!popup) return;
      if (!sel.contains(ev.target)) {
        closePopup(popup);
        var v = sel.querySelector('.giencoder-select-view');
        if (v) v.setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* ─────────── DatePicker 日期选择器交互 ───────────
   * 1. 点击触发框：展开/收起日历面板（display + 过渡动画，同步 aria-expanded）
   * 2. 点击日期格：单日变体互斥选中（giencoder-calendar-cell-selected）+ 回显触发框 + 收起
   * 3. 范围变体：第一击记开始、第二击记结束，回显 "开始 ~ 结束"（不做完整区间逻辑）
   * 4. 跨月格（-other）与空格：忽略，不参与选中与回显
   * 5. 月份导航按钮：切换面板月份标题（演示）
   * 6. 点击面板外部：收起
   */
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }

  $$('.giencoder-date-picker').forEach(function (picker) {
    var trigger = $('.giencoder-input-wrapper', picker);
    var popup = $('.giencoder-date-picker-popup', picker);
    var input = trigger ? $('.giencoder-input', trigger) : null;
    if (!trigger || !popup || !input) return;

    var isRange = picker.getAttribute('data-variant') === 'range';
    var range = { start: null, end: null };

    function setOpen(open) {
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        popup.style.display = 'block';
        requestAnimationFrame(function () {
          if (popup.isConnected) popup.classList.add('giencoder-panel-open');
        });
      } else {
        popup.classList.remove('giencoder-panel-open');
        setTimeout(function () {
          if (popup.isConnected && !popup.classList.contains('giencoder-panel-open')) {
            popup.style.display = 'none';
          }
        }, 200);
      }
    }

    // 1) 触发框点击：展开/收起
    trigger.addEventListener('click', function (ev) {
      ev.stopPropagation();
      setOpen(!popup.classList.contains('giencoder-panel-open'));
    });

    // 6) 点击面板外部收起
    document.addEventListener('click', function (ev) {
      if (!picker.contains(ev.target) && popup.classList.contains('giencoder-panel-open')) setOpen(false);
    });

    // 5) 月份导航：标题加减一个月
    $$('.giencoder-calendar-nav', picker).forEach(function (nav) {
      nav.addEventListener('click', function () {
        var back = nav.getAttribute('aria-label') === '上个月';
        $$('.giencoder-calendar', picker).forEach(function (cal) {
          var title = $('.giencoder-calendar-title', cal);
          if (!title) return;
          var m = title.textContent.match(/(\d{4})年(\d{1,2})月/);
          if (!m) return;
          var y = +m[1], mo = +m[2] + (back ? -1 : 1);
          if (mo < 1) { mo = 12; y -= 1; }
          if (mo > 12) { mo = 1; y += 1; }
          title.textContent = y + '年' + mo + '月';
        });
      });
    });

    // 2) 3) 4) 日期格点击
    $$('.giencoder-calendar-cell', picker).forEach(function (cell) {
      if (cell.classList.contains('giencoder-calendar-cell-empty')) return;
      cell.addEventListener('click', function (ev) {
        ev.stopPropagation();
        if (cell.classList.contains('giencoder-calendar-cell-other')) return;
        var day = parseInt(cell.textContent, 10);
        if (isNaN(day)) return;
        var cal = cell.closest('.giencoder-calendar');
        var title = cal ? $('.giencoder-calendar-title', cal) : null;
        var m = title ? title.textContent.match(/(\d{4})年(\d{1,2})月/) : null;
        var date = (m ? +m[1] : 2026) + '/' + pad2(m ? +m[2] : 8) + '/' + pad2(day);

        if (isRange) {
          if (!range.start || (range.start && range.end)) { range.start = date; range.end = null; }
          else { range.end = date; }
          input.value = range.end ? range.start + ' ~ ' + range.end : range.start;
          return;
        }

        $$('.giencoder-calendar-cell', picker).forEach(function (c) {
          c.classList.remove('giencoder-calendar-cell-selected');
        });
        cell.classList.add('giencoder-calendar-cell-selected');
        input.value = date;
        setOpen(false);
      });
    });
  });
})();
