import json, re
buf = open('mg-work/r93/ev/p95b.txt', encoding='utf-8', errors='replace').read()
parts = re.split(r'########## viewport (\d+) ##########', buf)
i = 1
while i < len(parts):
    vw, body = parts[i], parts[i + 1]; i += 2
    print('=' * 18, 'viewport', vw, '=' * 18)
    m = re.search(r'"\{.*\}"', body, re.S)
    if not m:
        print(body.strip()[:1200]); continue
    s = json.loads(m.group(0))
    if isinstance(s, str): s = json.loads(s)
    print('scroll ', s['scroll'])
    print('wrap   ', s['wrap'])
    print('bottom ', s['bottom'])
    for b in s['botKids']:
        print('   botKid %-30s r=%s  RIGHT=%s' % (b['c'], b['r'], b['r'][0] + b['r'][2]))
    print('outer  ', s['outer'])
    print('input  ', s['inputCard'])
    R = lambda k: (s[k]['r'][0] + s[k]['r'][2]) if s.get(k) else None
    anchor = s['outer']['r'][0] + s['outer']['r'][2] if s['outer'] else None
    print('--- 内容块右边界 vs composer 右边界(%s) ---' % anchor)
    for k in ('ctx', 'todo', 'bub', 'alert', 'diff', 'arts', 'artcard', 'note'):
        v = s.get(k)
        if not v: print('   %-9s (无)' % k); continue
        print('   %-9s left=%-5s w=%-5s right=%-5s  Δ=%-4s  %s' % (k, v['r'][0], v['r'][2], v['r'][0] + v['r'][2], (v['r'][0] + v['r'][2] - anchor) if anchor else '?', v['c']))
    print('   wrap     left=%-5s w=%-5s right=%-5s  Δ=%s' % (s['wrap']['r'][0], s['wrap']['r'][2], s['wrap']['r'][0] + s['wrap']['r'][2], (s['wrap']['r'][0] + s['wrap']['r'][2] - anchor) if anchor else '?'))
    print('   bottom   left=%-5s w=%-5s right=%-5s' % (s['bottom']['r'][0], s['bottom']['r'][2], s['bottom']['r'][0] + s['bottom']['r'][2]))
    print('tbsticky', s['tb'], 'btn', s['tbbtn'])
    print('doc/win', s['doc'], s['win'])
