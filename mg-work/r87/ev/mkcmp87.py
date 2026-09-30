# -*- coding: utf-8 -*-
"""r87 改前/改后对照图（v3）。

素材：元素截图 `el_{before,now}_page.png`（.r85-page 840×918）与
`el_{before,now}_nav.png`（.r85-nav-host 232×268）。
已用像素扫描确证两组图**特征行位置完全一致**（nav 选中底 76..111；page 内容首行 5）
⇒ 可直接按同一矩形裁剪对齐。

裁剪坐标 = 实测绝对矩形 − 元素原点（page 原点 (510,85)｜nav 原点 (18,48)）。
"""
from PIL import Image, ImageDraw, ImageFont

D = 'mg-work/r87/ev/'
pb = Image.open(D + 'el_before_page.png').convert('RGB')
pa = Image.open(D + 'el_now_page.png').convert('RGB')
nb = Image.open(D + 'el_before_nav.png').convert('RGB')
na = Image.open(D + 'el_now_nav.png').convert('RGB')

STRIP_W = 820          # 统一条宽（page 元素宽 840；留 20 边）
K = 1.3

# (标题, 左, 上, 右, 下, 用哪组图, 说明)
ROWS = [
    ('① 左栏导航：选中项文字变主题蓝 rgb(55,112,247) + 字重 500', 0, 58, 232, 124, 'nav',
     '仅文字色/字重变（像素差异区：行 87..99 · 列 36..91）'),
    ('② 字号调节器（6 级）· ③ 外观分段控件 → DS Button -secondary -size-large 128×40', 0, 602, 840, 740, 'page',
     '分段三颗 = DS Button；选中项 2px 虚线框由本页适配层叠加'),
    ('④ 版本更新按钮 -size-default 104×32 · ⑤ 退出登录 -secondary + 红字', 0, 772, 840, 908, 'page',
     'DS 无「带边框 + 危险色文字」组合 ⇒ 退出登录走适配层红字'),
    ('⑥ Select：去 --select-ring / 8px 圆角 / 宽度自适应 + 右对齐', 600, 62, 840, 198, 'page',
     '无内联 width；右缘贴行右缘（实测 ctlRight = rowRight = 1330）'),
]

PAD, GAP, HDR, TITLE = 20, 16, 40, 52
SW = int(STRIP_W * K)
LH = [int((r[4] - r[3]) * K) for r in ROWS]
H = TITLE + sum(HDR + int((r[4] - r[2]) * K) + 22 + GAP for r in ROWS) + PAD
CW = PAD * 2 + SW * 2 + GAP + 8

cv = Image.new('RGB', (CW, int(H) + 10), (255, 255, 255))
dr = ImageDraw.Draw(cv)


def font(sz):
    for f in ('C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf'):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f_t, f_h, f_c, f_n = font(23), font(17), font(17), font(14)
dr.text((PAD, 14), 'r87 改前（r86 态） → 改后（r87 态） · 设置页 · 视口 1600×1100 · 默认 14px',
        font=f_t, fill=(15, 23, 42))
y = TITLE
x0b, x0a = PAD, PAD + SW + GAP + 8
dr.text((x0b, y), '改前（r86）', font=f_c, fill=(132, 132, 132))
dr.text((x0a, y), '改后（r87）', font=f_c, fill=(55, 112, 247))
y += 28

for (title, l, t, r, b, src, note) in ROWS:
    dr.text((PAD, y), title, font=f_h, fill=(31, 31, 31))
    y += 26
    dr.text((PAD, y), note, font=f_n, fill=(140, 140, 140))
    y += HDR - 22
    hh = int((b - t) * K)
    for x0, srcimg in ((x0b, pb if src == 'page' else nb), (x0a, pa if src == 'page' else na)):
        strip = Image.new('RGB', (STRIP_W, b - t), (255, 255, 255))
        c = srcimg.crop((l, t, r, b))
        strip.paste(c, (0, 0))
        strip = strip.resize((SW, hh), Image.LANCZOS)
        cv.paste(strip, (x0, y))
        dr.rectangle([x0, y, x0 + SW, y + hh], outline=(230, 230, 230))
    dr.rectangle([x0a, y, x0a + SW, y + hh], outline=(55, 112, 247))
    y += hh + GAP

cv.save(D + 'cmp_r87.png')
print('cmp_r87.png', cv.size)
