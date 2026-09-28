#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r62 证据图：「执行中」卡片标题文字流光 —— 6 个确定性相位（WAAPI currentTime 钉死）
   量测口径：标题盒内逐列取最小灰度，<90 记为「在高光带内」。
   高光 = --color-text-1(#1F1F1F, 灰度31)；静置 = --color-text-3(#868686, 灰度134)，
   两者差 ≈103，阈值取偏黑侧的 90 最稳。"""
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/shaoyuming/Documents/GienCoderDesignEngineering"
EV = f"{ROOT}/mg-work/r62/ev"
OUT = f"{EV}/30-r62-summary.png"

BOX = (394, 564, 586, 598)      # 标题周围留白 192x34
TITLE = (400, 570, 562, 592)    # 标题盒本体 162x22（fit-content 后 = 文字154 + 右内距8）
Z = 3
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
f_ttl = ImageFont.truetype(FONT, 25, index=0)
f_cell = ImageFont.truetype(FONT, 19, index=0)
f_band = ImageFont.truetype(FONT, 19, index=0)
f_note = ImageFont.truetype(FONT, 19, index=0)

PH = [("41-ph01-1440.png", 0, "100%"), ("42-ph02-1440.png", 350, "82.5%"),
      ("43-ph03-1440.png", 700, "65%"), ("44-ph04-1440.png", 1050, "47.5%"),
      ("45-ph05-1440.png", 1400, "30%"), ("46-ph06-1440.png", 1750, "12.5%")]


def band_span(im):
    g = im.crop(TITLE).convert("L")
    w, h = g.size
    px = g.load()
    cols = [x for x in range(w) if min(px[x, y] for y in range(h)) < 90]
    if not cols:
        return None
    off = TITLE[0] - BOX[0]
    return (off + min(cols), off + max(cols))


CW, CH = (BOX[2] - BOX[0]) * Z, (BOX[3] - BOX[1]) * Z
PAD, GAP, CAP = 26, 18, 30
COLS = 2
W = PAD * 2 + COLS * CW + (COLS - 1) * GAP
H = PAD + 46 + 3 * (CH + CAP + GAP) + 74

canvas = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(canvas)
d.text((PAD, PAD), "「执行中」卡片标题文字流光 · 6 个确定性相位（WAAPI currentTime 钉死，可复现）",
       font=f_ttl, fill=(0x1F, 0x1F, 0x1F))

stats = []
for i, (fn, t, posv) in enumerate(PH):
    im = Image.open(f"{EV}/{fn}").convert("RGB")
    sp = band_span(im)
    stats.append((t, posv, sp))
    r, c = divmod(i, COLS)
    x0 = PAD + c * (CW + GAP)
    y0 = PAD + 46 + r * (CH + CAP + GAP)
    canvas.paste(im.crop(BOX).resize((CW, CH), Image.NEAREST), (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + CW, y0 + CH], outline=(0xD9, 0xD9, 0xD9))
    on = "高光带在文字上" if sp else "光带在文字区外"
    col = (0x00, 0x64, 0xFA) if sp else (0x86, 0x86, 0x86)
    d.text((x0, y0 + CH + 7),
           f"t={t}ms · pos {posv} · {on}" + (f" x{sp[0]}–{sp[1]}" if sp else ""),
           font=f_cell, fill=col)

y_note = H - 74 + 8
d.text((PAD, y_note),
       "配色：静置 --color-text-3(#868686) · 高光 --color-text-1(#1F1F1F) ｜ 带宽 = 11 字 × spread(2) = 44px ｜ 2s 线性无限循环",
       font=f_note, fill=(0x4E, 0x4E, 0x4E))
d.text((PAD, y_note + 26),
       "同页另外 16 张卡片标题实测：animation: none / background-image: none / color: rgb(31,31,31) —— 零影响",
       font=f_note, fill=(0x86, 0x86, 0x86))

canvas.save(OUT)
for t, posv, sp in stats:
    print(f"  t={t:>4}ms  pos={posv:<7} 带宽={'x%d-%d' % sp if sp else '不在文字上'}")
print("saved", OUT, canvas.size)
