# -*- coding: utf-8 -*-
"""设计稿像素结构扫描：色带 / 分隔线 / 控件矩形。"""
import os
import collections
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = os.path.join(REPO, 'mg-work', 'r88', 'raw')
im = Image.open(os.path.join(R, 'arch@2x_rgb.png')).convert('RGB')
A = np.asarray(im).astype(np.int16)
H, W, _ = A.shape
print('size WxH = %dx%d  (若 scale=2 ⇒ 设计 %.1f x %.1f)' % (W, H, W / 2.0, H / 2.0))

# ---- 1. 主色 ----
flat = A.reshape(-1, 3)
cnt = collections.Counter(map(tuple, flat[::7]))
print('\n--- 主色 top14 ---')
for c, n in cnt.most_common(14):
    print('  #%02X%02X%02X  %8d  %.2f%%' % (c[0], c[1], c[2], n * 7, 100.0 * n * 7 / flat.shape[0]))

# ---- 2. 每行「与上一行不同像素数」找水平带边界 ----
d = (np.abs(A[1:] - A[:-1]).max(axis=2) > 6).sum(axis=1)
rows = [(y + 1, int(v)) for y, v in enumerate(d) if v > W * 0.35]
print('\n--- 水平带边界（变化>35%%宽度）---')
for y, v in rows:
    print('  y=%4d  changed=%d' % (y, v))

# ---- 3. 每条扫描线的色段（run-length） ----
def runs(y, minlen=6):
    line = A[y]
    segs = []
    s = 0
    for x in range(1, W + 1):
        if x == W or tuple(line[x]) != tuple(line[s]):
            if x - s >= minlen:
                c = line[s]
                segs.append((s, x - 1, '#%02X%02X%02X' % (c[0], c[1], c[2])))
            s = x
    return segs

for y in (int(v) for v in os.environ.get('SCAN_Y', '20 60 100 140 200 240 300 380 420').split()):
    if y >= H:
        continue
    print('\n--- y=%d ---' % y)
    for a, b, c in runs(y):
        print('   x %4d..%-4d (%3d)  %s' % (a, b, b - a + 1, c))

# ---- 4. 竖直扫描（找左右边界） ----
def vruns(x, minlen=6):
    col = A[:, x]
    segs = []
    s = 0
    for y in range(1, H + 1):
        if y == H or tuple(col[y]) != tuple(col[s]):
            if y - s >= minlen:
                c = col[s]
                segs.append((s, y - 1, '#%02X%02X%02X' % (c[0], c[1], c[2])))
            s = y
    return segs

for x in (4, 20, 200, 900, 1300, 1660):
    print('\n--- x=%d ---' % x)
    for a, b, c in vruns(x):
        print('   y %4d..%-4d (%3d)  %s' % (a, b, b - a + 1, c))
