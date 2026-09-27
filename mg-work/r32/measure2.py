# -*- coding: utf-8 -*-
"""量取 v2：连通域 bbox + 边缘逐像素（coop.png 1440x900 1x）"""
from PIL import Image

im = Image.open("mg-work/r32/design/coop.png").convert("RGB")
px = im.load()


def c(x, y):
    return px[x, y]


def bbox_of(pred, x0, y0, x1, y1):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(c(x, y)):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)


def eq(v):
    return lambda p: p == v


def line(y, x0, x1):
    out, cur, s = [], c(x0, y), x0
    for x in range(x0 + 1, x1):
        v = c(x, y)
        if v != cur:
            out.append("%d-%d%s" % (s, x - 1, cur))
            cur, s = v, x
    out.append("%d-%d%s" % (s, x1 - 1, cur))
    return " ".join(out)


P1 = (60, 130, 700, 770)     # 左面板
print("① 纯白卡 / 灰 hover / 主色浅底 的 bbox（左面板内）")
print("  #FFFFFF :", bbox_of(eq((255, 255, 255)), 61, 131, 699, 769))
print("  #F7F7F7 :", bbox_of(eq((247, 247, 247)), 61, 131, 699, 769))
print("  #ECF2FF :", bbox_of(eq((236, 242, 255)), 61, 131, 699, 769))
print("  #F2F2F2 :", bbox_of(eq((242, 242, 242)), 61, 131, 699, 769))
print("  #F9F9F9 :", bbox_of(eq((249, 249, 249)), 61, 131, 699, 769))

print()
print("② 列表卡边缘（y=400 细扫 78~110）：")
print("   ", line(400, 78, 112))
print("    y=320:", line(320, 78, 112))
print("    y=560:", line(560, 78, 112))
print("    右缘 y=400 656~700:", line(400, 654, 700))
print("③ 列表卡上下缘（x=90 纵向 270~300 / 550~600）：")
print("    280~300:", line(90, 280, 302) if False else " ".join("%d:%s" % (y, c(90, y)) for y in range(280, 302)))
print("    300~310:", " ".join("%d:%s" % (y, c(120, y)) for y in range(294, 306)))
print("    545~585:", " ".join("%d:%s" % (y, c(120, y)) for y in range(545, 585)))

print()
print("④ 步骤条（左面板）")
print("  #ECF2FF bbox:", bbox_of(eq((236, 242, 255)), 61, 131, 699, 300))
print("  #F2F2F2 bbox:", bbox_of(eq((242, 242, 242)), 61, 180, 699, 240))
print("  y=210 细扫 80~100:", line(210, 80, 100))
print("  y=210 细扫 370~400:", line(210, 370, 400))
print("  y=193..197 x=150:", " ".join("%d:%s" % (y, c(150, y)) for y in range(191, 200)))

print()
print("⑤ 右面板（步骤2 态）")
P2x = 740
print("  #ECF2FF bbox:", bbox_of(eq((236, 242, 255)), 741, 131, 1380, 300))
print("  步骤1 对勾：找蓝色像素 bbox:", bbox_of(lambda v: v[2] > 150 and v[2] - v[0] > 40, 750, 190, 900, 230))
print("  右面板 y=210 细扫 760~790:", line(210, 760, 790))
print("  右面板 y=210 细扫 1055~1080:", line(210, 1055, 1080))

print()
print("⑥ 右面板 搜索框 / 成员行")
print("  搜索框 y=235 纵向 x=800:", " ".join("%d:%s" % (y, c(800, y)) for y in range(210, 260)))
print("  成员行 pitch 扫描 x=880(头像列) 270~400:", " ".join("%d:%s" % (y, c(880, y)) for y in range(270, 400, 2)))

print()
print("⑦ 底栏按钮（左面板）")
print("  y=730 细扫 520~700:", line(730, 520, 660))
print("  y=730 细扫 640~700:", line(730, 640, 700))
print("  已选文字（左面板底部）:", bbox_of(lambda v: min(v) < 160, 80, 700, 400, 760))
print("  取消按钮框线 y=716..748 x=535:  ", " ".join("%d:%s" % (y, c(535, y)) for y in range(712, 752, 2)))

print()
print("⑧ 关闭 X")
print("  X bbox:", bbox_of(lambda v: min(v) < 200, 650, 140, 700, 180))
print("  标题 bbox:", bbox_of(lambda v: min(v) < 160, 70, 140, 300, 180))
