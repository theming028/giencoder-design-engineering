# -*- coding: utf-8 -*-
"""扫描指定卡内文字的『行带』，输出每行中心与行距。png = design + 1。"""
from PIL import Image

im = Image.open('design-rgb.png').convert('RGB')
px = im.load()


def dark(p, th=170):
    return (p[0] + p[1] + p[2]) / 3 < th


def scan(name, y0, y1, x0=186, x1=990):
    p0, p1 = y0 + 1, y1 + 1
    bands = []
    cur = None
    for y in range(p0 + 2, p1 - 2):
        n = sum(1 for x in range(x0, x1) if dark(px[x, y]))
        if n >= 2:
            if cur is None:
                cur = [y, y]
            else:
                cur[1] = y
        else:
            if cur and cur[1] - cur[0] >= 2:
                bands.append(cur)
            cur = None
    if cur:
        bands.append(cur)
    print('--- %s (h=%d) ---' % (name, p1 - p0))
    prev = None
    for b in bands:
        c = (b[0] + b[1]) / 2
        d = ('Δ%.1f' % (c - prev)) if prev else ''
        print('   行 y%4d..%-4d 高%-3d 中心%-7.1f %s' % (b[0], b[1], b[1] - b[0] + 1, c, d))
        prev = c


scan('Bash 卡头', 1016, 1057)
scan('Bash 卡体', 1057, 1176)
scan('Tool call 卡体', 2640, 2732)
scan('更新任务清单 卡体', 1870, 2040)
scan('重试卡', 2816, 2880)
scan('SKILL 卡', 2452, 2516)
scan('搜索资料 卡', 3548, 3664)
