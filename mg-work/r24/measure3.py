# -*- coding: utf-8 -*-
"""全行扫描：一次列出 1440 宽画板在该行的所有色变点，定位所有竖线。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()

for y in (1200, 1500, 1900):
    print("\n===== 整行扫描 y=%d (css %.1f) =====" % (y, y / 2.0))
    prev = None
    start = 0
    for x in range(0, 2880):
        c = px[x, y]
        if prev is None:
            prev = c
            start = x
            continue
        if c != prev:
            if x - start >= 1:
                print("  x=%4d..%4d css %7.1f..%7.1f  %s" % (start, x - 1, start / 2.0, (x - 1) / 2.0, prev))
            prev = c
            start = x
    print("  x=%4d..2879 css %7.1f..1439.5  %s" % (start, start / 2.0, prev))
