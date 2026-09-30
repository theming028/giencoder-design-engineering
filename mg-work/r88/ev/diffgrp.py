# -*- coding: utf-8 -*-
"""两张同态元素截图（840×658）的逐行分组 diff —— 证「只改了该改的地方」。

用法：python diffgrp.py A.png B.png [阈值]
"""
import os, sys
import numpy as np
from PIL import Image

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'raw')
A = Image.open(os.path.join(D, sys.argv[1])).convert('RGB')
B = Image.open(os.path.join(D, sys.argv[2])).convert('RGB')
THR = int(sys.argv[3]) if len(sys.argv) > 3 else 8

a = np.asarray(A).astype(int)
b = np.asarray(B).astype(int)
m = (np.abs(a - b).max(axis=2) > THR)

print('A=%s  B=%s  阈值>%d  size=%s' % (sys.argv[1], sys.argv[2], THR, A.size))
print('差异像素 %d / %d = %.3f%%' % (m.sum(), m.size // 3, 100.0 * m.sum() / (m.size // 3)))
if m.sum() == 0:
    sys.exit(0)

rows = np.where(m.any(axis=1))[0]
# 连续行分组
groups = []
s = prev = rows[0]
for y in rows[1:]:
    if y == prev + 1:
        prev = y
    else:
        groups.append((s, prev)); s = prev = y
groups.append((s, prev))

print('共 %d 个差异行组：' % len(groups))
for y0, y1 in groups:
    sub = m[y0:y1 + 1]
    cols = np.where(sub.any(axis=0))[0]
    # 列也分组
    cs = []
    s2 = p2 = cols[0]
    for x in cols[1:]:
        if x == p2 + 1:
            p2 = x
        else:
            cs.append((s2, p2)); s2 = p2 = x
    cs.append((s2, p2))
    colstr = ','.join('%d-%d' % c for c in cs[:8]) + (' …' if len(cs) > 8 else '')
    print('  y %4d..%-4d (h=%2d)  n=%-6d  x: %s' % (y0, y1, y1 - y0 + 1, sub.sum(), colstr))
