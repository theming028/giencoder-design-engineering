# -*- coding: utf-8 -*-
"""r88 ③ 收尾量测：hover 钮（边框/文字 ink）、默认图标钮 ink、行文本 ink、头部/工具条 ink。只读。"""
import os
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')).convert('RGB')
px = im.load()
W, H = im.size


def c(x, y):
    return '#%02X%02X%02X' % px[x, y]


def ink(x0, y0, x1, y1, thr=0.45):
    """在区域内求「墨迹」bbox：以区域内最亮为底，取暗于底*(1-thr) 的像素。只报 bbox 与计数。"""
    vals = [(x, y, px[x, y]) for y in range(y0, y1) for x in range(x0, x1)]
    lum = [0.299 * r + 0.587 * g + 0.114 * b for _, _, (r, g, b) in vals]
    mx = max(lum)
    pts = [(x, y) for (x, y, _), l in zip(vals, lum) if l < mx * (1 - thr)]
    if not pts:
        return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys), len(pts))


print('=== 1. hover 钮（行3 左钮 1416..1519）左缘竖直取样 y=642 水平 ===')
print('   ', ' '.join('%d:%s' % (x, c(x, 642)) for x in range(1414, 1424)))
print('    右缘:', ' '.join('%d:%s' % (x, c(x, 642)) for x in range(1514, 1523)))
print('    顶边 x=1470:', ' '.join('%d:%s' % (y, c(1470, y)) for y in range(606, 614)))
print('    底边 x=1470:', ' '.join('%d:%s' % (y, c(1470, y)) for y in range(670, 678)))
bb = ink(1416, 612, 1520, 672, 0.45)
print('    文字 ink bbox =', bb, ' (x0,y0,x1,y1,count)')

print('\n=== 2. 默认图标钮（行1 左钮 1511..1568） ===')
print('    左缘 y=345:', ' '.join('%d:%s' % (x, c(x, 345)) for x in range(1509, 1518)))
print('    顶边 x=1540:', ' '.join('%d:%s' % (y, c(1540, y)) for y in range(314, 322)))
bb2 = ink(1513, 319, 1567, 373, 0.45)
print('    图标 ink bbox =', bb2)

print('\n=== 3. 各行 title / meta ink（x 从 30 起，避开左侧） ===')
ROWS = [(264, 418), (418, 566), (566, 714), (714, 862), (862, 1010), (1010, 1158), (1158, 1315)]
for i, (a, b) in enumerate(ROWS, 1):
    t = ink(30, a + 2, 1300, a + 60, 0.45)
    m = ink(30, a + 60, 1300, b - 2, 0.45)
    print('  行%d (%d..%d) title=%s' % (i, a, b, t))
    print('              meta =%s' % (m,))

print('\n=== 4. 头部：标题 / 副标题 ink ===')
print('  标题  ', ink(0, 4, 400, 50, 0.45))
print('  副标题', ink(0, 56, 1200, 100, 0.35))

print('\n=== 5. 清空按钮 ===')
print('  顶边 x=1550:', ' '.join('%d:%s' % (y, c(1550, y)) for y in range(20, 30)))
print('  左缘 y=60:', ' '.join('%d:%s' % (x, c(x, 60)) for x in range(1460, 1472)))
print('  文字 ink', ink(1470, 30, 1670, 92, 0.45))

print('\n=== 6. 搜索框 / 下拉 x 范围（y=190，tol 近白） ===')
row = []
for x in range(W):
    r, g, b = px[x, 190]
    row.append(1 if (abs(r - 255) + abs(g - 255) + abs(b - 255)) > 10 else 0)
segs, s = [], None
for x, v in enumerate(row):
    if v and s is None:
        s = x
    elif not v and s is not None:
        segs.append((s, x - 1)); s = None
if s is not None:
    segs.append((s, W - 1))
print('   ', segs)

print('\n=== 7. 搜索图标 / 下拉图标 ink ===')
print('  搜索图标', ink(10, 170, 60, 214, 0.45))
print('  下拉内容', ink(1284, 168, 1670, 216, 0.45))
