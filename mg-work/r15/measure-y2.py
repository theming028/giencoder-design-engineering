from PIL import Image
im = Image.open('mg-work/r15/design.png').convert('RGB')

def col_scan(x, y0, y1, label):
    print('\n=== %s  x=%d ===' % (label, x))
    prev=None; start=y0; segs=[]
    for y in range(y0,y1):
        c=im.getpixel((x,y))
        if c!=prev:
            if prev is not None: segs.append((start,y-1,prev))
            prev=c; start=y
    segs.append((start,y1-1,prev))
    for s,e,c in segs:
        if e-s+1>=1: print('  y %4d..%4d h=%3d  rgb%s' % (s,e,e-s+1,c))

col_scan(130, 540, 700, 'attach area (x=130)')
col_scan(1200, 40, 700, 'right column (x=1200)')
