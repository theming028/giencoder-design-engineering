#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r75 补丁 —— base.html：需求 7（补齐）基础工作台下拉/浮窗的显示·关闭动效。

本轮只改 base.html（用户确认范围）。三件事，全部纯 CSS、零脚本：
  A. 让设计系统自带的浮窗过渡真正起跑（关闭态的内联 display:none 让位给 visibility 隐藏）
  B. 「默认权限」自研浮层的进场（复用 r74-pop-in 关键帧）
  C. 冻结退场 ghost 里的克隆体：既修正它的定位（原先被顶出外壳、被 overflow 裁掉），
     也掐掉它会误播的进场动画（原先与外壳的淡出相乘后恒为 0 ⇒ 退场全程不可见）

幂等：NEW 标记命中即 SKIP；锚点 </body> count 必须为 1；跑完复跑应得「应用 0 页」。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'base.html')

MARK_STYLE = '<style id="r75-base-css">'
TAIL = '</body>'

CSS = """<style id="r75-base-css">
  /* ★ 第 75 轮 · 需求 7（补齐）：基础工作台的下拉浮窗补上「显示 / 关闭」动效。

     实测根因：设计系统本来就在 components 里为这类浮窗写好了过渡
     （关闭态 = 不透明 0 / 不可见 / 上移 4px / 缩放 0.96；
      打开态由 open 类切到不透明、归位、满标；两个方向各带一条过渡），
     但「过渡需要有上一帧已经渲染出来的起点」。而基础工作台里 React 给关闭态的
     浮窗又额外写了一条内联的 display:none（实测内联值就是 display: none;）
     ⇒ 元素从来没有被渲染过 ⇒ 打开的那一帧没有可插值的起点 ⇒ 整条过渡不启动
       （实测：getAnimations() 全程为空、首帧即到终值，进出两个方向都是硬跳）。

     修法：把内联 display:none 让位给设计系统自带的不可见态。
     浮窗本身是绝对定位、不占文档流；不可见元素既不接收指针事件、也不进无障碍树，
     因此观感与可访问性都等价 —— 唯一的差别是元素从此常驻渲染，
     设计系统原生过渡自然生效。

     参数一律沿用设计系统原生（打开 200ms + 弹性缓动、关闭 150ms），不另造数值：
     这样与「数字分身」页里同组件的浮窗逐帧同构
     （实测两者帧序列一致，含上移量轻微冲过 0 再回落的弹性特征）。 */
  .giencoder-select-popup {
    display: block !important;
  }

  /* ★ 第 75 轮 · 需求 7（补齐）：「默认权限」这个自研浮层的进场。
     它按需挂载（实测：打开才插入 DOM、关闭即被移除），自身只有一条无时长的
     transition ⇒ 完全没有动效。
     进场直接复用第 74 轮已定义的关键帧（与同页「添加内容」菜单、「技能选择」面板
     同一套参数）；退场由第 74 轮页尾的快照克隆机制接管 ——
     它的选择器本来就包含 listbox 角色，无需改动。 */
  [role="listbox"][aria-label="权限选择"] {
    animation: r74-pop-in 160ms cubic-bezier(0.34, 0.69, 0.1, 1) both;
  }

  /* ★ 第 75 轮 · 需求 7（补齐）修正：让退场快照（页尾那套克隆机制产的 ghost）真的看得见。

     实测两个叠加的缺陷：
       ① 定位 —— 被克隆的浮窗自带内联定位（如 bottom: calc(100% + 4px)、
          position: fixed; top: 41px; left: 133px），塞进 fixed 外壳后会重新解析：
          实测外壳 365,267,180x92 / 克隆体 368,177,175x89，被顶到外壳上方 90px，
          再被外壳的 overflow 裁掉 ⇒ 退场那一侧什么都没有。
       ② 动画 —— 克隆体带着同一份内联样式，会**再次命中本页的进场动画选择器**，
          于是在克隆体上播「淡入」、在外壳上又播「淡出」，两者相乘恒为 0
          ⇒ 即使定位正确也依然看不见（实测克隆体不透明度 0→0.24→…→1，
             外壳 1→0.76→…→0，同帧相乘全程 ≈0）。

     修法：快照里的内容一律「静止 + 铺满外壳」——它是定格画面，不该再有任何动效。
     用声明式 CSS 而不是脚本，可以保证它在克隆体插入的那一刻就已生效，
     不会先闪一帧错位/错动画。 */
  [data-r74-ghost] * {
    animation: none !important;
    transition: none !important;
  }
  [data-r74-ghost] > * {
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    right: auto !important;
    bottom: auto !important;
    margin: 0 !important;
    transform: none !important;
    width: 100% !important;
    height: 100% !important;
    max-height: none !important;
  }
</style>
"""

TOKENS = [
    '.giencoder-select-popup',
    '[role="listbox"][aria-label="权限选择"]',
    'r74-pop-in',
    'display: block !important',
    '[data-r74-ghost] *',
    '[data-r74-ghost] > *',
]


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    if MARK_STYLE in s:
        print('  SKIP  base.html 已含 r75 标记')
        print('应用: 0 页 | 跳过: 1 页')
        return

    if s.count(TAIL) != 1:
        sys.exit('!! 锚点异常：%s 出现 %d 次' % (TAIL, s.count(TAIL)))

    for dep, want in (('@keyframes r74-pop-in', 1), ('<style id="r74-base-css">', 1),
                      ('<script id="r74-base-js">', 1)):
        if s.count(dep) != want:
            sys.exit('!! 前置依赖异常：%s 出现 %d 次（期望 %d）' % (dep, s.count(dep), want))

    b_style, b_estyle = s.count('<style'), s.count('</style>')
    b_script, b_escript = s.count('<script'), s.count('</script>')

    i = s.rindex(TAIL)
    s2 = s[:i] + CSS + s[i:]

    checks = [
        ('<style> 增量', s2.count('<style') - b_style, 1),
        ('</style> 增量', s2.count('</style>') - b_estyle, 1),
        ('<script> 增量（应为 0）', s2.count('<script') - b_script, 0),
        ('</script> 增量（应为 0）', s2.count('</script>') - b_escript, 0),
        (MARK_STYLE, s2.count(MARK_STYLE), 1),
        ('@keyframes r74-pop-in', s2.count('@keyframes r74-pop-in'), 1),
        ('第 74 轮脚本块仍在', s2.count('<script id="r74-base-js">'), 1),
    ]
    for tok in TOKENS:
        checks.append((tok + ' 增量', s2.count(tok) - s.count(tok), CSS.count(tok)))

    for name, got, want in checks:
        if got != want:
            sys.exit('!! 自检失败 %s: 实得 %s（期望 %s）' % (name, got, want))
        print('  ok  %-44s = %s' % (name, got))

    io.open(PAGE, 'w', encoding='utf-8').write(s2)
    print('应用: 1 页 | 跳过: 0 页')


if __name__ == '__main__':
    main()
