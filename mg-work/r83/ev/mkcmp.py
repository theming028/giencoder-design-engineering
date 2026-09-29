# -*- coding: utf-8 -*-
"""生成对照页：把候选 SVG 渲染出来，与设计稿 PNG 的实测裁剪并排，判断哪一个才是设计稿里的图标。
   产物：mg-work/r83/raw/cmp_icon.html（用 file:// 直开截图）
"""
import base64
import io
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PNG = os.path.join(REPO, 'mg-work', 'r83', 'raw', 'design_1389-18518.png')
DX, DY = 3, 2
Z = 10


def crop_b64(x0, y0, x1, y1, z=Z):
    im = Image.open(PNG).convert('RGB').crop((x0 + DX, y0 + DY, x1 + DX, y1 + DY))
    im = im.resize((im.width * z, im.height * z), Image.NEAREST)
    b = io.BytesIO()
    im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def svg_text(path):
    with io.open(os.path.join(REPO, path), encoding='utf-8') as f:
        return f.read()


# 设计稿：左枚（导出）与右枚（删除候选）
D_LEFT = crop_b64(400, 86, 419, 105)
D_RIGHT = crop_b64(432, 86, 451, 105)

LEFT_SVG = svg_text('mg-work/r83/raw/1389-18518__svg_5f4f2e22.svg')
DEL_SVG = svg_text('assets/icons/delete.svg')
DELFILL_SVG = svg_text('assets/icons/delete-fill.svg')

ROW = ('<div class="cell"><div class="cap">%s</div>%s</div>')


def cell(cap, inner):
    return ROW % (cap, inner)


def svgbox(svg, px, bg='#F2F2F2'):
    return ('<div class="box" style="background:%s">' % bg +
            svg.replace('<svg ', '<svg style="width:%dpx;height:%dpx;color:#868686" ' % (px, px)) +
            '</div>')


html = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;padding:20px;background:#fff;font:12px/1.5 -apple-system,'Segoe UI',sans-serif;color:#1f1f1f}
h3{margin:0 0 10px;font-size:13px}
.row{display:flex;gap:24px;align-items:flex-start;margin-bottom:26px;flex-wrap:wrap}
.cell{display:flex;flex-direction:column;gap:6px;align-items:center}
.cap{font-size:11px;color:#666}
.box{width:140px;height:140px;display:flex;align-items:center;justify-content:center;outline:1px solid #ddd}
</style></head><body>
<h3>A · 设计稿实测（10× 最近邻放大）</h3>
<div class="row">
%s
%s
</div>
<h3>B · 候选矢量（渲染 140px = 10×）</h3>
<div class="row">
%s
%s
%s
</div>
</body></html>""" % (
    cell('设计稿 左枚 = 导出', '<img class="box" src="%s">' % D_LEFT),
    cell('设计稿 右枚 = 删除？', '<img class="box" src="%s">' % D_RIGHT),
    cell('mgfetch svg_5f4f2e22（导出）', svgbox(LEFT_SVG, 140)),
    cell('assets/icons/delete.svg', svgbox(DEL_SVG, 140)),
    cell('assets/icons/delete-fill.svg', svgbox(DELFILL_SVG, 140)),
)

out = os.path.join(REPO, 'mg-work', 'r83', 'raw', 'cmp_icon.html')
with io.open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print('WROTE', out)
