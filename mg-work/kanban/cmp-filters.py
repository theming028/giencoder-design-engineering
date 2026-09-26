# -*- coding: utf-8 -*-
"""筛选控件盒子边界 + 关闭按钮"""
from PIL import Image
D=Image.open(r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\design-modal.png').convert('RGB')
R=Image.open(r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\x-modal.png').convert('RGB')
def H(c): return '#%02X%02X%02X'%c

def edges(im, y, x0, x1, ref=(250,250,250), thr=18):
    """找出与背景明显不同的 1px 竖线（控件边框）"""
    out=[]
    for x in range(x0,x1):
        c=im.getpixel((x,y))
        if abs(c[0]-ref[0])+abs(c[1]-ref[1])+abs(c[2]-ref[2])>thr:
            out.append((x,H(c)))
    # 压缩连续
    res=[]
    for x,c in out:
        if res and x-res[-1][1]<=1: res[-1][1]=x
        else: res.append([x,x,c])
    return [(a,b,cc) for a,b,cc in res]

print('设计稿 y=124 竖线:', edges(D,124,140,900))
print('设计稿 y=124 竖线(右段):', edges(D,124,900,1300))
print()
print('渲染  y=128 竖线:', edges(R,128,40,760))
print()
def box(im,x0,x1,y0,y1,label):
    print(label)
    for y in range(y0,y1):
        row=[(x,H(im.getpixel((x,y)))) for x in range(x0,x1)]
        dk=[(x,c) for x,c in row if sum(c)<620]
        if dk: print('   y%3d'%y, dk[:14])
print()
print('设计稿 关闭按钮区 x1210-1300 y60-110')
for y in range(60,110):
    dk=[(x,H(D.getpixel((x,y)))) for x in range(1210,1300) if sum(D.getpixel((x,y)))<640]
    if dk: print('   y%3d'%y, dk[:10])
print()
print('渲染 关闭按钮区 x1150-1230 y70-120')
for y in range(70,120):
    dk=[(x,H(R.getpixel((x,y)))) for x in range(1150,1230) if sum(R.getpixel((x,y)))<640]
    if dk: print('   y%3d'%y, dk[:10])
