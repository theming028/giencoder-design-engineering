
      /* 详情页：Esc 返回任务看板（全屏态下先退出全屏，第 26 轮第 5 项） */
      document.addEventListener('keydown', function (ev) {
        if (ev.key !== 'Escape') return;
        var tag = (ev.target && ev.target.tagName) || '';
        if (tag === 'TEXTAREA' || tag === 'INPUT') return;
        /* ★ 第 30 轮第 1 项：图片蒙层预览优先级最高 —— 打开时 Esc 只关预览，不继续往下走。
           预览侧监听自定义事件 td:close-image-preview（见 bindDescImagePreview）。 */
        if (document.documentElement.hasAttribute('data-td-img-preview')) {
          document.dispatchEvent(new CustomEvent('td:close-image-preview'));
          return;
        }
        /* ★ 第 28 轮第 4 项：对话框弹层打开时，Esc 先关弹层而不是跳回看板。
           弹层侧监听自定义事件 td:close-popovers（见 bindDetail 里的对话框绑定）。 */
        if (document.documentElement.hasAttribute('data-td-pop-open')) {
          document.dispatchEvent(new CustomEvent('td:close-popovers'));
          return;
        }
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
    