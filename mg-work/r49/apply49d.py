# -*- coding: utf-8 -*-
"""第 49 轮补丁 d：修 apply49c 的转义错误 —— 树图标在 JS 字符串数组里，
   属性引号必须是转义形式 \\" ，否则整页 bundle 语法错误。
   幂等。"""
import sys

F = 'pages/task-detail.html'
s = open(F, encoding='utf-8').read()
orig = len(s)

bad = '<svg class="td-bf-ico" '
good = '<svg class=\\"td-bf-ico\\" '
assert bad not in s or True

n = s.count(bad)
if n == 0:
    print('已修复（幂等）')
    sys.exit(0)
if n != 28:
    print('!! 待修复数量 = %d（期望 28）' % n)
    sys.exit(1)
s = s.replace(bad, good)

assert s.count(good) == 28, s.count(good)
assert bad not in s
open(F, 'w', encoding='utf-8').write(s)
print('修复 %d 处，%d → %d 字节' % (n, orig, len(s)))
print('OK')
