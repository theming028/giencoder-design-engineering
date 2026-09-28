# -*- coding: utf-8 -*-
"""第 49 轮补丁 b：.td-bf-guide 缺 left 定位 —— 3 级引导线落在 node x 34/54/74。
   设计稿实测：引导线正好穿过父级 chevron 的中心（row 相对 = 14px + 20px × 级数）。
   幂等：重复执行不改变文件。"""
import sys

F = 'pages/task-detail.html'
s = open(F, encoding='utf-8').read()
orig = len(s)

old = '      .td-bf-guide { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--td-tree-guide); }\n'
new = ('      .td-bf-guide {\n'
       '        position: absolute; top: 0; bottom: 0; width: 1px; background: var(--td-tree-guide);\n'
       '        /* 设计稿实测：引导线穿过父级 chevron 中心 —— row 相对 14px + 20px × 级数 */\n'
       '        left: calc(14px + var(--g, 0) * 20px);\n'
       '      }\n')

if s.count(new):
    print('已应用（幂等）')
    sys.exit(0)
if s.count(old) != 1:
    print('!! 锚点命中 %d 次' % s.count(old))
    sys.exit(1)
s = s.replace(old, new)

assert s.count('left: calc(14px + var(--g, 0) * 20px);') == 1, '引导线 left 未落盘'
assert s.count('.td-bf-guide') == 1, '引导线规则数异常'
assert s.count('<style') == 3 and s.count('</style>') == 3, '标签计数异常'

open(F, 'w', encoding='utf-8').write(s)
print('OK  %d → %d 字节' % (orig, len(s)))
