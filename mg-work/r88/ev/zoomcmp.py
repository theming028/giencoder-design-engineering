# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(REPO, 'mg-work', 'r88', 'raw')
dg = Image.open(os.path.join(D, 'arch@2x_rgb.png')).convert('RGB').resize((840, 658), Image.LANCZOS)
web = Image.open(os.path.join(D, 'web-arch-hover@1x.png')).convert('RGB')

REG = [
    ('head',   (0, 0, 420, 56), 3),
    ('clear',  (700, 0, 840, 56), 4),
    ('search', (0, 74, 380, 118), 4),
    ('proj',   (620, 74, 840, 118), 4),
    ('row1',   (0, 132, 300, 210), 3),
    ('btns',   (690, 284, 840, 358), 4),
    ('iconbtn',(690, 132, 840, 210), 4),
]
for name, box, z in REG:
    a = dg.crop(box); b = web.crop(box)
    w, h = a.size
    out = Image.new('RGB', (w * z * 2 + 24, h * z + 26), (255, 255, 255))
    d = ImageDraw.Draw(out)
    d.text((4, 4), 'DESIGN', fill=(180, 0, 0))
    d.text((w * z + 20, 4), 'WEB', fill=(0, 90, 180))
    out.paste(a.resize((w * z, h * z), Image.NEAREST), (4, 22))
    out.paste(b.resize((w * z, h * z), Image.NEAREST), (w * z + 20, 22))
    p = os.path.join(D, 'z_' + name + '.png')
    out.save(p)
    print(' ->', p, out.size)
