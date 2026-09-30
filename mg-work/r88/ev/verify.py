# -*- coding: utf-8 -*-
"""r88 ③ 三个未决量测点的复核：内容宽 / 分隔线水平范围 / 圆角。
只读，不动仓库页面。用法：python mg-work/r88/ev/verify.py
"""
import io, os, sys
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PNG = os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')
im = Image.open(PNG).convert('RGB')
W, H = im.size
px = im.load()
print('PNG = %dx%d' % (W, H))


def runs(y, bg, tol=6):
    """扫一行，返回 [(x0,x1,color)]，仅列出与 bg 差异 > tol 的连续段"""
    out = []
    cur = None
    for x in range(W):
        r, g, b = px[x, y]
        d = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
        if d > tol:
            if cur and cur[2] == d and x == cur[1] + 1:
                cur = (cur[0], x, d)
            else:
                if cur:
                    out.append(cur)
                cur = (x, x, d)
        else:
            if cur:
                out.append(cur)
                cur = None
    if cur:
        out.append(cur)
    # 用段中点取色
    return [(a, b, px[(a + b) // 2, y]) for a, b, _ in out]


def vruns(x, bg, tol=6, y0=0, y1=None):
    y1 = H if y1 is None else y1
    out = []
    cur = None
    for y in range(y0, y1):
        r, g, b = px[x, y]
        d = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
        if d > tol:
            if cur and y == cur[1] + 1:
                cur = (cur[0], y)
            else:
                if cur:
                    out.append(cur)
                cur = (y, y)
        else:
            if cur:
                out.append(cur)
                cur = None
    if cur:
        out.append(cur)
    return out


# ---------------------------------------------------------------- 1. 内容宽
print('\n[1] 列表卡顶边直段（找卡左右缘）')
# 卡底色 #F8F9FA，页底色 #FFFFFF
for y in (270, 300, 400):
    rr = runs(y, (255, 255, 255), tol=4)
    if rr:
        print('  y=%d  首个非白段 %s .. 末个非白段 %s' % (y, rr[0][:2], rr[-1][:2]))
    else:
        print('  y=%d  全白' % y)

print('\n[1b] 分隔线（行 y=418 附近逐行打印非卡底段）')
CARD = (248, 249, 250)
for y in range(414, 424):
    rr = runs(y, CARD, tol=5)
    seg = ' | '.join('%d..%d%s' % (a, b, ('#%02X%02X%02X' % c)) for a, b, c in rr)
    print('  y=%d  %s' % (y, seg[:180]))

# ---------------------------------------------------------------- 2. 圆角（顶边直段反推）
print('\n[2] 圆角反推：搜索框（顶边 y 附近）')
# 搜索框边框 #F2F2F2 以上/浅；底色白
for y in range(158, 168):
    rr = runs(y, (255, 255, 255), tol=5)
    seg = ' | '.join('%d..%d' % (a, b) for a, b, c in rr if b - a > 40)
    print('  y=%d  %s' % (y, seg[:200]))

print('\n[2b] 卡顶边（列表卡圆角）')
for y in range(262, 274):
    rr = runs(y, (255, 255, 255), tol=5)
    seg = ' | '.join('%d..%d' % (a, b) for a, b, c in rr if b - a > 40)
    print('  y=%d  %s' % (y, seg[:200]))

# ---------------------------------------------------------------- 3. 行高与列表总高
print('\n[3] 竖直扫描 x=840（卡片中线）非白段')
print('  ', vruns(840, (255, 255, 255), tol=4)[:12])
