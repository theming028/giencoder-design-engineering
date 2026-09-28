#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r44 · 两处修正
  A) pages/settings.html — 侧栏「返回」按钮文字色 text-3 → text-1（正文色，与同栏其它项一致）
  B) pages/base.html     — 左栏 aside 的「新会话」胶囊按钮宽度联动拖宽：
       · style width:240 → width:100%
       · 图标居中不再依赖硬编码 marginLeft:91 → 改由 flex 居中 + ⌘K 提示绝对定位
幂等：重复执行输出「已应用」。
"""
import sys, os, shutil, glob

BK = '/tmp/r44-backup'
os.makedirs(BK, exist_ok=True)

def patch(path, edits, name):
    s = open(path, encoding='utf-8').read()
    bkp = os.path.join(BK, name)
    if not os.path.exists(bkp):
        shutil.copy2(path, bkp)
    applied = skipped = 0
    for old, new, cnt in edits:
        if s.count(new) == cnt and s.count(old) == 0:
            skipped += 1
            continue
        if s.count(old) != cnt:
            print('!! [%s] 锚点数量异常 %d (期望 %d): %r' % (name, s.count(old), cnt, old[:70]))
            return False
        s = s.replace(old, new)
        applied += 1
    if applied:
        open(path, 'w', encoding='utf-8').write(s)
    print('  %-14s 应用 %d 项 / 跳过 %d 项' % (name, applied, skipped))
    return True

# ---------------- A) settings.html：返回按钮 ----------------
RET_OLD = 'flex w-fit items-center gap-1.5 rounded-md px-2 py-1 text-sm [color:var(--color-text-3)] hover:bg-black/[0.05] hover:[color:var(--color-text-1)]'
RET_NEW = 'flex w-fit items-center gap-1.5 rounded-md px-2 py-1 text-sm [color:var(--color-text-1)] hover:bg-black/[0.05]'
ok = patch('pages/settings.html', [(RET_OLD, RET_NEW, 2)], 'settings.html')

# ---------------- B) base.html：新会话按钮联动宽度 ----------------
NCBTN_OLD = 'className:`mb-2 new-chat-btn`,style:{width:240,height:32,'
NCBTN_NEW = 'className:`mb-2 new-chat-btn`,style:{width:`100%`,height:32,'

CSS_OLD = '.new-chat-btn{transition:background-color .15s ease}'
CSS_NEW = (
    '.new-chat-btn{transition:background-color .15s ease;position:relative;justify-content:center}'
    '.new-chat-btn>span:first-child{margin-left:0!important}'
    '.new-chat-btn>span:last-child{position:absolute;right:8px;top:50%;transform:translateY(-50%);margin:0!important}'
)

if ok:
    ok = patch('pages/base.html', [(NCBTN_OLD, NCBTN_NEW, 1), (CSS_OLD, CSS_NEW, 1)], 'base.html')

if not ok:
    sys.exit(1)

# ---------------- 自检 ----------------
bad = 0
s = open('pages/settings.html', encoding='utf-8').read()
if s.count(RET_NEW) != 2: print('!! settings 新串数量', s.count(RET_NEW)); bad += 1
if RET_OLD in s: print('!! settings 旧串残留'); bad += 1
a2 = open(os.path.join(BK, 'settings.html'), encoding='utf-8').read()
# text-3 在本页别处合法使用（右上角图标按钮等），只断言「恰好少 2 处」
if s.count('[color:var(--color-text-3)]') != a2.count('[color:var(--color-text-3)]') - 2:
    print('!! settings text-3 减少数量 ≠ 2：%d → %d'
          % (a2.count('[color:var(--color-text-3)]'), s.count('[color:var(--color-text-3)]'))); bad += 1

b = open('pages/base.html', encoding='utf-8').read()
a = open(os.path.join(BK, 'base.html'), encoding='utf-8').read()
if 'width:240' in b: print('!! base 仍有 width:240'); bad += 1
if b.count('width:`100%`,height:32') != 1: print('!! base 新 width 数量异常'); bad += 1
for frag in ['justify-content:center', '.new-chat-btn>span:first-child{margin-left:0!important}',
             '.new-chat-btn>span:last-child{position:absolute']:
    if frag not in b: print('!! base 缺少', frag); bad += 1
# new-chat-btn 词频 = 原 3（1 JSX + 2 CSS）+ 2（新增选择器）= 5
if b.count('new-chat-btn') != a.count('new-chat-btn') + 2:
    print('!! base new-chat-btn 词频异常: %d → %d' % (a.count('new-chat-btn'), b.count('new-chat-btn'))); bad += 1
# 真·结构标签计数（不含 CSS 词频）
for key in ['<style', '</style>', '<script', '</script>']:
    if b.count(key) != a.count(key):
        print('!! base 结构漂移 %s: %d → %d' % (key, a.count(key), b.count(key))); bad += 1
for key in ['<style', '</style>', '<script', '</script>', '返回']:
    if s.count(key) != a2.count(key):
        print('!! settings 结构漂移 %s: %d → %d' % (key, a2.count(key), s.count(key))); bad += 1

print('ALL OK' if not bad else 'FAILED')
sys.exit(0 if not bad else 1)
