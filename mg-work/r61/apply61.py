#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r61：task-detail.html「更多操作」下拉菜单两处调整

需求（邵先生 2026-09-28）：
  1. 菜单里的图标偏大，小两号；
  2. 「取消任务」item hover 时呈现红色系 —— 图标、文字、背景色三者同时转红。

改法：
  1. 只缩 svg（16px → 12px，墨迹 14px → 10.5px）；图标框仍 16px，
     文字起始 x 保持 37px 不变 → r59 的逐像素对齐结论继续成立，flex 居中自动吸收两侧各 2px。
  2. 给「取消任务」加 is-danger 标记，CSS 里按页内既有 danger 配方接管 hover 配色：
     底 --color-danger-light-1(#FFECE8) / 前景 --color-danger-6(#F53F3F)，
     与 .giencoder-tag-danger 同源。

幂等：每处替换带独立 MARK，命中即 SKIP。
自检：标签级计数不变 + 关键既有选择器计数不变 + 每个新 MARK 恰好出现 1 次。
"""
import io
import os
import sys

P = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pages', 'task-detail.html'))

# ---------------------------------------------------------------- 替换清单
SUBS = []

# ① item 的 transition 补上 color（危险项换前景色时要跟着过渡）
SUBS.append((
    'item transition 加 color',
    """        transition: background 120ms var(--transition-timing-function-standard, ease);
      }
      /* 与 r54 右键菜单、r57 定稿同档：hover 底 --color-fill-2（非 fill-1） */""",
    """        transition: background 120ms var(--transition-timing-function-standard, ease),
                    color 120ms var(--transition-timing-function-standard, ease);
      }
      /* 与 r54 右键菜单、r57 定稿同档：hover 底 --color-fill-2（非 fill-1） */""",
    'color 120ms var(--transition-timing-function-standard, ease);\n      }\n      /* 与 r54 右键菜单',
))

# ② 危险项 hover / 虚拟焦点配色
SUBS.append((
    '危险项 hover 配色',
    """      .td-more .giencoder-dropdown-item:hover,
      .td-more .giencoder-dropdown-item.is-hover { background: var(--color-fill-2); }
      .td-more-ico {""",
    """      .td-more .giencoder-dropdown-item:hover,
      .td-more .giencoder-dropdown-item.is-hover { background: var(--color-fill-2); }
      /* ★ 第 61 轮：「取消任务」= 危险项，hover / 虚拟焦点时 底 / 字 / 图标 同时转红。
         色档沿用页内既有 danger 配方（与 .giencoder-tag-danger 同源，不新造色）：
           底色 --color-danger-light-1(#FFECE8) · 前景 --color-danger-6(#F53F3F)。
         选择器 (0,4,0) > 上方通用 hover 的 (0,3,0)，与书写顺序无关。 */
      .td-more .giencoder-dropdown-item.is-danger:hover,
      .td-more .giencoder-dropdown-item.is-danger.is-hover {
        background: var(--color-danger-light-1);
        color: var(--color-danger-6);
      }
      /* 图标自带 color(--color-text-1)，必须单独覆盖，靠继承拿不到 */
      .td-more .giencoder-dropdown-item.is-danger:hover .td-more-ico,
      .td-more .giencoder-dropdown-item.is-danger.is-hover .td-more-ico {
        color: var(--color-danger-6);
      }
      .td-more-ico {""",
    '危险项，hover / 虚拟焦点时',
))

# ③ .td-more-ico 加 color 过渡
SUBS.append((
    '图标加 color 过渡',
    """      .td-more-ico {
        flex: none; width: 16px; height: 16px; display: inline-flex;
        align-items: center; justify-content: center; color: var(--color-text-1);
      }
      .td-more-ico svg { display: block; width: 16px; height: 16px; }""",
    """      .td-more-ico {
        flex: none; width: 16px; height: 16px; display: inline-flex;
        align-items: center; justify-content: center; color: var(--color-text-1);
        transition: color 120ms var(--transition-timing-function-standard, ease);
      }
      /* ★ 第 61 轮：图标墨迹「小两号」—— 16px → 12px（墨迹 14px → 10.5px）。
         只缩 svg，图标框仍 16px：文字起始 x 保持 37px 不变（r59 的逐像素对齐结论继续成立），
         且 flex 居中会自动吸收两侧各 2px 余量。 */
      .td-more-ico svg { display: block; width: 12px; height: 12px; }""",
    '图标墨迹「小两号」',
))

# ④ ITEMS 里给「取消任务」打 danger 标记
SUBS.append((
    'ITEMS 标记 danger',
    """      { id: 'cancel', label: '取消任务', svg: ICONS.cancel }""",
    """      /* ★ 第 61 轮：取消任务 = 危险项 → hover 时底色/文字/图标转红色系 */
      { id: 'cancel', label: '取消任务', svg: ICONS.cancel, danger: true }""",
    "label: '取消任务', svg: ICONS.cancel, danger: true",
))

# ⑤ build() 落类名
SUBS.append((
    'build 落 is-danger 类',
    """        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item';""",
    """        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item' + (it.danger ? ' is-danger' : '');""",
    "+ (it.danger ? ' is-danger' : '')",
))

# ⑥ 两处图标注释同步到 12px 口径
SUBS.append((
    '图标注释同步 12px',
    """      /* 终止任务：圆圈 + 实心方块。24 viewBox + stroke 2.2 落在 16px 框里
         ⇒ 视觉笔画 1.47px、外圈墨迹 ≈14px，与设计稿 2× 量测（笔画 ≈1.5、墨迹 28px@2×）吻合。 */""",
    """      /* 终止任务：圆圈 + 实心方块。24 viewBox + stroke 2.2。
         r59 定稿 16px 框（笔画 1.47px / 墨迹 14px，与设计稿 2× 量测吻合）；
         ★ r61 按要求「小两号」→ 12px 框（笔画 1.10px / 墨迹 10.5px），几何比例不变。 */""",
    'r61 按要求「小两号」→ 12px 框',
))

SUBS.append((
    '叉号注释同步 12px',
    """      /* 取消任务：圆圈 + 叉（设计稿叉臂实测 ≈6px ⇒ 24 viewBox 里 ±4.2） */""",
    """      /* 取消任务：圆圈 + 叉（设计稿叉臂实测 ≈6px ⇒ 24 viewBox 里 ±4.2）；
         ★ r61 同终止任务，框 16px → 12px。 */""",
    '★ r61 同终止任务，框 16px → 12px',
))

# ---------------------------------------------------------------- 自检清单
STABLE = [
    '<style>', '</style>', '<script>', '</script>',
    '.td-more.giencoder-dropdown-popup {',
    '.td-more .giencoder-dropdown-item.is-hover { background: var(--color-fill-2); }',
    '.td-more-label { flex: 1;',
    '.td-more .giencoder-dropdown-item:hover,',
]


def main():
    with io.open(P, encoding='utf-8') as f:
        before = f.read()
    src = before

    for label, old, new, mark in SUBS:
        if mark in src:
            print('[SKIP] %-22s MARK 已存在' % label)
            continue
        n = src.count(old)
        if n != 1:
            print('[FAIL] %-22s OLD 命中 %d 次（应为 1）→ 未写盘' % (label, n))
            return 1
        src = src.replace(old, new, 1)
        print('[OK]   %-22s 已替换' % label)

    fails = []
    for t in STABLE:
        if src.count(t) != before.count(t):
            fails.append('stable token %r 计数变化：%d → %d'
                         % (t, before.count(t), src.count(t)))
    for label, old, new, mark in SUBS:
        c = src.count(mark)
        if c != 1:
            fails.append('MARK %r 出现 %d 次（应为 1）[%s]' % (mark[:32], c, label))

    if fails:
        for x in fails:
            print('[FAIL]', x)
        print('!! 自检未通过，未写盘')
        return 1

    print('[OK] 自检通过：标签计数不变 / 既有选择器计数不变 / 6 处 MARK 各 1 次')
    for t in STABLE:
        print('      %-62s %d' % (t[:62], src.count(t)))

    if src == before:
        print('      bytes %d（no-op）' % len(src.encode('utf-8')))
        print('ALL PASS (no-op)')
        return 0

    with io.open(P, 'w', encoding='utf-8') as f:
        f.write(src)
    print('      bytes %d → %d (Δ %+d)' % (len(before.encode('utf-8')),
                                           len(src.encode('utf-8')),
                                           len(src.encode('utf-8')) - len(before.encode('utf-8'))))
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
