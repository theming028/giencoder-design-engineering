
      /* 看板切换：任务看板 ↔ 需求看板 */
      document.addEventListener('click', function (ev) {
        var tab = ev.target.closest && ev.target.closest('.kb-radio-btn[data-goto]');
        if (tab && !tab.classList.contains('is-on')) {
          var g = tab.getAttribute('data-goto');
          if (g) location.href = g;
        }
      });
      /* r29-exec-goto：点「执行」按钮 → 进入任务详情页。
         与「点卡片进详情页」同目标；卡内其它按钮（如「转派」）仍不跳转。 */
      document.addEventListener('click', function (ev) {
        var ex = ev.target.closest && ev.target.closest('.kb-btn-exec');
        if (!ex) return;
        ev.preventDefault();
        location.href = 'task-detail.html';
      });
      /* 任务卡片：进入任务详情页（转派/执行等卡内按钮不触发跳转） */
      document.addEventListener('click', function (ev) {
        var card = ev.target.closest && ev.target.closest('.kb-card');
        if (!card) return;
        /* 第 26 轮第 8 项：虚线卡（「进行中」首卡的待确认态）也要能进详情页，
           改为「只放行带标题的真实任务卡」，占位卡依然不跳。 */
        if (!card.querySelector('.kb-card-title')) return;
        if (ev.target.closest('button, a, input, textarea, select, [data-nogo]')) return;
        location.href = 'task-detail.html';
      });
    