# -*- coding: utf-8 -*-
"""列出设计稿里每个 <img> 的宿主节点（id / name / 尺寸 / color）→ 便于分类「形状」与「图标」。"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = json.load(io.open(os.path.join(HERE, 'spec.json'), encoding='utf-8'))
sizes = {}
d = os.path.join(HERE, 'asset', 'icons')
for f in os.listdir(d):
    sizes[f] = os.path.getsize(os.path.join(d, f))

rows = []


def walk(n, path):
    for k in n['kids']:
        if k['tag'] == 'img':
            st = k['style']
            rows.append((path, os.path.basename(k['src'] or ''), st.get('width', ''), st.get('height', ''), st.get('color', '')))
        walk(k, path + '/' + (k['id'] or k['name'] or '?'))


walk(spec, '')
for r in rows:
    print('%-46s %-22s w=%-6s h=%-6s %-9s %6dB' % (r[0][-44:], r[1], r[2], r[3], r[4], sizes.get(r[1], 0)))
print('total %d imgs, %d bytes' % (len(rows), sum(sizes.get(r[1], 0) for r in rows)))
