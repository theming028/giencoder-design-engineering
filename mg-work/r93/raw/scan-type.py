# -*- coding: utf-8 -*-
"""从设计稿导出 HTML 里统计全部文字样式，建立字号地图。"""
import io, re, collections, sys

S = io.open('design-1393-18748.html', encoding='utf-8').read()

print('=== 1. font-size 全局分布 ===')
c = collections.Counter(re.findall(r'font-size:\s*(\d+)px', S))
for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0])):
    print('   fs=%-4s : %d' % (k, v))

print('=== 2. line-height 全局分布 ===')
c = collections.Counter(re.findall(r'line-height:\s*(\d+)px', S))
for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0])):
    print('   lh=%-4s : %d' % (k, v))

print('=== 3. (fs,lh,weight) 组合 ===')
c = collections.Counter()
for m in re.finditer(r'<span([^>]*)>', S):
    blob = m.group(1)
    fs = re.search(r'font-size:\s*(\d+)px', blob)
    lh = re.search(r'line-height:\s*(\d+)px', blob)
    w = re.search(r'font-weight:\s*(\w+)', blob)
    if fs:
        c[(fs.group(1), lh.group(1) if lh else '-', w.group(1) if w else '-')] += 1
for k, v in sorted(c.items(), key=lambda x: (-x[1])):
    print('   %3d  fs=%-4s lh=%-4s w=%s' % (v, k[0], k[1], k[2]))

print('=== 4. 每个顶层块内 span 的文字样式（按块） ===')
# 顶层块：data-node-id + data-name，style 带 position:absolute
blocks = []
for m in re.finditer(r'data-node-id="(\d+:\d+)"\s*\n?\s*data-name="([^"]*)"\s*\n?\s*style="([^"]*position: absolute[^"]*)"', S):
    blocks.append((m.start(), m.group(1), m.group(2), m.group(3)))
# 只取 left:164px（内容列）的块作为分节
tops = []
for i, (pos, nid, name, st) in enumerate(blocks):
    if 'left: 164px' in st:
        tops.append((pos, nid, name, st))
for i, (pos, nid, name, st) in enumerate(tops):
    end = tops[i + 1][0] if i + 1 < len(tops) else len(S)
    seg = S[pos:end]
    h = re.search(r'height:\s*(\d+)px', st)
    t = re.search(r'top:\s*(\d+)px', st)
    styles = collections.Counter()
    for m in re.finditer(r'<span([^>]*)>', seg):
        blob = m.group(1)
        fs = re.search(r'font-size:\s*(\d+)px', blob)
        lh = re.search(r'line-height:\s*(\d+)px', blob)
        if fs:
            styles['%s/%s' % (fs.group(1), lh.group(1) if lh else '-')] += 1
    ui = collections.Counter()
    for m in re.finditer(r'<ui-component([^>]*)>', seg):
        blob = m.group(1)
        hh = re.search(r'height:\s*(\d+)px', blob)
        ww = re.search(r'width:\s*(\d+)px', blob)
        if hh:
            ui['%sx%s' % (ww.group(1) if ww else '?', hh.group(1))] += 1
    print('  [%s %s] top=%s h=%s' % (nid, name, t.group(1) if t else '?', h.group(1) if h else '?'))
    print('      span样式: %s' % dict(styles))
    if ui:
        print('      ui-component框: %s' % dict(ui))
