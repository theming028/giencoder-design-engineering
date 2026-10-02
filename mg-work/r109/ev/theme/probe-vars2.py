# -*- coding: utf-8 -*-
"""r109 · 查剩余三类面板所用变量的「浅/暗两档」实际值，判断是否偏离基准。
   基准面板 = rgba(var(--gray-1), 0.88)  ⇒ 浅 rgba(247,247,247,.88) / 暗 rgba(31,31,31,.88)"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
t = io.open(os.path.join(ROOT, 'pages', 'base.html'), encoding='utf-8', newline='').read()

NAMES = ['--color-bg-white', '--color-bg-popup', '--color-bg-1', '--color-bg-2',
         '--color-bg-5', '--color-white', '--gray-1']

for n in NAMES:
    vals = []
    for m in re.finditer(re.escape(n) + r'\s*:\s*([^;}]+)', t):
        vals.append((m.start(), m.group(1).strip()))
    if not vals:
        print('%-20s （未定义）' % n)
        continue
    print('%-20s' % n)
    for pos, v in vals[:4]:
        # 判断落在浅色块还是暗色块：看前面最近的 [giencoder-theme='dark']
        dark = False
        seg = t[max(0, pos - 4000):pos]
        k = seg.rfind("giencoder-theme='dark'")
        k2 = seg.rfind('}')
        if k > 0 and k > k2:
            dark = True
        print('    %-8s %s' % ('暗色' if dark else '浅色', v[:52]))
    print()
