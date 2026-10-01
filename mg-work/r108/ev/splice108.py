# -*- coding: utf-8 -*-
"""r108 · 组装 `part108/browse.html`。

体位与 `ev/splice107.py` 一致：**从 r105 移植件里「剪」出 Files 正文逐字复用**，
只把「头部」换掉、后面追加新模块。

  part105/browse.html = <split><slot><aside> + <header …> + <div.td-browse-body>…(Files 正文) + </aside></div>

  新文件 = <split><slot><aside> + part107/_head.html + 【原 <div.td-browse-body>… 逐字】 + part108/_mods.html + </aside></div>

⇒ 「文件」模块的 DOM 与 r105/r106/r107 完全一致（r106 的 44px 适配层、ctrl-conv.js 的选择器全部继续成立），
  r108 的改动面 = `_mods.html` 末尾追加的文件树抽屉 + 审查工具条里那枚新按钮。

★ 与 r107 的唯一差别：`_head.html` **本代已覆盖**（第十八拍 ② 删「最大化侧栏」按钮 +
  ④ 菜单里「摘要」挪到第一项）⇒ 从 **part108** 取；`_mods.html` 也从 part108 取。
  ★ 体位（硬规则「要改跨代资产 ⇒ 放本代同名覆盖件」）：`part107/_head.html` **一字未动**，
    本代先 `cp` 成 `part108/_head.html` 再由 `ev/patch108l7.py` 打两处改动。

用法： python mg-work/r108/ev/splice108.py           # 写 part108/browse.html
      python mg-work/r108/ev/splice108.py --check   # 只校验（不写）
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
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
OUT = os.path.join(P108, 'browse.html')


def read(p):
    return io.open(p, encoding='utf-8').read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    src = read(SRC)
    # ★ r108 第十八拍：头部改由**本代覆盖件**提供（原从 part107 取）。
    #   回退链：part108/_head.html 不存在时退回 part107 —— 但那样 ②④ 就不生效，
    #   所以这里宁可硬失败，避免「静默用了旧头部」这种最难查的错。
    head_path = os.path.join(P108, '_head.html')
    if not os.path.exists(head_path):
        sys.exit('!! 缺少本代头部覆盖件 %s（第十八拍 ②④ 的落点）' % head_path)
    head = read(head_path)
    mods = read(os.path.join(P108, '_mods.html'))

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
