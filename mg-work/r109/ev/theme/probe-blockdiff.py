# -*- coding: utf-8 -*-
"""取每页实际的 r109-border-css 块，与目标 BLOCK 逐字节比对（含换行符差异）。"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location(
    'ab', os.path.join(HERE, 'apply-border.py'))
ab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ab)

for pg in ab.ALL:
    t = ab.rd(os.path.join(ab.PAGES, pg + '.html'))
    m = ab.RE_BLOCK.search(t)
    if not m:
        print('%-12s 无块' % pg)
        continue
    got = m.group(0)
    same_exact = (got == ab.BLOCK)
    same_norm = (got.replace('\r\n', '\n') == ab.BLOCK.replace('\r\n', '\n'))
    print('%-12s 逐字节同=%-5s 规范化后同=%-5s  CRLF=%d LF=%d'
          % (pg, same_exact, same_norm,
             got.count('\r\n'), got.count('\n') - got.count('\r\n')))
    if not same_norm:
        a = got.replace('\r\n', '\n')
        b = ab.BLOCK.replace('\r\n', '\n')
        for i in range(min(len(a), len(b))):
            if a[i] != b[i]:
                print('     首个差异 @%d: got=%r want=%r' % (i, a[i - 40:i + 40], b[i - 40:i + 40]))
                break
        else:
            print('     长度不同 got=%d want=%d' % (len(a), len(b)))
