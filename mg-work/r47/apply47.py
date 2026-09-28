#!/usr/bin/env python3
# 第 47 轮第 1 项：全局滚动条 —— 默认 0.08→0.16（对齐设计稿 rgba(0,0,0,0.16)）
#                              hover 0.12/0.28→0.24，active 0.16→0.32
import os, sys, shutil

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
BK = '/tmp/r47-backup'
os.makedirs(BK, exist_ok=True)

PAGES = ['automation', 'avatar', 'base', 'dev', 'kanban', 'req-kanban',
         'settings', 'skills', 'task-detail']

# 页面内联产物：用带前缀的窄锚点。（注意顺序见下方注释）
PAGE_SUBS = [
    ('scrollbar-thumb:active{background-color:rgba(var(--gray-10), .16)}',
     'scrollbar-thumb:active{background-color:rgba(var(--gray-10), .32)}'),
    ('scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .12)}',
     'scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .24)}'),
    ('scrollbar-thumb{background-color:rgba(var(--gray-10), .08)',
     'scrollbar-thumb{background-color:rgba(var(--gray-10), .16)'),
    ('scrollbar-color:rgba(var(--gray-10), .08) transparent',
     'scrollbar-color:rgba(var(--gray-10), .16) transparent'),
]

# DS 权威源：tokens 里的 3 档（先 0.16→0.32 避免与 0.08→0.16 串味）
DS_SUBS = [
    ('rgba(var(--gray-10), 0.16)', 'rgba(var(--gray-10), 0.32)'),
    ('rgba(var(--gray-10), 0.08)', 'rgba(var(--gray-10), 0.16)'),
    ('rgba(var(--gray-10), 0.12)', 'rgba(var(--gray-10), 0.24)'),
]
DS_FILES = ['giencoder-design-system/colors_and_type.css',
            'giencoder-design-system/gienx-templates/_shared/tokens.css']

# 手写那套：只把 hover 0.28 降到 0.24（默认已是 0.16）
HAND_SUBS = [
    ('--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.28);',
     '--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.24);'),
    ('scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.28); }',
     'scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.24); }'),
]

fail = 0


def apply(path, subs, label):
    global fail
    full = os.path.join(ROOT, path)
    bkp = os.path.join(BK, path.replace('/', '__'))
    if not os.path.exists(bkp):
        shutil.copy2(full, bkp)
    s = open(full, encoding='utf-8').read()
    orig = s
    hits = []
    for old, new in subs:
        n = s.count(old)
        if n == 0:
            hits.append('0')
            continue
        s = s.replace(old, new)
        hits.append(str(n))
    if s != orig:
        open(full, 'w', encoding='utf-8').write(s)
        print('%-46s 命中 %s  已写入' % (label, ','.join(hits)))
    else:
        print('%-46s 命中 %s  （无变化）' % (label, ','.join(hits)))
    return s


print('=== 页面（9 页内联产物）===')
for name in PAGES:
    apply('pages/%s.html' % name, PAGE_SUBS, 'pages/%s.html' % name)

print('=== DS 权威源 ===')
for f in DS_FILES:
    apply(f, DS_SUBS, f)

print('=== 手写那套（task-detail / avatar）===')
for name in ['task-detail', 'avatar']:
    apply('pages/%s.html' % name, HAND_SUBS, 'pages/%s.html [hand]' % name)

# ---- 自检：禁用「全文件关键词总数」类断言，只查被替换对象的残留 ----
print('=== 自检 ===')
ok = True
for name in PAGES:
    s = open(os.path.join(ROOT, 'pages', name + '.html'), encoding='utf-8').read()
    for bad in ['scrollbar-thumb{background-color:rgba(var(--gray-10), .08)',
                'scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .12)}',
                'scrollbar-thumb:active{background-color:rgba(var(--gray-10), .16)}',
                'scrollbar-color:rgba(var(--gray-10), .08) transparent']:
        if bad in s:
            print('  !! %s 残留 %s' % (name, bad[:60])); ok = False
    for want in ['scrollbar-thumb{background-color:rgba(var(--gray-10), .16)',
                 'scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .24)}',
                 'scrollbar-thumb:active{background-color:rgba(var(--gray-10), .32)}',
                 'scrollbar-color:rgba(var(--gray-10), .16) transparent']:
        if want not in s:
            print('  !! %s 缺少 %s' % (name, want[:60])); ok = False
    a = open(os.path.join(BK, 'pages__' + name + '.html'), encoding='utf-8').read()
    for tag in ['<style', '</style>', '<script', '</script>']:
        if s.count(tag) != a.count(tag):
            print('  !! %s 结构漂移 %s %d->%d' % (name, tag, a.count(tag), s.count(tag))); ok = False

for f in DS_FILES:
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    if 'rgba(var(--gray-10), 0.08)' in s or 'rgba(var(--gray-10), 0.12)' in s:
        print('  !! %s 仍有旧值' % f); ok = False
    if s.count('rgba(var(--gray-10), 0.16)') != 2 or s.count('rgba(var(--gray-10), 0.24)') != 1 \
            or s.count('rgba(var(--gray-10), 0.32)') != 1:
        print('  !! %s 三档分布异常 16x%d 24x%d 32x%d' % (
            f, s.count('rgba(var(--gray-10), 0.16)'),
            s.count('rgba(var(--gray-10), 0.24)'),
            s.count('rgba(var(--gray-10), 0.32)'))); ok = False

for name, key in [('task-detail', '--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.28);'),
                  ('avatar', 'scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.28); }')]:
    s = open(os.path.join(ROOT, 'pages', name + '.html'), encoding='utf-8').read()
    if key in s:
        print('  !! %s 手写 hover 未更新' % name); ok = False

print('OK' if ok else 'FAIL')
sys.exit(0 if ok else 1)
