# -*- coding: utf-8 -*-
"""r92 ①：顶栏背景图两种放法的离线预览（不占 browser）。

A. background-size 默认(auto)：图片按原始 1580×134 铺，右对齐 ⇒ 48px 高的顶栏只看到
   图片竖直中段（y 43..91），且因 1580 > 1440 左侧被裁掉 140px。
B. background-size: auto 100%：整张图缩到顶栏高 48px（宽 566），完整渐变都在，占右侧 566px。
"""
from PIL import Image, ImageDraw

W, H = 1440, 48
BG = (244, 245, 246)          # 顶栏自身底色 #F4F5F6
img = Image.open('assets/images/bg-img-1.png').convert('RGBA')
iw, ih = img.size


def canvas():
    c = Image.new('RGB', (W, H), BG)
    return c


# ---------- A：原始尺寸、右对齐、竖直居中 ----------
a = canvas()
left = W - iw                 # -140
top = (H - ih) // 2           # -43
a.paste(img, (left, top), img)   # paste 自带裁剪

# ---------- B：高度撑满 100%、右对齐 ----------
bh = H
bw = round(iw * H / ih)
b = canvas()
bimg = img.resize((bw, bh), Image.LANCZOS)
b.paste(bimg, (W - bw, 0), bimg)

out = Image.new('RGB', (W, H * 2 + 12), (255, 255, 255))
out.paste(a, (0, 0))
out.paste(b, (0, H + 12))
out = out.resize((W, (H * 2 + 12) * 2), Image.NEAREST)
out.save('mg-work/r92/raw/hdr-preview.png')

# 右侧细节 2x 放大（各取右 600px）
za = a.crop((W - 600, 0, W, H)).resize((1200, H * 2), Image.NEAREST)
zb = b.crop((W - 600, 0, W, H)).resize((1200, H * 2), Image.NEAREST)
z = Image.new('RGB', (1200, H * 4 + 12), (255, 255, 255))
z.paste(za, (0, 0))
z.paste(zb, (0, H * 2 + 12))
z.save('mg-work/r92/raw/hdr-preview-zoom.png')

print('A(auto 原尺寸): 图片绘制原点 x=%d y=%d ⇒ 顶栏被图片完全覆盖，看到图片 y43..91 的横带' % (left, top))
print('B(auto 100%%):  图片 %d×%d，落在 x %d..%d' % (bw, bh, W - bw, W))
print('图像底色 #F6F8FA vs 顶栏底色 #F4F5F6 ⇒ Δ=(2,3,4)')
