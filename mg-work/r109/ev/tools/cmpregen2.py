# -*- coding: utf-8 -*-
"""③ 重新生成图标：设计真值 vs 真机渲染 —— 并排放大对照。
   设计真值 = raw/design-rgb.png 的 14px 盒（OX,OY = 956,221）
   真机渲染 = raw/g-regen-btn.png（24×24 元素截图，图标在 (5,5) 的 14×14 里）"""
import sys
from PIL import Image

RAW = r'E:/GienCoder/giencoder-design-engineering/mg-work/r109/raw'
DES = r'E:/GienCoder/giencoder-design-engineering/mg-work/r93/raw/design-rgb.png'
Z = 16

d = Image.open(DES).convert('RGB')
design = d.crop((956, 221, 970, 235))
r = Image.open(RAW + '/g-regen-btn.png').convert('RGB')
print('真机截图尺寸 =', r.size)
real = r.crop((5, 5, 19, 19))

def ink(img, th=140):
    """墨迹盒（按亮度阈值）"""
    px = img.load()
    xs, ys = [], []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if sum(px[x, y]) / 3 < th:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))

def darkest(img):
    px = img.load()
    return min(sum(px[x, y]) / 3 for y in range(img.size[1]) for x in range(img.size[0]))

print('设计墨迹盒 =', ink(design), ' 真机墨迹盒 =', ink(real))
dmin, rmin = darkest(design), darkest(real)
print('设计最深 = %.0f（覆盖率 1.0）  真机最深 = %.0f（覆盖率 1.0）' % (dmin, rmin))

w, h = 14 * Z, 14 * Z
canvas = Image.new('RGB', (w * 2 + 24, h + 34), (255, 255, 255))
canvas.paste(design.resize((w, h), Image.NEAREST), (0, 30))
canvas.paste(real.resize((w, h), Image.NEAREST), (w + 24, 30))
canvas.save(RAW + '/cmp-regen-l2.png')
print('写出', RAW + '/cmp-regen-l2.png', canvas.size)

# 逐像素差（两边各按**自身最深像素**归一到覆盖率，比较 |Δ|）
left = design.convert('L'); right = real.convert('L')
lp, rp = left.load(), right.load()
rows, worst = [], []
for y in range(14):
    row = []
    for x in range(14):
        a = max(0.0, (255 - lp[x, y]) / (255 - dmin))
        b = max(0.0, (255 - rp[x, y]) / (255 - rmin))
        row.append(b - a)
        if abs(b - a) >= 0.33:
            worst.append((x, y, round(b - a, 2)))
    rows.append(row)
bad = len(worst)
tot = sum(sum(v * v for v in row) for row in rows) ** 0.5
print('平方和 err = %.3f  坏格数(|Δ|>=0.33) = %d' % (tot, bad))
for w_ in worst:
    print('   坏格', w_)
print()
print('每行 (设计→真机, 正=真机更深):')
for y in range(14):
    print(' y%-2d ' % y + ' '.join(('%+.2f' % v) for v in rows[y]))
