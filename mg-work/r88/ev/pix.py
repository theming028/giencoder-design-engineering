# -*- coding: utf-8 -*-
"""打印卡片角部原始像素表，定描边色 + 圆角几何。只读。"""
import os
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')).convert('RGB')
px = im.load()


def c(x, y):
    return '#%02X%02X%02X' % px[x, y]


print('=== 1. 卡片顶边（x=400 竖直 258..274） ===')
for y in range(258, 275):
    print('   y=%d  %s' % (y, c(400, y)))

print('\n=== 2. 卡片左边（y=700 水平 0..12） ===')
for x in range(0, 13):
    print('   x=%d  %s' % (x, c(x, 700)))

print('\n=== 3. 卡片底边（x=400 竖直 1308..1316） ===')
for y in range(1308, min(1316, im.height)):
    print('   y=%d  %s' % (y, c(400, y)))

print('\n=== 4. 角部亮度图（device x 2..40, y 258..296） ===')
print('       ' + ''.join('%-4d' % (x % 100) for x in range(2, 41, 2)))
CH = {0: '.', 1: ':', 2: '-'}
for y in range(258, 297):
    row = []
    for x in range(2, 41):
        r, g, b = px[x, y]
        v = (r + g + b) / 3
        # 页底白 254 ; 卡fill 249 ; 描边 238 ; 更暗
        if v >= 253:
            ch = '.'
        elif v >= 247:
            ch = 'o'      # 卡内 fill
        elif v >= 234:
            ch = '+'      # 浅描边
        elif v >= 220:
            ch = '#'
        else:
            ch = '@'
        row.append(ch)
    print('  y=%3d  %s' % (y, ' '.join(row)))

print('\n=== 5. 搜索框顶边（x=600 竖直 156..166） ===')
for y in range(156, 167):
    print('   y=%d  %s' % (y, c(600, y)))
print('\n=== 6. 搜索框左边（y=190 水平 0..12） ===')
for x in range(0, 13):
    print('   x=%d  %s' % (x, c(x, 190)))
