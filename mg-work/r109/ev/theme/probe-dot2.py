# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 E2：settings 页 .dot-bg 的**定义处 vs 使用处**分离。

★ 关键：.dot-bg 的 CSS 定义在「全站共享的 DS 编译包」里 ⇒ 改不得（会波及 10 页）。
  必须分清：哪几处是 CSS 规则、哪几处是 HTML/JS 的 className 使用。
  只有「使用处」能安全摘除（或加 settings 专用覆盖）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

RE_DOTBG = re.compile(u'\\.dot-bg')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    pg = sys.argv[1] if len(sys.argv) > 1 else u'settings'
    t = norm(rd(os.path.join(PAGES, pg + u'.html')))
    print(u'=== .dot-bg 出现处 · 页 = %s ===' % pg)
    ms = list(RE_DOTBG.finditer(t))
    print(u'  命中总数：%d' % len(ms))
    print()
    for i, m in enumerate(ms):
        a = max(0, m.start() - 150)
        b = min(len(t), m.end() + 170)
        seg = t[a:b].replace(u'\n', u' ')
        kind = u'?'
        if re.search(u'\\.dot-bg\\s*\\{', t[m.start():m.start() + 40]):
            kind = u'CSS定义'
        elif re.search(u'\\.dot-bg\\s*::', t[m.start():m.start() + 40]):
            kind = u'CSS伪元素'
        elif u'className' in t[max(0, m.start() - 60):m.start() + 20] or u'class=' in t[max(0, m.start() - 60):m.start() + 20]:
            kind = u'★使用处'
        print(u'  #%d [%s] @%d' % (i, kind, m.start()))
        print(u'      …%s…' % seg)
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
