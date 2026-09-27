# -*- coding: utf-8 -*-
# 第 29 轮第 1 项：点看板卡片上的「执行」按钮 → 进入任务详情页
#
# 现状（修前）：.kb-btn-exec 是真实的 <button class="giencoder-btn ... kb-btn-exec">，
#   而栏内已有的「点卡片进详情页」处理器显式排除按钮：
#       if (ev.target.closest('button, a, input, textarea, select, [data-nogo]')) return;
#   → 点卡片能进详情页，但点「执行」按钮没有任何反应。
# 本补丁为 .kb-btn-exec 单独加一个委托处理器，跳转目标与点卡片一致（task-detail.html）；
#   「转派」等卡内其它按钮仍保持不跳转。
#
# 作用对象：pages/kanban.html（全站只有它有「执行」按钮；
#   pages/req-kanban.html 是表格视图，没有 .kb-btn-exec 元素，只有同名 CSS 规则）。
import io, os, sys

PAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pages')
P = os.path.join(PAGES, 'kanban.html')

MARK = 'r29-exec-goto'
ANCHOR = "      /* 任务卡片：进入任务详情页（转派/执行等卡内按钮不触发跳转） */"

JS = '''      /* r29-exec-goto：点「执行」按钮 → 进入任务详情页。
         与「点卡片进详情页」同目标；卡内其它按钮（如「转派」）仍不跳转。 */
      document.addEventListener('click', function (ev) {
        var ex = ev.target.closest && ev.target.closest('.kb-btn-exec');
        if (!ex) return;
        ev.preventDefault();
        location.href = 'task-detail.html';
      });
'''

s = io.open(P, encoding='utf-8').read()

if MARK in s:
    print('[skip] 已打过补丁（幂等）')
    sys.exit(0)

assert ANCHOR in s, '找不到插入锚点，kanban.html 结构可能已变'
s = s.replace(ANCHOR, JS + ANCHOR, 1)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] 已在 pages/kanban.html 插入 .kb-btn-exec → task-detail.html 处理器')
