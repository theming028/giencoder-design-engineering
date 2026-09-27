# -*- coding: utf-8 -*-
"""收尾取数：分隔线色 / h2 墨色 / label·value 墨色 / 段落 vs 列表墨色。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()


def vprofile(x, y0, y1, tag=""):
    print("--- 竖切 %s x=%d(css%.1f)" % (tag, x, x / 2.0))
    prev = None; s = y0
    for y in range(y0, y1 + 1):
        c = px[x, y]
        if prev is None:
            prev = c; s = y; continue
        if c != prev:
            if y - s >= 2:
                print("    css y %6.1f..%6.1f  %s" % (s / 2.0, (y - 1) / 2.0, prev))
            prev = c; s = y


def ink(a, b, x0, x1, tag=""):
    best = None; pos = None
    for y in range(a, b + 1):
        for x in range(x0, x1):
            c = px[x, y]
            v = sum(c)
            if best is None or v < best:
                best = v; pos = (x, y, c)
    print("   %-18s 最暗像素 %s @ css(%.1f, %.1f)" % (tag, pos[2], pos[0] / 2.0, pos[1] / 2.0))


# 1) 顶栏底 / 标题区底（css x 200 附近；避开文字）
vprofile(660, 176, 260, "顶栏底+标题区")
vprofile(660, 260, 320, "标题区底")
# 2) 侧栏 h2 底 与 属性行底色
vprofile(1750, 200, 300, "侧栏 y100..150")

print("\n--- 墨色 ---")
ink(130, 155, 1425, 1560, "任务属性 h2")
ink(317, 339, 1425, 1470, "label 执行人")
ink(317, 339, 1553, 1650, "value 邵禹铭")
ink(522, 549, 96, 1360, "desc 段落行")
ink(570, 595, 96, 1360, "desc 列表行(含圆点)")
ink(570, 595, 150, 400, "desc 列表正文字")
ink(116, 171, 96, 1360, "h1 标题")
