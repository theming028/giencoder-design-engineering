# -*- coding: utf-8 -*-
"""精测：主列文本行 / list 圆点 / 侧栏 h2 与 label·value 起点 / 高优先级胶囊。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()


def rows(x0, x1, y0, y1, thr=200, label="", minh=2):
    print("### %s x=%d..%d y=%d..%d thr<%d" % (label, x0, x1, y0, y1, thr))
    inside = False; s = 0
    for y in range(y0, y1 + 1):
        hit = any(sum(px[x, y]) / 3 < thr for x in range(x0, x1))
        if hit and not inside:
            inside = True; s = y
        elif not hit and inside:
            inside = False
            if y - s >= minh:
                print("   y=%4d..%4d css %6.1f..%6.1f h=%4.1f" % (s, y - 1, s / 2.0, (y - 1) / 2.0, (y - s) / 2.0))
    if inside:
        print("   y=%4d..%4d css %6.1f..%6.1f" % (s, y1, s / 2.0, y1 / 2.0))


def cols(y, x0, x1, thr=200, label="", gap=6):
    print("### %s y=%d(css %.1f) x=%d..%d" % (label, y, y / 2.0, x0, x1))
    runs = []; inside = False; s = 0
    for x in range(x0, x1 + 1):
        hit = sum(px[x, y]) / 3 < thr
        if hit and not inside:
            inside = True; s = x
        elif not hit and inside:
            inside = False; runs.append((s, x - 1))
    if inside:
        runs.append((s, x1))
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    for a, b in merged:
        print("   x=%4d..%4d css %6.1f..%6.1f w=%4.1f" % (a, b, a / 2.0, b / 2.0, (b - a + 1) / 2.0))


# 主列所有文本行（左栏 main 内容区）
rows(96, 1360, 100, 900, 200, "主列文本行", 2)
