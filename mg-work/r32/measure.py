# -*- coding: utf-8 -*-
"""量取协作弹窗设计稿（mg-work/r32/design/coop.png，1440x900 1x）
文字输出的坐标即设计稿坐标（root 622:20081 就是 1440x900）。
"""
from PIL import Image
import sys

im = Image.open("mg-work/r32/design/coop.png").convert("RGB")
W, H = im.size
px = im.load()


def c(x, y):
    return px[x, y]


def same(a, b, tol=6):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))


def scan_row(y, x0, x1, step=1):
    """返回该行上颜色变化的分段 [(x_start, x_end, color)]"""
    out = []
    cur = c(x0, y)
    s = x0
    for x in range(x0 + 1, x1, step):
        v = c(x, y)
        if not same(v, cur, 4):
            out.append((s, x - 1, cur))
            cur = v
            s = x
    out.append((s, x1 - 1, cur))
    return out


def scan_col(x, y0, y1):
    out = []
    cur = c(x, y0)
    s = y0
    for y in range(y0 + 1, y1):
        v = c(x, y)
        if not same(v, cur, 4):
            out.append((s, y - 1, cur))
            cur = v
            s = y
    out.append((s, y1 - 1, cur))
    return out


def dark_bbox(x0, y0, x1, y1, thr=200):
    """区域内「墨色」（任一分量 < thr）像素的外接框"""
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = c(x, y)
            if min(r, g, b) < thr:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def colored_bbox(x0, y0, x1, y1, test):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if test(c(x, y)):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def is_blue(v):
    r, g, b = v
    return b > 150 and b - r > 40 and b - g > 20


def ink_density(x0, y0, x1, y1, thr=200):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if min(c(x, y)) < thr:
                n += 1
    return n


print("=" * 90)
print("① 遮罩与面板")
print("  遮罩取样 (10,450) =", c(10, 450), " (1430,880) =", c(1430, 880))
print("  面板1 水平扫描 y=400:", [s for s in scan_row(400, 40, 720) if s[1] - s[0] > 3][:8])
print("  面板1 垂直扫描 x=400:", [s for s in scan_col(400, 110, 800) if s[1] - s[0] > 3][:8])
print("  面板2 水平扫描 y=400:", [s for s in scan_row(400, 720, 1420) if s[1] - s[0] > 3][:8])

print("=" * 90)
print("② 标题「任务协作」+ 关闭")
print("  标题墨色框:", dark_bbox(70, 130, 300, 175))
b = dark_bbox(70, 130, 300, 175)
if b:
    print("  标题墨色高 =", b[3] - b[1] + 1, " 宽 =", b[2] - b[0] + 1, " 左缘相对面板 x =", b[0] - 60)
print("  关闭 X 墨色框:", dark_bbox(640, 130, 700, 175), "（相对面板 x =", None, ")")
x = dark_bbox(640, 130, 700, 175)
if x:
    print("      → 相对面板 left/top =", x[0] - 60, x[1] - 130, " size =", x[2] - x[0] + 1, x[3] - x[1] + 1)

print("=" * 90)
print("③ 步骤条（容器150 @面板(24,64) 592x32）")
print("  纵向扫描 x=150（面板1）:", scan_col(150, 185, 225))
print("  横向扫描 y=面板1(64+16=80)+130=210:", [s for s in scan_row(210, 70, 700) if s[1] - s[0] > 2])
print("  步骤1 文字墨色框:", dark_bbox(75, 195, 300, 225))
b1 = dark_bbox(75, 195, 300, 225)
if b1:
    print("     相对面板:", b1[0] - 60, b1[1] - 130, b1[2] - b1[0] + 1, b1[3] - b1[1] + 1)
print("  步骤2 文字墨色框:", dark_bbox(320, 195, 660, 225))
b2 = dark_bbox(320, 195, 660, 225)
if b2:
    print("     相对面板:", b2[0] - 60, b2[1] - 130, b2[2] - b2[0] + 1, b2[3] - b2[1] + 1)
# 右面板（步骤2 态）：步骤1 带对勾、灰底
print("  右面板 步骤条 横向扫描 y=210:", [s for s in scan_row(210, 750, 1380) if s[1] - s[0] > 2])

print("=" * 90)
print("④ divider（592x22，含文字）")
for y in range(240, 280):
    row = scan_row(y, 70, 700, 4)
    cols = set(s[2] for s in row)
    if len(cols) > 1:
        print("   y=%d 相对面板 y=%d 段数=%d 样例=%s" % (y, y - 130, len(row), row[:6]))
print("  divider 文字墨色框:", dark_bbox(150, 240, 620, 280))

print("=" * 90)
print("⑤ 列表容器（容器151 @面板(40,166) 560x270）")
print("  垂直扫描 x=120:", scan_col(120, 285, 570))
print("  水平扫描 y=300:", [s for s in scan_row(300, 80, 690) if s[1] - s[0] > 1][:6])
print("  表头底 矩形486 取色:", c(120, 300), c(300, 300))

print("=" * 90)
print("⑥ 行（pitch 34）：勾选框 / 文本")
for i in range(3):
    y0 = 300 + i * 34
    print("  行%d 带 y=%d ~ %d 墨色框:" % (i, y0, y0 + 34), dark_bbox(85, y0, 660, y0 + 34))
    print("     蓝色框:", colored_bbox(85, y0, 130, y0 + 34, is_blue))
print("  勾选框取色:", c(93, 316), c(96, 320))

print("=" * 90)
print("⑦ 底栏")
print("  已选文字墨色框:", dark_bbox(70, 560, 300, 620))
bt = dark_bbox(70, 560, 300, 620)
if bt:
    print("     相对面板:", bt[0] - 60, bt[1] - 130, bt[2] - bt[0] + 1, bt[3] - bt[1] + 1)
print("  按钮区蓝色框（panel1）:", colored_bbox(400, 700, 700, 760, is_blue))
print("  按钮区蓝色框（panel2）:", colored_bbox(1050, 700, 1400, 760, is_blue))
print("  取消按钮扫描 y=面板1(584+16)+130=730:", [s for s in scan_row(730, 480, 700) if s[1] - s[0] > 2])
print("  按钮文字 取消 墨色框:", dark_bbox(480, 715, 560, 750))
print("  底栏扫描（panel2）y=730:", [s for s in scan_row(730, 1150, 1390) if s[1] - s[0] > 2])
