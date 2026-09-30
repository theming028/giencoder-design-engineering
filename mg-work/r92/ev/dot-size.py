# -*- coding: utf-8 -*-
"""r92 ①：量源图点阵的实际尺寸（点径 / 点距），用于判断「原尺寸铺」还是「缩到顶栏高」。"""
from PIL import Image

im = Image.open('assets/images/bg-img-1.png').convert('RGB')
w, h = im.size
BASE = (246, 248, 250)


def is_dot(p):
    return abs(p[0] - BASE[0]) + abs(p[1] - BASE[1]) + abs(p[2] - BASE[2]) > 24


print('--- 沿 y=67 的水平游程（点宽 / 间隙）---')
runs = []
cur = None
start = 0
for x in range(w):
    d = is_dot(im.getpixel((x, 67)))
    if cur is None:
        cur = d
        start = x
    elif d != cur:
        runs.append((cur, x - start))
        cur = d
        start = x
runs.append((cur, w - start))
for kind, ln in runs[:40]:
    print('  %s len=%d' % ('DOT ' if kind else 'gap ', ln))

dots = [ln for k, ln in runs if k]
gaps = [ln for k, ln in runs if not k]
if dots:
    print('点宽: min=%d max=%d 众数≈%d' % (min(dots), max(dots), sorted(dots)[len(dots) // 2]))
if gaps:
    print('间隙: min=%d max=%d' % (min(gaps), max(gaps)))

print()
print('--- 沿 x=1578 的竖直游程（点高）---')
runs2 = []
cur = None
start = 0
for y in range(h):
    d = is_dot(im.getpixel((1578, y)))
    if cur is None:
        cur = d
        start = y
    elif d != cur:
        runs2.append((cur, y - start))
        cur = d
        start = y
runs2.append((cur, h - start))
for kind, ln in runs2:
    print('  %s len=%d' % ('DOT ' if kind else 'gap ', ln))
