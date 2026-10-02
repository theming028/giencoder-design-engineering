# -*- coding: utf-8 -*-
u"""模拟 apply109.py 的「净底自检」，列出到底是哪些禁用 token 还残留在 net 里。

用于定位「拍3 注入的主题 / 暗色块」是否破坏了下游链的自检。
"""
import importlib.util
import io
import os
import sys

REPO = 'E:/GienCoder/giencoder-design-engineering'
AP = os.path.join(REPO, 'mg-work', 'r109', 'apply109.py')

spec = importlib.util.spec_from_file_location('ap109', AP)
mod = importlib.util.module_from_spec(spec)
# apply109.py 顶层只定义常量 / 函数（main 在 __main__ 里）⇒ 直接 exec 是安全的
spec.loader.exec_module(mod)

src = io.open(os.path.join(REPO, 'pages', 'base.html'), encoding='utf-8').read()
net = src
for rx in (mod.RE_STYLE, mod.RE_JS, mod.RE_NAV, mod.RE_HDR):
    net = rx.sub('', net)

print('GENS = %r' % (mod.GENS,))
toks = []
for g in mod.GENS:
    toks += [g[1], g[2], g[3]]
toks += [mod.ATTR_HOST, mod.HDR_ID]
bad = []
for t in toks:
    n = net.count(t)
    if n:
        bad.append((t, n))
print('net 长度 = %d（原 %d）' % (len(net), len(src)))
print('残留 token 数 = %d' % len(bad))
for t, n in bad:
    print('  !!! %-24s × %d' % (t, n))
    for m in __import__('re').finditer(__import__('re').escape(t), net):
        print('        ctx: %r' % net[max(0, m.start() - 120):m.start() + 80])
if (mod.NAV_TAG + '-nav') in net:
    print('  !!! nav 注释 %s-nav 也在' % mod.NAV_TAG)
if not bad and (mod.NAV_TAG + '-nav') not in net:
    print('  ✓ 净底自检应通过')
