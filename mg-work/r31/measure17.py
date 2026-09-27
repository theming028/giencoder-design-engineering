# -*- coding: utf-8 -*-
"""圆角终测 v2：覆盖率 0.5 亚像素交点法（顶边行）
原理：圆角矩形顶边行的直线段起点 = r。用「背景色→前景色」的线性插值求覆盖率，
      取覆盖率 0.5 的亚像素 x 作为圆弧外缘 -> r = x - 元素左缘。
"""
from PIL import Image
PNG="mg-work/r31/design/dispatch.png"; OX,OY,S=60,44,2.0
im=Image.open(PNG).convert("RGB"); px=im.load()
def d2p(x,y): return (int(round(OX+x*S)), int(round(OY+y*S)))
def chan(c,i): return c[i]

def cross(yrow, left, back, fore, ch, span=40):
    """在 yrow 行、从 left 往右扫，求前景覆盖率 0.5 的 x（亚像素）"""
    lo, hi = back[ch], fore[ch]
    rng = hi - lo
    prev = None
    for k in range(0, int(span*8)):
        x = left - 2 + k*0.125
        c = px[d2p(x, yrow)]
        cov = (c[ch] - lo) / rng
        if prev is not None and prev[1] < 0.5 <= cov:
            # 线性插值
            t = (0.5 - prev[1]) / (cov - prev[1])
            return prev[0] + t*0.125
        prev = (x, cov)
    return None

print("=" * 70)
print("顶边行覆盖率 0.5 交点 -> r = 交点 x - 元素左缘")
cases = [
    ("面板   ", 0.25,  0,  (255,255,255),(229,229,229), 0, 40),
    ("搜索框 ", 70.25, 16, (255,255,255),(229,229,229), 0, 20),
    ("选中行 ", 118.25,16, (255,255,255),(211,226,255), 1, 20),
    ("按钮   ", 432.25,16, (255,255,255),(55,112,247),  1, 20),
]
for name, yrow, left, back, fore, ch, span in cases:
    x = cross(yrow, left, back, fore, ch, span)
    print("  %s y=%-7s 覆盖率0.5 交点 x=%s  -> r≈%s" % (
        name, yrow, ("%.3f"%x) if x is not None else "无",
        ("%.2f"%(x-left)) if x is not None else "-"))

print("=" * 70)
print("对照：面板底部行（应同样得 r）")
for yrow in [479.75, 479.5]:
    x = cross(yrow, 0, (255,255,255),(229,229,229), 0, 40)
    print("  y=%-7s r≈%s" % (yrow, ("%.2f"%x) if x is not None else "无"))
print("对照：搜索框底部行")
for yrow in [101.75, 101.5]:
    x = cross(yrow, 16, (255,255,255),(229,229,229), 0, 20)
    print("  y=%-7s r≈%s" % (yrow, ("%.2f"%(x-16)) if x is not None else "无"))
