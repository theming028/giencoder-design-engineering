# -*- coding: utf-8 -*-
"""r108 第十三拍 ⑤ —— 任务详情页（`pages/task-detail.html`）的「状态」徽章文字改 13px。

为什么单独一个脚本（不进 `patch108l2.py`）：
    `patch108l2.py` 改的是 r108 组装链的三件（`part108/{_mods.html,panel.css,panel.js}`），
    产物是**会话详情页**；task-detail.html 是另一页、另一条血脉（r42→…→r92 建成后只被
    r101/r102/r106 改过文案），既不参与 `splice108` 也不参与 `apply108` ⇒ 直接对页面落盘。

为什么只改本页、不改 DS 源：
    `.giencoder-badge-status-text` 是全站 DS 类（10 个页面都带）。邵先生点名的是「任务详情页的」
    ⇒ 按硬规则「不得改动其他不必涉及的模块」，只在**本页页级适配层**加一条覆盖。
    DS 侧的字号其实在父级 `.giencoder-badge-status{font-size:var(--font-size-body-3)}`（14px）上，
    文字节点自己不声明字号（继承）⇒ 给文字补 `--font-size-body-2`（13px）即可，无需特异性竞争。

用法： python mg-work/r108/ev/patch108td.py
      python mg-work/r108/ev/patch108td.py --revert   # 摘掉本块（回到原状）
"""
import argparse
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
TD = os.path.join(REPO, 'pages', 'task-detail.html')

# 锚点：本页最后一个样式块的收尾 + 紧随其后的脚本 ⇒ 新块插在两者之间。
# （task-detail.html 的样式块按轮次带 id：r73-popup-css / r74-* / r76-td-css / r77-pop-css / r81-ws-css）
ANCHOR = '</style><script id="r81-ws-js">'
# ⚠ 替换串要把锚点自己那两个 token 原样接回去（只多插一个 BLOCK），否则会留下双 `</style>`。
REPLACEMENT = '</style>' + '{{BLOCK}}' + '<script id="r81-ws-js">'

BLOCK = '''<style id="r108-td-css">
  /* ★ 第十三拍 ⑤：任务详情页「状态」徽章的文字改 13px。
     DS 的 `.giencoder-badge-status` 默认 `font-size: var(--font-size-body-3)`（14px），
     文字节点 `.giencoder-badge-status-text` 自己不声明字号（靠继承）⇒ 这里只给它补一条
     同档 token（`--font-size-body-2` = 13px），不动父级、不需要抬特异性。
     ⚠ 只落本页：该类是全站 DS 类，改 DS 源会连带动其余 9 页（硬规则「不得改动其他不必涉及的模块」）。 */
  .giencoder-badge-status-text { font-size: var(--font-size-body-2); }
</style>'''

MARK = '<style id="r108-td-css">'


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revert', action='store_true')
    a = ap.parse_args()

    t, nl = rd(TD)
    has = MARK in t

    if a.revert:
        if not has:
            print('   跳过  回退（本块不存在）')
            return
        i = t.find(MARK)
        j = t.find('</style>', i) + len('</style>')
        wr(TD, t[:i] + t[j:], nl)
        print('   应用  回退（摘掉 %d 字符）' % (j - i))
        return

    if has:
        print('   跳过  ⑤ 任务详情页徽章字号（已应用）')
        return

    n = t.count(ANCHOR)
    if n != 1:
        sys.exit('!! 锚点 %r 命中 %d 次（应 1 次）' % (ANCHOR, n))
    wr(TD, t.replace(ANCHOR, REPLACEMENT.replace('{{BLOCK}}', BLOCK), 1), nl)
    print('   应用  ⑤ 任务详情页徽章字号（%d → %d 字符）' % (len(t), len(t) + len(BLOCK)))


if __name__ == '__main__':
    main()
