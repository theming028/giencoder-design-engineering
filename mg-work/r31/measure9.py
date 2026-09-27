# -*- coding: utf-8 -*-
"""第 31 轮设计稿精量 v9 —— alpha 通道量面板圆角 + 头像字形（圆内）+ 次级文字色"""
from PIL import Image

PNG = "mg-work/r31/design/dispatch.png"
OX, OY, S = 60, 44, 2.0
im = Image.open(PNG).convert("RGBA")
W, H = im.size
px = im.load()


def d2p(x, y):
    return (int(round(OX + x * S)), int(round(OY + y * S)))


def hexs(c):
    return "#%02X%02X%02X" % c[:3]


def lum(c):
    return (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000


print("=" * 74)
print("A. alpha 通道：面板实体（alpha>250）逐 design y 的最左 x -> 推圆角")
print("   上左角：")
for yy in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
    for xx in [i * 0.5 for i in range(0, 40)]:
        a, b = d2p(xx, yy)
        if px[a, b][3] > 250:
            print("     y=%-5s 最左 x=%.1f  %s" % (yy, xx, hexs(px[a, b])))
            break
    else:
        print("     y=%-5s 无实体" % yy)

print("   上右角（距右缘 320-x）：")
for yy in [0, 1, 2, 3, 4, 5, 6, 8, 10]:
    for xx in [319 - i * 0.5 for i in range(0, 40)]:
        a, b = d2p(xx, yy)
        if px[a, b][3] > 250:
            print("     y=%-5s 最右 x=%.1f (距右 %.1f)  %s" % (yy, xx, 320 - xx, hexs(px[a, b])))
            break
    else:
        print("     y=%-5s 无实体" % yy)

print("=" * 74)
print("B. 头像白字（圆内：距圆心 <=9）")
rows = [("邵禹铭", 118, "#E57470"), ("秦怡", 152, "#E88B4D"), ("韩佳毅", 186, "#DCAB35"),
        ("顾帆", 220, "#A2C143"), ("姜嘉怡", 254, "#67B85D"), ("朱甜", 288, "#47C2C4"),
        ("齐瑞辰", 322, "#4C93D4")]
cy_base = None
for name, top, ring in rows:
    gx, gy = [], []
    X0, X1 = 24, 44
    Y0, Y1 = top + 12, top + 20
    for yy in [Y0 + i * 0.25 for i in range(0, int((Y1 - Y0) * 4) + 1)]:
        for xx in [X0 + i * 0.25 for i in range(0, int((X1 - X0) * 4) + 1)]:
            a, b = d2p(xx, yy)
            c = px[a, b]
            if lum(c) > 210 and (max(c[:3]) - min(c[:3])) < 30:
                gx.append(xx); gy.append(yy)
    if gx:
        print("  %-8s 白字 ink x %.2f..%.2f (w %.2f)  y %.2f..%.2f (h %.2f)"
              % (name, min(gx), max(gx), max(gx) - min(gx),
                 min(gy), max(gy), max(gy) - min(gy)))
    else:
        print("  %-8s 无" % name)

print("=" * 74)
print("C. 行内「名字」与「(工号)」文字色（秦怡行，取 ink 最深处色）")
for label, x0, x1 in [("名字 秦怡", 52, 80), ("工号 (P0098603)", 86, 163)]:
    dark = None
    for yy in [156 + i * 0.5 for i in range(0, 48)]:
        for xx in [x0 + i * 0.5 for i in range(0, int((x1 - x0) * 2))]:
            a, b = d2p(xx, yy)
            c = px[a, b]
            if dark is None or lum(c) < dark[0]:
                dark = (lum(c), c, xx, yy)
    print("  %-18s 最暗 %s (lum %.0f) @ x%.1f y%.1f" % (label, hexs(dark[1]), dark[0], dark[2], dark[3]))

print("=" * 74)
print("D. 逐元素取色")
probes = [
    ("面板底", 160, 400), ("面板边框 左", 0, 300), ("面板边框 上", 160, 0),
    ("标题字", 20, 27), ("副标题字", 20, 50),
    ("搜索框边框", 16, 86), ("搜索框内底", 150, 86), ("占位字", 54, 86), ("放大镜", 30, 86),
    ("选中行底", 150, 134), ("选中行边框", 16.25, 134),
    ("hover行底", 150, 236), ("普通行底", 150, 168),
    ("工号字", 91, 168), ("分隔线", 160, 415.5), ("按钮底", 160, 448), ("按钮字", 136, 448),
    ("滚动条", 313, 180),
]
for label, x, y in probes:
    a, b = d2p(x, y)
    print("  %-14s design(%.2f,%.2f) %s" % (label, x, y, hexs(px[a, b])))
