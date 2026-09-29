# -*- coding: utf-8 -*-
"""把设计稿 PNG 的某个矩形区域渲成 ASCII 灰度图，用来精确读图标形状。
   用法：python scan.py <x0> <y0> <x1> <y1>   （节点内坐标，自动加 DX,DY 偏移）
"""
import sys
from PIL import Image

PNG = 'mg-work/r83/raw/design_1389-18518.png'
DX, DY = 3, 2

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
im = Image.open(PNG).convert('L')
px = im.load()

RAMP = ' .:-=+*#%@'
print('     ' + ''.join(str((x // 10) % 10) for x in range(x0, x1)))
print('     ' + ''.join(str(x % 10) for x in range(x0, x1)))
for y in range(y0, y1):
    row = []
    for x in range(x0, x1):
        v = px[max(0, min(im.width - 1, x + DX)), max(0, min(im.height - 1, y + DY))]
        # 255=白底 → ' '；越黑越靠后
        idx = int((255 - v) / 256 * len(RAMP))
        row.append(RAMP[min(idx, len(RAMP) - 1)])
    print('%4d ' % y + ''.join(row))
