# -*- coding: utf-8 -*-
"""设计稿局部放大：python crop.py <src.png> <out.png> <x> <y> <w> <h> [zoom]

坐标为**源图 device px**（左上原点）。
"""
import io
import sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
x, y, w, h = (int(v) for v in sys.argv[3:7])
zoom = float(sys.argv[7]) if len(sys.argv) > 7 else 3.0

im = Image.open(src).convert('RGB')
box = (x, y, x + w, y + h)
c = im.crop(box)
c = c.resize((int(c.width * zoom), int(c.height * zoom)), Image.NEAREST)
c.save(out)
print('OK %s  crop%s  zoom=%s  → %s' % (out, box, zoom, c.size))
