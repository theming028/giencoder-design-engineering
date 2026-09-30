# -*- coding: utf-8 -*-
"""补充量测：按钮垂直尺寸 / 圆角 / 分隔线范围 / 图标 bbox。"""
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


def bbox(x0, y0, x1, y1, bg, tol):
    sub = A[y0:y1, x0:x1]
    m = np.abs(sub - bg).sum(axis=2) > tol
    ys = np.where(m.any(axis=1))[0]
    xs = np.where(m.any(axis=0))[0]
    if not len(ys):
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(),
            xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)


print('1) 行1 默认图标按钮 垂直范围（x=1541，tol=12）')
col = A[300:400, 1541]
for y in range(300, 400):
    d = abs(int(A[y, 1541][0]) - 248) + abs(int(A[y, 1541][1]) - 249) + abs(int(A[y, 1541][2]) - 250)
    if d > 12:
        pass
segs = []
s = None
for y in range(300, 400):
    c = A[y, 1541]
    d = abs(int(c[0]) - 248) + abs(int(c[1]) - 249) + abs(int(c[2]) - 250)
    nz = d > 12
    if nz and s is None:
        s = y
    elif not nz and s is not None:
        segs.append((s, y - 1)); s = None
print('   ', segs)

print('\n2) 行1 默认图标按钮 水平范围（y=355，按钮下半，避开图标）')
for y in (330, 355, 360):
    segs = []
    s = None
    for x in range(1480, 1680):
        c = A[y, x]
        d = abs(int(c[0]) - 248) + abs(int(c[1]) - 249) + abs(int(c[2]) - 250)
        nz = d > 12
        if nz and s is None:
            s = x
        elif not nz and s is not None:
            segs.append((s, x - 1, hx(A[y, (s + x - 1) // 2]))); s = None
    print('   y=%d %s' % (y, segs))

print('\n3) 清空按钮 顶部若干行的粉色范围（推圆角）')
PINK = np.array([255, 236, 232])
for y in range(24, 42, 2):
    xs = np.where(np.abs(A[y, 1440:1680] - PINK).sum(axis=1) < 24)[0]
    print('   y=%d 粉 x %s..%s' % (y, 1440 + xs.min() if len(xs) else '-', 1440 + xs.max() if len(xs) else '-'))

print('\n4) 卡片左上角（#F8F9FA vs #FFFFFF）逐行左缘')
for y in range(262, 284):
    xs = np.where(np.abs(A[y, 0:60] - FILL).sum(axis=1) < 12)[0]
    print('   y=%d 首个 fill x=%s' % (y, xs.min() if len(xs) else '-'))

print('\n5) 分隔线水平范围（y=418）')
row = A[418]
xs = np.where(np.abs(row - FILL).sum(axis=1) > 12)[0]
print('   非 fill x %s..%s  (共%d)  颜色 %s' % (xs.min(), xs.max(), len(xs), hx(A[418, xs[len(xs) // 2]])))

print('\n6) 图标 bbox')
print('   搜索图标 :', bbox(10, 170, 60, 215, np.array([255, 255, 255]), 30))
print('   下拉图标 :', bbox(1290, 170, 1345, 215, np.array([255, 255, 255]), 30))
print('   行2 meta图标:', bbox(38, 505, 68, 535, FILL, 30))
print('   行1 恢复图标:', bbox(1515, 325, 1565, 370, np.array([255, 255, 255]), 30))
print('   行1 删除图标:', bbox(1588, 325, 1638, 370, np.array([255, 255, 255]), 30))

print('\n7) 行1 与 行2 的右缘对齐核对')
for tag, y in [('行1', 345), ('行2', 493), ('行4', 789)]:
    segs = []
    s = None
    for x in range(1480, 1680):
        c = A[y, x]
        d = abs(int(c[0]) - 248) + abs(int(c[1]) - 249) + abs(int(c[2]) - 250)
        nz = d > 12
        if nz and s is None:
            s = x
        elif not nz and s is not None:
            segs.append((s, x - 1)); s = None
    print('   %s y=%d %s' % (tag, y, segs))
