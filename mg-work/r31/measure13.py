# -*- coding: utf-8 -*-
"""搜索框圆角：逐 y 找 #E5E5E5 边框最左 x（框左=16 上=70）"""
from PIL import Image
PNG="mg-work/r31/design/dispatch.png"; OX,OY,S=60,44,2.0
im=Image.open(PNG).convert("RGB"); px=im.load()
def d2p(x,y): return (int(round(OX+x*S)), int(round(OY+y*S)))
def near(c,t,tol=4): return all(abs(c[i]-t[i])<=tol for i in range(3))
print("搜索框上左角（框 left=16 top=70）：")
for dy in [0,0.5,1,1.5,2,2.5,3,3.5,4,5,6]:
    for xx in [i*0.25 for i in range(80,160)]:
        if near(px[d2p(xx,70+dy)],(229,229,229)):
            print("  dy=%-4s 最左 x=%.2f (内缩 %.2f)"%(dy,xx,xx-16)); break
    else: print("  dy=%-4s 无"%dy)
print("按钮上左角（按钮 left=16 top=432）：")
for dy in [0,0.5,1,1.5,2,2.5,3,3.5,4,5,6,7,8]:
    for xx in [i*0.25 for i in range(56,140)]:
        c=px[d2p(xx,432+dy)]
        if c[2]>c[0]+30:
            print("  dy=%-4s 最左 x=%.2f (内缩 %.2f)"%(dy,xx,xx-16)); break
    else: print("  dy=%-4s 无"%dy)
