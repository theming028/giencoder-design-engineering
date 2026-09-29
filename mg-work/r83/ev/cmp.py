# -*- coding: utf-8 -*-
"""r83 · 会话历史：设计稿 vs 实现 对照图
   设计稿 design_1389-18518.png 488x990，节点原点落在 PNG (3,2)，内容 482x984
   实现   impl_hs.png           480x944（#av-chat-drawer 元素截图，含左右各 1px 边框）
   → 左右并排（各带 32px 标头）+ 第 3 栏 50% 叠图（对齐到表头左上角）
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'raw')
DESIGN = os.path.join(RAW, 'design_1389-18518.png')
IMPL = os.path.join(HERE, 'impl_hs.png')
OUT = os.path.join(HERE, 'cmp_hs.png')

DX, DY = 3, 2            # 设计稿 PNG 的节点原点偏移
PAD = 16
HEAD = 32

d = Image.open(DESIGN).convert('RGB').crop((DX, DY, DX + 482, DY + 984))
i = Image.open(IMPL).convert('RGB')

# 叠图：把实现按「边框 1px」对到设计稿的 (0,0)
W = min(d.width, i.width)
H = min(d.height, i.height)
ov = Image.blend(d.crop((0, 0, W, H)), i.crop((0, 0, W, H)), 0.5)

cols = [(d, '设计稿 1389:18518  482x984'), (i, '实现 avatar.html  480x944'), (ov, '50%% 叠图 %dx%d' % (W, H))]
w = PAD + sum(c.width + PAD for c, _ in cols)
h = HEAD + max(c.height for c, _ in cols) + PAD
canvas = Image.new('RGB', (w, h), (250, 250, 250))
dr = ImageDraw.Draw(canvas)

x = PAD
for im, label in cols:
    dr.rectangle([x - 1, HEAD - 1, x + im.width, HEAD + im.height], outline=(200, 200, 200))
    canvas.paste(im, (x, HEAD))
    dr.text((x + 2, HEAD - 20), label, fill=(40, 40, 40))
    x += im.width + PAD

# 表头/列表分界参考线（y = 表头 48 + 标头）
for yy in (HEAD + 48,):
    dr.line([(0, yy), (w, yy)], fill=(255, 90, 90))

canvas.save(OUT)
print('WROTE', OUT, canvas.size)
