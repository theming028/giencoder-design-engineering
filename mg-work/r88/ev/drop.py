# -*- coding: utf-8 -*-
import os
from PIL import Image
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(REPO, 'mg-work', 'r88', 'raw')
dg = Image.open(os.path.join(D, 'arch@2x_rgb.png')).convert('RGB').resize((840, 658), Image.LANCZOS)
web = Image.open(os.path.join(D, 'web-arch-hover@1x.png')).convert('RGB')

def runs(im, y0, y1, x0, x1, thr=170):
    px = im.load()
    cols = []
    for x in range(x0, x1):
        m = min(px[x, y][0]+px[x, y][1]+px[x, y][2] for y in range(y0, y1))
        cols.append(1 if m/3 < thr else 0)
    segs, s = [], None
    for i, v in enumerate(cols):
        if v and s is None: s = x0 + i
        elif not v and s is not None: segs.append((s, x0 + i - 1)); s = None
    if s is not None: segs.append((s, x1 - 1))
    # 合并间距 < 3 的段（同一字的笔画）
    out = []
    for a, b in segs:
        if out and a - out[-1][1] <= 2: out[-1] = (out[-1][0], b)
        else: out.append((a, b))
    return out

for name, im in (('DESIGN', dg), ('WEB', web)):
    segs = runs(im, 86, 106, 640, 840)
    print('%-7s 下拉行分段:' % name, segs)
    # 逐个分段的宽度
    print('        宽度:', [b - a + 1 for a, b in segs])

print()
for name, im in (('DESIGN', dg), ('WEB', web)):
    segs = runs(im, 86, 106, 0, 340)
    print('%-7s 搜索行分段:' % name, segs)
