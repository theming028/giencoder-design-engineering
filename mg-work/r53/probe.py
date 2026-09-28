# -*- coding: utf-8 -*-
"""r53 探针：只打印目标片段，避免整文件 Read。
用法: python probe.py <token> [<token2> ...]  —— 线性 find，带 ±win 上下文，去重。"""
import sys, re
PAGE = 'pages/task-detail.html'
s = open(PAGE, encoding='utf-8').read()
WIN = 200


def windows(tok, win=WIN):
    out = []
    start = 0
    while True:
        i = s.find(tok, start)
        if i < 0:
            break
        a = max(0, i - win)
        b = min(len(s), i + len(tok) + win)
        seg = s[a:b].replace('\n', '\\n')
        out.append((i, seg))
        start = i + 1
    return out


for tok in sys.argv[1:]:
    ws = windows(tok)
    print('=' * 70)
    print('TOKEN %r  出现 %d 次' % (tok, len(ws)))
    print('=' * 70)
    seen = set()
    for i, seg in ws:
        key = seg[:80]
        if key in seen:
            continue
        seen.add(key)
        print('  @%d  ...%s...' % (i, seg))
    print()
