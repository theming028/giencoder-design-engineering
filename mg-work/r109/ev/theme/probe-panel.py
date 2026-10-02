# -*- coding: utf-8 -*-
"""r109 · 找出 base 页所有「下拉浮层面板」的样式定义，横向对比配色是否统一。

判据：面板 = 带 `0px 8px 20px` 阴影（本项目浮层的统一阴影签名）的容器。
抽出 background / border / backdropFilter / className / role，去重后列出。
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PG = sys_pg = os.path.join(ROOT, 'pages', 'base.html')

t = io.open(PG, encoding='utf-8', newline='').read()

seen = set()
rows = []
for m in re.finditer(r'0px 8px 20px', t):
    i = m.start()
    seg = t[max(0, i - 900):i + 260]
    def grab(pat):
        v = re.findall(pat, seg)
        return v[-1] if v else ''
    bg = grab(r'background:\s*`([^`]{0,70})`')
    bd = grab(r'border:\s*`([^`]{0,60})`')
    bf = grab(r'backdropFilter:\s*`([^`]{0,40})`')
    cls = grab(r'className:\s*`([^`]{0,70})`')
    role = grab(r'role:\s*`([^`]{0,24})`')
    br = grab(r'borderRadius:\s*([0-9`][^,}]{0,12})')
    k = (bg, bd, bf, br)
    if k in seen:
        continue
    seen.add(k)
    rows.append((i, bg, bd, bf, br, cls, role))

print('面板样式变体数 =', len(rows))
print()
for i, bg, bd, bf, br, cls, role in rows:
    print('@%d' % i)
    print('   background      =', bg or '-')
    print('   border          =', bd or '-')
    print('   backdropFilter  =', bf or '-')
    print('   borderRadius    =', br or '-')
    print('   className/role  =', cls or '-', '/', role or '-')
    print()

# 另外：把所有「面板底」用到的变量/字面值汇总，看是否同源
print('=' * 70)
print('面板底取值汇总（出现次数）')
print('=' * 70)
bgs = {}
for i, bg, *_ in rows:
    if bg:
        bgs[bg] = bgs.get(bg, 0) + 1
for k, v in sorted(bgs.items(), key=lambda x: -x[1]):
    print('  %-46s x%d' % (k, v))
