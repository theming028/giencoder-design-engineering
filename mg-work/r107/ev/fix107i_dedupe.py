# -*- coding: utf-8 -*-
"""一次性修补：MEMORY.md 里被重复插入 3 次的「P3.44 索引块」去重（保留 1 份）。"""
import importlib.util
import io
import sys

P = u'.workbuddy/memory/MEMORY.md'
spec = importlib.util.spec_from_file_location('d', u'mg-work/r107/ev/doc107i.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

t = io.open(P, 'rb').read().decode('utf-8')
k = m.MEM_IDX_INLINE
n = t.count(k)
print(u'当前重复次数 = %d，长度 %d' % (n, len(t)))
if n <= 1:
    print(u'无需修补')
    sys.exit(0)
t2 = t.replace(k, u'', n - 1)
io.open(P, 'wb').write(t2.encode('utf-8'))
print(u'去重后 = %d 次，长度 %d' % (t2.count(k), len(t2)))
