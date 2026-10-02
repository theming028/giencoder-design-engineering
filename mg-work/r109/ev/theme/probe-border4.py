# -*- coding: utf-8 -*-
"""统计全站 var(--color-border*) 引用量；并算出改动后的实际灰度值。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = ['base', 'conversation', 'avatar', 'kanban', 'req-kanban',
         'dev', 'settings', 'automation', 'skills', 'task-detail']

TOK = ['--color-border-1', '--color-border-2', '--color-border-3',
       '--color-border-4', '--color-border']

tot = {}
per = {}
for pg in PAGES:
    s = io.open(os.path.join(ROOT, 'pages', pg + '.html'), encoding='utf-8').read()
    per[pg] = {}
    for tk in TOK:
        n = len(re.findall(r'var\(\s*' + tk + r'\s*[,)]', s))
        per[pg][tk] = n
        tot[tk] = tot.get(tk, 0) + n

hdr = '%-12s' % 'page' + ''.join('%14s' % t.replace('--color-', '') for t in TOK)
print(hdr)
print('-' * len(hdr))
for pg in PAGES:
    print('%-12s' % pg + ''.join('%14d' % per[pg][t] for t in TOK))
print('-' * len(hdr))
print('%-12s' % 'TOTAL' + ''.join('%14d' % tot[t] for t in TOK))

print()
print('--- 灰度阶梯（浅 / 暗 镜像 N<->11-N）---')
LIGHT = {1: 247, 2: 242, 3: 229, 4: 201, 5: 169, 6: 134, 7: 107, 8: 78, 9: 43, 10: 31}
DARK = dict((n, LIGHT[11 - n]) for n in LIGHT)
print('  idx :', ' '.join('%4d' % n for n in range(1, 11)))
print('  浅  :', ' '.join('%4d' % LIGHT[n] for n in range(1, 11)))
print('  暗  :', ' '.join('%4d' % DARK[n] for n in range(1, 11)))

print()
print('--- border 令牌取值对照（bg 浅=#fff 255 / 暗=#17171a 23）---')
print('  %-18s %-10s %-10s %-10s %-10s' % ('令牌', '浅 idx', '浅值', '暗 idx(新)', '暗值(新)'))
old = {'border-1': 2, 'border-2': 3, 'border-3': 4, 'border-4': 6}
new = {'border-1': 1, 'border-2': 2, 'border-3': 3, 'border-4': 5}
for k in ['border-1', 'border-2', 'border-3', 'border-4']:
    oi = old[k]; ni = new[k]
    print('  %-18s gray-%-5d %-10d gray-%-6d %-10d' % (
        k, oi, LIGHT[oi], ni, DARK[ni]))
print()
print('  （暗色旧值：border-1=%d border-2=%d border-3=%d border-4=%d）' % (
    DARK[2], DARK[3], DARK[4], DARK[6]))
print('  （浅色保持不变：border-1=%d border-2=%d border-3=%d border-4=%d）' % (
    LIGHT[2], LIGHT[3], LIGHT[4], LIGHT[6]))
