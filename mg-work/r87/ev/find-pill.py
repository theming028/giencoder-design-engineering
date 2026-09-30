# -*- coding: utf-8 -*-
"""定位 task-detail / avatar 里 pill 形（border-radius 大值）select 触发框来源。"""
import io, re, sys

for pg in ['task-detail.html', 'avatar.html', 'kanban.html', 'req-kanban.html']:
    css = io.open('pages/' + pg, encoding='utf-8').read()
    print('==================== %s ====================' % pg)
    # 任何带 border-radius 且选择器里含 select 的规则
    for m in re.finditer(r'(?P<sel>[^{}]{0,200}?)\{(?P<body>[^{}]*)\}', css):
        sel, body = m.group('sel'), m.group('body')
        if 'select' not in sel.lower():
            continue
        rad = re.findall(r'border-radius\s*:\s*([^;}]+)', body)
        if not rad:
            continue
        vals = [r.strip() for r in rad]
        if all(v in ('8px',) for v in vals):
            continue          # 已是目标值，略过
        print('  SEL : %s' % sel.strip().replace('\n', ' ')[-170:])
        print('  RAD : %s' % vals)
        print()
