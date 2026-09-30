# -*- coding: utf-8 -*-
"""把 MasterGo 导出的设计稿 DOM 解析成规格 JSON（r93 会话详情 1393:18748）。

产物 mg-work/r93/raw/spec.json：
  { id, tag, name, style:{...}, props:{...}, text:'...', kids:[...] }
以及 mg-work/r93/raw/icons.txt：节点 id → svg 文件名（只列 <img>）。
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'design-1393-18748.html')

raw = io.open(SRC, encoding='utf-8').read()
i = raw.find('代码内容：')
body = raw[i:]

TAG_RE = re.compile(r'<(/?)([a-zA-Z][\w-]*)((?:\s+[\w:-]+="[^"]*")*)\s*(/?)>')
ATTR_RE = re.compile(r'([\w:-]+)="([^"]*)"')


def parse_style(s):
    d = {}
    for part in s.split(';'):
        part = part.strip()
        if not part or ':' not in part:
            continue
        k, v = part.split(':', 1)
        d[k.strip()] = v.strip()
    return d


def parse_text(t):
    if not t:
        return None
    try:
        d = json.loads(t)
    except Exception:
        return t
    vals = [v for v in d.values() if v]
    return vals[0] if vals else None


stack = []
root = None
icons = {}
for m in TAG_RE.finditer(body):
    closing, tag, attrs_s, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
    if tag in ('br',):
        continue
    attrs = dict(ATTR_RE.findall(attrs_s))
    if closing:
        if stack and stack[-1]['tag'] == tag:
            stack.pop()
        continue
    node = {
        'id': attrs.get('data-node-id'),
        'tag': tag,
        'name': attrs.get('data-name'),
        'style': parse_style(attrs.get('style', '')),
        'props': attrs.get('props'),
        'text': parse_text(attrs.get('text')),
        'src': attrs.get('src'),
        'kids': [],
    }
    if stack:
        stack[-1]['kids'].append(node)
    else:
        root = node
    if node['src']:
        icons[node['id'] or ('__img_%d' % len(icons))] = node['src']
    if not (selfclose or tag in ('img', 'input', 'ui-component')):
        stack.append(node)

json.dump(root, io.open(os.path.join(HERE, 'spec.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
with io.open(os.path.join(HERE, 'icons.txt'), 'w', encoding='utf-8') as f:
    for k, v in icons.items():
        f.write('%s\t%s\n' % (k, os.path.basename(v)))
print('nodes ok, icons=%d' % len(icons))
