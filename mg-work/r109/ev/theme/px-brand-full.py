# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 解码 base 页品牌 LOGO 的 data-URI，列出全部色值与其用量。

来源：raw/find11/brand-full.txt（<img src> 的完整内容，URL-encoded SVG）
"""
import collections
import io
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, os.pardir, os.pardir, u'raw', u'find11', u'brand-full.txt')


def main():
    raw = io.open(FULL, encoding='utf-8', newline='').read().strip()
    # 去掉 data:image/svg+xml, 前缀再解码
    if raw.startswith(u'data:'):
        raw = raw.split(u',', 1)[1]
    svg = urllib.parse.unquote(raw)
    print(u'=== 解码后 SVG 长度 %d ===' % len(svg))
    print(svg[:400].replace(u'><', u'>\n<')[:900])
    print()
    print(u'=== 全部色值统计 ===')
    c = collections.Counter(re.findall(u"#[0-9A-Fa-f]{6}\\b|#[0-9A-Fa-f]{3}\\b", svg))
    for v, n in c.most_common():
        print(u'   %-10s ×%d' % (v, n))
    print()
    # 逐个 fill / stroke 属性值统计（含 fill-opacity）
    print(u'=== fill / stroke 取值 ===')
    cf = collections.Counter(re.findall(u"fill='([^']*)'", svg))
    for v, n in cf.most_common(12):
        print(u'   fill   %-16s ×%d' % (v, n))
    cs = collections.Counter(re.findall(u"stroke='([^']*)'", svg))
    for v, n in cs.most_common(12):
        print(u'   stroke %-16s ×%d' % (v, n))
    print()
    # 上下文：#3D3D3D 出现在哪（是否集中在后半段文字部分）
    print(u'=== #3D3D3D 出现位置（相对长度）===')
    idxs = [m.start() for m in re.finditer(u'#3D3D3D', svg)]
    for i in idxs[:12]:
        print(u'   @%d (%.0f%%)  …%s…' % (i, 100.0 * i / len(svg), svg[max(0, i - 70):i + 20].replace(u'\n', u' ')))
    print(u'   共 %d 处' % len(idxs))
    print()
    print(u'=== #D0D3D6（分隔线）出现位置 ===')
    idxs2 = [m.start() for m in re.finditer(u'#D0D3D6', svg)]
    for i in idxs2[:8]:
        print(u'   @%d (%.0f%%)  …%s…' % (i, 100.0 * i / len(svg), svg[max(0, i - 100):i + 60].replace(u'\n', u' ')))
    print(u'   共 %d 处' % len(idxs2))
    # 保存解码结果
    out = os.path.join(os.path.dirname(FULL), u'brand-decoded.svg')
    io.open(out, 'w', encoding='utf-8', newline='').write(svg)
    print()
    print(u'解码 SVG 已存 → %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
