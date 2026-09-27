
      /* 背景：顶栏页签是外壳的公共模块，外壳自己的导航函数是：
           navigate(route){ if (protocol === 'file:') { location.href = 路由映射[route] }
                            else { location.hash = '#/route' } }
         也就是说**只有用 file:// 直接打开时才真的跳页**；用本地服务器（http://）打开时
         只改 hash，而外壳没有 hashchange 监听 → 点页签不跳转、也不重渲染，表现为「点了没反应」。
         实测 9 个页面（base/dev/kanban/req-kanban/task-detail/avatar/automation/skills/settings）全部如此。

         修复：在 document 捕获阶段接管点击（早于 React 的根监听，且不依赖 React 是否已挂载），
         按外壳自己的 route → 文件名映射直接跳转。stopPropagation 顺带阻止外壳自己那个
         「只改 hash」的 onClick，避免出现 `base.html#/dev` 这种半吊子状态。

         「当前分组」判定：优先用 DOM（aria-selected="true" 的页签），但**必须与实际文件名自洽** ——
         dev.html 上外壳把「基础工作台」标成了选中态（第 10 轮遗留的高亮错位），若只信 DOM，
         该页两个页签都会变成空操作。故：DOM 与文件一致才采信 DOM，否则回落到文件名分组。 */
      (function () {
        var FILE = { base: 'base.html', dev: 'dev.html' };
        var DEV_PAGES = { 'dev.html': 1, 'kanban.html': 1, 'req-kanban.html': 1, 'task-detail.html': 1 };
        var here = location.pathname.split('/').pop() || '';
        var fileGroup = DEV_PAGES[here] ? 'dev' : 'base';
        function groupOf() {
          var tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
          var cur = tl && tl.querySelector('[data-tab][aria-selected="true"]');
          var dom = cur && cur.getAttribute('data-tab');
          if (dom && FILE[dom] === here) return dom;
          return fileGroup;
        }
        document.addEventListener('click', function (e) {
          var t = e.target;
          var btn = t && t.closest ? t.closest('[role="tablist"][aria-label="工作台切换"] [data-tab]') : null;
          if (!btn) return;
          e.preventDefault();
          e.stopPropagation();
          var n = btn.getAttribute('data-tab');
          if (!n || n === groupOf() || !FILE[n]) return;
          location.href = FILE[n];
        }, true);
      })();
    