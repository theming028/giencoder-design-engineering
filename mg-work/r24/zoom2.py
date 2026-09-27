# -*- coding: utf-8 -*-
from PIL import Image
P = (r"C:\Users\Administrator\.mgmcp\resources\screenshots"
     r"\193158744355579\622-13950\详情页-1_622-13950.png")
im = Image.open(P).convert("RGB")
# 侧栏整体（css x680..944, y48..760）
c = im.crop((1360, 96, 1888, 1520))
c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
c.save("mg-work/r24/z-side.png"); print("z-side", c.size)
# 任务属性区放大
c = im.crop((1360, 110, 1888, 800))
c = c.resize((int(c.width * 2.4), int(c.height * 2.4)), Image.LANCZOS)
c.save("mg-work/r24/z-attr.png"); print("z-attr", c.size)
# 描述区 list
c = im.crop((90, 540, 900, 760))
c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
c.save("mg-work/r24/z-list.png"); print("z-list", c.size)
