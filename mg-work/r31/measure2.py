# -*- coding: utf-8 -*-
"""转派浮窗 二次精量（换算原点校准为 PNG(60,44)，即 design_x=(png-60)/2）。"""
from PIL import Image

im = Image.open("mg-work/r31/design/dispatch.png").convert("RGB")
px = im.load()
OX, OY, S = 60, 44, 2


def hx(c):
    return "#%02X%02X%02X" % c


def P(dx, dy):
    return px[int(round(OX + S * dx)), int(round(OY + S * dy))]


def ink_bbox(x0, x1, y0, y1, thr=235):
    xs, ys = [], []
    for x in range(int(OX + S * x0), int(OX + S * x1)):
        for y in range(int(OY + S * y0), int(OY + S * y1)):
            if sum(px[x, y]) / 3 < thr:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return (round((xs[0] - OX) / S, 1), round((xs[-1] - OX) / S, 1), round((xs[-1] - xs[0] + 1) / S, 1),
            round((ys[0] - OY) / S, 1), round((ys[-1] - OY) / S, 1), round((ys[-1] - ys[0] + 1) / S, 1))


print("== 校准校验：搜索框 x=160 竖扫 66..106 ==")
for dy in range(66, 107):
    c = hx(P(160, dy))
    if c != "#FFFFFF":
        print("   y=%d %s" % (dy, c))
print("   左缘 x=13..20 @y=86:", [(x, hx(P(x, 86))) for x in range(13, 21)])
print("   右缘 x=300..308 @y=86:", [(x, hx(P(x, 86))) for x in range(300, 309)])

print()
print("== 面板圆角（用非白判定，避开阴影影响：取第 1 层「明显非白」）==")
for dy in range(0, 10):
    row = "".join("#" if sum(P(dx, dy)) / 3 > 250 else "." for dx in range(0, 12))
    print("   y=%2d %s" % (dy, row))

print()
print("== 头像色（多点采样，取众数）==")
AX = 23.0
for name, y in [("邵禹铭", 118), ("秦怡", 152), ("韩佳毅", 186), ("顾帆", 220),
                ("姜嘉怡", 254), ("朱甜", 288), ("齐瑞辰", 322)]:
    cy = y + 16
    samples = []
    for ddx in (-6, -5, 5, 6):
        for ddy in (-3, 0, 3):
            samples.append(P(AX + 10 + ddx, cy + ddy))
    cnt = {}
    for c in samples:
        cnt[c] = cnt.get(c, 0) + 1
    top = sorted(cnt.items(), key=lambda kv: -kv[1])
    print("   %-6s 主色 %s (x%d)  备选 %s" % (name, hx(top[0][0]), top[0][1],
                                             ", ".join(hx(c) for c, _ in top[1:3])))

print()
print("== 头像 ink 边界（含白字）==")
for name, y in [("邵禹铭", 118), ("秦怡", 152)]:
    cy = y + 16
    xs = [x for x in range(int(OX + S * 14), int(OX + S * 52)) if P((x - OX) / S, cy) != (255, 255, 255)]
    print("   %s 环 x %.1f..%.1f" % (name, (xs[0] - OX) / S, (xs[-1] - OX) / S))

print()
print("== 搜索图标（放大镜）ink bbox ==", ink_bbox(16, 40, 76, 98))
print("== 选中行对勾 ink bbox ==", ink_bbox(275, 302, 120, 146))
print("== 选中行对勾最深色 ==", hx(min((P(x / S, y / S) for x in range(int(OX + S * 275), int(OX + S * 302))
                                       for y in range(int(OY + S * 120), int(OY + S * 146))), key=sum)))
print()
print("== 文字 ink bbox（x0,x1,宽,y0,y1,高）==")
print("   标题「将任务转派给：」:", ink_bbox(10, 130, 12, 36))
print("   副标题:", ink_bbox(10, 310, 38, 62))
print("   搜索占位「搜索成员」:", ink_bbox(38, 160, 74, 98))
print("   行1「邵禹铭 (P0098602)」:", ink_bbox(46, 300, 120, 146))
print("   行1「邵禹铭」3 字:", ink_bbox(46, 100, 120, 146))
print("   行2「秦怡 (P0098603)」:", ink_bbox(46, 300, 154, 180))
print("   按钮文字「确定转派」:", ink_bbox(120, 200, 434, 462, thr=200))
print()
print("== 选中行/普通行 行高与圆角 ==")
print("   选中行左缘 x=12..22 @y=132:", [(x, hx(P(x, 132))) for x in range(12, 23)])
print("   选中行右缘 x=296..308 @y=132:", [(x, hx(P(x, 132))) for x in range(296, 309)])
print("   选中行角 y=120..124 @x=16..24:")
for dy in range(119, 126):
    print("      y=%d %s" % (dy, [(x, hx(P(x, dy))) for x in range(16, 24)]))
print()
print("== 搜索框圆角 左上角 ==")
for dy in range(69, 76):
    print("   y=%d %s" % (dy, "".join("E" if hx(P(dx, dy)) == "#E5E5E5" else ("." if hx(P(dx, dy)) == "#FFFFFF" else "?")
                                     for dx in range(13, 25))))
print()
print("== 滚动条精确 ==")
for dy in [110, 116, 117, 118, 119, 200, 240, 244, 245, 246, 247, 250]:
    print("   y=%3d 切片 x=306..316: %s" % (dy, [hx(P(x, dy)) for x in range(306, 317)]))
