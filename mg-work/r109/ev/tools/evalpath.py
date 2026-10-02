# -*- coding: utf-8 -*-
"""r109 · 第二拍 · 「重新生成」图标：把**真实 SVG path 串**解析后光栅化，与设计位图逐像素比。

为什么要新写一个（`optregen.py` 是拟合器，参数是「圆心 + 角度」）：
  本脚本的输入就是**要写进 ICON_INLINE 的那串 path**（含 SVG 弧的 large-arc/sweep 旗标），
  ⇒ 误差是「最终交付物」的误差，不是「拟合参数」的误差。采样口与 `optregen.py` 同源：
  目标图 = `mg-work/r93/raw/design-rgb.png` 的 14px 盒（x956..969 / y221..234），
  INK=134（由 r99 ⑭ 那轮逐像素读出），SS=8 超采样算覆盖度。

用法： python mg-work/r109/ev/tools/evalpath.py
"""
import math
import re
from PIL import Image

W = H = 14
SS = 8
INK = 134.0
SRC = 'mg-work/r93/raw/design-rgb.png'
OX, OY = 956, 221

_im = Image.open(SRC).convert('RGB')
_px = _im.load()


def lum(x, y):
    r, g, b = _px[x, y]
    return (r * 299 + g * 587 + b * 114) // 1000


# 目标图：0..1 的覆盖率（(255-lum)/121 把 lum=134 映到 1.0，把白 255 映到 0）
T = [[max(0.0, min(1.0, (255.0 - lum(OX + x, OY + y)) / 121.0)) for x in range(W)] for y in range(H)]

# 采样点：每像素 8×8 子样
PTS = [(x + (i + 0.5) / SS, y + (j + 0.5) / SS)
       for y in range(H) for x in range(W) for j in range(SS) for i in range(SS)]

RE_ARC = re.compile(r'M\s*(-?[\d.]+)\s+(-?[\d.]+)\s*A\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+([01])\s+([01])\s+(-?[\d.]+)\s+(-?[\d.]+)')
RE_TRI = re.compile(r'M\s*(-?[\d.]+)\s+(-?[\d.]+)[\s,]+(-?[\d.]+)\s+(-?[\d.]+)[\s,]+(-?[\d.]+)\s+(-?[\d.]+)\s*Z')


def arc_center(x0, y0, x1, y1, r, laf, sf):
    """SVG 端点参数 → 圆心 + 起止角（弧度）。实现按 SVG 规范 F.6.5 的等价三角式。"""
    dx, dy = (x0 - x1) / 2.0, (y0 - y1) / 2.0
    x1p, y1p = dx, dy
    lam = (x1p * x1p + y1p * y1p) / (r * r)
    if lam > 1:
        r *= math.sqrt(lam)
    num = max(0.0, r * r * r * r - r * r * (x1p * x1p + y1p * y1p))
    den = r * r * (x1p * x1p + y1p * y1p)
    co = math.sqrt(num / den) if den else 0.0
    if laf == sf:
        co = -co
    cxp = co * r * y1p / r
    cyp = -co * r * x1p / r
    cx = cxp + (x0 + x1) / 2.0
    cy = cyp + (y0 + y1) / 2.0
    a0 = math.atan2((y0 - cy) / r, (x0 - cx) / r)
    a1 = math.atan2((y1 - cy) / r, (x1 - cx) / r)
    return cx, cy, a0, a1, sf


def in_sweep(a, a0, a1, sf):
    """a 是否落在 a0→a1 这段弧上（按 sweep 旗标定向）。"""
    if sf == 1:                                   # 正方向（角度递增）
        while a1 < a0:
            a1 += 2 * math.pi
        while a < a0:
            a += 2 * math.pi
        return a <= a1
    while a1 > a0:
        a1 -= 2 * math.pi
    while a > a0:
        a -= 2 * math.pi
    return a >= a1


def render(arc, tri, sw=1.3):
    """arc = (x0,y0,r,laf,sf,x1,y1) 或 None；tri = ((x,y),(x,y),(x,y)) 或 None。"""
    cov = [[0] * W for _ in range(H)]
    rc = None
    if arc:
        x0, y0, r, laf, sf, x1, y1 = arc
        cx, cy, a0, a1, sf = arc_center(x0, y0, x1, y1, r, laf, sf)
        rc = (cx, cy, a0, a1, sf, sw / 2.0)
    A = B = C = None
    if tri:
        A, B, C = tri

        def sg(p, q, s):
            return (p[0] - s[0]) * (q[1] - s[1]) - (q[0] - s[0]) * (p[1] - s[1])
    for (x, y) in PTS:
        hit = False
        if rc:
            cx, cy, a0, a1, sf, half = rc
            d = math.hypot(x - cx, y - cy)
            if abs(d - r) <= half:
                if in_sweep(math.atan2(y - cy, x - cx), a0, a1, sf):
                    hit = True
        if not hit and A:
            d1 = sg((x, y), A, B)
            d2 = sg((x, y), B, C)
            d3 = sg((x, y), C, A)
            if not (((d1 < 0) or (d2 < 0) or (d3 < 0)) and ((d1 > 0) or (d2 > 0) or (d3 > 0))):
                hit = True
        if hit:
            cov[int(y)][int(x)] += 1
    return [[cov[y][x] / float(SS * SS) for x in range(W)] for y in range(H)]


def err(m):
    return sum((m[y][x] - T[y][x]) ** 2 for y in range(H) for x in range(W))


def bbox(m, th=0.04):
    xs = [x for y in range(H) for x in range(W) if m[y][x] > th]
    ys = [y for y in range(H) for x in range(W) if m[y][x] > th]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def show(m, t=''):
    ch = ' .:-=+*#%@'
    print('-- %s' % t)
    for y in range(H):
        print('%3d %s' % (y, ''.join(ch[min(9, int(m[y][x] * 10))] for x in range(W))))


def parse_arc(d):
    m = RE_ARC.search(d)
    if not m:
        return None
    g = m.groups()
    return (float(g[0]), float(g[1]), float(g[2]), int(g[5]), int(g[6]), float(g[7]), float(g[8]))


def parse_tri(d):
    m = RE_TRI.search(d)
    if not m:
        return None
    g = [float(v) for v in m.groups()]
    return ((g[0], g[1]), (g[2], g[3]), (g[4], g[5]))


OLD_A = 'M13.9 9.4A5 5 0 0 0 4.1 8.9'
OLD_T = 'M1.05 7.85 4.4 7.95 2.95 10.6Z'
NEW_A = 'M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5'
NEW_T = 'M2.07 11.4 5.61 9.61 1.05 7.56Z'

if __name__ == '__main__':
    print('target ink bbox', bbox(T))
    for name, ad, td in (('OLD(r99 ⑭)', OLD_A, OLD_T), ('NEW(本拍)', NEW_A, NEW_T)):
        a, t = parse_arc(ad), parse_tri(td)
        if a is None:
            raise SystemExit('!! 弧解析失败: %s' % ad)
        if t is None:
            raise SystemExit('!! 三角解析失败: %s' % td)
        m = render(a, t)
        print('%s  err=%.3f   ink bbox=%s' % (name, err(m), bbox(m)))
    show(T, 'DESIGN')
    show(render(parse_arc(NEW_A), parse_tri(NEW_T)), 'NEW')
    show(render(parse_arc(OLD_A), parse_tri(OLD_T)), 'OLD')
