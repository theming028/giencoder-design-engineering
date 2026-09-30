# -*- coding: utf-8 -*-
"""量各卡片内**深色文字**的最左/最上边界（排除卡边缘抗锯齿干扰）。"""
from PIL import Image

im = Image.open('design-rgb.png').convert('RGB')
px = im.load()


def dark(p, th=170):
    return (p[0] + p[1] + p[2]) / 3 < th


CARDS = [
    ('上下文注入', 426, 576),
    ('深度思考', 660, 860),
    ('Bash', 1016, 1176),
    ('网页搜索', 1260, 1444),
    ('需求采访', 1528, 1736),
    ('更新任务清单', 1820, 2040),
    ('文件写入', 2124, 2368),
    ('SKILL', 2452, 2516),
    ('Tool call', 2600, 2732),
    ('重试', 2816, 2880),
    ('搜索资料', 3548, 3664),
    ('未知surface', 3876, 3960),
]
CL, CR = 183, 1005  # 卡片左右（含）

for name, y0, y1 in CARDS:
    p0, p1 = y0 + 1, y1 + 1
    # 从上往下找第一行有深色像素的（跳过卡边缘 2px）
    top = None
    for y in range(p0 + 2, p1 - 2):
        if any(dark(px[x, y]) for x in range(CL + 3, CR - 10)):
            top = y
            break
    # 最左深色像素
    left = None
    for x in range(CL + 2, CR - 10):
        if any(dark(px[x, y]) for y in range(p0 + 2, p1 - 2)):
            left = x
            break
    # 底部最后一行深色
    bot = None
    for y in range(p1 - 2, p0 + 2, -1):
        if any(dark(px[x, y]) for x in range(CL + 3, CR - 10)):
            bot = y
            break
    print('%-12s h=%-4d 文字top=+%-3s left=+%-3s padL=%-3s bot→底=%s'
          % (name, p1 - p0,
             (top - p0) if top else '?',
             (left - CL) if left else '?',
             (left - CL) if left else '?',
             (p1 - bot) if bot else '?'))
