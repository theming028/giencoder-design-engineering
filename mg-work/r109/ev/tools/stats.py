# -*- coding: utf-8 -*-
import hashlib, io, re, os

def rd(p):
    return io.open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')

FILES = ['mg-work/r109/part109/_head.html', 'mg-work/r109/part109/_mods.html',
         'mg-work/r109/part109/panel.css', 'mg-work/r109/part109/panel.js',
         'mg-work/r109/part109/browse.html', 'mg-work/r109/ev/patch109l1.py',
         'mg-work/r109/ev/patch109l2.py', 'mg-work/r109/ev/make109.py',
         'mg-work/r109/apply109.py', 'pages/conversation.html', 'pages/base.html']
for p in FILES:
    s = rd(p)
    print('%-40s %8d chars %6d lines' % (p, len(s), s.count('\n') + 1))
s = rd('pages/conversation.html')
print('conversation.html md5 =', hashlib.md5(s.encode('utf-8')).hexdigest())
print('conversation.html UTF-8 bytes(LF) =', len(s.encode('utf-8')))
print('base.html md5 =', hashlib.md5(rd('pages/base.html').encode('utf-8')).hexdigest())
c = rd('mg-work/r109/part109/panel.css')
j = rd('mg-work/r109/part109/panel.js')
for k in ['r107-l1', 'r108-l', 'r109-l1', 'r109-l2']:
    print('  标记 %-9s css=%d js=%d' % (k, len(re.findall(re.escape(k), c)), len(re.findall(re.escape(k), j))))
print('acceptance.md =', len(rd('mg-work/r109/acceptance.md')))
print('raw 新增 =', sorted(f for f in os.listdir('mg-work/r109/raw') if f.startswith(('f-', 'g-', 'd2-', 'e2-', 'cmp-regen-l2', 'l2-'))))
