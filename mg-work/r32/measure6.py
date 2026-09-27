# -*- coding: utf-8 -*-
"""对 coop.png（1440×900 1x 设计稿）做像素扫描，复核：
   左面板(left) 与 右面板(right) 的：面板边界 / 内容区边界 / 行墨色带 / 行 pitch / 底栏按钮
"""
from PIL import Image
import io
import sys

im = Image.open("mg-work/r32/design/coop.png").convert("RGB")
W, H = im.size
px = im.load()
print("size", W, H)


def col(x, y):
    return px[x, y]


def scan_rows(x0, x1, y0, y1, thresh=200):
    """在 x 区间内找「平均亮度 < thresh」的 y 段（墨色带）"""
    segs = []
    cur = None
    for y in range(y0, y1):
        s = 0
        n = 0
        for x in range(x0, x1):
            r, g, b = px[x, y]
            lum = (r * 299 + g * 587 + b * 114) // 1000
            if lum < thresh:
                s += 1
            n += 1
        dark = s > 1
        if dark and cur is None:
            cur = y
        elif not dark and cur is not None:
            segs.append((cur, y - 1))
            cur = None
    if cur is not None:
        segs.append((cur, y1 - 1))
    return segs


def scan_cols(y0, y1, x0, x1, thresh=200):
    segs = []
    cur = None
    for x in range(x0, x1):
        s = 0
        for y in range(y0, y1):
            r, g, b = px[x, y]
            lum = (r * 299 + g * 587 + b * 114) // 1000
            if lum < thresh:
                s += 1
        dark = s > 1
        if dark and cur is None:
            cur = x
        elif not dark and cur is not None:
            segs.append((cur, x - 1))
            cur = None
    if cur is not None:
        segs.append((cur, x1 - 1))
    return segs


def find_panel_edges(y, x0, x1, bg=(255, 255, 255), tol=6):
    """在 y 行上找与背景差异明显的连续白块边界"""
    spans = []
    cur = None
    for x in range(x0, x1):
        r, g, b = px[x, y]
        white = abs(r - 255) < 30 and abs(g - 255) < 30 and abs(b - 255) < 30
        if white and cur is None:
            cur = x
        elif not white and cur is not None:
            if x - cur > 100:
                spans.append((cur, x - 1))
            cur = None
    if cur is not None and x1 - cur > 100:
        spans.append((cur, x1 - 1))
    return spans


print("\n== 面板横向范围（取 y=200 一行） ==")
print(find_panel_edges(200, 0, W))

print("\n== 面板纵向范围（取 x=70 一列，左面板左缘附近） ==")
# 左面板左缘：在 y=200 的 span 起点取值
sp = find_panel_edges(200, 0, W)
for (a, b) in sp:
    print("  panel span", a, b)
    xm = a + 5
    seg = []
    cur = None
    for y in range(0, H):
        r, g, b2 = px[xm, y]
        white = abs(r - 255) < 30 and abs(g - 255) < 30 and abs(b2 - 255) < 30
        if white and cur is None:
            cur = y
        elif not white and cur is not None:
            if y - cur > 50:
                seg.append((cur, y - 1))
            cur = None
    if cur is not None and H - cur > 50:
        seg.append((cur, H - 1))
    print("   vertical white span @x=%d ->" % xm, seg)

print("\n== 左面板内部分隔线（x=300 一列，找非白像素） ==")
for name, xm in [("x=300", 300), ("x=120", 120)]:
    lines = []
    for y in range(130, 771):
        r, g, b = px[xm, y]
        if not (abs(r - 255) < 12 and abs(g - 255) < 12 and abs(b - 255) < 12) and \
           not (abs(r - 247) < 4 and abs(g - 247) < 4 and abs(b - 247) < 4):
            lines.append((y, (r, g, b)))
    # 压缩连续
    out = []
    prev = None
    for y, c in lines:
        if prev is None or y != prev + 1:
            out.append([y, y, c])
        else:
            out[-1][1] = y
        prev = y
    print(" ", name, [(a, b, c) for a, b, c in out][:40])

print("\n== 左面板内容区墨色带（x 120..700） ==")
segs = scan_rows(120, 700, 150, 780, 200)
print(segs)
if len(segs) > 2:
    centers = [round((a + b) / 2, 1) for a, b in segs]
    print("  centers", centers)
    print("  diffs", [round(centers[i + 1] - centers[i], 1) for i in range(len(centers) - 1)])

print("\n== 右面板内容区墨色带（x 800..1400） ==")
segs2 = scan_rows(800, 1400, 150, 780, 200)
print(segs2)
if len(segs2) > 2:
    centers2 = [round((a + b) / 2, 1) for a, b in segs2]
    print("  centers", centers2)
    print("  diffs", [round(centers2[i + 1] - centers2[i], 1) for i in range(len(centers2) - 1)])
