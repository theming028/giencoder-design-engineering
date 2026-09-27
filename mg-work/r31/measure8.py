# -*- coding: utf-8 -*-
"""第 31 轮设计稿精量 v8 —— 字形档位（列/行 ink 连续段）+ 对勾 + 面板圆角拟合 + 头像字形"""
from PIL import Image

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


def runs(flags, coords):
    """把 bool 序列切成连续 True 段，返回 [(起, 止)]（用 coords 映射）"""
    out = []
    i = 0
    while i < len(flags):
        if flags[i]:
            j = i
            while j + 1 < len(flags) and flags[j + 1]:
                j += 1
            out.append((coords[i], coords[j + 1]))
            i = j + 1
        else:
            i += 1
    return out


print("=" * 74)
print("A. 行 2（秦怡）文字：x 46..175 的竖向 ink 连续段（每个 CJK 字 = 1 段）")
prof = []
for xx in [46 + i * 0.5 for i in range(0, 260)]:
    hit = False
    for yy in [156 + i * 0.5 for i in range(0, 60)]:
        a, b = d2p(xx, yy)
        if lum(px[a, b]) < 200:
            hit = True; break
    prof.append(hit)
xs = [46 + i * 0.5 for i in range(0, 260)]
for a, b in runs(prof, xs):
    print("  段 x %.1f..%.1f  宽 %.1f" % (a, b, b - a))

print("=" * 74)
print("B. 行 2 名字「秦怡」的横向 ink 连续段（形高 = 字号参考）")
prof = []
ys = [156 + i * 0.5 for i in range(0, 60)]
for yy in ys:
    hit = False
    for xx in [53 + i * 0.5 for i in range(0, 40)]:
        a, b = d2p(xx, yy)
        if lum(px[a, b]) < 200:
            hit = True; break
    prof.append(hit)
for a, b in runs(prof, ys):
    print("  段 y %.1f..%.1f  高 %.1f" % (a, b, b - a))

print("=" * 74)
print("C. 选中行对勾（严判 c[2]-c[0]>120）")
xs2, ys2 = [], []
for yy in [118 + i * 0.5 for i in range(0, 64)]:
    for xx in [270 + i * 0.5 for i in range(0, 68)]:
        a, b = d2p(xx, yy)
        c = px[a, b]
        if c[2] - c[0] > 120:
            xs2.append(xx); ys2.append(yy)
if xs2:
    print("  对勾 design x %.1f..%.1f (w %.1f)  y %.1f..%.1f (h %.1f)" % (
        min(xs2), max(xs2), max(xs2) - min(xs2),
        min(ys2), max(ys2), max(ys2) - min(ys2)))
    print("  色 %s" % hexs(px[d2p((min(xs2) + max(xs2)) / 2, (min(ys2) + max(ys2)) / 2)[0],
                            d2p(0, (min(ys2) + max(ys2)) / 2)[1]]))

print("=" * 74)
print("D. 头像白字（秦怡行，x 25..43 / y top+4..top+28）")
gx, gy = [], []
for yy in [156 + i * 0.5 for i in range(0, 24)]:
    for xx in [25 + i * 0.5 for i in range(0, 38)]:
        a, b = d2p(xx, yy)
        c = px[a, b]
        if lum(c) > 210 and (max(c) - min(c)) < 30:
            gx.append(xx); gy.append(yy)
if gx:
    print("  白字 ink x %.1f..%.1f (w %.1f)  y %.1f..%.1f (h %.1f)" % (
        min(gx), max(gx), max(gx) - min(gx), min(gy), max(gy), max(gy) - min(gy)))

print("=" * 74)
print("E. 面板圆角拟合：逐 design y 找面板最左「非白」像素")
for yy in [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    for xx in [i * 0.5 for i in range(0, 30)]:
        a, b = d2p(xx, yy)
        c = px[a, b]
        if lum(c) < 250:
            print("  y=%-4s 最左非白 x=%.1f  色 %s" % (yy, xx, hexs(c)))
            break
    else:
        print("  y=%-4s 无" % yy)

print("=" * 74)
print("F. 选择行蓝底圆角：逐 y 找蓝底（含边框）最左 x")
for yy in [118, 118.5, 119, 120, 121, 122, 123, 124, 125]:
    for xx in [i * 0.5 for i in range(24, 80)]:
        a, b = d2p(xx, yy)
        c = px[a, b]
        if c[2] - c[0] > 12:
            print("  y=%-6s 最左 x=%.1f 色 %s" % (yy, xx, hexs(c)))
            break
    else:
        print("  y=%-6s 无" % yy)

print("=" * 74)
print("G. 搜索框「搜索成员」占位字形段")
prof = []
xs3 = [48 + i * 0.5 for i in range(0, 130)]
for xx in xs3:
    hit = False
    for yy in [76 + i * 0.5 for i in range(0, 40)]:
        a, b = d2p(xx, yy)
        if lum(px[a, b]) < 200:
            hit = True; break
    prof.append(hit)
for a, b in runs(prof, xs3):
    print("  段 x %.1f..%.1f 宽 %.1f" % (a, b, b - a))

print("=" * 74)
print("H. 标题「将任务转派给：」字形段（字号核对）")
prof = []
xs4 = [16 + i * 0.5 for i in range(0, 110)]
for xx in xs4:
    hit = False
    for yy in [16 + i * 0.5 for i in range(0, 26)]:
        a, b = d2p(xx, yy)
        if lum(px[a, b]) < 150:
            hit = True; break
    prof.append(hit)
for a, b in runs(prof, xs4):
    print("  段 x %.1f..%.1f 宽 %.1f" % (a, b, b - a))

print("=" * 74)
print("I. 按钮「确定转派」字形段")
prof = []
xs5 = [125 + i * 0.5 for i in range(0, 80)]
for xx in xs5:
    hit = False
    for yy in [436 + i * 0.5 for i in range(0, 24)]:
        a, b = d2p(xx, yy)
        c = px[a, b]
        if lum(c) > 235:
            hit = True; break
    prof.append(hit)
for a, b in runs(prof, xs5):
    print("  段 x %.1f..%.1f 宽 %.1f" % (a, b, b - a))
