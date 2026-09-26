from PIL import Image
im = Image.open('mg-work/r15/design.png').convert('RGB')
W,H = im.size
print('design size', W, H)

def col_scan(x, y0, y1, label):
    print('\n=== %s  x=%d  y=%d..%d ===' % (label, x, y0, y1))
    prev=None; start=y0
    segs=[]
    for y in range(y0,y1):
        c=im.getpixel((x,y))
        if c!=prev:
            if prev is not None:
                segs.append((start,y-1,prev))
            prev=c; start=y
    segs.append((start,y1-1,prev))
    for s,e,c in segs:
        if e-s+1>=1 and abs(c[0]-c[1])<6 and abs(c[1]-c[2])<6:
            print('  y %4d..%4d h=%3d  rgb%s' % (s,e,e-s+1,c))

col_scan(200, 40, 900, 'left column x=200')
