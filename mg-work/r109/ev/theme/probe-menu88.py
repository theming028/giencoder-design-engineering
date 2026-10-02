# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 C：浅色档下拉面板底 rgba(var(--gray-1),0.88) 的**全部注入点**。

真机（raw/dd9-light/panel-{0..5}.json）显示 base 页 6 类下拉面板浅色档底**全是**
rgba(247,247,247,0.88)，连基准「默认权限」也是 ⇒ 说明除 CSS 的 .giencoder-select-popup
外，还有 JS inline 注入点。本脚本把全站所有写法（含空格变体）穷举出来，并打上下文。
"""
import collections
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

PAT = re.compile(u'rgba\\(\\s*var\\(--gray-1\\)\\s*,\\s*0?\\.88\\s*\\)')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    total = 0
    per = collections.OrderedDict()
    ctx = collections.OrderedDict()
    for pg in ALL:
        t = norm(rd(os.path.join(PAGES, pg + u'.html')))
        ms = list(PAT.finditer(t))
        per[pg] = len(ms)
        total += len(ms)
        for m in ms:
            a = max(0, m.start() - 90)
            b = min(len(t), m.end() + 30)
            key = norm(t[a:b]).replace(u'\n', u' ')
            ctx.setdefault(key, []).append(pg)
    print(u'=== rgba(var(--gray-1),0.88) 注入点普查 ===')
    print()
    for pg, n in per.items():
        print(u'   %-14s %d' % (pg, n))
    print(u'   ── 合计 %d' % total)
    print()
    print(u'=== 上下文（去重）===')
    for c, pgs in ctx.items():
        print(u'  [%s]' % u','.join(sorted(set(pgs))))
        print(u'     …%s…' % c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
