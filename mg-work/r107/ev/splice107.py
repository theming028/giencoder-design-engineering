# -*- coding: utf-8 -*-
"""r107 · 组装 `part107/browse.html`。

体位：**从 r105 移植件里「剪」出 Files 正文逐字复用**，只把「头部」换掉、后面追加新模块。
  part105/browse.html = <split><slot><aside> + <header …> + <div.td-browse-body>…(Files 正文) + </aside></div>

  新文件 = <split><slot><aside> + part107/_head.html + 【原 <div.td-browse-body>… 逐字】 + part107/_mods.html + </aside></div>

⇒ 「文件」模块的 DOM 与 r105/r106 完全一致（r106 的 44px 适配层、ctrl-conv.js 的选择器全部继续成立），
  改动面 = 头部一行 + 追加四个新模块。

用法： python mg-work/r107/ev/splice107.py           # 写 part107/browse.html
      python mg-work/r107/ev/splice107.py --check   # 只校验（不写）
"""
import argparse
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(REPO, 'mg-work', 'r102', 'part105', 'browse.html')
P107 = os.path.join(REPO, 'mg-work', 'r107', 'part107')
OUT = os.path.join(P107, 'browse.html')


def read(p):
    return io.open(p, encoding='utf-8').read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    src = read(SRC)
    head = read(os.path.join(P107, '_head.html'))
    mods = read(os.path.join(P107, '_mods.html'))

    # 1) 前缀 = …<aside class="td-browse" aria-label="文件预览">
    i_aside = src.find('<aside class="td-browse"')
    if i_aside < 0:
        sys.exit('!! 找不到 <aside class="td-browse"')
    i_aside_end = src.find('>', i_aside) + 1
    prefix = src[:i_aside_end]

    # 2) 原头部：<header class="td-browse-bar"> … </header>
    i_h = src.find('<header class="td-browse-bar"')
    if i_h < 0:
        sys.exit('!! 找不到原 <header class="td-browse-bar"')
    if i_h != i_aside_end + 2:
        sys.exit('!! 原头部不是紧跟在 <aside> 之后（中间还有别的内容：%r）' % src[i_aside_end:i_h])
    i_h_end = src.find('</header>', i_h)
    if i_h_end < 0:
        sys.exit('!! 找不到原 </header>')
    i_h_end += len('</header>')

    # 3) Files 正文：<div class="td-browse-body"> … 到 </aside>
    i_b = src.find('<div class="td-browse-body">', i_h_end)
    if i_b < 0:
        sys.exit('!! 找不到 <div class="td-browse-body">')
    i_a = src.find('</aside>', i_b)
    if i_a < 0:
        sys.exit('!! 找不到收尾 </aside>')
    body = src[i_b:i_a]
    if body.count('td-browse-body') != 1 or 'td-browse-files' not in body:
        sys.exit('!! 剪出来的 Files 正文不像原样')

    out = prefix + head + body + mods + '</aside></div>\n'

    # 4) 守卫：静态片段里不能出现 <script / <style（会打乱注入结构）
    for tok in ('<script', '</script', '<style', '</style'):
        if tok in out:
            sys.exit('!! 组装结果里出现了 %r' % tok)
    for need in ('id="av-browse-split"', 'id="av-browse-slot"', 'data-td-browse-close="1"',
                 'data-td-split="tree"', 'td-browse-files', 'class="td-browse-body"'):
        if need not in out:
            sys.exit('!! 组装结果缺少 %r' % need)
    if out.count('<aside') != 1 or out.count('</aside>') != 1:
        sys.exit('!! <aside> 计数异常')

    print('   前缀 %d + 头部 %d + Files 正文 %d + 新模块 %d = 总 %d 字符'
          % (len(prefix), len(head), len(body), len(mods), len(out)))
    if a.check:
        old = read(OUT) if os.path.exists(OUT) else ''
        print('   --check：%s' % ('已是最新' if old == out else '与落盘文件不同（需重跑）'))
        return
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(out)
    print('   写出', OUT)


if __name__ == '__main__':
    main()
