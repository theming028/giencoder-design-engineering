# -*- coding: utf-8 -*-
"""全站 ZCode 出现处 + 上下文（排除 node_modules/.git/mg-work）。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

hits = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames
                   if d not in ('node_modules', '.git', '.workbuddy', 'mg-work')]
    for fn in filenames:
        fp = os.path.join(dirpath, fn)
        try:
            s = io.open(fp, encoding='utf-8').read()
        except Exception:
            continue
        for m in re.finditer(r'ZCode', s):
            a = max(0, m.start() - 150)
            b = min(len(s), m.end() + 150)
            hits.append((os.path.relpath(fp, ROOT), m.start(), s[a:b]))

print('总计 ZCode 出现次数 =', len(hits))
print()
for fp, pos, ctx in hits:
    print('--- %s @%d ---' % (fp, pos))
    print(repr(ctx))
    print()
