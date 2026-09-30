# -*- coding: utf-8 -*-
"""r92 ①：分析 assets/images/bg-img-1.png 的尺寸/底色/点阵分布，用于决定 background 位置与尺寸。"""
from PIL import Image

im = Image.open('assets/images/bg-img-1.png').convert('RGB')
w, h = im.size
print('size', w, h)
print('base color L', im.getpixel((0, h // 2)))

print('--- horizontal profile y=h/2 (每 20px) ---')
for x in range(0, w, 20):
    r, g, b = im.getpixel((x, h // 2))
    print('x=%4d  #%02X%02X%02X' % (x, r, g, b))

print('--- vertical column x=%d (每 6px) ---' % (w - 2))
for y in range(0, h, 6):
    r, g, b = im.getpixel((w - 2, y))
    print('y=%3d  #%02X%02X%02X' % (y, r, g, b))

# 点阵最右端在哪里（相对底色 #F6F8FA 出现明显差异的第一列）
base = (246, 248, 250)
first = None
for x in range(w):
    r, g, b = im.getpixel((x, h // 2))
    if abs(r - base[0]) + abs(g - base[1]) + abs(b - base[2]) > 12:
        first = x
        break
print('第一个明显偏离底色的 x =', first, '(占比 %.1f%%)' % (100.0 * first / w))
