# -*- coding: utf-8 -*-
import io, re, sys
s = io.open('mg-work/r93/raw/design-1393-18748.html', encoding='utf-8').read()
TOK = re.compile(r'<(/?)(div|ui-component|span|img|p|svg|text)\b([^>]*?)(/?)>', re.S)
stack = []
nodes = {}
for m in TOK.finditer(s):
    close, tag, attrs, selfc = m.group(1), m.group(2), m.group(3), m.group(4)
    if close:
        for i in range(len(stack) - 1, -1, -1):
            if stack[i]['tag'] == tag:
                del stack[i:]
                break
        continue
    nid = re.search(r'data-node-id="([^"]*)"', attrs)
    nm = re.search(r'data-name="([^"]*)"', attrs)
    st = re.search(r'style="([^"]*)"', attrs)
    left = top = None
    if st:
        l = re.search(r'left:/s*(-?[/d.]+)px', st.group(1))
        t = re.search(r'top:/s*(-?[/d.]+)px', st.group(1))
        w = re.search(r'width:/s*(-?[/d.]+)px', st.group(1))
        h = re.search(r'height:/s*(-?[/d.]+)px', st.group(1))
        left = float(l.group(1)) if l else None
        top = float(t.group(1)) if t else None
        width = float(w.group(1)) if w else None
        height = float(h.group(1)) if h else None
    else:
        width = height = None
    node = {'tag': tag, 'id': nid.group(1) if nid else None, 'name': nm.group(1) if nm else None,
            'left': left, 'top': top, 'w': width, 'h': height, 'parent': stack[-1] if stack else None}
    if node['id']:
        nodes[node['id']] = node
    if selfc or tag in ('img',):
        continue
    stack.append(node)

def absrect(nid):
    n = nodes.get(nid)
    if not n:
        return None
    L = T = 0.0
    chain = []
    cur = n
    while cur:
        chain.append(cur)
        if cur['left'] is not None: L += cur['left']
        if cur['top'] is not None: T += cur['top']
        cur = cur['parent']
    return L, T, n['w'], n['h'], n['name'], [c['id'] + '/' + str(c['name']) for c in chain]

for nid in sys.argv[1:]:
    print(nid, absrect(nid))
