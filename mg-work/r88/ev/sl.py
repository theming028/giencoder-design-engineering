# -*- coding: utf-8 -*-
"""按指定底色做 run 扫描：python sl.py <h|v> <bghex> <tol> <idx...>"""
import os
import sys
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A = np.asarray(Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png'))
               .convert('RGB')).astype(np.int16)
H, W, _ = A.shape

mode = sys.argv[1]
bg = np.array([int(sys.argv[2][i:i + 2], 16) for i in (1, 3, 5)])
tol = int(sys.argv[3])


def hx(c):
    return '#%02X%02X%02X' % (int(c[0]), int(c[1]), int(c[2]))


for v in (int(x) for x in sys.argv[4:]):
    line = A[v] if mode == 'h' else A[:, v]
    n = W if mode == 'h' else H
    segs = []
    s = None
    for i in range(n):
        nz = np.abs(line[i] - bg).sum() > tol
        if nz and s is None:
            s = i
        elif not nz and s is not None:
            segs.append((s, i - 1, hx(line[(s + i - 1) // 2])))
            s = None
    if s is not None:
        segs.append((s, n - 1, hx(line[(s + n - 1) // 2])))
    tag = ('y=%d' % v) if mode == 'h' else ('x=%d' % v)
    print('--- %s  (bg=%s tol=%d) 共 %d 段 ---' % (tag, sys.argv[2], tol, len(segs)))
    for a, b, c in segs:
        print('   %4d..%-4d  (%3d)  %s' % (a, b, b - a + 1, c))
