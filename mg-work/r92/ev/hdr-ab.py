# -*- coding: utf-8 -*-
"""r92 ①：1:1 可读的两种放法对照（右 720px），避免 Read 端缩放失真。"""
from PIL import Image

W, H = 1440, 48
BG = (244, 245, 246)
img = Image.open('assets/images/bg-img-1.png').convert('RGBA')
iw, ih = img.size

a = Image.new('RGB', (W, H), BG)
a.paste(img, (W - iw, (H - ih) // 2), img)

b = Image.new('RGB', (W, H), BG)
bw = round(iw * H / ih)
bimg = img.resize((bw, H), Image.LANCZOS)
b.paste(bimg, (W - bw, 0), bimg)

CROP = 720
out = Image.new('RGB', (CROP, H * 2 + 8), (255, 255, 255))
out.paste(a.crop((W - CROP, 0, W, H)), (0, 0))
out.paste(b.crop((W - CROP, 0, W, H)), (0, H + 8))
out.save('mg-work/r92/raw/hdr-ab-1x.png')
print('saved mg-work/r92/raw/hdr-ab-1x.png', out.size)
