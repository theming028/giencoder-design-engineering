#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r76c 补丁 —— 修掉 r76b 涟漪 mask 的「前段退化成实心圆盘」问题。

现象（r76b 取帧实锤）：mask 的内缘用固定负偏移 calc(r - 168px)，
当 r < 168 时该值为负 → CSS 把负位置的 stop 钳到 0、最后一个负 stop（#000）胜出
⇒ 圆心到 r 之间全被填成不透明，取帧 t=100ms 看到的是**一大块暗点**（不是环）。

修法：内缘改成 max(比例 × r, r − 固定值) ——
  · 小 r 时走「比例」（内缘 = 0.40r），圆心永远留洞 ⇒ 一定是个环；
  · 大 r 时走「固定值」（内缘 = r − 156px），带宽被钉住 ⇒ 不会越扩越糊。
两条 max 分支的系数与偏移都单调递增 ⇒ 合成后的 6 个 stop 位置必然单调不降，CSS 合法。

顺带把峰值调亮一档（0.34 → 0.45 / 0.88），峰核由 18px 放到 30px。
时长不变（300ms）。幂等：NEW 命中即 skip，OLD 必须恰 1 次。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'base.html')

OLD_MASK = """    -webkit-mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 168px),
        rgba(0, 0, 0, 0.22) calc(var(--r74-rip-r) - 118px),
        rgba(0, 0, 0, 0.62) calc(var(--r74-rip-r) - 66px),
        #000 calc(var(--r74-rip-r) - 30px),
        #000 calc(var(--r74-rip-r) + 2px),
        transparent calc(var(--r74-rip-r) + 22px));
    mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 168px),
        rgba(0, 0, 0, 0.22) calc(var(--r74-rip-r) - 118px),
        rgba(0, 0, 0, 0.62) calc(var(--r74-rip-r) - 66px),
        #000 calc(var(--r74-rip-r) - 30px),
        #000 calc(var(--r74-rip-r) + 2px),
        transparent calc(var(--r74-rip-r) + 22px));"""

NEW_MASK = """    -webkit-mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent max(calc(var(--r74-rip-r) * 0.40), calc(var(--r74-rip-r) - 156px)),
        rgba(0, 0, 0, 0.45) max(calc(var(--r74-rip-r) * 0.62), calc(var(--r74-rip-r) - 96px)),
        rgba(0, 0, 0, 0.88) max(calc(var(--r74-rip-r) * 0.82), calc(var(--r74-rip-r) - 52px)),
        #000 max(calc(var(--r74-rip-r) * 0.90), calc(var(--r74-rip-r) - 30px)),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 20px));
    mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent max(calc(var(--r74-rip-r) * 0.40), calc(var(--r74-rip-r) - 156px)),
        rgba(0, 0, 0, 0.45) max(calc(var(--r74-rip-r) * 0.62), calc(var(--r74-rip-r) - 96px)),
        rgba(0, 0, 0, 0.88) max(calc(var(--r74-rip-r) * 0.82), calc(var(--r74-rip-r) - 52px)),
        #000 max(calc(var(--r74-rip-r) * 0.90), calc(var(--r74-rip-r) - 30px)),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 20px));"""

OLD_NOTE2 = """          · mask 改「长尾 0.22 → 强肩 0.62 → 峰核 #000」，峰核 32px、
            强肩再铺约 52px ⇒ 可见带宽约 106→190px，一次亮起 5~6 行点；
          · 不透明度包络 62% 处仍留 0.98，环在中段不早衰。 */"""

NEW_NOTE2 = """          · mask 改「尾 0.45 → 强肩 0.88 → 峰核 #000」，峰核 30px、
            强肩再铺约 44px ⇒ 一次亮起 4~5 行点；
          · 不透明度包络 62% 处仍留 0.98，环在中段不早衰。
          ⚠️ 但固定负偏移（r − 168px）在 r < 168 时会把内缘钳到 0 ⇒ 圆心被#000 填死、
            退化成**实心圆盘**（取帧 t=100ms 是一大块暗点，不是环）。故 r76c 把内缘换成
            max(比例 × r, r − 固定值)：小 r 走比例（内缘 = 0.40r，圆心恒留洞 ⇒ 必是环），
            大 r 走固定值（内缘 = r − 156px，带宽钉住 ⇒ 不会越扩越糊）。
            两分支的系数与偏移各自单调递增 ⇒ 6 个 stop 位置必单调不降，CSS 合法。 */"""


def main():
    s = io.open(PAGE, encoding='utf-8').read()

    if NEW_MASK in s:
        print('  skip  base.html 涟漪 mask 已应用')
    else:
        n = s.count(OLD_MASK)
        if n != 1:
            sys.exit('!! 锚点 OLD_MASK 出现 %d 次（期望 1）' % n)
        s = s.replace(OLD_MASK, NEW_MASK)
        print('  ok    base.html 涟漪 mask 1 处')

    if NEW_NOTE2 in s:
        print('  skip  base.html 涟漪注释 已应用')
    else:
        n = s.count(OLD_NOTE2)
        if n != 1:
            sys.exit('!! 锚点 OLD_NOTE2 出现 %d 次（期望 1）' % n)
        s = s.replace(OLD_NOTE2, NEW_NOTE2)
        print('  ok    base.html 涟漪注释 1 处')

    # 自检：新串计数；旧串不得残留；标签计数不变
    old = io.open(PAGE, encoding='utf-8').read()
    for tok, want in (('<style>', None), ('</style>', None),
                      ('max(calc(var(--r74-rip-r) * 0.40), calc(var(--r74-rip-r) - 156px))', 2),
                      ('calc(var(--r74-rip-r) - 168px)', 0),
                      ('rgba(0, 0, 0, 0.22) calc(var(--r74-rip-r) - 118px)', 0)):
        got = s.count(tok)
        if want is None:
            if got != old.count(tok):
                sys.exit('!! 自检失败 %s 计数变动：%d → %d' % (tok, old.count(tok), got))
        elif got != want:
            sys.exit('!! 自检失败 %s 计 %d（期望 %d）' % (tok, got, want))

    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('应用完成 →', os.path.relpath(PAGE, ROOT))


if __name__ == '__main__':
    main()
