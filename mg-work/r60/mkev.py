#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r60 证据图：浏览态「隐藏 .td-side」改前 / 改后 左栏对照"""
from PIL import Image, ImageDraw, ImageFont

W_OUT = "/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r60/ev/30-r60-summary.png"
BEFORE = "/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r58/ev/20-browse-keep-left-1920.png"
AFTER = "/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r60/ev/10-browse-1920.png"

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
f_ttl = ImageFont.truetype(FONT, 26, index=0)
f_sub = ImageFont.truetype(FONT, 20, index=0)
f_note = ImageFont.truetype(FONT, 20, index=0)

# 左栏区域：x 8..628（左栏 16..616，600px 宽），y 36..1080
BOX = (8, 36, 628, 1080)
CW = BOX[2] - BOX[0]
CH = BOX[3] - BOX[1]

PAD, GAP, LBL, NOTE = 26, 26, 62, 56
W = PAD * 2 + CW * 2 + GAP
H = PAD + LBL + CH + NOTE

canvas = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(canvas)

panels = [
    (BEFORE, "改前 · r58 浏览态保留左栏 600px", "正文列仅 ≈332px：标题折 3 行，第一步流程示意被压成一条", (0x86, 0x86, 0x86)),
    (AFTER, "改后 · r60 浏览态隐藏属性栏", "正文列 ≈598px：标题 1 行，流程示意图完整展开", (0x00, 0x64, 0xFA)),
]

for i, (path, ttl, sub, col) in enumerate(panels):
    x0 = PAD + i * (CW + GAP)
    d.text((x0, PAD + 2), ttl, font=f_ttl, fill=col)
    d.text((x0, PAD + 34), sub, font=f_sub, fill=(0x4E, 0x4E, 0x4E))
    im = Image.open(path).convert("RGB").crop(BOX)
    canvas.paste(im, (x0, PAD + LBL))
    d.rectangle([x0 - 1, PAD + LBL - 1, x0 + CW, PAD + LBL + CH], outline=(0xE5, 0xE5, 0xE5))

y_note = PAD + LBL + CH + 18
d.text((PAD, y_note), "普通态未受影响：改后 1920 普通态截图与 r58 关闭态截图 md5 完全一致（bfdbba5a…）",
       font=f_note, fill=(0x86, 0x86, 0x86))

canvas.save(W_OUT)
print("saved", W_OUT, canvas.size)
