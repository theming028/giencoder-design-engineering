# -*- coding: utf-8 -*-
"""笔画密度：标题 vs 行名（同 14px）-> 判字重"""
from PIL import Image
PNG="mg-work/r31/design/dispatch.png"; OX,OY,S=60,44,2.0
im=Image.open(PNG).convert("RGB"); px=im.load()
def d2p(x,y): return (int(round(OX+x*S)), int(round(OY+y*S)))
def lum(c): return (c[0]*299+c[1]*587+c[2]*114)/1000
def dens(x0,y0,x1,y1,thr):
    n=0; ink=0
    for yy in [y0+i*0.25 for i in range(0,int((y1-y0)*4)+1)]:
        for xx in [x0+i*0.25 for i in range(0,int((x1-x0)*4)+1)]:
            n+=1
            if lum(px[d2p(xx,yy)])<thr: ink+=1
    return ink, n, 100.0*ink/n
# 标题「将任务转派给：」x17..104.5 y20..33  -> 逐字取「将」x17..30
print("标题 将 :", dens(17,20,30,33,150))
print("标题 任 :", dens(31,20,44,33,150))
print("行名 邵 :", dens(53,161,66,174,150))
print("行名 禹 :", dens(67,161,80,174,150))
print("副标题 转 :", dens(16.5,45,26,56.5,180))
print("按钮 确 :", dens(133,441,146,454,235))
