# -*- coding: utf-8 -*-
"""改前(r86) vs 改后(r87) 同口径对照：select 触发框的 圆角/ring/宽度/高度/截断。"""
import json, io, os

PAIRS = [('settings', 'g_settings'), ('kanban', 'g_kanban'), ('req-kanban', 'g_req-kanban'),
         ('task-detail', 'g_task-detail'), ('avatar', 'g_avatar')]
D = 'mg-work/r87/ev'


def load(f):
    return json.loads(json.loads(io.open(os.path.join(D, f), encoding='utf-8').read().strip()))


for page, stem in PAIRS:
    try:
        bef = load(stem + '.bef.txt'); now = load(stem + '.now.txt')
    except Exception as e:
        print('!! %s 读取失败 %s' % (page, e)); continue
    print('══════════ %s ══════════' % page)
    print('  overflowX   bef=%-4s now=%-4s    selCount bef=%-3s now=%-3s'
          % (bef['overflowX'], now['overflowX'], bef['selCount'], now['selCount']))

    def key(s):
        return s['cls'] + '|' + (s['txt'] or '')

    bmap, nmap = {}, {}
    for s in bef['selects']:
        bmap.setdefault(key(s), []).append(s)
    for s in now['selects']:
        nmap.setdefault(key(s), []).append(s)
    allk = sorted(set(bmap) | set(nmap))
    for k in allk:
        bl = bmap.get(k, []); nl = nmap.get(k, [])
        for i in range(max(len(bl), len(nl))):
            b = bl[i] if i < len(bl) else None
            n = nl[i] if i < len(nl) else None
            def fmt(x):
                if x is None:
                    return '（缺）'
                return 'wh=%-13s r=%-6s ring=%-9s trunc=%s' % (str(x['wh']), x['radius'], x['ring'], x['truncated'])
            changed = (b is None or n is None or b['wh'] != n['wh'] or b['radius'] != n['radius']
                       or b['ring'] != n['ring'])
            mark = '  ← 变' if changed else ''
            print('   %s' % k[:46])
            print('      改前 %s' % fmt(b))
            print('      改后 %s%s' % (fmt(n), mark))
    print('  改前 clipped: %s' % bef['clipped'])
    print('  改后 clipped: %s' % now['clipped'])
    print()
