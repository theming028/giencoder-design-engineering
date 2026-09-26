# -*- coding: utf-8 -*-
"""r16 补丁：泳道假滚动条移除 / rq-status 字号 / 浅灰底加深一级 / 两个弹窗尺寸统一。

1) 泳道 `.kb-col-scroll` 是自建的装饰性假滚动条（`.kb-col` 本身是 overflow:hidden，
   不产生滚动），按用户要求移除（CSS 定义 + HTML 使用处）。
2) `.rq-status` 字号由 --font-size-body-3(14px) 改为 --font-size-body-1(12px)。
3) `.kb-proj-select` 的 select 视图 与 `.kb-radio` 容器底色由 fill-1(#F7F7F7)
   加深一级到 fill-2(#F2F2F2)；hover 相应由 fill-2 提到 fill-3(#E5E5E5) 以保留反馈。
4) 「待协作任务」弹窗 .kb-coop-dialog 的尺寸/定位/圆角与「创建任务」弹窗 .kb-crt-dialog
   统一：min(1280px,100%-64px) × min(820px,100%-24px)，main 内居中，四角 12。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')

# ---------------- 两个页面共用 ----------------
COMMON = [
    (
        """.kb-proj-select .giencoder-select-view {
        height: 32px; min-height: 32px; padding: 0 12px; border-radius: 8px;
        background: var(--color-fill-1); border-color: transparent; box-shadow: none;
      }""",
        """.kb-proj-select .giencoder-select-view {
        height: 32px; min-height: 32px; padding: 0 12px; border-radius: 8px;
        background: var(--color-fill-2); border-color: transparent; box-shadow: none;
      }""",
        '项目选择器底色 fill-1 -> fill-2（加深一级）',
    ),
    (
        ".kb-proj-select .giencoder-select-view:hover { background: var(--color-fill-2); box-shadow: none; }",
        ".kb-proj-select .giencoder-select-view:hover { background: var(--color-fill-3); box-shadow: none; }",
        '项目选择器 hover fill-2 -> fill-3（保持反馈层级）',
    ),
    (
        """.kb-proj-select .giencoder-select-view[aria-expanded='true'] {
        background: var(--color-fill-1); border-color: var(--color-primary-6); box-shadow: none;
      }""",
        """.kb-proj-select .giencoder-select-view[aria-expanded='true'] {
        background: var(--color-fill-2); border-color: var(--color-primary-6); box-shadow: none;
      }""",
        '项目选择器展开态底色 fill-1 -> fill-2',
    ),
    (
        """.kb-radio {
        position: absolute; left: 228px; top: 8px; height: 32px;
        display: flex; align-items: center; background: var(--color-fill-1); border-radius: 6px;
      }""",
        """.kb-radio {
        position: absolute; left: 228px; top: 8px; height: 32px;
        display: flex; align-items: center; background: var(--color-fill-2); border-radius: 6px;
      }""",
        'kb-radio 容器底色 fill-1 -> fill-2（加深一级）',
    ),
    (
        "\n      .kb-col-scroll { position: absolute; right: 2px; top: 44px; width: 6px; height: 250px; border-radius: 3px; background: var(--color-fill-4); opacity: 0.55; }",
        "",
        '移除自建假滚动条 kb-col-scroll 的 CSS 定义',
    ),
]

# ---------------- 仅 kanban.html ----------------
KANBAN_ONLY = [
    (
        ', "            <span class=\\"kb-col-scroll\\"></span>"',
        "",
        '移除泳道内 kb-col-scroll 元素',
    ),
    (
        """.kb-coop-dialog {
        position: absolute; left: 50%; top: 0; transform: translateX(-50%);
        width: var(--kb-coop-width);
        height: auto; max-height: calc(100% - var(--kb-coop-gap-bottom));
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--kb-coop-bg); border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
      }""",
        """.kb-coop-dialog {
        position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
        width: min(1280px, calc(100% - 64px));
        height: min(820px, calc(100% - 24px));
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--kb-coop-bg); border-radius: var(--border-radius-xl);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
      }""",
        'kb-coop 尺寸/定位与创建任务弹窗统一（1280x820 居中）',
    ),
    # r13 覆盖块：把「顶部吸附」改回居中，并同步动效基准点
    (
        """        top: 0; bottom: var(--kb-coop-gap-bottom);
        height: auto; max-height: none;
        border-radius: 0 0 12px 12px;""",
        """        top: 50%; bottom: auto;
        border-radius: var(--border-radius-xl);""",
        'kb-coop r13 覆盖块改回居中 + 四角 12',
    ),
    (
        "        transform-origin: top center;\n        transform: translateX(-50%) translateY(-12px) scaleY(0.97);",
        "        transform-origin: center center;\n        transform: translate(-50%, -50%) translateY(-12px) scaleY(0.97);",
        'kb-coop 展开动效基准点 top -> center',
    ),
    (
        "transform: translateX(-50%) translateY(0) scaleY(1);",
        "transform: translate(-50%, -50%) translateY(0) scaleY(1);",
        'kb-coop 打开态 transform 补 translateY(-50%)',
    ),
]

# ---------------- 仅 req-kanban.html ----------------
REQ_ONLY = [
    (
        ".rq-status { display: inline-flex; align-items: center; gap: 4px; height: 22px; padding: 0 8px; border-radius: 4px; font-size: var(--font-size-body-3); line-height: 22px; white-space: nowrap; }",
        ".rq-status { display: inline-flex; align-items: center; gap: 4px; height: 22px; padding: 0 8px; border-radius: 4px; font-size: var(--font-size-body-1); line-height: 22px; white-space: nowrap; }",
        'rq-status 字号 14px -> 12px',
    ),
]


def apply(path, patches, label):
    s = open(path, 'rb').read().decode('utf-8')
    before = len(s)
    for old, new, why in patches:
        n = s.count(old)
        if n != 1:
            print('[ABORT] %s：锚点命中 %d 次（应为 1）-> %s' % (label, n, why))
            sys.exit(1)
        s = s.replace(old, new)
        print('  [OK] %s' % why)
    open(path, 'wb').write(s.encode('utf-8'))
    print('  %s  %d -> %d chars\n' % (os.path.basename(path), before, len(s)))


print('### kanban.html')
apply(os.path.join(PAGES, 'kanban.html'), COMMON + KANBAN_ONLY, 'kanban')
print('### req-kanban.html')
apply(os.path.join(PAGES, 'req-kanban.html'), COMMON + REQ_ONLY, 'req-kanban')
print('完成。')
