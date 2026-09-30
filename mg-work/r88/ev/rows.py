# -*- coding: utf-8 -*-
"""逐行/逐元素量测：文字 ink bbox、字形投影（推字号）。"""
import os
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A = np.asarray(Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png'))
               .convert('RGB')).astype(np.int16)
H, W, _ = A.shape
WHITE = np.array([255, 255, 255])
FILL = np.array([248, 249, 250])
EE = np.array([238, 238, 238])


def ink(x0, y0, x1, y1, bg=WHITE, tol=40):
    sub = A[y0:y1, x0:x1]
    d = np.abs(sub - bg).sum(axis=2)
    m = d > tol
    ys = np.where(m.any(axis=1))[0]
    xs = np.where(m.any(axis=0))[0]
    if not len(ys):
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(),
            xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)


def glyphs(x0, y0, x1, y1, bg=WHITE, tol=40, gap=3):
    sub = A[y0:y1, x0:x1]
    d = (np.abs(sub - bg).sum(axis=2) > tol)
    col = d.any(axis=0)
    segs = []
    s = None
    blank = 0
    for i, v in enumerate(col):
        if v:
            if s is None:
                s = i
            blank = 0
        else:
            if s is not None:
                blank += 1
                if blank >= gap:
                    segs.append((x0 + s, x0 + i - blank))
                    s = None
    if s is not None:
        segs.append((x0 + s, x0 + len(col) - 1))
    return [(a, b, b - a + 1) for a, b in segs]


def line(t):
    print('  · %s' % t)


print('=== 卡片/行结构 ===')
for y in range(260, H):
    row = A[y]
    n_fill = int((np.abs(row - FILL).sum(axis=1) < 20).sum())
    if n_fill < W * 0.5:
        print('  y=%d  非 #F8F9FA 占比高（fill像素 %d）' % (y, n_fill))

print()
print('=== 标题 / 副标题 字形投影 ===')
print('  标题 整块 bbox :', ink(0, 0, 600, 58))
print('  标题 字形段    :', glyphs(0, 0, 600, 58))
print('  副标题 bbox    :', ink(0, 60, 900, 110))
print('  副标题 前6字形 :', glyphs(0, 60, 900, 110)[:6])

print()
print('=== 行内文字 / 按钮 ===')
bands = [(266, 418), (420, 566), (568, 714), (716, 862), (864, 1010), (1012, 1158), (1160, 1314)]
for i, (a, b) in enumerate(bands, 1):
    t = ink(0, a, 1380, b, bg=FILL, tol=40)
    m = ink(0, a, 1380, b, bg=FILL, tol=40)
    print('  行%d  band y %d..%d (高%d)' % (i, a, b, b - a + 1))
    # 标题（上半）与副标题（下半）：先做纵向投影找两段
    sub = A[a:b, 0:1380]
    d = (np.abs(sub - FILL).sum(axis=2) > 40)
    rowsum = d.sum(axis=1)
    nz = np.where(rowsum > 0)[0]
    if len(nz):
        # 分组
        gs = []
        s = nz[0]
        p = nz[0]
        for r in nz[1:]:
            if r - p > 2:
                gs.append((s, p)); s = r
            p = r
        gs.append((s, p))
        for g in gs:
            bb = ink(0, a + g[0], 1380, a + g[1] + 1, bg=FILL)
            print('      纵段 rel %3d..%-3d → bbox x %d..%d (W %d)  H %d' % (g[0], g[1], bb[0], bb[2], bb[4], bb[5]))
    bl = ink(1400, a, 1680, b, bg=FILL)
    print('      右侧控件 bbox x %s..%s y %s..%s  (%sx%s)' % (bl[0], bl[2], bl[1], bl[3], bl[4], bl[5]) if bl else '      右侧无')
