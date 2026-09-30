# -*- coding: utf-8 -*-
"""精细边缘扫描：非白/非底色像素的精确 run（minlen=1）。

用法：
  python edges.py h <y1> [y2 ...]        # 水平线扫描
  python edges.py v <x1> [x2 ...]        # 垂直线扫描
  python edges.py rect <x0> <y0> <x1> <y1>   # 区域内非底色像素的外接盒
"""
import os
import sys
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')).convert('RGB')
A = np.asarray(im).astype(np.int16)
H, W, _ = A.shape


def hx(c):
    return '#%02X%02X%02X' % (int(c[0]), int(c[1]), int(c[2]))


def hline(y, tol=6, minlen=1):
    line = A[y]
    out = []
    s = None
    for x in range(W):
        d = abs(int(line[x][0]) - 255) + abs(int(line[x][1]) - 255) + abs(int(line[x][2]) - 255)
        nz = d > tol
        if nz and s is None:
            s = x
        elif not nz and s is not None:
            if x - s >= minlen:
                out.append((s, x - 1, hx(line[(s + x - 1) // 2])))
            s = None
    if s is not None:
        out.append((s, W - 1, hx(line[(s + W - 1) // 2])))
    return out


def vline(x, tol=6, minlen=1):
    col = A[:, x]
    out = []
    s = None
    for y in range(H):
        d = abs(int(col[y][0]) - 255) + abs(int(col[y][1]) - 255) + abs(int(col[y][2]) - 255)
        nz = d > tol
        if nz and s is None:
            s = y
        elif not nz and s is not None:
            if y - s >= minlen:
                out.append((s, y - 1, hx(col[(s + y - 1) // 2])))
            s = None
    if s is not None:
        out.append((s, H - 1, hx(col[(s + H - 1) // 2])))
    return out


def show(segs, tag):
    print('--- %s ---' % tag)
    for a, b, c in segs:
        print('   %4d..%-4d  (%3d)  %s' % (a, b, b - a + 1, c))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'h':
        for y in (int(v) for v in sys.argv[2:]):
            show(hline(y), 'y=%d 非白段' % y)
    elif mode == 'v':
        for x in (int(v) for v in sys.argv[2:]):
            show(vline(x), 'x=%d 非白段' % x)
    else:
        x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
        sub = A[y0:y1, x0:x1]
        d = (np.abs(sub - np.array([255, 255, 255])).sum(axis=2) > 6)
        ys = np.where(d.any(axis=1))[0]
        xs = np.where(d.any(axis=0))[0]
        print('rect(%d,%d)-(%d,%d)  非白外接盒: x %d..%d  y %d..%d  (W=%d H=%d)' % (
            x0, y0, x1, y1, x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(),
            xs.max() - xs.min() + 1, ys.max() - ys.min() + 1))
