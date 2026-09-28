#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r62：kanban.html「执行中」卡片标题文字流光（Text Shimmer）

需求（邵先生 2026-09-28）：
  任务看板「进行中」泳道里，状态为「执行中」的卡片，其标题 .kb-card-title
  要有文字流光动效；具体效果复刻 https://motion-primitives.com/docs/text-shimmer，
  但配色换成 GienCoder 设计系统 token（选定方案：灰底 + 深灰扫光，原版复刻）。

原版机制（已从官方 registry JSON 取回原文，非凭记忆）：
  · className: bg-[length:250%_100%,auto] + bg-clip-text + text-transparent
  · --bg = linear-gradient(90deg, #0000 calc(50% - var(--spread)), <hi>, #0000 calc(50% + var(--spread)))
  · backgroundImage = var(--bg), linear-gradient(<base>, <base>)
  · initial backgroundPosition '100% center' → animate '0% center'
  · transition { repeat: Infinity, duration: 2, ease: 'linear' }
  · dynamicSpread = children.length * spread(spread 默认 2)，写进 --spread（px）
本页落地：色值换成 --color-text-3(静置) / --color-text-1(高光)。

触发条件：卡片内存在「执行中」状态标签 .kb-running（= 该卡状态为执行中）。

幂等：每处替换带独立 MARK，命中即 SKIP。
"""
import io
import os
import sys

P = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pages', 'kanban.html'))

SHIMMER_CSS = """      /* ★ 第 62 轮：「执行中」卡片标题文字流光（Text Shimmer）
         复刻 motion-primitives.com/docs/text-shimmer 的机制（原文取自官方 registry，非凭记忆）：
           · 两层背景：上层 = 移动的高光带，下层 = 静置底色；
           · background-size: 250% 100% —— 高光带横向 2.5 倍于文字宽，扫动全程铺满不漏底；
           · background-clip: text + 文字透明 → 把背景裁进字形（原版做法）；
           · background-position 从 100% 线性扫到 0%，2s 一轮、无限循环（原版 duration=2）。
           · 高光带宽 = 字数 × spread(2)，由 JS 写入 --kb-shimmer-spread，20px 兜底。
         配色全部走 DS token（原版硬编码 #a1a1aa / #000）：
           静置色 = --color-text-3(#868686) · 高光色 = --color-text-1(#1F1F1F)
         触发 = 卡片内存在「执行中」状态标签 .kb-running。
         写法上放在整个样式表最末：与 .kb-card:hover .kb-card-title(0,3,0) 同特异性，
         靠「后写」取胜，避免将来新增同权重规则被抢先。 */
      @keyframes kb-title-shimmer {
        from { background-position: 100% center, 100% center; }
        to   { background-position: 0% center, 0% center; }
      }
      .kb-card:has(.kb-running) .kb-card-title {
        --kb-shimmer-spread: 20px;
        background-image:
          linear-gradient(90deg,
            #0000 calc(50% - var(--kb-shimmer-spread)),
            var(--color-text-1),
            #0000 calc(50% + var(--kb-shimmer-spread))),
          linear-gradient(var(--color-text-3), var(--color-text-3));
        background-size: 250% 100%, auto;
        background-repeat: no-repeat;
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        -webkit-text-fill-color: transparent;
        animation: kb-title-shimmer 2s linear infinite;
      }
      /* 无障碍：偏好减弱动效时退回普通标题色，不做流光 */
      @media (prefers-reduced-motion: reduce) {
        .kb-card:has(.kb-running) .kb-card-title {
          animation: none;
          background-image: none;
          color: var(--color-text-1);
          -webkit-text-fill-color: currentColor;
        }
      }
"""

SHIMMER_JS = """  /* ★ 第 62 轮：「执行中」卡片标题文字流光（Text Shimmer）
     —— 复刻 motion-primitives.com/docs/text-shimmer 的 JS 部分，色值换成 DS token。
     原版 JS 只做一件事：dynamicSpread = children.length * spread（spread 默认 2），
     写进 --spread 交给 CSS 算渐变带宽 —— 这里同样只写 --kb-shimmer-spread，
     让「高光带宽度随标题字数自适应」，而不是固定值。 */
  var SHIMMER_SPREAD = 2;
  function bindShimmer(wrap) {
    var titles = wrap.querySelectorAll('.kb-card-title');
    Array.prototype.forEach.call(titles, function (el) {
      var len = (el.textContent || '').length || 1;
      el.style.setProperty('--kb-shimmer-spread', (len * SHIMMER_SPREAD) + 'px');
    });
  }

"""

SUBS = [
    ('插入 shimmer CSS',
     """      .kb-crt-msgs .giencoder-message-icon { display: inline-flex; flex: none; color: var(--color-danger-6); }
</style>""",
     """      .kb-crt-msgs .giencoder-message-icon { display: inline-flex; flex: none; color: var(--color-danger-6); }
""" + SHIMMER_CSS + """</style>""",
     '@keyframes kb-title-shimmer {'),

    ('定义 bindShimmer',
     """  function inject() {
    var main = document.querySelector('main');""",
     SHIMMER_JS + """  function inject() {
    var main = document.querySelector('main');""",
     'function bindShimmer(wrap) {'),

    ('注册 bindShimmer',
     """    bindCreateModal(wrap);
    return true;
  }""",
     """    bindCreateModal(wrap);
    bindShimmer(wrap);
    return true;
  }""",
     'bindShimmer(wrap);'),
]

STABLE = [
    '<style>', '</style>', '<script>', '</script>',
    '.kb-card-title { color: var(--color-text-1); font-size: 14px; font-weight: 400; line-height: 22px; }',
    '.kb-card:hover .kb-card-title { font-weight: 500; }',
    '.kb-running { margin-left: auto;',
    'animation: kb-dash-run .7s linear infinite;',
]


def main():
    with io.open(P, encoding='utf-8') as f:
        before = f.read()
    src = before

    for label, old, new, mark in SUBS:
        if mark in src:
            print('[SKIP] %-18s MARK 已存在' % label)
            continue
        n = src.count(old)
        if n != 1:
            print('[FAIL] %-18s OLD 命中 %d 次（应为 1）→ 未写盘' % (label, n))
            return 1
        src = src.replace(old, new, 1)
        print('[OK]   %-18s 已替换' % label)

    fails = []
    for t in STABLE:
        if src.count(t) != before.count(t):
            fails.append('stable token %r 计数变化：%d → %d'
                         % (t[:48], before.count(t), src.count(t)))
    for label, old, new, mark in SUBS:
        c = src.count(mark)
        if c != 1:
            fails.append('MARK %r 出现 %d 次（应为 1）[%s]' % (mark[:32], c, label))
    # 兜底：--kb-shimmer-spread 的 20px 缺省档必须恰好 1 处
    if src.count('--kb-shimmer-spread: 20px;') != 1:
        fails.append('--kb-shimmer-spread: 20px 出现 %d 次（应为 1）'
                     % src.count('--kb-shimmer-spread: 20px;'))

    if fails:
        for x in fails:
            print('[FAIL]', x)
        print('!! 自检未通过，未写盘')
        return 1

    print('[OK] 自检通过：标签计数不变 / 既有规则计数不变 / 3 处 MARK 各 1 次')
    for t in STABLE:
        print('      %-58s %d' % (t[:58], src.count(t)))

    if src == before:
        print('      bytes %d（no-op）' % len(src.encode('utf-8')))
        print('ALL PASS (no-op)')
        return 0

    with io.open(P, 'w', encoding='utf-8') as f:
        f.write(src)
    print('      bytes %d → %d (Δ %+d)' % (len(before.encode('utf-8')),
                                           len(src.encode('utf-8')),
                                           len(src.encode('utf-8')) - len(before.encode('utf-8'))))
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
