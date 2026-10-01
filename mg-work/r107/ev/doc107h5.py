# -*- coding: utf-8 -*-
"""r107 第七拍 · 工作区顶层 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 补硬规则 35~37。
用法： python mg-work/r107/ev/doc107h5.py
"""
import io
import os
import sys

P = u'E:/GienCoder/.workbuddy/memory/MEMORY.md'

NEW = u"""35. ★★ **「用户说全局去掉某词」先给页面里的出现**分类**再动手**：① 渲染成页面文字的（文本节点 / `title`）**必改**；
    ② 外链 `href` / `src` 里的**不改**（替换域名段即 404，且本来就不渲染成页面文字）；③ 历史上写下的**设计来源注释保留**
    （那是后续维护者判断「照谁做的」的唯一线索）。判据配方 = `createTreeWalker(容器, SHOW_TEXT)` 数渲染文字 +
    遍历 `el.attributes`（**排除 `href`/`src`**）数属性。★ **顺手扫别的页**（r107 第七拍就在 `avatar.html` 会话列表里又挖到 1 处）；
    ★ **自己新增的注释要避开被清理的词** —— 否则「清理这件事」的文档本身又把它引入。
36. ★★ **同一处改动先判「节点从哪来」：静态 HTML vs JS 现场生成** —— r107 第七拍的下拉菜单标题行有两类来源
    （`.td-mm-cap` 是写死的 + `.td-ctx-head` 由 `ctxBuild()` 现场建的）⇒ **删 HTML 治不全**，
    正解 = **一段 CSS 把两类一起 `display:none`**（菜单是 `flex-direction: column` ⇒ 塌行不参与布局、与真删节点**视觉等价**）。
    ★ 同源推论：**联动显隐（「A 出现时隐藏 B」）先量「状态类挂在哪一级」** —— `.av-browse-on` 实测挂在 shell 的 flex 行上
    （`main` 与预览栏的**共同父级**），而按钮在 `main` 里 ⇒ 是它的**后代** ⇒ **纯 CSS 可判，省掉一整个 MutationObserver**。
    ⚠ 只写你要隐藏的那一枚（`[data-…]` 属性选择器），别用整组类名 —— 组里有几枚先数一遍。
37. ★★ **「统一某个属性（字体族 / 字号 / 描边）」要分清「本代自己的样式」与「跨代沿用的移植件」**（r107 第七拍）：
    本代样式**就地改**；落在**已交付的历史代**的移植件里的那条（本拍 = `mg-work/r102/part105/browse.css` 的 `.td-browse-pre`）
    **不回改历史代**，只能在页内**多一级类数覆盖**（`.td-browse .td-browse-pre`），子树靠继承。
    ★★ **判据要覆盖「整棵子树」，别只验自己改过的那些选择器** —— 本拍首轮只改了 8 条、量到「仍有 **153 个节点**落等宽」
    才顺藤摸到移植件。配方：`querySelectorAll(容器 + ' *')` 逐个比 `getComputedStyle`，
    并把不匹配的**按 `tagName + className` 分组**输出 ⇒ 一眼看出剩下的都挂在哪个父级上。

"""


def main():
    b = io.open(P, 'rb').read()
    t = b.decode('utf-8')
    anchor = u'\n## 二、Windows 环境速记'
    n = t.count(anchor)
    if n != 1:
        sys.exit(u'!! 锚点命中 %d 次（应 1 次）' % n)
    if u'35. ★★ ' in t:
        print(u'   已存在 35，跳过')
        return
    t = t.replace(anchor, u'\n' + NEW.rstrip('\n') + anchor, 1)
    io.open(P, 'wb').write(t.encode('utf-8'))
    print(u'   MEMORY.md %d → %d 字符' % (len(b.decode('utf-8')), len(t)))
    for k in [u'35. ★★ ', u'36. ★★ ', u'37. ★★ ', u'153 个节点']:
        print(u'     %s x %d' % (k, t.count(k)))


if __name__ == '__main__':
    main()
