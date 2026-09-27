# -*- coding: utf-8 -*-
"""转派浮窗 四次精量：图标 ink（修正版 bbox）。原点 PNG(60,44)，1 设计像素 = 2 PNG 像素。"""
from PIL import Image

im = Image.open("mg-work/r31/design/dispatch.png").convert("RGB")
px = im.load()
OX, OY, S = 60, 44, 2


def hx(c):
    return "#%02X%02X%02X" % c


def bbox(dx0, dx1, dy0, dy1, pred, name=""):
    """设计坐标区间 → ink bbox（返回设计坐标）"""
    xs, ys = [], []
    for pxx in range(int(OX + S * dx0), int(OX + S * dx1)):
        for pxy in range(int(OY + S * dy0), int(OY + S * dy1)):
            if pred(px[pxx, pxy]):
                xs.append(pxx)
                ys.append(pxy)
    if not xs:
        print("  %s: 无 ink" % name)
        return None
    r = dict(x0=round((xs[0] - OX) / S, 1), x1=round((xs[-1] - OX) / S, 1),
             y0=round((ys[0] - OY) / S, 1), y1=round((ys[-1] - OY) / S, 1))
    r["w"] = round(r["x1"] - r["x0"] + 1 / S, 1)
    r["h"] = round(r["y1"] - r["y0"] + 1 / S, 1)
    print("  %-16s x %.1f..%.1f (w %.1f)   y %.1f..%.1f (h %.1f)" % (name, r["x0"], r["x1"], r["w"], r["y0"], r["y1"], r["h"]))
    return r


is_ink = lambda c: sum(c) / 3 < 205 and not (abs(c[0] - 229) < 6 and abs(c[1] - 229) < 6 and abs(c[2] - 229) < 6)
is_blue = lambda c: c[2] - c[0] > 50 and c[2] > 140
is_white = lambda c: c[0] > 240 and c[1] > 240 and c[2] > 240

print("== 搜索框放大镜 ==")
bbox(18, 46, 72, 100, is_ink, "放大镜(含边框?)")
bbox(18, 46, 72, 100, lambda c: sum(c) / 3 < 190 and not (abs(c[0] - c[1]) < 4 and abs(c[1] - c[2]) < 4 and c[0] > 220), "放大镜-纯")
# 逐行扫描放大镜区域
print("  逐行（x 18..46，标 M=像素暗）:")
for dy in range(74, 98):
    row = "".join("M" if sum(px[int(OX + S * dx), int(OY + S * dy)]) / 3 < 190 else "." for dx in range(18, 46))
    print("     y=%3d %s" % (dy, row))

print()
print("== 选中行对勾（蓝色）==")
bbox(270, 302, 120, 148, is_blue, "对勾")
for dy in range(126, 144):
    row = "".join("B" if is_blue(px[int(OX + S * dx), int(OY + S * dy)]) else "." for dx in range(276, 298))
    print("     y=%3d %s" % (dy, row))

print()
print("== 头像白字 ==")
for name, y in [("邵禹铭", 118), ("秦怡", 152), ("韩佳毅", 186), ("顾帆", 220), ("姜嘉怡", 254), ("朱甜", 288), ("齐瑞辰", 322)]:
    bbox(24, 44, y + 1, y + 31, is_white, name)

print()
print("== 头像圆几何（按「非白」找环）==")
for name, y in [("邵禹铭", 118), ("秦怡", 152)]:
    cy = y + 16
    xs = [dx for dx in [x / 2 for x in range(2 * 14, 2 * 52)]
          if not all(v > 246 for v in px[int(OX + S * dx), int(OY + S * cy)])]
    ys = [dy for dy in [yy / 2 for yy in range(2 * (y - 6), 2 * (y + 30))]
          if not all(v > 246 for v in px[int(OX + S * 34), int(OY + S * dy)])]
    print("   %-6s x %.1f..%.1f (%.1f)   y %.1f..%.1f (%.1f)" % (name, xs[0], xs[-1], xs[-1] - xs[0] + .5, ys[0], ys[-1], ys[-1] - ys[0] + .5))

print()
print("== 面板边框色 ==", hx(px[OX, int(OY + S * 240)]), hx(px[int(OX + S * 160), int(OY + S * 479)]))
