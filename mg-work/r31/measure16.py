# -*- coding: utf-8 -*-
"""面板圆角复核：沿顶部边框行打印 RGBA（区分「描边」与「投影」——投影 alpha<255）"""
from PIL import Image
PNG="mg-work/r31/design/dispatch.png"; OX,OY,S=60,44,2.0
im=Image.open(PNG).convert("RGBA"); px=im.load()
def d2p(x,y): return (int(round(OX+x*S)), int(round(OY+y*S)))
print("沿 design y=0.25（面板顶端边框行）逐 x 的 RGBA：")
for x in [0,1,2,3,4,5,6,7,8,9,10,12,16,160]:
    c=px[d2p(x,0.25)]
    print("  x=%-4s %s  alpha=%d" % (x, "#%02X%02X%02X"%c[:3], c[3]))
print("沿 design x=0.25（面板左端边框列）逐 y 的 RGBA：")
for y in [0,1,2,3,4,5,6,7,8,9,10,12,16,240]:
    c=px[d2p(0.25,y)]
    print("  y=%-4s %s  alpha=%d" % (y, "#%02X%02X%02X"%c[:3], c[3]))
print("对照：搜索框顶部边框行 design y=70.25 的 RGBA（无投影干扰）")
for x in [16,17,18,19,20,21,22,23,24,26,30,152]:
    c=px[d2p(x,70.25)]
    print("  x=%-4s %s  alpha=%d" % (x, "#%02X%02X%02X"%c[:3], c[3]))
