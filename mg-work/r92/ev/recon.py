# -*- coding: utf-8 -*-
"""r92 侦察：顶栏 header 结构 / 危险色 token / 各页 activeTab / 深色主题覆盖。"""
import glob
import os
import re

for f in sorted(glob.glob('pages/*.html')):
    s = open(f, encoding='utf-8').read()
    nm = os.path.basename(f)
    print('#####', nm)
    # 1) header 元素创建点
    for m in re.finditer(r'\(0,A\.jsxs\)\(`header`', s):
        a = m.start()
        print('   header-elem @%d: %s' % (a, s[a:a + 200]))
    print('   (`header` count =', s.count('(`header`'), ')')
    # 2) 危险色 token
    print('   --color-danger-6:', s.count('--color-danger-6'),
          '| --color-danger-5:', s.count('--color-danger-5'),
          '| danger-light-1:', s.count('--color-danger-light-1'))
    # 3) activeTab 传入值
    for m in re.finditer(r'activeTab[:=]\s*[`\'"](base|dev)[`\'"]', s):
        print('   activeTab ->', m.group(0), '@%d' % m.start())
    for m in re.finditer(r'active[:=]\s*[`\'"](base|dev)[`\'"]', s):
        print('   active ->', m.group(0), '@%d' % m.start())
    # 4) 深色主题下 header 是否有覆盖
    for m in re.finditer(r"giencoder-theme['\"]?=?['\"]?dark[^{]{0,80}header", s):
        print('   dark header rule @%d' % m.start(), s[m.start():m.start() + 120])
    print()
