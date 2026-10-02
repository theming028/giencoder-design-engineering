# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 G2：base 页暗色顶栏里的「灰系墨迹」定位。

上一脚本发现暗色顶栏左 400 有 L096/L064/L048（灰）合计约 0.7%，浅色档没有
⇒ 这正是邵先生说的「LOGO 黑灰部分在暗色档没变白」。
本脚本按列扫描，找出这些灰像素的**水平区间**，与 DOM 里 svg 的 x 坐标对齐。
"""
import collections
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, os.pardir, os.pardir, u'raw', u'find11')


def load(path):
    im = Image.open(path).convert('RGB')
    return im.load(), im.size


def grayish(px):
    r, g, b = px
    mx, mn = max(r, g, b), min(r, g, b)
    return (mx - mn) <= 20


def main():
    lp, size = load(os.path.join(RAW, u'base-light.png'))
    dp, _ = load(os.path.join(RAW, u'base-dark.png'))
    w, h = size

    # 暗色档：灰系且亮度在 40~130（「黑灰」区间），y 0~56
    col = collections.Counter()
    box = []
    for y in range(0, 48):
        for x in range(0, w):
            p = dp[x, y]
            if grayish(p) and 40 <= max(p) <= 132:
                col[x] += 1
                box.append((x, y))
    print(u'=== 暗色顶栏「灰系墨迹」(L40~132) ===')
    print(u'  命中像素 %d' % len(box))
    if box:
        xs = [b[0] for b in box]
        ys = [b[1] for b in box]
        print(u'  包围盒 x:%d~%d  y:%d~%d' % (min(xs), max(xs), min(ys), max(ys)))
        # 水平聚类（间隔 > 12px 视为新簇）
        s = sorted(col.items())
        clusters = []
        cur = [s[0]]
        for it in s[1:]:
            if it[0] - cur[-1][0] <= 12:
                cur.append(it)
            else:
                clusters.append(cur)
                cur = [it]
        clusters.append(cur)
        print(u'  水平簇（x 起止 · 像素数）：')
        for c in clusters:
            print(u'     x %4d ~ %4d   n=%d' % (c[0][0], c[-1][0], sum(v for _, v in c)))
    print()

    # 浅色档同区间：深色墨迹（LOGO 在浅色下就是黑灰）
    col2 = collections.Counter()
    box2 = []
    for y in range(0, 48):
        for x in range(0, w):
            p = lp[x, y]
            if grayish(p) and max(p) <= 132:
                col2[x] += 1
                box2.append((x, y))
    print(u'=== 浅色顶栏「深色墨迹」(<=132) 作对照 ===')
    print(u'  命中像素 %d' % len(box2))
    if box2:
        xs = [b[0] for b in box2]
        ys = [b[1] for b in box2]
        print(u'  包围盒 x:%d~%d  y:%d~%d' % (min(xs), max(xs), min(ys), max(ys)))
        s = sorted(col2.items())
        clusters = []
        cur = [s[0]]
        for it in s[1:]:
            if it[0] - cur[-1][0] <= 12:
                cur.append(it)
            else:
                clusters.append(cur)
                cur = [it]
        clusters.append(cur)
        print(u'  水平簇（x 起止 · 像素数）：')
        for c in clusters:
            print(u'     x %4d ~ %4d   n=%d' % (c[0][0], c[-1][0], sum(v for _, v in c)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
