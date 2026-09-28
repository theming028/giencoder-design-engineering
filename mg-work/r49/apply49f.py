# -*- coding: utf-8 -*-
"""第 49 轮补丁 f：激活行内容被高亮盖住
   原因：.td-bf::before 是**绝对定位**元素，按 CSS 绘制顺序（positioned 后于 in-flow）会盖在
         同级的图标/文字之上 → 截图实测激活行「只有蓝底、无文字」。
   修法：把行内容（箭头/图标/文件名）提到 z-index:1（正 z-index 最后绘制）。
   幂等。"""
import sys

F = 'pages/task-detail.html'
s = open(F, encoding='utf-8').read()
orig = len(s)

old = '      .td-bf-name { overflow: hidden; text-overflow: ellipsis; }\n'
new = ('      .td-bf-name { overflow: hidden; text-overflow: ellipsis; }\n'
       '      /* 激活高亮是绝对定位的 ::before —— 按绘制顺序会盖住同级的图标/文字，\n'
       '         必须把行内容提到正 z-index 层（实测：不提升则激活行只剩蓝底） */\n'
       '      .td-bf-arrow, .td-bf-ico, .td-bf-name { position: relative; z-index: 1; }\n')

if new in s:
    print('已应用（幂等）')
    sys.exit(0)
if s.count(old) != 1:
    print('!! 锚点命中 %d 次' % s.count(old))
    sys.exit(1)
s = s.replace(old, new)

assert s.count('.td-bf-arrow, .td-bf-ico, .td-bf-name { position: relative; z-index: 1; }') == 1
assert s.count('<style') == 3 and s.count('</style>') == 3 and s.count('</aside>') == 4

open(F, 'w', encoding='utf-8').write(s)
print('OK  %d → %d 字节' % (orig, len(s)))
