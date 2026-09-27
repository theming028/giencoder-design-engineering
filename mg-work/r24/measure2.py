# -*- coding: utf-8 -*-
"""多行平均 -> 精确还原设计稿容器边缘的投影衰减曲线。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
W, H = im.size
px = im.load()
BG = px[2, 2]
print("size=%dx%d bg=%s" % (W, H, BG))


def avg(x0, x1, y0, y1, axis):
    """对区域求均值；axis='y' 表示沿 y 平均（用于竖直边界）"""
    acc = [0, 0, 0]
    n = 0
    for x in range(x0, x1):
        for y in range(y0, y1):
            c = px[x, y]
            acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            n += 1
    return tuple(round(v / n, 2) for v in acc)


print("\n### 左栏左边界：沿 y=400..1100 平均，x=0..30（2x）")
for x in range(0, 31):
    c = avg(x, x + 1, 400, 1100, 'y')
    d = [round(c[i] - BG[i], 2) for i in range(3)]
    print("  x=%2d(css %.1f)  %s  delta=%s" % (x, x / 2.0, c, d))

print("\n### 左栏上边界：沿 x=300..900 平均，y=86..106")
for y in range(86, 107):
    c = avg(300, 900, y, y + 1, 'x')
    d = [round(c[i] - BG[i], 2) for i in range(3)]
    print("  y=%3d(css %.1f)  %s  delta=%s" % (y, y / 2.0, c, d))

print("\n### 左栏下边界：沿 x=300..900 平均，y=2138..2160")
for y in range(2138, 2160):
    c = avg(300, 900, y, y + 1, 'x')
    d = [round(c[i] - BG[i], 2) for i in range(3)]
    print("  y=%4d(css %.1f)  %s  delta=%s" % (y, y / 2.0, c, d))

print("\n### 两栏间隙：沿 y=400..1100 平均，x=1878..1912")
for x in range(1878, 1913):
    c = avg(x, x + 1, 400, 1100, 'y')
    d = [round(c[i] - BG[i], 2) for i in range(3)]
    print("  x=%4d  %s  delta=%s" % (x, c, d))
