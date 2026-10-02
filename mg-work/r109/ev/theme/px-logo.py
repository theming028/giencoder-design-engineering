# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 G：base 页截图**顶栏区域**的像素颜色分布（找 LOGO 的黑灰）。

DOM 探针没抓到明显的品牌 LOGO（顶栏只有 4 个 svg，最左 @x=89 是 gray-7 的 14×12 图标）。
★ 换像素视角：直接看浅/暗两档顶栏（y 0~56）里有哪些颜色团，尤其「黑灰」团在哪。
"""
import collections
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))          # .../ev/theme
RAW = os.path.join(HERE, os.pardir, os.pardir, u'raw', u'find11')   # .../r109/raw/find11


def cls(px):
    r, g, b = px[0], px[1], px[2]
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn > 34:
        return u'彩色'
    return u'L%03d' % (mx // 16 * 16)


def scan(path, y0, y1, x0, x1, label):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    px = im.load()
    c = collections.Counter()
    for y in range(y0, min(y1, h)):
        for x in range(x0, min(x1, w)):
            c[cls(px[x, y])] += 1
    tot = sum(c.values())
    print(u'  %s  [%d,%d)×[%d,%d)' % (label, x0, x1, y0, y1))
    for k, v in sorted(c.items(), key=lambda kv: -kv[1])[:12]:
        print(u'      %-6s %6d  %5.1f%%' % (k, v, 100.0 * v / tot))
    return c


def main():
    for th in (u'light', u'dark'):
        p = os.path.join(RAW, u'base-%s.png' % th)
        if not os.path.exists(p):
            print(u'  ✗ 缺 %s' % p)
            continue
        im = Image.open(p)
        print(u'=== base %s ===  图幅 %s' % (th, im.size))
        scan(p, 0, 56, 0, 400, u'顶栏左 400')
        scan(p, 0, 56, 0, 1440, u'顶栏全宽')
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
