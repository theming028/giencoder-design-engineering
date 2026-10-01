# -*- coding: utf-8 -*-
import hashlib, io, os
R = r'E:/GienCoder/giencoder-design-engineering'

def info(p):
    raw = io.open(p, 'rb').read()
    n = raw.decode('utf-8')
    lf = n.replace('\r\n', '\n')
    return dict(bytes=len(raw), chars=len(lf), lines=lf.count('\n') + (0 if lf.endswith('\n') else 1),
                sha1_lf=hashlib.sha1(lf.encode('utf-8')).hexdigest()[:12])

for rel in ['pages/conversation.html', 'pages/task-detail.html', 'pages/base.html',
            'mg-work/r108/part108/_head.html', 'mg-work/r108/part108/_mods.html',
            'mg-work/r108/part108/panel.css', 'mg-work/r108/part108/panel.js',
            'mg-work/r108/part108/browse.html', 'mg-work/r108/acceptance.md']:
    p = os.path.join(R, rel)
    if not os.path.exists(p):
        print('MISS %s' % rel); continue
    d = info(p)
    print('%-44s bytes=%-9d chars=%-9d lines=%-6d sha1_lf=%s' % (rel, d['bytes'], d['chars'], d['lines'], d['sha1_lf']))

# panel.css 行数（LF 口径已含）
print()
print('acceptance 节标题计数：', end='')
t = io.open(os.path.join(R, 'mg-work/r108/acceptance.md'), 'rb').read().decode('utf-8').replace('\r\n', '\n')
import re
secs = re.findall(r'(?m)^## ([^\n]+)$', t)
print(len(secs))
print('  最后一个：', secs[-1] if secs else None)
