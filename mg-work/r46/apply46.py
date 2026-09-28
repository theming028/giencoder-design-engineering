#!/usr/bin/env python3
# 第 46 轮：task-detail 左栏 .td-side 的 gap 24px -> 0
import os, sys, shutil

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
F = os.path.join(ROOT, 'pages/task-detail.html')
BK = '/tmp/r46-backup'
os.makedirs(BK, exist_ok=True)
if not os.path.exists(os.path.join(BK, 'task-detail.html')):
    shutil.copy2(F, os.path.join(BK, 'task-detail.html'))

s = open(F, encoding='utf-8').read()

OLD = 'display: flex; flex-direction: column; gap: 24px;\n        border-left'
MARK = '第 46 轮：.td-side 区块间距归零'
NEW = ('display: flex; flex-direction: column; gap: 0;   /* ★ ' + MARK + ' */\n'
       '        border-left')

if MARK in s and OLD not in s:
    print('已应用（幂等跳过）')
else:
    if s.count(OLD) != 1:
        print('!! 锚点异常 x%d' % s.count(OLD)); sys.exit(1)
    s = s.replace(OLD, NEW, 1)
    open(F, 'w', encoding='utf-8').write(s)
    print('已应用')

# ---- 自检 ----
s = open(F, encoding='utf-8').read()
a = open(os.path.join(BK, 'task-detail.html'), encoding='utf-8').read()
ok = True
if s.count('gap: 24px;') != 0:
    print('!! gap: 24px 残留 x%d' % s.count('gap: 24px;')); ok = False
if s.count(MARK) != 1:
    print('!! 标记数量异常 x%d' % s.count(MARK)); ok = False
for k in ['<style', '</style>', '<script', '</script>', 'td-side-attr', 'td-side-dyn', 'td-side-foot']:
    if s.count(k) != a.count(k):
        print('!! 结构漂移 %s: %d -> %d' % (k, a.count(k), s.count(k))); ok = False
print('OK' if ok else 'FAIL')
sys.exit(0 if ok else 1)
