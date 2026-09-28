#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r41b · 间隔线取色修正：--td-hairline(#F2F2F2，几乎不可见) → --color-border-2(#E5E5E5)
依据：页内既有分隔线先例 .td-bar-sep 用的就是 --color-border-2；DS 里 border-1(#F2F2F2) 是
最浅一档，border-3(#C9C9C9) 过重，border-2 才是标准「列表/栏内分隔」档。
幂等 + 自检。
"""
import sys

P = 'pages/task-detail.html'
OLD = 'border-top: 1px solid var(--td-hairline); }'
NEW = 'border-top: 1px solid var(--color-border-2); }'
OLD_C = '整体高度与值列起点均不变。仅作用于左栏 .td-side 下的 .td-attr。 */'
NEW_C = '整体高度与值列起点均不变。仅作用于左栏 .td-side 下的 .td-attr。\n         线色取 --color-border-2(#E5E5E5)：与页内 .td-bar-sep 同档，border-1(#F2F2F2) 太浅\n         几乎不可见，border-3(#C9C9C9) 过重。 */'

s = open(P, encoding='utf-8').read()
if NEW in s:
    print('ALREADY APPLIED'); sys.exit(0)
if s.count(OLD) != 1:
    print('FAILED: anchor count', s.count(OLD)); sys.exit(1)
s = s.replace(OLD, NEW, 1)
if s.count(OLD_C) != 1:
    print('FAILED: comment anchor', s.count(OLD_C)); sys.exit(1)
s = s.replace(OLD_C, NEW_C, 1)
assert 'var(--td-hairline); }' not in s
open(P, 'w', encoding='utf-8').write(s)
print('OK line color -> --color-border-2')
