# -*- coding: utf-8 -*-
"""r87 关键细节 4× 放大对照（改前 r86 vs 改后 r87）。"""
from PIL import Image, ImageDraw, ImageFont

D = 'mg-work/r87/ev/'
pb = Image.open(D + 'el_before_page.png').convert('RGB')
pa = Image.open(D + 'el_now_page.png').convert('RGB')
nb = Image.open(D + 'el_before_nav.png').convert('RGB')
na = Image.open(D + 'el_now_nav.png').convert('RGB')

# (标题, l, t, r, b, k, 组)
Z = [
    ('① 导航选中项：文字变主题蓝 + 字重 500', 4, 74, 150, 116, 3.4, 'nav'),
    ('⑥-select 触发框：去 ring（外扩 1px 同色圈）/ 圆角 4→8px', 700, 60, 840, 122, 4.2, 'page'),
    ('⑥-select 宽度自适应（原本 JS 写死内联 width）', 600, 140, 840, 200, 4.2, 'page'),
    ('③ 分段控件 浅色/深色：DS Button -secondary -size-large 40px', 540, 684, 760, 736, 4.0, 'page'),
    ('④ 版本更新/检查更新：DS Button -secondary -size-default 32px', 600, 776, 840, 832, 4.0, 'page'),
    ('⑤ 退出登录：-secondary + 危险色文字（新）', 590, 852, 840, 906, 4.0, 'page'),
]

PAD, GAP, HDR, TITLE = 22, 18, 44, 56
SW = max(int((z[3] - z[1]) * z[5]) for z in Z)
H = TITLE + sum(HDR + int((z[4] - z[2]) * z[5]) + GAP for z in Z) + PAD
CW = PAD * 2 + SW * 2 + GAP + 8
cv = Image.new('RGB', (CW, H), (255, 255, 255))
dr = ImageDraw.Draw(cv)


def font(sz):
    for f in ('C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf'):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


dr.text((PAD, 16), 'r87 关键细节 4× 放大 · 左 = 改前（r86）｜右 = 改后（r87）',
        font=font(25), fill=(15, 23, 42))
y = TITLE
x0b, x0a = PAD, PAD + SW + GAP + 8

for (title, l, t, r, b, k, src) in Z:
    dr.text((PAD, y), title, font=font(19), fill=(31, 31, 31))
    y += HDR
    hh = int((b - t) * k)
    ww = int((r - l) * k)
    for x0, img in ((x0b, pb if src == 'page' else nb), (x0a, pa if src == 'page' else na)):
        c = img.crop((l, t, r, b)).resize((ww, hh), Image.LANCZOS)
        cv.paste(c, (x0, y))
        dr.rectangle([x0, y, x0 + ww, y + hh], outline=(228, 228, 228))
    dr.rectangle([x0a, y, x0a + ww, y + hh], outline=(55, 112, 247))
    y += hh + GAP

cv.save(D + 'cmp_r87_zoom.png')
print('cmp_r87_zoom.png', cv.size)
