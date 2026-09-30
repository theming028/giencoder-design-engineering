import json, re, sys
buf = open('mg-work/r93/ev/p95a.txt', encoding='utf-8', errors='replace').read()
parts = re.split(r'########## viewport (\d+) ##########', buf)
i = 1
while i < len(parts):
    vw, body = parts[i], parts[i + 1]; i += 2
    print('=' * 18, 'viewport', vw, '=' * 18)
    m = re.search(r'"\{.*\}"', body, re.S)
    if not m:
        print(body.strip()[:1500]); continue
    s = json.loads(m.group(0))
    if isinstance(s, str): s = json.loads(s)
    print('main   ', s['main'])
    print('wrap   ', s['wrap'])
    print('scroll ', s['scroll'])
    print('bottom ', s['bottom'])
    print('--- blocks (.r93-wrap > *) ---')
    for b in s['blocks']:
        print('  %-64s it=%-10s r=%s w=%s ml=%s' % (b['c'], b['it'], b['r'], b['w'], b['ml']))
    print('--- bottom kids ---')
    for b in s['botKids']:
        print('  %-52s r=%s w=%s ml=%s' % (b['c'], b['r'], b['w'], b['ml']))
    print('outer  ', s['outer'])
    for b in s['outerKids']:
        print('  outerKid %-52s disp=%-8s r=%s w=%s' % (b['c'], b['d'], b['r'], b['w']))
    print('ctx/full/todo/bub')
    for k in ('ctx', 'full', 'todo', 'bub'):
        print('   %-5s %s' % (k, s[k]))
    print('doc/win', s['doc'], s['win'])
