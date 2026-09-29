# -*- coding: utf-8 -*-
"""
第 71 轮 · 补丁 f（需求 2 一致性收尾）

apply71.py 给 task-detail 的收起加了 `transition-duration: 240ms`，注释写的是「与 JS 的 240ms 定时器对齐」。
但需求 2 的口径是「与 avatar 的动效**保持一致**」，而 avatar（r70 参考实现）的收起源码是：

    .td-browse-slot.av-slot-placed { transition: flex-basis 200ms var(--av-browse-ease); }
    /* 无任何 transition-duration 覆盖 → 展开/收起同为 200ms */

  ⇒ 展开：两页都 200ms  ✅
  ⇒ 收起：avatar 200ms / task-detail 240ms  ❌（且本页面板行程更长 1024 vs 641，240ms 更显拖沓）

修法：`transition-duration: 240ms` → `200ms`。JS 定时器 240ms **不动** ——
  它只是「摘 is-browse」的保险，视觉在 t=200 已到位；t∈[200,240] 期间
  `:has(> .is-closing)` 仍把 basis 钉在 0，摘类瞬间 basis 落回基础值 0，无跳变。

⚠️ 两页的 **CSS 机制**有一点结构性差异，这是必要的、不算「不一致」：
  · avatar：`setOpen(false)` **立刻**摘 `.av-browse-on` → basis 立即回落基础 0 → 过渡自然起跑，不需要额外规则；
  · task-detail：`.is-browse` 是在 `done()`（t=240ms）里才摘的 → 若没有 `:has` 那条规则，
    收起期间 basis 会一直停在 `calc(100% - 400px)`（不回弹）。
  用户可见的「时长 + 缓动 + 宽度舒展/收拢」两者现已完全一致。

幂等三要素：newmark 命中即 SKIP；OLD 恰好命中 1 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r71f-backup'
PAGE = 'task-detail.html'

MARK = u'\u6536\u8d77\u4e0e\u5c55\u5f00\u540c\u4e3a 200ms'

OLD = u'flex-basis: 0px;\n        /* \u6536\u8d77\u65f6\u957f\u4e0e JS \u7684 240ms \u5b9a\u65f6\u5668\u5bf9\u9f50\uff1a\u6536\u62e2\u5230\u4f4d\u7684\u540c\u4e00\u523b\u624d\u6458 is-browse\uff0c\n           \u5de6\u4fa7\u5185\u5bb9\u4e0d\u4f1a\u5148\u6d88\u5931\u3001\u7559\u51fa\u4e00\u6bb5\u7a7a\u6863\u518d\u300c\u556a\u300d\u5730\u56de\u6765\u3002 */\n        transition-duration: 240ms;'
NEW = (
    u'flex-basis: 0px;\n'
    u'        /* \u2605 \u7b2c 71 \u8f6e\uff1a\u6536\u8d77\u4e0e\u5c55\u5f00\u540c\u4e3a 200ms\uff0c\u4e0e avatar \u53c2\u8003\u5b9e\u73b0\u540c\u53e3\u5f84\n'
    u'           \uff08\u5b83\u7684 JS \u5b9a\u65f6\u5668 220ms\u3001\u672c\u9875 240ms\uff0c\u90fd\u53ea\u662f\u300c\u6458 is-browse\u300d\u7684\u4fdd\u9669\uff0c\u89c6\u89c9\u5728 t=200 \u5df2\u5230\u4f4d\uff09\u3002 */\n'
    u'        transition-duration: 200ms;'
)


def load():
    with io.open(os.path.join(ROOT, 'pages', PAGE), encoding='utf-8') as f:
        return f.read()


def save(s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    dst = os.path.join(BACKUP, PAGE)
    if not os.path.exists(dst):
        with io.open(os.path.join(ROOT, 'pages', PAGE), encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(os.path.join(ROOT, 'pages', PAGE), 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    for bad in ('</style', '</script', '<style', '<script', '</body', '</html'):
        if bad in payload:
            sys.exit('!! \u5143\u5b88\u536b\u5931\u8d25\uff1a%s \u8f7d\u8377\u542b %s' % (label, bad))


def main():
    guard(u'\u6536\u8d77\u65f6\u957f', NEW)
    s = load()
    before = s
    if MARK in s:
        print(u'\u5e94\u7528: 0 \u9879 | \u8df3\u8fc7: 1 \u9879\uff08\u6536\u8d77\u65f6\u957f\u5df2\u4e3a 200ms\uff09')
    else:
        n = s.count(OLD)
        if n != 1:
            sys.exit('!! \u951a\u70b9\u547d\u4e2d %d \u6b21\uff08\u671f\u671b 1\uff09\u2014\u2014 \u4e2d\u6b62' % n)
        s = s.replace(OLD, NEW)
        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != 0:
                sys.exit('!! \u6807\u7b7e\u8ba1\u6570\u5f02\u5e38 %s: \u0394%d' % (tag, d))
        save(s)
        print(u'\u5e94\u7528: 1 \u9879\uff08task-detail \u6536\u8d77\u65f6\u957f 240ms \u2192 200ms\uff09')

    # ================= 自检 =================
    print(u'\n--- \u81ea\u68c0 ---')
    t = load()
    checks = [
        (u'240ms \u6e05\u96f6', t.count(u'transition-duration: 240ms') == 0),
        (u'200ms \u6070\u597d\u4e00\u5904\uff08\u5373\u6536\u8d77\u89c4\u5219\uff09', t.count(u'transition-duration: 200ms;') == 1),
        (u'\u6536\u8d77\u89c4\u5219\u4ecd\u6302\u5728 :has \u4e0a',
         t.count(u'.td-root.is-browse .td-browse-slot:has(> .td-browse.is-closing)') == 1),
        (u'\u57fa\u7840\u8fc7\u6e21\u4ecd\u662f 200ms + \u540c\u4e00\u6761\u7f13\u52a8',
         t.count(u'flex-basis 200ms var(--td-browse-ease)') == 1),
        (u'\u5c55\u5f00\u57fa\u7840\u89c4\u5219\u5728\u4f4d', t.count(u'flex-basis: calc(100% - var(--td-browse-right-w, 480px));') == 1),
        (u'JS \u5b9a\u65f6\u5668\u4ecd\u4e3a 240ms\uff08\u672c\u8f6e\u4e0d\u6539 JS\uff09', t.count(u'setTimeout(done, 240)') == 1),
        (u'\u65e7\u5f4e\u4f4d\u79fb\u52a8\u753b\u4ecd\u4e3a 0', t.count(u'tdBrowseIn') + t.count(u'tdBrowseOut') == 0),
        (u'<style>/</style> \u914d\u5e73', t.count(u'<style') == t.count(u'</style>')),
    ]
    ok = 0
    for name, cond in checks:
        if cond:
            ok += 1
        else:
            print(u'  \u2717 %s' % name)
    print(u'自检\uff1a%d/%d \u901a\u8fc7' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
