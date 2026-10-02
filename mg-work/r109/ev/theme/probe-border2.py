# -*- coding: utf-8 -*-
"""1) 打印 base.html 暗色变量块的“选择器原文”字节级上下文
   2) 列出全站所有 --color-border* 令牌的定义名（去重）
   3) 检查 giencoder-design-system/colors_and_type.css 是否被页面引用
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = ['base', 'conversation', 'avatar', 'kanban', 'req-kanban',
         'dev', 'settings', 'automation', 'skills', 'task-detail']

p = os.path.join(ROOT, 'pages', 'base.html')
t = io.open(p, encoding='utf-8').read()

print('--- A. base 暗色块选择器原文（@339748 前 260 字节）---')
print(repr(t[339748 - 300:339748 + 40]))

print()
print('--- B. base 浅色块选择器原文（@331830 前 260 字节）---')
print(repr(t[331830 - 300:331830 + 40]))

print()
print('--- C. 全站 --color-border* 定义名（去重，全仓）---')
names = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames
                   if d not in ('node_modules', '.git', '.workbuddy', 'mg-work')]
    for fn in filenames:
        if not fn.endswith(('.html', '.css', '.js', '.vue', '.tsx', '.ts')):
            continue
        fp = os.path.join(dirpath, fn)
        try:
            s = io.open(fp, encoding='utf-8').read()
        except Exception:
            continue
        for m in re.finditer(r'(--color-border[a-z0-9\-]*)\s*:', s):
            pre = s[max(0, m.start() - 6):m.start()]
            if 'var(' in pre:
                continue
            names.setdefault(m.group(1), set()).add(os.path.relpath(fp, ROOT))
for k in sorted(names):
    print('  %-24s %d 处文件: %s' % (k, len(names[k]),
                                     sorted(names[k])[:3]))

print()
print('--- D. 页面是否引用 colors_and_type.css ---')
for pg in PAGES:
    s = io.open(os.path.join(ROOT, 'pages', pg + '.html'), encoding='utf-8').read()
    print('  %-12s colors_and_type.css 引用 = %d ; <link href> 总数 = %d'
          % (pg, s.count('colors_and_type'), len(re.findall(r'<link[^>]*href=', s))))
