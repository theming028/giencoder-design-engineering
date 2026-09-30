# -*- coding: utf-8 -*-
"""圆角面积法拟合 + 顶部曲线 + hover 行底色。只读。
原理：圆角矩形「角外」面积只存在于 r×r 角箱内，A = r²(1 - π/4) ⇒ r = sqrt(A/0.21460…)
"""
import os, math
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')).convert('RGB')
W, H = im.size
px = im.load()
K = 1 - math.pi / 4.0
print('PNG = %dx%d' % (W, H))


def near(c, t, tol):
    return abs(c[0] - t[0]) + abs(c[1] - t[1]) + abs(c[2] - t[2]) <= tol


def fit_corner(x0, y0, fill, n=40, tol=14, zone=None):
    """以 (x0,y0) 为形状左上角，在 n×n 箱内数「非 fill」= 角外像素，反推 r。"""
    A = 0
    for y in range(y0, y0 + n):
        for x in range(x0, x0 + n):
            if zone and not (zone[0] <= x < zone[1]):
                continue
            if not near(px[x, y], fill, tol):
                A += 1
    r = math.sqrt(A / K) if A else 0
    return A, r, r / 2.0


print('\n=== 面积法拟合圆角（device / design） ===')
# 卡片：fill #F8F9FA，左缘 x=2（0..1 是画板边），顶缘待定 -> 先扫顶缘
top = None
for y in range(255, 280):
    if near(px[400, y], (248, 249, 250), 12):
        top = y
        break
print('  卡片顶缘 y = %s (x=400 处首个 #F8F9FA)' % top)
if top:
    A, r, rd = fit_corner(2, top, (248, 249, 250), n=40, tol=14, zone=(2, 1678))
    print('  卡左上角 A=%d  r=%.2f dev = %.2f design' % (A, r, rd))
    print('  卡右上角   (1677-r?) 反向：')
    A2, r2, rd2 = fit_corner(1678 - 40 + 1, top, (248, 249, 250), n=40, tol=14, zone=(2, 1678))
    print('    A=%d  r=%.2f dev = %.2f design' % (A2, r2, rd2))

# 搜索框：#FFFFFF 内 + #F2F2F2 边 -> 角外 = 页底白。用「非白」计数
print('\n  搜索框：找顶缘（x=600 处首个非白）')
st = None
for y in range(150, 175):
    if not near(px[600, y], (255, 255, 255), 8):
        st = y
        break
print('    搜索框顶缘 y = %s' % st)
if st:
    A3, r3, rd3 = fit_corner(2, st, (255, 255, 255), n=40, tol=8, zone=(2, 700))
    print('    左上角(n=40) A=%d  r=%.2f dev = %.2f design' % (A3, r3, rd3))
    A4, r4, rd4 = fit_corner(2, st, (255, 255, 255), n=24, tol=8, zone=(2, 700))
    print('    左上角(n=24) A=%d  r=%.2f dev = %.2f design' % (A4, r4, rd4))

# 顶部曲线（卡片）
print('\n=== 卡片左上角每行最左 fill 像素 ===')
for y in range(260, 284):
    xs = [x for x in range(2, 300) if near(px[x, y], (248, 249, 250), 12)]
    print('  y=%d  x0=%s' % (y, xs[0] if xs else '-'))

# hover 行底色
print('\n=== 行底色 ===')
for name, y in [('行1', 320), ('行2', 480), ('行3(hover)', 640), ('行4', 790), ('行7', 1230)]:
    print('  %-11s y=%4d  x=400 -> %s | x=1800? n/a | x=1380 -> %s' % (
        name, y, '#%02X%02X%02X' % px[400, y], '#%02X%02X%02X' % px[1380, y]))
