# -*- coding: utf-8 -*-
"""第 31 轮设计稿精量 v6 —— 在已确认映射 design=(png-(60,44))/2 下输出全部真值"""
from PIL import Image
from collections import Counter

PNG = "mg-work/r31/design/dispatch.png"
OX, OY, S = 60, 44, 2.0
im = Image.open(PNG).convert("RGB")
W, H = im.size
px = im.load()


def d2p(x, y):
    return (int(round(OX + x * S)), int(round(OY + y * S)))


def p2d(x, y):
    return ((x - OX) / S, (y - OY) / S)


def hexs(c):
    return "#%02X%02X%02X" % c


def box_design(x0, y0, x1, y1):
    """设计坐标矩形内扫描，返回找到的像素集合的 bbox（设计坐标）"""
    px0, py0 = d2p(x0, y0)
    px1, py1 = d2p(x1, y1)
    return px0, py0, px1, py1


def scan(pred, x0, y0, x1, y1, label):
    a, b, c, d = box_design(x0, y0, x1, y1)
    xs, ys = [], []
    for y in range(max(0, b), min(H, d)):
        for x in range(max(0, a), min(W, c)):
            if pred(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        print("  %-14s 无匹配" % label)
        return None
    r = (p2d(min(xs), min(ys)), p2d(max(xs) + 1, max(ys) + 1))
    print("  %-14s x %.1f..%.1f (w %.1f)   y %.1f..%.1f (h %.1f)"
          % (label, r[0][0], r[1][0], r[1][0] - r[0][0], r[0][1], r[1][1], r[1][1] - r[0][1]))
    return r


def lum(c):
    return (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000


print("=" * 74)
print("A. 调色板 TOP20（面板内部区域）")
cnt = Counter()
for y in range(OY + 2, OY + 958):
    for x in range(OX + 2, OX + 638):
        cnt[px[x, y]] += 1
for c, n in cnt.most_common(20):
    print("   %s  %-6d  lum %.0f" % (hexs(c), n, lum(c)))

print("=" * 74)
print("B. 标题区（容器 145: left16 top16 228x42）")
print("  标题「将任务转派给：」")
scan(lambda c: lum(c) < 120, 14, 14, 200, 40, "title ink")
print("  副标题「转派仅变更…」")
scan(lambda c: lum(c) < 180, 14, 40, 260, 60, "subtitle ink")

print("=" * 74)
print("C. 搜索框（组 10280: left16 top70 288x32）")
scan(lambda c: 200 < lum(c) < 245, 12, 66, 308, 106, "边框/内容")
scan(lambda c: lum(c) < 150, 20, 74, 48, 100, "放大镜 ink")
scan(lambda c: lum(c) < 190, 48, 74, 200, 100, "占位 ink")

print("=" * 74)
print("D. 选中行（容器 144: left16 top118 288x32）—— 蓝色底")
scan(lambda c: c[2] > c[0] + 8 and c[2] > 235, 14, 114, 306, 154, "蓝底 bbox")
print("  蓝底内部采样:", [
    hexs(px[d2p(150, 134)[0] + i, d2p(150, 134)[1]]) for i in range(0, 5)])
print("  边框色采样(左边缘扫描):")
py = d2p(150, 134)[1]
for x in range(d2p(14, 0)[0], d2p(22, 0)[0]):
    print("     png x=%d (%s) -> design x=%.1f  %s" % (x, "", p2d(x, py)[0], hexs(px[x, py])))

print("=" * 74)
print("E. hover 行（顾帆，第 4 行）—— 灰色底")
scan(lambda c: 243 <= c[0] <= 250 and c[0] == c[1] == c[2], 14, 216, 306, 258, "灰底 bbox")

print("=" * 74)
print("F. 7 个头像（20x20，圆心在行内 x8..28）")
rows = [("邵禹铭", 118), ("秦怡", 152), ("韩佳毅", 186), ("顾帆", 220),
        ("姜嘉怡", 254), ("朱甜", 288), ("齐瑞辰", 322)]
for name, top in rows:
    cy = top + 16
    cx = 16 + 8 + 10
    c = px[d2p(cx, cy)[0], d2p(cx, cy)[1]]
    # 头像环几何：非背景色像素
    r = scan(lambda p: not (p[0] > 250 and p[1] > 250 and p[2] > 250), 20, top, 48, top + 32, name)
    print("     ↑ 环色 %s" % hexs(c))

print("=" * 74)
print("G. 分隔线 / 按钮（容器 146: left16 top416 288x48）")
for y in range(400, 425):
    a = d2p(200, y)[1]
    c = px[OX + 400, a]
    if not (c[0] > 250 and c[1] > 250 and c[2] > 250):
        print("   y=%.1f 色 %s" % (y, hexs(c)))
scan(lambda c: c[2] > c[0] + 30, 12, 424, 308, 470, "按钮蓝块")
scan(lambda c: lum(c) > 230 and c[2] > 230, 100, 436, 220, 462, "按钮白字")

print("=" * 74)
print("H. 滚动条（矩形 480: left310 top118 6x128）")
scan(lambda c: 200 <= c[0] <= 240 and c[0] == c[1] == c[2], 306, 114, 320, 260, "滑块")
print("  滑块色采样:", hexs(px[d2p(313, 180)[0], d2p(313, 180)[1]]))
