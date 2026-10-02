# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 D：base.html 的 LOGO —— 定位「黑灰部分」的来源。

邵先生原话：把暗色模式下 base.html 页面的 LOGO 的**黑灰部分**改成白色，浅色模式不变。
要回答三件事：
  1. LOGO 是内联 SVG / <img> / 背景图 / 图标字体？
  2. 「黑灰部分」由谁上色（fill / color / stop-color / background / currentColor）？
  3. 该上色值是不是 DS 变量？是哪一个？暗色档它现在解析成什么？
只打片段，不整文件读。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

RE_LOGO = re.compile(u'[Ll]ogo|LOGO|logoSvg|logoViewBox|brand|Brand|商标|标识')
# 上色来源
RE_FILL = re.compile(
    u'(fill|stop-color|color|background|stroke)\\s*[:=]\\s*[`\'"]?\\s*'
    u'(#[0-9a-fA-F]{3,8}|rgba?\\([^)]*\\)|var\\(--[a-z0-9-]+\\)|currentColor)')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    pg = sys.argv[1] if len(sys.argv) > 1 else u'base'
    t = norm(rd(os.path.join(PAGES, pg + u'.html')))
    print(u'=== LOGO 线索 · 页 = %s ===' % pg)
    print(u'  logo 类字面命中：%d' % len(RE_LOGO.findall(t)))
    print()
    seen = 0
    for m in RE_LOGO.finditer(t):
        a = max(0, m.start() - 110)
        b = min(len(t), m.end() + 130)
        seg = t[a:b]
        # 只打印「同段里带上色声明」的命中（其余信息量低）
        fm = RE_FILL.search(seg)
        if not fm:
            continue
        print(u'  @%d  …%s…' % (m.start(), seg.replace(u'\n', u' ')))
        print(u'        ↳ 上色 = %s' % fm.group(0))
        print()
        seen += 1
        if seen >= 22:
            break
    print(u'  带色命中条数：%d' % seen)
    print()
    print(u'=== --color-white / --color-text-? 在暗色档的值 ===')
    for tok in [u'--color-white', u'--color-text-1', u'--color-text-2',
                u'--color-text-3', u'--gray-10', u'--gray-9', u'--gray-8']:
        i = 0
        out = []
        while len(out) < 3:
            k = t.find(tok, i)
            if k < 0:
                break
            m = re.match(re.escape(tok) + u'\\s*:\\s*([^;}]+)', t[k:k + 80])
            if m:
                head = t[max(0, k - 240):k]
                tag = u'暗' if u'theme=dark' in head else u'浅'
                out.append(u'[%s] %s' % (tag, m.group(1).strip()[:40]))
            i = k + len(tok)
        print(u'  %-18s %s' % (tok, u'  |  '.join(out) if out else u'(无定义)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
