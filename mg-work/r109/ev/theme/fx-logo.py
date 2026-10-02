# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 设计并验证「暗色档 LOGO <img> CSS 反色」的滤镜参数。

约束：
  - <img src=data:image/svg+xml> 内部色值 **无法** 用 CSS 改（无 SVG 上下文）
  - 唯一手段 = 给 <img> 加 filter（作用于渲染后的像素）
目标：
  - #1E1E1E(30,30,30) → 白
  - #3D3D3D(61,61,61) → 白/近白（邵先生原话「黑灰部分改成白色」）
  - #D0D3D6(208,211,214) → 偏白（分隔线，可接受）
  - #3770F7(55,112,247) 品牌蓝 → 尽量保留色相
本脚本纯数值演算（CSS filter 规范公式），挑出最优组合。
"""
import sys


def clamp(v):
    return max(0.0, min(255.0, v))


def apply_invert(r, g, b, amt):
    return (r + (255 - 2 * r) * amt,
            g + (255 - 2 * g) * amt,
            b + (255 - 2 * b) * amt)


def apply_brightness(r, g, b, k):
    return (clamp(r * k), clamp(g * k), clamp(b * k))


def apply_saturate(r, g, b, s):
    """CSS saturate 矩阵（Rec.709 luma 权重）"""
    lr, lg, lb = 0.213, 0.715, 0.072
    l = lr * r + lg * g + lb * b
    return (clamp(l + s * (r - l)), clamp(l + s * (g - l)), clamp(l + s * (b - l)))


SAMPLES = {
    u'#1E1E1E 主体': (30, 30, 30),
    u'#3D3D3D 工作台': (61, 61, 61),
    u'#D0D3D6 分隔线': (208, 211, 214),
    u'#3770F7 品牌蓝': (55, 112, 247),
    u'#3770F7@20% 光晕': (215, 226, 252),
}


def run(spec, label):
    print(u'--- %s ---' % label)
    for name, (r, g, b) in SAMPLES.items():
        rr, gg, bb = float(r), float(g), float(b)
        for step in spec:
            op, k = step
            if op == u'invert':
                rr, gg, bb = apply_invert(rr, gg, bb, k)
            elif op == u'brightness':
                rr, gg, bb = apply_brightness(rr, gg, bb, k)
            elif op == u'saturate':
                rr, gg, bb = apply_saturate(rr, gg, bb, k)
        print(u'   %-18s (%3d,%3d,%3d) → (%3d,%3d,%3d)' % (
            name, r, g, b, round(rr), round(gg), round(bb)))
    print()


def main():
    run([], u'原图（无滤镜）')
    run([(u'invert', 1.0)], u'invert(1)')
    run([(u'invert', 1.0), (u'brightness', 1.35)], u'invert(1) brightness(1.35)')
    run([(u'invert', 1.0), (u'saturate', 1.6)], u'invert(1) saturate(1.6)')
    run([(u'invert', 0.92), (u'brightness', 1.1)], u'invert(.92) brightness(1.1)')
    run([(u'invert', 0.95), (u'brightness', 1.15), (u'saturate', 1.4)],
        u'invert(.95) brightness(1.15) saturate(1.4)')
    run([(u'invert', 0.88)], u'invert(.88)')
    run([(u'invert', 0.94), (u'saturate', 1.5)], u'invert(.94) saturate(1.5)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
