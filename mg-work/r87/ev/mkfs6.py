# -*- coding: utf-8 -*-
"""6 级字号实测条：同一元素在 13/14/16/18/20/24 下的真实渲染 + 实测尺寸。"""
import io, json
from PIL import Image, ImageDraw, ImageFont

D = 'mg-work/r87/ev/'
LEV = [13, 14, 16, 18, 20, 24]

navs, cards, info = {}, {}, {}
for px in LEV:
    navs[px] = Image.open('%sfs_%d_nav.png' % (D, px)).convert('RGB')
    cards[px] = Image.open('%sfs_%d_card.png' % (D, px)).convert('RGB')
    d = json.loads(json.loads(io.open('%sfs_%d.txt' % (D, px), encoding='utf-8').read().strip()))
    info[px] = {'navH': navs[px].height, 'cardH': cards[px].height,
                'naviH': round(d['navCur'][3] - d['navCur'][1]),
                'rowH': round(d['rows']['字号'][3] - d['rows']['字号'][1]),
                'selW': round(d['r85ctl0'][2] - d['r85ctl0'][0]),
                'selH': round(d['r85ctl0'][3] - d['r85ctl0'][1]),
                'segH': round(d['seg0'][3] - d['seg0'][1])}

PAD, GAP, LAB, TITLE, K = 22, 14, 58, 62, 0.52
NAVW = 232
CW_ = int(840 * K)
NPW = 6 * NAVW + 5 * GAP
CPW = 6 * CW_ + 5 * GAP
W = PAD * 2 + max(NPW, CPW)
NAVH = max(n.height for n in navs.values())
CH = int(max(c.height for c in cards.values()) * K)
H = TITLE + LAB + NAVH + LAB + CH + PAD + 20
cv = Image.new('RGB', (W, H), (255, 255, 255))
dr = ImageDraw.Draw(cv)


def font(sz):
    for f in ('C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf'):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


dr.text((PAD, 14), 'r87 全局字号机制实测 · 6 档（默认 14px）· 同一元素真实渲染，非示意',
        font=font(24), fill=(15, 23, 42))
y = TITLE
dr.text((PAD, y), '左栏导航（.r85-nav-host）· 1:1', font=font(18), fill=(90, 90, 90))
y += 28
x = PAD
for px in LEV:
    im = navs[px]
    cv.paste(im, (x, y + (NAVH - im.height)))
    dr.rectangle([x, y, x + NAVW, y + NAVH], outline=(228, 228, 228))
    tag = '%d px%s' % (px, '（默认）' if px == 14 else '')
    dr.text((x, y + NAVH + 4), tag, font=font(16), fill=(55, 112, 247) if px == 14 else (60, 60, 60))
    dr.text((x, y + NAVH + 24), '导航高 %d' % info[px]['naviH'], font=font(14), fill=(140, 140, 140))
    x += NAVW + GAP
y += NAVH + LAB

dr.text((PAD, y), '内容卡片（.r85-card，首卡）· 等比 0.52', font=font(18), fill=(90, 90, 90))
y += 28
x = PAD
for px in LEV:
    im = cards[px].resize((CW_, int(cards[px].height * K)), Image.LANCZOS)
    cv.paste(im, (x, y))
    dr.rectangle([x, y, x + CW_, y + CH], outline=(228, 228, 228))
    dr.text((x, y + CH + 4), '行高 %d · select %d×%d · 分段 %d' % (info[px]['rowH'], info[px]['selW'], info[px]['selH'], info[px]['segH']),
            font=font(14), fill=(140, 140, 140))
    x += CW_ + GAP

cv.save(D + 'fs6_levels.png')
print('fs6_levels.png', cv.size)
for px in LEV:
    print(px, info[px])
