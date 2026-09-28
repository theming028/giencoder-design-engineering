# -*- coding: utf-8 -*-
"""第 49 轮补丁 e：浏览态彻底免疫 r35 的两栏布局记忆
   （实测 {swapped:true, collapsed:true} 下开侧栏 → 位置被 row-reverse 翻过来、
    且 .td-right-inner 被 display:none 整块隐藏 —— 因为 r35 的规则在我这条规则之后、同权重会压过来）
   幂等。"""
import sys

F = 'pages/task-detail.html'
s = open(F, encoding='utf-8').read()
orig = len(s)

old = '''      .td-root.is-browse { flex-direction: row; }
      .td-root.is-browse .td-right { width: var(--td-browse-right-w, 480px); }
'''
new = '''      .td-root.is-browse,
      .td-root.is-browse.is-swapped { flex-direction: row; }
      .td-root.is-browse .td-right { width: var(--td-browse-right-w, 480px); }
      /* r35 的折叠态会整块隐藏会话内容、并亮出 48px 折叠条 —— 浏览态必须复位，
         否则「上次把右栏拖窄成窄条」的记忆会让 AI 会话栏变成空白。 */
      .td-root.is-browse .td-right-inner,
      .td-root.is-browse.is-collapsed .td-right-inner { display: flex; }
      .td-root.is-browse .td-collapsed,
      .td-root.is-browse.is-collapsed .td-collapsed { display: none; }
'''
if new in s:
    print('已应用（幂等）')
    sys.exit(0)
if s.count(old) != 1:
    print('!! 锚点命中 %d 次' % s.count(old))
    sys.exit(1)
s = s.replace(old, new)

assert s.count('.td-root.is-browse.is-swapped { flex-direction: row; }') == 1
assert s.count('.td-root.is-browse.is-collapsed .td-right-inner { display: flex; }') == 1
assert s.count('.td-root.is-browse.is-collapsed .td-collapsed { display: none; }') == 1
assert s.count('<style') == 3 and s.count('</style>') == 3 and s.count('</aside>') == 4

open(F, 'w', encoding='utf-8').write(s)
print('OK  %d → %d 字节' % (orig, len(s)))
