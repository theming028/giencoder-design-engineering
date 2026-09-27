# -*- coding: utf-8 -*-
"""定位：描述区 list 圆点 / 任务属性 label 列与值列的 x、行距。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()


def dark_runs(x0, x1, y0, y1, thr=200, label=""):
    """在 x0..x1 区间内逐行判断是否存在暗像素，输出连续暗行区间（2x 设备像素）。"""
    print("### %s  x=%d..%d(2x) y=%d..%d thr<%d" % (label, x0, x1, y0, y1, thr))
    inside = False
    s = 0
    for y in range(y0, y1 + 1):
        hit = False
        for x in range(x0, x1):
            c = px[x, y]
            if (c[0] + c[1] + c[2]) / 3 < thr:
                hit = True
                break
        if hit and not inside:
            inside = True; s = y
        elif not hit and inside:
            inside = False
            print("   y=%4d..%4d  css %6.1f..%6.1f  h=%4.1f" % (s, y - 1, s / 2.0, (y - 1) / 2.0, (y - s) / 2.0))
    if inside:
        print("   y=%4d..%4d  css %6.1f..%6.1f" % (s, y1, s / 2.0, y1 / 2.0))


def dark_cols(x0, x1, y, thr=200, label=""):
    print("### %s  y=%d(css %.1f) x=%d..%d" % (label, y, y / 2.0, x0, x1))
    inside = False
    s = 0
    for x in range(x0, x1 + 1):
        c = px[x, y]
        hit = (c[0] + c[1] + c[2]) / 3 < thr
        if hit and not inside:
            inside = True; s = x
        elif not hit and inside:
            inside = False
            print("   x=%4d..%4d  css %6.1f..%6.1f" % (s, x - 1, s / 2.0, (x - 1) / 2.0))


# 1) 描述区列表圆点：ours 在 css x 42..46 -> device 84..92
dark_runs(80, 100, 150, 1000, 230, "描述区小圆点(css x40..50)")
# 2) 任务属性列：label 与 value 的纵向位置
dark_runs(1400, 1500, 100, 820, 200, "任务属性 label 列(css x700..750)")
dark_runs(1540, 1880, 100, 820, 200, "任务属性 value 列(css x770..940)")
