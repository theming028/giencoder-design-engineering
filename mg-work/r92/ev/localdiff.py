# -*- coding: utf-8 -*-
"""r92：把 5 页与 r92 前置基线对比 —— 先摘掉本代注入的 r92-* 样式块，
再用「公共前缀 / 公共后缀」定位剩余改动窗口。窗口应只剩本代手改的几处。"""
import io
import re

BLOCKS = [r'\n?<style id="r92-hdr-css">.*?</style>', r'\n?<style id="r92-perm-css">.*?</style>']


def strip92(s):
    for rx in BLOCKS:
        s = re.sub(rx, '', s, flags=re.S)
    return s


for pg in ['base', 'settings', 'avatar', 'skills', 'automation']:
    a = io.open('mg-work/r92/before/%s.html' % pg, encoding='utf-8').read()
    raw = io.open('pages/%s.html' % pg, encoding='utf-8').read()
    n_block = len(raw) - len(strip92(raw))
    b = strip92(raw)

    print('##### %-11s %d → %d（+%d；其中 r92-* 注入块 %d 字符）'
          % (pg + '.html', len(a), len(raw), len(raw) - len(a), n_block))
    if a == b:
        print('   ✅ 摘掉 r92 注入块后与前置基线**逐字节相同**（除注入块外零改动）')
        print()
        continue

    # 公共前缀
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    # 公共后缀
    j = 0
    while j < n - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
        j += 1
    mid_a = a[i:len(a) - j]
    mid_b = b[i:len(b) - j]
    print('   仍有改动：位置 %d，旧 %d 字符 / 新 %d 字符' % (i, len(mid_a), len(mid_b)))
    print('   - %r' % mid_a[:500])
    print('   + %r' % mid_b[:500])
    print()
