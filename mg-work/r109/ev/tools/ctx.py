# -*- coding: utf-8 -*-
import io, sys, re
def load(p):
    return io.open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')
def ctx(p, kw, before=300, after=900, limit=20, nth=None):
    s = load(p)
    n = 0
    start = 0
    while True:
        i = s.find(kw, start)
        if i < 0:
            break
        n += 1
        if nth is None or n == nth:
            print('#### %s @%d (#%d)' % (kw, i, n))
            print(s[max(0, i-before): i+after])
            print('----------------------------------------------------------')
        start = i + len(kw)
        if n > limit:
            break
    if n == 0:
        print('!! no hit for', kw, 'in', p)
if __name__ == '__main__':
    p = sys.argv[1]
    kw = sys.argv[2]
    b = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    a = int(sys.argv[4]) if len(sys.argv) > 4 else 900
    lim = int(sys.argv[5]) if len(sys.argv) > 5 else 20
    ctx(p, kw, b, a, lim)
