# -*- coding: utf-8 -*-
"""
第 72 轮 · Esc 层级裁决（浏览态优先于跳页）

【问题】task-detail.html 浏览态下按真实 Esc 会直接跳 kanban.html，预览栏关不掉。

【根因（已取证，见 HANDOFF 第三节第 1 项 + 本轮复核）】
  两条监听都在 document 冒泡段 → 执行顺序 = 注册顺序：
    · 页尾链 —— 写在同步 <script> 里，页面初始化即注册（最早）；链尾
      `location.href = 'kanban.html'` 直接触发导航。
    · 浏览侧栏 —— **懒注册**（首次开侧栏才挂），永远排在页尾链之后。
  ⇒ 页尾链先跑并开始导航，侧栏那句 setOpen(false) 根本没机会执行。
  旁证：同页 ctx-open 分支被同一问题逼出 `e.__tdCtxHandled` 事件标记补丁（第 54 轮）。

【为什么不改成「捕获段 + stopPropagation」】
  捕获段能抢到优先级，但要新引入一条捕获段监听，且必须自己重排「谁是最高层浮层」
  （编辑弹窗 / 更多菜单 / 协作模态 / 转派浮窗 / 右键菜单 / 对话框弹层…各占一条捕获监听），
  条件一旦漏项就会出现「一次 Esc 关两层」。更稳且更同构的做法是**复用页尾链既有的派发模式**。

【改法】
  页尾链本来就用 `document.dispatchEvent(new CustomEvent('td:close-*'))` 派发给各浮层侧
  （image-preview / edit / coop / dispatch / ctx / popovers）。本轮新增一层
  `td:close-browse`，插在「全屏」分支之后、「跳转」分支之前：
    · 位置即优先级 —— 链上所有浮层都关完了，最后才轮预览栏；再按一次才真的回看板，
      符合「Esc 逐层关闭」惯例，且**全屏态既有语义一字未动**；
    · 不新增捕获段监听 → 零优先级冲突面；
    · 与链上其他分支同样只 `return`（不 stopPropagation），风格一致。

  浏览侧栏侧新增 `document.addEventListener('td:close-browse', () => setOpen(false))`。
  连按两次为何安全：第一次进 `pane.is-closing`（240ms 后才摘 is-browse），第二次
  `setOpen(false)` 命中 `if (pane.classList.contains('is-closing')) return;` 直接返回；
  第三次 is-browse 已摘 → 页尾链跳过浏览分支 → 正常回看板。

幂等三要素：newmark 命中即 SKIP；OLD 恰好命中 1 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r72-backup'
PAGE = 'task-detail.html'

MARK = u"'td:close-browse'"

# ---------- 改动 1：页尾 Esc 链插入「浏览态」分支 ----------
OLD1 = u"        location.href = 'kanban.html';\n      });"
NEW1 = (
    u'        /* \u2605 \u7b2c 72 \u8f6e\uff1a\u6d4f\u89c8\u6001\u4e0b Esc \u5148\u5173\u9884\u89c8\u680f\uff08\u8fde\u6309\u4e24\u6b21\u624d\u56de\u4efb\u52a1\u770b\u677f\uff09\u3002\n'
    u'           \u4f4d\u7f6e\u6709\u8bb2\u7a76\uff1a\u6392\u5728\u94fe\u4e0a\u6240\u6709\u6d6e\u5c42\u4e0e\u300c\u5168\u5c4f\u300d\u4e4b\u540e\u3001\u8df3\u8f6c\u4e4b\u524d \u2014\u2014\n'
    u'           \u5373\u300c\u8df3\u79bb\u9875\u9762\u524d\u7684\u6700\u540e\u4e00\u9053\u95e8\u300d\uff0c\u7b26\u5408 Esc \u9010\u5c42\u5173\u95ed\uff1b\u5168\u5c4f\u6001\u8bed\u4e49\u4e0d\u53d8\u3002\n'
    u'           \u9884\u89c8\u680f\u4fa7\u63a5\u4f4f\u8be5\u4e8b\u4ef6\uff08\u89c1 bindBrowse \u91cc setOpen \u65c1\u7684\u7ed1\u5b9a\uff09\u3002 */\n'
    u"        if (document.querySelector('.td-root.is-browse')) {\n"
    u"          document.dispatchEvent(new CustomEvent('td:close-browse'));\n"
    u'          return;\n'
    u'        }\n'
    + OLD1
)

# ---------- 改动 2：浏览侧栏接住该事件 ----------
OLD2 = u'        });\n\n        /* ---------- \u5206\u9694\u6761\u62d6\u52a8 ---------- */'
NEW2 = (
    u'        });\n\n'
    u'        /* \u2605 \u7b2c 72 \u8f6e\uff1a\u63a5\u4f4f\u9875\u5c3e\u94fe\u6d3e\u53d1\u7684\u6536\u8d77\u4e8b\u4ef6\uff08\u89c1\u9875\u5c3e Esc \u94fe\u7684\u6d4f\u89c8\u6001\u5206\u652f\uff09\u3002\n'
    u'           \u4e3a\u4f55\u4e0d\u6539\u4e0a\u9762\u90a3\u6761\u76d1\u542c\u7684\u6ce8\u518c\u65b9\u5f0f\uff1a\u5b83\u5728\u5192\u6ce1\u6bb5\u61d2\u6ce8\u518c\uff0c\u6c38\u8fdc\u665a\u4e8e\u9875\u5c3e\u94fe\uff0c\n'
    u'           \u62a2\u4e0d\u5230\u4f18\u5148\u7ea7\uff1b\u7531\u9875\u5c3e\u94fe\u4e3b\u52a8\u6d3e\u53d1\u624d\u662f\u53ef\u9760\u901a\u8def\u3002 */\n'
    u"        document.addEventListener('td:close-browse', function () { setOpen(false); });\n\n"
    u'        /* ---------- \u5206\u9694\u6761\u62d6\u52a8 ---------- */'
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
    guard(u'\u6d4f\u89c8\u6001\u5206\u652f', NEW1)
    guard(u'close-browse \u7ed1\u5b9a', NEW2)

    s = load()
    before = s

    if MARK in s:
        print(u'\u5e94\u7528: 0 \u9879 | \u8df3\u8fc7: 2 \u9879\uff08td:close-browse \u5df2\u5c31\u4f4d\uff09')
    else:
        applied = 0
        for label, old, new in ((u'\u9875\u5c3e\u94fe\u6d4f\u89c8\u6001\u5206\u652f', OLD1, NEW1),
                                (u'\u4fa7\u680f close-browse \u7ed1\u5b9a', OLD2, NEW2)):
            n = s.count(old)
            if n != 1:
                sys.exit('!! \u951a\u70b9\u547d\u4e2d %d \u6b21\uff08\u671f\u671b 1\uff09\u2014\u2014 %s\uff0c\u4e2d\u6b62' % (n, label))
            s = s.replace(old, new)
            applied += 1

        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != 0:
                sys.exit('!! \u6807\u7b7e\u8ba1\u6570\u5f02\u5e38 %s: \u0394%d' % (tag, d))
        save(s)
        print(u'\u5e94\u7528: %d \u9879\uff08task-detail Esc \u5c42\u7ea7\u88c1\u51b3\uff09' % applied)

    # ================= 自检 =================
    print(u'\n--- \u81ea\u68c0 ---')
    t = load()
    base = os.path.join(ROOT, 'mg-work', 'r72', 'before', PAGE)
    if os.path.exists(base):
        with io.open(base, encoding='utf-8') as f:
            b = f.read()
    else:
        b = before
    # 位置断言：全屏分支 < 浏览态派发 < 跳转
    p_fs = t.find(u"document.querySelector('.td-root.is-fullscreen')")
    p_disp = t.find(u"document.dispatchEvent(new CustomEvent('td:close-browse'))")
    p_go = t.rfind(u"location.href = 'kanban.html';")

    checks = [
        (u'\u88c1\u51b3\u4e8b\u4ef6\u540d\uff08\u5e26\u5f15\u53f7\uff09\u6070\u597d 2 \u5904\uff1a\u6d3e\u53d1 1 + \u7ed1\u5b9a 1', t.count(MARK) == 2),
        (u'\u9875\u5c3e\u94fe\u5171 1 \u5904\u6d4f\u89c8\u6001\u5206\u652f', t.count(u"if (document.querySelector('.td-root.is-browse'))") == 1),
        (u'\u56de\u770b\u677f\u8df3\u8f6c\u4ecd 2 \u5904\uff08\u8fd4\u56de\u6309\u94ae + \u9875\u5c3e\u94fe\uff09', t.count(u"location.href = 'kanban.html';") == 2),
        (u'\u9875\u5c3e\u94fe ctx \u4fee\u8865\u5b8c\u6574\uff08e.__tdCtxHandled\uff09', t.count(u'!e.__tdCtxHandled') == 1),
        (u'\u4fa7\u680f\u65e7\u76d1\u542c\u4ecd\u5728\uff08\u4ec5\u4f5c\u515c\u5e95\uff09', t.count(u"root.classList.contains('is-browse')") >= 1),
        (u'\u6536\u8d77\u5b9a\u65f6\u5668\u4ecd\u4e3a 240ms\uff08\u672c\u8f6e\u4e0d\u52a8\u52a8\u753b\uff09', t.count(u'setTimeout(done, 240)') == 1),
        (u'\u4f4d\u7f6e\uff1a\u5168\u5c4f\u5206\u652f < \u6d4f\u89c8\u6001\u6d3e\u53d1', 0 <= p_fs < p_disp),
        (u'\u4f4d\u7f6e\uff1a\u6d4f\u89c8\u6001\u6d3e\u53d1 < \u8df3\u8f6c', p_disp < p_go),
        (u'<style> \u6807\u7b7e\u6570\u4e0e\u57fa\u7ebf\u4e00\u81f4', t.count(u'<style') == b.count(u'<style')),
        (u'</style> \u6807\u7b7e\u6570\u4e0e\u57fa\u7ebf\u4e00\u81f4', t.count(u'</style>') == b.count(u'</style>')),
        (u'<script \u6807\u7b7e\u6570\u4e0e\u57fa\u7ebf\u4e00\u81f4\uff08\u672c\u9875\u57fa\u7ebf\u672c\u5c31 9v8\uff0c\u4e0d\u505a\u914d\u5e73\u65ad\u8a00\uff09', t.count(u'<script') == b.count(u'<script')),
        (u'</script \u6807\u7b7e\u6570\u4e0e\u57fa\u7ebf\u4e00\u81f4', t.count(u'</script') == b.count(u'</script')),
        (u'\u6539\u52a8\u540e\u672a\u65b0\u589e style/script \u6807\u7b7e',
         t.count(u'<style') == b.count(u'<style') and t.count(u'<script') == b.count(u'<script')),
    ]
    ok = 0
    for name, cond in checks:
        if cond:
            ok += 1
        else:
            print(u'  \u2717 %s' % name)
    print(u'\u81ea\u68c0\uff1a%d/%d \u901a\u8fc7' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
