# -*- coding: utf-8 -*-
"""r109 · 取 ZCode 菜单（.zd-menu.giencoder-dropdown-popup）与日期选择器面板的完整规则串 + 出现次数。"""
import io, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

for pat, name in [
    (r'\.zd-menu\.giencoder-dropdown-popup[^{]*\{[^}]*\}', u'ZCode 菜单'),
    (r'\.giencoder-date-picker-popup[^{]*\{[^}]*\}', u'日期选择器面板'),
]:
    print('=' * 100)
    print(name)
    print('=' * 100)
    sigs = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'pages', '*.html'))):
        s = io.open(p, encoding='utf-8', newline='').read()
        for m in re.finditer(pat, s):
            b = ' '.join(m.group(0).split())
            sigs.setdefault(b, []).append(os.path.basename(p))
    if not sigs:
        print('  （未找到）')
    for k, v in sigs.items():
        print('  x%d 页  LEN=%d' % (len(v), len(k)))
        print('  页: %s' % ', '.join(v[:4]))
        print('  ' + k)
    print()
