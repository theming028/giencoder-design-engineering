# -*- coding: utf-8 -*-
"""r92：把 5 页与 r92 前置基线做字符级 diff，列出「改了哪些片段」，证明只动了该动的地方。"""
import difflib
import io
import os

for pg in ['base', 'settings', 'avatar', 'skills', 'automation']:
    a = io.open('mg-work/r92/before/%s.html' % pg, encoding='utf-8').read()
    b = io.open('pages/%s.html' % pg, encoding='utf-8').read()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
    print('##### %-11s %d → %d (%+d chars)  改动块 %d 处'
          % (pg + '.html', len(a), len(b), len(b) - len(a), len(ops)))
    for tag, i1, i2, j1, j2 in ops:
        old = a[i1:i2]
        new = b[j1:j2]
        print('  [%s] -%d/+%d' % (tag, len(old), len(new)))
        if len(old) <= 700:
            print('    - %r' % old[:400])
        else:
            print('    - <前 300> %r' % old[:300])
        if len(new) <= 900:
            print('    + %r' % new[:600])
        else:
            print('    + <前 500> %r' % new[:500])
    print()
