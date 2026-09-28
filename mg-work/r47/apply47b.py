#!/usr/bin/env python3
# 第 47 轮第 1 项（幂等修复）：DS 权威源的滚动条三档
# 关键：锚点必须带上选择器名 —— 裸值替换（0.16→0.32）会与「0.08→0.16」串味、复跑不幂等。
import os, sys

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
FILES = ['giencoder-design-system/colors_and_type.css',
         'giencoder-design-system/gienx-templates/_shared/tokens.css']

SUBS = [
    ('scrollbar-color: rgba(var(--gray-10), 0.08)',
     'scrollbar-color: rgba(var(--gray-10), 0.16)'),
    ('::-webkit-scrollbar-thumb {\n    background-color: rgba(var(--gray-10), 0.08);',
     '::-webkit-scrollbar-thumb {\n    background-color: rgba(var(--gray-10), 0.16);'),
    ('::-webkit-scrollbar-thumb:hover {\n    background-color: rgba(var(--gray-10), 0.12);',
     '::-webkit-scrollbar-thumb:hover {\n    background-color: rgba(var(--gray-10), 0.24);'),
    ('::-webkit-scrollbar-thumb:active {\n    background-color: rgba(var(--gray-10), 0.16);',
     '::-webkit-scrollbar-thumb:active {\n    background-color: rgba(var(--gray-10), 0.32);'),
]

ok = True
for f in FILES:
    full = os.path.join(ROOT, f)
    s = open(full, encoding='utf-8').read()
    orig = s
    hits = []
    for old, new in SUBS:
        if new in s and old not in s:
            hits.append('idem')
            continue
        n = s.count(old)
        hits.append(str(n))
        if n != 1:
            print('  !! %s 锚点数量异常 x%d: %s' % (f, n, old[:52])); ok = False
        s = s.replace(old, new)
    if s != orig:
        open(full, 'w', encoding='utf-8').write(s)
    print('%-58s 命中 %s %s' % (f.split('/')[-1], ','.join(hits),
                                '已写入' if s != orig else '（无变化）'))

print('=== 自检 ===')
for f in FILES:
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    c = {v: s.count('rgba(var(--gray-10), %s)' % v) for v in ['0.08', '0.12', '0.16', '0.24', '0.32']}
    print('  %-28s %s' % (f.split('/')[-1], c))
    if c['0.08'] or c['0.12']:
        print('  !! 仍有旧值'); ok = False
    if c['0.16'] != 2 or c['0.24'] != 1 or c['0.32'] != 1:
        print('  !! 三档分布应为 16x2 / 24x1 / 32x1'); ok = False
print('OK' if ok else 'FAIL')
sys.exit(0 if ok else 1)
