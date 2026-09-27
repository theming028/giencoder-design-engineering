# -*- coding: utf-8 -*-
"""裁切放大：容器左上角 / 侧栏分割线，肉眼确认有无描边。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")

crops = [
    ("corner-tl", (0, 80, 120, 200)),
    ("divider", (1340, 1100, 1460, 1300)),
    ("corner-bottom", (0, 2090, 120, 2160)),
]
tiles = []
for name, box in crops:
    c = im.crop(box)
    f = 6 if c.width < 200 else 4
    c = c.resize((c.width * f, c.height * f), Image.NEAREST)
    c.save("mg-work/r24/zoom-%s.png" % name)
    print(name, box, "->", c.size)
