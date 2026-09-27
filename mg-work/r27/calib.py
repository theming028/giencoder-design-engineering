# -*- coding: utf-8 -*-
"""校准 board-design.png 是否为无损导出：采样若干已知 token 色区域。"""
import collections
from PIL import Image

im = Image.open("mg-work/kanban/root/board-design.png").convert("RGB")
px = im.load()
print("size", im.size, "mode", im.mode)


def probe(name, x0, y0, x1, y1, expect):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            cnt[px[x, y]] += 1
    c = cnt.most_common(1)[0][0]
    ok = "OK " if c == expect else "DIFF"
    print("  %-22s most=%s #%02X%02X%02X  expect=%s #%02X%02X%02X  %s"
          % (name, c, c[0], c[1], c[2], expect, expect[0], expect[1], expect[2], ok))


# 页面外底色 --kb-surround: #E5EDF5
probe("surround", 300, 830, 340, 860, (0xE5, 0xED, 0xF5))
# 卡片白底
probe("card bg", 60, 300, 100, 306, (0xFF, 0xFF, 0xFF))
# 待开始列头圆点 --kb-col-todo #A9A9A9
probe("col bar todo", 44, 214, 48, 226, (0xA9, 0xA9, 0xA9))
# 栏间距/列底 -- 列容器底（浅灰白 #F7F8FA?）
probe("col body", 120, 630, 160, 660, (0xFF, 0xFF, 0xFF))
