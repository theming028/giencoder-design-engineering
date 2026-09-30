# -*- coding: utf-8 -*-
"""verify-design 全量输出归一化比对（v2）：
只抓『带 tag 的问题标题行』，抹掉 行号 / 上级目录前缀，再做集合比对。
标题行特征：含 '[' 与 ']' 且在 HTML 文件名之后带 ':行号'。"""
import re, io, collections, sys

RE_LN = re.compile(r'([A-Za-z0-9_.-]+\.html):\d+')
RE_DIR = re.compile(r'(?:\./)?(?:mg-work/r87/gate/base/)?pages[\\/]')
RE_TAG = re.compile(r'^\s*[│|]?\s*[🟡🔵🔴]\s*\[([A-Z0-9-]+)\]\s*(.+)$')

def norm(path):
    c = collections.Counter()
    for ln in io.open(path, encoding='utf-8'):
        m = RE_TAG.match(ln.rstrip())
        if not m:
            continue
        tag, body = m.group(1), m.group(2)
        body = RE_DIR.sub('', body).strip()
        body = RE_LN.sub(lambda x: x.group(1) + ':*', body)
        c['[%s] %s' % (tag, body)] += 1
    return c

a = norm(sys.argv[1]); b = norm(sys.argv[2])
print('HEAD %d 条 / NOW %d 条' % (sum(a.values()), sum(b.values())))
d1 = sorted((a - b).elements()); d2 = sorted((b - a).elements())
print('--- 只在 HEAD（被消除）---'); [print('  - ' + x) for x in d1] or print('  (无)')
print('--- 只在 NOW（新增）---');  [print('  + ' + x) for x in d2] or print('  (无)')
print('--- 计数变化 ---')
ch = False
for k in sorted(set(a) | set(b)):
    if a[k] != b[k]:
        ch = True; print('  ~ %s  %d -> %d' % (k, a[k], b[k]))
if not ch: print('  (无)')
