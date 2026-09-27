import io, re, sys
for f in ['pages/kanban.html','pages/req-kanban.html']:
    s = io.open(f, encoding='utf-8').read()
    print('='*20, f, len(s))
    for m in re.finditer(r'task-detail\.html', s):
        a=max(0,m.start()-300); b=min(len(s), m.end()+200)
        print('--- ctx @%d ---' % m.start())
        print(s[a:b].replace('\n','\\n')[:520])
