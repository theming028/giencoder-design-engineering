# -*- coding: utf-8 -*-
"""gaps.log 去行号归一化比对：只关心『文件 + 描述』的集合与计数，忽略行号位移。"""
import re, io, collections, sys

RE_LN = re.compile(r'^(?P<f>[^:]+):\d+')

def norm(path):
    c = collections.Counter()
    for ln in io.open(path, encoding='utf-8'):
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        c[RE_LN.sub(lambda m: m.group('f') + ':*', ln)] += 1
    return c

a = norm(sys.argv[1])   # HEAD
b = norm(sys.argv[2])   # NOW
print('HEAD 缺口 %d 条 / NOW 缺口 %d 条' % (sum(a.values()), sum(b.values())))
print('--- 只在 HEAD（本轮被消除）---')
for k in sorted((a - b).elements()):
    print('  - ' + k)
print('--- 只在 NOW（本轮新增）---')
for k in sorted((b - a).elements()):
    print('  + ' + k)
print('--- 计数变化 ---')
same = True
for k in sorted(set(a) | set(b)):
    if a[k] != b[k]:
        same = False
        print('  ~ %s  %d -> %d' % (k, a[k], b[k]))
if same:
    print('  (无)')
