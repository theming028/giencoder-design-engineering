# -*- coding: utf-8 -*-
"""每页 </head> 的两次出现分别在哪（上下文 + 是否注释/JS 串内）。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

ALL = ['base', 'avatar', 'automation', 'skills', 'settings',
       'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail']


def comment_spans(t):
    out = []
    for m in re.finditer(u'<!--', t):
        e = t.find(u'-->', m.end())
        out.append((m.start(), (e + 3) if e > 0 else len(t)))
    for m in re.finditer(u'/\\*', t):
        e = t.find(u'*/', m.end())
        out.append((m.start(), (e + 2) if e > 0 else len(t)))
    return out


for pg in ALL:
    t = io.open(os.path.join(PAGES, pg + '.html'), encoding='utf-8').read()
    spans = comment_spans(t)
    pos = [m.start() for m in re.finditer(u'</head>', t)]
    print('=' * 70)
    print(pg, '  </head> @', pos, '  文件长度', len(t))
    for i in pos:
        inc = any(a <= i < b for a, b in spans)
        print('   @%-8d 注释内=%s' % (i, inc))
        print('       %r' % t[max(0, i - 200):i + 30])
    print('   <body 首个位置 =', t.find('<body'))
    for m in re.finditer(r'<style id="(r109-[a-z\-]+)"', t):
        print('   已有块: %-16s @%d' % (m.group(1), m.start()))
