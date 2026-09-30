# -*- coding: utf-8 -*-
"""行内元信息图标：设计稿 vs 实现，**同倍率**对照 + ASCII 墨迹图。"""
import io, os
from PIL import Image

RAW = os.path.join(os.path.dirname(__file__), '..', 'raw')

# 行2（未右移那行）：design px 坐标
BASE_1X = (18, 250, 38, 267)          # design px
BASE_DEV = tuple(v * 2 for v in BASE_1X)

d = Image.open(os.path.join(RAW, 'arch@2x_rgb.png')).convert('RGB')
WEBF = __import__('sys').argv[1] if len(__import__('sys').argv) > 1 else 'web-arch@1x.png'
w = Image.open(os.path.join(RAW, WEBF)).convert('RGB')


def ascii_map(img, box, label, step=1):
    c = img.crop(box).convert('L')
    px = c.load()
    print('--- %s  %s  (%dx%d) ---' % (label, box, c.width, c.height))
    for y in range(0, c.height, step):
        row = ''
        for x in range(0, c.width, step):
            v = px[x, y]
            row += '#' if v < 110 else ('+' if v < 170 else ('.' if v < 225 else ' '))
        print('%3d|%s' % (y, row))
    print()


coarse = len(__import__('sys').argv) > 1 and __import__('sys').argv[1] == 'coarse'
ascii_map(d, BASE_DEV, 'DESIGN(device 2x)')
ascii_map(w, BASE_1X, 'WEB(1x)')

# 同倍率并排：设计 14x，实现 28x（1x -> 2x -> 14x）
Z = 14
a = d.crop(BASE_DEV).resize(((BASE_DEV[2] - BASE_DEV[0]) * Z, (BASE_DEV[3] - BASE_DEV[1]) * Z), Image.NEAREST)
b = w.crop(BASE_1X).resize(((BASE_1X[2] - BASE_1X[0]) * 2 * Z, (BASE_1X[3] - BASE_1X[1]) * 2 * Z), Image.NEAREST)
canvas = Image.new('RGB', (a.width + b.width + 20, max(a.height, b.height)), (255, 0, 255))
canvas.paste(a, (0, 0))
canvas.paste(b, (a.width + 20, 0))
canvas.save(os.path.join(RAW, 'mic-pair.png'))
print('saved mic-pair.png', a.size, b.size)
