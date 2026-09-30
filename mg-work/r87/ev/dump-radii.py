# -*- coding: utf-8 -*-
"""精确提取「选择器含 .giencoder-select-view 且声明了硬编码 border-radius」的规则原文。
⚠ 页面 bundle 是单行压缩产物（600KB 一行）⇒ 量词必须**有界**，否则回溯爆炸（r87 踩过）。"""
import io, re

RE = re.compile(r'(?P<sel>[^{}]{0,300}?)\{(?P<body>[^{}]{0,400}?border-radius\s*:\s*\d+px[^{}]{0,400}?)\}')

for pg in ['kanban.html', 'req-kanban.html', 'task-detail.html', 'avatar.html',
           'settings.html', 'base.html', 'dev.html', 'skills.html', 'automation.html']:
    css = io.open('pages/' + pg, encoding='utf-8').read()
    rows = []
    for m in RE.finditer(css):
        sel, body = m.group('sel'), m.group('body')
        if 'giencoder-select-view' not in sel:
            continue
        sel = sel.split('*/')[-1].strip()
        rows.append((sel, body))
    print('================== %s  (%d 条)' % (pg, len(rows)))
    for sel, body in rows:
        print('  SEL  : %r' % sel)
        print('  BODY : %r' % body)
        print()
