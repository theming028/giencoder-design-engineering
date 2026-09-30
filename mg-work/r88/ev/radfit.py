# -*- coding: utf-8 -*-
"""圆角定值：按候选 r 渲染理想圆角矩形（含 2device 描边 + 4x 超采样抗锯齿），
与真实截图逐像素比 SSD，取最小者。只读。
"""
import os, math
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO, 'mg-work', 'r88', 'raw', 'arch@2x_rgb.png')).convert('RGB')
px = im.load()


def ss(box, r, border, fill, out, bw=2.0, n=4):
    """返回 box=(x0,y0,x1,y1) 的 RGB 列表；形状左上角 =(x0,y0)，r=外圆角(device)。"""
    x0, y0, x1, y1 = box
    ox0, oy0 = 0.0, 0.0                      # 形状外边界 = 该 box 的左上
    res = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            acc = [0.0, 0.0, 0.0]
            for sy in range(n):
                for sx in range(n):
                    fx = (x - x0) + (sx + 0.5) / n
                    fy = (y - y0) + (sy + 0.5) / n
                    d = dist_to_shape(fx, fy, x1 - x0, y1 - y0, r, ox0, oy0)
                    if d > bw:
                        col = fill
                    elif d > 0:
                        col = border
                    else:
                        col = out
                    acc[0] += col[0]; acc[1] += col[1]; acc[2] += col[2]
            res.append(tuple(int(v / (n * n) + .5) for v in acc))
    return res


def dist_to_shape(x, y, w, h, r, ox, oy):
    """点 (x,y) 到圆角矩形**内部**的有符号距离：>0 在内（离外边界距离），<0 在外。
    这里换算成「离外边界往内的距离」= 半径 - 到圆心的距离 形式。
    简化：先算到外边界的有符号距离 sdf（内正外负），返回 sdf。
    """
    cx0, cy0 = ox + r, oy + r
    cx1, cy1 = ox + w - r, oy + h - r
    qx = min(max(x, cx0), cx1)
    qy = min(max(y, cy0), cy1)
    if x < ox or x >= ox + w or y < oy or y >= oy + h:
        return -1.0        # 在包围盒外
    dx = x - qx
    dy = y - qy
    if qx == cx0 and qy == cy0:      # 左上角距圆心
        return r - math.hypot(dx, dy)
    if qx == cx1 and qy == cy0:
        return r - math.hypot(dx, dy)
    if qx == cx0 and qy == cy1:
        return r - math.hypot(dx, dy)
    if qx == cx1 and qy == cy1:
        return r - math.hypot(dx, dy)
    # 边带：离最近边的距离（内正）
    return min(x - ox, ox + w - x, y - oy, oy + h - y)


def fit(name, box, cands, border, fill, out, bw=2.0):
    x0, y0, x1, y1 = box
    real = [px[x, y] for y in range(y0, y1) for x in range(x0, x1)]
    best = None
    for r in cands:
        sim = ss(box, r, border, fill, out, bw)
        e = sum((sim[i][0] - real[i][0]) ** 2 + (sim[i][1] - real[i][1]) ** 2 + (sim[i][2] - real[i][2]) ** 2
                for i in range(len(real)))
        e /= float(len(real))
        print('  %-10s r=%2d device (%4.1f design)  RMSE=%.2f' % (name, r, r / 2.0, math.sqrt(e)))
        if best is None or e < best[1]:
            best = (r, e)
    print('  >>> %s 最佳 r=%d device = %.1f design px' % (name, best[0], best[0] / 2.0))
    return best[0]


print('=== 卡片左上角（外边界 = 截图左上 (0,264)）===')
fit('card', (0, 264, 40, 304), [8, 10, 12, 13, 14, 16, 18, 20],
    (238, 238, 238), (248, 249, 250), (255, 255, 255), bw=2.0)

print('\n=== 搜索框左上角（外边界 = (0,160)）===')
fit('input', (0, 160, 40, 200), [8, 10, 12, 13, 14, 16, 18, 20],
    (229, 229, 229), (255, 255, 255), (255, 255, 255), bw=2.0)

print('\n=== 行2 默认钮左上角（外边界 = (1511,317)?；先扫）===')
for y in range(312, 322):
    print('    y=%d  x=1511..1516 -> %s' % (y, ' '.join('#%02X%02X%02X' % px[x, y] for x in range(1511, 1517))))
print('   竖直 x=1540 312..380:', ' '.join('%d:#%02X%02X%02X' % (y, *px[1540, y]) for y in range(314, 322)))
