# -*- coding: utf-8 -*-
import re

s = open('pages/kanban.html', encoding='utf-8').read()
i = s.find('kb-crt-lbl\\">状态')
print('label 位置:', i)
print('--- 前后原文 repr ---')
print(repr(s[i - 420:i + 40]))
print()

tests = {
    'p_row': r'<div class=\\"kb-crt-row\\">',
    'p_row_div': r'<div class=\\"kb-crt-row\\"><div class=\\"giencoder-select kb-crt-fld',
    'p_cls_a': r'<div class=\\"(giencoder-select kb-crt-fld[a-z0-9 -]*)\\">',
    'p_view': r'<div class=\\"giencoder-select-view\\"([^>]*)>',
    'p_lbl': r'<span class=\\"kb-crt-lbl\\">([^<]+)</span>',
}
for name, p in tests.items():
    print('%-12s -> %d 命中' % (name, len(re.findall(p, s))))
