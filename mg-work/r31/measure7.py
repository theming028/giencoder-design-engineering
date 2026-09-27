# -*- coding: utf-8 -*-
"""第 31 轮设计稿精量 v7 —— 收口：头像色/面板圆角/滚动条/行内字号/对勾"""
from PIL import Image
from collections import Counter

PNG = "mg-work/r31/design/dispatch.png"
OX, OY, S = 60, 44, 2.0
im = Image.open(PNG).convert("RGB")
W, H = im.size
px = im.load()


def d2p(x, y):
    return (int(round(OX + x * S)), int(round(OY + y * S)))


def p2d(x, y):
    return ((x - OX) / S, (y - OY) / S)


def hexs(c):
    return "#%02X%02X%02X" % c


def lum(c):
    return (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000


print("=" * 74)
print("A. 7 枚头像：20x20 圆内出现最多的「非白、非灰、非蓝」主色 + 圆内白字 ink")
rows = [("邵禹铭", 118), ("秦怡", 152), ("韩佳毅", 186), ("顾帆", 220),
        ("姜嘉怡", 254), ("朱甜", 288), ("齐瑞辰", 322)]
for name, top in rows:
    cnt = Counter()
    xs, ys = [], []
    for yy in range(top, top + 32):
        for xx in range(20, 50):
            a, b = d2p(xx, yy)
            c = px[a, b]
            sat = max(c) - min(c)
            if sat > 25:            # 有彩度 -> 头像环
                cnt[c] += 1
                xs.append(a); ys.append(b)
    top3 = " ".join("%s(%d)" % (hexs(c), n) for c, n in cnt.most_common(3))
    # 白字 ink：圆内 lum>200 且彩度 <20
    gx, gy = [], []
    for yy in range(top, top + 32):
        for xx in range(22, 46):
            a, b = d2p(xx, yy)
            c = px[a, b]
            if lum(c) > 205 and (max(c) - min(c)) < 25:
                gx.append(a); gy.append(b)
    ink = ("x %.1f..%.1f (w %.1f) y %.1f..%.1f (h %.1f)" % (
        p2d(min(gx), 0)[0], p2d(max(gx) + 1, 0)[0], (max(gx) - min(gx) + 1) / S,
        p2d(0, min(gy))[1], p2d(0, max(gy) + 1)[1], (max(gy) - min(gy) + 1) / S)) if gx else "无"
    geo = "x %.1f..%.1f y %.1f..%.1f" % (p2d(min(xs), 0)[0], p2d(max(xs) + 1, 0)[0],
                                         p2d(0, min(ys))[1], p2d(0, max(ys) + 1)[1]) if xs else "-"
    print("  %-8s %-12s 圆 %s | 白字ink %s" % (name, top3, geo, ink))

print("=" * 74)
print("B. 面板圆角：左边框直线段的 y 起止（radius = 起止值）")
col = []
for y in range(OY, OY + 960):
    for x in range(OX - 4, OX + 5):
        if abs(px[x, y][0] - 229) <= 6 and abs(px[x, y][1] - 229) <= 6:
            col.append(y); break
print("  左边框 png y %d..%d -> design y %.1f..%.1f" % (
    min(col), max(col), p2d(0, min(col))[1], p2d(0, max(col) + 1)[1]))
rowt = []
for x in range(OX, OX + 640):
    for y in range(OY - 4, OY + 5):
        if abs(px[x, y][0] - 229) <= 6 and abs(px[x, y][1] - 229) <= 6:
            rowt.append(x); break
print("  上边框 png x %d..%d -> design x %.1f..%.1f" % (
    min(rowt), max(rowt), p2d(min(rowt), 0)[0], p2d(max(rowt) + 1, 0)[0]))

print("=" * 74)
print("C. 滚动条（节点声明 6x128 @(310,118)，色 #D6D6D6）")
xs, ys = [], []
for yy in range(110, 300):
    for xx in range(304, 322):
        a, b = d2p(xx, yy)
        c = px[a, b]
        if abs(c[0] - 214) <= 3 and c[0] == c[1] == c[2]:
            xs.append(a); ys.append(b)
if xs:
    print("  滑块 design x %.1f..%.1f (w %.1f)  y %.1f..%.1f (h %.1f)" % (
        p2d(min(xs), 0)[0], p2d(max(xs) + 1, 0)[0], (max(xs) - min(xs) + 1) / S,
        p2d(0, min(ys))[1], p2d(0, max(ys) + 1)[1], (max(ys) - min(ys) + 1) / S))

print("=" * 74)
print("D. 行内文字 ink（第 2 行 秦怡，白底最干净）")
for label, x0, x1 in [("名字段(秦怡)", 48, 90), ("括号段((P0098603))", 88, 200)]:
    xs, ys = [], []
    for yy in range(152, 184):
        for xx in range(x0, x1):
            a, b = d2p(xx, yy)
            c = px[a, b]
            if lum(c) < 200:
                xs.append(a); ys.append(b)
    if xs:
        print("  %-16s x %.1f..%.1f (w %.1f)  y %.1f..%.1f (h %.1f)" % (
            label, p2d(min(xs), 0)[0], p2d(max(xs) + 1, 0)[0], (max(xs) - min(xs) + 1) / S,
            p2d(0, min(ys))[1], p2d(0, max(ys) + 1)[1], (max(ys) - min(ys) + 1) / S))

print("=" * 74)
print("E. 选中行对勾（节点 icon-wrapper 14x14，右侧）")
xs, ys = [], []
for yy in range(118, 150):
    for xx in range(270, 306):
        a, b = d2p(xx, yy)
        c = px[a, b]
        if c[2] > c[0] + 40:
            xs.append(a); ys.append(b)
if xs:
    print("  对勾 design x %.1f..%.1f (w %.1f)  y %.1f..%.1f (h %.1f) 色 %s" % (
        p2d(min(xs), 0)[0], p2d(max(xs) + 1, 0)[0], (max(xs) - min(xs) + 1) / S,
        p2d(0, min(ys))[1], p2d(0, max(ys) + 1)[1], (max(ys) - min(ys) + 1) / S,
        hexs(px[(min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2])))

print("=" * 74)
print("F. 行的左右内距核对（选中行：头像左缘 24 -> 行左 16；对勾右缘 -> 行右 304）")
print("  头像左缘 24 - 行左 16 = 8 ; 头像右缘 44")
print("=" * 74)
print("G. 选中行圆角（蓝底在 y=118 行的 x 起止推 r）")
for yy in [118, 119, 120, 121, 122, 123]:
    xs = [xx for xx in range(10, 310)
          if (lambda c: c[2] > c[0] + 8 and c[2] > 230)(px[d2p(xx, yy)[0], d2p(xx, yy)[1]])]
    if xs:
        print("  design y=%d -> 蓝底 x %.1f..%.1f" % (yy, min(xs), max(xs)))
