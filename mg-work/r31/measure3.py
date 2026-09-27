# -*- coding: utf-8 -*-
"""转派浮窗 三次精量：图标 / 头像字号 / 文字边界 / 分隔线。原点 PNG(60,44)。"""
from PIL import Image

im = Image.open("mg-work/r31/design/dispatch.png").convert("RGB")
px = im.load()
OX, OY, S = 60, 44, 2


def hx(c):
    return "#%02X%02X%02X" % c


def to_png(dx, dy):
    return int(round(OX + S * dx)), int(round(OY + S * dy))


def bbox(pred, x0, x1, y0, y1):
    xs, ys = [], []
    for dx in range(int(x0 * 2), int(x1 * 2)):
        for dy in range(int(y0 * 2), int(y1 * 2)):
            x, y = to_png(dx / 2, dy / 2)
            if pred(px[x, y]):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return dict(x0=round((xs[0] - OX) / S, 1), x1=round((xs[-1] - OX) / S, 1), w=round((xs[-1] - xs[0] + 1) / S, 1),
                y0=round((ys[0] - OY) / S, 1), y1=round((ys[-1] - OY) / S, 1), h=round((ys[-1] - ys[0] + 1) / S, 1))


dark = lambda t: (lambda c: sum(c) / 3 < t)
blue = lambda c: c[2] - c[0] > 60 and c[2] > 150
whiteish = lambda c: c[0] > 235 and c[1] > 235 and c[2] > 235
gray = lambda c: 100 < sum(c) / 3 < 200

print("== 放大镜图标（排除 #E5E5E5 边框）==")
print("  ", bbox(lambda c: gray(c) and not (c[0] == c[1] == c[2] and c[0] in (229,)), 17, 44, 74, 98))
print("   采样: ", [(d, hx(px[to_png(d, 84)[0], to_png(d, 84)[1]])) for d in (20, 22, 24, 26, 28, 30, 32)])

print()
print("== 选中行对勾（蓝色像素）==")
print("  ", bbox(blue, 260, 302, 120, 148))

print()
print("== 头像白字 ink ==")
for name, y in [("邵禹铭", 118), ("秦怡", 152), ("韩佳毅", 186)]:
    print("   %-5s" % name, bbox(whiteish, 24, 44, y + 2, y + 30))

print()
print("== 行1 文字 ink（阈值 150，排除浅蓝底）==")
print("  ", bbox(dark(150), 46, 280, 122, 146))
print("   分列：对勾左界前：", bbox(dark(150), 46, 275, 122, 146))

print()
print("== 标题 ink（阈值扫描）==")
for t in (170, 200, 220, 240):
    print("   thr=%d" % t, bbox(dark(t), 10, 130, 10, 40))

print()
print("== 副标题 ink（阈值扫描）==")
for t in (170, 200, 220, 240):
    print("   thr=%d" % t, bbox(dark(t), 10, 300, 40, 64))

print()
print("== 搜索占位 ink（阈值扫描，x 起 40 避开图标）==")
for t in (170, 200, 220, 240):
    print("   thr=%d" % t, bbox(dark(t), 40, 160, 74, 98))

print()
print("== 分隔线精确 y（x=160 竖直）==")
for dy in range(410, 420):
    print("   y=%d %s" % (dy, hx(px[to_png(160, dy)[0], to_png(160, dy)[1]])))

print()
print("== 按钮白字 ink ==")
print("  ", bbox(whiteish, 100, 220, 434, 462))

print()
print("== 面板阴影范围（左下角外）==")
for dx in range(-8, 1):
    print("   x=%d y=470 %s   y=250 %s" % (dx, hx(px[to_png(dx, 470)[0], to_png(dx, 470)[1]]),
                                          hx(px[to_png(dx, 250)[0], to_png(dx, 250)[1]])))
for dy in range(478, 492):
    print("   y=%d x=160 %s" % (dy, hx(px[to_png(160, dy)[0], to_png(160, dy)[1]])))
