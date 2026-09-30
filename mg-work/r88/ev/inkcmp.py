# -*- coding: utf-8 -*-
import os
from PIL import Image
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(REPO, 'mg-work', 'r88', 'raw')
dg = Image.open(os.path.join(D, 'arch@2x_rgb.png')).convert('RGB').resize((840, 658), Image.LANCZOS)
import sys
WEBF = sys.argv[1] if len(sys.argv) > 1 else 'web-arch-hover@1x.png'
web = Image.open(os.path.join(D, WEBF)).convert('RGB')

def ink(im, box, thr=0.55):
    x0,y0,x1,y1 = box
    px = im.load()
    vals=[(x,y,px[x,y]) for y in range(y0,y1) for x in range(x0,x1)]
    lum=[0.299*r+0.587*g+0.114*b for _,_,(r,g,b) in vals]
    mx=max(lum); pts=[(x,y) for (x,y,_),l in zip(vals,lum) if l < mx*thr]
    if not pts: return None
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return (min(xs),min(ys),max(xs),max(ys),max(xs)-min(xs)+1,max(ys)-min(ys)+1,len(pts))

CASES = [
    ('页标题 已归档任务',      (0, 3, 200, 26)),
    ('页副标题',               (0, 30, 360, 50)),
    ('搜索占位「搜索已归档任务」',(24, 84, 200, 108)),
    ('下拉「全部项目」',        (24+620, 84, 180+620, 108)),
    ('清空钮文字',             (740, 16, 836, 44)),
    ('行1 标题',               (0, 145, 300, 172)),
    ('行1 元信息',             (16, 172, 300, 200)),
    ('行3 hover文字 恢复/删除', (700, 296, 830, 346)),
]
print('%-28s %-28s %-28s' % ('区域', 'DESIGN (x0,y0,x1,y1,w,h)', 'WEB'))
for name, box in CASES:
    a = ink(dg, box); b = ink(web, box)
    fa = '(%d,%d,%d,%d) w%d h%d' % a[:6] if a else '-'
    fb = '(%d,%d,%d,%d) w%d h%d' % b[:6] if b else '-'
    print('%-28s %-28s %-28s' % (name, fa, fb))
