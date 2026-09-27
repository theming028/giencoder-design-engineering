# -*- coding: utf-8 -*-
"""侧栏（css x684..944）逐带扫描：左起始 x / 竖线位置 / 底色带。"""
from PIL import Image

P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
px = im.load()
X0, X1 = 1370, 1888

print("=== 竖线：device x 1360..1440，取 y=1000..2100 平均 ===")
for x in range(1360, 1441):
    acc = [0, 0, 0]; n = 0
    for y in range(1000, 2100):
        c = px[x, y]
        acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]; n += 1
    avg = tuple(round(v / n, 1) for v in acc)
    if avg[0] < 252:
        print("   x=%4d css %6.1f avg=%s" % (x, x / 2.0, avg))

print("\n=== 侧栏文本带（thr<200）===")
inside = False; s = 0
bands = []
for y in range(96, 2144):
    hit = any(sum(px[x, y]) / 3 < 200 for x in range(X0, X1))
    if hit and not inside:
        inside = True; s = y
    elif not hit and inside:
        inside = False; bands.append((s, y - 1))
if inside:
    bands.append((s, 2143))

for a, b in bands:
    m = None
    for y in range(a, b + 1):
        for x in range(X0, X1):
            if sum(px[x, y]) / 3 < 200:
                m = x if m is None else min(m, x)
                break
    print("   css y %6.1f..%6.1f h=%4.1f   左起 css x=%6.1f" % (a / 2.0, b / 2.0, (b - a + 1) / 2.0, m / 2.0))

print("\n=== 底色带：device x=1400 竖切（css 700）===")
prev = None; s = 0
for y in range(96, 2144):
    c = px[1400, y]
    if prev is None:
        prev = c; s = y; continue
    if c != prev:
        if y - s >= 4:
            print("   css y %6.1f..%6.1f h=%5.1f  %s" % (s / 2.0, (y - 1) / 2.0, (y - s) / 2.0, prev))
        prev = c; s = y
print("   css y %6.1f..1071.5  %s" % (s / 2.0, prev))
