#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r41 · 任务详情页 3 项调整
1) .td-attr-k 文字色加深一级：--td-meta(text-3) → --color-text-2
2) .td-attr 列表加间隔线（gap 归零 + 行内 padding 承担行距 + 1px 行间细线，pitch 保持 30px）
3) .td-composer（右栏 AI 输入框）总高 154 → 128px：输入区 min-height 96 → 70
幂等：已应用则跳过；自检：替换次数 + 结构计数 + style 花括号配平。
"""
import re, shutil, sys, os

P = 'pages/task-detail.html'
BAK = '/tmp/td-r41-backup.html'

A_OLD = '.td-attr-k { flex: none; color: var(--td-meta); }'
A_NEW = '.td-attr-k { flex: none; color: var(--color-text-2); }'

B_OLD = '      .td-side .td-attr { gap: 10px; }\n      .td-side .td-attr-k { width: 64px; }\n'
B_NEW = ('      .td-side .td-attr { gap: 10px; }\n'
         '      .td-side .td-attr-k { width: 64px; }\n'
         '      /* ★ 第 41 轮：属性列表加间隔线。gap 归零，行距改由行内上下 padding（4.5+4.5=9）\n'
         '         + 行间 1px 细线共同承担 → pitch = 20(行高) + 9 + 1 = 30px，与原先「行高20 + gap10」\n'
         '         完全一致，整体高度与值列起点均不变。仅作用于左栏 .td-side 下的 .td-attr。 */\n'
         '      .td-side .td-attr { gap: 0; }\n'
         '      .td-side .td-attr .td-attr-row { padding: 4.5px 0; }\n'
         '      .td-side .td-attr .td-attr-row:first-child { padding-top: 0; }\n'
         '      .td-side .td-attr .td-attr-row:last-child { padding-bottom: 0; }\n'
         '      .td-side .td-attr .td-attr-row + .td-attr-row { border-top: 1px solid var(--td-hairline); }\n')

C_OLD = '.td-composer .min-h-\\[96px\\] { min-height: 96px; }'
C_NEW = ('/* ★ 第 41 轮：输入区 96 → 70，使 .td-composer 总高 = 70 + 34(工具条) + 12x2(padding) '
         '+ 1x2(边框) = 128px（原 154px）。只压输入区空白，工具条/圆角/外边距不动。 */\n'
         '      .td-composer .min-h-\\[96px\\] { min-height: 70px; }')

s = open(P, encoding='utf-8').read()
orig = s
before = {'attr_row': s.count('td-attr-row'), 'sec_head': s.count('td-sec-head'),
          'file': s.count('td-file'), 'style': s.count('<style'), 'est': s.count('</style>')}

if A_NEW in s and 'min-height: 70px' in s and '第 41 轮：属性列表加间隔线' in s:
    print('ALREADY APPLIED'); sys.exit(0)

if not os.path.exists(BAK):
    shutil.copy2(P, BAK)
    print('backup ->', BAK)

fails = []

def sub(old, new, tag):
    global s
    n = s.count(old)
    if n != 1:
        fails.append(f'{tag}: expected 1 occurrence, got {n}')
        return
    s = s.replace(old, new, 1)
    print(f'{tag}: replaced 1')

sub(A_OLD, A_NEW, 'A td-attr-k 配色')
sub(B_OLD, B_NEW, 'B 间隔线')
sub(C_OLD, C_NEW, 'C 输入区高度')

if fails:
    print('SELF-CHECK FAILED:', fails); sys.exit(1)

after = {'attr_row': s.count('td-attr-row'), 'sec_head': s.count('td-sec-head'),
         'file': s.count('td-file'), 'style': s.count('<style'), 'est': s.count('</style>')}
# 新增 CSS 自身含 5 处 td-attr-row 文本，属预期增量；DOM/结构标记必须零漂移
expect = dict(before); expect['attr_row'] = before['attr_row'] + 5
if after != expect:
    print('SELF-CHECK FAILED: structure drift', before, after, 'expect', expect); sys.exit(1)

# style 块花括号配平
blocks = re.findall(r'<style[^>]*>(.*?)</style>', s, re.S)
for i, b in enumerate(blocks):
    if b.count('{') != b.count('}'):
        print(f'SELF-CHECK FAILED: style#{i} brace mismatch {b.count("{")}/{b.count("}")}'); sys.exit(1)

# 幂等断言
for needle in [A_NEW, 'gap: 0;', 'border-top: 1px solid var(--td-hairline);', 'min-height: 70px;']:
    if needle not in s:
        print('SELF-CHECK FAILED: missing', needle); sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print(f'OK  {len(orig)} -> {len(s)} bytes (+{len(s)-len(orig)})')
print('   before:', before, '\n   after :', after)
