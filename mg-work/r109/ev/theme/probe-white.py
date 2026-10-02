# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 A：DS 里「白色」的正规表达。

目标：铁律 #2 禁硬编码 hex ⇒ 必须用 DS 变量表达白色。
  - 找 --color-bg-white / --color-bg-1 / --gray-1 在浅色档与暗色档的字面定义
  - 找还有哪些语义 token 浅色档 = #fff / #ffffff / 255,255,255
  - 只打片段，不整文件读
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

# 白的各种字面写法
RE_WHITE = re.compile(
    u'#[Ff]{6}\\b|#[Ff]{3}\\b|#ffffff|#FFFFFF|255,\\s*255,\\s*255|'
    u'rgb\\(\\s*255\\s*,\\s*255\\s*,\\s*255\\s*\\)|white\\b')

# 关心的 token 名
TOKENS = [u'--color-bg-white', u'--color-bg-1', u'--color-bg-2', u'--color-bg-3',
          u'--color-bg-4', u'--color-bg-5', u'--color-bg-popup',
          u'--gray-1', u'--gray-2', u'--gray-3']


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def block_of(t, i):
    u"""回溯第 i 字节所属的选择器块（往前找最近的 } 或者 <style 起点）"""
    j = t.rfind(u'}', 0, i)
    k = t.rfind(u'{', 0, i)
    if k > j:
        # 选择器在 { 之前
        s = t.rfind(u'}', 0, k)
        sel = t[s + 1:k]
    else:
        sel = u'(顶层/无选择器)'
    return sel.strip().replace(u'\n', u' ')[:90]


def main():
    pg = ALL[0] if len(sys.argv) < 2 else sys.argv[1]
    t = norm(rd(os.path.join(PAGES, pg + u'.html')))
    print(u'=== DS 白色相关令牌定义 · 页 = %s ===' % pg)
    print()
    for tok in TOKENS:
        hits = []
        i = 0
        while True:
            k = t.find(tok, i)
            if k < 0:
                break
            # 定义 = 紧跟 ':'
            seg = t[k:k + 90]
            m = re.match(re.escape(tok) + u'\\s*:\\s*([^;}]+)', seg)
            if m:
                sel = block_of(t, k)
                hits.append((sel, m.group(1).strip()))
            i = k + len(tok)
        if not hits:
            print(u'  %-22s （无定义）' % tok)
            continue
        print(u'  %-22s' % tok)
        for sel, val in hits[:4]:
            tag = u'暗' if u'dark' in sel else u'浅'
            print(u'      [%s] %-46s = %s' % (tag, sel, val[:44]))
    print()
    print(u'=== 全白字面量出现（前 25 处，含上下文）===')
    n = 0
    for m in RE_WHITE.finditer(t):
        a = max(0, m.start() - 70)
        print(u'  …%s…' % norm(t[a:m.end() + 24]).replace(u'\n', u' '))
        n += 1
        if n >= 25:
            break
    print(u'  合计命中（该页）：%d' % len(RE_WHITE.findall(t)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
