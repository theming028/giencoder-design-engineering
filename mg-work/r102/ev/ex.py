import io, re, sys
p = sys.argv[1]
t = io.open(p, encoding='utf-8').read()
key = sys.argv[2] if len(sys.argv) > 2 else '打开侧栏'
i = t.find(key)
print('first idx', i)
if i < 0:
    sys.exit(0)
# 往前找最近的 td-right-acts
j = t.rfind('td-right-acts', 0, i)
print('acts idx', j)
seg = t[j-40:i+3000]
print(seg.replace('\\"', '"'))
