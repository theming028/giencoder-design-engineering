# -*- coding: utf-8 -*-
"""对比设计稿 coop.png 与实测截图 coop-s1/s2.png
设计稿面板 @(60,130)，实测面板 @(400,130) → 实测相对坐标 = 绝对 - 400 / -130
"""
from PIL import Image

A = Image.open("mg-work/r32/design/coop.png").convert("RGB")
pa = A.load()
B = Image.open("mg-work/r32/shots/coop-s1.png").convert("RGB")
pb = B.load()
C = Image.open("mg-work/r32/shots/coop-s2.png").convert("RGB")
pc = C.load()
PAX, PAY = 60, 130
PBX, PBY = 400, 130


def d(x, y):
    """设计稿：相对面板坐标"""
    return pa[PAX + x, PAY + y]


def b(x, y):
    return pb[PBX + x, PBY + y]


def c(x, y):
    return pc[PBX + x, PBY + y]


print("=== 关键色（相对面板坐标）===")
pts = [(-30, 320, "遮罩"), (300, 400, "内容区底"), (280, 80, "步骤 active 底"),
       (380, 80, "步骤 wait 底"), (150, 40, "面板底(标题区)"), (190, 127, "divider 线"),
       (300, 320, "行底"), (24, 320, "内容区左边框"), (615, 320, "内容区右边框"),
       (4, 320, "面板左缘内")]
for x, y, tag in pts:
    print("  %-16s design=%-18s live=%s" % (tag, str(d(x, y)), str(b(x, y))))

print()
print("=== 步骤条：段1 右缘 / 段2 左缘（逐 y）===")
for y in (66, 70, 80, 90, 94):
    def edge(px, ox, oy, axis="R"):
        row = [(x, px[ox + x, oy + y]) for x in range(240, 400)]
        if axis == "R":
            cand = [x for x, v in row if not (abs(v[0] - v[1]) < 6 and abs(v[1] - v[2]) < 6 and v[0] > 235)]
            return cand[-1] if cand else None
        cand = [x for x, v in row if abs(v[0] - 242) < 8 and abs(v[1] - 242) < 8 and abs(v[2] - 242) < 8]
        return cand[0] if cand else None
    print("  y=%2d  段1右缘 design=%-4s live=%-4s | 段2左缘 design=%-4s live=%s"
          % (y, edge(pa, PAX, PAY, "R"), edge(pb, PBX, PBY, "R"),
             edge(pa, PAX, PAY, "L"), edge(pb, PBX, PBY, "L")))

print()
print("=== 步骤1 标题墨色盒（阈值 200）===")


def ink(px, ox, oy, x0, y0, x1, y1, thr=200):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if min(px[ox + x, oy + y]) < thr:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1) if xs else None


print("  step1 设计=", ink(pa, PAX, PAY, 100, 65, 300, 96, 200), " 实测=", ink(pb, PBX, PBY, 100, 65, 300, 96, 200))
print("  step2 设计=", ink(pa, PAX, PAY, 400, 65, 600, 96, 200), " 实测=", ink(pb, PBX, PBY, 400, 65, 600, 96, 200))
print("  标题 设计=", ink(pa, PAX, PAY, 10, 12, 200, 50, 200), " 实测=", ink(pb, PBX, PBY, 10, 12, 200, 50, 200))
print("  计数 设计=", ink(pa, PAX, PAY, 10, 585, 300, 620, 200), " 实测=", ink(pb, PBX, PBY, 10, 585, 300, 620, 200))
print("  divider文字 设计=", ink(pa, PAX, PAY, 100, 110, 500, 140, 190), " 实测=", ink(pb, PBX, PBY, 100, 110, 500, 140, 190))
print("  文件名行1 设计=", ink(pa, PAX, PAY, 40, 166, 300, 198, 200), " 实测=", ink(pb, PBX, PBY, 40, 166, 300, 198, 200))

print()
print("=== Step2（实测截图 coop-s2）===")
print("  搜索框图标 设计=", ink(pa, 740, PAY, 40, 166, 70, 198, 200), " 实测=", ink(pc, PBX, PBY, 40, 166, 70, 198, 200))
print("  占位文字   设计=", ink(pa, 740, PAY, 70, 166, 300, 198, 210), " 实测=", ink(pc, PBX, PBY, 70, 166, 300, 198, 210))
for i in range(3):
    y0 = 214 + i * 34
    print("  成员行%d 设计=%s 实测=%s" % (i + 1, ink(pa, 740, PAY, 40, y0, 300, y0 + 32, 235),
                                        ink(pc, PBX, PBY, 40, y0, 300, y0 + 32, 235)))
print("  底栏 左钮/中钮/右钮：")
for tag, (x0, x1) in [("取消", (400, 470)), ("上一步", (470, 555)), ("提交", (555, 620))]:
    print("    %-6s 设计=%s 实测=%s" % (tag, ink(pa, 740, PAY, x0, 580, x1, 620, 210),
                                       ink(pc, PBX, PBY, x0, 580, x1, 620, 210)))
