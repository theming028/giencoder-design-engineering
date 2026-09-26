# -*- coding: utf-8 -*-
"""r18：创建任务弹窗宽度自适应 + main/aside 比例 8:2。

1) .kb-crt-title / .kb-crt-editor 去掉 max-width:880px
   （弹窗 80% 宽后 main 内容区已 < 880，该上限当前不生效；但窗口变宽时会把输入区卡在 880
   而右侧留白，故按用户要求改为完全自适应，跟随 main 内容宽）。
2) .kb-crt-main : .kb-crt-aside = 8 : 2
   原为 main flex:1 + aside 固定 320px（实测 818:320 ≈ 71.9:28.1）。
   改为两侧都按 flex-grow 分配（8 / 2），aside 去掉固定宽度。
   aside 变窄后其内部「label 80px + 控件」必须能收缩，故 .kb-crt-fld 与 .kb-crt-date
   改为 flex:1 + min-width:0。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'pages', 'kanban.html')
s = open(P, 'rb').read().decode('utf-8')
before = len(s)


def sub(old, new, why):
    global s
    n = s.count(old)
    if n != 1:
        print('[ABORT] 命中 %d 次（应为 1）：%s' % (n, why))
        sys.exit(1)
    s = s.replace(old, new)
    print('  [OK] %s' % why)


print('### 1. 标题 / 编辑器宽度自适应（去掉 max-width:880px）')
sub(
    """.kb-crt-main .kb-crt-title {
        width: 100%; max-width: 880px; height: 40px; flex: none;
        border-radius: var(--border-radius-large); padding: 0 12px;
      }""",
    """.kb-crt-main .kb-crt-title {
        width: 100%; height: 40px; flex: none;
        border-radius: var(--border-radius-large); padding: 0 12px;
      }""",
    'kb-crt-title 去掉 max-width',
)
sub(
    """.kb-crt-editor {
        margin-top: 20px; width: 100%; max-width: 880px;
        flex: 1 1 320px; min-height: 140px; max-height: 320px;""",
    """.kb-crt-editor {
        margin-top: 20px; width: 100%;
        flex: 1 1 320px; min-height: 140px; max-height: 320px;""",
    'kb-crt-editor 去掉 max-width',
)

print('### 2. main : aside = 8 : 2')
sub(
    """.kb-crt-main {
        flex: 1; min-width: 0; display: flex; flex-direction: column;
        padding: 24px 40px 0; overflow: hidden;
      }""",
    """.kb-crt-main {
        flex: 8 1 0; min-width: 0; display: flex; flex-direction: column;
        padding: 24px 40px 0; overflow: hidden;
      }""",
    'kb-crt-main flex 1 -> 8',
)
sub(
    """.kb-crt-aside {
        width: 320px; flex: none; display: flex; flex-direction: column;
        border-left: 1px solid var(--kb-crt-divider);
      }""",
    """.kb-crt-aside {
        flex: 2 1 0; min-width: 0; display: flex; flex-direction: column;
        border-left: 1px solid var(--kb-crt-divider);
      }""",
    'kb-crt-aside 固定 320px -> flex 2（可收缩）',
)
sub(
    ".kb-crt-fld { width: 192px; flex: none; }",
    ".kb-crt-fld { flex: 1 1 0; min-width: 0; }",
    'kb-crt-fld 固定 192px -> flex:1（随 aside 收缩）',
)
sub(
    ".kb-crt-date, .kb-crt-date .giencoder-input-wrapper { width: 192px; min-width: 192px; }",
    ".kb-crt-date, .kb-crt-date .giencoder-input-wrapper { width: auto; min-width: 0; }",
    'kb-crt-date 固定 192px -> 自适应',
)

open(P, 'wb').write(s.encode('utf-8'))
print('\n%s  %d -> %d chars' % (os.path.basename(P), before, len(s)))
