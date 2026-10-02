# -*- coding: utf-8 -*-
"""把真机截图里的关键区域裁出来拼成一张对照图（省 token，也便于人眼核对）。"""
from PIL import Image
RAW = r'E:/GienCoder/giencoder-design-engineering/mg-work/r109/raw'
OUT = RAW + '/l2-evidence.png'
Z = 2

crops = [
    ('f-zd-mini.png', (560, 80, 900, 170), '① 右栏展开 ⇒ zd 折成胶囊'),
    ('d2-anchor-committed.png', (940, 280, 1360, 460), '④ 提交后：锚点已落，气泡收起'),
    ('d2-anchor-reopen.png', (940, 300, 1360, 520), '④ 单击锚点 ⇒ 编辑态详情重开'),
    ('e2-anchor-corner-note.png', (760, 750, 1440, 900), '⑤配套 底角锚点 ⇒ 气泡夹回可视区'),
]
pad, top = 10, 26
w = max(c[1][2] - c[1][0] for c in crops)
total_h = sum((c[1][3] - c[1][1]) * Z + top + pad for c in crops)
canvas = Image.new('RGB', (w * Z + pad * 2, total_h + pad), (245, 245, 245))
y = pad
for f, box, cap in crops:
    im = Image.open(RAW + '/' + f).convert('RGB').crop(box)
    im = im.resize((im.size[0] * Z, im.size[1] * Z), Image.NEAREST)
    canvas.paste(im, (pad, y + top))
    y += im.size[1] + top + pad
canvas.save(OUT)
print('写出', OUT, canvas.size)
