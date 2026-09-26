# -*- coding: utf-8 -*-
import io
from PIL import Image

def H(c): return '#%02X%02X%02X' % c
def dist(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

def runs_h(im, y, x0, x1, thr=10):
    out=[]; prev=None
    for x in range(x0,x1):
        c=im.getpixel((x,y))
        if prev is None or dist(c,prev)>thr: out.append([x,x,c]); prev=c
        else: out[-1][1]=x; prev=c
    return out

def runs_v(im, x, y0, y1, thr=10):
    out=[]; prev=None
    for y in range(y0,y1):
        c=im.getpixel((x,y))
        if prev is None or dist(c,prev)>thr: out.append([y,y,c]); prev=c
        else: out[-1][1]=y; prev=c
    return out

def show(runs, minlen=1, label=''):
    print(label, [(a,b,H(c)) for a,b,c in runs if b-a+1>=minlen])

D=Image.open(r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\design-modal.png').convert('RGB')
R=Image.open(r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\x-modal.png').convert('RGB')

print('=== 设计稿 1440x900 ===')
show(runs_h(D, 165, 100, 1400, 8), 3, 'y=165(第1行)  ')
show(runs_h(D, 300, 100, 1400, 8), 3, 'y=300(第6行)  ')
show(runs_v(D, 130, 30, 900, 8), 3, 'x=130(面板内边距)')
show(runs_v(D, 1000, 60, 900, 8), 3, 'x=1000(表格区) ')
show(runs_v(D, 200, 90, 220, 8), 1, 'x=200(表头+前2行)')

print()
print('=== 渲染 1264x569 ===')
show(runs_h(R, 170, 20, 1250, 8), 3, 'y=170(第1行)  ')
show(runs_h(R, 300, 20, 1250, 8), 3, 'y=300(第4行)  ')
show(runs_v(R, 40, 20, 569, 8), 3, 'x=40(面板左)  ')
show(runs_v(R, 900, 40, 569, 8), 3, 'x=900(表格区) ')
show(runs_v(R, 200, 100, 260, 8), 1, 'x=200(表头+前2行)')
