# -*- coding: utf-8 -*-
"""把设计稿 spec.json 展平成绝对坐标表：色块矩形 + 文本节点 + 结构层次。"""
import io, json, sys

D = json.load(io.open('spec.json', encoding='utf-8'))


def px(v):
    if v is None:
        return 0.0
    s = str(v).replace('px', '').strip()
    try:
        return float(s)
    except Exception:
        return 0.0


rows = []


def walk(k, ax, ay, depth, path):
    st = k.get('style') or {}
    x = ax + px(st.get('left'))
    y = ay + px(st.get('top'))
    w = px(st.get('width'))
    h = px(st.get('height'))
    bg = st.get('background') or st.get('backgroundColor') or ''
    bd = st.get('border') or st.get('borderColor') or ''
    if w and h:
        rows.append((y, x, w, h, k['id'], k['name'], bg, bd, depth, k.get('text')))
    for c in (k.get('kids') or []):
        walk(c, x, y, depth + 1, path + '/' + k['id'])


for c in D['kids']:
    walk(c, 0, 0, 0, '')

# 只看内容列（x>=164）的、宽>=300 的块，按 y 排序
print('=== 内容列主要块（w>=300, x>=160）===')
for (y, x, w, h, nid, name, bg, bd, depth, text) in sorted(rows):
    if x >= 160 and w >= 300:
        t = ('  TEXT=' + repr(text)[:60]) if text else ''
        print('T%-6s H%-6s L%-6s W%-6s %-14s %-16s bg=%-22s bd=%-16s%s'
              % (y, h, x, w, nid, name, bg, bd, t))

print()
print('=== 全部文本节点（按 y）===')
for (y, x, w, h, nid, name, bg, bd, depth, text) in sorted(rows):
    if text:
        print('T%-6s L%-6s H%-5s %-14s %-18s %s' % (y, x, h, nid, name, repr(text)[:80]))
