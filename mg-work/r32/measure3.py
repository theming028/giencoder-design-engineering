# -*- coding: utf-8 -*-
"""量取 v3：协作弹窗面板内部几何（coop.png 1440x900 1x）
输出坐标一律换算成「相对面板左上角」。
"""
from PIL import Image

im = Image.open("mg-work/r32/design/coop.png").convert("RGB")
px = im.load()


def c(x, y):
    return px[x, y]


def same(a, b, tol=5):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))


def row(y, x0, x1, minw=1):
    out, cur, s = [], c(x0, y), x0
    for x in range(x0 + 1, x1):
        v = c(x, y)
        if not same(v, cur, 4):
            if x - s >= minw:
                out.append((s, x - 1, cur))
            cur, s = v, x
    out.append((s, x1 - 1, cur))
    return out


def col(x, y0, y1, minh=1):
    out, cur, s = [], c(x, y0), y0
    for y in range(y0 + 1, y1):
        v = c(x, y)
        if not same(v, cur, 4):
            if y - s >= minh:
                out.append((s, y - 1, cur))
            cur, s = v, y
    out.append((s, y1 - 1, cur))
    return out


def show(tag, segs, off):
    print("  " + tag + ": " + "  ".join("%d..%d(%d)%s" % (a - off, b - off, b - a + 1, v) for a, b, v in segs))


def ink(x0, y0, x1, y1, thr=200):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if min(c(x, y)) < thr:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1) if xs else None


def rel(bb, ox, oy, tag):
    if not bb:
        print("  " + tag + ": None"); return
    print("  %s: x=%d y=%d w=%d h=%d" % (tag, bb[0] - ox, bb[1] - oy, bb[4], bb[5]))


# ---- 找面板精确边界 ----
print("=" * 96)
print("① 面板边界（面板底色≈#F9F9F9，遮罩区明显更暗）")
for y in (140, 400, 760):
    segs = [s for s in row(y, 30, 1430) if s[1] - s[0] > 30]
    print("   y=%d:" % y, [(a, b, b - a + 1, v) for a, b, v in segs])
for x in (100, 400, 800, 1100):
    segs = [s for s in col(x, 100, 880) if s[1] - s[0] > 30]
    print("   x=%d:" % x, [(a, b, b - a + 1, v) for a, b, v in segs])

print("=" * 96)
print("② 面板圆角剖面（左下角：找每行左缘 x）")
for y in range(755, 772):
    for x in range(55, 100):
        if same(c(x, y), (249, 249, 249), 8) or min(c(x, y)) > 220:
            print("   y=%d 左缘 x=%d (相对面板 %d)" % (y, x, x - 60)); break

print("=" * 96)
print("③ 步骤条（面板1）—— 横向 y=210，纵向 x=150")
show("y=210", row(210, 70, 700, 2), 60)
show("x=150", col(150, 186, 240), 130)
print("  步骤条上下缘 x=110:", [(a - 130, b - 130, v) for a, b, v in col(110, 180, 245, 1)])
print("  active 段圆角剖面（左上角）:")
for y in range(192, 202):
    for x in range(80, 110):
        if not same(c(x, y), (249, 249, 249), 8) and not same(c(x, y), (236, 242, 255), 8):
            print("     y=%d(面板%d) 左缘 x=%d(面板%d) %s" % (y, y - 130, x, x - 60, c(x, y))); break
print("  步骤1 文字:", ink(90, 195, 300, 235, 200), "→相对", )
b = ink(90, 195, 300, 235, 200)
if b: print("     x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))
print("  步骤2 文字:", end=" ")
b = ink(330, 195, 660, 235, 200)
if b: print("x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))

print("=" * 96)
print("④ divider 行（面板内 y≈110~120）")
for y in range(236, 274, 2):
    segs = row(y, 70, 700, 1)
    cols = set(s[2] for s in segs)
    if len(cols) > 1:
        print("   y=%d(面板%d) 段数=%d" % (y, y - 130, len(segs)), [(a - 60, b - 60, v) for a, b, v in segs][:6])
b = ink(120, 236, 660, 276, 210)
if b: print("  divider 文字墨色: x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))

print("=" * 96)
print("⑤ 列表区（面板内）")
print("  纵向 x=120:", [(a - 130, b - 130, v) for a, b, v in col(120, 280, 620, 2)])
print("  纵向 x=690(近右缘):", [(a - 130, b - 130, v) for a, b, v in col(690, 280, 620, 2)])
for y in (300, 320, 360, 500, 545):
    show("y=%d 横扫" % y, [s for s in row(y, 75, 695, 1)], 60)

print("=" * 96)
print("⑥ 单行结构（第 3 行 y≈362~396）")
show("y=380", [s for s in row(380, 75, 695, 1)], 60)
b = ink(100, 366, 145, 400, 210)
if b: print("  勾选框(墨): x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))
b2 = ink(148, 360, 500, 402, 210)
if b2: print("  文件名(墨): x=%d y=%d w=%d h=%d" % (b2[0] - 60, b2[1] - 130, b2[4], b2[5]))
print("  勾选蓝取色(面板内 40,235):", c(100, 365), c(103, 372))

print("=" * 96)
print("⑦ 底栏（面板1）")
b = ink(70, 700, 320, 760, 210)
if b: print("  已选文字: x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))
show("y=730", [s for s in row(730, 430, 700, 1)], 60)
b = ink(520, 705, 700, 760, 210)
if b: print("  按钮区墨色: x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))
for y in range(585, 600):
    pass
print("  按钮纵向 x=560:", [(a - 130, b - 130, v) for a, b, v in col(560, 700, 765, 1)])
print("  按钮纵向 x=620:", [(a - 130, b - 130, v) for a, b, v in col(620, 700, 765, 1)])
print("  取消文字:", end=" ")
b = ink(520, 710, 570, 758, 210)
if b: print("x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))
print("  下一步文字:", end=" ")
b = ink(590, 710, 680, 758, 210)
if b: print("x=%d y=%d w=%d h=%d" % (b[0] - 60, b[1] - 130, b[4], b[5]))

print("=" * 96)
print("⑧ 右面板（Step2 态）")
OX, OY = 740, 130
print("  步骤条 y=210:", [(a - OX, b - OX, v) for a, b, v in row(210, 750, 1380, 2)])
print("  已完成对勾 bbox:", end=" ")
bb = None
xs = []
for y in range(190, 235):
    for x in range(790, 860):
        v = c(x, y)
        if v[2] > 140 and v[2] - v[0] > 30:
            xs.append((x, y))
if xs:
    print("x=%d..%d y=%d..%d" % (min(p[0] for p in xs) - OX, max(p[0] for p in xs) - OX,
                                 min(p[1] for p in xs) - OY, max(p[1] for p in xs) - OY))
print("  搜索框纵向 x=800:", [(a - OY, b - OY, v) for a, b, v in col(800, 200, 280, 1)])
print("  搜索框横向 y=247:", [(a - OX, b - OX, v) for a, b, v in row(247, 750, 1380, 2)])
b = ink(770, 240, 1250, 262, 210)
if b: print("  搜索占位文字: x=%d y=%d w=%d h=%d" % (b[0] - OX, b[1] - OY, b[4], b[5]))
print("  成员行纵向 x=1180:", [(a - OY, b - OY, v) for a, b, v in col(1180, 260, 470, 1)][:14])
print("  成员行横向 y=337:", [(a - OX, b - OX, v) for a, b, v in row(337, 750, 1380, 1)][:14])
b = ink(770, 320, 1250, 360, 210)
if b: print("  成员行1文字: x=%d y=%d w=%d h=%d" % (b[0] - OX, b[1] - OY, b[4], b[5]))
print("  底栏按钮 y=730:", [(a - OX, b - OX, v) for a, b, v in row(730, 1150, 1390, 2)])
b = ink(1080, 700, 1380, 760, 210)
if b: print("  按钮区墨色: x=%d y=%d w=%d h=%d" % (b[0] - OX, b[1] - OY, b[4], b[5]))
b = ink(1070, 700, 1180, 760, 210)
if b: print("  左钮文字: x=%d y=%d w=%d h=%d" % (b[0] - OX, b[1] - OY, b[4], b[5]))
b = ink(1180, 700, 1290, 760, 210)
if b: print("  中钮文字: x=%d y=%d w=%d h=%d" % (b[0] - OX, b[1] - OY, b[4], b[5]))
print("  已选文字(panel2):", end=" ")
b = ink(750, 700, 1000, 760, 210)
if b: print("x=%d y=%d w=%d h=%d" % (b[0] - OX, b[1] - OY, b[4], b[5]))

print("=" * 96)
print("⑨ 关键色")
for tag, (x, y) in [("面板底", (600, 640)), ("面板底2", (1200, 640)), ("遮罩", (20, 500)),
                    ("列表容器底", (120, 300)), ("行底", (300, 380)),
                    ("active 步骤底", (200, 210)), ("inactive 步骤底", (500, 210)),
                    ("active 边框", (200, 195)), ("搜索框底", (900, 247))]:
    print("  %s (%d,%d) = %s" % (tag, x, y, c(x, y)))
