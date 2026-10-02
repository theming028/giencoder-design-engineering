# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 E：设置页的「波点背景」——定位声明来源。

「波点背景」可能的写法：
  - background-image: radial-gradient(... ) 重复圆点（最常见）
  - background: url("data:image/svg+xml,...<circle>...")
  - background-size: Npx Npx + background-image: radial-gradient
  - CSS 类里带 dot / dotted / pattern / grid / polka
  - 内联 <svg><pattern><circle>
本脚本把 settings.html（并横向比对它页）里所有可疑声明打出来，带上下文。
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

RE_BGI = re.compile(
    u'background(?:-image)?\\s*:\\s*([^;`\'}]*(?:radial-gradient|url\\(|pattern|'
    u'data:image)[^;`\'}]*)', re.I)
RE_DOTCLS = re.compile(u'(?:dot|polka|pattern|grid-bg|noise|wave)[a-z0-9-]*', re.I)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    print(u'=== 波点/点阵背景普查（10 页）===')
    print()
    for pg in ALL:
        t = norm(rd(os.path.join(PAGES, pg + u'.html')))
        hits = []
        for m in RE_BGI.finditer(t):
            a = max(0, m.start() - 120)
            hits.append(u'…%s…' % t[a:m.end() + 20].replace(u'\n', u' '))
        cls = collections.Counter(RE_DOTCLS.findall(t))
        if not hits and not cls:
            print(u'  %-14s （无）' % pg)
            continue
        print(u'  %-14s 可疑声明 %d 条' % (pg, len(hits)))
        for h in hits[:8]:
            print(u'       %s' % h[:190])
        top = cls.most_common(6)
        if top:
            print(u'       类名词频：%s' % u', '.join(u'%s×%d' % (k, v) for k, v in top))
    return 0


if __name__ == '__main__':
    sys.exit(main())
