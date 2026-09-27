# -*- coding: utf-8 -*-
"""对设计稿里若干候选底色做连通域分析，输出每个色块的包围盒。"""
import collections
from PIL import Image

im = Image.open("mg-work/kanban/root/board-design.png").convert("RGB")
px = im.load()
W, H = im.size

TARGETS = [
    (0xE7, 0xF0, 0xFF),
    (0xEF, 0xF4, 0xFF),
    (0xF5, 0xE8, 0xFF),
    (0xFF, 0xE8, 0xF1),
    (0xFF, 0xF3, 0xE8),
]


def comps(color, minrun=8):
    mask = [[False] * W for _ in range(H)]
    for y in range(H):
        row = mask[y]
        for x in range(W):
            if px[x, y] == color:
                row[x] = True
    seen = [[False] * W for _ in range(H)]
    out = []
    for y in range(H):
        for x in range(W):
            if not mask[y][x] or seen[y][x]:
                continue
            stack = [(x, y)]
            seen[y][x] = True
            x0 = x1 = x
            y0 = y1 = y
            n = 0
            while stack:
                cx, cy = stack.pop()
                n += 1
                if cx < x0: x0 = cx
                if cx > x1: x1 = cx
                if cy > y1: y1 = cy
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < W and 0 <= ny < H and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            if n >= minrun * minrun // 4 and (x1 - x0 + 1) >= minrun:
                out.append((x0, y0, x1, y1, n))
    return sorted(out, key=lambda r: (r[1], r[0]))


for c in TARGETS:
    cs = comps(c)
    print("\n#%02X%02X%02X  rgb%s  连通域 %d 个（面积>=16）" % (c[0], c[1], c[2], str(c), len(cs)))
    for (x0, y0, x1, y1, n) in cs[:14]:
        print("   x%4d..%-4d y%4d..%-4d  %3dx%-3d  px=%d" % (x0, x1, y0, y1, x1 - x0 + 1, y1 - y0 + 1, n))
