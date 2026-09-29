# -*- coding: utf-8 -*-
"""r84 取证图：设计稿 vs 实现 —— ① 两枚图标 ② 点击删除图标后的确认态
   设计稿坐标 = 节点内坐标（PNG 需 +DX,DY）；实现坐标 = 抽屉**元素截图**内的像素。
   两边窗口取同样大，直接并排可比。
   ★ 实现侧截图 s2_click.png = 点「删除会话」图标之后的确认态（v3 交互定稿）。
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RAW = os.path.join(REPO, 'mg-work', 'r83', 'raw', 'design_1389-18518.png')
SHOT = os.path.join(HERE, 's2_click.png')
OUT = os.path.join(HERE, 'cmp_r84.png')
DX, DY = 3, 2

design = Image.open(RAW).convert('RGB')
impl = Image.open(SHOT).convert('RGB')


def dnode(b):
    return design.crop((b[0] + DX, b[1] + DY, b[2] + DX, b[3] + DY))


def shot(b):
    return impl.crop(b)


# ① 图标窗口 60×28（各自把自己那对图标摆在窗口中间）
#    设计稿：图标按钮 row 内 x376..432 ⇒ 节点 x396..452；实现：行宽少 4 ⇒ 整体左移 4
ICON_D = dnode((395, 83, 455, 111))
ICON_I = shot((389, 83, 449, 111))
# ② 确认态窗口 142×36（取消起笔 + 确定删除收笔）
CONF_D = dnode((314, 194, 458, 230))
CONF_I = shot((311, 195, 455, 231))

try:
    F = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 17)
    FS = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 14)
except Exception:
    F = FS = ImageFont.load_default()

Z1, Z2 = 7, 5
GAP, PAD, HEAD, LBL = 20, 22, 46, 30
rows = [
    ('① 两枚图标 · 左 = 导出 / 右 = 删除', ICON_D, ICON_I, Z1),
    ('② 点击「删除会话」图标 → 图标组换成 [取消][确定删除]', CONF_D, CONF_I, Z2),
]

need = max(a.width * z + GAP + b.width * z for _, a, b, z in rows)
W = PAD * 2 + need
H = HEAD + sum(LBL + a.height * z + GAP for _, a, _, z in rows) + PAD
canvas = Image.new('RGB', (W, H), (252, 252, 252))
dr = ImageDraw.Draw(canvas)
dr.text((PAD, 12), 'r84：左 = 设计稿 1389:18518   右 = 实现 pages/avatar.html', fill=(20, 20, 20), font=F)
dr.text((PAD, 12 + 22), '表格线内为同一逻辑窗口，等比放大（① ×7、② ×5，最近邻）；② 两侧都是「确认态」', fill=(130, 130, 130), font=FS)

y = HEAD
for cap, imd, imi, z in rows:
    dr.text((PAD, y), cap, fill=(30, 30, 30), font=F)
    y += LBL
    a = imd.resize((imd.width * z, imd.height * z), Image.NEAREST)
    b = imi.resize((imi.width * z, imi.height * z), Image.NEAREST)
    canvas.paste(a, (PAD, y))
    x2 = PAD + a.width + GAP
    canvas.paste(b, (x2, y))
    dr.rectangle([PAD - 1, y - 1, PAD + a.width, y + a.height], outline=(205, 205, 205))
    dr.rectangle([x2 - 1, y - 1, x2 + b.width, y + b.height], outline=(205, 205, 205))
    y += a.height + GAP

canvas.save(OUT)
print('WROTE', OUT, canvas.size)
