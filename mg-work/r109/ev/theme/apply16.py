# -*- coding: utf-8 -*-
"""第十六拍 · ① r93-artgrid 产物卡可点开右栏浏览。

改法（与 ③④ 同族扩展，最小侵入）：
  A. `attShow(el)` 的文件名来源扩成三选一：
     `data-r93-att-file`（附件卡） / `data-r93-artname`（产物卡） / 空
  B. 委托锚点从 `[data-r93-att-file]` 扩到 `[data-r93-att-file],[data-r93-artname]`
  C. `meta` 尺寸文案：产物卡读卡内 `.r93-artmeta`（"128KB"）⇒ 走同一张 SIZE_BY_EXT 表

只动 `pages/conversation.html` 一处 JS 段。
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, u'..', u'..', u'..', u'..'))
PAGE = os.path.join(ROOT, u'pages', u'conversation.html')


def _read(p):
    with io.open(p, 'rb') as f:
        return f.read().decode('utf-8').replace(u'\r\n', u'\n')


def _write(p, t):
    with io.open(p, 'wb') as f:
        f.write(t.replace(u'\n', u'\r\n').encode('utf-8'))


# ---------------- EDIT 1: attShow 名字来源扩成两种 ----------------
ATT_NAME_OLD = (
    u"      var name = el.getAttribute('data-r93-att-file') || '\u6587\u4ef6';\n"
    u"      var ext = (name.split('.').pop() || '').toLowerCase();\n"
)
ATT_NAME_NEW = (
    u"      /* \u2605 r109 \u7b2c\u5341\u516d\u62cd \u2460\uff08\u90b5\u5148\u751f\uff1a\u300c\u5361\u7247\"r93-artgrid\"\u7684\u6587\u4ef6\u4e5f\u8981\u652f\u6301\u70b9\u51fb\u540e\u5c55\u5f00\u53f3\u680f\u6d4f\u89c8\u300d\uff09\uff1a\n"
    u"         \u6587\u4ef6\u540d\u6765\u6e90\u6269\u6210**\u4e24\u79cd** \u2014\u2014 \u9644\u4ef6\u5361 `data-r93-att-file`\uff08r109-l12 \u5c31\u6709\uff09\n"
    u"         \u4e0e\u4ea7\u7269\u5361 `data-r93-artname`\uff08r101 \u2466 \u4e3a\u53f3\u952e\u83dc\u5355\u300c\u590d\u5236\u8def\u5f84\u300d\u8865\u7684\uff09\u3002\n"
    u"         \u2605 \u4e24\u8005**\u540c\u6784**\uff1a\u90fd\u662f\u300c\u5361\u4e0a\u6302\u4e00\u4e2a\u6587\u4ef6\u540d\u5c5e\u6027 + \u5361\u5185\u4e00\u679a 24px \u56fe\u6807\u300d\n"
    u"         \u21d2 \u5171\u7528\u540c\u4e00\u5957\u9aa8\u67b6\u5207\u6362 / \u6587\u6848\u586b\u5145 / \u72ec\u7acb\u9875\u7b7e\u903b\u8f91\uff0c\u4e0d\u518d\u53e6\u8d77\u4e00\u4efd\u3002\n"
    u"         \u26a0 `\u67e5\u770b\u6240\u6709\u4ea7\u7269 (12)` \u4e0d\u662f\u6587\u4ef6 \u21d2 r101 \u2466 \u5c31\u6ca1\u7ed9\u5b83\u6253 `data-r93-artname`\uff0c\u8fd9\u91cc\u81ea\u7136\u4e0d\u4f1a\u88ab\u547d\u4e2d\u3002 */\n"
    u"      var name = el.getAttribute('data-r93-att-file')\n"
    u"        || el.getAttribute('data-r93-artname') || '\u6587\u4ef6';\n"
    u"      var ext = (name.split('.').pop() || '').toLowerCase();\n"
)

# ---------------- EDIT 2: ico 选择器扩成两种 ----------------
ATT_ICO_OLD = (
    u"      var ico = el.querySelector('.r93-iblk svg');\n"
    u"      var meta = (SIZE_BY_EXT[ext] || '\u6587\u4ef6') + ' \u00b7 \u53ea\u8bfb\u9884\u89c8';\n"
)
ATT_ICO_NEW = (
    u"      /* \u56fe\u6807\uff1a\u9644\u4ef6\u5361 = `.r93-iblk svg`\uff1b\u4ea7\u7269\u5361 = `.r93-artic svg`\uff08\u5361\u5185\u90a3\u679a 24px \u56fe\u6807\u5b50\u76d2\uff09\u3002\n"
    u"         \u5148\u8bd5 `.r93-iblk`\uff08\u9644\u4ef6\u5361\u7528\uff09\u3001\u518d\u56de\u9000 `.r93-artic`\uff08\u4ea7\u7269\u5361\u7528\uff09\u3002 */\n"
    u"      var ico = el.querySelector('.r93-iblk svg') || el.querySelector('.r93-artic svg');\n"
    u"      /* \u5c3a\u5bf8\u6587\u6848\uff1a\u4ea7\u7269\u5361\u628a `128KB` \u5199\u5728\u5361\u5185 `.r93-artmeta`\uff08\u6bd4\u6269\u5c55\u540d\u67e5\u8868\u66f4\u771f\u5b9e\uff09\n"
    u"         \u21d2 \u6709\u5c31\u8bfb\u5b83\u3001\u6ca1\u6709\u624d\u56de\u9000\u5230 `SIZE_BY_EXT` \u8868\u3002 */\n"
    u"      var mt = el.querySelector('.r93-artmeta');\n"
    u"      var size = mt && mt.textContent ? mt.textContent.replace(/\\s+/g, '') : '';\n"
    u"      var meta = (size ? size + ' \u00b7 ' : '') + (size ? '\u53ea\u8bfb\u9884\u89c8'\n"
    u"        : (SIZE_BY_EXT[ext] || '\u6587\u4ef6') + ' \u00b7 \u53ea\u8bfb\u9884\u89c8');\n"
)

# ---------------- EDIT 3/4: 委托锚点扩成两种 ----------------
CLA_OLD = u"ev.target.closest('[data-r93-att-file]')"
CLA_NEW = u"ev.target.closest('[data-r93-att-file],[data-r93-artname]')"

EDITS = [
    (u'att-name', ATT_NAME_OLD, ATT_NAME_NEW, 1),
    (u'att-ico', ATT_ICO_OLD, ATT_ICO_NEW, 1),
    (u'att-cla1', CLA_OLD, CLA_NEW, 2),
]


def main():
    t = _read(PAGE)
    total = 0
    changed = []
    for name, old, new, want in EDITS:
        if (new in t) and (t.count(old) == new.count(old)):
            print(u'  [skip] %-12s \u5df2\u662f\u76ee\u6807\u6001' % name)
            continue
        if (old not in t) and (old not in new):
            print(u'  [skip] %-12s \u5df2\u662f\u76ee\u6807\u6001' % name)
            continue
        c = t.count(old)
        if c != want:
            raise SystemExit(u'[FATAL] %s \u547d\u4e2d %d \u5904\uff0c\u671f\u671b %d' % (name, c, want))
        t = t.replace(old, new)
        total += c
        changed.append(name)
    print(u'\u66ff\u6362\u603b\u6570 = %d  \u53d8\u66f4 = %s' % (total, changed))
    if total:
        _write(PAGE, t)
        print(u'[OK] \u5df2\u5199\u56de %s' % PAGE)


if __name__ == '__main__':
    main()
