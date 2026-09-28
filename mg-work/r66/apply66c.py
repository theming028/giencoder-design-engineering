#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r66c：蒙层全局统一 —— 补最后一处漏网 task-detail.html 的 .kb-crt-mask

r66 审计结论（全站 13 处 mask 规则）：
  12 处已统一为  var(--color-mask-bg)  +  backdrop-filter: blur(10px) saturate(100%)
  漏 1 处：task-detail.html 的 .kb-crt-mask（页内嵌的看板「创建任务」弹窗）
          现状 --kb-crt-mask: rgba(0,0,0,.32) + blur(5px) → 与全局口径不一致。

注：kanban.html 的 .kb-crt-mask 已在 r66 同步过（var(--color-mask-bg) + blur(10px)），
    task-detail 里这一份是同一套令牌的副本，当时未覆盖到。
（avatar/task-detail 里另有 .td-add-pop 的 blur(20px)：那是毛玻璃浮层，不是蒙层，不动。）
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = os.path.join(ROOT, 'pages', 'task-detail.html')

applied, skipped = [], []


def sub(label, old, new, newmark, expect=1):
    txt = open(PAGE, encoding='utf-8').read()
    if newmark and newmark in txt:
        skipped.append(label)
        return False
    n = txt.count(old)
    if n != expect:
        sys.exit('✗ %s 锚点命中 %d 次（期望 %d）' % (label, n, expect))
    open(PAGE, 'w', encoding='utf-8').write(txt.replace(old, new, 1))
    applied.append((label, len(new) - len(old)))
    return True


# ── 1. 令牌改走全局口径 ────────────────────────────────────────────────
OLD_TOK = ('        --kb-crt-mask: rgba(0, 0, 0, 0.32);'
           '   /* 遮罩：svg_8e860390（#000 32% + backdrop blur 5px） */')
NEW_TOK = ('        --kb-crt-mask: var(--color-mask-bg);'
           '   /* ★ 第 66 轮：并入全局统一蒙层口径（= #000 40%） */')
sub('crt 令牌并入全局', OLD_TOK, NEW_TOK, '并入全局统一蒙层口径')

# ── 2. 模糊 5px → 10px，与全局 .giencoder-modal-mask 同档 ─────────────
OLD_BLUR = ('      .kb-crt-mask {\n'
            '        position: absolute; inset: 0; background: var(--kb-crt-mask);\n'
            '        -webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);\n')
NEW_BLUR = ('      /* ★ 第 66 轮：与 .giencoder-modal-mask 同口径（blur 5px → 10px，令牌并入 --color-mask-bg） */\n'
            '      .kb-crt-mask {\n'
            '        position: absolute; inset: 0; background: var(--kb-crt-mask);\n'
            '        -webkit-backdrop-filter: blur(10px) saturate(100%); backdrop-filter: blur(10px) saturate(100%);\n')
sub('crt 模糊 5px→10px', OLD_BLUR, NEW_BLUR, '与 .giencoder-modal-mask 同口径（blur 5px → 10px')

print('应用 %d 项 / 跳过 %d 项' % (len(applied), len(skipped)))
for l, d in applied:
    print('  + %s  (%+d B)' % (l, d))
for l in skipped:
    print('  = %s  (已存在)' % l)

# ── 自检（只断言被改对象）─────────────────────────────────────────────
txt = open(PAGE, encoding='utf-8').read()
assert txt.count('blur(5px)') == 0, '✗ 仍残留 blur(5px) × %d' % txt.count('blur(5px)')
assert txt.count('--kb-crt-mask: var(--color-mask-bg);') == 1, '✗ crt 令牌未并入全局'
assert txt.count('rgba(0, 0, 0, 0.32)') == 0, '✗ 旧罩色值仍残留'
assert txt.count('.kb-crt-mask {\n') == 1, '✗ .kb-crt-mask 规则应恰好 1 条'
print('自检 PASS：blur(5px)×0 / rgba(0,0,0,.32)×0 / crt 令牌并入全局×1 / .kb-crt-mask 规则×1')
