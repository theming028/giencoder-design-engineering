# -*- coding: utf-8 -*-
"""从设计稿看板图里量三个标签的底色与文字色：找『有饱和度』的色块 = 标签底色。"""
import collections
from PIL import Image

SRC = "mg-work/kanban/root/board-design.png"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()
print("design board size =", W, "x", H)


def sat(c):
    r, g, b = c
    return max(r, g, b) - min(r, g, b)


def boxes(x0, x1, y0, y1, minsat=14, minrun=12):
    """在区域内找出饱和度 >= minsat 的连通横向色块（简化：逐行找 x 运行区间，再按 y 合并）。"""
    rects = []
    active = {}  # key = (xl, xr) rough -> [y0,y1,colors]
    for y in range(y0, y1):
        x = x0
        while x < x1:
            if sat(px[x, y]) >= minsat:
                xs = x
                while x < x1 and sat(px[x, y]) >= minsat:
                    x += 1
                xe = x - 1
                if xe - xs + 1 >= minrun:
                    # 合并到已有
                    merged = False
                    for k in list(active.keys()):
                        if abs(k[0] - xs) <= 6 and abs(k[1] - xe) <= 6 and y - active[k][1] <= 2:
                            rec = active.pop(k)
                            rec[1] = y
                            rec[2] += 1
                            active[(min(k[0], xs), max(k[1], xe))] = rec
                            merged = True
                            break
                    if not merged:
                        active[(xs, xe)] = [y, y, 1]
            else:
                x += 1
    for k, v in active.items():
        if v[2] >= 4:  # 至少 4 行
            rects.append((k[0], k[1], v[0], v[1]))
    return sorted(rects, key=lambda r: (r[2], r[0]))


for col, (x0, x1, name) in enumerate([(28, 250, "待开始"), (278, 505, "进行中"),
                                      (528, 755, "已终止"), (778, 1005, "已完成")]):
    print("\n==== %s 列 x%d..%d ====" % (name, x0, x1))
    for (xl, xr, yt, yb) in boxes(x0, x1, 250, 640):
        h = yb - yt + 1
        w = xr - xl + 1
        if h < 8 or h > 34 or w < 20:
            continue
        # 底色 = 出现最多的颜色；文字色 = 该块内最暗且饱和度高的颜色
        cnt = collections.Counter()
        for y in range(yt, yb + 1):
            for x in range(xl, xr + 1):
                cnt[px[x, y]] += 1
        bg = cnt.most_common(1)[0][0]
        dark = sorted([c for c, n in cnt.items() if n >= 3 and min(c) < 200],
                      key=lambda c: sum(c))[:3]
        print("  tag box x%d..%d y%d..%d  %dx%d  bg=%s #%02X%02X%02X  dark=%s"
              % (xl, xr, yt, yb, w, h, bg, bg[0], bg[1], bg[2],
                 ["#%02X%02X%02X" % c for c in dark]))
