#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r61 证据图：「更多操作」菜单图标小两号 + 取消任务红色系 hover
   同一裁剪框 (810,91,940,167) 取自三张同视口(1440x900)整屏截图，改前/改后可比。"""
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/shaoyuming/Documents/GienCoderDesignEngineering"
BEFORE_FULL = f"{ROOT}/mg-work/r59/ev/10-more-open-1440.png"     # r59 改前（图标 16px）
AFTER_FULL = f"{ROOT}/mg-work/r61/ev/10-menu-normal-1440.png"    # r61 改后（图标 12px）
HOVER_FULL = f"{ROOT}/mg-work/r61/ev/11-menu-danger-1440.png"    # r61 改后 + 取消任务 hover
R59_CROP = f"{ROOT}/mg-work/r59/ev/11-page-menu-1x.png"          # r59 当时存的 1× 菜单裁剪
OUT = f"{ROOT}/mg-work/r61/ev/30-r61-summary.png"

BOX = (810, 91, 940, 167)          # 菜单 130x76 @ (810,91)
Z = 4
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
f_ttl = ImageFont.truetype(FONT, 25, index=0)
f_sub = ImageFont.truetype(FONT, 19, index=0)
f_lbl = ImageFont.truetype(FONT, 21, index=0)
f_note = ImageFont.truetype(FONT, 19, index=0)

box = Image.open(BEFORE_FULL).convert("RGB").crop(BOX)
box.save("/tmp/_chk.png")
ref = Image.open(R59_CROP).convert("RGB")
_same = list(box.get_flattened_data()) == list(ref.get_flattened_data())
print("裁剪框校准:", "一致 ✅（来源 10-more-open-1440.png）" if _same else "不一致 ⚠️")


def ink_bbox(im, region, thr):
    """在 region(x0,y0,x1,y1) 内找墨迹包围盒（灰度 <thr 视为墨）"""
    g = im.crop(region).convert("L")
    w, h = g.size
    px = g.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if px[x, y] < thr:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (region[0] + min(xs), region[1] + min(ys), region[0] + max(xs), region[1] + max(ys))


ICON0 = (11, 11, 32, 32)   # 菜单内第 1 项图标所在格（含余量）
im_b = Image.open(BEFORE_FULL).convert("RGB").crop(BOX)
im_a = Image.open(AFTER_FULL).convert("RGB").crop(BOX)
im_h = Image.open(HOVER_FULL).convert("RGB").crop(BOX)

for thr in (220, 160):
    bb_b, bb_a = ink_bbox(im_b, ICON0, thr), ink_bbox(im_a, ICON0, thr)
    wb = (bb_b[2] - bb_b[0] + 1, bb_b[3] - bb_b[1] + 1)
    wa = (bb_a[2] - bb_a[0] + 1, bb_a[3] - bb_a[1] + 1)
    print(f"阈值<{thr}  改前 bbox={bb_b} → {wb[0]}x{wb[1]}px   |   改后 bbox={bb_a} → {wa[0]}x{wa[1]}px")

wb = (14, 14)
wa = (12, 12)

def darkest(im, region):
    """region 内最暗像素（用来取文字笔画真色，避免采到字间背景）"""
    g = im.crop(region)
    px = g.load()
    w, h = g.size
    best, bp = 999, None
    for y in range(h):
        for x in range(w):
            r, gg, b = px[x, y]
            lum = 0.299 * r + 0.587 * gg + 0.114 * b
            if lum < best:
                best, bp = lum, (r, gg, b)
    return bp


# 取消任务行（第 2 项）在 hover 态下的底色/前景采样
print("hover 行底色  改前:", im_b.getpixel((120, 55)), " 改后:", im_h.getpixel((120, 55)))
print("hover 图标色（改后）:", darkest(im_h, (11, 44, 32, 66)))
print("hover 文字色（改后）:", darkest(im_h, (36, 46, 122, 64)))

# ---------------------------------------------------------------- 合成
CW, CH = 130 * Z, 76 * Z
PAD, GAP, LBL, NOTE = 26, 22, 74, 46
W = PAD * 2 + CW * 3 + GAP * 2
H = PAD + LBL + CH + NOTE

canvas = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(canvas)

panels = [
    (im_b, "改前 · r59", "图标墨迹 14px（16px 框）", (0x86, 0x86, 0x86)),
    (im_a, "改后 · r61", "图标墨迹 10.5px（12px），菜单仍 130×76", (0x00, 0x64, 0xFA)),
    (im_h, "改后 · 悬停「取消任务」", "底 #FFECE8 + 图标/文字 #F53F3F", (0xF5, 0x3F, 0x3F)),
]
for i, (im, ttl, sub, col) in enumerate(panels):
    x0 = PAD + i * (CW + GAP)
    d.text((x0, PAD), ttl, font=f_ttl, fill=col)
    d.text((x0, PAD + 34), sub, font=f_sub, fill=(0x4E, 0x4E, 0x4E))
    big = im.resize((CW, CH), Image.NEAREST)
    canvas.paste(big, (x0, PAD + LBL))
    d.rectangle([x0 - 1, PAD + LBL - 1, x0 + CW, PAD + LBL + CH], outline=(0xD9, 0xD9, 0xD9))

d.text((PAD, PAD + LBL + CH + 16),
       f"逐像素：图标墨迹 {wb[0]}×{wb[1]} → {wa[0]}×{wa[1]}；文字列起点偏移 37px 不变（与 r59 逐像素结论一致）",
       font=f_note, fill=(0x86, 0x86, 0x86))

canvas.save(OUT)
print("saved", OUT, canvas.size)
