# -*- coding: utf-8 -*-
"""方法标定：滚动条节点代码明确 border-radius:6px（宽6 高128 @(310,118)）-> 测出方法偏差"""
from PIL import Image
PNG="mg-work/r31/design/dispatch.png"; OX,OY,S=60,44,2.0
im=Image.open(PNG).convert("RGB"); px=im.load()
def d2p(x,y): return (int(round(OX+x*S)), int(round(OY+y*S)))
def near(c,t,tol=8): return all(abs(c[i]-t[i])<=tol for i in range(3))
print("滚动条（r=6 已知；left 310 top 118 w6 h128 色 #D6D6D6）")
for xcol in [310.25, 311, 312.5]:
    ys=[]
    for k in range(0,140*4):
        y=118+k*0.25
        if near(px[d2p(xcol,y)],(214,214,214)): ys.append(y)
    if ys:
        s=ys[0]; prev=ys[0]
        for y in ys[1:]:
            if y-prev>0.75: break
            prev=y
        print("  左列 x=%.2f 直线段起 y=%.2f -> 偏移 %.2f"%(xcol,s,s-118))
# 上边缘行：最左/最右
for yrow in [118.25, 119, 120]:
    xs=[x for x in [i*0.25 for i in range(1220,1280)] if near(px[d2p(x,yrow)],(214,214,214))]
    if xs: print("  上行 y=%.2f x %.2f..%.2f (左内缩 %.2f)"%(yrow,min(xs),max(xs),min(xs)-310))
