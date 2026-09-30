# -*- coding: utf-8 -*-
"""量设计稿「深度思考」卡正文的笔画色（判定 r101 ② 的档位）。

设计稿祖先链解析（node 绝对坐标，见 ev/findnode.py 同法）：
  1393:18748 容器 264
    1393:18489 容器 190  left 164 / top 592  840x268
      1393:18488 容器 189  left   0 / top  34  840x234
        1393:18487 容器 188  left  18 / top  34  822x200   ← 深度思考卡（DS text/text）
=> 绝对 board(182, 660) 822x200；PNG 坐标 = board + 1（design-rgb.png 1170x5146）。
"""
import io, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, '..', '..', 'r93', 'raw', 'design-rgb.png')
im = Image.open(PNG)
print('PNG', im.size, im.mode)
im = im.convert('RGBA')
bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
im = Image.alpha_composite(bg, im).convert('RGB')

L, T, W, H = 182 + 1, 660 + 1, 822, 200
box = im.crop((L, T, L + W, T + H))
px = box.load()
# 逐行统计：最暗像素（文字笔画）与"最暗那一档"的众数
from collections import Counter
dark = []
for y in range(H):
    row = [px[x, y] for x in range(W)]
    mn = min(sum(c) for c in row)
    dark.append(mn)
print('每行最暗灰度（前 12 行 + 后 4 行）:', dark[:12], dark[-4:])
cnt = Counter()
for y in range(H):
    for x in range(W):
        c = px[x, y]
        if sum(c) < 600:            # 比卡底 #F5F6F7(741) 明显暗
            cnt[c] += 1
print('卡内深色像素 Top10:', cnt.most_common(10))
