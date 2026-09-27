# -*- coding: utf-8 -*-
"""量取 v5：修正 seg（段的颜色取 cur 而非 v），补齐内容区底 / 成员行 / 搜索框"""
from PIL import Image

im = Image.open("mg-work/r32/design/coop.png").convert("RGB")
px = im.load()


def c(x, y):
    return px[x, y]


def same(a, b, tol=5):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))


def seg_row(y, x0, x1, minw=1):
    out, cur, s = [], c(x0, y), x0
    for x in range(x0 + 1, x1):
        v = c(x, y)
        if not same(v, cur, 4):
            if x - s >= minw:
                out.append((s, x - 1, cur))          # ★ 段的颜色是 cur（旧色）
            cur, s = v, x
    out.append((s, x1 - 1, cur))
    return out


def seg_col(x, y0, y1, minh=1):
    out, cur, s = [], c(x, y0), y0
    for y in range(y0 + 1, y1):
        v = c(x, y)
        if not same(v, cur, 4):
            if y - s >= minh:
                out.append((s, y - 1, cur))
            cur, s = v, y
    out.append((s, y1 - 1, cur))
    return out


def ink(x0, y0, x1, y1, thr=200):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if min(c(x, y)) < thr:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1) if xs else None


P1, P2, OY = 60, 740, 130

print("=" * 92)
print("① 面板1 纵向 x=1000（相对 260）—— 全高节奏")
print("  ", [(a - OY, b - OY, v) for a, b, v in seg_col(1000, 130, 775, 2)])

print("=" * 92)
print("② 面板2 纵向 x=940（相对 200）—— 全高节奏")
print("  ", [(a - OY, b - OY, v) for a, b, v in seg_col(940, 130, 775, 2)])

print("=" * 92)
print("③ 内容区左右边界（面板1 y=450 绝对 = 面板 320）")
print("  ", [(a - P1, b - P1, v) for a, b, v in seg_row(450, 70, 700, 1)][:10])
print("   面板2 y=450:")
print("  ", [(a - P2, b - P2, v) for a, b, v in seg_row(450, 750, 1390, 1)][:10])

print("=" * 92)
print("④ 面板2 搜索框（绝对 y=311 → 面板 181 中线）")
print("   y=311:", [(a - P2, b - P2, v) for a, b, v in seg_row(311, 750, 1390, 1)][:12])
print("   搜索框上下边框 x=1000(相对260):", [(a - OY, b - OY, v) for a, b, v in seg_col(1000, 280, 340, 1)])

print("=" * 92)
print("⑤ 面板2 成员行元素 x（行1 绝对 y 344..375，中心 359）")
for i in range(7):
    yc = 359 + i * 34
    b = ink(750, yc - 12, 1100, yc + 12, 235)
    print("   行%d(y=%d) 墨色/彩盒:" % (i + 1, yc), None if not b else
          "x=%d..%d(面板 %d..%d) y=%d..%d" % (b[0], b[2], b[0] - P2, b[2] - P2, b[1] - OY, b[3] - OY))
print("   行1 细分（checkbox/头像/文字）：")
print("     全宽 ink 阈值235:", ink(750, 347, 1100, 372, 235))
print("     蓝/彩像素:", end=" ")
xs = []
for y in range(347, 372):
    for x in range(750, 1100):
        v = c(x, y)
        if max(v) - min(v) > 25:
            xs.append(x)
print("x %d..%d（面板 %d..%d）" % (min(xs), max(xs), min(xs) - P2, max(xs) - P2) if xs else None)

print("=" * 92)
print("⑥ 面板1 行1 元素（绝对 y 296..327，中心 311）")
print("   y=311:", [(a - P1, b - P1, v) for a, b, v in seg_row(311, 70, 700, 1)][:14])
print("   勾选框 ink:", ink(100, 300, 125, 325, 235), "→ 面板", end=" ")
b = ink(100, 300, 125, 325, 235)
print(None if not b else "x=%d..%d" % (b[0] - P1, b[2] - P1))
print("   文件名 ink(面板 64..200):", end=" ")
b = ink(124, 300, 260, 325, 215)
print(None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))

print("=" * 92)
print("⑦ divider 文字精量（阈值 170，避抗锯齿）")
b = ink(150, 240, 640, 285, 170)
print("   ", None if not b else "x=%d..%d y=%d..%d w=%d h=%d（面板）" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))
print("   divider 线 y 精扫 x=250(相对190):", [(a - OY, b - OY, v) for a, b, v in seg_col(250, 240, 275, 1)])
print("   divider 线右端 x 精扫 y=257:", [(a - P1, b - P1, v) for a, b, v in seg_row(257, 420, 700, 1)][:10])

print("=" * 92)
print("⑧ 步骤条文字字号（阈值 170）")
b = ink(180, 200, 290, 230, 170)
print("   step1 '选择阶段产物':", None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))
b = ink(500, 200, 600, 230, 190)
print("   step2 '选择协作者':", None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))

print("=" * 92)
print("⑨ 底栏文字字号（阈值 170）")
b = ink(80, 715, 300, 750, 190)
print("   '已选 8/8 个产物':", None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))
b = ink(530, 715, 610, 750, 190)
print("   '取消':", None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))
b = ink(570, 720, 610, 748, 250)
print("   下一步 白字墨色:", None if not b else "x=%d..%d y=%d..%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY))

print("=" * 92)
print("⑩ 标题与关闭 X")
b = ink(70, 140, 300, 180, 170)
print("   标题:", None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))
b = ink(640, 140, 700, 185, 190)
print("   关闭 X:", None if not b else "x=%d..%d y=%d..%d w=%d h=%d" % (b[0] - P1, b[2] - P1, b[1] - OY, b[3] - OY, b[4], b[5]))
