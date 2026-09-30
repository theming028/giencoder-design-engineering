import io, re, sys
p = sys.argv[1]
t = io.open(p, encoding='utf-8').read()
pos = [m.start() for m in re.finditer('td-right-acts', t)]
print('occurrences:', len(pos), pos)
for i in pos:
    ctx = t[max(0, i-90):i+60].replace('\n', ' ')
    print('---', i, repr(ctx))
