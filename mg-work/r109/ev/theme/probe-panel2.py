# -*- coding: utf-8 -*-
"""r109 · 抠出「基准面板」（默认权限/技能，role=listbox）的**完整 inline 规格**，
   以及待统一面板的现有定义，供 apply-popup.py 做整条替换。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
t = io.open(os.path.join(ROOT, 'pages', 'base.html'), encoding='utf-8', newline='').read()

# 基准：rgba(var(--gray-1), 0.88) 出现处，向前找 style={ 的起点
print('=== 基准面板（rgba(var(--gray-1), 0.88)）完整 style 定义 ===')
for m in re.finditer(r'rgba\(var\(--gray-1\), 0\.88\)', t):
    i = m.start()
    s = t.rfind('style:{', 0, i)
    if s < 0:
        s = max(0, i - 400)
    e = t.find('}', i)
    print('@%d' % i)
    print(t[s:i + 260][:520])
    print()
    break

print('=== 待统一：.giencoder-select-popup 的 CSS 规则（全站是否逐字相同）===')
import glob
sigs = {}
for p in sorted(glob.glob(os.path.join(ROOT, 'pages', '*.html'))):
    s = io.open(p, encoding='utf-8', newline='').read()
    for mm in re.finditer(r'\.giencoder-select-popup\s*\{[^}]*\}', s):
        body = ' '.join(mm.group(0).split())
        if 'background' not in body:
            continue
        sigs.setdefault(body[:200], []).append(os.path.basename(p))
for k, v in sigs.items():
    print('  x%d 页: %s' % (len(v), k))
    print('     首个: %s' % v[0])
    print()

print('=== 待统一：add 菜单面板（var(--color-bg-2) + blur(20px)）===')
for m in re.finditer(r'blur\(20px\)', t):
    i = m.start()
    s = t.rfind('style:', 0, i)
    print('@%d' % i)
    print(t[max(0, s):i + 90][:420])
    print()
    break
