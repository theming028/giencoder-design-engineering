# -*- coding: utf-8 -*-
"""r15 补丁 B：创建任务弹窗 3 处实测偏差修正（幂等）。

1) 任务标题输入框高度 40px 被设计系统 `.giencoder-input-wrapper[data-size="large"]{height:36px}`
   以 (0,2,0) 特异性覆盖（原规则仅 (0,1,0)）。加 `.kb-crt-main` 前缀提到 (0,3,0)。
2) 同上，`.kb-crt-type + .kb-crt-title` 的 margin-top 一并加前缀保持一致。
3) 富文本编辑器在设计稿为固定 320 高；`flex:1 1 320px` 在大视口会撑大，补 max-height 封顶，
   小视口仍由 min-height:140px 收缩。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'pages', 'kanban.html')
s = open(P, 'rb').read()
before = len(s)

PATCHES = [
    (b'.kb-crt-type + .kb-crt-title { margin-top: 16px; }',
     b'.kb-crt-main .kb-crt-type + .kb-crt-title { margin-top: 16px; }',
     'type -> title 间距规则提到 (0,3,0)'),
    (b'\n      .kb-crt-title {',
     b'\n      .kb-crt-main .kb-crt-title {',
     'task title 高度 40px 覆盖 DS 的 36px'),
    (b'flex: 1 1 320px; min-height: 140px;',
     b'flex: 1 1 320px; min-height: 140px; max-height: 320px;',
     'editor 大视口封顶 320px（设计稿值）'),
]

for old, new, why in PATCHES:
    n = s.count(old)
    if n != 1:
        print('[ABORT] 锚点命中 %d 次（应为 1）：%s' % (n, why))
        sys.exit(1)
    s = s.replace(old, new)
    print('[OK] %s' % why)

open(P, 'wb').write(s)
print('\n%s  %d -> %d chars' % (os.path.basename(P), before, len(s)))
