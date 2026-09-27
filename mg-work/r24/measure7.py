# -*- coding: utf-8 -*-
"""精测：list 圆点几何/颜色、list 文本缩进；侧栏 label/value 起点；高优先级胶囊。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()


def runs(y, x0, x1, thr=200, gap=6, tag=""):
    out = []; inside = False; s = 0
    for x in range(x0, x1 + 1):
        hit = sum(px[x, y]) / 3 < thr
        if hit and not inside:
            inside = True; s = x
        elif not hit and inside:
            inside = False; out.append([s, x - 1])
    if inside:
        out.append([s, x1])
    m = []
    for r in out:
        if m and r[0] - m[-1][1] <= gap:
            m[-1][1] = r[1]
        else:
            m.append(r)
    print("  %s y=%d css %.1f -> %s" % (tag, y, y / 2.0,
          "  ".join("css%.1f..%.1f" % (a / 2.0, b / 2.0) for a, b in m[:8])))
    return m


def vruns(x, y0, y1, thr=200, tag=""):
    out = []; inside = False; s = 0
    for y in range(y0, y1 + 1):
        hit = sum(px[x, y]) / 3 < thr
        if hit and not inside:
            inside = True; s = y
        elif not hit and inside:
            inside = False; out.append((s, y - 1))
    if inside:
        out.append((s, y1))
    print("  %s x=%d css %.1f -> %s" % (tag, x, x / 2.0,
          "  ".join("css%.1f..%.1f(h%.1f)" % (a / 2.0, b / 2.0, (b - a + 1) / 2.0) for a, b in out)))
    return out


print("=== A. list 圆点几何（行 css 285..297.5 / device 570..595）===")
vruns(110, 560, 600, 200, "圆点竖切 x=110")
runs(582, 96, 700, 200, 6, "list 行1")
runs(606, 96, 700, 200, 6, "list 行2")
runs(630, 96, 700, 200, 6, "list 行3")
runs(534, 96, 700, 200, 6, "上一段(对照)")

print("\n=== B. 列表圆点像素矩阵（device x 104..124, y 574..594）===")
for y in range(574, 595):
    row = "".join("#" if sum(px[x, y]) / 3 < 200 else ("+" if sum(px[x, y]) / 3 < 246 else ".")
                  for x in range(104, 126))
    print("   y=%3d %s" % (y, row))
print("   圆点中心色 =", px[111, 584])

print("\n=== C. 侧栏 任务属性：label / value 起点 ===")
for dev_y, name in ((250, "状态(胶囊)"), (300, "执行人"), (330, "优先级"), (396, "项目"),
                    (480, "来源需求"), (640, "实际开始"), (700, "实际完成")):
    runs(dev_y, 1360, 1890, 200, 10, name)

print("\n=== D. 侧栏 h2 起点 ===")
runs(140, 1360, 1600, 200, 10, "任务属性 h2")

print("\n=== E. 高优先级胶囊（扫描底色 rgb(255,236,232)）===")
ys = [y for y in range(370, 430)]
for y in range(376, 420, 2):
    cs = [x for x in range(1540, 1720) if px[x, y][0] > 250 and 228 < px[x, y][1] < 244 and px[x, y][2] < 240]
    if cs:
        print("   y=%d css%.1f 胶囊底色 css x %.1f..%.1f  w=%.1f  色=%s"
              % (y, y / 2.0, min(cs) / 2.0, max(cs) / 2.0, (max(cs) - min(cs) + 1) / 2.0, px[cs[len(cs) // 2], y]))
