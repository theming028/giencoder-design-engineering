# -*- coding: utf-8 -*-
"""r92 ①：在真实顶栏截图里量点阵 —— 点色 / 点距 / 竖直裁切是否落在整格上。"""
from PIL import Image

im = Image.open('mg-work/r92/raw/web-hdr-r92-base.png').convert('RGB')
W, H = im.size
DOT = (221, 227, 235)


def is_dot(p):
    return abs(p[0] - DOT[0]) + abs(p[1] - DOT[1]) + abs(p[2] - DOT[2]) < 24


print('顶栏截图 %dx%d；图片右对齐 ⇒ 图片左原点 x = %d' % (W, H, W - 1580))
print('点阵首个 x（源图 1067）⇒ 顶栏 x = %d' % (W - 1580 + 1067))

col = W - 3
runs = []
cur, start = None, 0
for y in range(H):
    d = is_dot(im.getpixel((col, y)))
    if cur is None:
        cur, start = d, y
    elif d != cur:
        runs.append((cur, y - start))
        cur, start = d, y
runs.append((cur, H - start))
print('\n竖直游程 @x=%d：%s' % (col, [(('DOT' if k else 'gap'), v) for k, v in runs]))

row = H // 2
runs2 = []
cur, start = None, 0
for x in range(W):
    d = is_dot(im.getpixel((x, row)))
    if cur is None:
        cur, start = d, x
    elif d != cur:
        runs2.append((cur, x - start))
        cur, start = d, x
runs2.append((cur, W - start))
ds = [v for k, v in runs2 if k]
gs = [v for k, v in runs2 if not k]
print('\n水平游程 @y=%d：前 6 段 %s' % (row, [(('DOT' if k else 'gap'), v) for k, v in runs2[:6]]))
if ds:
    print('点宽 min/max = %d/%d' % (min(ds), max(ds)))
if gs:
    print('间隙 min/max = %d/%d（含左侧空白 %d）' % (min(gs), max(gs), max(gs)))
print('\n点色实测 =', im.getpixel((W - 3, 3)))
