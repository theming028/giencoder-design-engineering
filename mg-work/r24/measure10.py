# -*- coding: utf-8 -*-
"""高优先级胶囊几何/配色。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()

print("=== 优先级行（css y226.5..237.5 => device 453..475）底色扫描 ===")
for y in range(440, 490):
    cs = [x for x in range(1540, 1700)
          if px[x, y][0] > 249 and 225 <= px[x, y][1] <= 246 and px[x, y][2] <= 242]
    if cs:
        print("   y=%3d css%6.1f  x css %.1f..%.1f w=%.1f  色=%s"
              % (y, y / 2.0, min(cs) / 2.0, max(cs) / 2.0, (max(cs) - min(cs) + 1) / 2.0, px[(min(cs) + max(cs)) // 2, y]))

print("\n=== 行切片（device y=464）===")
prev = None; s = 0
for x in range(1540, 1700):
    c = px[x, 464]
    if prev is None:
        prev = c; s = x; continue
    if c != prev:
        print("   x=%4d..%4d css %.1f..%.1f  %s" % (s, x - 1, s / 2.0, (x - 1) / 2.0, prev))
        prev = c; s = x

print("\n=== 竖切 device x=1560（css 780，胶囊内）===")
prev = None; s = 0
for y in range(440, 490):
    c = px[1560, y]
    if prev is None:
        prev = c; s = y; continue
    if c != prev:
        print("   y=%3d..%3d css %.1f..%.1f  %s" % (s, y - 1, s / 2.0, (y - 1) / 2.0, prev))
        prev = c; s = y
