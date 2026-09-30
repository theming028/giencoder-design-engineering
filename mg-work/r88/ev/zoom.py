# -*- coding: utf-8 -*-
"""角部放大 + 对比度拉伸 + 5device 网格（看清 1~2 灰阶差）。"""
import os
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(REPO, 'mg-work', 'r88', 'raw')
im = Image.open(os.path.join(D, 'arch@2x_rgb.png')).convert('RGB')

# 把 [240,255] 灰阶拉伸到 [0,255]，让 #F8F9FA 与 #FFFFFF 的差变明显
LUT = [0] * 256
for v in range(256):
    LUT[v] = 0 if v <= 240 else min(255, int((v - 240) * 255 / 15))
STRETCH = LUT * 3

CROPS = [
    ('z_card', (2, 256, 82, 336), 7, 5),
    ('z_search', (2, 152, 82, 232), 7, 5),
    ('z_btn2', (1500, 306, 1580, 386), 7, 5),
]
for name, box, z, step in CROPS:
    c = im.crop(box).point(STRETCH).convert('RGB')
    c = c.resize((c.width * z, c.height * z), Image.NEAREST)
    d = ImageDraw.Draw(c)
    for i in range(0, c.width, z * step):
        d.line([(i, 0), (i, c.height)], fill=(255, 60, 200), width=1)
    for j in range(0, c.height, z * step):
        d.line([(0, j), (c.width, j)], fill=(255, 60, 200), width=1)
    p = os.path.join(D, name + '.png')
    c.save(p)
    print(' ->', p, c.size, ' 网格 = %d device px (%0.1f design px)' % (step, step / 2.0))
