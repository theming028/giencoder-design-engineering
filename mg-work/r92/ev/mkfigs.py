# -*- coding: utf-8 -*-
"""r92 汇报用三张对照图（都在 1x 或放大后可读的尺度）。"""
from PIL import Image, ImageDraw

R = 'mg-work/r92/raw/'


def load(p):
    return Image.open(R + p).convert('RGB')


# ---------- 1) 设置页 aside：改前 | 改后（取上半段，3x 放大） ----------
CROP = (0, 0, 200, 232)
a = load('web-aside-r91sat.png').crop(CROP)
b = load('web-aside-r92-def.png').crop(CROP)
Z = 2
a = a.resize((a.width * Z, a.height * Z), Image.NEAREST)
b = b.resize((b.width * Z, b.height * Z), Image.NEAREST)
gap = 14
out = Image.new('RGB', (a.width * 2 + gap, a.height), (255, 60, 60))
out.paste(a, (0, 0))
out.paste(b, (a.width + gap, 0))
out.save(R + 'r92-aside-ab.png')
print('r92-aside-ab.png', out.size)

# ---------- 2) 顶栏：改前（无图）| 改后（有图），取右 700px ----------
W = 1920
before_hdr = Image.new('RGB', (W, 48), (244, 245, 246))     # 改前 = 纯底色 #F4F5F6
after_hdr = load('web-hdr-r92-base.png')
c = (W - 700, 0, W, 48)
a2 = before_hdr.crop(c)
b2 = after_hdr.crop(c)
out2 = Image.new('RGB', (700, 48 * 2 + gap), (255, 60, 60))
out2.paste(a2, (0, 0))
out2.paste(b2, (0, 48 + gap))
out2 = out2.resize((700 * 2, (48 * 2 + gap) * 2), Image.NEAREST)
out2.save(R + 'r92-hdr-ab.png')
print('r92-hdr-ab.png', out2.size)

# ---------- 3) 权限触发器：默认权限 | 完全访问 ----------
def2 = load('web-perm-def-r92.png')
full = load('web-perm-full-r92.png')
w = max(def2.width, full.width)
h = max(def2.height, full.height)
Z3 = 3
out3 = Image.new('RGB', (w * Z3, (h * 2 + 8) * Z3), (255, 60, 60))
out3.paste(def2.resize((def2.width * Z3, def2.height * Z3), Image.NEAREST), (0, 0))
out3.paste(full.resize((full.width * Z3, full.height * Z3), Image.NEAREST), (0, (h + 8) * Z3))
out3.save(R + 'r92-perm-ab.png')
print('r92-perm-ab.png', out3.size)
