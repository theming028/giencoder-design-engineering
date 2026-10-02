# -*- coding: utf-8 -*-
"""r109 · 第二拍 · regen 图标：**放宽边界 + 起止角自由**的坐标下降重拟。

与 `optregen.py` 的三点差别（就是为了修掉它留下的残差）：
  ① 弧的**起始角 t0 也当参数**（旧工具写死 t0=0 ⇒ 「右端恰好在圆心正右方」这个假设
     是 r99 那轮的读法，不是设计真值）；
  ② `BOUND` 放宽（cy 9.4~11.2 / r 4.5~5.6 / t0 -30~30）：旧工具的 cy 上界 10.7 被**顶住**了，
     说明真解在界外 ⇒ 旧解是「被边界夹住」的次优解；
  ③ 目标函数仍是 SS=8 的覆盖率平方误差，**但同时对「墨迹包络」加一道软约束**（见 PEND），
     免得又收敛到「大三角 + 小弧」那种 err 更低但形状明显错的过拟合解。

用法： python mg-work/r109/ev/tools/refiteregen.py
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evalpath as E                                          # noqa: E402  复用目标图 / 采样口 / err

W, H, SS = E.W, E.H, E.SS
PTS = E.PTS
T = E.T


def render(cx, cy, r, t0, t1, hw, L, da, w=1.3):
    """弧 = 圆心 (cx,cy) 半径 r、角度 [t0,t1]（度，y 向下、顺时针为正方向的坐标系里按数值区间）；
       三角 = 挂在弧的 t1 端、沿切向外伸 L、半宽 hw、整体再偏转 da 度。"""
    cov = [[0] * W for _ in range(H)]
    half = w / 2.0
    lo, hi = min(t0, t1), max(t0, t1)
    th = math.radians(t1 + da)
    Ex, Ey = cx + r * math.cos(math.radians(t1)), cy + r * math.sin(math.radians(t1))
    dv = (math.sin(th), -math.cos(th))
    pp = (dv[1], -dv[0])
    b1 = (Ex + hw * pp[0], Ey + hw * pp[1])
    b2 = (Ex - hw * pp[0], Ey - hw * pp[1])
    tip = (Ex + L * dv[0], Ey + L * dv[1])
    A, B, C = tip, b1, b2

    def sg(p, q, s):
        return (p[0] - s[0]) * (q[1] - s[1]) - (q[0] - s[0]) * (p[1] - s[1])

    for (x, y) in PTS:
        hit = False
        dx, dy = x - cx, y - cy
        if abs(math.hypot(dx, dy) - r) <= half:
            ad = math.degrees(math.atan2(dy, dx))
            for k in (-1, 0, 1):
                if lo <= ad + k * 360 <= hi:
                    hit = True
                    break
        if not hit:
            d1 = sg((x, y), A, B)
            d2 = sg((x, y), B, C)
            d3 = sg((x, y), C, A)
            if not (((d1 < 0) or (d2 < 0) or (d3 < 0)) and ((d1 > 0) or (d2 > 0) or (d3 > 0))):
                hit = True
        if hit:
            cov[int(y)][int(x)] += 1
    return [[cov[y][x] / float(SS * SS) for x in range(W)] for y in range(H)]


def err(m):
    """覆盖率平方误差（与 `evalpath.py` 同一口径，便于两处数字互相对照）。

    ⚠ 曾经试过在这一项上加「越界包络罚」来防止过拟合，**结论是罚项不能在这里做**：
      设计真值本身在弧顶下方有洞（y=6 的 x7/x8 就是 0），任何候选只要在洞里有半格墨
      都会被罚 ⇒ 罚项实际上在**惩罚正确的弧顶**，把解推向「弧更扁」的另一侧（err 从
      2.3 抬到 10.7）。防过拟合的正解是**收紧参数的物理边界**（BOUND），不是加罚项。
    """
    return sum((m[y][x] - T[y][x]) ** 2 for y in range(H) for x in range(W))


def clamp(lo, hi, v):
    return max(lo, min(hi, v))


# 设计真值的墨迹盒（含箭头尖端那点 0.25 的淡墨）：x 0..13 / y 4..10。
# ★ 防过拟合的**正解**：把「形状必须落在这个盒子里」写成硬约束（下界/上界），
#   而不是往目标函数里加罚项（见 err() 的注释）。
BOX = (0.10, 4.20, 13.90, 11.00)


def tri_pts(cx, cy, r, t0, t1, hw, L, da):
    th = math.radians(t1 + da)
    Ex, Ey = cx + r * math.cos(math.radians(t1)), cy + r * math.sin(math.radians(t1))
    dv = (math.sin(th), -math.cos(th))
    pp = (dv[1], -dv[0])
    return [(Ex + L * dv[0], Ey + L * dv[1]),
            (Ex + hw * pp[0], Ey + hw * pp[1]),
            (Ex - hw * pp[0], Ey - hw * pp[1])]


def feasible(*p):
    x0, y0, x1, y1 = BOX
    for (px, py) in tri_pts(*p):
        if not (x0 <= px <= x1 and y0 <= py <= y1):
            return False
    return True


# (名字, 初值, 下界, 上界)
PAR = [
    ('cx', 7.92, 7.0, 8.6),
    ('cy', 10.64, 9.4, 11.2),
    ('r', 5.03, 4.5, 5.6),
    ('t0', 0.0, -30.0, 30.0),
    ('t1', -154.88, -180.0, -125.0),
    ('hw', 2.5, 1.4, 2.6),
    ('L', 2.70, 1.6, 3.4),
    ('da', -1.0, -30.0, 30.0),
]


def svg(cx, cy, r, t0, t1, hw, L, da, w=1.3):
    """把参数转成真正要写进 ICON_INLINE 的 path 串（弧用 A 命令，含 large-arc/sweep 旗标）。"""
    p0 = (cx + r * math.cos(math.radians(t0)), cy + r * math.sin(math.radians(t0)))
    p1 = (cx + r * math.cos(math.radians(t1)), cy + r * math.sin(math.radians(t1)))
    sweep = 0 if t1 < t0 else 1
    span = abs(t1 - t0)
    laf = 1 if span > 180 else 0
    th = math.radians(t1 + da)
    dv = (math.sin(th), -math.cos(th))
    pp = (dv[1], -dv[0])
    E_ = p1
    b1 = (E_[0] + hw * pp[0], E_[1] + hw * pp[1])
    b2 = (E_[0] - hw * pp[0], E_[1] - hw * pp[1])
    tip = (E_[0] + L * dv[0], E_[1] + L * dv[1])
    return ('<path d="M%.2f %.2fA%.2f %.2f 0 %d %d %.2f %.2f" stroke="currentColor" '
            'stroke-width="%.1f" stroke-linecap="round"/>'
            '<path d="M%.2f %.2f %.2f %.2f %.2f %.2fZ" fill="currentColor"/>'
            % (p0[0], p0[1], r, r, laf, sweep, p1[0], p1[1], w,
               tip[0], tip[1], b1[0], b1[1], b2[0], b2[1]))


if __name__ == '__main__':
    import random
    random.seed(109)

    def descend(seed):
        P = seed[:]
        best = err(render(*P))
        for step in (0.5, 0.25, 0.12, 0.06, 0.03, 0.015):
            improved = True
            while improved:
                improved = False
                for i, (nm, _v, lo, hi) in enumerate(PAR):
                    for d in (step, -step):
                        c = P[:]
                        c[i] = clamp(lo, hi, P[i] + d)
                        if c[i] == P[i]:
                            continue
                        if not feasible(*c):
                            continue
                        e = err(render(*c))
                        if e < best - 1e-9:
                            best, P = e, c
                            improved = True
        return best, P

    seeds = [[p[1] for p in PAR],
             [7.92, 10.64, 5.03, 0.0, -154.88, 2.50, 2.70, -1.0],
             [7.5, 10.2, 4.8, 5.0, -150.0, 2.2, 2.4, 0.0],
             [8.2, 10.9, 5.2, -5.0, -160.0, 2.0, 2.8, -10.0]]
    for _ in range(26):
        seeds.append([random.uniform(*b) for (_n, _v, b, _h) in [(p[0], p[1], p[2], p[3]) for p in PAR]]
                     if False else [random.uniform(PAR[i][2], PAR[i][3]) for i in range(len(PAR))])

    best_all = None
    for s in seeds:
        if not feasible(*s):
            continue
        e, P = descend(s)
        if best_all is None or e < best_all[0]:
            best_all = (e, P)
    best, P = best_all
    print('final err %.3f' % best)
    print('  ' + ' '.join('%s=%.2f' % (p[0], v) for p, v in zip(PAR, P)))
    m = render(*P)
    print('  ink bbox', E.bbox(m))
    print('  TARGET bbox', E.bbox(T))
    print('  SVG:', svg(*P))
    E.show(T, 'DESIGN')
    E.show(m, 'FIT')
