# -*- coding: utf-8 -*-
"""定位设计稿里精确出现的目标色像素，判断哪些元素用的是『原色』。"""
import sys
from PIL import Image

im = Image.open("mg-work/kanban/root/board-design.png").convert("RGB")
px = im.load()
W, H = im.size

TARGETS = ["3770F7", "3D6EBF", "7A4B9E", "A74B6F", "F5319D", "722ED1", "4E4E4E", "868686"]

for hx in TARGETS:
    t = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))
    mask = [[False] * W for _ in range(H)]
    n = 0
    for y in range(H):
        for x in range(W):
            if px[x, y] == t:
                mask[y][x] = True
                n += 1
    if n == 0:
        print("\n#%s  出现 0 次" % hx)
        continue
    seen = [[False] * W for _ in range(H)]
    out = []
    for y in range(H):
        for x in range(W):
            if not mask[y][x] or seen[y][x]:
                continue
            st = [(x, y)]
            seen[y][x] = True
            x0 = x1 = x
            y0 = y1 = y
            k = 0
            while st:
                cx, cy = st.pop()
                k += 1
                x0 = min(x0, cx); x1 = max(x1, cx); y0 = min(y0, cy); y1 = max(y1, cy)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < W and 0 <= ny < H and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        st.append((nx, ny))
            out.append((x0, y0, x1, y1, k))
    out.sort(key=lambda r: -r[4])
    print("\n#%s  总 %d px，%d 个色块，TOP8：" % (hx, n, len(out)))
    for (x0, y0, x1, y1, k) in out[:8]:
        print("   x%4d..%-4d y%4d..%-4d  %3dx%-3d px=%d" % (x0, x1, y0, y1, x1 - x0 + 1, y1 - y0 + 1, k))
