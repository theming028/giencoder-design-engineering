#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r66 证据图合成：① 泳道内滚+固定标题栏  ② 蒙层高斯模糊改前后"""
import os
from PIL import Image, ImageDraw, ImageFont

EV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ev')
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'   # idx0=W3 常规 / idx2=W6 粗
FONT_FALLBACK = '/System/Library/Fonts/STHeiti Medium.ttc'


def font(sz, bold=False):
    for path, idx in ((FONT, 2 if bold else 0), (FONT_FALLBACK, 1 if bold else 0)):
        try:
            return ImageFont.truetype(path, sz, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()


def label(d, xy, text, sz=22, fill=(31, 31, 31), bold=True):
    d.text(xy, text, font=font(sz, bold), fill=fill)


# ───────── 图 1：泳道内滚 + 固定标题栏 ─────────
HEAD_TOP, BODY_TOP, BODY_BOT = 265, 309, 879   # DOM 实测（.kb-col-head / .kb-col-body）
CROP = (0, 175, 1440, 900)
LANE0 = (29, 363)
RED = (226, 45, 45)
GRAY = (110, 110, 110)

top = Image.open(os.path.join(EV, '21-after.png')).convert('RGB').crop(CROP)
bot = Image.open(os.path.join(EV, '22-after-scrolled.png')).convert('RGB').crop(CROP)
W, H = top.size
PAD, GAP, GUT = 34, 30, 250
CAPH = 62
canvas = Image.new('RGB', (PAD * 2 + W + GUT, (CAPH + H) * 2 + GAP + PAD * 2 + 46), (250, 250, 250))
d = ImageDraw.Draw(canvas)


def draw_panel(img, y0, cap, capfill):
    label(d, (PAD, y0), cap, 25, capfill)
    y = y0 + CAPH
    canvas.paste(img, (PAD, y))
    gx = PAD + W
    # 右侧标注竖线 + 文字（尽量不侵入画板）
    def band(a, b, color, text):
        d.line([(gx + 6, y + (a - CROP[1])), (gx + 6, y + (b - CROP[1]))], fill=color, width=4)
        d.line([(gx + 6, y + (a - CROP[1])), (gx + 4, y + (a - CROP[1]))], fill=color, width=4)
        d.line([(gx + 6, y + (b - CROP[1])), (gx + 4, y + (b - CROP[1]))], fill=color, width=4)
        label(d, (gx + 16, y + (a + b) // 2 - CROP[1] - 14), text, 19, color, False)
    band(HEAD_TOP, BODY_TOP, RED, '标题栏 44px')
    label(d, (gx + 16, y + (HEAD_TOP + BODY_TOP) // 2 - CROP[1] + 8), '固定不滚 ↓', 19, RED, False)
    band(BODY_TOP, BODY_BOT, (0, 106, 250), '卡片滚动区')
    label(d, (gx + 16, y + (BODY_TOP + BODY_BOT) // 2 - CROP[1] + 8), 'overflow-y: auto', 19, (0, 106, 250), False)
    # 泳道 0 左右红线
    d.line([(PAD + LANE0[0], y), (PAD + LANE0[0], y + H)], fill=RED, width=2)
    d.line([(PAD + LANE0[1], y), (PAD + LANE0[1], y + H)], fill=RED, width=2)
    return y + H


y = PAD
y = draw_panel(top, y, '① 改后 · 滚前：泳道 0「待开始」显示第 1~5 张卡（首张在最上）', (31, 31, 31))
y += GAP
y = draw_panel(bot, y, '② 改后 · 泳道 0 滚到底：卡片整体上移，「待开始 · 12」标题栏位置分毫未动', (31, 31, 31))

label(d, (PAD, y + 14),
      '红框 = 泳道 0 的卡片滚动区；红竖条 = 标题栏（44px）。两张图标题栏 y 均为 265，正文区 309~879 完全重合。',
      19, GRAY, False)
canvas.save(os.path.join(EV, 'r66-1-scroll.png'))
print('saved r66-1-scroll.png', canvas.size)

# ───────── 图 2：蒙层高斯模糊 改前 / 改后 ─────────
a = Image.open(os.path.join(EV, '40-modal-before.png')).convert('RGB')
b = Image.open(os.path.join(EV, '41-modal-after.png')).convert('RGB')
CROP2 = (240, 120, 1200, 760)
a2, b2 = a.crop(CROP2), b.crop(CROP2)
w2, h2 = a2.size
canvas2 = Image.new('RGB', (w2 * 2 + PAD * 3, h2 + CAPH + PAD * 2), (250, 250, 250))
d2 = ImageDraw.Draw(canvas2)
label(d2, (PAD, PAD), '改前 · r65 口径：蒙层 rgba(31,31,31,.6)、无模糊；面板不透明白', 21, (31, 31, 31))
label(d2, (PAD * 2 + w2, PAD), '改后 · r66 全局统一：rgba(0,0,0,.4) + blur(10px)；面板 .95 + blur(12px)', 21, (0, 106, 250))
canvas2.paste(a2, (PAD, PAD + CAPH))
canvas2.paste(b2, (PAD * 2 + w2, PAD + CAPH))
d2.line([(PAD, PAD + CAPH - 4), (PAD + w2, PAD + CAPH - 4)], fill=(205, 205, 205), width=2)
d2.line([(PAD * 2 + w2, PAD + CAPH - 4), (PAD * 2 + w2 * 2, PAD + CAPH - 4)], fill=(205, 205, 205), width=2)
canvas2.save(os.path.join(EV, 'r66-2-modal.png'))
print('saved r66-2-modal.png', canvas2.size)
