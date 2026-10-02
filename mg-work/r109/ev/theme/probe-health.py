# -*- coding: utf-8 -*-
"""全站健康体检：第十拍落盘后的关键契约是否齐备。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')
ALL = ['base', 'avatar', 'automation', 'skills', 'settings',
       'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail']

CHK = [
    (u'DS 包指纹', lambda t: ':root{--giencoderblue-1:245, 248, 255' in t),
    (u'r109-theme-css', lambda t: 'id="r109-theme-css"' in t),
    (u'r109-dark-css', lambda t: 'id="r109-dark-css"' in t),
    (u'r109-tw-css', lambda t: 'id="r109-tw-css"' in t),
    (u'r109-border-css', lambda t: 'id="r109-border-css"' in t),
    (u'data-gi-dark', lambda t: 'data-gi-dark="1"' in t),
    (u'ZCode 残留=0', lambda t: t.count('ZCode') == 0),
    (u'GienCoder 替换', lambda t: True),
    (u'select 浮层=gray-1', lambda t: '.giencoder-select-popup{z-index:1000;'
                                      'background:rgba(var(--gray-1),0.88)' in t),
    (u'r93-line 已令牌化', lambda t: '--r93-line: rgb(var(--gray-2));' in t
                                     or '--r93-line' not in t),
]

print('%-12s' % 'page' + ''.join('%18s' % c[0][:16] for c in CHK))
print('-' * (12 + 18 * len(CHK)))
bad = []
for pg in ALL:
    t = io.open(os.path.join(PAGES, pg + '.html'), encoding='utf-8').read()
    row = ''
    for name, fn in CHK:
        if name == u'GienCoder 替换':
            row += '%18s' % ('%d 处' % t.count('GienCoder'))
            continue
        ok = fn(t)
        row += '%18s' % ('OK' if ok else '✗✗')
        if not ok:
            bad.append((pg, name))
    print('%-12s' % pg + row)
print()
print('异常项：', bad if bad else '无')
print()
print('--- conversation 专项 ---')
t = io.open(os.path.join(PAGES, 'conversation.html'), encoding='utf-8').read()
for key in ['--r93-line:', '--r93-card:', 'data-gi-dark', 'id="r109-border-css"',
            'zai-org/GienCoder', 'ZCode']:
    i = t.find(key)
    print('  %-22s %s' % (key, ('@%d  %r' % (i, t[i:i + 60])) if i >= 0 else '无'))
