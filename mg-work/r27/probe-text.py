# -*- coding: utf-8 -*-
"""校验取色方法：对比「已知 #1F1F1F 正文」与「标签文字」的最暗像素。"""
import collections
from PIL import Image

im = Image.open("mg-work/kanban/root/board-design.png").convert("RGB")
px = im.load()

REGIONS = [
    # (名字, x0, y0, x1, y1)
    ("卡片标题(14px 正文, 期望 #1F1F1F)", 44, 285, 245, 296),
    ("拆分需求项 标签内文字", 398, 346, 460, 363),
    ("拆分需求条目 标签内文字", 48, 464, 121, 481),
    ("拆分子条目 标签内文字", 48, 582, 110, 599),
    ("TASK-001 灰度标签(期望 #4E4E4E?)", 124, 366, 180, 383),
]

for name, x0, y0, x1, y1 in REGIONS:
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            cnt[px[x, y]] += 1
    mn = min(cnt, key=lambda c: sum(c))
    # 最暗 3 个（按计数>=2）
    dark = sorted([c for c, n in cnt.items() if n >= 2], key=lambda c: sum(c))[:5]
    print("\n== %s ==" % name)
    print("   最暗单像素: #%02X%02X%02X %s" % (mn[0], mn[1], mn[2], (mn,)))
    for c in dark:
        print("      #%02X%02X%02X %s x%d" % (c[0], c[1], c[2], c, cnt[c]))
    top = cnt.most_common(3)
    print("   最多: " + ", ".join("#%02X%02X%02X x%d" % (c[0], c[1], c[2], n) for c, n in top))
