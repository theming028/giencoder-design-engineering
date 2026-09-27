
      /* 看板切换：任务看板 ↔ 需求看板 */
      document.addEventListener('click', function (ev) {
        var tab = ev.target.closest && ev.target.closest('.kb-radio-btn[data-goto]');
        if (tab && !tab.classList.contains('is-on')) {
          var g = tab.getAttribute('data-goto');
          if (g) location.href = g;
        }
      });
      /* 任务卡片：进入任务详情页（转派/执行等卡内按钮不触发跳转） */
      document.addEventListener('click', function (ev) {
        var card = ev.target.closest && ev.target.closest('.kb-card');
        if (!card) return;
        if (card.classList.contains('is-dashed')) return;
        if (ev.target.closest('button, a, input, textarea, select, [data-nogo]')) return;
        location.href = 'task-detail.html';
      });
    