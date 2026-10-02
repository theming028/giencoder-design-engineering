# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 F：assets/images/bg-img-1.png 的像素构成。

顶栏 header 浅色档 background-image 就是它（background-size:70% auto）。
要回答：图里有没有「黑灰部分」（LOGO 的黑灰）？在图的哪块区域？占比多少？
"""
import collections
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
IMG = os.path.join(ROOT, 'assets', 'images', 'bg-img-1.png')


def bucket(px):
    u"""按亮度 + 饱和度粗分类"""
    r, g, b, a = px
    if a < 16:
        return u'透明'
    mx, mn = max(r, g, b), min(r, g, b)
    sat = mx - mn
    if sat > 30:
        return u'彩色'
    if mx < 60:
        return u'黑(#<60)'
    if mx < 110:
        return u'深灰(60-110)'
    if mx < 170:
        return u'中灰(110-170)'
    if mx < 225:
        return u'浅灰(170-225)'
    return u'近白(>=225)'


def main():
    im = Image.open(IMG).convert('RGBA')
    w, h = im.size
    print(u'=== %s ===' % os.path.basename(IMG))
    print(u'  尺寸 %d × %d' % (w, h))
    print()
    px = im.load()
    cnt = collections.Counter()
    # 分区：3 列 × 2 行
    zone = collections.defaultdict(collections.Counter)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            b = bucket(px[x, y])
            cnt[b] += 1
            zi = u'%s-%s' % (u'左' if x < w / 3 else (u'中' if x < 2 * w / 3 else u'右'),
                             u'上' if y < h / 2 else u'下')
            zone[zi][b] += 1
    tot = sum(cnt.values())
    print(u'=== 全图分类（采样 1/4 像素）===')
    for k, v in cnt.most_common():
        print(u'   %-14s %6d  %5.1f%%' % (k, v, 100.0 * v / tot))
    print()
    print(u'=== 分区：非透明且非近白（＝看得见的图形）占比 ===')
    for zi in [u'左上', u'中上', u'右上', u'左下', u'中下', u'右下']:
        c = zone.get(zi, collections.Counter())
        s = sum(c.values())
        if not s:
            continue
        ink = s - c.get(u'透明', 0) - c.get(u'近白(>=225)', 0)
        print(u'   %-6s 可见墨迹 %5.1f%%   %s' % (
            zi, 100.0 * ink / s,
            u' '.join(u'%s=%d' % (k, v) for k, v in c.most_common(4))))
    print()
    # 找「黑 / 深灰」像素的包围盒
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            b = bucket(px[x, y])
            if b in (u'黑(#<60)', u'深灰(60-110)', u'中灰(110-170)'):
                xs.append(x)
                ys.append(y)
    if xs:
        print(u'=== 黑/深灰/中灰像素包围盒 ===')
        print(u'   x: %d ~ %d   y: %d ~ %d   共 %d 个像素' % (
            min(xs), max(xs), min(ys), max(ys), len(xs)))
    else:
        print(u'   （图中没有黑/深灰/中灰像素）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
