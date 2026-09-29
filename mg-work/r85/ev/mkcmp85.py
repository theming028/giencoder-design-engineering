# -*- coding: utf-8 -*-
"""r85 拼接「设计稿 ↔ 实机」对照图。
   A 区：整页 1:1（设计稿 2x 降采样 vs 实机 1x 截图）
   B 区：两处细节 ×2（设计稿原生 2x vs 实机 1x 放大 2 倍）
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, '..', 'raw'))
DESIGN = os.path.join(RAW, 'design_1389-18725.png')
PAGE = os.path.join(HERE, 'shot_page.png')
OUT = os.path.join(HERE, 'cmp_r85.png')

def font(sz):
    for p in (r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\msyhbd.ttc', r'C:\Windows\Fonts\simhei.ttf'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()

F14, F13 = font(14), font(13)

d = Image.open(DESIGN).convert('RGBA')
d = Image.alpha_composite(Image.new('RGBA', d.size, (255, 255, 255, 255)), d).convert('RGB')   # 透明区补白
d1 = d.resize((840, 919), Image.LANCZOS)
a1 = Image.open(PAGE).convert('RGB')

# ---------------- A 区 ----------------
GAP, PAD, HDR = 16, 14, 34
W = PAD * 2 + 840 * 2 + GAP
# ---------------- B 区（细节，原生 2x vs 放大 2x）----------------
# 设计坐标（逻辑 px）→ 裁切区；实机同坐标（.r85-page 原点一致）
DETAIL = [
    ('字号滑块（卡片2 第 5 行）', (560, 610, 838, 656)),
    ('卡片3 首行控件组', (500, 780, 838, 826)),
]
DH = sum((b[3] - b[1]) * 2 + 26 for _, b in DETAIL) + 8
HA = PAD + HDR + 919 + PAD
AK = a1.height / 918.0
H = HA + HDR + DH + PAD

canvas = Image.new('RGB', (W, H), (250, 250, 251))
dr = ImageDraw.Draw(canvas)

dr.text((PAD, 8), '设计稿 MasterGo 1389:18725（840×919，2x 导出降采样）', fill=(20, 20, 20), font=F14)
dr.text((PAD + 840 + GAP, 8), '实机 pages/settings.html（.r85-page 840×918）', fill=(20, 20, 20), font=F14)
canvas.paste(d1, (PAD, PAD + 12))
canvas.paste(a1.resize((840, 919), Image.NEAREST), (PAD + 840 + GAP, PAD + 12))
dr.rectangle([PAD - 1, PAD + 11, PAD + 840, PAD + 12 + 919], outline=(200, 200, 205))
dr.rectangle([PAD + 840 + GAP - 1, PAD + 11, PAD + 840 * 2 + GAP, PAD + 12 + 919], outline=(200, 200, 205))

y = HA
dr.line([PAD, y - 6, W - PAD, y - 6], fill=(215, 215, 220))
dr.text((PAD, y + 2), '细节 ×2（设计稿原生 2x ／ 实机 1x 放大 2 倍）', fill=(20, 20, 20), font=F14)
y += HDR

for name, (x0, y0, x1, y1) in DETAIL:
    dw, dh = (x1 - x0) * 2, (y1 - y0) * 2
    cd = d.crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2))
    ca = a1.crop((int(x0 * AK), int(y0 * AK), int(x1 * AK), int(y1 * AK))).resize((dw, dh), Image.LANCZOS)
    dr.text((PAD, y), name, fill=(20, 20, 20), font=F13)
    yy = y + 22
    canvas.paste(cd, (PAD, yy))
    canvas.paste(ca, (PAD + dw + GAP, yy))
    dr.rectangle([PAD - 1, yy - 1, PAD + dw, yy + dh], outline=(200, 200, 205))
    dr.rectangle([PAD + dw + GAP - 1, yy - 1, PAD + dw * 2 + GAP, yy + dh], outline=(200, 200, 205))
    y = yy + dh + 26

canvas.save(OUT)
print('saved', OUT, canvas.size)
