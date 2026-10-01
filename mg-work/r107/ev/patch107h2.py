# -*- coding: utf-8 -*-
"""r107 第七拍 · 需求①：右栏里的竞品名 → GienCoder（可见文案 + 悬停 title）。
   只动 `part107/_mods.html`（右栏四个新模块的静态片段）。
   ⚠ 全程走二进制，不动行尾（本仓页面是 CRLF）。
   ⚠ 三条外链 href（flaviocopes / developers.openai / worldprogramming）**有意不改** ——
      它们是真实可打开的地址，替换域名段会直接 404；且不渲染成页面文字。
用法： python mg-work/r107/ev/patch107h2.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(REPO, 'mg-work', 'r107', 'part107', '_mods.html')

TABLE = [
    (u'docs/codex-sidepanel-research.md', u'docs/giencoder-sidepanel-research.md', 3),
    (u'# Codex 右栏调研', u'# GienCoder 右栏调研', 3),
    (u'升级成 Codex 那套', u'升级成 GienCoder 那套', 1),
    (u'The complete guide to Codex', u'The complete guide to GienCoder', 2),
    (u'Codex changelog', u'GienCoder changelog', 1),
]


def main():
    b = io.open(P, 'rb').read()
    for old, new, want in TABLE:
        ob, nb = old.encode('utf-8'), new.encode('utf-8')
        n = b.count(ob)
        if n not in (0, want):
            sys.exit('!! %r 命中 %d 次（应 %d 或 0 次）' % (old, n, want))
        b = b.replace(ob, nb)
    io.open(P, 'wb').write(b)
    t = b.decode('utf-8').replace('\r\n', '\n')
    print(u'   _mods.html %d 字符；CRLF %d' % (len(t), b.count(b'\r\n')))
    low = t.lower()
    i, k = 0, 0
    while True:
        i = low.find('codex', i)
        if i < 0:
            break
        k += 1
        print(u'   残留 @%d | %s' % (i, t[max(0, i - 70):i + 40].replace('\n', ' ')))
        i += 5
    print(u'   codex 残留 %d 处（应 3 = 三条外链 href）' % k)


if __name__ == '__main__':
    main()
