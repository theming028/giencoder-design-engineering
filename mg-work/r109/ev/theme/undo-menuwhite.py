# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 精确摘除器（把页面还原到「第十拍定稿态」）。

背景：apply-menuwhite.py 的 snapshot() 在第 2/3 遍时**覆盖了干净快照**
⇒ --revert 无法回到干净态（这是本层流程失误，已记入红线）。
本脚本不依赖快照，而是**逆运算**第 11 拍的两步改动：
  1) 删掉 <style id="r109-menuwhite-css">…</style> 整块
  2) var(--color-bg-1) 还原成原写法（按所在上下文选正确的原串）
  3) step1b 的 0.88 还原成 0.9
然后重新写入 ev/bak-menuwhite/ 作为**干净快照**。
"""
import argparse
import collections
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')
BAK = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-menuwhite')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

BLOCK_ID = u'r109-menuwhite-css'
RE_BLOCK = re.compile(u'<style id="%s">.*?</style>\\n?' % BLOCK_ID, re.S)

# ⚠ 必须带**选择器/上下文**做唯一还原：页面里本来就有大量 `var(--color-bg-1)`
#   （实测 61 处），裸串还原会误伤既有规则。
RESTORE = [
    # .giencoder-select-popup（CSS，无空格）
    (u'.giencoder-select-popup{z-index:1000;background:var(--color-bg-1)',
     u'.giencoder-select-popup{z-index:1000;background:rgba(var(--gray-1),0.88)'),
    # .skills-popup-bg —— 经核：本层从未改到它（它一直是 rgba(var(--gray-1), 0.88)）
    #   ⇒ 不需要还原条目（保留注释说明，避免后人误加）
    # .td-skill-pop（avatar/task-detail，跨行书写）—— 文件是 CRLF ⇒ 用正则匹配
    (re.compile(u'background: var\\(--color-bg-1\\);\\s*\\r?\\n\\s*-webkit-backdrop-filter: blur\\(10px\\) saturate\\(100%\\)'),
     u'background: rgba(var(--gray-1), 0.88);\\r\\n        -webkit-backdrop-filter: blur(10px) saturate(100%)'),
    # JS 三处（模板串）
    (u'borderRadius:`8px`,background:`var(--color-bg-1)`',
     u'borderRadius:`8px`,background:`rgba(var(--gray-1), 0.88)`'),
    (u'width:180,height:92,background:`var(--color-bg-1)`',
     u'width:180,height:92,background:`rgba(var(--gray-1), 0.88)`'),
    (u'width:760,height:320,borderRadius:12,background:`var(--color-bg-1)`',
     u'width:760,height:320,borderRadius:12,background:`rgba(var(--gray-1), 0.88)`'),
    # step1b 逆（产物为「冒号后有空格、逗号后无空格」的 0.88 —— 见 apply 里 ★★ 注释）
    (u"html[giencoder-theme='dark'] .td-skill-pop { background: rgba(var(--gray-1),0.88) !important; }",
     u"html[giencoder-theme='dark'] .td-skill-pop { background: rgba(var(--gray-1), 0.9) !important; }"),
    (u"html[giencoder-theme='dark'] .skills-popup-bg { background: rgba(var(--gray-1),0.88) !important;",
     u"html[giencoder-theme='dark'] .skills-popup-bg { background: rgba(var(--gray-1), 0.9) !important;"),
]


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def norm(t):
    return t.replace(u'\r\n', u'\n')


def comment_spans(t):
    out = []
    i, n = 0, len(t)
    while i < n:
        a = t.find(u'/*', i)
        if a < 0:
            break
        e = t.find(u'*/', a + 2)
        if e < 0:
            out.append((a, n))
            break
        out.append((a, e + 2))
        i = e + 2
    i = 0
    while i < n:
        a = t.find(u'<!--', i)
        if a < 0:
            break
        e = t.find(u'-->', a + 4)
        if e < 0:
            out.append((a, n))
            break
        out.append((a, e + 3))
        i = e + 3
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    sink = collections.Counter()
    per = collections.OrderedDict()
    staged = []
    for pg in ALL:
        p = os.path.join(PAGES, pg + u'.html')
        t = rd(p)
        before = len(norm(t))
        # 1) 去覆盖块
        n = 0
        while True:
            m = RE_BLOCK.search(t)
            if not m:
                break
            t = t[:m.start()] + t[m.end():]
            n += 1
        sink[u'(block-removed)'] += n
        # 2) 还原字面（跳过注释区，逐次重算；支持「正则 / 字面」两种 pattern）
        for pat, old in RESTORE:
            i = 0
            while True:
                spans = comment_spans(t)
                if hasattr(pat, u'search'):
                    m = pat.search(t, i)
                    if not m:
                        break
                    k, e = m.start(), m.end()
                else:
                    k = t.find(pat, i)
                    if k < 0:
                        break
                    e = k + len(pat)
                if any(a <= k < b for a, b in spans):
                    i = e
                    continue
                t = t[:k] + old + t[e:]
                sink[pat if not hasattr(pat, u'search') else pat.pattern] += 1
                i = k + len(old)
        per[pg] = len(norm(t)) - before
        if t != rd(p):
            staged.append((p, t))
    print(u'=== 第十一拍 · 精确摘除（%s）===' % (u'检查' if args.check else u'落盘'))
    print()
    print(u'  覆盖块移除 %d 处' % sink[u'(block-removed)'])
    for pat, _old in RESTORE:
        key = pat if not hasattr(pat, u'search') else pat.pattern
        label = key if isinstance(key, str) else key
        print(u'  还原 ×%-3d %s' % (sink[key], label[:62]))
    print()
    print(u'── 每页字符数变化（相对当前）──')
    for pg, d in per.items():
        print(u'   %-12s %+d' % (pg, d))
    if not args.check:
        # 写干净快照（供 --revert）
        if os.path.isdir(BAK):
            shutil.rmtree(BAK)
        os.makedirs(BAK)
        for p, t in staged:
            wr(p, t)
            shutil.copy2(p, os.path.join(BAK, os.path.basename(p)))
        print()
        print(u'  干净快照已重建 → ev/bak-menuwhite/（%d 页）' % len(staged))
    return 0


if __name__ == '__main__':
    sys.exit(main())
