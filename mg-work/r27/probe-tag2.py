# -*- coding: utf-8 -*-
"""裁剪 + 8x 放大三个标签，并打印前 12 个高频色（排除白底）。"""
import collections
from PIL import Image

SRC = "mg-work/kanban/root/board-design.png"
im = Image.open(SRC).convert("RGB")
px = im.load()

TAGS = [
    ("拆分需求项", 398, 460, 464, 481),
    ("拆分需求条目", 48, 121, 464, 481),
    ("拆分子条目", 48, 110, 582, 599),
]

for name, xl, xr, yt, yb in TAGS:
    pad = 4
    box = (xl - pad, yt - pad, xr + 1 + pad, yb + 1 + pad)
    crop = im.crop(box)
    crop.resize((crop.width * 9, crop.height * 9), Image.NEAREST).save(
        "mg-work/r27/zoom-%s.png" % {"拆分需求项": "item", "拆分需求条目": "entry", "拆分子条目": "sub"}[name])
    cnt = collections.Counter()
    for y in range(yt, yb + 1):
        for x in range(xl, xr + 1):
            cnt[px[x, y]] += 1
    top = cnt.most_common(12)
    print("\n== %s  %dx%d ==" % (name, xr - xl + 1, yb - yt + 1))
    for c, n in top:
        print("   #%02X%02X%02X  rgb%-16s x%d" % (c[0], c[1], c[2], str(c), n))
