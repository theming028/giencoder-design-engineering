# -*- coding: utf-8 -*-
from PIL import Image
im = Image.open('mg-work/r93/raw/design-rgb.png').convert('RGB')
px = im.load()
X0, Y0, X1, Y1 = 950, 218, 976, 238
print('     ' + ''.join('%4d' % x for x in range(X0, X1)))
for y in range(Y0, Y1):
    print('%4d ' % y + ''.join('%4d' % ((px[x,y][0]*299+px[x,y][1]*587+px[x,y][2]*114)//1000) for x in range(X0, X1)))
# ink = lum < 235
pts = []
for y in range(Y0, Y1):
    for x in range(X0, X1):
        lum = (px[x,y][0]*299+px[x,y][1]*587+px[x,y][2]*114)//1000
        if lum < 235:
            pts.append((x, y, lum))
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
print()
print('ink count', len(pts), 'bbox x %d..%d (w=%d)  y %d..%d (h=%d)' % (min(xs), max(xs), max(xs)-min(xs)+1, min(ys), max(ys), max(ys)-min(ys)+1))
