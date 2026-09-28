"""r65：把「设计稿 2×」与「实现 2×」的弹窗面板并排拼成对照证据图。

设计稿面板矩形：alpha 通道切边得到 img(48,32)-(1008,*) ⇒ 960 宽 = 480 CSS px（精确 2×）。
页面面板矩形：在 2880×1800 的 2× 截图里，遮罩把背景压暗、面板恒为纯白 → 纯白像素 bbox 即面板。
"""
from PIL import Image, ImageDraw, ImageFont

DS = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'
EV = '/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r65/ev/'
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'

# 设计稿：面板左上角都在 (48,32)，宽 960
DESIGN = {
    'cancel': (DS + '容器-165_1350-18230.png', (48, 32, 1008, 940)),   # 960×908 ⇒ 480×454
    'stop':   (DS + '容器-171_1350-18236.png', (48, 32, 1008, 864)),   # 960×832 ⇒ 480×416
}
# 页面：两个弹窗的面板矩形相同（本页两条 desc 都是 1 行、任务名都是 1 行）
PAGE = {
    'cancel': (EV + '20-cancel-2x.png', (960, 468, 1920, 1332)),       # 960×864 ⇒ 480×432
    'stop':   (EV + '21-stop-2x.png', (960, 468, 1920, 1332)),
}
ROWS = [
    ('cancel', '取消任务  ·  MasterGo 1350:18230', '设计稿 480×454 ｜ 实现 480×432'),
    ('stop',   '终止任务  ·  MasterGo 1350:18236', '设计稿 480×416 ｜ 实现 480×432'),
]

f_h1 = ImageFont.truetype(FONT, 28, index=0)
f_sub = ImageFont.truetype(FONT, 18, index=0)
f_row = ImageFont.truetype(FONT, 22, index=1)
f_cap = ImageFont.truetype(FONT, 18, index=0)

COLW = 960
M, GAP = 30, 26
TOP = 26
HDR = TOP + 42 + 30 + 18        # 大标题 + 副标题 + 分隔线后留白 = 116
ROW_H = [max(Image.open(DESIGN[k][0]).crop(DESIGN[k][1]).height,
             Image.open(PAGE[k][0]).crop(PAGE[k][1]).height) for k, _, _ in ROWS]
# 每行：28(行标题) + 26(列标注) + 图max高 + 24(尺寸标注) + 22(行距)
W = M * 2 + COLW * 2 + GAP
H = HDR + sum(28 + 26 + h + 24 + 22 for h in ROW_H)
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

y = TOP
d.text((M, y), 'r65 · 任务详情页「取消任务 / 终止任务」弹窗 · 设计稿（左）↔ 实现（右）',
       font=f_h1, fill=(31, 31, 31))
y += 42
d.text((M, y), '两边都是 2× 原图裁切、1:1 显示，按面板左上角对齐。量测口径：设计稿面板矩形由 alpha 通道切边、'
               '页面面板矩形由纯白像素 bbox 取得，均为 960 宽 = 480 CSS px。',
       font=f_sub, fill=(78, 78, 78))
y += 30
d.line([(M, y), (W - M, y)], fill=(229, 229, 229))

for (key, title, sub), h in zip(ROWS, ROW_H):
    y += 22
    d.text((M, y), title, font=f_row, fill=(55, 112, 247))
    d.text((M + 430, y + 3), sub, font=f_cap, fill=(134, 134, 134))
    y += 34
    for col in (0, 1):
        d.text((M + col * (COLW + GAP), y),
               '设计稿（MasterGo 2×）' if col == 0 else '实现（页面 2×）',
               font=f_cap, fill=(134, 134, 134))
    y += 24
    for col, src in ((0, DESIGN[key]), (1, PAGE[key])):
        cx = M + col * (COLW + GAP)
        c = Image.open(src[0]).convert('RGB').crop(src[1])
        img.paste(c, (cx, y))
        d.rectangle([cx - 1, y - 1, cx + c.width, y + c.height], outline=(229, 229, 229))
        d.text((cx, y + c.height + 5), '%.0f × %.0f CSS px' % (c.width / 2, c.height / 2),
               font=f_cap, fill=(134, 134, 134))
    y += h + 24

img.crop((0, 0, W, y + 12)).save(EV + '40-modal-design-vs-impl.png')
print('saved 40-modal-design-vs-impl.png', img.crop((0, 0, W, y + 12)).size)

