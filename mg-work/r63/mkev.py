# -*- coding: utf-8 -*-
"""
r63 证据图合成
  30-r63-weight.png    ① 同一句话在两个泳道的 3× 同串 A/B；② 两列全部标题并排
  31-r63-shimmer.png   新配色（深底 + 品牌蓝扫光）6 个确定性相位
"""
from PIL import Image, ImageDraw, ImageFont

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
EV = ROOT + '/mg-work/r63/ev'

BASE = EV + '/41-ph01-1440.png'        # currentTime=0 → 高光带完全落在文字区外，纯静置色
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
f_h1 = ImageFont.truetype(FONT, 30, index=1)
f_h2 = ImageFont.truetype(FONT, 23, index=1)
f_sub = ImageFont.truetype(FONT, 19, index=0)
f_lb = ImageFont.truetype(FONT, 20, index=0)
f_note = ImageFont.truetype(FONT, 18, index=0)
f_cell = ImageFont.truetype(FONT, 17, index=0)

C_TX = (31, 31, 31)
C_SUB = (134, 134, 134)
C_DIM = (78, 78, 78)
C_ACC = (55, 112, 247)
C_BG = (255, 255, 255)
C_PANEL = (247, 248, 250)
C_LINE = (229, 229, 229)

W = 1110
M = 30


def ink(im):
    im = im.convert('L')
    return sum(1 for p in im.getdata() if p < 200)


# ---------------------------------------------------------------- 图 1
base = Image.open(BASE).convert('RGB')

# 同串 A/B：进行中 #3 与 待开始 #2 都是「读取业务方原始需求文档」
AB_BOX_DOING = (400, 569, 575, 593)     # 175 x 24
AB_BOX_TODO = (50, 455, 225, 479)
ab_doing = base.crop(AB_BOX_DOING)
ab_todo = base.crop(AB_BOX_TODO)

Z_AB = 3
Z_STRIP = 1.6

# 全列标题条（x0 带 4px 左余量，宽 300）
DOING_STRIPS = [(396, 318, 696, 348), (396, 432, 696, 484), (396, 566, 696, 596),
                (396, 678, 696, 708), (396, 790, 696, 820)]
TODO_STRIPS = [(46, 318, 346, 370), (46, 452, 346, 482), (46, 564, 346, 616),
               (46, 698, 346, 750), (46, 832, 346, 884)]

img = Image.new('RGB', (W, 1000), C_BG)
d = ImageDraw.Draw(img)

y = 30
d.text((M, y), 'r63 · 任务看板「进行中」泳道：卡片标题字重 → 中粗 500', font=f_h1, fill=C_TX)
y += 44
d.text((M, y), '规则：.kb-col--doing .kb-card-title { font-weight: 500 }　其余泳道保持 400（hover 才 500）',
       font=f_sub, fill=C_SUB)
y += 40
d.line([(M, y), (W - M, y)], fill=C_LINE)
y += 20

# ---- ① 同串 A/B ----
d.text((M, y), '① 同一句话「读取业务方原始需求文档」在两个泳道的实测（3× 放大）', font=f_h2, fill=C_TX)
y += 36

rows = [('进行中 · font-weight 500', ab_doing), ('待开始 · font-weight 400', ab_todo)]
for label, crop in rows:
    d.text((M, y + 2), label, font=f_lb, fill=C_ACC if '500' in label else C_DIM)
    z = crop.resize((crop.width * Z_AB, crop.height * Z_AB), Image.NEAREST)
    img.paste(z, (M + 300, y))
    n = ink(crop)
    d.text((M + 300 + z.width + 16, y + 24), '墨迹 %d px' % n, font=f_note, fill=C_DIM)
    y += z.height + 14

d.text((M, y), '两串 advanceWidth 均为 154px（等宽、不产生任何位移），同窗口墨迹 %d → %d px（+%.0f%%）—— 加粗可见且零重排。'
       % (ink(ab_todo), ink(ab_doing), (ink(ab_doing) / ink(ab_todo) - 1) * 100),
       font=f_note, fill=C_SUB)
y += 40

d.line([(M, y), (W - M, y)], fill=C_LINE)
y += 20

# ---- ② 两列全部标题并排 ----
d.text((M, y), '② 两列全部卡片标题并排（1.6× 放大；左：进行中 全 500　右：待开始 全 400）', font=f_h2, fill=C_TX)
y += 38

col_x = [M, M + 540]
d.text((col_x[0], y), '进行中 (kb-col--doing) · 5 张', font=f_lb, fill=C_ACC)
d.text((col_x[1], y), '待开始 (kb-col--todo) · 5 张', font=f_lb, fill=C_DIM)
y += 30

top = y
yy = y
for box in DOING_STRIPS:
    c = base.crop(box)
    z = c.resize((int(c.width * Z_STRIP), int(c.height * Z_STRIP)), Image.LANCZOS)
    img.paste(z, (col_x[0], yy))
    d.rectangle([col_x[0], yy, col_x[0] + z.width - 1, yy + z.height - 1], outline=(226, 232, 240))
    yy += z.height + 8
end_doing = yy

yy = top
for box in TODO_STRIPS:
    c = base.crop(box)
    z = c.resize((int(c.width * Z_STRIP), int(c.height * Z_STRIP)), Image.LANCZOS)
    img.paste(z, (col_x[1], yy))
    d.rectangle([col_x[1], yy, col_x[1] + z.width - 1, yy + z.height - 1], outline=(226, 232, 240))
    yy += z.height + 8
end_todo = yy

y = max(end_doing, end_todo) + 10
d.text((M, y), '左列 5 张标题全部为 500（含第 3 张走文字流光的「读取业务方原始需求文档」，此处相位已钉在静置色）。',
       font=f_note, fill=C_SUB)
y += 36

img = img.crop((0, 0, W, y))
img.save(EV + '/30-r63-weight.png')
print('30-r63-weight.png', img.size, ' A/B 墨迹: doing=%d todo=%d' % (ink(ab_doing), ink(ab_todo)))

# ---------------------------------------------------------------- 图 2
SB = (396, 566, 566, 596)      # 流光标题盒 170 x 30
PH = [('0 ms', '100%', '4 1-ph01-1440.png'),
      ('350 ms', '82.5%', '4 2-ph02-1440.png'),
      ('700 ms', '65%', '4 3-ph03-1440.png'),
      ('1050 ms', '47.5%', '4 4-ph04-1440.png'),
      ('1400 ms', '30%', '4 5-ph05-1440.png'),
      ('1750 ms', '12.5%', '4 6-ph06-1440.png')]
PH = [(a, b, EV + '/' + c.replace(' ', '')) for a, b, c in PH]

Z_SB = 3
cw = (SB[2] - SB[0]) * Z_SB
ch = (SB[3] - SB[1]) * Z_SB
gap = 30

H2 = 28 + 44 + 30 + 26 + 22 + 3 * (ch + 46) + 30
img2 = Image.new('RGB', (W, H2), C_BG)
d2 = ImageDraw.Draw(img2)
y = 28
d2.text((M, y), 'r63 · 「执行中」卡片标题文字流光：新配色（深底 + 品牌蓝扫光）', font=f_h1, fill=C_TX)
y += 44
d2.text((M, y), '静置 = --color-text-1  rgb(31, 31, 31)　·　高光 = --color-primary-6  rgb(55, 112, 247)'
                '（与同卡「执行中」蓝标签同源）', font=f_sub, fill=C_SUB)
y += 30
d2.text((M, y), 'background-size 250% × 100%　·　background-position 100% → 0%　·　2s 线性无限循环',
        font=f_sub, fill=C_SUB)
y += 26
d2.line([(M, y), (W - M, y)], fill=C_LINE)
y += 22

x0 = M
for i, (t, pos, path) in enumerate(PH):
    col = i % 2
    row = i // 2
    cx = x0 + col * (cw + gap)
    cy = y + row * (ch + 46)
    src = Image.open(path).convert('RGB').crop(SB)
    z = src.resize((cw, ch), Image.NEAREST)
    img2.paste(z, (cx, cy))
    d2.rectangle([cx, cy, cx + cw - 1, cy + ch - 1], outline=C_LINE)

    # 高光带定位：找「偏蓝」像素（b − r > 50）的 x 区间。
    # ⚠️ 不能用「亮度高」判定 —— 白底本身就是最亮的，会把背景误判成高光。
    w0, h0 = src.size
    bcols = []
    for xx in range(w0):
        for yy2 in range(h0):
            p = src.getpixel((xx, yy2))
            if p[2] - p[0] > 50:
                bcols.append(xx)
                break
    if bcols:
        lo, hi = min(bcols), max(bcols)
        inkx = [xx for xx in range(w0)
                if any(src.getpixel((xx, yy2))[0] < 150 for yy2 in range(h0))]
        x0i, x1i = (min(inkx), max(inkx)) if inkx else (0, w0 - 1)
        tag = '高光带 x%d–%d（文字区 x%d–%d）' % (lo, hi, x0i, x1i)
        on = lo >= x0i - 2 and hi <= x1i + 4
    else:
        tag = '高光已在文字区外（整串纯静置色）'
        on = False
    d2.text((cx, cy + ch + 8), 'currentTime %s · background-position %s' % (t, pos),
            font=f_cell, fill=C_TX)
    d2.text((cx, cy + ch + 26), tag, font=f_cell, fill=C_ACC if on else C_SUB)

H = y + 3 * (ch + 46) + 10
img2 = img2.crop((0, 0, W, H))
img2.save(EV + '/31-r63-shimmer.png')
print('31-r63-shimmer.png', img2.size)
