# -*- coding: utf-8 -*-
"""校验 part-ctx.js 的图标抽取正则（r101 ⑦）。用文件形式写，避免 heredoc 吞反斜杠。"""
import io
import re
import sys

src = io.open(sys.argv[1], encoding='utf-8').read()
plain = dict(re.findall(r"\n\s*(\w+):\s*'(<svg.*?</svg>)'", src))
brand = dict(re.findall(r"\{\s*id:\s*'(\w+)',\s*label:\s*'[^']*',\s*svg:\s*'(<svg.*?</svg>)'\s*\}", src))
print('plain', len(plain), sorted(plain))
print('brand', len(brand), sorted(brand))
tot = 0
for k, v in sorted(plain.items()):
    print('  plain', k, len(v))
    tot += len(v)
for k, v in sorted(brand.items()):
    print('  brand', k, len(v))
    tot += len(v)
print('total chars', tot)
