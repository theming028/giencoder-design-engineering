# -*- coding: utf-8 -*-
"""r109 · 组装 `part109/browse.html`。

体位与 `ev/splice108.py` 完全一致：**从 r105 移植件里「剪」出 Files 正文逐字复用**，
只把「头部」换掉、后面追加新模块。

  part105/browse.html = <split><slot><aside> + <header …> + <div.td-browse-body>…(Files 正文) + </aside></div>

  新文件 = <split><slot><aside> + part109/_head.html + 【原 <div.td-browse-body>… 逐字】 + part109/_mods.html + </aside></div>

⇒ 「文件」模块的 DOM 与 r105/r106/r107/r108 完全一致（r106 的 44px 适配层、ctrl-conv.js 的选择器全部继续成立），
  r109 的改动面 = `_mods.html` 里浏览器模块的 `td-page-blank` 删除 + `panel.css` / `panel.js`。

★ 与 r108 的差别：本代 `_head.html` **一字未动**（仍与 part108 逐字节相同），
  `_mods.html` 只删了 `.td-page-blank` 一行 —— 但仍从 **part109** 取，保持「本代优先」的资产体位。

用法： python mg-work/r109/ev/splice109.py           # 写 part109/browse.html
      python mg-work/r109/ev/splice109.py --check   # 只校验（不写）
"""
import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(REPO, 'mg-work', 'r102', 'part105', 'browse.html')
P107 = os.path.join(REPO, 'mg-work', 'r107', 'part107')
P109 = os.path.join(REPO, 'mg-work', 'r109', 'part109')
OUT = os.path.join(P109, 'browse.html')


def read(p):
    return io.open(p, encoding='utf-8').read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    src = read(SRC)
    # ★ r109：头部 / 新模块都从**本代**取（资产体位「本代优先」）。
    #   回退链：part109/_head.html 不存在时退回 part107 —— 但那样 r108 十八拍的 ②④ 就不生效，
    #   所以这里宁可硬失败，避免「静默用了旧头部」这种最难查的错。
    head_path = os.path.join(P109, '_head.html')
    if not os.path.exists(head_path):
        sys.exit('!! 缺少本代头部覆盖件 %s（沿用 r107/r108 的落点）' % head_path)
    head = read(head_path)
    mods = read(os.path.join(P109, '_mods.html'))

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
                 'data-td-split="tree"', 'td-browse-files', 'class="td-browse-body"',
                 # ★ r108 新增两件：审查工具条里那枚按钮 + 末尾的文件树抽屉
                 'data-td-rv-act="tree"', 'data-td-tree'):
        if need not in out:
            sys.exit('!! 组装结果缺少 %r' % need)
    if out.count('<aside') != 1 or out.count('</aside>') != 1:
        sys.exit('!! <aside> 计数异常')
    # ★ r108：抽屉里的树用独立类名 ⇒ 组装结果里**不该**出现第二个 `.td-browse-files`
    #   （⚠ 判据必须写成**属性形式**：注释里为解释原因提到过这个名字，裸词会误报）
    if out.count('class="td-browse-files"') != 1:
        sys.exit('!! 出现了第二个 class="td-browse-files"（抽屉树必须用 td-tf* 独立类名）')
    # 抽屉树（`.td-tf`）的行数由 `ev/patch108l1.py` 的白名单决定 = 10 行
    if out.count('<div class="td-tf') != 10:
        sys.exit('!! 抽屉树行数 %d（应 10）' % out.count('<div class="td-tf'))
    # ★ r108 第十八拍（头部两处的下游守卫）：
    #   ② 「最大化侧栏」按钮必须不在组装结果里。
    #      ⚠★ 判据**不能**写 `'data-td-max' in out`：`_mods.html` 的 demo diff 文本里
    #        逐字展示着 `&lt;button … aria-label="最大化" data-td-max="1"&gt;…`（转义后的**示例代码**）
    #        ⇒ 裸属性名必然误报。要取「真按钮」的整段特征（含 `&lt;` 与「最大化**侧栏**」的差异）。
    if '<button class="td-browse-ico" type="button" aria-label="最大化侧栏"' in out:
        sys.exit('!! 组装结果里仍有「最大化侧栏」按钮（第十八拍 ② 要删掉它）')
    #   ④ 菜单里 5 项的顺序必须是 摘要 → 审查 → 终端 → 浏览器 → 文件。
    order = re.findall(r'data-td-open-mod="([a-z]+)"', out)
    if order != ['summary', 'review', 'terminal', 'browser', 'files']:
        sys.exit('!! 菜单项顺序应为 summary/review/terminal/browser/files（实 %r）' % (order,))

    # ★★ r109 第一拍（邵先生需求 ①）：`.td-page-blank`（浏览器视图顶部那条 26px 灰带）
    #    必须从组装结果里消失。
    #    ⚠★ 判据**必须先剥掉 HTML 注释**再查 —— 本文件的那段说明注释里逐字写着
    #      `<div class="td-page-blank">&nbsp;</div>`（讲「这里原有…」），裸查必然误报。
    #      （这是 PLAYBOOK 里「判据不能写裸词，注释会误报」那条的又一次复现。）
    bare = re.sub(r'<!--.*?-->', '', out, flags=re.S)
    if 'class="td-page-blank"' in bare:
        sys.exit('!! 组装结果里仍有 class="td-page-blank"（第一拍 ① 要删掉它）')
    #   需求 ②：`.td-annot-bar` 仍在（只是改成置顶），且必须是 `.td-view` 的**首个子件**。
    if 'data-td-annot-bar' not in bare:
        sys.exit('!! 组装结果缺少 data-td-annot-bar（第一拍 ② 的落点）')
    i_view = bare.find('class="td-view"')
    i_bar = bare.find('data-td-annot-bar')
    i_page = bare.find('class="td-page"')
    if not (i_view < i_bar < i_page):
        sys.exit('!! .td-annot-bar 不是 .td-view 的首个子件（view@%d bar@%d page@%d）'
                 % (i_view, i_bar, i_page))
    #   需求 ③：`.td-url-annot` 的**标签文字**必须仍是初始态「标注」（运行期才换成「退出批注」）。
    if '<span>标注</span>' not in bare:
        sys.exit('!! 组装结果缺少 <span>标注</span>（第一拍 ③ 的初始态文案）')

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
