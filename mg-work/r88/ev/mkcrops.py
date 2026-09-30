# -*- coding: utf-8 -*-
import os
from PIL import Image

R = os.path.join('mg-work', 'r88', 'raw')
im = Image.open(os.path.join(R, 'arch@2x_rgb.png')).convert('RGB')
jobs = [
    ('c_top.png', (0, 0, 1680, 320), 2),
    ('c_row1.png', (0, 350, 1680, 480), 3),
    ('c_row3.png', (0, 690, 1680, 800), 3),
]
for name, box, z in jobs:
    c = im.crop(box)
    c = c.resize((int(c.width * z), int(c.height * z)), Image.NEAREST)
    p = os.path.join(R, name)
    c.save(p)
    print('OK', p, c.size)
