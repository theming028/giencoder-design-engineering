# -*- coding: utf-8 -*-
"""量取「转派」浮窗设计稿（1345:18366, 320x480 @2x 导出 760x1080）的关键色与几何。
PNG 坐标 = (62 + 2*dx, 46 + 2*dy)。
"""
from PIL import Image

im = Image.open("mg-work/r31/design/dispatch.png").convert("RGB")
px = im.load()
W, H = im.size
OX, OY, S = 62, 46, 2


def P(dx, dy):
    return px[int(OX + S * dx), int(OY + S * dy)]


def hexs(c):
    return "#%02X%02X%02X" % c


def darkest(x0, y0, x1, y1):
    """在 1x 设计坐标区间内找最暗像素（文字色）"""
    best = (999, None, None)
    for x in range(int(OX + S * x0), int(OX + S * x1)):
        for y in range(int(OY + S * y0), int(OY + S * y1)):
            c = px[x, y]
            s = sum(c)
            if s < best[0]:
                best = (s, c, (x, y))
    return hexs(best[1]), best[2]


def glyph_rows(x0, y0, x1, y1, thr=200):
    """返回文字像素的竖直范围（1x 设计坐标）"""
    ys = []
    for y in range(int(OY + S * y0), int(OY + S * y1)):
        n = sum(1 for x in range(int(OX + S * x0), int(OX + S * x1)) if sum(px[x, y]) / 3 < thr)
        if n:
            ys.append(y)
    if not ys:
        return None
    return (round((ys[0] - OY) / S, 1), round((ys[-1] - OY) / S, 1), round((ys[-1] - ys[0] + 1) / S, 1))


print("PNG", im.size)
print()
print("== 面板底色 ==", hexs(P(160, 400)), hexs(P(160, 60)))
print("== 标题「将任务转派给：」最深像素 ==", darkest(16, 16, 114, 38), " 字形竖直范围:", glyph_rows(16, 10, 120, 40))
print("== 副标题最深像素 ==", darkest(16, 40, 200, 58), " 字形竖直范围:", glyph_rows(16, 36, 240, 60))
print()
print("== 搜索框 ==")
print("  边框(上边 y=70):", hexs(P(160, 70)), hexs(P(160, 70.5)))
print("  底色(中心):", hexs(P(160, 86)))
print("  占位文字最深:", darkest(48, 74, 110, 98), " 字形竖直:", glyph_rows(48, 72, 110, 100))
print("  放大镜图标最深:", darkest(18, 76, 40, 96))
print()
print("== 列表行（设计 y 起 118，pitch 34）==")
for i, (name, y) in enumerate([("邵禹铭 选中", 118), ("秦怡", 152), ("韩佳毅", 186), ("顾帆(hover)", 220),
                               ("姜嘉怡", 254), ("朱甜", 288), ("齐瑞辰", 322)]):
    cy = y + 17
    print("  行%d %-12s 左端(2px内) %s  中心 %s  右端 %s  文字最深 %s 字形竖直 %s"
          % (i + 1, name, hexs(P(18, cy)), hexs(P(160, cy)), hexs(P(300, cy)),
             darkest(34, y + 6, 160, y + 28), glyph_rows(34, y + 2, 170, y + 32)))
print()
print("== 选中行背景（邵禹铭）==")
for dx in (16, 17, 20, 160, 300, 303):
    print("   x=%d y=130 %s" % (dx, hexs(P(dx, 130))))
print("  上边 y=118:", hexs(P(160, 118)), " y=117:", hexs(P(160, 117)), " y=151:", hexs(P(160, 151)))
print()
print("== 头像（设计 20x20，圆心 x≈? ）==")
for name, y in [("邵禹铭", 118), ("秦怡", 152), ("韩佳毅", 186), ("顾帆", 220), ("姜嘉怡", 254), ("朱甜", 288), ("齐瑞辰", 322)]:
    cy = y + 17
    row = [px[int(OX + S * dx), int(OY + S * cy)] for dx in range(16, 48)]
    nonwhite = [(i + 16, c) for i, c in enumerate(row) if not (c[0] > 246 and c[1] > 246 and c[2] > 246)]
    if nonwhite:
        print("  %-8s 头像水平 %.1f..%.1f 宽%.1f 中心色 %s  左缘色 %s"
              % (name, nonwhite[0][0], nonwhite[-1][0], nonwhite[-1][0] - nonwhite[0][0] + 1,
                 hexs(P((nonwhite[0][0] + nonwhite[-1][0]) / 2, cy)), hexs(nonwhite[0][1])))
print()
print("== 选中行右侧对勾 ==")
print("  最深:", darkest(270, 122, 300, 148))
xs = [dx for dx in range(260, 306) if sum(P(dx, 133)) / 3 < 200]
print("  对勾水平范围:", xs[:1], xs[-1:])
print()
print("== 滚动条（设计 left310 宽6 top118 高128）==")
print("  滑块色:", hexs(P(313, 180)), "  顶 y=118:", hexs(P(313, 118)), "  底 y=246:", hexs(P(313, 246)))
print("  轨道外 y=100:", hexs(P(313, 100)), "  y=260:", hexs(P(313, 260)))
print()
print("== 底部分隔线 y=416 ==", hexs(P(160, 416)), " y=415:", hexs(P(160, 415)), " y=417:", hexs(P(160, 417)))
print()
print("== 主按钮（设计 top~432 高32）==")
for dy in (420, 424, 428, 430, 432, 436, 448, 452, 456, 460, 464, 468):
    print("   y=%d  %s" % (dy, hexs(P(160, dy))))
ys = [dy for dy in range(415, 480) if P(160, dy)[2] > 200 and P(160, dy)[0] < 120]
print("  按钮蓝色竖直范围:", ys[0], "..", ys[-1], " 高", ys[-1] - ys[0] + 1)
xs = [dx for dx in range(0, 320) if P(dx, 448)[2] > 200 and P(dx, 448)[0] < 120]
print("  按钮蓝色水平范围:", xs[0], "..", xs[-1], " 宽", xs[-1] - xs[0] + 1)
print("  按钮文字色/字形:", glyph_rows(120, 436, 200, 462, thr=250), darkest(120, 436, 200, 462))
