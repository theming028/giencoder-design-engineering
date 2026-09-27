# -*- coding: utf-8 -*-
"""圆角终测：扫「左边缘列」上直线段的起始 y -> r = 起始偏移"""
from PIL import Image
PNG="mg-work/r31/design/dispatch.png"; OX,OY,S=60,44,2.0
im=Image.open(PNG).convert("RGB"); px=im.load()
def d2p(x,y): return (int(round(OX+x*S)), int(round(OY+y*S)))
def near(c,t,tol=5): return all(abs(c[i]-t[i])<=tol for i in range(3))

def edge_start(name, top, xcol, pred, span=200):
    ys=[]
    for k in range(0,int(span*4)):
        y=top+k*0.25
        if pred(px[d2p(xcol,y)]):
            ys.append(y)
    if not ys: print("  %-12s 无"%name); return
    # 找第一段连续（允许 0.5 空隙）
    s=ys[0]; prev=ys[0]
    for y in ys[1:]:
        if y-prev>0.75: break
        prev=y
    print("  %-12s 左边缘列 x=%.2f 直线段 y %.2f..%.2f  -> r≈%.2f (框顶 %.1f)"
          %(name,xcol,s,prev,s-top,top))

print("面板（left 0 / top 0 / 边框 #E5E5E5）：")
edge_start("面板", 0, 0.25, lambda c: near(c,(229,229,229)))
print("搜索框（left 16 / top 70 / 边框 #E5E5E5）：")
edge_start("搜索框", 70, 16.25, lambda c: near(c,(229,229,229)))
print("选中行（left 16 / top 118 / 边框 #D3E2FF）：")
edge_start("选中行-边框", 118, 16.25, lambda c: near(c,(211,226,255)))
edge_start("选中行-蓝底", 118, 17.25, lambda c: near(c,(236,242,255)))
print("按钮（left 16 / top 432 / 蓝底 #3770F7）：")
edge_start("按钮", 432, 16.5, lambda c: c[2]>c[0]+60)
print("hover 行（left 16 / top 220 / 底 #F7F7F7，无描边）：")
edge_start("hover行", 220, 16.5, lambda c: near(c,(247,247,247),3))
