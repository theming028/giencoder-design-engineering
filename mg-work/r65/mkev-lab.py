"""r65：把 现状 / A / B 三方案的四相位裁剪拼成运动条证据图（同一张卡、同一句标题）"""
from PIL import Image, ImageDraw, ImageFont

EV = '/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r65/ev/'
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
PHASES = ['ph-0.10.png', 'ph-0.35.png', 'ph-0.60.png', 'ph-0.85.png']
LBL = ['相位 0.10', '相位 0.35', '相位 0.60', '相位 0.85']

# 三张卡片几何完全一致（318×104 + 14px 下边距），只是所在格子不同
BOX = {'now': (69, 244, 387, 362), 'A': (533, 244, 851, 362), 'B': (997, 264, 1315, 382)}
ROWS = [
    ('now', 'now · 现状 · 标题文字渐变扫光', '标题被 background-clip:text 透明化，静置时必然比同排其它卡弱 —— 这就是“差强人意”的根因'),
    ('A',   'A · 卡片描边流光', '标题完全静止（正文色 text-1）；光带绕卡片 1px 描边走一圈，2.4s'),
    ('B',   'B · 底部不确定进度条', '标题完全静止；卡底边 3px 光条左右往返，1.5s · alternate'),
]
ZOOM, PAD = 2, 10

f_h1 = ImageFont.truetype(FONT, 26, index=0)
f_h2 = ImageFont.truetype(FONT, 21, index=1)
f_sub = ImageFont.truetype(FONT, 17, index=0)
f_cap = ImageFont.truetype(FONT, 16, index=0)

M, GAPX, GAPY = 26, 18, 14
cw = (851 - 533 + PAD * 2) * ZOOM
ch = (362 - 244 + PAD * 2) * ZOOM
W = M * 2 + cw * 4 + GAPX * 3
# 表头 116 = 26(top) + 40(大标题) + 32(副标题) + 18(分隔线后留白)
# 每行 = 28(方案名) + 24(说明) + ch(图) + 36(相位标签) + GAPY
H = 116 + (28 + 24 + ch + 36 + GAPY) * len(ROWS) + 4
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

y = 26
d.text((M, y), 'r65 · 「执行中」卡片状态动效 · 运动过程（每行 4 个相位，同一张卡同一句标题）',
       font=f_h1, fill=(31, 31, 31))
y += 40
d.text((M, y), '三行的标题文字本身都完全相同；差别只在“正在进行”这件事被画在哪里。'
               '相位 = 把该行所有动画钉在同一相对进度（WAAPI currentTime）后截图。',
       font=f_sub, fill=(78, 78, 78))
y += 32
d.line([(M, y), (W - M, y)], fill=(229, 229, 229))
y += 18

for key, title, note in ROWS:
    d.text((M, y), title, font=f_h2, fill=(55, 112, 247))
    y += 28
    d.text((M, y), note, font=f_sub, fill=(134, 134, 134))
    y += 24
    for i, ph in enumerate(PHASES):
        im = Image.open(EV + ph).convert('RGB')
        x0, y0, x1, y1 = BOX[key]
        c = im.crop((x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD)).resize((cw, ch), Image.LANCZOS)
        cx = M + i * (cw + GAPX)
        img.paste(c, (cx, y))
        d.rectangle([cx, y, cx + cw - 1, y + ch - 1], outline=(229, 229, 229))
        d.text((cx, y + ch + 5), LBL[i], font=f_cap, fill=(134, 134, 134))
    y += ch + 36 + GAPY

img.crop((0, 0, W, y + 4)).save(EV + '31-shimmer-motion.png')
print('saved 31-shimmer-motion.png', img.size)
