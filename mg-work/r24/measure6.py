# -*- coding: utf-8 -*-
"""逐行文本带 -> 每带内首个暗色 run 的 x 位置（用于识别 list 圆点）。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()
X0, X1 = 96, 1360   # 主列内容区 device

bands = []
inside = False; s = 0
for y in range(100, 1000):
    hit = any(sum(px[x, y]) / 3 < 200 for x in range(X0, X1))
    if hit and not inside:
        inside = True; s = y
    elif not hit and inside:
        inside = False; bands.append((s, y - 1))
if inside:
    bands.append((s, 999))

for a, b in bands:
    mid = (a + b) // 2
    # 该带内所有暗像素的 x 最小值 & 各暗列计数
    cnt = {}
    for y in range(a, b + 1):
        for x in range(X0, X1):
            if sum(px[x, y]) / 3 < 200:
                cnt[x] = cnt.get(x, 0) + 1
    xs = sorted(cnt)
    if not xs:
        continue
    first = xs[0]
    # 第一段连续暗列的宽度
    w = 1
    for x in xs[1:]:
        if x == first + w:
            w += 1
        else:
            break
    c = px[first, mid]
    print("带 css %6.1f..%6.1f h=%4.1f | 首暗列 css x=%6.1f 宽=%4.1f 色=%s | 暗列数=%d"
          % (a / 2.0, b / 2.0, (b - a + 1) / 2.0, first / 2.0, w / 2.0, c, len(xs)))
