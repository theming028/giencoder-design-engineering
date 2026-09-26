# -*- coding: utf-8 -*-
"""r15 补丁 A：补齐页面内联 :root 缺失的 --border-radius-xl。

根因：设计源 giencoder-design-system/colors_and_type.css 定义了 6 个圆角 token
      （none/small/medium/large/xl/circle），但 8 个页面内联的 :root 只拷贝了 5 个，
      漏了 --border-radius-xl:12px。导致 DS 契约 `.giencoder-modal{ border-radius:
      var(--border-radius-xl) }` 解析为空值 → 全站 modal/drawer 圆角失效（实测 0px）。

本补丁按设计源的顺序（large 之后、circle 之前）把 xl 补回页面，幂等。
全程二进制读写，避免换行符被转换。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')

OLD = b'--border-radius-large:8px;--border-radius-circle:50%;'
NEW = b'--border-radius-large:8px;--border-radius-xl:12px;--border-radius-circle:50%;'
DELTA = len(NEW) - len(OLD)

SRC = os.path.join(ROOT, 'giencoder-design-system', 'colors_and_type.css')
src = open(SRC, 'rb').read()
if b'--border-radius-xl:12px' not in src.replace(b' ', b''):
    print('[ABORT] 设计源未定义 --border-radius-xl:12px，请先确认契约')
    sys.exit(1)
print('[OK] 设计源确认 --border-radius-xl:12px')

changed = skipped = warned = 0
for name in sorted(os.listdir(PAGES)):
    if not name.endswith('.html'):
        continue
    path = os.path.join(PAGES, name)
    s = open(path, 'rb').read()
    before = len(s)
    if b'--border-radius-xl:' in s:
        print('[skip] %-18s 已含 --border-radius-xl' % name)
        skipped += 1
        continue
    n = s.count(OLD)
    if n != 1:
        print('[WARN] %-18s 锚点命中 %d 次（应为 1），跳过不动' % (name, n))
        warned += 1
        continue
    s = s.replace(OLD, NEW)
    if len(s) != before + DELTA:
        print('[ABORT] %s 长度增量异常' % name)
        sys.exit(1)
    open(path, 'wb').write(s)
    print('[OK]   %-18s +--border-radius-xl:12px;  (%d -> %d chars)' % (name, before, len(s)))
    changed += 1

print('\n完成：修改 %d / 跳过 %d / 警告 %d' % (changed, skipped, warned))
