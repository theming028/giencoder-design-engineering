# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
OUT = "mg-work/r53/ev"; SH = "mg-work/r53/shots"
os.makedirs(OUT, exist_ok=True)
def F(sz): return ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", sz)
FA, FB, FS = F(21), F(25), F(17)
INK=(24,36,58); HDBG=(226,236,250); OKB=(214,240,214); BADB=(252,224,224)
def load(p):
    im=Image.open(p)
    if im.mode!="RGB":
        bg=Image.new("RGB",im.size,(255,255,255)); bg.paste(im.convert("RGBA"),(0,0),im.convert("RGBA")); return bg
    return im
def cs(img,box,sc=1):
    c=img.crop(tuple(box)); return c.resize((int(c.width*sc),int(c.height*sc)), Image.NEAREST) if sc!=1 else c
def bar(w,text,bg=HDBG,fg=INK,f=FA,h=40):
    w=max(w,int(f.getlength(text))+30)
    im=Image.new("RGB",(w,h),bg); ImageDraw.Draw(im).text((14,h//2),text,font=f,fill=fg,anchor="lm"); return im
def stack(parts,gap=8,pad=18,bg=(255,255,255)):
    W=max(p.width for p in parts); H=sum(p.height for p in parts)+gap*(len(parts)-1)
    out=Image.new("RGB",(W+pad*2,H+pad*2),bg); y=pad
    for p in parts: out.paste(p,(pad,y)); y+=p.height+gap
    return out
def side(l,r,gap=16,pad=18,bg=(255,255,255)):
    H=max(l.height,r.height)
    out=Image.new("RGB",(l.width+gap+r.width+pad*2,H+pad*2),bg)
    out.paste(l,(pad,pad)); out.paste(r,(pad+l.width+gap,pad)); return out
def paircols(cols,gap=16,pad=18,bg=(255,255,255)):
    W=sum(c.width for c in cols)+gap*(len(cols)-1); H=max(c.height for c in cols)
    out=Image.new("RGB",(W+pad*2,H+pad*2),bg); x=pad
    for c in cols: out.paste(c,(x,pad)); x+=c.width+gap
    return out

A=lambda n: load(f"{SH}/a-{n}.png"); B=lambda n: load(f"{SH}/b-{n}.png")

# ===== EV1 微动效 =====
crop=[470,48,1080,300]
f_a0=cs(A("anim-000"),crop); f_a9=cs(A("anim-090"),crop); f_a26=cs(A("anim-260"),crop); f_b=cs(B("anim-090"),crop)
W=max(f_a0.width,f_b.width)
p=stack([bar(W,"① 改动前 · 点「打开侧栏」瞬间（t=0ms 与 t=90ms 完全相同：无过渡，整栏硬切出现）",bg=BADB),
         f_b,
         bar(W,"② 改动后 · t=0ms：外框 clip 抹开 40px + 内容右移 24px + 透明度 0（整栏尚未显形）"),
         f_a0,
         bar(W,"③ 改动后 · t=90ms：抹开剩余 6.6px、内容位移 4.0px、透明度 0.835（正在滑入）",bg=OKB),
         f_a9,
         bar(W,"④ 改动后 · t=260ms：抹开归零、位移归零、透明度 1（落定）",bg=OKB),
         f_a26], gap=6)
p.save(f"{OUT}/ev1-browse-motion.png"); print("ev1", p.size)

# ===== EV2 描述区底部渐隐 =====
c=[40,462,660,600]
p=stack([bar(620,"① 改动前 · .td-desc-body 折叠态底部：文字在 374px 处硬切（实测 scrollH 845 > clientH 374）",bg=BADB),
         cs(B("normal"),c),
         bar(620,"② 改动后 · mask 渐隐 56px（展开全文后自动归零，随 max-height 同曲线过渡）",bg=OKB),
         cs(A("normal"),c)], gap=6)
p.save(f"{OUT}/ev2-desc-fade.png"); print("ev2", p.size)

# ===== EV3 三处尺寸/圆角 =====
def trio(pre):
    return [cs(load(f"{SH}/{pre}-normal.png"),[758,150,804,190],10),
            cs(load(f"{SH}/{pre}-normal.png"),[848,46,938,100],8),
            cs(load(f"{SH}/{pre}-browse.png"),[496,201,702,253],6)]
tb,tri_b = trio("b")[0], trio("b"); ta,tri_a = trio("a")[0], trio("a")
p=stack([bar(760,"① 状态点 .giencoder-badge-status-dot（×10）",h=36,f=FS), side(tri_b[0],tri_a[0]),
         bar(760,"② 顶栏导航 .td-bar-nav svg（×8）—— 左：改动前 16px　右：改动后 14px",h=36,f=FS), side(tri_b[1],tri_a[1]),
         bar(760,"③ 文件目录 .td-bf 行底色（×6，注入等效 hover 底色取证）—— 左：直角　右：4px 圆角",h=36,f=FS), side(tri_b[2],tri_a[2]),
        ], gap=8)
p.save(f"{OUT}/ev3-sizes-radius.png"); print("ev3", p.size)

# ===== EV4 下拉右对齐 =====
c=[1028,146,1302,358]
sb=cs(B("modal-select"),c); sa=cs(A("modal-select"),c)
p=stack([bar(sb.width,"① 改动前 · 弹层 left:0（与触发器左对齐）→ 右缘冲出字段 9px",bg=BADB,h=36,f=FS), sb,
         bar(sb.width,"② 改动后 · .kb-crt-fld > .giencoder-select-popup { right: 0 } → 右缘差 0px",bg=OKB,h=36,f=FS), sa], gap=6)
p.save(f"{OUT}/ev4-select-align.png"); print("ev4", p.size)

# ===== EV5 日期弹层 =====
c=[982,364,1302,708]
db=cs(B("modal-date"),c,2); da=cs(A("modal-date"),c,2)
p=stack([bar(db.width,"① 改动前 · 只有「预想完成」的日期弹层：padding/radius 均 0，日历塌成一行文本（×2）",bg=BADB,h=36,f=FS), db,
         bar(db.width,"② 改动后 · 补齐 DatePicker 面板 + 日历 CSS（DS 源 ui-controls.css）×2",bg=OKB,h=36,f=FS), da], gap=6)
p.save(f"{OUT}/ev5-datepicker.png"); print("ev5", p.size)

# ===== EV6 间距逐像素取证 =====
z=cs(load(f"{SH}/_gap-zoom8.png"),[0,0,336,320],1)
tab=Image.new("RGB",(560,320),(255,255,255)); d=ImageDraw.Draw(tab)
rows=[("x = 943","rgb(218,227,237)","左栏 1px 描边 #DAE3ED"),
      ("x = 944–951","rgb(229,237,245)","8px 包围底色 --td-surround"),
      ("x = 952","rgb(218,227,237)","右栏 1px 描边 #DAE3ED"),
      ("x ≥ 953","rgb(255,255,255)","右栏内容")]
d.text((14,14),"第 4 项取证 · 1440 视口 y=400 逐像素取色",font=F(19),fill=INK)
y=52
for a,b_,c2 in rows:
    d.text((14,y),a,font=F(17),fill=INK); d.text((120,y),b_,font=F(17),fill=(70,90,120)); d.text((270,y),c2,font=F(17),fill=(70,90,120)); y+=34
d.text((14,y+8),"结论：盒到盒 = 944→952 恰为 8px，与设计稿口径一致，无需改动。",font=F(17),fill=(0,110,60))
p=stack([bar(max(z.width,tab.width),"① 交接缝 ×8 放大（白 │ 描边 │ 8px 底 │ 描边 │ 白）"), side(z,tab,gap=16)], gap=6)
p.save(f"{OUT}/ev6-gap-pixel.png"); print("ev6", p.size)
