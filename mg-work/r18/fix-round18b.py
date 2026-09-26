# -*- coding: utf-8 -*-
"""r18b：把 main:aside 由「flex-grow 8:2」改为「基准 80%:20%」，得到精确 8:2。

原写法 flex:8 1 0 / flex:2 1 0 只按 basis(0) 之外的自由空间分配，
而 .kb-crt-main 自身有左右各 40px padding，未计入比例 → 实测 81.4 : 18.6。
改为 flex-basis 直接用百分比 + box-sizing:border-box（让百分比含 padding），
即得精确 80 : 20；保留 flex-grow/shrink 以维持窄屏可伸缩。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'pages', 'kanban.html')
s = open(P, 'rb').read().decode('utf-8')
before = len(s)


def sub(old, new, why):
    global s
    n = s.count(old)
    if n != 1:
        print('[ABORT] 命中 %d 次（应为 1）：%s' % (n, why))
        sys.exit(1)
    s = s.replace(old, new)
    print('  [OK] %s' % why)


sub(
    """        flex: 8 1 0; min-width: 0; display: flex; flex-direction: column;
        padding: 24px 40px 0; overflow: hidden;""",
    """        flex: 1 1 80%; box-sizing: border-box; min-width: 0;
        display: flex; flex-direction: column;
        padding: 24px 40px 0; overflow: hidden;""",
    '.kb-crt-main flex-basis 80% + border-box',
)
sub(
    """        flex: 2 1 0; min-width: 0; display: flex; flex-direction: column;
        border-left: 1px solid var(--kb-crt-divider);""",
    """        flex: 1 1 20%; box-sizing: border-box; min-width: 0;
        display: flex; flex-direction: column;
        border-left: 1px solid var(--kb-crt-divider);""",
    '.kb-crt-aside flex-basis 20% + border-box',
)

open(P, 'wb').write(s.encode('utf-8'))
print('\n%s  %d -> %d chars' % (os.path.basename(P), before, len(s)))
