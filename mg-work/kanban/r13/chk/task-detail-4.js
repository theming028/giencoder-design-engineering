
      /* 详情页：Esc 返回任务看板（全屏态下先退出全屏，第 26 轮第 5 项） */
      document.addEventListener('keydown', function (ev) {
        if (ev.key !== 'Escape') return;
        var tag = (ev.target && ev.target.tagName) || '';
        if (tag === 'TEXTAREA' || tag === 'INPUT') return;
        var fsRoot = document.querySelector('.td-root.is-fullscreen');
        if (fsRoot) {
          fsRoot.classList.remove('is-fullscreen');
          var fb = fsRoot.querySelector('[data-td-fullscreen]');
          if (fb) {
            fb.setAttribute('aria-label', '全屏');
            fb.setAttribute('title', '全屏');
            fb.setAttribute('aria-pressed', 'false');
          }
          return;
        }
        location.href = 'kanban.html';
      });
    