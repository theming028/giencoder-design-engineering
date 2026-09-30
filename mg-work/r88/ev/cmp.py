# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageChops, ImageDraw
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(REPO, 'mg-work', 'r88', 'raw')
dg = Image.open(os.path.join(D, 'arch@2x_rgb.png')).convert('RGB').resize((840, 658), Image.LANCZOS)
import sys
WEBF = sys.argv[1] if len(sys.argv) > 1 else 'web-arch-hover@1x.png'
web = Image.open(os.path.join(D, WEBF)).convert('RGB')
assert dg.size == web.size == (840, 658), (dg.size, web.size)

def band(a, b, name):
    diff = ImageChops.difference(a, b).convert('L')
    g = diff.point(lambda v: 255 if v > 28 else 0)
    n = sum(g.point(lambda v: 1 if v else 0).getdata())
    print('%s: >28 灰阶差像素 %d / %d = %.2f%%' % (name, n, 840 * 658, 100.0 * n / (840 * 658)))
    return g

g = band(dg, web, '全页')
# 只比结构区（去掉文字密集的行内主体）：行右侧按钮列 + 分隔线带
for y0, y1, tag in [(0, 130, '头部+工具条'), (132, 658, '列表卡'), (136, 658, '列表卡内')]:
    a = dg.crop((0, y0, 840, y1)); b = web.crop((0, y0, 840, y1))
    band(a, b, tag)

GAP, LBL = 10, 18
W = 840
out = Image.new('RGB', (W + 20, (658 + LBL + GAP) * 2 + 46), (255, 255, 255))
d = ImageDraw.Draw(out)
y = 0
d.text((4, y + 3), 'DESIGN  (MasterGo 1393:18344, 2x -> 1x)', fill=(0, 0, 0)); y += LBL
out.paste(dg, (10, y)); y += 658 + GAP
d.text((4, y + 3), 'WEB  (row3 hovered = design state)', fill=(0, 0, 0)); y += LBL
out.paste(web, (10, y)); y += 658 + GAP
d.text((4, y + 3), 'DIFF  (>28 gray levels)', fill=(200, 0, 0)); y += LBL
out.paste(g.convert('RGB'), (10, y))
p = os.path.join(D, 'cmp-arch-hover.png')
out.save(p)
print('->', p, out.size)
