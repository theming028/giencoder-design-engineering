#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""截图取色核验（防「目视误判明暗」）。

本轮教训：暗色档的两张截图（`p-1440-dark.png` / `n-1440-zd-dark.png`）在预览里
看起来是浅底，实际像素是 rgb(35,35,36) —— **主题确实生效了**，是肉眼/预览器骗人。
⇒ 任何「暗色 / 对比度 / 底色」结论都先跑本脚本取色，再下判断。

用法：
  python mg-work/r108/ev/pix.py <png> [x,y] [x,y] ...
  省略坐标时取「中心 + 左上 + 四个 1/4 点」。
"""
import sys
from PIL import Image


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = argv[1]
    im = Image.open(path).convert('RGB')
    w, h = im.size
    pts = []
    for a in argv[2:]:
        x, y = a.split(',')
        pts.append((int(x), int(y)))
    if not pts:
        pts = [(w // 2, h // 2), (2, 2), (w // 4, h // 2), (3 * w // 4, h // 2),
               (w // 2, h // 4), (w // 2, 3 * h // 4)]
    print('%s  %dx%d' % (path, w, h))
    for p in pts:
        r, g, b = im.getpixel(p)
        print('  (%4d,%4d)  rgb(%3d, %3d, %3d)  #%02X%02X%02X  lum=%.1f%s'
              % (p[0], p[1], r, g, b, r, g, b, (r + g + b) / 3.0,
                 '  ← 深底' if (r + g + b) / 3.0 < 128 else '  ← 浅底'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
