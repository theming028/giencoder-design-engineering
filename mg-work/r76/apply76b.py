#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r76b 补丁 —— 只加强「需求 2」的波点涟漪（在 r76 已应用的终态上做二次加固）。

背景（实测）：r76 版涟漪虽然从内容之下提到了内容之上、点色也换到了 gray-9，
但取帧对比「基线 vs t=160ms」后发现：
  · 全画幅只有约 1036 个像素变化（>=6 灰阶），其中强变化(>=12) 835；
  · 差分图显示可见的只是一段很淡的月牙 —— 因为 mask 里真正「全不透明」的
    只有 r-18…r 这 18px（约 1 行点），其余全是 <=34% 的拖尾；
  · 观感上"看不出是一圈水波"。

本补丁不动时长（仍 300ms，守住 craft.md 的 UI 动画上限），只加大「单位面积对比」：
  ① 点径 1.5px → 1.8px，点色不透明度 0.42 → 0.62
     （gray-9 = 43,43,43 ⇒ 白底合成由 rgb(166) 压到 rgb(124)；
       底色 A 层波点是 gray-7 @ 0.1 ⇒ rgb(240)，对比从 Δ74 拉到 Δ116）；
  ② mask 由「峰核只有 18px」改为三段带：长尾 0.22 → 强肩 0.62 → 峰核 #000，
     峰核宽 32px（约 1.6 行点）+ 强肩 ~52px（约 2.6 行点）
     ⇒ 可见带宽由约 106px 放到约 190px，一次能看到 5~6 行点整齐地亮起；
  ③ 不透明度包络保持高位更久（62% 处仍 0.98），让环在扩散中段不早衰。

幂等：NEW 片段命中即 skip；OLD 片段 count 必须恰为 1，否则 sys.exit。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'base.html')

OLD_RIP = """  .r74-ripple {
    z-index: 10;
    --r76-rip-cap: 480px;
    background-image: radial-gradient(circle, rgba(var(--gray-9), 0.42) 1.5px, transparent 1.5px);
    background-size: 20px 20px;
    -webkit-mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 130px),
        rgba(0, 0, 0, 0.34) calc(var(--r74-rip-r) - 74px),
        transparent calc(var(--r74-rip-r) - 40px),
        #000 calc(var(--r74-rip-r) - 18px),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 16px));
    mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
        transparent calc(var(--r74-rip-r) - 130px),
        rgba(0, 0, 0, 0.34) calc(var(--r74-rip-r) - 74px),
        transparent calc(var(--r74-rip-r) - 40px),
        #000 calc(var(--r74-rip-r) - 18px),
        #000 var(--r74-rip-r),
        transparent calc(var(--r74-rip-r) + 16px));
    animation: r76-ripple-out 300ms linear both;
  }
  /* 波前用 linear 推进（缓动会在中段把半径一次推到接近终值，看不出「扩散」），
     分段关键帧只负责「先起、后收」的不透明度包络。 */
  @keyframes r76-ripple-out {
    0% {
      --r74-rip-r: 0px;
      opacity: 0;
    }
    7% {
      opacity: 1;
    }
    55% {
      --r74-rip-r: calc(var(--r76-rip-cap) * 0.62);
      opacity: 0.9;
    }
    100% {
      --r74-rip-r: var(--r76-rip-cap);
      opacity: 0;
    }
  }"""

NEW_RIP = """  .r74-ripple {
    z-index: 10;
    --r76-rip-cap: 480px;
    background-image: radial-gradient(circle, rgba(var(--gray-9), 0.62) 1.8px, transparent 1.8px);
    background-size: 20px 20px;
    -webkit-mask-image: radial-gradient(circle at var(--r74-rip-x, 50%) var(--r74-rip-y, 50%),
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
        transparent calc(var(--r74-rip-r) + 22px));
    animation: r76-ripple-out 300ms linear both;
  }
  /* 波前用 linear 推进（缓动会在中段把半径一次推到接近终值，看不出「扩散」），
     分段关键帧只负责「先起、后收」的不透明度包络。 */
  @keyframes r76-ripple-out {
    0% {
      --r74-rip-r: 0px;
      opacity: 0;
    }
    6% {
      opacity: 1;
    }
    62% {
      --r74-rip-r: calc(var(--r76-rip-cap) * 0.62);
      opacity: 0.98;
    }
    100% {
      --r74-rip-r: var(--r76-rip-cap);
      opacity: 0;
    }
  }"""

# 旧注释段（描述 r76 加强项）→ 新注释段（补记 r76b 的实测与再加强）
OLD_NOTE = """     元素本身仍由第 74 轮页尾脚本生成（它负责定位变量与播放结束自毁），
     这里只重置绘制，四处一起加强：
       ① 层级：由 0 提到 10。实测 main 内有非 auto 层级的后代只有 1000 / 9999 的弹层，
          故涟漪高于所有常规内容、仍低于弹层；
       ② 点色：灰阶由 gray-8 换到更深一档的 gray-9，不透明度同步微升 ——
          在卡片白底上也要看得清；
       ③ 环带：单薄前缘换成「波峰 + 尾迹」双带，可见带宽由 58px 放到约 106px；
       ④ 半径：上限由 360px 提到 480px（仍在 300ms 内推进 ⇒ 1.6px/ms，
          与原先 1.2px/ms 同量级，波前不会糊成一道闪光）。 */"""

NEW_NOTE = """     元素本身仍由第 74 轮页尾脚本生成（它负责定位变量与播放结束自毁），
     这里只重置绘制，四处一起加强：
       ① 层级：由 0 提到 10。实测 main 内有非 auto 层级的后代只有 1000 / 9999 的弹层，
          故涟漪高于所有常规内容、仍低于弹层；
       ② 点色：灰阶由 gray-8 换到更深一档的 gray-9；
       ③ 环带：单薄前缘换成「波峰 + 尾迹」双带；
       ④ 半径：上限由 360px 提到 480px（仍在 300ms 内推进 ⇒ 1.6px/ms，
          与原先 1.2px/ms 同量级，波前不会糊成一道闪光）。

     ⚠️ 二次加固（r76b）：上述四步之后取帧复核，发现真正「全不透明」的只有
        r-18…r 这 18px（约 1 行点），其余全是 ≤34% 的拖尾 ⇒ 观感还是一段很淡的
        月牙。故再压三点（时长仍守 300ms 不破 craft 上限）：
          · 点径 1.5→1.8px、点色 α 0.42→0.62 ⇒ 白底合成 rgb(166)→rgb(124)，
            对底色点阵（gray-7@0.1 ⇒ rgb(240)）的对比由 Δ74 拉到 Δ116；
          · mask 改「长尾 0.22 → 强肩 0.62 → 峰核 #000」，峰核 32px、
            强肩再铺约 52px ⇒ 可见带宽约 106→190px，一次亮起 5~6 行点；
          · 不透明度包络 62% 处仍留 0.98，环在中段不早衰。 */"""


def main():
    s = io.open(PAGE, encoding='utf-8').read()

    # 幂等三判
    # ⚠️ 「已应用」判据必须用**稳定标记**，不能整串匹配 NEW_RIP ——
    #    r76c 会把 NEW_RIP 里的 mask 段整段换掉 ⇒ 整串不再存在，
    #    若按整串判就会误判成「未应用」再去找 OLD_RIP（也不存在）而 sys.exit。
    #    'rgba(var(--gray-9), 0.62) 1.8px' 是 r76b 引入、r76c 保留的标记。
    RIP_MARK = 'rgba(var(--gray-9), 0.62) 1.8px'
    NOTE_MARK = '二次加固（r76b）'
    changed = False
    if RIP_MARK in s or NEW_RIP in s:
        print('  skip  base.html 涟漪加强  已应用')
    else:
        n = s.count(OLD_RIP)
        if n != 1:
            sys.exit('!! 锚点 OLD_RIP 出现 %d 次（期望 1）' % n)
        s = s.replace(OLD_RIP, NEW_RIP)
        changed = True
        print('  ok    base.html 涟漪 CSS   1 处')

    if NOTE_MARK in s or NEW_NOTE in s:
        print('  skip  base.html 涟漪注释  已应用')
    else:
        n = s.count(OLD_NOTE)
        if n != 1:
            sys.exit('!! 锚点 OLD_NOTE 出现 %d 次（期望 1）' % n)
        s = s.replace(OLD_NOTE, NEW_NOTE)
        changed = True
        print('  ok    base.html 涟漪注释  1 处')

    # 自检：只在「本次真的应用了」时跑 ——
    #   r76c 会把 r76b 的 mask 段换掉，故 NEW_RIP 专属的 token（如 - 168px）
    #   在「已应用 + 再被 r76c 覆盖」的终态里计数为 0，拿它做自检会误报。
    if changed:
        checks = [
            ('<style>', 1), ('</style>', 1),
            ('rgba(var(--gray-9), 0.62) 1.8px', 1),
            ('calc(var(--r74-rip-r) - 168px)', 2),
            ('opacity: 0.98;', 1),
            ('rgba(var(--gray-9), 0.42) 1.5px', 0),
            ('calc(var(--r74-rip-r) - 130px)', 0),
        ]
        old = io.open(PAGE, encoding='utf-8').read()
        for tok, want in checks[:2]:
            got = s.count(tok)
            if got != old.count(tok):
                sys.exit('!! 自检失败 %s：改前 %d → 改后 %d' % (tok, old.count(tok), got))
        for tok, want in checks[2:]:
            got = s.count(tok)
            if got != want:
                sys.exit('!! 自检失败 %s 计 %d（期望 %d）' % (tok, got, want))
        io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('应用完成 →', os.path.relpath(PAGE, ROOT))


if __name__ == '__main__':
    main()
