# -*- coding: utf-8 -*-
"""r88 ③ 定稿量测：一次拿全（底/缘/圆角/分隔线/控件盒）。只读。"""
import os
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')).convert('RGB')
W, H = im.size
px = im.load()
S = 2.0          # device / design
print('PNG = %dx%d  (scale %.0f)' % (W, H, S))


def hexat(x, y):
    r, g, b = px[x, y]
    return '#%02X%02X%02X' % (r, g, b)


def runs(y, tol=5):
    """一行里「与**左侧首像素**不同」的连续段（用于找盒边界）。"""
    out, cur = [], None
    for x in range(W):
        r, g, b = px[x, y]
        d = abs(r - 248) + abs(g - 249) + abs(b - 250)
        if d > tol:
            if cur and x == cur[1] + 1:
                cur = (cur[0], x)
            else:
                if cur:
                    out.append(cur)
                cur = (x, x)
        else:
            if cur:
                out.append(cur); cur = None
    if cur:
        out.append(cur)
    return out


print('\n=== A. 底色取样 ===')
for name, (x, y) in [
    ('页底(卡外左上)', (5, 5)), ('卡内左上', (30, 300)), ('卡内中线', (840, 700)),
    ('行1区内', (400, 300)), ('工具条区(搜索框内)', (600, 190)),
    ('卡外右侧', (1670, 200)), ('行尾按钮内', (1540, 345)),
]:
    print('  %-18s (%4d,%4d) = %s' % (name, x, y, hexat(x, y)))

print('\n=== B. 卡片水平范围（y=300 全段） ===')
print('  ', runs(300)[:8], '... 共', len(runs(300)))

print('\n=== C. 卡片竖向范围（x=840 与 x=30） ===')
for x in (840, 30, 100):
    ys = [y for y in range(250, H - 1) if abs(px[x, y][0] - 255) + abs(px[x, y][1] - 255) + abs(px[x, y][2] - 255) > 12]
    print('  x=%4d  非白 y: %s .. %s   (n=%d)' % (x, ys[0] if ys else '-', ys[-1] if ys else '-', len(ys)))

print('\n=== D. 卡左上角「每行最左非白像素」曲线（反推圆角 r） ===')
for y in range(262, 282):
    xs = [x for x in range(2, 400) if abs(px[x, y][0] - 255) + abs(px[x, y][1] - 255) + abs(px[x, y][2] - 255) > 12]
    print('  y=%d  x0=%s' % (y, xs[0] if xs else '-'))

print('\n=== E. 搜索框左上角曲线（toolbar 顶边） ===')
for y in range(157, 175):
    xs = [x for x in range(2, 600) if abs(px[x, y][0] - 255) + abs(px[x, y][1] - 255) + abs(px[x, y][2] - 255) > 10]
    print('  y=%d  x0=%s' % (y, xs[0] if xs else '-'))

print('\n=== F. 搜索框 / 下拉水平范围（y=190 中线） ===')
row = runs(190, tol=6)
print('  ', [(a, b) for a, b in row])

print('\n=== G. 分隔线 y=418 / y=566 全段 ===')
for y in (418, 419, 566, 567):
    print('  y=%d %s' % (y, runs(y, tol=5)[:6]))

print('\n=== H. 行尾按钮（默认态行2；hover 态行3）===')
for y in (345, 640):
    print('  y=%d %s' % (y, runs(y, tol=6)[:8]))
print('  行2 btn 内色 =', hexat(1540, 345), ' 边 =', hexat(1512, 345))
print('  行3 btn 内色 =', hexat(1470, 640))
for y in (315, 316, 374, 375, 606, 610, 673, 676):
    print('  btn 竖直 y=%d  x=1540 -> %s | x=1470 -> %s' % (y, hexat(1540, y), hexat(1470, y)))
