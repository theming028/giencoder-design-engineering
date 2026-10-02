# -*- coding: utf-8 -*-
import io, sys
from PIL import Image
def measure(p, thr=170):
    im = Image.open(p)
    print('== %s  mode=%s size=%s' % (p, im.mode, im.size))
    rgba = im.convert('RGBA')
    w, h = rgba.size
    px = rgba.load()
    x0, y0, x1, y1 = w, h, -1, -1
    n = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 20:  # transparent -> ignore
                continue
            lum = (r*299 + g*587 + b*114) // 1000
            # ink = anything darker than thr on an opaque pixel
            if lum < thr:
                n += 1
                if x < x0: x0 = x
                if y < y0: y0 = y
                if x > x1: x1 = x
                if y > y1: y1 = y
    if x1 < 0:
        print('   no ink'); return None
    bw, bh = x1-x0+1, y1-y0+1
    print('   ink bbox = (%d,%d)-(%d,%d)  w=%d h=%d  px=%d' % (x0, y0, x1, y1, bw, bh, n))
    print('   bbox center = (%.2f, %.2f) ; canvas center = (%.2f, %.2f)' % ((x0+x1)/2, (y0+y1)/2, w/2, h/2))
    print('   margins  L=%d R=%d T=%d B=%d' % (x0, w-1-x1, y0, h-1-y1))
    print('   aspect w/h = %.3f' % (bw/bh))
    return (x0, y0, x1, y1, bw, bh)
if __name__ == '__main__':
    for p in sys.argv[1:]:
        measure(p)
