# -*- coding: utf-8 -*-
"""投影轮廓：从面板边缘向外测 alpha 衰减"""
from PIL import Image
PNG = "mg-work/r31/design/dispatch.png"
OX, OY, S = 60, 44, 2.0
im = Image.open(PNG).convert("RGBA"); px = im.load()
print("面板边缘外的 alpha（design 距离 -> alpha）：")
print(" 右侧：", [(d, px[int(OX + 640 + d * S), int(OY + 480)][3]) for d in [0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14]])
print(" 左侧：", [(d, px[int(OX - 1 - d * S), int(OY + 480)][3]) for d in [0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14]])
print(" 下侧：", [(d, px[int(OX + 320), int(OY + 960 + d * S)][3]) for d in [0.5, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18]])
print(" 上侧：", [(d, px[int(OX + 320), int(OY - 1 - d * S)][3]) for d in [0.5, 1, 2, 3, 4, 6, 8, 10, 12, 14]])
print("质量检查：(60+d,44+d) 角外 alpha:", [(d, px[OX - 1 - int(d*S), OY - 1 - int(d*S)][3]) for d in [1,2,4,6,8]])
