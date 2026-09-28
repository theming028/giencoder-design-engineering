# -*- coding: utf-8 -*-
"""第 49 轮补丁 c：给树里的 folder-open / folder-closed / file 图标补上 class="td-bf-ico"
   （CSS 靠这个类给 16px 尺寸、flex:none 与前后间距；漏了类 → 图标会被 flex 压缩、间距丢失）
   只改这 3 类图标，页面上其它 <svg> 一律不动。幂等。"""
import re
import sys

F = 'pages/task-detail.html'
s = open(F, encoding='utf-8').read()
orig = len(s)

MARKERS = {
    'm6 14 1.45-2.9': 'folder-open',
    'M2 10h20': 'folder-closed',
    'M16 12H8': 'file',
}
hits = {'folder-open': 0, 'folder-closed': 0, 'file': 0}
other = 0


def fix(m):
    global other
    tag, body = m.group(0), m.group(0)
    inner = tag[tag.index('>') + 1:]
    kind = None
    for k, v in MARKERS.items():
        if k in inner:
            kind = v
            break
    if kind is None:
        other += 1
        return tag
    if 'class="td-bf-ico"' in tag:
        hits[kind] += 1
        return tag
    hits[kind] += 1
    return tag.replace('<svg ', '<svg class="td-bf-ico" ', 1)


s2 = re.sub(r'<svg[^>]*>[^\n]*?</svg>', fix, s)
assert s2.count('class="td-bf-ico"') == 28, 'td-bf-ico 数量 = %d（期望 28）' % s2.count('class="td-bf-ico"')
assert hits['folder-open'] == 4 and hits['folder-closed'] == 6 and hits['file'] == 18, hits
assert s2.count('<style') == 3 and s2.count('</style>') == 3
assert s2.count('</aside>') == s.count('</aside>')

open(F, 'w', encoding='utf-8').write(s2)
print('命中:', hits, ' 未处理 svg:', other)
print('OK  %d → %d 字节' % (orig, len(s2)))
