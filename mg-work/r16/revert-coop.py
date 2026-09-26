# -*- coding: utf-8 -*-
"""r16 回滚：把「待协作任务」弹窗 .kb-coop-dialog 恢复到 r16 改动前的原样。

第 16 轮第 4 项把 kb-coop 改成与 kb-crt 相同的 1280x820 居中，属误改，需原样恢复为：
  · 宽度 var(--kb-coop-width)（80%）
  · top:0 + bottom:var(--kb-coop-gap-bottom)（顶部吸附、纵向拉伸）
  · 圆角 0 0 12px 12px（顶角直角）
  · 展开动效基准点 top center + transform: translateX(-50%) ...
第 16 轮的其余三项（假滚动条移除 / rq-status 12px / 浅灰底加深）保持不变。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'pages', 'kanban.html')
s = open(P, 'rb').read().decode('utf-8')
before = len(s)

REVERTS = [
    # 1) 基础块
    (
        """        position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
        width: min(1280px, calc(100% - 64px));
        height: min(820px, calc(100% - 24px));
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--kb-coop-bg); border-radius: var(--border-radius-xl);""",
        """        position: absolute; left: 50%; top: 0; transform: translateX(-50%);
        width: var(--kb-coop-width);
        height: auto; max-height: calc(100% - var(--kb-coop-gap-bottom));
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--kb-coop-bg); border-radius: 12px;""",
        '基础块：宽度/高度/定位/圆角还原',
    ),
    # 2) r13 覆盖块
    (
        """        top: 50%; bottom: auto;
        border-radius: var(--border-radius-xl);""",
        """        top: 0; bottom: var(--kb-coop-gap-bottom);
        height: auto; max-height: none;
        border-radius: 0 0 12px 12px;""",
        'r13 覆盖块：顶部吸附 + 顶角直角还原',
    ),
    # 3) 展开动效基准点与位移
    (
        """        transform-origin: center center;
        transform: translate(-50%, -50%) translateY(-12px) scaleY(0.97);""",
        """        transform-origin: top center;
        transform: translateX(-50%) translateY(-12px) scaleY(0.97);""",
        '展开动效基准点还原为 top center',
    ),
    # 4) 打开态 transform
    (
        "transform: translate(-50%, -50%) translateY(0) scaleY(1);",
        "transform: translateX(-50%) translateY(0) scaleY(1);",
        '打开态 transform 还原',
    ),
]

for old, new, why in REVERTS:
    n = s.count(old)
    if n != 1:
        print('[ABORT] 锚点命中 %d 次（应为 1）：%s' % (n, why))
        sys.exit(1)
    s = s.replace(old, new)
    print('[OK] %s' % why)

open(P, 'wb').write(s.encode('utf-8'))
print('\n%s  %d -> %d chars' % (os.path.basename(P), before, len(s)))
