# -*- coding: utf-8 -*-
"""第 31 轮设计稿精量 v10 —— 收口两项：行圆角(严阈值) + 头像字形(圆内) + 图标/副标题最暗色"""
from PIL import Image

PNG = "mg-work/r31/design/dispatch.png"
OX, OY, S = 60, 44, 2.0
im = Image.open(PNG).convert("RGB")
W, H = im.size
px = im.load()


def d2p(x, y):
    return (int(round(OX + x * S)), int(round(OY + y * S)))


def hexs(c):
    return "#%02X%02X%02X" % c


def lum(c):
    return (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000


def near(c, t, tol):
    return all(abs(c[i] - t[i]) <= tol for i in range(3))


print("=" * 74)
print("A. 选中行蓝底圆角（严阈值：只认 #ECF2FF 或 #D3E2FF ±2）")
for dy in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8]:
    y = 118 + dy
    hit = None
    for xx in [i * 0.25 for i in range(56, 130)]:
        c = px[d2p(xx, y)]
        if near(c, (236, 242, 255), 2) or near(c, (211, 226, 255), 2):
            hit = xx; break
    print("  dy=%-4s 最左 x=%s" % (dy, ("%.2f" % hit) if hit else "无"))

print("=" * 74)
print("B. 头像字形（严格圆内 x 27..41, y top+4..top+28；环色滤除）")
rows = [("铭/邵禹铭", 118, (229, 116, 112)), ("怡/秦怡", 152, (232, 139, 77)),
        ("毅/韩佳毅", 186, (220, 171, 53)), ("帆/顾帆", 220, (162, 193, 67)),
        ("怡/姜嘉怡", 254, (103, 184, 93)), ("甜/朱甜", 288, (71, 194, 196)),
        ("辰/齐瑞辰", 322, (76, 147, 212))]
for name, top, ring in rows:
    gx, gy = [], []
    for yy in [top + 6 + i * 0.25 for i in range(0, 81)]:
        for xx in [26 + i * 0.25 for i in range(0, 57)]:
            # 圆内判定
            if ((xx - 34) ** 2 + (yy - (top + 16)) ** 2) > 81:
                continue
            c = px[d2p(xx, yy)]
            if lum(c) > 220 and (max(c) - min(c)) < 40:
                gx.append(xx); gy.append(yy)
    if gx:
        print("  %-10s 白字 ink x %.2f..%.2f (w %.2f)  y %.2f..%.2f (h %.2f)  → 形高 %.1f"
              % (name, min(gx), max(gx), max(gx) - min(gx), min(gy), max(gy),
                 max(gy) - min(gy), max(gy) - min(gy)))
    else:
        print("  %-10s 无" % name)

print("=" * 74)
print("C. 副标题 / 放大镜 / 工号 的最暗像素（定色档）")
for label, box in [("副标题", (16, 44, 240, 58)), ("放大镜", (26, 78, 42, 94)),
                   ("占位字", (50, 76, 110, 96)), ("工号", (86, 156, 164, 180)),
                   ("滚动条", (309, 120, 317, 240))]:
    x0, y0, x1, y1 = box
    best = None
    for yy in [y0 + i * 0.25 for i in range(0, int((y1 - y0) * 4) + 1)]:
        for xx in [x0 + i * 0.25 for i in range(0, int((x1 - x0) * 4) + 1)]:
            c = px[d2p(xx, yy)]
            if best is None or lum(c) < best[0]:
                best = (lum(c), c, xx, yy)
    print("  %-8s 最暗 %s (lum %.0f) @ (%.1f, %.1f)" % (label, hexs(best[1]), best[0], best[2], best[3]))
