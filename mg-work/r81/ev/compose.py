# -*- coding: utf-8 -*-
"""把 r81 的截图拼成两张对照证据图。"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
EV = HERE          # 本脚本就放在 ev/ 里

F_BOLD = 'C:/Windows/Fonts/msyhbd.ttc'
F_REG = 'C:/Windows/Fonts/msyh.ttc'
SCALE = 2
CROP_W = 480          # 只裁顶栏左侧（改动都在左簇）


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_header(src, w=CROP_W):
    im = Image.open(os.path.join(EV, src)).convert('RGB')
    box = im.crop((0, 0, w, 48))
    return box.resize((w * SCALE, 48 * SCALE), Image.LANCZOS)


def compose_topbar():
    rows = [
        ('改前 · dev（触发器在顶栏右侧，看不到）', 'full-dev-before.png', (120, 120, 120)),
        ('改后 · dev', 'full-dev.png', (20, 20, 20)),
        ('改后 · kanban', 'full-kanban.png', (20, 20, 20)),
        ('改后 · req-kanban', 'full-req-kanban.png', (20, 20, 20)),
        ('改后 · task-detail', 'full-task-detail.png', (20, 20, 20)),
    ]
    pad = 20
    lab_h = 26
    gap = 10
    img_w = CROP_W * SCALE
    W = img_w + pad * 2
    H = pad * 2 + len(rows) * (lab_h + 48 * SCALE + gap) - gap
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    f = font(F_BOLD, 17)
    y = pad
    for lab, src, col in rows:
        d.text((pad, y), lab, font=f, fill=col)
        y += lab_h
        im = crop_header(src)
        canvas.paste(im, (pad, y))
        d.rectangle([pad, y, pad + img_w - 1, y + 48 * SCALE - 1], outline=(200, 200, 200))
        y += 48 * SCALE + gap
    out = os.path.join(EV, 'r81-topbar.png')
    canvas.save(out)
    print('写出', out, canvas.size)


def compose_popup():
    im = Image.open(os.path.join(EV, 'full-dev-open.png')).convert('RGB')
    pop = im.crop((88, 41, 88 + 388, 41 + 526))
    pop = pop.resize((388 * SCALE, 526 * SCALE), Image.LANCZOS)
    # 顶栏连同浮窗顶部一起裁，左缘都从 x=0 起 —— 便于直观看「浮窗左缘 = 触发器左缘」
    top = im.crop((0, 0, 620, 96)).resize((620 * SCALE, 96 * SCALE), Image.LANCZOS)
    pad = 20
    lab_h = 26
    W = max(pop.width, top.width) + pad * 2
    H = pad * 2 + lab_h + top.height + 14 + lab_h + pop.height
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(F_BOLD, 17)
    y = pad
    d.text((pad, y), '顶栏左簇：红绿灯 → 20px → 触发器（浮窗左缘与之左对齐）', font=f, fill=(20, 20, 20))
    y += lab_h
    canvas.paste(top, (pad, y))
    d.rectangle([pad, y, pad + top.width - 1, y + top.height - 1], outline=(200, 200, 200))
    y += top.height + 14
    d.text((pad, y), '浮窗 388x526（设计稿同尺寸）', font=f, fill=(20, 20, 20))
    y += lab_h
    canvas.paste(pop, (pad, y))
    d.rectangle([pad, y, pad + pop.width - 1, y + pop.height - 1], outline=(200, 200, 200))
    out = os.path.join(EV, 'r81-popup-2x.png')
    canvas.save(out)
    print('写出', out, canvas.size)


if __name__ == '__main__':
    compose_topbar()
    compose_popup()
