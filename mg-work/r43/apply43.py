#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r43 · 任务详情页左栏「任务属性」两项微调
  1) 列表底部收口线贴合最后一行（原为 .td-side-dyn 的 border-top，隔了 24px 侧栏 gap）
     同时线色由 --color-border-2(#E5E5E5) 浅一级 → --color-border-1(#F2F2F2)
  2) 单行行高统一 32px（box-sizing:border-box + min-height，边框不再额外占高）
幂等：重复执行输出「已应用」。
"""
import sys, os, shutil

SRC = 'pages/task-detail.html'
BK = '/tmp/td-r43-backup.html'

s = open(SRC, encoding='utf-8').read()
first = not os.path.exists(BK)
if first:
    shutil.copy2(SRC, BK)

# ---------- 改动清单：(锚点, 替换) 只替换锚点正文，保留缩进 ----------
EDITS = [
    # 1. 行盒：显式 32px，边框含在盒内（原 padding:4.5px 0 → 高 30/26 不等）
    ('.td-side .td-attr .td-attr-row { padding: 4.5px 0; }',
     '.td-side .td-attr .td-attr-row { box-sizing: border-box; min-height: 32px; }'),
    # 2. 原首行去上内距（32px 盒高后不再需要）→ 改给 is-wrap 两行文本行留上下呼吸
    ('.td-side .td-attr .td-attr-row:first-child { padding-top: 0; }',
     '.td-side .td-attr .td-attr-row.is-wrap { padding: 6px 0; }'),
    # 3. 末行加收口线（取代 .td-side-dyn 的分段线，使其贴合最后一行）
    ('.td-side .td-attr .td-attr-row:last-child { padding-bottom: 0; }',
     '.td-side .td-attr .td-attr-row:last-child { border-bottom: 1px solid var(--color-border-1); }'),
    # 4. 行间线浅一级 #E5E5E5 → #F2F2F2
    ('.td-side .td-attr .td-attr-row + .td-attr-row { border-top: 1px solid var(--color-border-2); }',
     '.td-side .td-attr .td-attr-row + .td-attr-row { border-top: 1px solid var(--color-border-1); }'),
    # 5. 移除分段顶线（线已下移到列表末行；上下间距仍由 --td-side gap 24 + padding-top 24 承担）
    ('.td-side-dyn { border-top: 1px solid var(--td-line); padding-top: 24px; }',
     '.td-side-dyn { padding-top: 24px; }'),
]

applied, skipped = 0, 0
for old, new in EDITS:
    if new in s and old not in s:
        skipped += 1
        continue
    if s.count(old) != 1:
        print('!! 锚点不唯一或缺失 (%d): %r' % (s.count(old), old[:60])); sys.exit(1)
    s = s.replace(old, new, 1)
    applied += 1

if applied == 0:
    print('已应用（无改动，幂等）'); sys.exit(0)

open(SRC, 'w', encoding='utf-8').write(s)

# ---------- 自检 ----------
ok = True
new_bits = [
    'box-sizing: border-box; min-height: 32px;',
    '.td-side .td-attr .td-attr-row.is-wrap { padding: 6px 0; }',
    '.td-attr-row:last-child { border-bottom: 1px solid var(--color-border-1); }',
    '+ .td-attr-row { border-top: 1px solid var(--color-border-1); }',
    '.td-side-dyn { padding-top: 24px; }',
]
for b in new_bits:
    if b not in s:
        print('!! 新样式缺失:', b); ok = False
# 旧锚点残留检查（只查被替换掉的那几条，不做全文件关键字扫描：
#  `--color-border-2` / `--td-line` 在别处合法使用，如 .td-side-foot / .td-bar-sep）
for b in ['.td-side .td-attr .td-attr-row { padding: 4.5px 0; }',
          '.td-side .td-attr .td-attr-row:first-child { padding-top: 0; }',
          '.td-side .td-attr .td-attr-row:last-child { padding-bottom: 0; }',
          '.td-side .td-attr .td-attr-row + .td-attr-row { border-top: 1px solid var(--color-border-2); }',
          '.td-side-dyn { border-top: 1px solid var(--td-line); padding-top: 24px; }']:
    if b in s:
        print('!! 旧锚点残留:', b); ok = False
if s.count('<style') != s.count('</style>'):
    print('!! style 标签不配平'); ok = False
a = open(BK, encoding='utf-8').read()
for key in ('td-attr-row', 'td-sec-head', 'td-file', '<style', '</style>'):
    if s.count(key) != a.count(key):
        print('!! 结构漂移 %s: %d → %d' % (key, a.count(key), s.count(key))); ok = False
print(('OK · 应用 %d 项（跳过 %d 项）' % (applied, skipped)) if ok else 'FAILED')
sys.exit(0 if ok else 1)
