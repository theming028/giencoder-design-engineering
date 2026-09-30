# -*- coding: utf-8 -*-
"""r86 取证：拼「设计稿 | r85 改前 | r86 改后」三方对照 + 局部放大（select 与分割线）。"""
import io
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
W, H = 840, 918


def load(p, w=W, h=H):
    im = Image.open(p)
    if im.mode == 'RGBA':
        im = Image.alpha_composite(Image.new('RGBA', im.size, (255, 255, 255, 255)), im).convert('RGB')
    else:
        im = im.convert('RGB')
    return im.resize((w, h), Image.LANCZOS)


design = load(os.path.join(REPO, 'mg-work', 'r85', 'raw', 'design_1389-18725.png'))
before = load(os.path.join(REPO, 'mg-work', 'r85', 'ev', 'shot_page.png'))
after = load(os.path.join(REPO, 'mg-work', 'r86', 'ev', 'after_page.png'))

GAP, PAD, TOP = 16, 20, 34
cw, ch = W, H
canvas = Image.new('RGB', (PAD * 2 + cw * 3 + GAP * 2, TOP + ch + PAD), (255, 255, 255))
d = ImageDraw.Draw(canvas)
for i, (im, label) in enumerate([(design, '设计稿 1389:18725 (840x919)'),
                                 (before, 'r85 实机 改前'),
                                 (after, 'r86 实机 改后')]):
    x = PAD + i * (cw + GAP)
    d.text((x + 2, 12), label, fill=(31, 31, 31))
    canvas.paste(im, (x, TOP))
canvas.save(os.path.join(HERE, 'cmp_r86.png'))

# ---------- 局部放大：卡片1（3 个 select + 2 条分割线） ----------
CROP = (0, 40, 840, 300)   # 卡片1 区域（页面坐标）
Z = 2
files = [('设计稿', design), ('r85 改前', before), ('r86 改后', after)]
bw, bh = (CROP[2] - CROP[0]) * Z, (CROP[3] - CROP[1]) * Z
zoom = Image.new('RGB', (PAD * 2 + bw * 3 + GAP * 2, 34 + bh + 56 + PAD), (255, 255, 255))
dz = ImageDraw.Draw(zoom)
for i, (label, im) in enumerate(files):
    box = im.crop(CROP).resize((bw, bh), Image.NEAREST)
    x = PAD + i * (bw + GAP)
    dz.text((x + 2, 12), '%s  (卡片1 放大 %dx)' % (label, Z), fill=(31, 31, 31))
    zoom.paste(box, (x, 34))
# 底部色卡：分割线 / 图标底 取色对比
sy = 34 + bh + 14
for i, (label, im) in enumerate(files):
    x = PAD + i * (bw + GAP)
    line = im.getpixel((400, 253))     # 卡片1 第一/二行之间的分割线
    icon = im.getpixel((70, 100))      # 行图标底
    dz.rectangle([x, sy, x + 28, sy + 16], fill=line, outline=(200, 200, 200))
    dz.rectangle([x + 36, sy, x + 64, sy + 16], fill=icon, outline=(200, 200, 200))
    dz.text((x + 74, sy + 2), '分割线 %s / 图标底 %s' % ('#%02X%02X%02X' % line, '#%02X%02X%02X' % icon),
            fill=(31, 31, 31))
zoom.save(os.path.join(HERE, 'cmp_r86_zoom.png'))
print('cmp_r86.png', canvas.size)
print('cmp_r86_zoom.png', zoom.size)
