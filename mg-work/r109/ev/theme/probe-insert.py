# -*- coding: utf-8 -*-
"""看 apply-dark.py / apply-theme.py 是怎么插入 <style id="r109-*-css"> 块的。"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
for fn in ['apply-dark.py', 'apply-theme.py', 'apply-tokens.py', 'apply-literals.py']:
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        print(fn, 'MISSING'); continue
    t = io.open(p, encoding='utf-8').read()
    print('=' * 70)
    print(fn, 'LEN=', len(t))
    for m in re.finditer(r'<style id=', t):
        print('   ', repr(t[max(0, m.start() - 120):m.start() + 60]))
    for m in re.finditer(r'ANCHOR|anchor', t):
        seg = t[max(0, m.start() - 100):m.start() + 160]
        print('  ANCHOR@%d %s' % (m.start(), repr(seg)))
        break
