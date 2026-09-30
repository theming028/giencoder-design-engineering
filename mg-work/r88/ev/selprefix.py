# -*- coding: utf-8 -*-
"""下拉前缀图标：设计稿 vs 实现，同倍率对照 + ASCII 墨迹图。"""
import io, os, sys
from PIL import Image

RAW = os.path.join(os.path.dirname(__file__), '..', 'raw')
d = Image.open(os.path.join(RAW, 'arch@2x_rgb.png')).convert('RGB')
WEBF = sys.argv[1] if len(sys.argv) > 1 else 'web-arch-r89@1x.png'
w = Image.open(os.path.join(RAW, WEBF)).convert('RGB')

# 下拉框 design 坐标 x 640..840, y 80..112  ⇒ 只取左侧前缀图标一带
DESIGN_1X = (640, 80, 672, 112)      # design px（框内左起 32px）
DESIGN_DEV = tuple(v * 2 for v in DESIGN_1X)
WEB_1X = DESIGN_1X


def ink_map(img, box, label, thr=200, hi=170):
    c = img.crop(box).convert('L')
    px = c.load()
    print('--- %s  box=%s  %dx%d ---' % (label, box, c.width, c.height))
    for y in range(c.height):
        row = ''
        for x in range(c.width):
            v = px[x, y]
            row += '#' if v < hi else ('+' if v < thr else '.')
        print('%3d|%s' % (y, row))
    print()


def bbox(img, box, thr=210):
    c = img.crop(box).convert('L')
    px = c.load()
    xs, ys = [], []
    for y in range(c.height):
        for x in range(c.width):
            if px[x, y] < thr:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)


ink_map(d, DESIGN_DEV, 'DESIGN(device 2x)')
ink_map(w, WEB_1X, 'WEB(1x)')
print('DESIGN ink bbox(局部 device):', bbox(d, DESIGN_DEV, 215))
print('WEB    ink bbox(局部 1x)    :', bbox(w, WEB_1X, 228))

# 同倍率并排
Z = 10
a = d.crop(DESIGN_DEV).resize(((DESIGN_DEV[2] - DESIGN_DEV[0]) * Z, (DESIGN_DEV[3] - DESIGN_DEV[1]) * Z), Image.NEAREST)
b = w.crop(WEB_1X).resize(((WEB_1X[2] - WEB_1X[0]) * 2 * Z, (WEB_1X[3] - WEB_1X[1]) * 2 * Z), Image.NEAREST)
canvas = Image.new('RGB', (a.width + b.width + 24, max(a.height, b.height)), (255, 0, 255))
canvas.paste(a, (0, 0)); canvas.paste(b, (a.width + 24, 0))
canvas.save(os.path.join(RAW, 'selprefix-pair.png'))
print('saved selprefix-pair.png', a.size, b.size)
