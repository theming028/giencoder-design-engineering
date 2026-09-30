# -*- coding: utf-8 -*-
"""圆角半径拟合 + 边缘像素取样。"""
import os
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A = np.asarray(Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png'))
               .convert('RGB')).astype(np.int16)


def hx(c):
    return '#%02X%02X%02X' % (int(c[0]), int(c[1]), int(c[2]))


def fit_radius(x0, y0, x1, y1, color, tol, name):
    """在 [x0,x1]x[y0,y1] 左上角内，找每行目标色的左缘，拟合半径。"""
    pts = []
    for y in range(y0, y1):
        xs = np.where(np.abs(A[y, x0:x1] - np.array(color)).sum(axis=1) <= tol)[0]
        if len(xs):
            pts.append((y - y0, xs.min() + (x0 - x0)))
    if not pts:
        print('  %-22s 未命中' % name)
        return
    # 左边界 x(y) = r - sqrt(r^2-(r-y)^2)，用最小二乘扫 r
    best = None
    for r10 in range(4, 260):
        r = r10 / 10.0
        err = 0.0
        n = 0
        for dy, dx in pts:
            if dy > r:
                continue
            pred = r - (r * r - (r - dy) ** 2) ** 0.5
            err += (pred - dx) ** 2
            n += 1
        if n >= 4:
            e = err / n
            if best is None or e < best[0]:
                best = (e, r)
    print('  %-22s 拟合半径 = %.2f design px  (rmse=%.2f, 采样 %d 行)' % (
        name, best[1] / 2.0, best[0] ** 0.5 / 2.0, len(pts)))


print('=== 圆角拟合（design px = device/2）===')
FILL = (248, 249, 250)
fit_radius(0, 264, 60, 290, FILL, 14, '卡片 左上')
fit_radius(0, 160, 60, 186, (229, 229, 229), 60, '搜索框 左上（边框色）')
fit_radius(1278, 160, 1340, 186, (229, 229, 229), 60, '下拉 左上（边框色）')
fit_radius(1460, 24, 1520, 50, (255, 236, 232), 24, '清空按钮 左上（粉底）')
fit_radius(1508, 317, 1545, 344, (255, 255, 255), 14, '行内图标按钮 左上（白底）')
fit_radius(1413, 610, 1450, 637, (255, 255, 255), 14, '行3文字按钮 左上（白底）')

print('\n=== 行1 默认图标按钮 左缘像素（y=345）===')
print('   ', ' '.join('%d:%s' % (x, hx(A[345, x])) for x in range(1505, 1518)))
print('   上缘像素（x=1541）')
print('   ', ' '.join('%d:%s' % (y, hx(A[y, 1541])) for y in range(312, 324)))

print('\n=== 行3 文字按钮 左缘像素（y=642）===')
print('   ', ' '.join('%d:%s' % (x, hx(A[642, x])) for x in range(1410, 1424)))
print('   上缘像素（x=1465）')
print('   ', ' '.join('%d:%s' % (y, hx(A[y, 1465])) for y in range(605, 617)))

print('\n=== 搜索框 左缘像素（y=192）===')
print('   ', ' '.join('%d:%s' % (x, hx(A[192, x])) for x in range(0, 8)))
print('   上缘像素（x=600）')
print('   ', ' '.join('%d:%s' % (y, hx(A[y, 600])) for y in range(156, 168)))
