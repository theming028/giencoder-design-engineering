# -*- coding: utf-8 -*-
"""定位各页里对 .giencoder-select-view 圆角的覆盖规则（含 6px / 32px 等非 8px 值）。"""
import re, io, sys, os

PAGES = ['kanban.html', 'req-kanban.html', 'task-detail.html', 'avatar.html',
         'settings.html', 'base.html', 'dev.html', 'skills.html', 'automation.html']

# 抓含 select-view 或 select 且含 border-radius 的规则体
RE_RULE = re.compile(r'([^{}]{0,220}?)\{([^{}]*border-radius\s*:[^{}]*)\}', re.S)

for pg in PAGES:
    p = os.path.join('pages', pg)
    if not os.path.exists(p):
        continue
    css = io.open(p, encoding='utf-8').read()
    hits = []
    for m in RE_RULE.finditer(css):
        sel, body = m.group(1).strip(), m.group(2)
        if 'select' not in sel.lower():
            continue
        rad = re.findall(r'border-radius\s*:\s*([^;}]+)', body)
        # 只看非 var 的硬编码（8px 是目标值；把 8px 也列出来便于核对）
        hits.append((sel[-110:], [r.strip() for r in rad]))
    print('=== %s ===' % pg)
    seen = set()
    for sel, rad in hits:
        key = (sel, tuple(rad))
        if key in seen:
            continue
        seen.add(key)
        if 'select-view' in sel or 'sel' in sel:
            print('   %-100s  %s' % (sel.replace('\n', ' '), rad))
