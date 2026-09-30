# -*- coding: utf-8 -*-
"""r92 侦察 2：权限触发器锚点精确串 + pe 图标定义 + danger token 值。"""
import re

s = open('pages/base.html', encoding='utf-8').read()

print('=== danger token 定义 ===')
for m in re.finditer(r'--color-danger-\d+:\s*[^;}]+', s):
    print('  ', m.group(0))
print()
for m in re.finditer(r'--giencoderred-\d+:[^;]+', s):
    print('  ', m.group(0))
print()

print('=== 触发器锚点（图标）===')
A1 = "`size-[14px] shrink-0 `+(l===`perm`?`[color:var(--color-text-1)]`:`[color:var(--color-text-2)]`)"
print('  count =', s.count(A1))
i = s.find(A1)
print('  ctx:', s[max(0, i - 120):i + len(A1) + 60] if i >= 0 else 'NOT FOUND')

print()
print('=== 触发器锚点（文字）===')
A2 = "style:{color:l===`perm`?`var(--color-text-1)`:`var(--color-text-2)`,lineHeight:`19px`,flex:`none`,overflow:`visible`,textOverflow:`clip`},children:s}"
print('  count =', s.count(A2))
i = s.find(A2)
print('  ctx:', s[max(0, i - 120):i + len(A2) + 60] if i >= 0 else 'NOT FOUND')

print()
print('=== pe 组件定义 ===')
for m in re.finditer(r'\bvar pe=', s):
    print('  ', s[m.start():m.start() + 700])
    print()
for m in re.finditer(r'\bpe=', s):
    print('   (pe= @%d)' % m.start(), s[m.start():m.start() + 600])
    break
