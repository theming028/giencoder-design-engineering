#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r66b：看板泳道内滚 —— 补齐 scrollbar-gutter: stable

背景（r66 取证结论）：
  .kb-col-body 加 overflow-y:auto 后，**只有溢出**的泳道出现滚动条，
  经典滚动条会占据 6px（headless 下 11px），导致 4 条泳道卡片宽度不一致
  （实测 cardW = 307 / 307 / 318 / 318），"有的泳道窄一点" 看起来像缺陷。

修法：
  scrollbar-gutter: stable → 所有泳道恒定预留滚动条槽位，4 条泳道卡片永远等宽。
  代价：不溢出的泳道右侧留 6px 空槽（视觉上与内距无异）。

幂等：newmark 命中即 SKIP；未命中要求锚点恰好 1 次。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = os.path.join(ROOT, 'pages', 'kanban.html')

applied, skipped = [], []


def sub(path, label, old, new, newmark, expect=1):
    txt = open(path, encoding='utf-8').read()
    if newmark and newmark in txt:
        skipped.append((os.path.basename(path), label))
        return False
    n = txt.count(old)
    if n != expect:
        sys.exit('✗ [%s] %s 锚点命中 %d 次（期望 %d）' % (os.path.basename(path), label, n, expect))
    open(path, 'w', encoding='utf-8').write(txt.replace(old, new, 1))
    applied.append((os.path.basename(path), label, len(new) - len(old)))
    return True


OLD = '.kb-col-body { flex: 1; min-height: 0; overflow-y: auto; overflow-x: hidden; padding: 0 8px; display: flex; flex-direction: column; gap: 8px; }'
NEW = ('.kb-col-body { flex: 1; min-height: 0; overflow-y: auto; overflow-x: hidden; scrollbar-gutter: stable; '
       'padding: 0 8px; display: flex; flex-direction: column; gap: 8px; }')
MARK = 'scrollbar-gutter: stable;'

sub(PAGE, 'kb-col-body 预留滚动条槽位', OLD, NEW, MARK)

print('应用 %d 项 / 跳过 %d 项' % (len(applied), len(skipped)))
for p, l, d in applied:
    print('  + %s  %s  (%+d B)' % (p, l, d))
for p, l in skipped:
    print('  = %s  %s  (已存在)' % (p, l))

txt = open(PAGE, encoding='utf-8').read()
assert txt.count(MARK) == 1, '✗ scrollbar-gutter 应恰好 1 次，实为 %d' % txt.count(MARK)
assert txt.count('.kb-col-body {') == 1, '✗ .kb-col-body 基础规则应恰好 1 条'
print('自检 PASS：scrollbar-gutter × 1 / .kb-col-body 基础规则 × 1')
