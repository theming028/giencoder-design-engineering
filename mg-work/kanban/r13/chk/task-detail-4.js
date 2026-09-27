
      /* 详情页：Esc 返回任务看板 */
      document.addEventListener('keydown', function (ev) {
        if (ev.key !== 'Escape') return;
        var tag = (ev.target && ev.target.tagName) || '';
        if (tag === 'TEXTAREA' || tag === 'INPUT') return;
        location.href = 'kanban.html';
      });
    