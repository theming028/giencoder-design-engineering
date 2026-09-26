# -*- coding: utf-8 -*-
"""r15 补丁 C：上传区回落到设计系统契约。

问题（实测 D 步骤发现）：
 1) 契约 upload.json 的 anatomy 明确规定 `remove-icon` 的 element 是 **svg**，
    而当前删除按钮是 `rm.textContent = 'x'`（字母 x），既非图标、也污染了文件名的
    文本读取（实测读到 "需求文档.mdx"）。
 2) 使用了 DS 中并不存在的虚构类名：giencoder-upload / -tip / -list / -remove /
    -file-name。DS 的 components.css 只提供 .giencoder-upload-trigger /
    .giencoder-upload-drag-trigger / .giencoder-upload-list-item 三个类。
 3) .kb-crt-upitem 把列表项高度写成 28px，覆盖了 DS 契约的 36px；设计稿未给出
    文件列表样式，应回落到契约值。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'pages', 'kanban.html')
s = open(P, 'rb').read()
before = len(s)

RM_SVG = ('<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
          'stroke-width="1.2" stroke-linecap="round"><path d="M3 3l6 6M9 3l-6 6"/></svg>')

PATCHES = [
    # --- HTML：去掉虚构契约类 ---
    (r'class=\"giencoder-upload kb-crt-upload\"',
     r'class=\"kb-crt-upload\"',
     'HTML 移除虚构类 giencoder-upload'),
    (r'class=\"giencoder-upload-tip kb-crt-uptip\"',
     r'class=\"kb-crt-uptip\"',
     'HTML 移除虚构类 giencoder-upload-tip'),
    (r'class=\"giencoder-upload-list kb-crt-uplist\"',
     r'class=\"kb-crt-uplist\"',
     'HTML 移除虚构类 giencoder-upload-list'),
    # --- HTML：触发按钮补上契约里真实存在的 trigger 类 ---
    (r'class=\"giencoder-btn giencoder-btn-size-default kb-crt-upbtn\"',
     r'class=\"giencoder-btn giencoder-btn-size-default giencoder-upload-trigger kb-crt-upbtn\"',
     'HTML 触发按钮补 giencoder-upload-trigger（契约 trigger part）'),
    # --- JS：文件名 span 用适配层类 ---
    ("nm.className = 'giencoder-upload-file-name';",
     "nm.className = 'kb-crt-upname';",
     'JS 移除虚构类 giencoder-upload-file-name'),
    # --- JS：删除按钮用适配层类 + SVG 图标（契约 remove-icon element=svg） ---
    ("rm.className = 'giencoder-upload-remove kb-crt-uprm';",
     "rm.className = 'kb-crt-uprm';",
     'JS 移除虚构类 giencoder-upload-remove'),
    ("rm.textContent = 'x';",
     "rm.innerHTML = '%s';" % RM_SVG,
     'JS 删除按钮 x 文本 -> SVG 图标'),
    # --- CSS：列表项高度回落 DS 契约 36px ---
    ('.kb-crt-upitem { display: flex; align-items: center; gap: 8px; height: 28px; font-size: var(--font-size-body-1); color: var(--color-text-2); }',
     '.kb-crt-upitem { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-1); color: var(--color-text-2); }\n'
     '      .kb-crt-upname { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }',
     'CSS 列表项高度回落契约 36px + 新增文件名适配类'),
    # --- CSS：删除按钮改为图标容器 ---
    ('.kb-crt-uprm { border: none; background: none; cursor: pointer; color: var(--color-text-3); padding: 0; line-height: 0; }',
     '.kb-crt-uprm { display: inline-flex; align-items: center; justify-content: center; width: 16px; height: 16px; flex: none; border: none; background: none; cursor: pointer; color: var(--color-text-3); padding: 0; line-height: 0; }',
     'CSS 删除按钮改 16x16 图标容器'),
]

for old, new, why in PATCHES:
    ob = old.encode('utf-8')
    n = s.count(ob)
    if n != 1:
        print('[ABORT] 锚点命中 %d 次（应为 1）：%s' % (n, why))
        print('        anchor=%r' % old[:80])
        sys.exit(1)
    s = s.replace(ob, new.encode('utf-8'))
    print('[OK] %s' % why)

open(P, 'wb').write(s)
print('\n%s  %d -> %d chars' % (os.path.basename(P), before, len(s)))

# 残留虚构类自检
for bad in [b'giencoder-upload-remove', b'giencoder-upload-file-name',
            b'giencoder-upload-tip', b'giencoder-upload-list"', b'giencoder-upload kb-']:
    if bad in s:
        print('[WARN] 仍残留: %s' % bad.decode())
print('虚构类名自检完成')
