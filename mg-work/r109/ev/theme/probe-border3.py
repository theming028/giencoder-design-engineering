# -*- coding: utf-8 -*-
"""A. base.html 全部 --color-border* 定义（含 border / border-4）+ 浅暗判定
   B. 暗色块选择器精确原文
   C. colors_and_type.css 在页面里怎么出现的（是否真加载）
   D. colors_and_type.css 自身是否含 border 定义与暗色块
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

t = io.open(os.path.join(ROOT, 'pages', 'base.html'), encoding='utf-8').read()

print('--- A. base.html 全部 --color-border* 定义 ---')
for m in re.finditer(r'(--color-border[a-z0-9\-]*)\s*:\s*([^;}]*)', t):
    pre = t[max(0, m.start() - 6):m.start()]
    if 'var(' in pre:
        continue
    # 浅/暗：向前找最近的块开口，再看它前面 400 字节里有没有 dark
    k = m.start(); d = 0; selb = -1
    while k >= 0:
        if t[k] == '}': d += 1
        elif t[k] == '{':
            if d == 0:
                selb = k; break
            d -= 1
        k -= 1
    win = t[max(0, selb - 500):selb] if selb >= 0 else ''
    dark = ('giencoder-theme' in win and 'dark' in win)
    print('  @%-8d %-6s %-22s = %s' % (
        m.start(), 'DARK' if dark else 'LIGHT', m.group(1), m.group(2).strip()))

print()
print('--- B. 暗色块选择器原文 ---')
i = t.find('--color-bg-1')
while i != -1 and i < 400000:
    # 找该位置所在块的开口
    k = i; d = 0; selb = -1
    while k >= 0:
        if t[k] == '}': d += 1
        elif t[k] == '{':
            if d == 0:
                selb = k; break
            d -= 1
        k -= 1
    s0 = max(t.rfind('}', 0, selb), t.rfind('{', 0, selb)) + 1 if selb > 0 else 0
    print('  --color-bg-1 @%d 值=%s' % (i, t[i:i + 40].split(';')[0]))
    print('     sel = %r' % t[s0:selb].strip()[-160:])
    i = t.find('--color-bg-1', i + 1)
    if i > 345000:
        break

print()
print('--- C. colors_and_type.css 在 base.html 的出现形态 ---')
j = t.find('colors_and_type')
print('  %r' % t[max(0, j - 260):j + 120])

print()
print('--- D. DS 源文件自身 ---')
cs = os.path.join(ROOT, 'giencoder-design-system', 'colors_and_type.css')
if os.path.exists(cs):
    s = io.open(cs, encoding='utf-8').read()
    print('  大小 = %d 字符' % len(s))
    print('  dark 选择器出现次数 = %d' % len(re.findall(r'giencoder-theme', s)))
    for m in re.finditer(r'(--color-border[a-z0-9\-]*)\s*:\s*([^;}]*)', s):
        print('    %-22s = %s' % (m.group(1), m.group(2).strip()))
else:
    print('  不存在')
