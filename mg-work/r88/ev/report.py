# -*- coding: utf-8 -*-
"""「已归档任务」设计稿完整量测报告（device px，scale=2 ⇒ 设计 px = /2）。"""
import os
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A = np.asarray(Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png'))
               .convert('RGB')).astype(np.int16)
H, W, _ = A.shape
FILL = np.array([248, 249, 250])


def hx(c):
    return '#%02X%02X%02X' % (int(c[0]), int(c[1]), int(c[2]))


def runs(line, bg, tol):
    segs = []
    s = None
    for i in range(len(line)):
        nz = np.abs(line[i] - bg).sum() > tol
        if nz and s is None:
            s = i
        elif not nz and s is not None:
            segs.append((s, i - 1, hx(line[(s + i - 1) // 2])))
            s = None
    if s is not None:
        segs.append((s, len(line) - 1, hx(line[(s + len(line) - 1) // 2])))
    return segs


def hr(y, x0, x1, bg, tol):
    print('  h y=%-4d x%d..%d tol=%d' % (y, x0, x1, tol))
    for a, b, c in runs(A[y, x0:x1], bg, tol):
        print('      %4d..%-4d (%3d) %s' % (x0 + a, x0 + b, b - a + 1, c))


def vr(x, y0, y1, bg, tol):
    print('  v x=%-4d y%d..%d tol=%d' % (x, y0, y1, tol))
    for a, b, c in runs(A[y0:y1, x], bg, tol):
        print('      %4d..%-4d (%3d) %s' % (y0 + a, y0 + b, b - a + 1, c))


print('########## 1. 行1 默认态图标按钮（白底 + #F2F2F2 边）')
hr(345, 1490, 1680, FILL, 12)
vr(1541, 320, 375, FILL, 12)

print('\n########## 2. 行3 hover 态文字按钮')
hr(642, 1400, 1680, FILL, 12)
vr(1465, 600, 690, FILL, 12)

print('\n########## 3. 清空归档任务按钮（#FFECE8 底）')
PINK = np.array([255, 236, 232])
hr(60, 1400, 1680, PINK, 30)
sub = A[24:96, 1464:1680]
m = np.abs(sub - PINK).sum(axis=2) > 60
ys, xs = np.where(m)
print('   文字 ink: x %d..%d (W %d)  y %d..%d (H %d)' % (
    1464 + xs.min(), 1464 + xs.max(), xs.max() - xs.min() + 1,
    24 + ys.min(), 24 + ys.max(), ys.max() - ys.min() + 1))

print('\n########## 4. 搜索框（icon + placeholder）')
hr(192, 0, 1270, np.array([255, 255, 255]), 40)

print('\n########## 5. 全部项目 下拉（icon + 文字 + 箭头）')
hr(192, 1280, 1680, np.array([255, 255, 255]), 40)

print('\n########## 6. 行标题字号（字形段 → 步进）')
for tag, y0, y1, x1 in [('行2 任务创建方式改写', 455, 490, 400), ('行6 自动任务手动触发对话创建', 1046, 1082, 420),
                        ('行7 Git Worktree…', 1194, 1230, 440)]:
    sub = A[y0:y1, 30:x1]
    d = (np.abs(sub - FILL).sum(axis=2) > 40)
    col = d.any(axis=0)
    segs = []
    s = None
    blank = 0
    for i, v in enumerate(col):
        if v:
            if s is None:
                s = i
            blank = 0
        elif s is not None:
            blank += 1
            if blank >= 2:
                segs.append((30 + s, 30 + i - blank)); s = None
    if s is not None:
        segs.append((30 + s, 30 + x1 - 30 - 1))
    print('  %s : %d 段  前 8: %s' % (tag, len(segs), segs[:8]))
    if len(segs) > 3:
        st = [(segs[i + 1][0] - segs[i][0]) for i in range(min(6, len(segs) - 1))]
        print('      步进 = %s' % st)

print('\n########## 7. 副标题（meta）结构 —— 行2 y 505..535')
sub = A[505:535, 0:520]
d = (np.abs(sub - FILL).sum(axis=2) > 40)
col = d.any(axis=0)
segs = []
s = None
blank = 0
for i, v in enumerate(col):
    if v:
        if s is None:
            s = i
        blank = 0
    elif s is not None:
        blank += 1
        if blank >= 4:
            segs.append((s, i - blank)); s = None
if s is not None:
    segs.append((s, 519))
print('  分组段（gap>=4）:')
for a, b in segs:
    bb = A[505:535, a:b + 1]
    m2 = np.abs(bb - FILL).sum(axis=2) > 40
    yy = np.where(m2.any(axis=1))[0]
    print('     x %3d..%-3d (W %3d)  y高 %d..%d (H %d)' % (a, b, b - a + 1, 505 + yy.min(), 505 + yy.max(), yy.max() - yy.min() + 1))

print('\n########## 8. 行3 标题行文字颜色')
for tag, y0, y1, x0, x1 in [('行2 标题', 455, 490, 41, 262), ('行2 副标题', 505, 535, 41, 500)]:
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    dk = sub[sub.sum(axis=1) < 500]
    if len(dk):
        print('  %s 最暗均值 %s  最暗 %s' % (tag, hx(dk.mean(axis=0)), hx(dk[dk.sum(axis=1).argmin()])))
