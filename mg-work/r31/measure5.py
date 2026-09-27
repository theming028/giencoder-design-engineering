# -*- coding: utf-8 -*-
"""第 31 轮设计稿精量 v5
目标：不依赖任何既有假设，从 PNG 自身反解 (origin, scale)，再输出设计坐标下的几何真值。
原点反解依据：面板边框 #E5E5E5 构成的最外环 -> 左/上/右边缘 + 尺寸应等于 320x480 * scale。
"""
import io, sys
from PIL import Image

PNG = "mg-work/r31/design/dispatch.png"
im = Image.open(PNG).convert("RGB")
W, H = im.size
px = im.load()
print("PNG = %dx%d" % (W, H))


def near(c, t, tol=6):
    return all(abs(c[i] - t[i]) <= tol for i in range(3))


def scan_ring(target, tol=6):
    """返回 target 色像素的最小外接矩形"""
    xs, ys = [], []
    for y in range(H):
        for x in range(W):
            if near(px[x, y], target, tol):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


# --- 1. 面板边框环 ---
ring = scan_ring((229, 229, 229), 5)   # #E5E5E5
print("边框环 bbox =", ring)
if ring:
    x0, y0, x1, y1 = ring
    print("  环 宽=%d 高=%d" % (x1 - x0 + 1, y1 - y0 + 1))
    print("  scale(估) = %.4f / %.4f" % ((x1 - x0 + 1) / 320.0, (y1 - y0 + 1) / 480.0))

# 取边框环上/左边所在扫描线，逐行统计长 run -> 更稳的边界
def long_runs(target, tol, minlen):
    rows = []
    for y in range(H):
        run = 0; best = 0; bs = 0; s = 0
        for x in range(W):
            if near(px[x, y], target, tol):
                if run == 0: s = x
                run += 1
                if run > best: best = run; bs = s
            else:
                run = 0
        if best >= minlen:
            rows.append((y, bs, best))
    return rows

print("\n边框色长 run 行（>=200px）:")
for y, s, l in long_runs((229, 229, 229), 5, 200)[:8]:
    print("  y=%d x=%d..%d len=%d" % (y, s, s + l - 1, l))
print("  ...")
for y, s, l in long_runs((229, 229, 229), 5, 200)[-8:]:
    print("  y=%d x=%d..%d len=%d" % (y, s, s + l - 1, l))

# --- 2. 关键色在 PNG 中出现次数（识别调色板）---
print("\n角点采样: (2,2)=%s (W-3,2)=%s (2,H-3)=%s (W-3,H-3)=%s" % (
    px[2, 2], px[W - 3, 2], px[2, H - 3], px[W - 3, H - 3]))
