# -*- coding: utf-8 -*-
"""r92 ①：把顶栏元素截图分段放大，便于肉眼判定点阵尺度。"""
from PIL import Image
import sys

src = sys.argv[1] if len(sys.argv) > 1 else 'mg-work/r92/raw/web-hdr-r92-base.png'
im = Image.open(src).convert('RGB')
W, H = im.size
print('src', W, H)

# 右 760px 1:1 + 右 380px 2x
a = im.crop((W - 760, 0, W, H))
z = im.crop((W - 380, 0, W, H)).resize((760, H * 2), Image.NEAREST)
pad = 10
out = Image.new('RGB', (760, H + pad + H * 2), (255, 0, 0))
out.paste(a, (0, 0))
out.paste(z, (0, H + pad))
out.save(src.replace('.png', '-zoom.png'))
print('saved', src.replace('.png', '-zoom.png'), out.size)

# 顺带量：图右端 20px 的最暗像素（点色）
px = [im.getpixel((W - 1 - i, j)) for i in range(20) for j in range(H)]
print('右缘最暗 =', min(px, key=lambda p: sum(p)))
