#!/usr/bin/env python3
# 第 47 轮第 2 项收尾：字号走 token；代码语法色收进局部变量（DS 无对应语义 token）
import os, re, sys, shutil

F = '/Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html'
BK = '/tmp/r47-backup'
os.makedirs(BK, exist_ok=True)
if not os.path.exists(os.path.join(BK, 'td-r47-b2c.html')):
    shutil.copy2(F, os.path.join(BK, 'td-r47-b2c.html'))

s = open(F, encoding='utf-8').read()
SUBS = [
    # 1) 硬编码字号 → token（--font-size-body-1 = 12px）
    ('font-size: 12px; font-weight: 500;',
     'font-size: var(--font-size-body-1); font-weight: 500;'),
    ('padding: 0 16px; font-size: 12px; color: var(--color-text-2);',
     'padding: 0 16px; font-size: var(--font-size-body-1); color: var(--color-text-2);'),
    ('font-size: 12px; line-height: 20px;',
     'font-size: var(--font-size-body-1); line-height: 20px;'),
    # 2) 语法色 → 局部变量（值仍取自设计稿实测的 VSCode Light 配色）
    ('background: var(--color-bg-1); border-radius: 8px; box-shadow: var(--td-panel-shadow);\n      }\n      .td-root.is-browse .td-left',
     'background: var(--color-bg-1); border-radius: 8px; box-shadow: var(--td-panel-shadow);\n'
     '        /* 代码语法配色：取设计稿实测值（VSCode Light 系），DS 暂无对应语义 token */\n'
     '        --td-code-key: #0451A5; --td-code-str: #A31515; --td-code-num: #098658;\n'
     '      }\n      .td-root.is-browse .td-left'),
    ('.td-code-k { color: #0451A5; }', '.td-code-k { color: var(--td-code-key); }'),
    ('.td-code-s { color: #A31515; }', '.td-code-s { color: var(--td-code-str); }'),
    ('.td-code-n { color: #098658; }', '.td-code-n { color: var(--td-code-num); }'),
]

hits = []
for old, new in SUBS:
    if new in s and old not in s:
        hits.append('idem'); continue
    n = s.count(old)
    hits.append(str(n))
    if n != 1:
        print('!! 锚点异常 x%d: %r' % (n, old[:70])); sys.exit(1)
    s = s.replace(old, new, 1)

open(F, 'w', encoding='utf-8').write(s)
print('命中:', ','.join(hits))

s = open(F, encoding='utf-8').read()
ok = True
# ⚠️ 自检只锚定本轮新增的 .td-browse 区块，禁止"全文件关键词计数"式断言。
#    事实：HEAD 基线里本就有 2 处 `font-size: 12px`（.td-dp-t2 / .td-dp-none .giencoder-empty-description，
#    属 r41 下拉弹层规则，非本轮范围 → 不得擅自改动），全文件断言必然误报。
_b0 = s.find('/* ★ 第 47 轮第 2 项')
_b1 = s.find('.td-chat {', _b0)
blk = s[_b0:_b1] if 0 <= _b0 < _b1 else ''
if not blk:
    print('!! 未能切出本轮新增的 .td-browse 区块'); ok = False
else:
    if 'font-size: 12px' in blk:
        print('!! 新增区块内仍有硬编码字号 12px'); ok = False
    if re.search(r'color:\s*#[0-9A-Fa-f]{6}', blk):
        print('!! 新增区块内仍有硬编码色值直接用于 color'); ok = False
    if blk.count('--td-code-key: #0451A5') != 1:
        print('!! 语法色变量定义缺失'); ok = False
    if blk.count('var(--font-size-body-') < 6:
        print('!! 字号 token 未按预期换入'); ok = False
    print('新增区块长度 %d / 硬编码 12px %d' % (len(blk), blk.count('font-size: 12px')))
if s.count('color: var(--td-code-key)') != 1 or s.count('color: var(--td-code-str)') != 1 \
        or s.count('color: var(--td-code-num)') != 1:
    print('!! 语法色变量未生效'); ok = False
if s.count('--td-code-key: #0451A5') != 1:
    print('!! 变量定义缺失'); ok = False
a = open(os.path.join(BK, 'td-r47-b2c.html'), encoding='utf-8').read()
for k in ['<style', '</style>', '<script', '</script>']:
    if s.count(k) != a.count(k):
        print('!! 结构漂移 %s' % k); ok = False
print('OK' if ok else 'FAIL')
sys.exit(0 if ok else 1)
