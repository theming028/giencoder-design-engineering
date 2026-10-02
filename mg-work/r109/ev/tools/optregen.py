# -*- coding: utf-8 -*-
import math
from PIL import Image
W=H=14; SS=5; INK=134.0
im=Image.open('mg-work/r93/raw/design-rgb.png').convert('RGB'); px=im.load()
T=[[max(0.0,min(1.0,(255.0-((px[956+x,221+y][0]*299+px[956+x,221+y][1]*587+px[956+x,221+y][2]*114)//1000))/121.0)) for x in range(W)] for y in range(H)]
PTS=[(x+(i+0.5)/SS,y+(j+0.5)/SS) for y in range(H) for x in range(W) for j in range(SS) for i in range(SS)]
def render(cx,cy,r,t1,hw,L,da,w=1.3):
    m=[[0]*W for _ in range(H)]
    half=w/2.0; lo,hi=min(0.0,t1),max(0.0,t1)
    for (x,y) in PTS:
        dx,dy=x-cx,y-cy; d=math.hypot(dx,dy)
        if abs(d-r)<=half:
            ad=math.degrees(math.atan2(dy,dx))
            for k in (-1,0,1):
                if lo<=ad+k*360<=hi: m[int(y)][int(x)]=1; break
    th=math.radians(t1+da)
    E=(cx+r*math.cos(th),cy+r*math.sin(th))
    dv=(math.sin(th),-math.cos(th)); pp=(dv[1],-dv[0])
    b1=(E[0]+hw*pp[0],E[1]+hw*pp[1]); b2=(E[0]-hw*pp[0],E[1]-hw*pp[1])
    tip=(E[0]+L*dv[0],E[1]+L*dv[1])
    A,B,C=tip,b1,b2
    def sg(a,b,c): return (a[0]-c[0])*(b[1]-c[1])-(b[0]-c[0])*(a[1]-c[1])
    for (x,y) in PTS:
        p=(x,y); d1=sg(p,A,B); d2=sg(p,B,C); d3=sg(p,C,A)
        if not(((d1<0)or(d2<0)or(d3<0)) and ((d1>0)or(d2>0)or(d3>0))):
            m[int(y)][int(x)]=1
    return [[sum(1 for (sx,sy) in PTS if int(sy)==y and int(sx)==x and False) or 0 for x in range(W)] for y in range(H)]
# the above is O(n^2); do it properly
def render2(cx,cy,r,t1,hw,L,da,w=1.3):
    cov=[[0]*W for _ in range(H)]
    half=w/2.0; lo,hi=min(0.0,t1),max(0.0,t1)
    th=math.radians(t1+da)
    E=(cx+r*math.cos(th),cy+r*math.sin(th))
    dv=(math.sin(th),-math.cos(th)); pp=(dv[1],-dv[0])
    b1=(E[0]+hw*pp[0],E[1]+hw*pp[1]); b2=(E[0]-hw*pp[0],E[1]-hw*pp[1])
    tip=(E[0]+L*dv[0],E[1]+L*dv[1]); A,B,C=tip,b1,b2
    def sg(a,b,c): return (a[0]-c[0])*(b[1]-c[1])-(b[0]-c[0])*(a[1]-c[1])
    for (x,y) in PTS:
        hit=False
        dx,dy=x-cx,y-cy; d=math.hypot(dx,dy)
        if abs(d-r)<=half:
            ad=math.degrees(math.atan2(dy,dx))
            for k in (-1,0,1):
                if lo<=ad+k*360<=hi: hit=True; break
        if not hit:
            p=(x,y); d1=sg(p,A,B); d2=sg(p,B,C); d3=sg(p,C,A)
            if not(((d1<0)or(d2<0)or(d3<0)) and ((d1>0)or(d2>0)or(d3>0))): hit=True
        if hit: cov[int(y)][int(x)]+=1
    return [[cov[y][x]/(SS*SS) for x in range(W)] for y in range(H)]
def err(m): return sum((m[y][x]-T[y][x])**2 for y in range(H) for x in range(W))
def show(m,t=''):
    ch=' .:-=+*#%@'
    print('--',t)
    for y in range(H): print('%3d %s'%(y,''.join(ch[min(9,int(m[y][x]*10))] for x in range(W))))
P=[7.8,10.3,5.0,-154.0,2.1,2.8,0.0]
names=['cx','cy','r','t1','hw','L','da']
BOUND={'hw':(1.4,2.5),'L':(1.8,3.2),'da':(-25.0,25.0),'cx':(7.2,8.2),'cy':(9.9,10.7),'r':(4.7,5.3),'t1':(-175.0,-135.0)}
def clamp(name,v):
    lo,hi=BOUND[name]; return max(lo,min(hi,v))
best=err(render2(*P)); print('init err %.3f'%best)
for st in [1.0,0.5,0.25,0.12,0.06,0.03]:
    improved=True
    while improved:
        improved=False
        for i,n in enumerate(names):
            for d in (st,-st):
                c=P[:]; c[i]=clamp(n,P[i]+d)
                if c[i]==P[i]: continue
                e=err(render2(*c))
                if e<best-1e-9: best=e; P=c; improved=True
print('final err %.3f'%best)
print('  '+' '.join('%s=%.3f'%(n,v) for n,v in zip(names,P)))
cx,cy,r,t1,hw,L,da=P
print('  ARC: M%.2f %.2f A%.2f %.2f 0 0 %.2f %.2f'%(cx+r,cy,r,r,cx+r*math.cos(math.radians(t1)),cy+r*math.sin(math.radians(t1))))
th=math.radians(t1+da); E=(cx+r*math.cos(th),cy+r*math.sin(th))
dv=(math.sin(th),-math.cos(th)); pp=(dv[1],-dv[0])
b1=(E[0]+hw*pp[0],E[1]+hw*pp[1]); b2=(E[0]-hw*pp[0],E[1]-hw*pp[1]); tip=(E[0]+L*dv[0],E[1]+L*dv[1])
print('  TRI: M%.2f %.2f L%.2f %.2f L%.2f %.2f Z'%(tip+b1+b2))
show(render2(*P),'FIT'); show(T,'DESIGN')
