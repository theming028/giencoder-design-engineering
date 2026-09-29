#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r76d 补丁 —— 压扁态下技能浮窗列表的「半行」收尾。

现象（1440×720 实拍）：max-height 生效后 .skill-pop-list 变成可滚动，
内容在半行处被切断，而这半行文字紧贴按钮条、透过半透明浮窗底
（rgba(255,255,255,0.88) + backdrop blur）透出来，像"串到按钮上"。

修法：给列表加一道底部渐隐 mask，**只在 max-height 真正生效的区间启用**
（max-height 开始生效的门槛 = 50vh − 120 < 320 ⇒ 视口高 < 880，
 故用 @media (max-height: 879px)）。自然高度下零影响。

范围：本选择器同时要求 `[aria-label="技能选择"]` 祖先 —— 该浮窗**只在 base.html 渲染**
（其余 8 页虽有 .skill-pop-list 的 CSS 拷贝，但无此 aria 节点），故不会波及其他页。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'base.html')

ANCHOR = """  [role="listbox"][aria-label="技能选择"][style*="position: absolute"] {
    max-height: calc(50vh - 120px);
  }
</style>
"""

NEW = """  [role="listbox"][aria-label="技能选择"][style*="position: absolute"] {
    max-height: calc(50vh - 120px);
  }
  /* 压扁后列表转为可滚，内容会在半行处被切断；浮窗底是半透明白 + 背景模糊，
     那半行文字会透出来、像是"串"到下方按钮条上。给列表补一道底部渐隐收口。
     ⚠️ 只在 max-height 真正生效的区间启用：其门槛 = 50vh − 120 < 320 ⇒ 视口高 < 880。
        自然高度下（≥880）这条完全不命中 ⇒ 零影响。
     选择器带 [aria-label="技能选择"] 祖先 —— 该浮窗只在 base.html 渲染，
     其余页面的 .skill-pop-list 拷贝不会被波及。 */
  @media (max-height: 879px) {
    [role="listbox"][aria-label="技能选择"] .skill-pop-list {
      -webkit-mask-image: linear-gradient(to bottom, #000 calc(100% - 30px), transparent 100%);
      mask-image: linear-gradient(to bottom, #000 calc(100% - 30px), transparent 100%);
    }
  }
</style>
"""


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    if '(max-height: 879px)' in s:
        print('  skip  base.html 列表收口 已应用')
        return
    if s.count(ANCHOR) != 1:
        sys.exit('!! 锚点 ANCHOR 出现 %d 次（期望 1）' % s.count(ANCHOR))
    b_style, b_estyle = s.count('<style'), s.count('</style>')
    s2 = s.replace(ANCHOR, NEW)
    if s2.count('<style') - b_style != 0 or s2.count('</style>') - b_estyle != 0:
        sys.exit('!! 自检失败：style 标签计数变动')
    if s2.count('mask-image: linear-gradient(to bottom, #000 calc(100% - 30px), transparent 100%)') != 2:
        sys.exit('!! 自检失败：mask 行数不符')
    io.open(PAGE, 'w', encoding='utf-8').write(s2)
    print('  ok    base.html 列表收口 1 处')
    print('应用完成 →', os.path.relpath(PAGE, ROOT))


if __name__ == '__main__':
    main()
