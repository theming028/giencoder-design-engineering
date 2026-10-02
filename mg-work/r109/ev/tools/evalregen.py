# -*- coding: utf-8 -*-
import io, math, sys
sys.path.insert(0, 'mg-work/r109/ev/tools')
import importlib.util
spec = importlib.util.spec_from_file_location('fr', 'mg-work/r109/ev/tools/fitregen.py')
fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr) if False else None
# fitregen's __main__ runs on import; instead re-implement the tiny bits we need
from PIL import Image
W = H = 14; SS = 8; INK = 134.0
im = Image.open('mg-work/r93/raw/design-rgb.png').convert('RGB'); px = im.load()
T = [[max(0.0, min(1.0, (255.0-((px[956+x,221+y][0]*299+px[956+x,221+y][1]*587+px[956+x,221+y][2]*114)//1000))/(255.0-INK))) for x in range(W)] for y in range(H)]
PTS = [(x+(i+0.5)/SS, y+(j+0.5)/SS) for y in range(H) for x in range(W) for j in range(SS) for i in range(SS)]
def cov(pred):
    m=[[0]*W for _ in range(H)]
    for (sx,sy) in PTS:
        if pred(sx,sy):
            m[int(sy)][int(sx)] += 1
    return [[m[y][x]/(SS*SS) for x in range(W)] for y in range(H)]
def arc_pred(cx,cy,r,t0,t1,w):
    half=w/2.0
    def f(x,y):
        dx,dy=x-cx,y-cy; d=math.hypot(dx,dy)
        if abs(d-r)>half: return False
        ad=math.degrees(math.atan2(dy,dx))
        for k in (-1,0,1):
            if min(t0,t1) <= ad+k*360 <= max(t0,t1): return True
        return False
    return f
def tri_pred(p,q,r_):
    def sgn(a,b,c): return (a[0]-c[0])*(b[1]-c[1])-(b[0]-c[0])*(a[1]-c[1])
    def f(x,y):
        pt=(x,y); d1=sgn(pt,p,q); d2=sgn(pt,q,r_); d3=sgn(pt,r_,p)
        return not (((d1<0)or(d2<0)or(d3<0)) and ((d1>0)or(d2>0)or(d3>0)))
    return f
def render(arc, tri):
    ma=cov(arc_pred(*arc)); mt=cov(tri_pred(tri[0:2],tri[2:4],tri[4:6]))
    return [[max(ma[y][x],mt[y][x]) for x in range(W)] for y in range(H)]
def err(m):
    return sum((m[y][x]-T[y][x])**2 for y in range(H) for x in range(W))
def show(m,t=''):
    ch=' .:-=+*#%@'
    print('--',t)
    for y in range(H): print('%3d %s'%(y,''.join(ch[min(9,int(m[y][x]*10))] for x in range(W))))
def arcp(cx,cy,r,t0,t1):
    x0=cx+r*math.cos(math.radians(t0)); y0=cy+r*math.sin(math.radians(t0))
    x1=cx+r*math.cos(math.radians(t1)); y1=cy+r*math.sin(math.radians(t1))
    print('  path: M%.2f %.2f A%.2f %.2f 0 0 %.2f %.2f'%(x0,y0,r,r,x1,y1))
def arrow_from(cx, cy, r, t1, hw, L):
    """proper arrowhead at the arc end: base perpendicular to tangent, tip along tangent"""
    th = math.radians(t1)
    E = (cx + r*math.cos(th), cy + r*math.sin(th))
    d = (math.sin(th), -math.cos(th))       # travel direction for decreasing angle
    p = (d[1], -d[0])                        # perpendicular
    b1 = (E[0] + hw*p[0], E[1] + hw*p[1])
    b2 = (E[0] - hw*p[0], E[1] - hw*p[1])
    tip = (E[0] + L*d[0], E[1] + L*d[1])
    return (tip[0], tip[1], b1[0], b1[1], b2[0], b2[1])

def render2(cx, cy, r, t1, hw, L, w=1.3):
    arc = (cx, cy, r, 0, t1, w)
    tri = arrow_from(cx, cy, r, t1, hw, L)
    ma = cov(arc_pred(*arc)); mt = cov(tri_pred(tri[0:2], tri[2:4], tri[4:6]))
    m = [[max(ma[y][x], mt[y][x]) for x in range(W)] for y in range(H)]
    return m, arc, tri

def render3(cx, cy, r, t0, t1, hw, L, w=1.3, tri_da=0.0):
    ma = cov(arc_pred(cx, cy, r, t0, t1, w))
    th = math.radians(t1 + tri_da)
    E = (cx + r*math.cos(th), cy + r*math.sin(th))
    d = (math.sin(th), -math.cos(th))
    pp = (d[1], -d[0])
    b1 = (E[0] + hw*pp[0], E[1] + hw*pp[1])
    b2 = (E[0] - hw*pp[0], E[1] - hw*pp[1])
    tip = (E[0] + L*d[0], E[1] + L*d[1])
    tri = (tip[0], tip[1], b1[0], b1[1], b2[0], b2[1])
    mt = cov(tri_pred(tri[0:2], tri[2:4], tri[4:6]))
    m = [[max(ma[y][x], mt[y][x]) for x in range(W)] for y in range(H)]
    return m, tri, (cx, cy, r, t0, t1, w)

if __name__=='__main__':
    show(T,'DESIGN')
    best=None
    for cx in [7.2,7.4,7.5,7.6,7.8]:
        for cy in [9.8,10.0,10.2,10.4]:
            for r in [4.8,5.0,5.2]:
                for t1 in [-140,-146,-152,-158,-164,-170]:
                    for hw in [1.5,1.8,2.1,2.4]:
                        for L in [2.0,2.5,3.0,3.5]:
                            for da in [-20,0,20,40]:
                                m,tri,arc=render3(cx,cy,r,0,t1,hw,L,tri_da=da)
                                e=err(m)
                                if best is None or e<best[0]:
                                    best=(e,cx,cy,r,t1,hw,L,da,m,tri,arc)
    e,cx,cy,r,t1,hw,L,da,m,tri,arc=best
    print('BEST err=%.3f cx=%.2f cy=%.2f r=%.2f t1=%.2f hw=%.2f L=%.2f da=%.0f'%(e,cx,cy,r,t1,hw,L,da))
    x0=cx+r*math.cos(0); y0=cy
    x1=cx+r*math.cos(math.radians(t1)); y1=cy+r*math.sin(math.radians(t1))
    print('  ARC: M%.2f %.2f A%.2f %.2f 0 0 %.2f %.2f'%(x0,y0,r,r,x1,y1))
    print('  TRI: M%.2f %.2f L%.2f %.2f L%.2f %.2f Z'%tuple(tri))
    show(m,'BEST')
    show(T,'DESIGN')
