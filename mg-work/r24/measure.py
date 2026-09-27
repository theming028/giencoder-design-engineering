# -*- coding: utf-8 -*-
"""对 2x 设计稿截图逐像素测量：容器边缘色 / 内部发丝线色 / 底色。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
W, H = im.size
px = im.load()
print("screenshot size = %dx%d" % (W, H))
print("bg corner (2,2) =", px[2, 2])


def row(y, x0, x1, step=1, tag=""):
    print("--- row y=%d x=%d..%d %s" % (y, x0, x1, tag))
    prev = None
    for x in range(x0, x1, step):
        c = px[x, y]
        if c != prev:
            print("   x=%4d %s" % (x, c))
            prev = c


def col(x, y0, y1, step=1, tag=""):
    print("--- col x=%d y=%d..%d %s" % (x, y0, y1, tag))
    prev = None
    for y in range(y0, y1, step):
        c = px[x, y]
        if c != prev:
            print("   y=%4d %s" % (y, c))
            prev = c


# 横向扫一条位于「内容区中段」的行，穿过：页面底 -> 左栏左缘 -> 左栏 -> 右栏 -> 页面底
row(1200, 0, 140, 1, "左缘(左栏左边界)")
row(1200, 1860, 1940, 1, "两栏间隙")
row(1200, 2830, 2880, 1, "右栏右边界")
# 纵向扫左栏顶/底
col(900, 90, 140, 1, "左栏上边界")
col(900, 2130, 2170, 1, "左栏下边界")
