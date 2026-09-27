# -*- coding: utf-8 -*-
"""量取 v4：步骤条尖角几何 / divider 线 / Step2 成员行"""
from PIL import Image

im = Image.open("mg-work/r32/design/coop.png").convert("RGB")
px = im.load()


def c(x, y):
    return px[x, y]


def same(a, b, tol=5):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))


P1, P2 = 60, 740        # 两面板左缘（绝对）
OY = 130


def seg_row(y, x0, x1, minw=1):
    out, cur, s = [], c(x0, y), x0
    for x in range(x0 + 1, x1):
        v = c(x, y)
        if not same(v, cur, 4):
            if x - s >= minw:
                out.append((s, x - 1, v))
            cur, s = v, x
    out.append((s, x1 - 1, cur))
    return out


print("=" * 90)
print("① 步骤条 active 段（面板1）逐行右缘 —— 量尖角几何")
for y in range(193, 226):
    segs = seg_row(y, 80, 700, 2)
    # 找最后一个非面板底的段起点（active 蓝区终点）
    blue = [(a, b, v) for a, b, v in segs if v[2] > 240 and v[0] > 200 and v[2] - v[1] > 20]
    # 用：不是 (249,249,249) 也不是 (248,248,248) 的连续区
    body = [(a, b, v) for a, b, v in segs if not same(v, (249, 249, 249), 3) and not same(v, (248, 248, 248), 3)]
    if body:
        left = body[0][0]; right = body[-1][1]
        print("   y=%d(面板%d) 左缘 %d 右缘 %d 段数=%d" % (y, y - OY, left - P1, right - P1, len(body)))

print("=" * 90)
print("② 步骤条 step2(灰) 左缘逐行（凹陷尖角）")
for y in range(193, 226):
    segs = seg_row(y, 80, 700, 2)
    grey = [(a, b, v) for a, b, v in segs if same(v, (242, 242, 242), 4)]
    if grey:
        print("   y=%d(面板%d) 灰段 %d..%d" % (y, y - OY, grey[0][0] - P1, grey[-1][1] - P1))

print("=" * 90)
print("③ 右面板 step2(蓝) 左缘逐行（凹陷尖角，应对称）")
for y in range(193, 226):
    segs = seg_row(y, 750, 1390, 2)
    blue = [(a, b, v) for a, b, v in segs if same(v, (236, 242, 255), 6) or same(v, (211, 226, 255), 6)]
    if blue:
        print("   y=%d(面板%d) 蓝段 %d..%d" % (y, y - OY, blue[0][0] - P2, blue[-1][1] - P2))

print("=" * 90)
print("④ divider 线（面板1，y=256 绝对 = 面板 126）")
for y in (254, 255, 256, 257, 258):
    segs = seg_row(y, 80, 700, 3)
    print("   y=%d(面板%d):" % (y, y - OY), [(a - P1, b - P1, v) for a, b, v in segs if b - a > 3][:8])
print("   线色取样:", [(x, c(x, 256)) for x in (100, 150, 200, 300, 450, 550, 600)])
print("   线右端: ", [(x - P1, c(x, 256)) for x in range(430, 470, 2)])

print("=" * 90)
print("⑤ Step2 搜索框（面板2）")
for y in (180, 181, 182, 196, 197, 198):
    segs = seg_row(y, 750, 1390, 1)
    print("   y=%d(面板%d):" % (y, y - OY), [(a - P2, b - P2, v) for a, b, v in segs if b - a > 1][:10])
print("  纵向 x=1000(面板260):", [(a - OY, b - OY, v) for a, b, v in [(s[0], s[1], s[2]) for s in []]] or "")
col = []
cur, s = c(1000, 150), 150
for y in range(151, 320):
    v = c(1000, y)
    if not same(v, cur, 4):
        col.append((s - OY, y - 1 - OY, cur)); cur, s = v, y
col.append((s - OY, 319 - OY, cur))
print("  纵向 x=1000:", [(a, b, v) for a, b, v in col if b - a > 0])

print("=" * 90)
print("⑥ Step2 成员行（面板2，pitch 34）")
for i in range(3):
    yc = 337 + i * 34
    segs = seg_row(yc, 750, 1390, 1)
    print("   y=%d(面板%d):" % (yc, yc - OY), [(a - P2, b - P2, v) for a, b, v in segs][:18])


def ink(x0, y0, x1, y1, thr=200):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if min(c(x, y)) < thr:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1) if xs else None


print()
print("  成员行1（邵禹铭 y 322..356）逐元素：")
print("   checkbox:", ink(785, 322, 815, 356, 220))
print("   头像:", ink(815, 322, 860, 356, 230))
print("   姓名:", ink(860, 322, 1080, 356, 200))
print("  行1 底:", c(1000, 340), " 行2 底:", c(1000, 374), " 行3 底:", c(1000, 408))
print("  行灰色范围 x=1300:", end=" ")
cur, s = c(1300, 300), 300
for y in range(301, 500):
    v = c(1300, y)
    if not same(v, cur, 4):
        print("%d..%d%s" % (s - OY, y - 1 - OY, cur), end=" ")
        cur, s = v, y
print()

print("=" * 90)
print("⑦ Step2 内容区白卡边界（面板2）")
for y in (300, 400, 480):
    segs = seg_row(y, 745, 1395, 2)
    print("   y=%d(面板%d):" % (y, y - OY), [(a - P2, b - P2, v) for a, b, v in segs if b - a > 2][:8])
print("  纵向 x=1350(面板610):", end=" ")
cur, s = c(1350, 140), 140
out = []
for y in range(141, 560):
    v = c(1350, y)
    if not same(v, cur, 4):
        out.append("%d..%d%s" % (s - OY, y - 1 - OY, cur)); cur, s = v, y
print(" ".join(out))
