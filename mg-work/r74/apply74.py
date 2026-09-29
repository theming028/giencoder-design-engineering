#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r74 补丁 A —— 需求 1（「新会话」按钮全局统一）+ 需求 6（顶栏左端两触发器互换位置）。

幂等三要素：
  1) 先判 NEW 标记：命中即 SKIP（整页跳过）
  2) 再判 OLD 锚点 count 必须恰好等于期望值，否则 sys.exit
  3) 跑完立刻复跑一次，应得「应用 0 页」

不做整文件关键词总数断言；只断言「被注入块自身」的精确计数与标签级增减量。
"""
import io
import os
import sys
import glob
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGES = os.path.join(ROOT, 'pages')

# ============================================================ 需求 1：新会话按钮
# 基础工作台（base.html）那枚按钮的图标 = 「对话气泡 + 加号」，路径从 base 内联 SVG 原样搬来。
BUBBLE_D = (
    "M6.9999694625,1.16638263702396C2.5948902625,1.1655892944575,-0.22168413750000004,"
    "5.8603582359375,1.8523447525,9.7466325359375L1.1663447954,12.8336328359375L"
    "4.253344762499999,12.1476318359375C6.1716055625,13.1720828359375,8.5004577625,"
    "13.0444838359375,10.2953119625,11.8165898359375C12.0901665625,10.5886964359375,"
    "13.0530225625,8.4643750359375,12.7933445625,6.3052568359375L11.6339695625,"
    "6.4435067359375C11.8425565625,8.1707658359375,11.0729198625,9.8706331359375,"
    "9.6373042625,10.8534574359375C8.2016901625,11.8362828359375,6.3385276625,"
    "11.9388338359375,4.8037197625,11.1195068359375L4.4222195625000005,10.9147567359375L"
    "2.7028446625,11.2971318359375L3.0852197625,9.5777559359375L2.8813447625,"
    "9.1971311359375C2.0084967625,7.5634498359375,2.1845213625,5.5681734359375,"
    "3.3299105625,4.1125438359375C4.4752995625,2.6569132359375,6.3731965625,"
    "2.0165240159374997,8.1663451625,2.4806316359375L8.4568452625,1.3501315759375C"
    "7.9808807625,1.2278544049375,7.4913902625,1.1661172103775,6.9999694625,1.16638263702396Z"
    "M10.6163453625,2.9163825359375L10.6163453625,1.4000076059375L11.7835955625,"
    "1.4000076059375L11.7835955625,2.9163825359375L13.2999695625,2.9163825359375L"
    "13.2999695625,4.0836327359375L11.7835945625,4.0836327359375L11.7835945625,"
    "5.6000075359375L10.6163444625,5.6000075359375L10.6163444625,4.0836327359375L"
    "9.0999698625,4.0836327359375L9.0999698625,2.9163825359375L10.6163453625,2.9163825359375Z"
    "M4.1999695625,5.0163824359374996L6.9999694625,5.0163824359374996L6.9999694625,"
    "6.1836319359375L4.1999695625,6.1836319359375L4.1999695625,5.0163824359374996Z"
    "M9.0999698625,7.4663825359375L4.1999695625,7.4663825359375L4.1999695625,8.6336321359375L"
    "9.0999698625,8.6336321359375L9.0999698625,7.4663825359375Z"
)
_uri_svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='-0.22 1.17 13.52 12.01'>"
            "<path d='%s' fill='#000'/></svg>") % BUBBLE_D
BUBBLE_URI = urllib.parse.quote(_uri_svg, safe="'/:,.-")

NC_SEL = 'button.giencoder-btn.giencoder-btn-secondary[class*="rounded-[8px]"][class*="mb-2"]'

NC_CSS = """<style id="r74-nc-css">
  /* ★ 第 74 轮 · 需求 1：「新会话」按钮全局统一为「基础工作台」的外观。
     基础工作台那枚按钮是 React 内联样式（半透明白底 / #E4E6EA 描边 / 内阴影 /
     左侧「对话气泡」图标 / 右侧 K 快捷键提示），其余页走 DS 组件类 —— 两者肉眼可辨。
     此处按基础工作台逐项复刻：底色 / 描边 / 阴影 / 内距 / 字号 / 图标 / 快捷键提示。
     ⚠️ 图标用 mask 画、不替换节点 —— React 重渲染冲不掉它。 */
  __SEL__ {
    position: relative;
    justify-content: center;
    gap: 0;
    padding: 0;
    height: 32px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid #E4E6EA;
    box-shadow: inset 0px 2px 2px 0px rgba(255, 255, 255, 0.9);
    /* ⚠️ 字号必须走 token（设计系统硬规则）—— --font-size-body-2 恰好 = 13px，
       与基础工作台那枚按钮的内联字号逐像素同值。 */
    font-size: var(--font-size-body-2);
    line-height: 20px;
    color: #1F1F1F;
    transition: background-color .15s ease;
  }
  __SEL__:hover {
    background: #FFFFFF !important;
  }
  /* 原图标（各页的「加号」）让位给 mask 画出来的对话气泡 */
  __SEL__ > svg {
    display: none;
  }
  __SEL__::before {
    content: '';
    flex: none;
    width: 14px;
    height: 14px;
    margin-right: 5px;
    background-color: #1F1F1F;
    -webkit-mask-image: url("data:image/svg+xml,__URI__");
    -webkit-mask-repeat: no-repeat;
    -webkit-mask-position: center;
    -webkit-mask-size: contain;
    mask-image: url("data:image/svg+xml,__URI__");
    mask-repeat: no-repeat;
    mask-position: center;
    mask-size: contain;
  }
  __SEL__::after {
    content: '\u2318K';
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    /* ⌘K 提示字号同理走 token（--font-size-body-3 = 14px，与设计稿一致） */
    font-size: var(--font-size-body-3);
    line-height: 1;
    color: #A9A9A9;
  }
</style>
""".replace('__SEL__', NC_SEL).replace('__URI__', BUBBLE_URI)

# ============================================================ 需求 6：顶栏两触发器互换
HEAD_CSS = """<style id="r74-head-css">
  /* ★ 第 74 轮 · 需求 6：顶栏左端「切换空间」与「切换侧边栏」互换位置，间隔线仍居中。
     mn 组件（顶栏左端那一坨）的结构恒为：
       div.relative > [ button(切换空间) , div(1x16 间隔线) , button(aria-label=切换侧边栏) ]
     直接改 DOM 顺序会踩 React 的协调；用 order 重排（只影响视觉顺序，不动 DOM）最稳：
       order 1 → 切换侧边栏   order 2 → 间隔线   order 3 → 切换空间
     ⚠️ 锚点用 aria-label="切换侧边栏" —— 它是恒定属性；
        另一个按钮的 ws-trigger-hover 类在下拉展开时会摘掉，不能当锚点。 */
  header div:has(> button[aria-label="切换侧边栏"]) > button[aria-label="切换侧边栏"] {
    order: 1;
  }
  header div:has(> button[aria-label="切换侧边栏"]) > div {
    order: 2;
  }
  header div:has(> button[aria-label="切换侧边栏"]) > button:not([aria-label="切换侧边栏"]) {
    order: 3;
  }
</style>
"""

NC_MARK = '<style id="r74-nc-css">'
HEAD_MARK = '<style id="r74-head-css">'
TAIL = '</body>'


def inject(html, block):
    """把 block 插到 </body> 之前（页面里 </body> 唯一）。"""
    n = html.count(TAIL)
    if n != 1:
        sys.exit('!! 锚点异常：</body> 出现 %d 次（期望 1）' % n)
    i = html.rindex(TAIL)
    return html[:i] + block + html[i:]


def main():
    applied, skipped = 0, 0
    for f in sorted(glob.glob(os.path.join(PAGES, '*.html'))):
        name = os.path.basename(f)
        s = io.open(f, encoding='utf-8').read()
        if NC_MARK in s or HEAD_MARK in s:
            skipped += 1
            print('  SKIP  %-20s 已含 r74 标记' % name)
            continue

        before_style = s.count('<style')
        payload = HEAD_CSS
        if name != 'base.html':
            payload = NC_CSS + HEAD_CSS

        s2 = inject(s, payload)

        after_style = s2.count('<style')
        want = 1 if name == 'base.html' else 2
        if after_style - before_style != want:
            sys.exit('!! %s: <style> 增量 %d（期望 %d）' % (name, after_style - before_style, want))
        if s2.count('</style>') - s.count('</style>') != want:
            sys.exit('!! %s: </style> 增量不符' % name)
        if s2.count(NC_MARK) != (0 if name == 'base.html' else 1):
            sys.exit('!! %s: r74-nc-css 计数异常' % name)
        if s2.count(HEAD_MARK) != 1:
            sys.exit('!! %s: r74-head-css 计数异常' % name)
        if name != 'base.html' and s2.count('r74-nc-css') != 1:
            sys.exit('!! %s: 需求 1 块计数异常' % name)

        io.open(f, 'w', encoding='utf-8').write(s2)
        applied += 1
        print('  OK    %-20s +%d style 块' % (name, want))

    print('应用: %d 页 | 跳过: %d 页' % (applied, skipped))


if __name__ == '__main__':
    main()
