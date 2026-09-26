# -*- coding: utf-8 -*-
"""按行统计暗像素，定位文字行 / 分隔线"""
from PIL import Image

def prof(path, x0, x1, y0, y1, thr=150):
    im = Image.open(path).convert('RGB')
    out = []
    for y in range(y0, y1):
        n = 0
        for x in range(x0, x1):
            r, g, b = im.getpixel((x, y))
            if (r*299+g*587+b*114)//1000 < thr: n += 1
        out.append((y, n))
    return out

def bands(p, minn=2):
    res = []; cur = None
    for y, n in p:
        if n >= minn:
            if cur is None: cur = [y, y, 0]
            cur[1] = y; cur[2] = max(cur[2], n)
        else:
            if cur: res.append(tuple(cur)); cur = None
    if cur: res.append(tuple(cur))
    return res

D = r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\design-modal.png'
R = r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\x-modal.png'

print('=== 设计稿：文字行带 (x 145..1295) ===')
for b in bands(prof(D, 145, 1295, 60, 500)):
    print('  y%3d-%3d  高%2d  max%3d' % (b[0], b[1], b[1]-b[0]+1, b[2]))

print('=== 渲染：文字行带 (x 56..1208) ===')
for b in bands(prof(R, 56, 1208, 80, 500)):
    print('  y%3d-%3d  高%2d  max%3d' % (b[0], b[1], b[1]-b[0]+1, b[2]))
