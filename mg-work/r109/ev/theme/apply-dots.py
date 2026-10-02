# -*- coding: utf-8 -*-
r"""r109 第十一拍 ③ · 去掉「设置页面」的波点背景效果。

★ 邵先生原话（第十一拍 #3）：
    「去掉设置页面的波点背景效果。」

★ 现状（真机取证 raw/dots11/settings-{light,dark}.json）：
  settings 页 <main> 的真实背景 = 
    浅色档 radial-gradient(circle, rgba(107,107,107,0.1) 1.5px, transparent 1.5px) / 20px 20px
    暗色档 radial-gradient(circle, rgba(201,201,201,0.1) 1.5px, transparent 1.5px) / 20px 20px
  载体 = <main class="… bg-white dot-bg …">（类名 dot-bg 由 JS 挂上）。
  `.dot-bg` 的 CSS **定义在共享 DS 编译包内**（10 页共用）⇒ 直接改它会波及其它 9 页。

★★ 但 `bg-white dot-bg` 这个 class 组合在 **7 页**都存在
   （base / conversation / dev / kanban / req-kanban / settings / task-detail），
   7 页的 <main> 结构**逐字相同**、无 page-specific class/id ⇒
   纯 CSS 选择器无法区分「settings 的 main」与其它 6 页的 main。

★ 修法（最小侵入、只影响 settings、可逆、不碰 DS 编译包）：
  1) 给 settings.html 的 <html> 标签加一个**页面专属属性** `data-r109-nodots="1"`
     —— 静态 HTML 属性，不参与任何 JS 逻辑，零副作用。
  2) 在真 </head> 前追加覆盖块 `r109-nodots-css`：
       html[data-r109-nodots="1"] .dot-bg { background-image: none !important; }
     —— 只有 settings 页带该属性 ⇒ 其余 6 页的波点**逐像素不变**。

★ 真机验证（本层落地前）：注入同款规则 + 同款属性 ⇒
   getComputedStyle(main).backgroundImage === 'none' ✅

★ 幂等判据：① `<html … data-r109-nodots="1">` 恰好 1 处；
            ② 覆盖块内容（规范化换行后）与目标逐字符相同；
            ③ 重跑计数全为 0。
★ 回滚：python apply-dots.py --revert（摘属性 + 摘块；快照 ev/bak-dots/）
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
BAK = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-dots')

# 只有 settings 页需要处理
TARGET = u'settings'

RE_DS_BUNDLE = re.compile(re.escape(u':root{--giencoderblue-1:245, 248, 255'))

ATTR = u'data-r109-nodots'
BLOCK_ID = u'r109-nodots-css'

# settings 页的 <html> 标签（当前形态——须精确匹配）
HTML_OLD = u'<html lang="zh-CN" data-gi-dark="1">'
HTML_NEW = u'<html lang="zh-CN" data-gi-dark="1" data-r109-nodots="1">'

DOTS_BLOCK = u'''<style id="r109-nodots-css">
  /* ★ r109 第十一拍 ③：去掉**设置页面**的波点背景（邵先生 #3）。
     `.dot-bg` 的定义在共享 DS 编译包里（10 页共用）+ 7 页的 <main> class 逐字相同，
     故用「页面专属属性」锁作用域：只有 settings.html 的 <html> 带 data-r109-nodots="1"，
     其余 6 页（base/conversation/dev/kanban/req-kanban/task-detail）波点逐像素不变。
     浅暗双档同时生效（background-image 一置空，两档的 radial-gradient 都没了）。
     摘掉本块 + 去掉 <html> 上的 data-r109-nodots 属性即回滚。 */
  html[data-r109-nodots="1"] .dot-bg,
  html[data-r109-nodots="1"] main.dot-bg{
    background-image: none !important;
  }
</style>
'''

RE_BLOCK = re.compile(u'<style id="%s">.*?</style>\\r?\\n?' % BLOCK_ID, re.S)
RE_ATTR = re.compile(u'<html[^>]*\\b%s="1"[^>]*>' % ATTR)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def norm(t):
    return t.replace(u'\r\n', u'\n')


def comment_spans(t):
    u"""注释区间（顺序扫描，见 apply-menuwhite.py 同函数的教训说明）。"""
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


def real_head(t):
    spans = comment_spans(t)
    hits = []
    i = 0
    while True:
        k = t.find(u'</head>', i)
        if k < 0:
            break
        if not any(a <= k < b for a, b in spans):
            hits.append(k)
        i = k + 7
    return hits[0] if len(hits) == 1 else None


def apply_page(t, pg, sink, warn):
    u"""① 加页面属性 ② 注入覆盖块。每步都重算，避免偏移错位。"""
    # ── ① <html> 属性 ──
    own = RE_BLOCK.search(t)
    n_attr = len(RE_ATTR.findall(t))
    if n_attr == 0:
        # 确认唯一目标串存在
        cnt = t.count(HTML_OLD)
        if cnt != 1:
            warn.append(u'%s：<html> 目标串 %d 处（应为 1），拒绝改写' % (pg, cnt))
        else:
            spans = comment_spans(t)
            k = t.find(HTML_OLD)
            if any(a <= k < b for a, b in spans):
                warn.append(u'%s：<html> 命中落在注释里' % pg)
            else:
                t = t[:k] + HTML_NEW + t[k + len(HTML_OLD):]
                sink[u'(attr-add)'] += 1
    elif n_attr == 1:
        sink[u'(attr-already)'] += 1
    else:
        warn.append(u'%s：%s 已存在 %d 处（应为 ≤1）' % (pg, ATTR, n_attr))

    # ── ② 覆盖块 ──
    blk = DOTS_BLOCK
    m = RE_BLOCK.search(t)
    if m:
        if norm(m.group(0)) == norm(blk):
            sink[u'(block-already)'] += 1
        else:
            t = t[:m.start()] + blk + t[m.end():]
            sink[u'(block-refresh)'] += 1
    else:
        h = real_head(t)
        if h is None:
            warn.append(u'%s：真 </head> 不唯一，拒绝注入覆盖块' % pg)
        else:
            t = t[:h] + blk + t[h:]
            sink[u'(block-insert)'] += 1
    return t


def snapshot(force=False):
    if os.path.isdir(BAK) and not force:
        print(u'  ⚠ 快照已存在，跳过（需覆盖请加 --force）')
        return
    if os.path.isdir(BAK):
        shutil.rmtree(BAK)
    os.makedirs(BAK)
    src = os.path.join(PAGES, TARGET + u'.html')
    shutil.copy2(src, os.path.join(BAK, TARGET + u'.html'))
    print(u'  快照 → ev/bak-dots/%s.html' % TARGET)


def revert():
    src = os.path.join(BAK, TARGET + u'.html')
    if not os.path.exists(src):
        print(u'✗ 无快照：%s' % src)
        return 2
    shutil.copy2(src, os.path.join(PAGES, TARGET + u'.html'))
    print(u'✓ 已从快照还原 %s.html' % TARGET)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--revert', action='store_true')
    args = ap.parse_args()
    if args.revert:
        return revert()

    sink = collections.Counter()
    warn, problems = [], []
    p = os.path.join(PAGES, TARGET + u'.html')
    t = rd(p)
    if not RE_DS_BUNDLE.search(t):
        problems.append(u'%s：找不到 DS 编译包指纹' % TARGET)
    before = len(norm(t))
    t2 = apply_page(t, TARGET, sink, warn)
    after = len(norm(t2))
    if warn:
        problems.append(u'／'.join(warn))
    if problems:
        print(u'✗ 前置校验失败，拒绝落盘：')
        for x in problems:
            print(u'   ' + x)
        return 2
    if t2 != t and not args.check:
        snapshot()
        wr(p, t2)

    print(u'=== r109 第十一拍 ③ · 去掉设置页波点（%s）==='
          % (u'检查' if args.check else u'落盘'))
    print(u'  [属性] 添加 %d / 已存在 %d' % (sink[u'(attr-add)'], sink[u'(attr-already)']))
    print(u'  [覆盖块] 注入 %d / 刷新 %d / 已就绪 %d'
          % (sink[u'(block-insert)'], sink[u'(block-refresh)'], sink[u'(block-already)']))
    print(u'  字符数变化（规范化）= %+d' % (after - before))
    return 0


if __name__ == '__main__':
    sys.exit(main())
