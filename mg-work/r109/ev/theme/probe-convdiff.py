# -*- coding: utf-8 -*-
"""conversation.html 被 apply109 改动前后的差异定位。
   前 = ev/bak-zcode/conversation.html（zcode 之后、apply109 重跑之前）
   后 = pages/conversation.html
"""
import io, os, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
A = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-zcode', 'conversation.html')
B = os.path.join(ROOT, 'pages', 'conversation.html')

a = io.open(A, encoding='utf-8').read().split('\n')
b = io.open(B, encoding='utf-8').read().split('\n')
print('前 %d 行 / 后 %d 行' % (len(a), len(b)))

sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
ops = sm.get_opcodes()
nchg = 0
for tag, i1, i2, j1, j2 in ops:
    if tag == 'equal':
        continue
    nchg += 1
    print()
    print('--- %s  前[%d:%d] → 后[%d:%d] ---' % (tag, i1, i2, j1, j2))
    if tag in ('delete', 'replace'):
        print('  【前】')
        for x in a[i1:min(i2, i1 + 14)]:
            print('    ' + x[:200])
        if i2 - i1 > 14:
            print('    … 共 %d 行' % (i2 - i1))
    if tag in ('insert', 'replace'):
        print('  【后】')
        for x in b[j1:min(j2, j1 + 14)]:
            print('    ' + x[:200])
        if j2 - j1 > 14:
            print('    … 共 %d 行' % (j2 - j1))
print()
print('变更段数 =', nchg)
