# -*- coding: utf-8 -*-
import math, itertools
from PIL import Image

W = H = 14
SS = 8
INK = 134.0            # design ink grey

# ---------- design target ----------
im = Image.open('mg-work/r93/raw/design-rgb.png').convert('RGB')
px = im.load()
T = [[0.0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        r, g, b = px[956+x, 221+y]
        lum = (r*299 + g*587 + b*114)//1000
        T[y][x] = max(0.0, min(1.0, (255.0-lum)/(255.0-INK)))

# ---------- renderer ----------
def seg_cov(pts):
    """pts: list of (x,y) sample points inside the shape -> coverage per pixel"""
    m = [[0]*W for _ in range(H)]
    for (sx, sy) in pts:
        xi = int(sx); yi = int(sy)
        if 0 <= xi < W and 0 <= yi < H:
            m[yi][xi] += 1
    return [[m[y][x]/(SS*SS) for x in range(W)] for y in range(H)]

def samples():
    out = []
    for y in range(H):
        for x in range(W):
            for j in range(SS):
                for i in range(SS):
                    out.append((x + (i+0.5)/SS, y + (j+0.5)/SS))
    return out
PTS = samples()

def arc_pts(cx, cy, r, t0, t1, w):
    lo, hi = math.radians(min(t0, t1)), math.radians(max(t0, t1))
    half = w/2.0
    res = []
    for (x, y) in PTS:
        dx, dy = x-cx, y-cy
        d = math.hypot(dx, dy)
        if abs(d-r) > half:
            continue
        a = math.atan2(dy, dx)
        # unwrap into [t0,t1] window (degrees) - work in the arc's own frame
        lo2, hi2 = min(t0, t1), max(t0, t1)
        # candidate angles a + k*360
        for k in (-1, 0, 1):
            ad = math.degrees(a) + k*360.0
            if lo2 <= ad <= hi2:
                res.append((x, y)); break
    return res

def tri_pts(p, q, r_):
    res = []
    def sgn(a, b, c):
        return (a[0]-c[0])*(b[1]-c[1]) - (b[0]-c[0])*(a[1]-c[1])
    for (x, y) in PTS:
        pt = (x, y)
        d1 = sgn(pt, p, q); d2 = sgn(pt, q, r_); d3 = sgn(pt, r_, p)
        neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        if not (neg and pos):
            res.append(pt)
    return res

def render(params):
    a = params['arc']; t = params['tri']
    m = [[0.0]*W for _ in range(H)]
    for src in (arc_pts(*a), tri_pts(t[0:2], t[2:4], t[4:6])):
        cm = seg_cov(src)
        for y in range(H):
            for x in range(W):
                m[y][x] = max(m[y][x], cm[y][x])
    return m

def err(m, y0=0, y1=H, x0=0, x1=W):
    e = 0.0
    for y in range(y0, y1):
        for x in range(x0, x1):
            e += (m[y][x]-T[y][x])**2
    return e

def show(m, title=''):
    chars = ' .:-=+*#%@'
    print('--', title)
    for y in range(H):
        print('%3d %s' % (y, ''.join(chars[min(9, int(m[y][x]*10))] for x in range(W))))

if __name__ == '__main__':
    show(T, 'DESIGN target')
    def fit(arc0, tri0, freeze_cx=True):
        arc = list(arc0); tri = list(tri0)
        def total(a, t):
            return err(render({'arc': tuple(a), 'tri': tuple(t)}))
        best = total(arc, tri)
        for st in [1.0, 0.5, 0.25, 0.12, 0.06]:
            improved = True
            while improved:
                improved = False
                for idx in range(6):
                    if freeze_cx and idx == 0:
                        continue
                    for d in (st, -st):
                        c = arc[:]; c[idx] += d
                        e = total(c, tri)
                        if e < best - 1e-7:
                            best = e; arc = c; improved = True
                for idx in range(6):
                    for d in (st, -st):
                        c = tri[:]; c[idx] += d
                        e = total(arc, c)
                        if e < best - 1e-7:
                            best = e; tri = c; improved = True
        return best, arc, tri
    import math
    results = []
    for cx in (7.0, 7.25, 7.5, 7.87):
        for r0 in (5.0, 5.2):
            e, arc, tri = fit([cx, 10.3, r0, 0.0, -160.0, 1.3], [0.3, 7.9, 6.0, 9.6, 2.8, 11.4])
            results.append((e, cx, arc, tri))
            print('cx=%.2f r0=%.1f -> err %.4f | arc cx=%.3f cy=%.3f r=%.3f t0=%.2f t1=%.2f w=%.2f | tri %s' % (
                cx, r0, e, arc[0], arc[1], arc[2], arc[3], arc[4], arc[5],
                ' '.join('%.2f' % v for v in tri)))
    results.sort()
    e, cx, arc, tri = results[0]
    print()
    print('BEST: err %.4f cx=%.2f' % (e, cx))
    cx_, cy, r, t0, t1, w = arc
    x0 = cx_ + r*math.cos(math.radians(t0)); y0 = cy + r*math.sin(math.radians(t0))
    x1 = cx_ + r*math.cos(math.radians(t1)); y1 = cy + r*math.sin(math.radians(t1))
    print('ARC: M%.2f %.2f A%.2f %.2f 0 0 %.2f %.2f' % (x0, y0, r, r, x1, y1))
    print('TRI: M%.2f %.2f L%.2f %.2f L%.2f %.2f Z' % tuple(tri))
    m = render({'arc': tuple(arc), 'tri': tuple(tri)})
    show(m, 'FITTED')
    show(T, 'DESIGN')
