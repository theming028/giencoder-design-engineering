# -*- coding: utf-8 -*-
"""列位置 / 段落横向文字分布"""
from PIL import Image

def colprof(path, y0, y1, x0, x1, thr=170):
    im = Image.open(path).convert('RGB'); out=[]
    for x in range(x0, x1):
        n=0
        for y in range(y0, y1):
            r,g,b = im.getpixel((x,y))
            if (r*299+g*587+b*114)//1000 < thr: n+=1
        out.append((x,n))
    return out

def groups(p, gap=12, minn=1):
    res=[]; cur=None; last=None
    for x,n in p:
        if n>=minn:
            if cur is None: cur=[x,x]
            else:
                if x-cur[1] <= gap: cur[1]=x
                else: res.append(tuple(cur)); cur=[x,x]
            cur[1]=x
        last=x
    if cur: res.append(tuple(cur))
    return res

D=r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\design-modal.png'
R=r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\x-modal.png'

print('== 设计稿 表头横向文字组 (y168-178) ==')
print(groups(colprof(D,168,179,144,1300)))
print('== 设计稿 行1横向文字组 (y200-212) ==')
print(groups(colprof(D,200,213,144,1300)))
print('== 设计稿 筛选行文字组 (y117-129) ==')
print(groups(colprof(D,117,130,144,1300), gap=18))

print()
print('== 渲染 表头横向文字组 (y172-183) ==')
print(groups(colprof(R,172,184,56,1210)))
print('== 渲染 行1横向文字组 (y208-220) ==')
print(groups(colprof(R,208,221,56,1210)))
print('== 渲染 筛选行文字组 (y123-145) ==')
print(groups(colprof(R,123,146,56,1210), gap=18))

# 底部：footer 文字带
def bands(path,x0,x1,y0,y1,thr=150,minn=2):
    im=Image.open(path).convert('RGB'); res=[]; cur=None
    for y in range(y0,y1):
        n=0
        for x in range(x0,x1):
            r,g,b=im.getpixel((x,y))
            if (r*299+g*587+b*114)//1000<thr: n+=1
        if n>=minn:
            if cur is None: cur=[y,y,0]
            cur[1]=y; cur[2]=max(cur[2],n)
        else:
            if cur: res.append(tuple(cur)); cur=None
    if cur: res.append(tuple(cur))
    return res
print()
print('== 设计稿 底部文字带 y460-860 ==')
for b in bands(D,144,1300,460,860): print('   y%3d-%3d 高%2d max%3d'%(b[0],b[1],b[1]-b[0]+1,b[2]))
print('== 渲染 底部文字带 y460-560 ==')
for b in bands(R,56,1210,455,569): print('   y%3d-%3d 高%2d max%3d'%(b[0],b[1],b[1]-b[0]+1,b[2]))
