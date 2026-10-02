# -*- coding: utf-8 -*-
import math
# arc centreline samples extracted from the design raster (design px == 14px grid px),
# design box = x 956..969 (14 wide) , ink y 225..231 (7 tall)
#   left branch (excluding arrow blob) / top / right branch
samples = [(963.0,225.0),(963.5,226.0),(961.5,227.0),(966.0,227.0),
           (960.0,228.0),(966.5,228.0),(959.8,229.0),(967.6,229.0),
           (968.0,230.0),(968.6,231.0)]
# least squares circle fit
n=len(samples)
sx=sum(p[0] for p in samples); sy=sum(p[1] for p in samples)
sxx=sum(p[0]**2 for p in samples); syy=sum(p[1]**2 for p in samples)
sxy=sum(p[0]*p[1] for p in samples)
sxz=sum(p[0]*(p[0]**2+p[1]**2) for p in samples)
syz=sum(p[1]*(p[0]**2+p[1]**2) for p in samples)
sz=sum(p[0]**2+p[1]**2 for p in samples)
# solve  [sxx sxy sx; sxy syy sy; sx sy n] [a b c] = [sxz; syz; sz]
import itertools
A=[[sxx,sxy,sx],[sxy,syy,sy],[sx,sy,n]]
B=[sxz,syz,sz]
def solve(A,B):
    n=3; M=[row[:]+[B[i]] for i,row in enumerate(A)]
    for i in range(n):
        p=max(range(i,n),key=lambda r:abs(M[r][i])); M[i],M[p]=M[p],M[i]
        for r in range(n):
            if r!=i:
                f=M[r][i]/M[i][i]
                for c in range(i,n+1): M[r][c]-=f*M[i][c]
    return [M[i][n]/M[i][i] for i in range(n)]
a,b,c=solve(A,B)
cx=a/2; cy=b/2; r=math.sqrt(c+cx*cx+cy*cy)
print('fit (design px):  center=(%.3f, %.3f)  r=%.3f'%(cx,cy,r))
for (x,y) in samples:
    d=math.hypot(x-cx,y-cy)
    ang=math.degrees(math.atan2(y-cy,x-cx))
    print('   (%5.1f,%5.1f) r=%.2f  ang=%7.2f'%(x,y,d,ang))
# box origin: x0=956 ; ink y0=225 -> centre vertically in 14 => dy = 3.5
print()
print('--- in viewBox 14 (x_vb = x-956, y_vb = y-225+3.5) ---')
print('center = (%.3f, %.3f)  r = %.3f'%(cx-956, cy-225+3.5, r))
for (x,y) in samples:
    print('   (%6.2f,%6.2f)'%(x-956, y-225+3.5))
