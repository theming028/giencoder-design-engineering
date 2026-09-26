# -*- coding: utf-8 -*-
"""把 settings.html 左栏 base 分支的“返回”按钮插到 flex flex-col gap-1 之上"""
import re

BS = chr(92)
p = 'pages/settings.html'
s = open(p, encoding='utf-8').read()

BTN = ('(0,j.jsx)(`div`,{className:`mb-3 shrink-0`,children:(0,j.jsxs)(Tt,{to:`/`,'
       'className:`flex w-fit items-center gap-1.5 rounded-md px-2 py-1 text-sm '
       '[color:var(--color-text-3)] hover:bg-black/[0.05] hover:[color:var(--color-text-1)]`,'
       'children:[(0,j.jsx)(heBack,{className:`size-4`}),`返回`]})})')


def match_end(s, i):
    stack = []
    k = i
    n = len(s)
    while k < n:
        c = s[k]
        if c == '`':
            k += 1
            while k < n and s[k] != '`':
                if s[k] == BS:
                    k += 1
                k += 1
            k += 1
            continue
        if c == "'" or c == '"':
            q = c
            k += 1
            while k < n and s[k] != q:
                if s[k] == BS:
                    k += 1
                k += 1
            k += 1
            continue
        if c in '([{':
            stack.append(c)
        elif c in ')]}':
            stack.pop()
            if not stack:
                return k + 1
        k += 1
    return -1


start_marker = '(0,j.jsx)(`div`,{className:`pt-0 pr-3`,'
i = s.find(start_marker)
assert i != -1, 'start marker not found'
j = i + len('(0,j.jsx)')          # 从实参元组开始做括号匹配
e = match_end(s, j)
assert e != -1, 'no matching end'
seg = s[i:e]
print('seg len', len(seg))
print('seg tail:', repr(seg[-120:]))
assert seg[-2:] == '})', 'seg does not end with }) -> ' + repr(seg[-4:])

GAP = 'children:(0,j.jsxs)(`div`,{className:`flex flex-col gap-1`,children:['
NEWGAP = ('children:[' + BTN +
          ',(0,j.jsxs)(`div`,{className:`flex flex-col gap-1`,children:[')
assert GAP in seg, 'gap-1 head not found in seg'
seg2 = seg.replace(GAP, NEWGAP, 1)
# 外层改为 jsxs（children 变为数组）
seg2 = seg2.replace('(0,j.jsx)(`div`,{className:`pt-0 pr-3`,',
                    '(0,j.jsxs)(`div`,{className:`pt-0 pr-3`,', 1)
# 在最后一个 }) 之前补上数组右括号
seg2 = seg2[:-2] + ']' + seg2[-2:]

s2 = s[:i] + seg2 + s[e:]
open(p, 'w', encoding='utf-8').write(s2)
print('written, delta', len(s2) - len(s))

# 语法检查
s3 = open(p, encoding='utf-8').read()
for m in re.finditer(r'<script[^>]*>', s3):
    a = m.end()
    b = s3.find('</script>', a)
    body = s3[a:b]
    if 'heBack' in body:
        open('mg-work/kanban/_settings_bundle.js', 'w', encoding='utf-8').write(body)
        print('bundle script len', len(body))
        break
