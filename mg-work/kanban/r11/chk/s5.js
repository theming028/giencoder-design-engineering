
      /* 看板切换：任务看板 ↔ 需求看板 */
      document.addEventListener('click', function (ev) {
        var tab = ev.target.closest && ev.target.closest('.kb-radio-btn[data-goto]');
        if (tab && !tab.classList.contains('is-on')) {
          var g = tab.getAttribute('data-goto');
          if (g) location.href = g;
        }
      });
    