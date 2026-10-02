# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 H：品牌 LOGO 的 data-URI 在页面源码里的注入点。

真机确认 base 页 <img> 的 src = data:image/svg+xml,...（15213 字符）。
本脚本在 base.html 源码里找这个 svg 的**源头**（是否可读？还是 JS 拼的？）
以及它是否与暗色档有关系（有没有两套、或套了 filter/opacity）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

SIGS = [u'#1E1E1E', u'#3D3D3D', u'#3770F7', u'#D0D3D6',
        u'298.0999755859375', u'GIENC', u'data:image/svg+xml']


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    pg = sys.argv[1] if len(sys.argv) > 1 else u'base'
    p = os.path.join(PAGES, pg + u'.html')
    t = norm(rd(p))
    print(u'=== %s.html（%d 字符）品牌 LOGO 线索 ===' % (pg, len(t)))
    print()
    for sig in SIGS:
        n = t.count(sig)
        print(u'   %-24s ×%d' % (sig, n))
    print()
    for sig in [u'#1E1E1E', u'298.0999755859375']:
        for m in list(re.finditer(re.escape(sig), t))[:3]:
            i = m.start()
            print(u'   [%s] @%d  …%s…' % (sig, i, t[max(0, i - 200):i + 120].replace(u'\n', u' ')))
            print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
