#!/usr/bin/env python3
# 第 46 轮（第 2 项）：9 页顶栏右侧 w-60 模块内的两颗按钮清空（保留模块容器）
import os, sys, shutil

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
PAGES = ['automation', 'avatar', 'base', 'dev', 'kanban', 'req-kanban',
         'settings', 'skills', 'task-detail']
KEY = 'flex w-60 items-center justify-end gap-1'
BK = '/tmp/r46-backup'
os.makedirs(BK, exist_ok=True)


def match_bracket(s, i):
    """从 s[i] == '[' 起做括号配平扫描（跳过反引号/引号字符串），返回配对 ']' 下标。"""
    depth = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in '`"\'':
            q = c
            i += 1
            while i < n:
                if s[i] == '\\':
                    i += 2
                    continue
                if s[i] == q:
                    i += 1
                    break
                i += 1
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


print('=== 处理 ===')
for name in PAGES:
    f = os.path.join(ROOT, 'pages', name + '.html')
    bkp = os.path.join(BK, name + '.html')
    if not os.path.exists(bkp):
        shutil.copy2(f, bkp)
    s = open(f, encoding='utf-8').read()
    ki = s.find(KEY)
    if ki < 0:
        print('%-14s !! 无模块锚点' % name); sys.exit(1)
    bi = s.find('children:[', ki)
    if bi < 0:
        print('%-14s !! 无 children 锚点' % name); sys.exit(1)
    oi = bi + len('children:')
    ci = match_bracket(s, oi)
    if ci < 0:
        print('%-14s !! 括号不配平' % name); sys.exit(1)
    inner = s[oi + 1:ci]
    if inner == '':
        print('%-14s 已是空容器（跳过）' % name)
        continue
    if '设置' not in inner or '当前用户' not in inner:
        print('%-14s !! 内部结构与预期不符：%r' % (name, inner[:140])); sys.exit(1)
    open(f, 'w', encoding='utf-8').write(s[:oi + 1] + s[ci:])
    print('%-14s 已清空（移除 %d 字节）' % (name, len(inner)))

print('=== 自检 ===')
ok = True
for name in PAGES:
    f = os.path.join(ROOT, 'pages', name + '.html')
    a = open(os.path.join(BK, name + '.html'), encoding='utf-8').read()
    s = open(f, encoding='utf-8').read()
    ki = s.find(KEY)
    oi = s.find('children:[', ki) + len('children:')
    ci = match_bracket(s, oi)
    if ci < 0:
        print('%-14s !! 括号不配平' % name); ok = False; continue
    if s[oi + 1:ci] != '':
        print('%-14s !! children 未清空' % name); ok = False
    for k in ['<style', '</style>', '<script', '</script>']:
        if s.count(k) != a.count(k):
            print('%-14s !! 结构漂移 %s %d->%d' % (name, k, a.count(k), s.count(k))); ok = False
print('OK' if ok else 'FAIL')
sys.exit(0 if ok else 1)
