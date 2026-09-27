import io, re
for f in ['pages/kanban.html','pages/req-kanban.html']:
    s = io.open(f, encoding='utf-8').read()
    labs = re.findall(r'aria-label="([^"]{1,24})"', s)
    seen=[]
    for l in labs:
        if l not in seen: seen.append(l)
    print('===', f, 'n=',len(labs),'uniq',len(seen))
    print(' | '.join(seen))
