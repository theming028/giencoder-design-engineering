# -*- coding: utf-8 -*-
"""任务属性 8 个文本带：逐带列出暗色 run（label 段 / value 段）。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()
X0, X1 = 1370, 1888

BANDS = [(130, 155), (241, 263), (317, 339), (385, 407), (453, 475),
         (521, 543), (589, 611), (658, 679), (726, 747)]


def runs_of(a, b, thr=200, gap=14):
    cnt = {}
    for y in range(a, b + 1):
        for x in range(X0, X1):
            if sum(px[x, y]) / 3 < thr:
                cnt[x] = 1
    xs = sorted(cnt)
    out = []
    for x in xs:
        if out and x - out[-1][1] <= gap:
            out[-1][1] = x
        else:
            out.append([x, x])
    return out


for a, b in BANDS:
    rs = runs_of(a, b)
    txt = "  ".join("%.1f..%.1f" % (p / 2.0, q / 2.0) for p, q in rs[:6])
    print("css y %6.1f..%6.1f | %s" % (a / 2.0, b / 2.0, txt))
