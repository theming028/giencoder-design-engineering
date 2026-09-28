# -*- coding: utf-8 -*-
from PIL import Image, ImageChops, ImageDraw, ImageFont
import os
OUT="mg-work/r52/ev"; os.makedirs(OUT, exist_ok=True)
S=os.path.expanduser("~/.mgmcp/resources/screenshots/193158744355579/836-26404")

def F(sz):
    return ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", sz)
FA=F(21); FB=F(25); FS=F(17)

INK=(24,36,58); HDBG=(226,236,250); OKB=(214,240,214); BADB=(252,224,224)
def load(p):
    im=Image.open(p)
    if im.mode!="RGB":
        bg=Image.new("RGB",im.size,(255,255,255)); bg.paste(im.convert("RGBA"),(0,0),im.convert("RGBA")); return bg
    return im
def cs(img,box,sc):
    c=img.crop(box); return c.resize((int(c.width*sc),int(c.height*sc)), Image.NEAREST)
def bar(w,text,bg=HDBG,fg=INK,f=FA,h=40):
    need=int(f.getlength(text))+30
    w=max(w,need)
    im=Image.new("RGB",(w,h),bg); ImageDraw.Draw(im).text((14,h//2),text,font=f,fill=fg,anchor="lm"); return im
def stack(parts,gap=6,pad=18,bg=(255,255,255)):
    W=max(p.width for p in parts); H=sum(p.height for p in parts)+gap*(len(parts)-1)
    out=Image.new("RGB",(W+pad*2,H+pad*2),bg); y=pad
    for p in parts: out.paste(p,(pad,y)); y+=p.height+gap
    return out
def side(l,r,gap=14,pad=18,bg=(255,255,255)):
    H=max(l.height,r.height)
    out=Image.new("RGB",(l.width+gap+r.width+pad*2,H+pad*2),bg)
    out.paste(l,(pad,pad)); out.paste(r,(pad+l.width+gap,pad)); return out

normal=load("mg-work/r52/shots/normal.png")
browse=load("mg-work/r52/shots/browse.png")
wfix=load("mg-work/r52/shots/w300-fixed.png")
wcf =load("mg-work/r52/shots/w300-cf.png")

# ================= EV1 元信息区：设计稿 vs 实现 =================
des = cs(load(os.path.join(S,"组-10471_836-28473.png")), (0,108,558,342), 1)   # 已是 3x，直接裁
imp = cs(normal, (973,221,1159,299), 3)                                        # 1x -> 3x
W=max(des.width, imp.width)
p=stack([bar(W,"①  设计稿 · 节点 836:28473（3× 设备像素，逻辑 186×78）"),
         des,
         bar(W,"②  实现 · task-detail.html  .td-ai-meta / .td-ai-rule / .td-ai-ctx（同尺寸 3× 放大）"),
         imp], gap=8)
p.save(f"{OUT}/ev1-meta-compare.png"); print("ev1", p.size)

# ================= EV2 面板描边 =================
a=cs(normal,(944,40,1052,148),4)      # 右栏左上角
b=cs(browse,(478,40,586,148),4)       # 浏览态右栏↔预览栏接缝
c=cs(browse,(1382,44,1436,98),7)      # 预览栏右上（关闭按钮周边）
lbl=lambda w,t:bar(w,t,h=36,f=FS)
W=max(a.width,b.width,c.width)
p=stack([lbl(W,"① 普通态：左/右栏均为 1px #DAE3ED 描边（无投影）· 右栏左上角 ×4"),
         a,
         lbl(W,"② 浏览态：AI 栏↔文件预览栏接缝 ×4（右栏右缘 0 / 预览栏左缘 1px #E5E5E5）"),
         b,
         lbl(W,"③ 预览栏右上角圆角 ×7"),
         c], gap=8)
p.save(f"{OUT}/ev2-panel-border.png"); print("ev2", p.size)

# ================= EV3 预览栏按钮 =================
full=cs(browse,(480,42,1440,100),2)
az=cs(browse,(570,48,616,90),8)       # 加号
cz=cs(browse,(1378,48,1424,90),8)     # 关闭
W=max(full.width,az.width+cz.width+14)
p=stack([bar(W,"④ 打开侧栏 · 顶栏整行 ×2（.td-browse-tab │ .td-browse-add … .td-browse-acts）"),
         full,
         side(az,cz,gap=14,pad=0,bg=(255,255,255)),
         bar(W,"   .td-browse-add（加号）容器 28px / 图标 16px          .td-browse-ico（关闭）容器 28px / 图标 16px",h=34,f=FS),
        ], gap=8)
p.save(f"{OUT}/ev3-browsebar.png"); print("ev3", p.size)

# ================= EV4 窄宽文字截断 =================
z1=cs(normal,(960,738,1420,880),2)
z2=cs(load("mg-work/r52/shots/w300-closed.png"),(960,738,1420,880),2)
W=max(z1.width,z2.width)
p=stack([bar(W,"⑤ AI 对话框宽度不足时：模型选择器文字自动省略（对话框 438px 常规态）"),
         z1,
         bar(W,"   对话框压到 300px（模拟横向空间不足）→ 文字截断为 DeepSeek-V4-Pr…，气泡不越界",f=FS,h=34),
         z2], gap=8)
p.save(f"{OUT}/ev4-narrow-ellipsis.png"); print("ev4", p.size)

# ================= EV5 弹层右对齐 =================
f1=cs(wfix,(950,640,1340,880),2)
f2=cs(wcf ,(950,640,1340,880),2)
W=max(f1.width,f2.width)
p=stack([bar(W,"⑥ 弹层右对齐（第 11 项）：对话框 300px 时点开大模型下拉",bg=OKB),
         f1,
         bar(W,"   反事实：若恢复 DS 默认 left:0 —— 弹层右缘冲出白框 18px",bg=BADB),
         f2], gap=8)
p.save(f"{OUT}/ev5-popup-align.png"); print("ev5", p.size)
