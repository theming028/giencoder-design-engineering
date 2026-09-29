# -*- coding: utf-8 -*-
"""打印设计稿 PNG 某区域的**数值**灰度（0=白 255=黑），用于精确定几何。
   用法：python num.py <x0> <y0> <x1> <y1> [--hex]
"""
import sys
from PIL import Image

PNG = 'mg-work/r83/raw/design_1389-18518.png'
DX, DY = 3, 2

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
im = Image.open(PNG).convert('L')
px = im.load()
print('      ' + ''.join('%4d' % x for x in range(x0, x1)))
for y in range(y0, y1):
    cells = []
    for x in range(x0, x1):
        v = px[max(0, min(im.width - 1, x + DX)), max(0, min(im.height - 1, y + DY))]
        cells.append('   .' if v > 250 else '%4d' % (255 - v))   # 打印「墨量」
    print('%4d  ' % y + ''.join(cells))
