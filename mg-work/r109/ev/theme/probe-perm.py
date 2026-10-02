# -*- coding: utf-8 -*-
"""r109 · 定位「默认权限」对话框面板的**视觉来源**（可能是 SVG 画的，底色在 fill 里）。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
t = io.open(os.path.join(ROOT, 'pages', 'base.html'), encoding='utf-8', newline='').read()

print('=== 1) 权限相关类名 ===')
for c in sorted(set(re.findall(r'perm-[a-zA-Z0-9_-]+', t))):
    print('   %-28s x%d' % (c, t.count(c)))

print()
print('=== 2) .perm-menu-item 前后的 fill: 取值（面板很可能是 SVG）===')
for m in re.finditer(r'perm-menu-item', t):
    i = m.start()
    seg = t[max(0, i - 1500):i + 300]
    fills = re.findall(r'fill:\s*`([^`]{0,60})`', seg)
    rects = re.findall(r'(?:width|height):\s*([0-9]+)', seg)
    if fills:
        print('@%d  fills=%s' % (i, fills[-6:]))
        print('        dims=%s' % (rects[-4:],))
    print('   ----')

print()
print('=== 3) 全页 SVG 面板底 fill（含 gray / bg / 半透明）的去重汇总 ===')
cnt = {}
for m in re.finditer(r'fill:\s*`([^`]{1,70})`', t):
    v = m.group(1)
    if re.search(r'gray|bg-|color-', v) or v.startswith('rgb('):
        cnt[v] = cnt.get(v, 0) + 1
for k, v in sorted(cnt.items(), key=lambda x: -x[1])[:25]:
    print('   %-52s x%d' % (k, v))
