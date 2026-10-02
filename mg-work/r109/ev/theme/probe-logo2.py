# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 D2：base 页**顶栏左侧**的 LOGO 元素。

思路：顶栏 = header[class*="h-12"]（DS 里给它挂了 bg-img-1.png 背景图）。
LOGO 大概率在它最左侧。本脚本把 header 附近的 HTML/JSX 片段抠出来看结构，
重点找 <img> / <svg> / 内联 fill 的「黑灰」色来源。
另外横向统计全站 LOGO 相关的「黑灰」色值（#333 #666 #1F1F1F gray-10 等）。
"""
import collections
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

# 黑灰系字面量
RE_DARKHEX = re.compile(u'#(?:1[0-9a-fA-F]|2[0-9a-fA-F]|3[0-9a-fA-F]|4[0-9a-fA-F]|5[0-9a-fA-F]|6[0-9a-fA-F]){3}\\b')
RE_GRAYVAR = re.compile(u'var\\(--gray-(?:8|9|10)\\)|var\\(--color-text-[123]\\)')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    pg = sys.argv[1] if len(sys.argv) > 1 else u'base'
    t = norm(rd(os.path.join(PAGES, pg + u'.html')))
    print(u'=== header 区域结构 · 页 = %s ===' % pg)
    k = t.find(u'<header')
    if k < 0:
        k = t.find(u'header')
    print(u'  第一个 <header> @%d' % k)
    print()
    print(u'  --- 该处向前 300 / 向后 900 字符 ---')
    print(u'  %s' % t[max(0, k - 300):k + 900].replace(u'\n', u' '))
    print()
    print(u'=== 黑灰字面量（#1xx~#6xx）统计：top 12 ===')
    c = collections.Counter(RE_DARKHEX.findall(t))
    for v, n in c.most_common(12):
        print(u'   %-10s ×%d' % (v, n))
    print()
    print(u'=== gray-8/9/10 与 text-1/2/3 变量引用 ===')
    c2 = collections.Counter(RE_GRAYVAR.findall(t))
    for v, n in c2.most_common(12):
        print(u'   %-24s ×%d' % (v, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
