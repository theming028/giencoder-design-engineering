# -*- coding: utf-8 -*-
"""
第 73 轮 · 补丁 a（需求 2 + 需求 4，都只动 base.html）

【需求 2】撤销「新会话」液态玻璃
  第 71 轮在 base.html 尾部加了 `<style id="r71-glass-css">` 整块（作用于 .new-chat-btn：
  backdrop-filter 模糊 + 三层 inset 高光 + ::before 棱边色散 + ::after hover 扫光）。
  用户反馈观感不理想 → 恢复原样。
  ✅ 已对照 mg-work/r71/before/base.html 确认：r71 之前**既没有**该样式块、也没有 --nc-glass 变量；
     且共享样式表里的 .new-chat-btn 规则两版**逐字一致**（未被 r71 改动）
     ⇒ 只需删掉这一块，按钮即完全回到 React 内联样式的原样，无需回退别处。

  实现：把整块 `<style id="r71-glass-css">…</style>` **替换**为本轮新的 `<style id="r73-css">`。
  · 替换而非增删 ⇒ `<style>` / `</style>` 计数 Δ 恰好为 0（可断言）
  · 新块沿用同一位置（页面尾部、共享样式表之后）—— 这个层叠位置是 r71 验证过的，
    后续需求 1 / 需求 5 的覆盖规则也挂在这里。

【需求 4】基础工作台 main 底部版权区：鼠标移入文字加深一级
  版权区是 React 产物，className 走 Tailwind 任意值 `[color:var(--color-text-4)]`，
  无 data-* 钩子 → 只能按 class 特征选。
  实测（agent-browser，base.html）：`main div[class*=pb-6][class*=text-center]` **唯一命中** 1 个容器，
  内含 2 个 <p>（「内容由 AI 生成，请核实重要信息」/「© 2026 中电金信研究院 · …」），
  计算色 rgb(201,201,201) = --color-text-4（rgb(var(--gray-4))）。
  加深一级 ⇒ --color-text-4 → **--color-text-3**（rgb(var(--gray-6))）。
  :hover 挂在容器上（比挂 <p> 更好触发），颜色由 <p> 继承。
  ⚠️ avatar.html 也有一处同款版权区，但用户只点了「基础工作台」⇒ **不在本轮范围，未动**。

幂等三要素：newmark 命中即 SKIP；定位失败/命中数异常即 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r73-backup'
PAGE = 'base.html'

MARK = u'<style id="r73-css">'
BLOCK_START = u'<style id="r71-glass-css">'
BLOCK_END = u'</style>'

NEW = (
    u'<style id="r73-css">\n'
    u'  /* ★ 第 73 轮 · 需求 2：已移除第 71 轮加的「新会话」液态玻璃样式块，\n'
    u'     按钮回到 React 内联样式原样（共享样式表里的「新会话」按钮规则本就一字未改）。 */\n'
    u'\n'
    u'  /* ★ 第 73 轮 · 需求 4：基础工作台 main 底部版权区 —— 鼠标移入时文字加深一级。\n'
    u'     版权区是 React 产物（className 走 Tailwind 任意值 color:var(--color-text-4)），\n'
    u'     无 data-* 钩子，只能按 class 特征选：main 下同时含 pb-6 与 text-center 的容器\n'
    u'     —— 实测本页内唯一命中（内含 2 个 <p>）。\n'
    u'     加深一级 = --color-text-4（gray-4 / rgb(201,201,201)）→ --color-text-3（gray-6）。\n'
    u'     :hover 挂容器（比挂 <p> 更好触发），颜色由 <p> 继承；时长用 DS 的 duration-1 档。 */\n'
    u'  main div[class*="pb-6"][class*="text-center"] {\n'
    u'    transition: color var(--transition-duration-1) ease;\n'
    u'  }\n'
    u'  main div[class*="pb-6"][class*="text-center"]:hover,\n'
    u'  main div[class*="pb-6"][class*="text-center"]:hover p {\n'
    u'    color: var(--color-text-3) !important;\n'
    u'  }\n'
    u'</style>'
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


def main():
    s = load()
    before = s

    if MARK in s:
        print(u'应用: 0 项 | 跳过: 2 项（r73-css 块已就位）')
    else:
        n = s.count(BLOCK_START)
        if n != 1:
            sys.exit('!! 锚点命中 %d 次（期望 1）—— 中止' % n)
        i = s.find(BLOCK_START)
        j = s.find(BLOCK_END, i)
        if j < 0:
            sys.exit('!! 找不到块结束标签 —— 中止')
        OLD = s[i:j + len(BLOCK_END)]

        # 确认删掉的确实是那个玻璃块，不是别的
        for must in (u'--nc-glass', u'new-chat-btn', u'backdrop-filter'):
            if must not in OLD:
                sys.exit('!! 待删块内容不符（缺 %s）—— 中止' % must)
        if len(OLD) < 2000:
            sys.exit('!! 待删块过短（%d 字节）—— 中止' % len(OLD))

        s = s[:i] + NEW + s[j + len(BLOCK_END):]

        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != 0:
                sys.exit('!! 标签计数异常 %s: Δ%d' % (tag, d))
        save(s)
        print(u'应用: 2 项（删除 %d 字节玻璃块 + 写入版权区 hover 规则）' % len(OLD))

    # ================= 自检 =================
    print(u'\n--- 自检 ---')
    t = load()
    sel = u'main div[class*="pb-6"][class*="text-center"]'
    checks = [
        (u'旧玻璃块已消失（--nc-glass 归零）', t.count(u'--nc-glass') == 0),
        (u'旧玻璃块起始标签归零', t.count(BLOCK_START) == 0),
        (u'旧玻璃块的过渡时长变量也归零', t.count(u'--nc-glass-dur') == 0),
        (u'new-chat-btn 计数回到 r71 前的 5', t.count(u'new-chat-btn') == 5),
        (u'r73 块恰好 1 个', t.count(MARK) == 1),
        (u'版权区选择器恰好 3 次（1 基础 + 2 hover）', t.count(sel) == 3),
        (u'加深目标为 text-3', t.count(u'color: var(--color-text-3) !important;') == 1),
        (u'过渡走 DS duration-1 档', t.count(u'var(--transition-duration-1) ease') == 1),
        (u'<style> 计数与基线一致', t.count(u'<style') == before.count(u'<style')),
        (u'</style> 计数与基线一致', t.count(u'</style>') == before.count(u'</style>')),
        (u'<script> 计数与基线一致', t.count(u'<script') == before.count(u'<script')),
    ]
    ok = 0
    for name, cond in checks:
        if cond:
            ok += 1
        else:
            print(u'  ✗ %s' % name)
    print(u'自检：%d/%d 通过' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
